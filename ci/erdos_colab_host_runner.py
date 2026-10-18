#!/usr/bin/env python3
"""Host-side Colab launcher and evidence verifier for bounded Erdős #41 review.

Reuses the QTR/GSD google-colab-cli lifecycle (new/upload/exec/download/stop)
and existing Forge queue/source binding. The same authenticated GitHub operator
may staff logical reviewer roles; a Colab runtime never receives GH credentials.
No automatic issue publishing or claim promotion is authorized by this script.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

from ci.erdos_forge_copilot_pilot import (
    EVIDENCE_MARKER, PILOT_PROBLEM, REPO, ROSTER, comment_history,
    exact_existing, gh, prepare, review_ready, selected_record,
)

ROOT = Path(__file__).resolve().parents[1]
HOST = Path(__file__).resolve()
REMOTE = ROOT / "colab/erdos_024_remote_review.py"
SHA = re.compile(r"[a-f0-9]{40}\Z")
PROVENANCE = "GCL_ERDOS_COLAB_LOGICAL_REVIEW"
AUTHORITY = {
    "forge_source_semantics_accepted": False,
    "solve_dispatch_authorized": False,
    "mathcert_certified": False,
    "formal_publication": False,
    "protected_branch_mutation": False,
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def remote_module():
    spec = importlib.util.spec_from_file_location("gcl_erdos_remote_review", REMOTE)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def job_packet(task: bytes, prompt: bytes, *,
               backend: str, model_id: str | None,
               model_revision: str | None, max_new_tokens: int) -> dict:
    job = {"schema_version": 2, "kind": PROVENANCE,
           "cohort_id": "ERDOS-ROLLING-024-001",
           "problem_id": 41, "review_issue": 2536,
           "task_sha256": sha(task), "prompt_sha256": sha(prompt),
           "backend": backend, "model_id": model_id,
           "model_revision": model_revision, "max_new_tokens": max_new_tokens,
           "remote_source_sha256": sha(REMOTE.read_bytes()),
           "host_runner_source_sha256": sha(HOST.read_bytes())}
    remote_module().locked_inputs(task, prompt, job)
    return job


def verify_artifacts(directory: Path) -> dict:
    task_file = directory / "task.json"
    prompt_file = directory / "prompt.txt"
    job_file = directory / "job.json"
    receipt_file = directory / "erdos_review_receipt.json"
    result_file = directory / "erdos_review_result.json"
    task, prompt = task_file.read_bytes(), prompt_file.read_bytes()
    job = json.loads(job_file.read_text())
    remote = remote_module()
    remote.locked_inputs(task, prompt, job)
    receipt = json.loads(receipt_file.read_text())
    if receipt.get("status") != "GREEN_ENGINEERING":
        raise ValueError("Colab engine returned a failure receipt")
    if receipt.get("record_type") != "GCL_ERDOS_COLAB_LOGICAL_REVIEW_RECEIPT":
        raise ValueError("unexpected Colab review receipt kind")
    result = json.loads(result_file.read_text())
    if receipt.get("job_sha256") != sha(compact(job)):
        raise ValueError("changed job on remote runtime")
    if receipt.get("input_task_sha256") != sha(task) or receipt.get("input_prompt_sha256") != sha(prompt):
        raise ValueError("reviewed prompt/task not source-bound")
    if receipt.get("result_sha256") != sha(compact(result)):
        raise ValueError("Colab review result changed after execution")
    if (receipt.get("remote_source_sha256") != sha(REMOTE.read_bytes()) or
            result.get("remote_source_sha256") != sha(REMOTE.read_bytes())):
        raise ValueError("remote Colab source identity not attested")
    if (receipt.get("host_runner_source_sha256") != sha(HOST.read_bytes()) or
            result.get("host_runner_source_sha256") != sha(HOST.read_bytes())):
        raise ValueError("host Colab runner identity not attested")
    if receipt.get("authority_effects") != AUTHORITY or result.get("authority_effects") != AUTHORITY:
        raise ValueError("remote runtime tried to promote mathematical authority")
    if result.get("record_type") != "GCL_ERDOS_COLAB_LOGICAL_REVIEW_RESULT":
        raise ValueError("wrong evidence type")
    if result.get("source_comment_sha256") != json.loads(task)["source_comment_sha256"]:
        raise ValueError("original RESULT/1 digest not bound")
    if result.get("witness") != remote.finite_witness():
        raise ValueError("finite witness verification failed")
    passes = result.get("role_passes")
    if job["backend"] == "witness_only":
        if passes != [] or receipt.get("role_pass_count") != 0 or result.get("research_disposition") != "FINITE_WITNESS_ONLY_NOT_AI_REVIEW":
            raise ValueError("witness-only probe misrepresented as AI review")
    else:
        if not isinstance(passes, list) or len(passes) != 2 or receipt.get("role_pass_count") != 2:
            raise ValueError("missing the two substantive logical review passes")
        if result.get("research_disposition") != "LOGICAL_ROLE_FINDINGS_UNADJUDICATED":
            raise ValueError("review tried to claim acceptance")
        for role, record in zip(remote.ROLE_NAMES, passes):
            if (record.get("role"), record.get("mode"),
                record.get("subject_sha256"), record.get("reviewer_system_id")) != (
                role, "non_authoring_read_only", job["prompt_sha256"],
                job["model_id"] + "@" + job["model_revision"]):
                raise ValueError("reviewer pass provenance mismatch")
            remote.check_pass(record.get("finding"), role)
    return {"state": "GREEN_ENGINEERING_UNADJUDICATED",
            "subject": "ERDOS-024-41",
            "backend": job["backend"], "role_pass_count": len(passes),
            "task_sha256": sha(task), "prompt_sha256": sha(prompt),
            "result_sha256": receipt["result_sha256"],
            "authority_effects": AUTHORITY}


def write_status(directory: Path, state: str, detail: str) -> None:
    path = directory / "RUN_STATUS.json"
    try:
        value = json.loads(path.read_text()) if path.exists() else {}
    except json.JSONDecodeError:
        value = {}
    rows = value.get("history", [])
    rows.append({"state": state, "at": datetime.now(timezone.utc).isoformat(),
                 "detail": detail[:250]})
    value.update({"schema_version": 1, "record_type": "GCL_ERDOS_COLAB_RUN_STATUS",
                  "state": state, "history": rows, "authority_effects": AUTHORITY,
                  "terminal": state in ("GREEN", "RED")})
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def call(argv: list[str], trace: Path, *, deadline: int = 90) -> None:
    process = subprocess.run(argv, capture_output=True, text=True,
                             check=False, timeout=deadline)
    # Never retain raw CLI output because a provider could echo credentials.
    trace.write_text(json.dumps({"argv_operation": argv[2] if len(argv) > 2 else argv[0],
                                 "returncode": process.returncode,
                                 "output_sha256": sha((process.stdout + process.stderr).encode()),
                                 "output_bytes": len(process.stdout + process.stderr)}) + "\n")
    if process.returncode != 0:
        raise RuntimeError("Colab CLI operation failed: " + argv[2])


def colab_entry_source() -> str:
    return (
        "import runpy, sys\n"
        "worker = '/content/erdos_024_remote_review.py'\n"
        "sys.argv = [worker]\n"
        "try:\n"
        "    runpy.run_path(worker, run_name='__main__')\n"
        "except SystemExit as exc:\n"
        "    if exc.code not in (None, 0):\n"
        "        raise\n"
    )


def require_green_remote_receipt(path: Path) -> None:
    receipt = json.loads(path.read_text())
    if receipt.get("status") != "GREEN_ENGINEERING":
        error_type = str(receipt.get("error_type", "RemoteExecutionError"))[:80]
        error = str(receipt.get("error", "remote worker returned a failure receipt"))[:300]
        raise RuntimeError(f"Colab worker failed: {error_type}: {error}")


def colab_execute(folder: Path, args, session: str) -> None:
    cli = [args.colab, "--auth=oauth2"]
    active = False
    try:
        write_status(folder, "ALLOCATING", f"allocate {args.accelerator} runtime")
        alloc = cli + ["new", "-s", session]
        if args.accelerator != "CPU":
            alloc += ["--gpu", args.accelerator]
        call(alloc, folder / "colab-new.json")
        active = True
        entry = folder / "colab-entry.py"
        entry.write_text(colab_entry_source())
        for local, remote in [
            (folder / "task.json", "/content/erdos_task.json"),
            (folder / "prompt.txt", "/content/erdos_prompt.txt"),
            (folder / "job.json", "/content/erdos_job.json"),
            (REMOTE, "/content/erdos_024_remote_review.py"),
            (entry, "/content/erdos_colab_entry.py"),
        ]:
            call(cli + ["upload", "-s", session, str(local), remote],
                 folder / ("colab-upload-" + local.name + ".json"))
        write_status(folder, "RUNNING", "run fixed source-locked remote mathematical review")
        call(cli + ["exec", "-s", session, "-f", str(entry),
                    "--timeout", str(args.timeout)],
             folder / "colab-exec.json", deadline=args.timeout + 90)
        write_status(folder, "VERIFYING", "download authoritative receipt before result")
        receipt = folder / "erdos_review_receipt.json"
        call(cli + ["download", "-s", session,
                    "/content/erdos_review_receipt.json", str(receipt)],
             folder / "colab-download-erdos_review_receipt.json")
        require_green_remote_receipt(receipt)
        result = folder / "erdos_review_result.json"
        call(cli + ["download", "-s", session,
                    "/content/erdos_review_result.json", str(result)],
             folder / "colab-download-erdos_review_result.json")
    finally:
        if active:
            # A failed cleanup is not a successful terminal run.
            call(cli + ["stop", "-s", session], folder / "colab-stop.json")


def reserve_exact_job(root: Path, job: dict) -> Path:
    """One charge attempt per exact packet on this control host, including RED runs.

    No globally shared lock is claimed. A distributed host deployment needs its
    own persisted, atomic lease before unattended model execution is enabled.
    """
    ticket = root / (".attempted-" + sha(compact(job)))
    ticket.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(ticket, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "w") as handle:
        handle.write(datetime.now(timezone.utc).isoformat() + "\n")
    return ticket


def publish_provisional(directory: Path) -> dict:
    """Same authenticated host login; only an unadjudicated Forge issue comment.

    Only after independent source-bound, role-scoped model evidence exists.
    No GitHub reviewer identity separation or mathematical authority invented.
    """
    verification = verify_artifacts(directory)
    if verification["role_pass_count"] != 2 or verification["backend"] != "local_transformers":
        raise ValueError("not a substantive two-role AI critique")
    task = json.loads((directory / "task.json").read_text())
    result = json.loads((directory / "erdos_review_result.json").read_text())
    receipt = json.loads((directory / "erdos_review_receipt.json").read_text())
    row = selected_record(json.loads(ROSTER.read_text()))
    if row["source_critical_review_issue"] != 2536:
        raise ValueError("pilot docket has changed")
    source = gh(f"repos/{REPO}/issues/comments/{row['worker_result_comment_id']}")
    if sha((source.get("body") or "").encode()) != task["source_comment_sha256"]:
        raise ValueError("original worker return changed since reviewer execution")
    if source.get("issue_url") != f"https://api.github.com/repos/{REPO}/issues/{row['catalogue_issue']}":
        raise ValueError("source issue custody changed")
    review_id = row["source_critical_review_issue"]
    issue = gh(f"repos/{REPO}/issues/{review_id}")
    fields = gh(f"repos/{REPO}/issues/{review_id}/issue-field-values")
    comments = comment_history(review_id)
    allowed, reason = review_ready(issue, fields, comments)
    if not allowed:
        if reason == "CANDIDATE_EVIDENCE_ALREADY_SUBMITTED":
            prior = exact_existing(comments, EVIDENCE_MARKER)
            return {"state": "IDEMPOTENT_CANDIDATE_ALREADY_PRESENT",
                    "comment_url": prior[0].get("html_url") if len(prior) == 1 else None}
        raise ValueError("cannot publish candidate to changed queue: " + reason)
    body = (EVIDENCE_MARKER + "\n"
            + "COHORT_ID: ERDOS-ROLLING-024-001\n"
            + f"PROBLEM_ID: 41\nREVIEW_ISSUE: {review_id}\n"
            + f"SOURCE_COMMENT_ID: {row['worker_result_comment_id']}\n"
            + f"SOURCE_COMMENT_SHA256: {task['source_comment_sha256']}\n"
            + f"PROVIDER_BLOB: {task['protected_formal_source_blob']}\n"
            + f"RUNTIME: COLAB_LOCAL_TRANSFORMERS\n"
            + f"MODEL: {receipt['model_id']}\n"
            + f"PROMPT_SHA256: {verification['prompt_sha256']}\n"
            + f"RESULT_SHA256: {verification['result_sha256']}\n"
            + "AUTHENTICATION: SAME_EXISTING_GITHUB_OPERATOR\n"
            + "ROLE_SEPARATION: DISTINCT_LOGICAL_PASSES_NOT_PHYSICAL_IDENTITIES\n"
            + "STATUS: UNADJUDICATED_FORGE_PREPARATORY_EVIDENCE\n"
            + "FORGE_SOURCE_SEMANTICS_ACCEPTED: NO\n"
            + "MATHSOLVE_DISPATCH_AUTHORIZED: NO\n"
            + "MATHCERT_CERTIFIED: NO\n"
            + "FORMAL_PUBLICATION: NO\n\n"
            + "ROLE_FINDINGS_JSON:\n" + json.dumps(result["role_passes"], indent=2) + "\n\n"
            + "FINITE_WITNESS_JSON:\n" + json.dumps(result["witness"], sort_keys=True)
            + "\n\nNEXT: governed source-semantic review. No automatic Solve or Cert transition.\n")
    posted = subprocess.run(
        ["gh", "api", "--method", "POST", f"repos/{REPO}/issues/{review_id}/comments",
         "--input", "-"],
        input=json.dumps({"body": body}), text=True, capture_output=True,
        check=False, timeout=60)
    if posted.returncode:
        raise RuntimeError("authenticated Forge evidence comment rejected: " + posted.stderr[:200])
    comment = json.loads(posted.stdout)
    if not comment.get("id") or not comment.get("html_url"):
        raise RuntimeError("GitHub did not return an inspectable candidate receipt")
    receipt = {"state": "PROVISIONAL_COMMENT_PUBLISHED_NOT_CERTIFIED",
               "comment_id": comment["id"], "comment_url": comment["html_url"],
               "result_sha256": verification["result_sha256"], "authority_effects": AUTHORITY}
    (directory / "provisional-issue-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return receipt


def selftest() -> int:
    """No-network, no-Colab execution of the actual remote/host byte contract."""
    task = {"problem_id":41, "review_issue":2536,
            "cohort_id":"ERDOS-ROLLING-024-001",
            "source_comment_sha256":"a"*64,
            "protected_formal_source_sha256":"b"*64,
            "protected_formal_source_blob":"c"*40}
    with tempfile.TemporaryDirectory() as td:
        folder = Path(td)
        task_bytes = json.dumps(task, sort_keys=True).encode()
        prompt_bytes = b"Frozen synthetic offline proof-critic fixture; not a research result."
        job = job_packet(task_bytes, prompt_bytes,
                         backend="witness_only", model_id=None, model_revision=None,
                         max_new_tokens=0)
        result, receipt = remote_module().execute(task_bytes, prompt_bytes, job)
        (folder / "task.json").write_bytes(task_bytes)
        (folder / "prompt.txt").write_bytes(prompt_bytes)
        (folder / "job.json").write_text(json.dumps(job))
        (folder / "erdos_review_result.json").write_text(json.dumps(result))
        (folder / "erdos_review_receipt.json").write_text(json.dumps(receipt))
        output = verify_artifacts(folder)
        if output["role_pass_count"] != 0 or output["backend"] != "witness_only":
            raise RuntimeError("selftest falsely claims a model review")
        print(json.dumps({"state":"SELFTEST_GREEN_NO_COLAB_NO_MODEL",
                          "witness":result["witness"],
                          "authority_effects":AUTHORITY}))
        return 0


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true", help="no-network contract replay for governed CI")
    p.add_argument("--backend", choices=("witness_only", "local_transformers"),
                   default="witness_only")
    p.add_argument("--accelerator", choices=("CPU", "T4", "L4", "A100"),
                   default="CPU")
    p.add_argument("--model-id")
    p.add_argument("--model-revision")
    p.add_argument("--max-new-tokens", type=int, default=850)
    p.add_argument("--timeout", type=int, default=900)
    p.add_argument("--colab", default=str(Path.home() / ".local/bin/colab"))
    p.add_argument("--output-root", type=Path, default=ROOT / "runs/erdos-colab")
    p.add_argument("--execute", action="store_true",
                   help="Launch a real Colab session under existing operator authority")
    p.add_argument("--publish-provisional", action="store_true",
                   help="Post reviewed provisional evidence to existing GitHub issue, never certify")
    args = p.parse_args()
    if args.selftest:
        return selftest()
    if args.publish_provisional and (not args.execute or args.backend != "local_transformers"):
        p.error("only a genuinely executed two-role model review may publish provisional evidence")
    if not 60 <= args.timeout <= 3600:
        p.error("remote execution timeout must be 60-3600 seconds")
    if args.backend == "local_transformers" and args.accelerator == "CPU":
        p.error("explicit Colab GPU required for local model review")
    if args.backend == "local_transformers" and (
            not args.model_id or not args.model_revision or
            not re.fullmatch(r"[a-f0-9]{40}", args.model_revision)):
        p.error("explicit model repository and pinned 40-character commit required")
    if args.backend == "witness_only" and (args.model_id or args.model_revision):
        p.error("witness-only probe has no text-generation model")
    if args.backend == "local_transformers" and not args.execute:
        # Dry preparation is allowed but must still identify its exact remote model.
        if not args.model_id or not args.model_revision:
            p.error("model and commit required before any preparation")
    max_tokens = 0 if args.backend == "witness_only" else args.max_new_tokens
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    output = args.output_root / run_id
    output.mkdir(parents=True, exist_ok=False)
    write_status(output, "QUEUED", "prepare source-locked Forge candidate")
    try:
        prepared = prepare(
            output, model_run_identity="GCL_COLAB_LOGICAL_ROLE_PASSES",
            independence_claim="ROLE_SCOPED_PREPARATORY_NOT_CERT_INDEPENDENCE")
        if not prepared["ready"]:
            write_status(output, "RED", "queue not available: " + prepared["state"])
            print(json.dumps({"state":"NOT_READY", "reason":prepared["state"],
                              "run_dir":str(output)}))
            return 2
        task, prompt = (output / "task.json").read_bytes(), (output / "prompt.txt").read_bytes()
        job = job_packet(task, prompt, backend=args.backend,
                         model_id=args.model_id,
                         model_revision=args.model_revision,
                         max_new_tokens=max_tokens)
        (output / "job.json").write_text(json.dumps(job, indent=2, sort_keys=True) + "\n")
        if not args.execute:
            write_status(output, "PREPARED", "no Colab session or model started")
            print(json.dumps({"state":"PREPARED_ONLY_NOT_EXECUTED",
                              "run_dir":str(output),
                              "job_sha256":sha(compact(job)),
                              "authority_effects":AUTHORITY}))
            return 0
        if not Path(args.colab).is_file() and shutil.which(args.colab) is None:
            raise RuntimeError("Colab CLI missing on authorized control host")
        ticket = reserve_exact_job(args.output_root, job)
        session = "gcl-erdos41-" + uuid.uuid4().hex[:12]
        colab_execute(output, args, session)
        verified = verify_artifacts(output)
        from ci.erdos_41_colab_handoff import write_handoff
        intake_handoff = write_handoff(output, verified)
        report = publish_provisional(output) if args.publish_provisional else None
        write_status(output, "GREEN", "verified Colab receipt and role-scoped findings")
        print(json.dumps({**verified, "run_dir":str(output),
                          "one_shot_ticket":str(ticket),
                          "provisional_publication":report,
                          "intake_handoff":intake_handoff}))
        return 0
    except Exception as exc:
        write_status(output, "RED", type(exc).__name__ + ": " + str(exc))
        print("ERDOS_COLAB_HOST_BLOCKED: " + str(exc)[:300], file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
