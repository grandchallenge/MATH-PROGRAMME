#!/usr/bin/env python3
"""Erdos248 pinned, credential-free CPU Colab Lean replay. Evidence, not certification."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import os
import platform
import sys
import tarfile
import urllib.request
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

JOB = "ERDOS-0248-LEAN-REPLAY-001"
TOOLCHAIN = "leanprover/lean4:v4.33.0"
REPO = "https://github.com/plby/lean-proofs.git"
COMMIT = "8822f7ddef30fadbd92e1c6ab4ed897af356af5e"
MATHLIB = "db584cd6d46c92f209a44c0f1c829460d327499d"
SOURCE = "src/latest/ErdosProblems/Erdos248.lean"
SOURCE_BLOB = "166659f39a435831d1a751718f9a385effcd7dfa"
MANIFEST_BLOB = "1b7a0663de506f371211df75da206fa2c96befd2"
TOOLCHAIN_BLOB = "025e59548e48cf71f2744154e2890beefe30a258"
LAKEFILE_BLOB = "2a9bdb2fbef6ea320716b0341778f59507c15841"
AUTHORITY = {"mathematical_certification": False, "publication": False,
             "protected_state_mutation": False, "source_adjudication": False}
TIMEOUTS = {"git-init": 25, "git-fetch": 360, "git-checkout": 240,
            "lean-install": 240, "lean-version": 35,
            "mathlib-cache": 1500, "compat-post-update": 1200,
            "lean-build": 2400, "axiom-audit": 240}


# Exact compatibility set declared in the pinned external lakefile.lean.
COMPATIBILITY_PATCHES = (
    ("BoundedGaps", "formalpantheon-v4.33.0.patch", "ad5f8915e55205e15d4557958020d71314294d6e"),
    ("BoundedGaps", "formalpantheon-v4.33.0-s2.patch", "78471a0699e5669b3fa1baa676f5241133dc7e06"),
    ("BoundedGaps", "boundedgaps-linter-v4.33.0.patch", "ed5fb157c1564b865fe85ac2c7ffda31faa7d1a8"),
    ("AINTLIB", "aintlib-v4.33.0.patch", "e02a679298d785fa4e0af18e531356ba4fdacf02"),
    ("AINTLIB", "hasseweil-linter-v4.33.0.patch", "de07708b124f4a5704d16acb0c467b47a62fd8e3"),
    ("AINTLIB", "chebotarev-linter-v4.33.0.patch", "0a719f3a6b416c8e7465c627516f959b040c7550"),
    ("AINTLIB", "dedekind-flt-linter-v4.33.0.patch", "b2c5a35010b0087842674ce646d0e97306693cb1"),
    ("leancert", "leancert-linter-v4.33.0.patch", "f2c9e2e2f4186c7fb4b1c2edf4fefe8ebf780b1d"),
    ("Waring", "waring-linter-v4.33.0.patch", "981c78d177d2f819b7115451dc57e86aa4035e0a"),
)
PINNED_DEPENDENCIES = {
    "BoundedGaps": "ffbb65c21afc8a36ace67720f1b0df1c63d26bd1",
    "Waring": "ffbb65c21afc8a36ace67720f1b0df1c63d26bd1",
    "AINTLIB": "1c1c74664e40071c2c2165bc55ca2616a67ccd6b",
    "leancert": "7486c107f7c2ce814d0914a5f82f7f157ff8bb57",
}

ELAN_ARCHIVE_SHA256 = "42b94d4244e8353142c456ec0e4ca6528fd898a6c604d4059f494e706e431f63"
ELAN_RELEASE_URL = ("https://github.com/leanprover/elan/releases/download/v4.2.4/"
                    "elan-x86_64-unknown-linux-gnu.tar.gz")

def provision_elan():
    """Pinned elan archive bootstrap, never generic curl|sh."""
    existing = shutil.which("elan")
    if existing:
        return existing
    if sys.platform != "linux" or platform.machine().lower() not in ("x86_64", "amd64"):
        raise RuntimeError("unsupported pinned elan bootstrap platform")
    req = urllib.request.Request(ELAN_RELEASE_URL, headers={"User-Agent": "gcl-lean-replay/1"})
    with urllib.request.urlopen(req, timeout=50) as response:
        archive_bytes = response.read(8_000_001)
    if (len(archive_bytes) > 8_000_000 or
            hashlib.sha256(archive_bytes).hexdigest() != ELAN_ARCHIVE_SHA256):
        raise ValueError("elan installer release digest mismatch")
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
        members = tar.getmembers()
        if len(members) != 1 or members[0].name != "elan-init" or not members[0].isfile():
            raise ValueError("unexpected pinned elan archive layout")
        exe_bytes = tar.extractfile(members[0]).read()
    with tempfile.TemporaryDirectory(prefix="gcl-erdos248-elan-") as directory:
        exe = Path(directory) / "elan-init"
        exe.write_bytes(exe_bytes)
        exe.chmod(0o700)
        out = subprocess.run([str(exe), "-y", "--no-modify-path",
                              "--default-toolchain", TOOLCHAIN],
                             capture_output=True, text=True, timeout=200)
        if out.returncode:
            raise RuntimeError("pinned elan installation failed with " + str(out.returncode))
    elan = Path.home() / ".elan" / "bin" / "elan"
    if not elan.is_file():
        raise RuntimeError("pinned elan installer missing output")
    return str(elan)

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(argv, cwd, logdir, stage, timeout):
    if not isinstance(argv, list) or not argv or not all(isinstance(a, str) for a in argv):
        raise ValueError("invalid argv")
    out, err = logdir / (stage + ".out"), logdir / (stage + ".err")
    started = time.monotonic()
    try:
        with out.open("wb") as fo, err.open("wb") as fe:
            proc = subprocess.run(argv, cwd=cwd, stdout=fo, stderr=fe,
                                  timeout=timeout, check=False, env=os.environ.copy())
        rc = proc.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    record = {"stage": stage, "argv": argv, "exit_code": rc,
              "elapsed_seconds": round(time.monotonic() - started, 3),
              "stdout_sha256": sha256(out), "stderr_sha256": sha256(err),
              "stdout_bytes": out.stat().st_size, "stderr_bytes": err.stat().st_size,
              "stdout_tail": out.read_bytes()[-3000:].decode("utf-8", "replace"),
              "stderr_tail": err.read_bytes()[-3000:].decode("utf-8", "replace")}
    if rc != 0:
        raise RuntimeError("stage " + stage + " failed exit=" + str(rc) +
                           " stderr=" + record["stderr_tail"][-800:])
    return record

def git_blob(path):
    result = subprocess.run(["git", "hash-object", str(path)], capture_output=True,
                            text=True, timeout=30, check=True)
    return result.stdout.strip()

def verify_provider_patch_locks(project):
    """Fail closed unless the declared immutable provider post-update set matches."""
    lake = (project / "lakefile.lean").read_text(encoding="utf-8")
    if "post_update pkg do" not in lake or git_blob(project / "lakefile.lean") != LAKEFILE_BLOB:
        raise ValueError("provider post_update hook or pinned lakefile missing")
    manifest = json.loads((project / "lake-manifest.json").read_text())
    for dep, sha in PINNED_DEPENDENCIES.items():
        revs = [p["rev"] for p in manifest["packages"] if p.get("name") == dep]
        if revs != [sha]:
            raise ValueError("pinned dependency manifest drift for " + dep)
    entries = []
    for dep, name, expected in COMPATIBILITY_PATCHES:
        if ('("' + dep + '", "' + name + '")') not in lake:
            raise ValueError("undeclared compatibility patch " + name)
        patch = project / "patches" / name
        actual = git_blob(patch)
        if actual != expected:
            raise ValueError("provider compatibility patch blob drift: " + name)
        entries.append({"dependency": dep, "patch": name, "git_blob": actual})
    return entries


def verify_provider_post_update(project):
    """Require the pinned provider hook to change only declared Lean files."""
    result = {}
    for dep, sha in PINNED_DEPENDENCIES.items():
        root = project / ".lake" / "packages" / dep
        actual = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True,
            timeout=25).strip()
        if actual != sha:
            raise ValueError("post-update dependency HEAD drift: " + dep)
        changed = subprocess.check_output(
            ["git", "-C", str(root), "diff", "--name-only"], text=True,
            timeout=35).splitlines()
        if not changed or any(
                not file.endswith(".lean") or file.startswith("/") or
                ".." in Path(file).parts for file in changed):
            raise ValueError("missing or unexpected provider patch effects: " + dep)
        check = subprocess.run(["git", "-C", str(root), "diff", "--check"],
                               capture_output=True, text=True, timeout=35)
        if check.returncode:
            raise ValueError("provider patch diff check failed: " + dep)
        result[dep] = {"commit": actual, "modified_files": sorted(changed)}
    bg = set(result["BoundedGaps"]["modified_files"])
    if not {
        "BoundedGaps/BoundedGaps/Maynard/FaceDecomposition.lean",
        "BoundedGaps/BoundedGaps/Maynard/ImprovedGPY/S2Pair.lean"
    } <= bg:
        raise ValueError("known BoundedGaps failing modules not patched")
    if git_blob(project / "lake-manifest.json") != MANIFEST_BLOB:
        raise ValueError("Lake manifest drift after compatibility hook")
    return result


def validate_axiom_output(text):
    # Lean 4 prints "'theorem' depends on axioms: [..]"; tolerate older emitters.
    match = re.search(r"(?m)^.*(?:depends on axioms:|axioms used:)\s*\[[^\]]*\]", text)
    if match is None:
        raise ValueError("no observed #print axioms output")
    if re.search(r"\bsorryAx\b|\b(?:admit|sorry)\b", match.group(0)):
        raise ValueError("forbidden sorry/admit appears in axiom audit")
    if "Erdos248.erdos_248" not in text:
        raise ValueError("missing named final theorem in audit output")
    return match.group(0)[:1200]

def perform(source, worker, receipt, workdir):
    source, worker, receipt, workdir = map(Path, (source, worker, receipt, workdir))
    workdir.mkdir(parents=True, exist_ok=True)
    logdir = workdir / "logs"
    logdir.mkdir(exist_ok=True)
    started = time.monotonic()
    data = {"schema": "GCL-ERDOS-248-LEAN-REPLAY/1", "job": JOB, "status": "RED",
            "toolchain": TOOLCHAIN, "external_commit": COMMIT, "source_blob": SOURCE_BLOB,
            "mathlib_commit": MATHLIB, "source_sha256": sha256(source),
            "worker_sha256": sha256(worker), "authority_effects": AUTHORITY, "steps": [],
            "full_kernel_replay": False, "axioms_observed": False}
    try:
        if sha256(source) != data["source_sha256"]:
            raise ValueError("staged source changed before launch")
        repo = workdir / "provider"
        data["steps"].append(run(["git", "init", str(repo)], workdir, logdir,
                                 "git-init", TIMEOUTS["git-init"]))
        data["steps"].append(run(["git", "remote", "add", "origin", REPO], repo, logdir,
                                 "git-remote", 20))
        data["steps"].append(run(["git", "sparse-checkout", "init", "--cone"], repo,
                                 logdir, "git-sparse-init", 30))
        data["steps"].append(run(["git", "sparse-checkout", "set", "src/latest"], repo,
                                 logdir, "git-sparse-set", 30))
        data["steps"].append(run(["git", "fetch", "--depth=1", "--no-tags",
                                  "--filter=blob:none", "origin", COMMIT], repo, logdir,
                                 "git-fetch", TIMEOUTS["git-fetch"]))
        data["steps"].append(run(["git", "checkout", "--detach", "FETCH_HEAD"], repo,
                                 logdir, "git-checkout", TIMEOUTS["git-checkout"]))
        actual = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo,
                                         text=True, timeout=20).strip()
        if actual != COMMIT:
            raise ValueError("external checkout not pinned")
        project = repo / "src/latest"
        for relative, expected in ((SOURCE, SOURCE_BLOB),
                                   ("src/latest/lake-manifest.json", MANIFEST_BLOB),
                                   ("src/latest/lean-toolchain", TOOLCHAIN_BLOB),
                                   ("src/latest/lakefile.lean", LAKEFILE_BLOB)):
            actual_blob = git_blob(repo / relative)
            if actual_blob != expected:
                raise ValueError("protected external Git blob mismatch: " + relative)
        if (project / "lean-toolchain").read_text().strip() != TOOLCHAIN:
            raise ValueError("provider Lean pin differs")
        if (project / "ErdosProblems/Erdos248.lean").read_bytes() != source.read_bytes():
            raise ValueError("host-staged theorem differs from checked-out provider")
        manifest = json.loads((project / "lake-manifest.json").read_text())
        found = [entry["rev"] for entry in manifest["packages"]
                 if entry.get("name") == "mathlib"]
        if found != [MATHLIB]:
            raise ValueError("mathlib lock mismatch")
        elan = provision_elan()
        data["steps"].append(run([elan, "toolchain", "install", TOOLCHAIN], project,
                                 logdir, "lean-install", TIMEOUTS["lean-install"]))
        v = run([elan, "run", TOOLCHAIN, "lean", "--version"], project,
                logdir, "lean-version", TIMEOUTS["lean-version"])
        data["steps"].append(v)
        if not re.search(r"Lean \(version 4\.33\.0(?:,|\))", v["stdout_tail"]):
            raise ValueError("Lean runtime version mismatch")
        data["steps"].append(run([elan, "run", TOOLCHAIN, "lake", "exe", "cache", "get"], project, logdir,
                                 "mathlib-cache", TIMEOUTS["mathlib-cache"]))
        mathlib_path = project / ".lake/packages/mathlib"
        actual_mathlib = subprocess.check_output(["git", "-C", str(mathlib_path),
                                                  "rev-parse", "HEAD"], text=True,
                                                 timeout=25).strip()
        if actual_mathlib != MATHLIB:
            raise ValueError("downloaded mathlib revision mismatch")
        # Original replay failed because the pinned provider's compatibility
        # hook had never executed before compilation. Run that exact hook.
        data["compatibility_patch_plan"] = verify_provider_patch_locks(project)
        # Execute precisely the provider post_update hook's nine pinned
        # git-apply operations in declaration order. A generic lake update
        # regenerates lake-manifest.json, violating the source lock even when
        # all nine compatibility patches themselves succeed.
        for index, (dep, name, _blob) in enumerate(COMPATIBILITY_PATCHES):
            dependency = project / ".lake" / "packages" / dep
            patch_file = project / "patches" / name
            data["steps"].append(run(
                ["git", "apply", "--check", str(patch_file)],
                dependency, logdir, f"compat-{index:02d}-check", 60))
            data["steps"].append(run(
                ["git", "apply", str(patch_file)],
                dependency, logdir, f"compat-{index:02d}-apply", 60))
        data["steps"].append(run(
            ["git", "-C", str(project / ".lake" / "packages" / "BoundedGaps"),
             "diff", "--check"],
            project, logdir, "compat-post-update", 60))
        data["compatibility_patch_effects"] = verify_provider_post_update(project)
        data["source_mode"] = "PINNED_PROVIDER_WITH_DECLARED_COMPATIBILITY_PATCHES"
        data["steps"].append(run([elan, "run", TOOLCHAIN, "lake", "build", "ErdosProblems.Erdos248"], project,
                                 logdir, "lean-build", TIMEOUTS["lean-build"]))
        # A separate read-only audit proves the exact imported declaration type,
        # independent of merely finding a #print command in external source.
        audit = workdir / "Erdos248ReplayAudit.lean"
        audit.write_text(
            "import ErdosProblems.Erdos248\n"
            "#check Erdos248.erdos_248\n"
            "#print axioms Erdos248.erdos_248\n"
        )
        data["audit_source_sha256"] = sha256(audit)
        data["steps"].append(run([elan, "run", TOOLCHAIN, "lake", "env", "lean",
                                  str(audit)], project, logdir,
                                 "axiom-audit", TIMEOUTS["axiom-audit"]))
        output = (logdir / "axiom-audit.out").read_text(errors="replace")
        data["axiom_report"] = validate_axiom_output(output)
        data["axioms_observed"] = True
        if not re.search(r"Erdos248\.erdos_248\s*:\s*(?:∃|Exists)", output):
            raise ValueError("no observed theorem type in Lean #check output")
        data["theorem_type_observed"] = True
        data["theorem_audit_log_sha256"] = sha256(logdir / "axiom-audit.out")
        if git_blob(project / "lake-manifest.json") != MANIFEST_BLOB:
            raise ValueError("Lake manifest drift after build")
        if git_blob(project / "ErdosProblems/Erdos248.lean") != SOURCE_BLOB:
            raise ValueError("provider source drift after build")
        data["full_kernel_replay"] = True
        data["status"] = "GREEN_KERNEL_REPLAY_UNADJUDICATED"
    except Exception as exc:
        data["error"] = type(exc).__name__ + ": " + str(exc)[:1500]
    finally:
        # Retain complete compiler output across destructive Colab teardown.
        # Never archive the provider checkout, tokens, credentials, or caches.
        receipt.parent.mkdir(parents=True, exist_ok=True)
        archive = receipt.parent / "erdos248_lean_logs.tar.gz"
        try:
            with tarfile.open(archive, mode="w:gz") as tar:
                for path in sorted(logdir.glob("*")):
                    if path.is_file():
                        tar.add(path, arcname="logs/" + path.name)
                audit = workdir / "Erdos248ReplayAudit.lean"
                if audit.is_file():
                    tar.add(audit, arcname="Erdos248ReplayAudit.lean")
            data["log_archive_sha256"] = sha256(archive)
            data["log_archive_bytes"] = archive.stat().st_size
        except Exception as exc:
            data["status"] = "RED"
            data["archive_error"] = type(exc).__name__ + ": " + str(exc)[:400]
        data["elapsed_seconds"] = round(time.monotonic() - started, 3)
        receipt.parent.mkdir(parents=True, exist_ok=True)
        receipt.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    return 0 if data["status"] == "GREEN_KERNEL_REPLAY_UNADJUDICATED" else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="/content/Erdos248.lean")
    parser.add_argument("--worker", default="/content/erdos_248_lean_worker.py")
    parser.add_argument("--receipt", default="/content/erdos248_lean_receipt.json")
    parser.add_argument("--workdir", default="/content/gcl-erdos248-work")
    opts = parser.parse_args()
    raise SystemExit(perform(opts.source, opts.worker, opts.receipt, opts.workdir))
