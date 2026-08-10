from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from administrative_automation import parse_datetime
from administrative_autonomy_runtime_late_recovery import (
    eligible_candidates as existing_eligible_candidates,
)
from autonomy_github import AutonomyError, json_content

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = ROOT / "governance" / "administrative_recovery_queue_starvation_control.json"
STATE_PATH = "governance/administrative_maintenance_completion_state.json"
UTC = timezone.utc

EligibleFunction = Callable[
    [Any, str, dict[str, Any], datetime],
    list[tuple[dict[str, Any], dict[str, Any]]],
]
CompletionLoader = Callable[[Any, str], dict[str, Any]]
AncestryChecker = Callable[[Any, str, str], bool]


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def default_completion_loader(candidate: Any, repo: str) -> dict[str, Any]:
    completion = json_content(candidate, repo, STATE_PATH, "main")
    if completion is None:
        raise AutonomyError("protected completion ledger is absent")
    return completion


def default_ancestry_checker(candidate: Any, repo: str, source: str) -> bool:
    main = candidate.get(f"/repos/{repo}/branches/main")
    current = str(main.get("commit", {}).get("sha") or "")
    if not current:
        raise AutonomyError("protected main head readback is absent")
    if current == source:
        return True
    comparison = candidate.get(f"/repos/{repo}/compare/{source}...{current}")
    return str(comparison.get("status") or "") in {"ahead", "identical"}


def completion_absent(
    completion: dict[str, Any], control: dict[str, Any]
) -> bool:
    occurrence = control["correction"]["continuation_occurrence_key"]
    due_raw = occurrence.split(":", 1)[1]
    due = parse_datetime(due_raw)
    procedure = completion.get("procedures", {}).get("structural_sweep", {})
    completed_raw = procedure.get("completed_through_utc")
    if completed_raw and parse_datetime(str(completed_raw)) >= due:
        return False
    for receipt in procedure.get("receipts", []):
        if str(receipt.get("scheduled_due_at") or "") == due_raw:
            return False
    return True


def continuation_recovery_minutes(
    runtime: dict[str, Any], control: dict[str, Any]
) -> int:
    due = parse_datetime(
        control["correction"]["continuation_occurrence_key"].split(":", 1)[1]
    )
    expires = parse_datetime(control["correction"]["continuation_expires_at_utc"])
    bounded = int((expires - due).total_seconds() // 60)
    ordinary = int(runtime["scope"]["recovery_window_minutes_after_due"])
    if bounded <= ordinary:
        raise AutonomyError("transition continuation does not extend beyond ordinary recovery")
    return bounded


def eligible_candidates(
    candidate: Any,
    repo: str,
    runtime: dict[str, Any],
    now: datetime,
    base: EligibleFunction = existing_eligible_candidates,
    completion_loader: CompletionLoader = default_completion_loader,
    ancestry_checker: AncestryChecker = default_ancestry_checker,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    ordinary = base(candidate, repo, runtime, now)
    if ordinary:
        return ordinary

    if now.tzinfo is None:
        raise AutonomyError("transition-continuation evaluation time must include an offset")
    observed = now.astimezone(UTC)
    control = load_control()
    if control.get("control_id") != "MP-ADMIN-RECOVERY-QUEUE-STARVATION-001":
        raise AutonomyError("transition-continuation control identity drift")
    if control.get("status") != "PROPOSED_CONTROL_PLANE_CORRECTION":
        return []

    original_expiry = parse_datetime(
        control["problem"]["original_recovery_expires_at_utc"]
    )
    continuation_expiry = parse_datetime(
        control["correction"]["continuation_expires_at_utc"]
    )
    if observed <= original_expiry or observed >= continuation_expiry:
        return []

    completion = completion_loader(candidate, repo)
    if not completion_absent(completion, control):
        return []

    source = str(control["correction"]["required_source_protected_head"])
    if not ancestry_checker(candidate, repo, source):
        raise AutonomyError("transition-continuation source is not ancestral to protected main")

    widened = copy.deepcopy(runtime)
    widened["scope"]["recovery_window_minutes_after_due"] = (
        continuation_recovery_minutes(runtime, control)
    )
    replayed = base(candidate, repo, widened, observed)

    expected_occurrence = control["correction"]["continuation_occurrence_key"]
    expected_issue = int(control["correction"]["continuation_issue"])
    expected_pr = int(control["correction"]["continuation_pull_request"])
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for pull, manifest in replayed:
        if manifest.get("occurrence_key") != expected_occurrence:
            continue
        if int(manifest.get("issue_number") or 0) != expected_issue:
            raise AutonomyError("transition-continuation issue identity drift")
        if int(manifest.get("pull_request_number") or 0) != expected_pr:
            raise AutonomyError("transition-continuation manifest PR identity drift")
        if int(pull.get("number") or 0) != expected_pr:
            raise AutonomyError("transition-continuation pull-request identity drift")
        if str(manifest.get("source_protected_head") or "") != source:
            raise AutonomyError("transition-continuation source-head identity drift")
        matches.append((pull, manifest))

    if len(matches) > 1:
        raise AutonomyError("duplicate exact transition-continuation candidate")
    return matches
