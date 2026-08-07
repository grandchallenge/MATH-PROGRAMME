from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from autonomy_github import AutonomyError, Client
from administrative_autonomy_runtime_contract import RUNTIME_PATH, ROOT, load_json
from administrative_autonomy_runtime_execute import (
    execute as execute_without_behind_sync,
    parse_args,
    validate_command as validate_runtime_command,
)
from administrative_autonomy_runtime_github import eligible_candidates

CONTROL_PATH = ROOT / "governance" / "administrative_autonomy_behind_sync_control.json"
CONTROL_SCHEMA_PATH = ROOT / "schemas" / "administrative_autonomy_behind_sync_control.schema.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
UTC = timezone.utc


def validate_behind_sync_control(control: dict[str, Any]) -> list[str]:
    schema = load_json(CONTROL_SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = [
        f"behind-sync schema: {'/'.join(str(part) for part in error.absolute_path)}: {error.message}"
        for error in validator.iter_errors(control)
    ]
    sync = control.get("synchronization", {})
    if sync.get("expected_head_required") is not True:
        errors.append("behind-sync expected-head protection is required")
    if sync.get("base_branch") != "main":
        errors.append("behind-sync base branch must remain main")
    if sync.get("branch_prefix") != "automation/maintenance/":
        errors.append("behind-sync branch scope drift")
    authority = control.get("authority_boundary", {})
    if authority.get("human_steward_identity_asserted") is not False:
        errors.append("behind-sync control asserts Human Steward identity")
    if authority.get("bypass_may_be_exercised") is not False:
        errors.append("behind-sync control permits bypass")
    boundaries = control.get("claim_boundaries", {})
    if not boundaries or any(value is not False for value in boundaries.values()):
        errors.append("behind-sync claim boundaries must remain false")
    return errors


def _validate_candidate_scope(
    pull: dict[str, Any],
    manifest: dict[str, Any],
    repo: str,
    control: dict[str, Any],
) -> tuple[int, str]:
    sync = control["synchronization"]
    number = int(pull.get("number") or 0)
    if number != int(manifest["pull_request_number"]):
        raise AutonomyError("behind-sync pull-request identity drift")
    if pull.get("state") != "open":
        raise AutonomyError("behind-sync candidate is not open")
    head = pull.get("head", {})
    base = pull.get("base", {})
    branch = str(head.get("ref") or "")
    head_sha = str(head.get("sha") or "")
    if branch != str(manifest["branch"]):
        raise AutonomyError("behind-sync candidate branch does not match manifest")
    if not branch.startswith(str(sync["branch_prefix"])):
        raise AutonomyError("behind-sync candidate branch is outside bounded scope")
    if str(base.get("ref") or "") != str(sync["base_branch"]):
        raise AutonomyError("behind-sync candidate base is not main")
    head_repo = str(head.get("repo", {}).get("full_name") or repo)
    if head_repo != repo:
        raise AutonomyError("behind-sync candidate head repository drift")
    if not SHA_RE.fullmatch(head_sha):
        raise AutonomyError("behind-sync candidate head is not a commit SHA")
    return number, head_sha


def _current_pull(
    candidate: Client,
    repo: str,
    pr: int,
    manifest: dict[str, Any],
    control: dict[str, Any],
) -> dict[str, Any]:
    pull = candidate.get(f"/repos/{repo}/pulls/{pr}")
    _validate_candidate_scope(pull, manifest, repo, control)
    return pull


def synchronize_pull_if_behind(
    candidate: Client,
    repo: str,
    pull: dict[str, Any],
    manifest: dict[str, Any],
    control: dict[str, Any],
    attempt: int,
) -> dict[str, Any] | None:
    number, observed_head = _validate_candidate_scope(
        pull, manifest, repo, control
    )
    sync = control["synchronization"]
    deadline = time.monotonic() + int(sync["merge_state_wait_seconds"])
    latest = pull
    while str(latest.get("mergeable_state") or "unknown").lower() == "unknown":
        if time.monotonic() >= deadline:
            raise AutonomyError("behind-sync merge-state readback timed out")
        time.sleep(int(sync["poll_interval_seconds"]))
        latest = _current_pull(candidate, repo, number, manifest, control)
        _, observed_head = _validate_candidate_scope(
            latest, manifest, repo, control
        )

    merge_state = str(latest.get("mergeable_state") or "").lower()
    if merge_state != "behind":
        return None
    if attempt > int(sync["maximum_attempts_per_run"]):
        raise AutonomyError("behind-sync attempt limit exceeded")

    candidate.put(
        f"/repos/{repo}/pulls/{number}/update-branch",
        {"expected_head_sha": observed_head},
    )
    change_deadline = time.monotonic() + int(sync["head_change_wait_seconds"])
    while time.monotonic() < change_deadline:
        time.sleep(int(sync["poll_interval_seconds"]))
        updated = _current_pull(candidate, repo, number, manifest, control)
        _, updated_head = _validate_candidate_scope(
            updated, manifest, repo, control
        )
        if updated_head != observed_head:
            return {
                "pull_request": number,
                "trigger": "BEHIND",
                "attempt": attempt,
                "previous_head": observed_head,
                "synchronized_head": updated_head,
                "expected_head_used": True,
                "base_branch": "main",
            }
    raise AutonomyError("behind-sync head-change readback timed out")


def synchronize_eligible_candidate(
    candidate: Client,
    repo: str,
    runtime: dict[str, Any],
    control: dict[str, Any],
    attempt: int,
) -> dict[str, Any] | None:
    eligible = eligible_candidates(candidate, repo, runtime, datetime.now(UTC))
    if len(eligible) > 1:
        raise AutonomyError(
            "multiple frozen maintenance candidates require fail-closed triage"
        )
    if not eligible:
        return None
    pull, manifest = eligible[0]
    current = _current_pull(
        candidate, repo, int(pull["number"]), manifest, control
    )
    return synchronize_pull_if_behind(
        candidate, repo, current, manifest, control, attempt
    )


def is_behind_stabilization_failure(exc: Exception) -> bool:
    message = str(exc)
    return (
        "post-disposition stabilization timed out" in message
        and (
            "'merge_state': 'BEHIND'" in message
            or '"merge_state": "BEHIND"' in message
        )
    )


def _record_sync_events(report_path: Path, events: list[dict[str, Any]]) -> None:
    if not events or not report_path.exists():
        return
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["behind_candidate_synchronization"] = {
        "control_id": "MP-ADMIN-AUTONOMY-BEHIND-SYNC-001",
        "count": len(events),
        "events": events,
        "human_steward_identity_asserted": False,
        "bypass_used": False,
    }
    report_path.write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )


