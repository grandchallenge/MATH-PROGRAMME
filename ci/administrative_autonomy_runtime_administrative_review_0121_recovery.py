from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from administrative_automation import parse_datetime
from administrative_autonomy_runtime_structural_1809_recovery import (
    default_ancestry_checker,
    default_completion_loader,
    eligible_candidates as existing_eligible_candidates,
)
from autonomy_github import AutonomyError

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = (
    ROOT
    / "governance"
    / "administrative_review_0121_late_recovery_control.json"
)
UTC = timezone.utc

EligibleFunction = Callable[
    [Any, str, dict[str, Any], datetime],
    list[tuple[dict[str, Any], dict[str, Any]]],
]
CompletionLoader = Callable[[Any, str], dict[str, Any]]
AncestryChecker = Callable[[Any, str, str], bool]


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def _require_control(control: dict[str, Any]) -> None:
    if control.get("control_id") != "MP-ADMIN-ADMINISTRATIVE-0121-LATE-RECOVERY-001":
        raise AutonomyError("administrative 01:21 recovery control identity drift")
    if control.get("issue") != 549:
        raise AutonomyError("administrative 01:21 recovery issue identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        raise AutonomyError("administrative 01:21 recovery control is not active")
    if control.get("protected_base_at_opening") != "2dfe02c61a5c9b29e40c0df169589e9fe3d69216":
        raise AutonomyError("administrative 01:21 recovery protected-base drift")
    correction = control.get("correction", {})
    required = {
        "global_recovery_window_minutes_unchanged": 180,
        "exact_occurrence_only": True,
        "behind_sync_reconciliation_required": True,
        "completion_must_be_absent": True,
        "source_ancestry_required": True,
        "record_identity_must_be_preserved": True,
        "fresh_exact_head_referee_required": True,
        "deadline_reset": False,
        "cadence_anchor_reset": False,
        "historical_failed_closed_evidence_preserved": True,
        "intervening_occurrences_superseded": False,
        "structural_frontier_mutation_authorized": False,
    }
    for key, expected in required.items():
        if correction.get(key) != expected:
            raise AutonomyError(f"administrative 01:21 recovery control drift: {key}")
    authority = control.get("authority_boundary", {})
    if authority.get("human_steward_exact_head_authorization_required") is not True:
        raise AutonomyError("administrative 01:21 Human Steward gate drift")
    prohibited = (
        "candidate_branch_is_authority",
        "stale_referee_approval_is_authority",
        "bypass_created",
        "emergency_authority_created",
        "required_checks_weakened",
        "referee_gate_weakened",
        "direct_protected_push_authorized",
        "general_late_recovery_authority_created",
        "structural_1809_authority_inherited",
    )
    if any(authority.get(key) is not False for key in prohibited):
        raise AutonomyError("administrative 01:21 recovery authority-boundary drift")
    claims = control.get("claim_boundaries", {})
    if not claims or any(value is not False for value in claims.values()):
        raise AutonomyError("administrative 01:21 recovery claim-boundary drift")


def completion_absent(completion: dict[str, Any], control: dict[str, Any]) -> bool:
    _require_control(control)
    occurrence = control["occurrence"]
    procedure_id = str(occurrence["procedure_id"])
    due_raw = str(occurrence["due_at_utc"])
    due = parse_datetime(due_raw)
    procedure = completion.get("procedures", {}).get(procedure_id, {})
    completed_raw = procedure.get("completed_through_utc")
    if completed_raw and parse_datetime(str(completed_raw)) >= due:
        return False
    matches = [
        item
        for item in procedure.get("receipts", [])
        if str(item.get("scheduled_due_at") or "") == due_raw
    ]
    if len(matches) > 1:
        raise AutonomyError("duplicate administrative 01:21 completion receipts")
    return not matches


def bounded_recovery_minutes(runtime: dict[str, Any], control: dict[str, Any]) -> int:
    _require_control(control)
    due = parse_datetime(str(control["occurrence"]["due_at_utc"]))
    expires = parse_datetime(str(control["occurrence"]["bounded_recovery_expires_at_utc"]))
    bounded = int((expires - due).total_seconds() // 60)
    ordinary = int(runtime["scope"]["recovery_window_minutes_after_due"])
    declared = int(control["correction"]["global_recovery_window_minutes_unchanged"])
    if ordinary != declared:
        raise AutonomyError("administrative 01:21 control does not match ordinary recovery window")
    if bounded <= ordinary:
        raise AutonomyError("administrative 01:21 continuation does not extend beyond ordinary recovery")
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
    """Admit only exact #522/#523 inside its bounded administrative-review horizon."""

    ordinary = base(candidate, repo, runtime, now)
    if ordinary:
        return ordinary
    if now.tzinfo is None:
        raise AutonomyError("administrative 01:21 recovery evaluation time must include an offset")

    observed = now.astimezone(UTC)
    control = load_control()
    _require_control(control)
    occurrence = control["occurrence"]
    ordinary_expiry = parse_datetime(str(occurrence["ordinary_recovery_expires_at_utc"]))
    bounded_expiry = parse_datetime(str(occurrence["bounded_recovery_expires_at_utc"]))
    if observed <= ordinary_expiry or observed >= bounded_expiry:
        return []

    completion = completion_loader(candidate, repo)
    if not completion_absent(completion, control):
        return []

    source = str(occurrence["original_source_protected_head"])
    if not ancestry_checker(candidate, repo, source):
        raise AutonomyError("administrative 01:21 source is not ancestral to protected main")

    widened = copy.deepcopy(runtime)
    widened["scope"]["recovery_window_minutes_after_due"] = bounded_recovery_minutes(runtime, control)
    replayed = base(candidate, repo, widened, observed)

    expected_occurrence = str(occurrence["occurrence_key"])
    expected_issue = int(occurrence["candidate_issue"])
    expected_pr = int(occurrence["candidate_pull_request"])
    expected_branch = str(occurrence["candidate_branch"])
    expected_manifest = str(occurrence["manifest_path"])
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for pull, manifest in replayed:
        if str(manifest.get("occurrence_key") or "") != expected_occurrence:
            continue
        if str(manifest.get("procedure_id") or "") != "administrative_review":
            raise AutonomyError("administrative 01:21 procedure identity drift")
        if int(manifest.get("issue_number") or 0) != expected_issue:
            raise AutonomyError("administrative 01:21 issue identity drift")
        if int(manifest.get("pull_request_number") or 0) != expected_pr or int(pull.get("number") or 0) != expected_pr:
            raise AutonomyError("administrative 01:21 pull-request identity drift")
        if str(manifest.get("branch") or "") != expected_branch:
            raise AutonomyError("administrative 01:21 branch identity drift")
        if str(manifest.get("manifest_path") or "") != expected_manifest:
            raise AutonomyError("administrative 01:21 manifest-path drift")
        if str(manifest.get("source_protected_head") or "") != source:
            raise AutonomyError("administrative 01:21 source-head identity drift")
        matches.append((pull, manifest))

    if len(matches) > 1:
        raise AutonomyError("duplicate exact administrative 01:21 recovery candidate")
    return matches
