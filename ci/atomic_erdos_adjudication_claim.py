#!/usr/bin/env python3
"""Atomic per-issue adjudication claim and guarded worker lifecycle.

A GitHub create-ref is the linearization point: only one contender can create
refs/heads/gcl-adjudication-claims/issue-N. Never steal or auto-expire a claim.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import uuid

REPO = "grandchallenge/MATH-PROGRAMME"
PREFIX = "refs/heads/gcl-adjudication-claims/issue-"
CHECKPOINT_SCHEMA = "gcl.adjudication-claim-checkpoint.v1"

OUTCOME_SUBSTANTIVE = "SUBSTANTIVE_ADJUDICATION"
OUTCOME_READ_ONLY = "READ_ONLY_COMPLETION"
OUTCOME_EXCLUSIVE_BLOCK = "EXCLUSIVE_CLAIM_BLOCK"
OUTCOME_FAILED_CLOSURE = "FAILED_CLOSURE"

EXIT_OK = 0
EXIT_INELIGIBLE = 2
EXIT_ALREADY_ADJUDICATED = 3
EXIT_NOT_ACQUIRED = 4
EXIT_ABORT_EXISTING = 5
EXIT_ERROR = 6
EXIT_STALE_CUSTODY_HOLD = 7
EXIT_FAILED_CLOSURE = 8


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def api(method, path, fields=None):
    cmd = ["gh", "api", "--method", method, f"repos/{REPO}/{path}"]
    if fields is not None:
        cmd += ["--input", "-"]
    result = subprocess.run(
        cmd,
        input=json.dumps(fields) if fields is not None else None,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout) if result.stdout.strip() else {}


def current_actor():
    return subprocess.run(
        ["gh", "api", "user", "--jq", ".login"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def comments(issue):
    # GitHub REST pagination: never rely on first page or search results.
    cmd = [
        "gh",
        "api",
        "--paginate",
        "--slurp",
        f"repos/{REPO}/issues/{issue}/comments?per_page=100",
    ]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    pages = json.loads(result.stdout)
    return [c for page in pages for c in page], len(pages)


def adjudications(items, assignment_id=None):
    if assignment_id is not None and not re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9_.-]{2,127}", assignment_id
    ):
        raise ValueError("invalid assignment ID")
    matches = [
        {"id": c["id"], "url": c.get("html_url")}
        for c in items
        if any(
            s in (c.get("body") or "").lower()
            for s in (
                "source-critical adjudication",
                "source critical adjudication",
                "adjudication disposition",
                "adjudication/1",
            )
        )
    ]
    if assignment_id is None:
        return matches
    # A cohort issue contains many independent per-problem assignments.
    # A different, explicitly identified assignment is not a duplicate.
    # Ambiguous adjudication without ASSIGNMENT_ID remains blocking.
    selected = []
    for c in items:
        if not any(
            s in (c.get("body") or "").lower()
            for s in (
                "source-critical adjudication",
                "source critical adjudication",
                "adjudication disposition",
                "adjudication/1",
            )
        ):
            continue
        found = re.findall(r"(?im)^ASSIGNMENT_ID:\s*([^\s]+)", c.get("body") or "")
        if len(found) != 1 or found[0] == assignment_id:
            selected.append({"id": c["id"], "url": c.get("html_url")})
    return selected


def is_ref_conflict_error(exc):
    text = str(exc).lower()
    return "422" in text or "reference already exists" in text


def is_not_found_error(exc):
    text = str(exc).lower()
    return "404" in text or "not found" in text


def write_checkpoint(path, record):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(record)
    payload["updated_at_utc"] = utc_now()
    tmp = target.with_name(f".{target.name}.{os.getpid()}.{uuid.uuid4().hex}.tmp")
    data = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    with tmp.open("w", encoding="utf-8") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, target)
    return payload


def read_checkpoint(path):
    target = Path(path)
    if not target.exists():
        return None
    raw = target.read_text(encoding="utf-8")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("checkpoint must be a JSON object")
    return data


def is_checkpoint_unclosed(record):
    if record is None:
        return False
    return record.get("phase") != "CLOSED" or bool(record.get("claim_still_held"))


def release_owned_claim(ref, claim_sha):
    current = api("GET", "git/ref/" + ref.removeprefix("refs/"))
    live_sha = current["object"]["sha"]
    if live_sha != claim_sha:
        raise RuntimeError(
            f"claim SHA mismatch; refusing release (expected={claim_sha}, observed={live_sha})"
        )
    # Release only after durable adjudication readback, or explicitly documented abort.
    api("DELETE", "git/" + ref)
    return {"result": "RELEASED", "sha": claim_sha}


def run_worker_command(command, env_extra):
    env = os.environ.copy()
    env.update({k: str(v) for k, v in env_extra.items() if v is not None})
    completed = subprocess.run(command, env=env)
    return completed.returncode


def guarded_claim_run(
    issue_num,
    checkpoint_path,
    worker_fn,
    *,
    assignment_id=None,
    worker_id=None,
    command=None,
):
    """Acquire an issue claim, run worker_fn under a fail-closed finally guard,
    persist durable custody/checkpoint state, and release only our own SHA.
    """
    if assignment_id is not None:
        adjudications([], assignment_id)
    ref = PREFIX + str(issue_num)
    existing_cp = read_checkpoint(checkpoint_path)
    if is_checkpoint_unclosed(existing_cp):
        return EXIT_STALE_CUSTODY_HOLD, {
            "result": "STALE_CUSTODY_HOLD",
            "outcome_class": OUTCOME_FAILED_CLOSURE,
            "issue": issue_num,
            "ref": ref,
            "checkpoint": str(checkpoint_path),
            "existing_phase": existing_cp.get("phase"),
            "existing_claim_sha": existing_cp.get("claim_sha"),
            "existing_worker_id": existing_cp.get("worker_id"),
            "claim_still_held": bool(existing_cp.get("claim_still_held", True)),
            "recovery_required": True,
        }

    wid = worker_id or f"pid-{os.getpid()}-{uuid.uuid4().hex[:12]}"
    checkpoint = {
        "schema_version": CHECKPOINT_SCHEMA,
        "issue": issue_num,
        "assignment_id": assignment_id,
        "ref": ref,
        "worker_id": wid,
        "actor": None,
        "claim_sha": None,
        "nonce": None,
        "phase": "INIT",
        "outcome_class": None,
        "started_at_utc": utc_now(),
        "updated_at_utc": None,
        "closed_at_utc": None,
        "command": list(command) if command is not None else None,
        "command_returncode": None,
        "adjudication_comments_before": [],
        "adjudication_comments_after": [],
        "new_adjudication_comments": [],
        "abort_reason": None,
        "release_status": "NOT_APPLICABLE",
        "release_error": None,
        "claim_still_held": False,
    }
    checkpoint = write_checkpoint(checkpoint_path, checkpoint)

    issue_obj = api("GET", f"issues/{issue_num}")
    if issue_obj.get("state") != "open":
        checkpoint.update(
            {
                "phase": "CLOSED",
                "outcome_class": OUTCOME_READ_ONLY,
                "abort_reason": "issue_not_open",
                "closed_at_utc": utc_now(),
                "claim_still_held": False,
            }
        )
        checkpoint = write_checkpoint(checkpoint_path, checkpoint)
        return EXIT_INELIGIBLE, {
            "result": "INELIGIBLE",
            "reason": "issue not open",
            "outcome_class": OUTCOME_READ_ONLY,
            "checkpoint": str(checkpoint_path),
            "claim_still_held": False,
        }

    before_items, before_pages = comments(issue_num)
    before_adj = adjudications(before_items, assignment_id)
    before_ids = {item["id"] for item in before_adj}
    checkpoint["adjudication_comments_before"] = before_adj
    if before_adj:
        checkpoint.update(
            {
                "phase": "CLOSED",
                "outcome_class": OUTCOME_READ_ONLY,
                "abort_reason": "already_adjudicated_pre_acquire",
                "closed_at_utc": utc_now(),
                "claim_still_held": False,
            }
        )
        checkpoint = write_checkpoint(checkpoint_path, checkpoint)
        return EXIT_ALREADY_ADJUDICATED, {
            "result": "ALREADY_ADJUDICATED",
            "outcome_class": OUTCOME_READ_ONLY,
            "comments": before_adj,
            "count": len(before_items),
            "pages": before_pages,
            "checkpoint": str(checkpoint_path),
            "claim_still_held": False,
        }

    main_ref = api("GET", "git/ref/heads/main")
    head = main_ref["object"]["sha"]
    commit = api("GET", f"git/commits/{head}")
    actor = current_actor()
    nonce = uuid.uuid4().hex
    claim_commit = api(
        "POST",
        "git/commits",
        {
            "message": (
                f"GCL_ADJUDICATION_CLAIM/1 issue={issue_num} actor={actor} "
                f"worker={wid} nonce={nonce}"
            ),
            "tree": commit["tree"]["sha"],
            "parents": [head],
        },
    )
    own_sha = claim_commit["sha"]

    # Persist exact SHA BEFORE create-ref so an interrupted or lost response
    # retains recoverable ownership identity.
    checkpoint.update(
        {
            "actor": actor,
            "claim_sha": own_sha,
            "nonce": nonce,
            "phase": "ACQUIRING",
            "claim_still_held": True,
        }
    )
    checkpoint = write_checkpoint(checkpoint_path, checkpoint)

    try:
        api("POST", "git/refs", {"ref": ref, "sha": own_sha})
    except RuntimeError as exc:
        if is_ref_conflict_error(exc):
            checkpoint.update(
                {
                    "phase": "CLOSED",
                    "outcome_class": OUTCOME_EXCLUSIVE_BLOCK,
                    "abort_reason": "exclusive_claim_conflict_422",
                    "release_status": "NOT_APPLICABLE",
                    "closed_at_utc": utc_now(),
                    "claim_still_held": False,
                }
            )
            checkpoint = write_checkpoint(checkpoint_path, checkpoint)
            return EXIT_NOT_ACQUIRED, {
                "result": "NOT_ACQUIRED",
                "outcome_class": OUTCOME_EXCLUSIVE_BLOCK,
                "error": str(exc),
                "checkpoint": str(checkpoint_path),
                "claim_still_held": False,
            }
        # Non-422 failure during create-ref leaves remote state ambiguous: hold checkpoint.
        checkpoint.update(
            {
                "phase": "HELD_PENDING_RECOVERY",
                "outcome_class": OUTCOME_FAILED_CLOSURE,
                "abort_reason": f"ambiguous_create_ref_error: {exc}",
                "release_status": "HELD_AMBIGUOUS",
                "release_error": str(exc),
                "claim_still_held": True,
            }
        )
        checkpoint = write_checkpoint(checkpoint_path, checkpoint)
        return EXIT_FAILED_CLOSURE, {
            "result": "AMBIGUOUS_CREATE_REF_HOLD",
            "outcome_class": OUTCOME_FAILED_CLOSURE,
            "claim_sha": own_sha,
            "error": str(exc),
            "checkpoint": str(checkpoint_path),
            "claim_still_held": True,
        }

    # From this point onward, our ref exists with own_sha; always reconcile in finally.
    worker_rc = None
    worker_interrupted = None
    worker_exception = None
    post_acquire_duplicate = False
    post_acquire_duplicates = []
    ref_verified = False

    prior_handlers = {}

    def _on_signal(signum, _frame):
        raise KeyboardInterrupt(f"signal {signum}")

    for sig_name in ("SIGINT", "SIGTERM"):
        sig = getattr(signal, sig_name, None)
        if sig is not None:
            try:
                prior_handlers[sig] = signal.getsignal(sig)
                signal.signal(sig, _on_signal)
            except (ValueError, OSError):
                pass

    try:
        current = api("GET", "git/ref/" + ref.removeprefix("refs/"))
        if current["object"]["sha"] != own_sha:
            raise RuntimeError(
                f"post-acquisition ref mismatch (expected={own_sha}, observed={current['object']['sha']})"
            )
        ref_verified = True
        checkpoint.update({"phase": "ACQUIRED", "claim_still_held": True})
        checkpoint = write_checkpoint(checkpoint_path, checkpoint)

        after_acq_items, _ = comments(issue_num)
        post_acquire_duplicates = adjudications(after_acq_items, assignment_id)
        if post_acquire_duplicates:
            post_acquire_duplicate = True
            checkpoint.update(
                {
                    "abort_reason": "existing_adjudication_detected_post_acquire",
                    "adjudication_comments_after": post_acquire_duplicates,
                }
            )
            checkpoint = write_checkpoint(checkpoint_path, checkpoint)
        else:
            checkpoint.update({"phase": "EXECUTING"})
            checkpoint = write_checkpoint(checkpoint_path, checkpoint)
            worker_context = {
                "issue": issue_num,
                "assignment_id": assignment_id,
                "claim_sha": own_sha,
                "ref": ref,
                "actor": actor,
                "worker_id": wid,
                "checkpoint": str(checkpoint_path),
            }
            worker_rc = worker_fn(worker_context)
            checkpoint["command_returncode"] = worker_rc
            checkpoint = write_checkpoint(checkpoint_path, checkpoint)
    except KeyboardInterrupt as exc:
        worker_interrupted = str(exc) or "KeyboardInterrupt"
    except BaseException as exc:
        worker_exception = str(exc)
    finally:
        for sig, handler in prior_handlers.items():
            try:
                signal.signal(sig, handler)
            except (ValueError, OSError):
                pass

        # Phase 1 of finally: durable outcome readback before any release.
        checkpoint["phase"] = "RECONCILING"
        checkpoint = write_checkpoint(checkpoint_path, checkpoint)

        readback_error = None
        after_items = []
        after_pages = 0
        after_adj = list(post_acquire_duplicates)
        new_adj = []
        if not post_acquire_duplicate and ref_verified:
            try:
                after_items, after_pages = comments(issue_num)
                after_adj = adjudications(after_items, assignment_id)
                new_adj = [item for item in after_adj if item["id"] not in before_ids]
            except BaseException as exc:
                readback_error = str(exc)

        checkpoint["adjudication_comments_after"] = after_adj
        checkpoint["new_adjudication_comments"] = new_adj

        # Determine abort reason & whether release is permitted.
        allow_release = False
        if not ref_verified:
            checkpoint["abort_reason"] = (
                f"post_acquire_verification_failed: {worker_exception or worker_interrupted}"
            )
            checkpoint["release_status"] = "HELD_STALE_CUSTODY"
            checkpoint["release_error"] = worker_exception or worker_interrupted
            allow_release = False
        elif post_acquire_duplicate:
            checkpoint["abort_reason"] = "existing_adjudication_detected_post_acquire"
            allow_release = True
        elif readback_error is not None:
            checkpoint["abort_reason"] = f"readback_failed_hold_claim: {readback_error}"
            checkpoint["release_status"] = "HELD_AMBIGUOUS"
            checkpoint["release_error"] = readback_error
            allow_release = False
        else:
            if worker_interrupted is not None:
                checkpoint["abort_reason"] = (
                    f"interrupted_after_readback: {worker_interrupted}"
                    if new_adj
                    else f"interrupted_before_adjudication: {worker_interrupted}"
                )
            elif worker_exception is not None:
                checkpoint["abort_reason"] = (
                    f"worker_exception_after_readback: {worker_exception}"
                    if new_adj
                    else f"worker_exception: {worker_exception}"
                )
            elif worker_rc not in (None, 0):
                checkpoint["abort_reason"] = (
                    f"worker_nonzero_exit_after_readback: {worker_rc}"
                    if new_adj
                    else f"worker_nonzero_exit: {worker_rc}"
                )
            elif not new_adj:
                checkpoint["abort_reason"] = "no_adjudication_posted_read_only"
            else:
                checkpoint["abort_reason"] = None
            allow_release = True

        # Phase 2 of finally: release ONLY our own exact claim SHA.
        release_ok = False
        if allow_release:
            checkpoint["phase"] = "RELEASING"
            checkpoint = write_checkpoint(checkpoint_path, checkpoint)
            try:
                release_owned_claim(ref, own_sha)
                release_ok = True
                checkpoint["release_status"] = "RELEASED"
                checkpoint["release_error"] = None
                checkpoint["claim_still_held"] = False
            except BaseException as exc:
                err_text = str(exc)
                checkpoint["release_error"] = err_text
                checkpoint["claim_still_held"] = True
                if "mismatch" in err_text.lower():
                    checkpoint["release_status"] = "HELD_STALE_CUSTODY"
                else:
                    checkpoint["release_status"] = "RELEASE_ERROR"

        # Final classification.
        clean_worker = (
            worker_interrupted is None
            and worker_exception is None
            and worker_rc in (None, 0)
            and readback_error is None
        )
        if not release_ok:
            outcome_class = OUTCOME_FAILED_CLOSURE
            checkpoint["phase"] = "HELD_PENDING_RECOVERY"
            checkpoint["claim_still_held"] = True
        elif post_acquire_duplicate:
            outcome_class = OUTCOME_READ_ONLY
            checkpoint["phase"] = "CLOSED"
            checkpoint["closed_at_utc"] = utc_now()
        elif not clean_worker:
            outcome_class = OUTCOME_FAILED_CLOSURE
            checkpoint["phase"] = "CLOSED"
            checkpoint["closed_at_utc"] = utc_now()
        elif new_adj:
            outcome_class = OUTCOME_SUBSTANTIVE
            checkpoint["phase"] = "CLOSED"
            checkpoint["closed_at_utc"] = utc_now()
        else:
            outcome_class = OUTCOME_READ_ONLY
            checkpoint["phase"] = "CLOSED"
            checkpoint["closed_at_utc"] = utc_now()

        checkpoint["outcome_class"] = outcome_class
        checkpoint = write_checkpoint(checkpoint_path, checkpoint)

    if post_acquire_duplicate:
        exit_code = EXIT_ABORT_EXISTING if release_ok else EXIT_FAILED_CLOSURE
        result_label = "ABORT_EXISTING_RELEASED" if release_ok else "ABORT_EXISTING_RELEASE_FAILED"
    elif not release_ok:
        exit_code = EXIT_FAILED_CLOSURE
        result_label = checkpoint["release_status"]
    elif outcome_class == OUTCOME_SUBSTANTIVE:
        exit_code = EXIT_OK
        result_label = "ADJUDICATED_AND_RELEASED"
    elif outcome_class == OUTCOME_READ_ONLY:
        exit_code = EXIT_OK
        result_label = "READ_ONLY_AND_RELEASED"
    else:
        exit_code = EXIT_FAILED_CLOSURE
        result_label = "INTERRUPTED_AND_RELEASED" if worker_interrupted else "FAILED_AND_RELEASED"

    summary = {
        "result": result_label,
        "outcome_class": outcome_class,
        "issue": issue_num,
        "assignment_id": assignment_id,
        "actor": actor,
        "worker_id": wid,
        "claim_sha": own_sha,
        "ref": ref,
        "command_returncode": worker_rc,
        "new_adjudication_comments": new_adj,
        "existing": post_acquire_duplicates if post_acquire_duplicate else [],
        "abort_reason": checkpoint["abort_reason"],
        "release_status": checkpoint["release_status"],
        "release_error": checkpoint["release_error"],
        "claim_still_held": checkpoint["claim_still_held"],
        "checkpoint": str(checkpoint_path),
        "phase": checkpoint["phase"],
    }
    return exit_code, summary


def recover_checkpoint(issue_num, checkpoint_path, *, release_owned=False, abort_reason=None):
    """Inspect an interrupted run's durable checkpoint against live GitHub state.
    Never steal or release a mismatched SHA; release only our own verified SHA
    when explicitly requested with readback or documented abort_reason.
    """
    cp = read_checkpoint(checkpoint_path)
    if cp is None:
        raise RuntimeError(f"checkpoint not found: {checkpoint_path}")
    if cp.get("issue") != issue_num:
        raise RuntimeError(
            f"checkpoint issue mismatch (expected={issue_num}, checkpoint={cp.get('issue')})"
        )
    ref = PREFIX + str(issue_num)
    own_sha = cp.get("claim_sha")
    assignment_id = cp.get("assignment_id")
    before_ids = {item["id"] for item in cp.get("adjudication_comments_before") or []}

    live_items, live_pages = comments(issue_num)
    live_adj = adjudications(live_items, assignment_id)
    new_adj = [item for item in live_adj if item["id"] not in before_ids]

    live_sha = None
    ref_exists = False
    try:
        current = api("GET", "git/ref/" + ref.removeprefix("refs/"))
        live_sha = current["object"]["sha"]
        ref_exists = True
    except RuntimeError as exc:
        if not is_not_found_error(exc):
            raise

    if not ref_exists:
        if new_adj:
            recovered_outcome = OUTCOME_SUBSTANTIVE
            recovered_abort = cp.get("abort_reason")
        elif cp.get("phase") == "CLOSED" and cp.get("outcome_class") in {
            OUTCOME_READ_ONLY,
            OUTCOME_EXCLUSIVE_BLOCK,
        }:
            recovered_outcome = cp["outcome_class"]
            recovered_abort = cp.get("abort_reason")
        else:
            recovered_outcome = OUTCOME_FAILED_CLOSURE
            recovered_abort = (
                cp.get("abort_reason") or "recovered_unclaimed_without_adjudication"
            )
        cp.update(
            {
                "phase": "CLOSED",
                "claim_still_held": False,
                "adjudication_comments_after": live_adj,
                "new_adjudication_comments": new_adj,
                "abort_reason": recovered_abort,
                "release_status": "ALREADY_RELEASED",
                "outcome_class": recovered_outcome,
                "closed_at_utc": cp.get("closed_at_utc") or utc_now(),
            }
        )
        write_checkpoint(checkpoint_path, cp)
        return EXIT_OK, {
            "result": "RECOVERED_ALREADY_UNCLAIMED",
            "outcome_class": cp["outcome_class"],
            "issue": issue_num,
            "claim_sha": own_sha,
            "live_sha": None,
            "new_adjudication_comments": new_adj,
            "abort_reason": recovered_abort,
            "pages": live_pages,
            "claim_still_held": False,
            "checkpoint": str(checkpoint_path),
        }

    if not own_sha or live_sha != own_sha:
        cp.update(
            {
                "phase": "HELD_PENDING_RECOVERY",
                "claim_still_held": True,
                "adjudication_comments_after": live_adj,
                "new_adjudication_comments": new_adj,
                "release_status": "HELD_STALE_CUSTODY",
                "outcome_class": OUTCOME_FAILED_CLOSURE,
            }
        )
        write_checkpoint(checkpoint_path, cp)
        return EXIT_STALE_CUSTODY_HOLD, {
            "result": "STALE_CUSTODY_SHA_MISMATCH",
            "outcome_class": OUTCOME_FAILED_CLOSURE,
            "issue": issue_num,
            "claim_sha": own_sha,
            "live_sha": live_sha,
            "new_adjudication_comments": new_adj,
            "claim_still_held": True,
            "checkpoint": str(checkpoint_path),
        }

    if not release_owned:
        return EXIT_STALE_CUSTODY_HOLD, {
            "result": "HELD_BY_CHECKPOINT_OWNER",
            "outcome_class": OUTCOME_FAILED_CLOSURE,
            "issue": issue_num,
            "claim_sha": own_sha,
            "live_sha": live_sha,
            "new_adjudication_comments": new_adj,
            "claim_still_held": True,
            "checkpoint": str(checkpoint_path),
        }

    if not new_adj and not (abort_reason and abort_reason.strip()):
        raise ValueError(
            "--abort-reason is required with --release-owned when no new adjudication comment is present"
        )

    release_owned_claim(ref, own_sha)
    final_outcome = OUTCOME_SUBSTANTIVE if new_adj else OUTCOME_FAILED_CLOSURE
    cp.update(
        {
            "phase": "CLOSED",
            "claim_still_held": False,
            "adjudication_comments_after": live_adj,
            "new_adjudication_comments": new_adj,
            "abort_reason": abort_reason if not new_adj else cp.get("abort_reason"),
            "release_status": "RELEASED",
            "release_error": None,
            "outcome_class": final_outcome,
            "closed_at_utc": utc_now(),
        }
    )
    write_checkpoint(checkpoint_path, cp)
    return EXIT_OK, {
        "result": "RECOVERED_AND_RELEASED",
        "outcome_class": final_outcome,
        "issue": issue_num,
        "claim_sha": own_sha,
        "new_adjudication_comments": new_adj,
        "abort_reason": cp["abort_reason"],
        "claim_still_held": False,
        "checkpoint": str(checkpoint_path),
    }


def main(argv=None):
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    if "--" in raw_argv:
        sep = raw_argv.index("--")
        cli_argv = raw_argv[:sep]
        worker_cmd = raw_argv[sep + 1 :]
    else:
        cli_argv = raw_argv
        worker_cmd = []

    p = argparse.ArgumentParser(
        description=(
            "Atomic per-issue adjudication claim and guarded worker lifecycle. "
            "For `run`, supply the worker command after `--`."
        )
    )
    p.add_argument(
        "action",
        choices=["acquire", "inspect", "release", "run", "recover"],
    )
    p.add_argument("issue", type=int)
    p.add_argument(
        "--assignment-id",
        help="Exact cohort work item; ambiguous adjudications fail closed",
    )
    p.add_argument(
        "--claim-sha",
        help="Exact claim commit SHA, mandatory for release",
    )
    p.add_argument(
        "--checkpoint",
        help="Path to durable JSON custody checkpoint (mandatory for run and recover)",
    )
    p.add_argument(
        "--worker-id",
        help="Stable worker invocation identifier recorded in claim commit and checkpoint",
    )
    p.add_argument(
        "--release-owned",
        action="store_true",
        help="For recover: release the live claim only if its SHA exactly matches the checkpoint",
    )
    p.add_argument(
        "--abort-reason",
        help="For recover --release-owned: explicit abort reason when no adjudication was posted",
    )
    args = p.parse_args(cli_argv)
    if args.issue < 1310:
        p.error("issue must be at least 1310")
    ref = PREFIX + str(args.issue)

    if args.action != "run" and worker_cmd:
        p.error("worker command after `--` is only valid with `run`")

    if args.action == "inspect":
        try:
            current = api("GET", "git/ref/" + ref.removeprefix("refs/"))
            print(json.dumps({"result": "HELD", "sha": current["object"]["sha"]}))
        except RuntimeError as e:
            if not is_not_found_error(e):
                raise
            print(json.dumps({"result": "UNCLAIMED"}))
        return EXIT_OK

    if args.action == "release":
        if not args.claim_sha:
            p.error("--claim-sha required")
        print(json.dumps(release_owned_claim(ref, args.claim_sha)))
        return EXIT_OK

    if args.action == "run":
        if not args.checkpoint:
            p.error("--checkpoint required for run")
        cmd = list(worker_cmd)
        if not cmd:
            p.error("worker command required after `--` for run")

        def _invoke(ctx):
            return run_worker_command(
                cmd,
                {
                    "GCL_CLAIM_ISSUE": ctx["issue"],
                    "GCL_CLAIM_SHA": ctx["claim_sha"],
                    "GCL_CLAIM_REF": ctx["ref"],
                    "GCL_CLAIM_ACTOR": ctx["actor"],
                    "GCL_CLAIM_WORKER_ID": ctx["worker_id"],
                    "GCL_CLAIM_CHECKPOINT": ctx["checkpoint"],
                    "GCL_ASSIGNMENT_ID": ctx["assignment_id"],
                },
            )

        status, summary = guarded_claim_run(
            args.issue,
            args.checkpoint,
            _invoke,
            assignment_id=args.assignment_id,
            worker_id=args.worker_id,
            command=cmd,
        )
        print(json.dumps(summary))
        return status

    if args.action == "recover":
        if not args.checkpoint:
            p.error("--checkpoint required for recover")
        status, summary = recover_checkpoint(
            args.issue,
            args.checkpoint,
            release_owned=args.release_owned,
            abort_reason=args.abort_reason,
        )
        print(json.dumps(summary))
        return status

    # Legacy standalone acquire mode (preserved for compatibility).
    issue = api("GET", f"issues/{args.issue}")
    if issue.get("state") != "open":
        print(json.dumps({"result": "INELIGIBLE", "reason": "issue not open"}))
        return EXIT_INELIGIBLE
    before, pages = comments(args.issue)
    found = adjudications(before, args.assignment_id)
    if found:
        print(
            json.dumps(
                {
                    "result": "ALREADY_ADJUDICATED",
                    "comments": found,
                    "count": len(before),
                    "pages": pages,
                }
            )
        )
        return EXIT_ALREADY_ADJUDICATED
    main_ref = api("GET", "git/ref/heads/main")
    head = main_ref["object"]["sha"]
    commit = api("GET", f"git/commits/{head}")
    actor = current_actor()
    nonce = uuid.uuid4().hex
    claim_commit = api(
        "POST",
        "git/commits",
        {
            "message": f"GCL_ADJUDICATION_CLAIM/1 issue={args.issue} actor={actor} nonce={nonce}",
            "tree": commit["tree"]["sha"],
            "parents": [head],
        },
    )
    try:
        api("POST", "git/refs", {"ref": ref, "sha": claim_commit["sha"]})
    except RuntimeError as e:
        # A 422 race is a losing claim, never authorization to retry or post.
        print(json.dumps({"result": "NOT_ACQUIRED", "error": str(e)}))
        return EXIT_NOT_ACQUIRED
    current = api("GET", "git/ref/" + ref.removeprefix("refs/"))
    if current["object"]["sha"] != claim_commit["sha"]:
        raise RuntimeError("post-acquisition ref mismatch")
    after, pages_after = comments(args.issue)
    duplicates = adjudications(after, args.assignment_id)
    print(
        json.dumps(
            {
                "result": "ACQUIRED" if not duplicates else "ABORT_EXISTING",
                "issue": args.issue,
                "actor": actor,
                "claim_sha": claim_commit["sha"],
                "ref": ref,
                "before_count": len(before),
                "after_count": len(after),
                "before_pages": pages,
                "after_pages": pages_after,
                "existing": duplicates,
            }
        )
    )
    return EXIT_OK if not duplicates else EXIT_ABORT_EXISTING


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.CalledProcessError, ValueError) as exc:
        print(json.dumps({"result": "ERROR_FAIL_CLOSED", "error": str(exc)}))
        sys.exit(EXIT_ERROR)