def validate_command() -> int:
    result = validate_runtime_command()
    control = load_json(CONTROL_PATH)
    errors = validate_behind_sync_control(control)
    if errors:
        for error in errors:
            print(error)
        return 1
    if result != 0:
        return result
    print("administrative autonomy BEHIND synchronization control: valid")
    return 0


def execute(report_path: Path) -> int:
    runtime = load_json(RUNTIME_PATH)
    control = load_json(CONTROL_PATH)
    errors = validate_behind_sync_control(control)
    if errors:
        raise AutonomyError("; ".join(errors))
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if repo != control["repository"]:
        raise AutonomyError("behind-sync runtime repository drift")
    candidate = Client(os.environ.get("CANDIDATE_TOKEN", ""))
    maximum = int(
        control["synchronization"]["maximum_attempts_per_run"]
    )
    events: list[dict[str, Any]] = []

    for attempt in range(1, maximum + 1):
        event = synchronize_eligible_candidate(
            candidate, repo, runtime, control, attempt
        )
        if event is not None:
            events.append(event)
        try:
            result = execute_without_behind_sync(report_path)
            _record_sync_events(report_path, events)
            return result
        except AutonomyError as exc:
            if not is_behind_stabilization_failure(exc) or attempt >= maximum:
                raise
            continue
    raise AutonomyError("behind-sync attempt limit exhausted")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.command == "validate":
        return validate_command()
    return execute(args.report)


if __name__ == "__main__":
    raise SystemExit(main())
