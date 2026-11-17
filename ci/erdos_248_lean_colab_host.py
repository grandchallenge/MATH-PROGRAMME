#!/usr/bin/env python3
"""One-shot authenticated Colab launcher for pinned Erdős #248 Lean replay."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
JOB_ID = "ERDOS-0248-LEAN-REPLAY-001"
ISSUE = 3204
REPO = "grandchallenge/MATH-PROGRAMME"
TOOLCHAIN = "leanprover/lean4:v4.33.0"
# Bounded CPU duration accommodates expensive pinned formal-proof imports.
# Prior exact worker RED: lean-build exit 124 at 2400s, no Lean error.
MAX_RUNTIME_SECONDS = 15000
SOURCE = ROOT / "experiments/erdos_proof_verification/0248/Erdos248.lean"
WORKER = ROOT / "colab/erdos_248_lean_worker.py"
REGISTRY = ROOT / "governance/lean_colab/JOBS.json"
REMOTE_SOURCE = "/content/Erdos248.lean"
REMOTE_WORKER = "/content/erdos_248_lean_worker.py"
REMOTE_RECEIPT = "/content/erdos248_lean_receipt.json"
REMOTE_LOG_ARCHIVE = "/content/erdos248_lean_logs.tar.gz"

def digest(file):
    return hashlib.sha256(Path(file).read_bytes()).hexdigest()

def registered_identity():
    obj = json.loads(REGISTRY.read_text())
    matches = [r for r in obj["jobs"] if r.get("id") == JOB_ID]
    if len(matches) != 1:
        raise ValueError("missing/duplicate protected Erdos248 job")
    j = matches[0]
    if (j.get("review_issue"), j.get("problem_id"), j.get("toolchain"),
        j.get("authority"), j.get("accelerator"), j.get("launcher")) != (
            ISSUE, 248, TOOLCHAIN, "UNADJUDICATED_COMPUTATIONAL_EVIDENCE_ONLY",
            "CPU", "ci.erdos_248_lean_colab_host"):
        raise ValueError("protected identity or authority mismatch")
    if j.get("max_runtime_seconds") != MAX_RUNTIME_SECONDS:
        raise ValueError("protected CPU runtime budget mismatch")
    if j.get("source") != SOURCE.relative_to(ROOT).as_posix() or (
            j.get("worker") != WORKER.relative_to(ROOT).as_posix()):
        raise ValueError("protected source/worker path mismatch")
    if digest(SOURCE) != j.get("source_sha256") or digest(WORKER) != j.get("worker_sha256"):
        raise ValueError("source or worker SHA256 drift")
    return {"job": JOB_ID, "issue": ISSUE, "source_sha256": j["source_sha256"],
            "worker_sha256": j["worker_sha256"], "toolchain": TOOLCHAIN,
            "authority": "UNADJUDICATED_COMPUTATIONAL_EVIDENCE_ONLY"}

def project_available():
    q = """query {
      repository(owner:"grandchallenge",name:"MATH-PROGRAMME") {
        issue(number:3204) {
          state
          labels(first:30) { nodes { name } }
          projectItems(first:10) {
            nodes {
              project { number }
              fieldValues(first:40) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    name
                    field { ... on ProjectV2SingleSelectField { name } }
                  }
                }
              }
            }
          }
        }
      }
    }"""
    p = subprocess.run(["gh", "api", "graphql", "-f", "query=" + q],
                       text=True, capture_output=True, timeout=45, check=False)
    if p.returncode:
        raise RuntimeError("authenticated GitHub queue read failed: " + p.stderr[-350:])
    data = json.loads(p.stdout)
    if data.get("errors"):
        raise RuntimeError("Project query returned errors: " + str(data["errors"])[:200])
    issue = data["data"]["repository"]["issue"]
    labels = {l["name"] for l in issue["labels"]["nodes"]}
    if issue["state"] != "OPEN" or not {
            "gcl-job", "gcl-state:available", "gcl-role:verify"} <= labels:
        raise RuntimeError("Erdos248 queue issue not open/available")
    rows = [p for p in issue["projectItems"]["nodes"]
            if p["project"]["number"] == 2]
    if len(rows) != 1:
        raise RuntimeError("expected one Project #2 item")
    fields = {v["field"]["name"]: v["name"] for v in rows[0]["fieldValues"]["nodes"]
              if v.get("field") and v.get("name")}
    if fields.get("Status") != "Todo" or fields.get("Queue Class") != "Mathematics":
        raise RuntimeError("Project queue state changed: " + str(fields))
    return {"issue_state": issue["state"], "labels": sorted(labels),
            "project_fields": fields}

def cli(argv, timeout=75):
    p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
    if p.returncode:
        # Do not include auth material or command output in user-visible failures.
        raise RuntimeError("Colab CLI step failed: " + argv[2] + " exit=" + str(p.returncode))
    return p

def launch(colab, directory):
    session = "gcl-e248-lean-" + uuid.uuid4().hex[:12]
    prefix = [colab, "--auth=oauth2"]
    allocated = False
    error = None
    try:
        cli(prefix + ["new", "-s", session], timeout=100)
        allocated = True
        for source, remote in ((SOURCE, REMOTE_SOURCE), (WORKER, REMOTE_WORKER)):
            cli(prefix + ["upload", "-s", session, str(source), remote], timeout=150)
        script = directory / "launch.py"
        script.write_text(
            "import runpy,sys\n"
            "sys.argv=['/content/erdos_248_lean_worker.py']\n"
            "runpy.run_path('/content/erdos_248_lean_worker.py',run_name='__main__')\n"
        )
        try:
            cli(prefix + ["exec", "-s", session, "-f", str(script),
                          "--timeout", str(MAX_RUNTIME_SECONDS)],
                timeout=MAX_RUNTIME_SECONDS + 200)
        except Exception as exc:
            error = exc
        # Download the evidence even after a failed computation when possible.
        try:
            cli(prefix + ["download", "-s", session, REMOTE_RECEIPT,
                          str(directory / "receipt.json")], timeout=90)
            cli(prefix + ["download", "-s", session, REMOTE_LOG_ARCHIVE,
                          str(directory / "logs.tar.gz")], timeout=150)
        except Exception:
            if error is None:
                raise
        if error is not None:
            raise error
    finally:
        if allocated:
            cli(prefix + ["stop", "-s", session], timeout=75)

def validate_receipt(data, identity):
    if not isinstance(data, dict) or (
            data.get("schema"), data.get("job"), data.get("toolchain"),
            data.get("source_sha256"), data.get("worker_sha256")) != (
            "GCL-ERDOS-248-LEAN-REPLAY/1", JOB_ID, TOOLCHAIN,
            identity["source_sha256"], identity["worker_sha256"]):
        raise ValueError("receipt source/worker/toolchain identity mismatch")
    if data.get("authority_effects") != {
            "mathematical_certification": False, "publication": False,
            "protected_state_mutation": False, "source_adjudication": False}:
        raise ValueError("receipt claims unauthorized authority")
    if (data.get("status") != "GREEN_KERNEL_REPLAY_UNADJUDICATED" or
            not data.get("full_kernel_replay") or not data.get("axioms_observed") or
            not data.get("theorem_type_observed") or
            not data.get("theorem_audit_log_sha256") or
            not data.get("log_archive_sha256") or
            not any(token in data.get("axiom_report", "") for token in ("axioms used:", "depends on axioms:")) or
            "sorryAx" in data.get("axiom_report", "") or
            data.get("external_commit") !=
            "8822f7ddef30fadbd92e1c6ab4ed897af356af5e" or
            data.get("mathlib_commit") !=
            "db584cd6d46c92f209a44c0f1c829460d327499d"):
        raise ValueError("kernel/axiom replay not attested")
    if data.get("source_mode") != "PINNED_PROVIDER_WITH_DECLARED_COMPATIBILITY_PATCHES":
        raise ValueError("exact provider compatibility status missing")
    from colab.erdos_248_lean_worker import COMPATIBILITY_PATCHES, PINNED_DEPENDENCIES
    expected = [{"dependency": dep, "patch": filename, "git_blob": blob}
                for dep, filename, blob in COMPATIBILITY_PATCHES]
    if data.get("compatibility_patch_plan") != expected:
        raise ValueError("declared provider compatibility plan mismatch")
    effects = data.get("compatibility_patch_effects")
    if not isinstance(effects, dict) or set(effects) != set(PINNED_DEPENDENCIES):
        raise ValueError("missing patched dependency custody")
    for dep, sha in PINNED_DEPENDENCIES.items():
        row = effects[dep]
        if row.get("commit") != sha or not row.get("modified_files"):
            raise ValueError("patched dependency revision or files missing")
    bg = set(effects["BoundedGaps"]["modified_files"])
    if not {"BoundedGaps/BoundedGaps/Maynard/FaceDecomposition.lean",
            "BoundedGaps/BoundedGaps/Maynard/ImprovedGPY/S2Pair.lean"} <= bg:
        raise ValueError("failing module patch not attested")
    needed = {"git-fetch", "git-checkout", "lean-version",
              "mathlib-cache", "compat-post-update", "lean-build", "axiom-audit"}
    successful = {s.get("stage") for s in data.get("steps", [])
                  if s.get("exit_code") == 0}
    needed.update(f"compat-{index:02d}-{action}"
                  for index in range(9) for action in ("check", "apply"))
    if not needed <= successful:
        raise ValueError("missing successful exact replay stages")
    return True

def validate_log_archive(data, archive):
    """Compare complete Colab compiler outputs against source-bound receipt digests."""
    archive = Path(archive)
    if (not archive.is_file() or not data.get("log_archive_sha256") or
            digest(archive) != data["log_archive_sha256"] or
            archive.stat().st_size != data.get("log_archive_bytes")):
        raise ValueError("log archive digest/size mismatch")
    with tarfile.open(archive, mode="r:gz") as tar:
        names = tar.getnames()
        if len(names) != len(set(names)) or any(
                not (n.startswith("logs/") or n == "Erdos248ReplayAudit.lean")
                or ".." in n.split("/") for n in names):
            raise ValueError("unexpected log archive member")
        for step in data.get("steps", []):
            for kind in ("stdout", "stderr"):
                member = tar.extractfile("logs/" + step["stage"] +
                                         (".out" if kind == "stdout" else ".err"))
                if member is None:
                    raise ValueError("missing log for " + step["stage"])
                actual = hashlib.sha256(member.read()).hexdigest()
                if actual != step[kind + "_sha256"]:
                    raise ValueError("logged stage digest mismatch")
        source = tar.extractfile("Erdos248ReplayAudit.lean")
        if source is None or hashlib.sha256(source.read()).hexdigest() != data.get(
                "audit_source_sha256"):
            raise ValueError("theorem audit source digest mismatch")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--colab", default="colab")
    parser.add_argument("--output", type=Path, default=ROOT / "runs/erdos-248-lean")
    opts = parser.parse_args()
    identity = registered_identity()
    if opts.selftest:
        import unittest
        suite = unittest.TestLoader().loadTestsFromNames(
            ["tests.test_erdos_248_lean_colab_host", "tests.test_erdos_248_lean_colab"])
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            raise SystemExit(1)
        print(json.dumps({"state": "SELFTEST_GREEN_NO_COLAB", **identity}))
        return
    ready = project_available()
    if not opts.execute:
        print(json.dumps({"state": "PREFLIGHT_READY_NO_ALLOCATION",
                          **identity, "project": ready}))
        return
    opts.output.mkdir(parents=True, exist_ok=True)
    attempt = opts.output / (".attempted-" + identity["source_sha256"] +
                             "-" + identity["worker_sha256"])
    fd = os.open(attempt, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    directory = opts.output / ("run-" + uuid.uuid4().hex)
    directory.mkdir()
    try:
        launch(opts.colab, directory)
        receipt = json.loads((directory / "receipt.json").read_text())
        validate_receipt(receipt, identity)
        validate_log_archive(receipt, directory / "logs.tar.gz")
        print(json.dumps({"state": "VERIFIED_UNADJUDICATED",
                          "receipt_sha256": digest(directory / "receipt.json"),
                          "directory": str(directory), **identity}))
    except Exception as exc:
        print(json.dumps({"state": "RED_EVIDENCE_PRESERVED",
                          "error": type(exc).__name__ + ": " + str(exc)[:250],
                          "directory": str(directory), "attempt": str(attempt)}))
        raise

if __name__ == "__main__":
    main()
