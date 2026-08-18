from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from administrative_automation import parse_datetime, validate_completion_state
from administrative_autonomy_receipt_stage import (
    STATE_PATH,
    advance_completion_state as base_advance_completion_state,
    completion_has_receipt,
)
from administrative_autonomy_runtime_mirror_sync import (
    wait_mirror_sync as base_wait_mirror_sync,
)
from administrative_autonomy_runtime_structural_0833_recovery import (
    default_ancestry_checker,
    default_completion_loader,
    eligible_candidates as existing_eligible_candidates,
)
from autonomy_github import AutonomyError, json_content

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = (
    ROOT
    / "governance"
    / "administrative_structural_0121_late_recovery_control.json"
)
UTC = timezone.utc

EligibleFunction = Callable[
    [Any, str, dict[str, Any], datetime],
    list[tuple[dict[str, Any], dict[str, Any]]],
]
CompletionLoader = Callable[[Any, str], dict[str, Any]]
AncestryChecker = Callable[[Any, str, str], bool]
MirrorWaiter = Callable[[Any, Any, str, str, str, str, dict[str, Any]], int]


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def _require_control(control: dict[str, Any]) -> None:
    if control.get("control_id") != "MP-ADMIN-STRUCTURAL-0121-HOLE-RECOVERY-001":
        raise AutonomyError("01:21 hole recovery control identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        raise AutonomyError("01:21 hole recovery control is not active")
    correction = control.get("correction", {})
    required = {
        "global_recovery_window_minutes_unchanged": 180,
        "exact_occurrence_only": True,
        "exact_receipt_absence_is_recovery_condition": True,
        "later_completion_frontier_preserved": True,
        "historical_receipt_backfill_allowed_for_exact_occurrence": True,
        "mirror_current_frontier_preserved": True,
        "behind_sync_reconciliation_required": True,
        "source_ancestry_required": True,
        "deadline_reset": False,
        "cadence_anchor_reset": False,
        "eventual_recovery_relabels_on_time": False,
        "historical_failed_closed_evidence_preserved": True,
        "intervening_occurrences_superseded": False,
    }
    for key, expected in required.items():
        if correction.get(key) != expected:
            raise AutonomyError(f"01:21 hole recovery control drift: {key}")


def _target_due(control: dict[str, Any]) -> str:
    return str(control["occurrence"]["due_at_utc"])


def _target_receipt(receipt: dict[str, Any], control: dict[str, Any]) -> bool:
    occurrence = control["occurrence"]
    return (
        str(receipt.get("procedure_id") or "") == str(occurrence["procedure_id"])
        and str(receipt.get("scheduled_due_at") or "") == str(occurrence["due_at_utc"])
        and str(receipt.get("record_path") or "") == str(occurrence["record_path"])
        and int(receipt.get("pull_request") or 0)
        == int(occurrence["candidate_pull_request"])
    )


def exact_receipt_absent(
    completion: dict[str, Any], control: dict[str, Any]
) -> bool:
    """Detect the exact historical hole without lowering the later frontier."""

    _require_control(control)
    occurrence = control["occurrence"]
    procedure = completion.get("procedures", {}).get(
        str(occurrence["procedure_id"]), {}
    )
    target = parse_datetime(str(occurrence["due_at_utc"]))
    frontier_raw = procedure.get("completed_through_utc")
    if not frontier_raw:
        raise AutonomyError("01:21 hole recovery completion frontier is absent")
    frontier = parse_datetime(str(frontier_raw))
    if frontier <= target:
        raise AutonomyError(
            "01:21 hole recovery requires a protected frontier later than the hole"
        )
    due_raw = str(occurrence["due_at_utc"])
    for receipt in procedure.get("receipts", []):
        if str(receipt.get("scheduled_due_at") or "") == due_raw:
            return False
    return True


def bounded_recovery_minutes(
    runtime: dict[str, Any], control: dict[str, Any]
) -> int:
    _require_control(control)
    due = parse_datetime(str(control["occurrence"]["due_at_utc"]))
    expires = parse_datetime(
        str(control["occurrence"]["bounded_recovery_expires_at_utc"])
    )
    bounded = int((expires - due).total_seconds() // 60)
    ordinary = int(runtime["scope"]["recovery_window_minutes_after_due"])
    declared = int(
        control["correction"]["global_recovery_window_minutes_unchanged"]
    )
    if ordinary != declared:
        raise AutonomyError(
            "01:21 hole recovery control does not match protected ordinary "
            "recovery window"
        )
    if bounded <= ordinary:
        raise AutonomyError(
            "01:21 hole recovery continuation does not extend beyond ordinary "
            "recovery"
        )
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
    """Admit only the missing 01:21 receipt-hole candidate.

    Ordinary protected eligibility and all earlier exact-occurrence recovery
    wrappers retain precedence. The global recovery window is never mutated.
    A temporary horizon is replayed and then filtered back to #515 / #516.
    """

    ordinary = base(candidate, repo, runtime, now)
    if ordinary:
        return ordinary

    if now.tzinfo is None:
        raise AutonomyError("01:21 hole recovery evaluation time must include an offset")
    observed = now.astimezone(UTC)
    control = load_control()
    _require_control(control)

    ordinary_expiry = parse_datetime(
        str(control["occurrence"]["ordinary_recovery_expires_at_utc"])
    )
    bounded_expiry = parse_datetime(
        str(control["occurrence"]["bounded_recovery_expires_at_utc"])
    )
    if observed <= ordinary_expiry or observed >= bounded_expiry:
        return []

    completion = completion_loader(candidate, repo)
    if not exact_receipt_absent(completion, control):
        return []

    source = str(control["occurrence"]["original_source_protected_head"])
    if not ancestry_checker(candidate, repo, source):
        raise AutonomyError(
            "01:21 hole recovery source is not ancestral to protected main"
        )

    widened = copy.deepcopy(runtime)
    widened["scope"]["recovery_window_minutes_after_due"] = (
        bounded_recovery_minutes(runtime, control)
    )
    replayed = base(candidate, repo, widened, observed)

    occurrence = control["occurrence"]
    expected_occurrence = str(occurrence["occurrence_key"])
    expected_issue = int(occurrence["candidate_issue"])
    expected_pr = int(occurrence["candidate_pull_request"])
    expected_branch = str(occurrence["candidate_branch"])
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for pull, manifest in replayed:
        if str(manifest.get("occurrence_key") or "") != expected_occurrence:
            continue
        if int(manifest.get("issue_number") or 0) != expected_issue:
            raise AutonomyError("01:21 hole recovery issue identity drift")
        if int(manifest.get("pull_request_number") or 0) != expected_pr:
            raise AutonomyError("01:21 hole recovery manifest PR identity drift")
        if int(pull.get("number") or 0) != expected_pr:
            raise AutonomyError("01:21 hole recovery pull-request identity drift")
        if str(manifest.get("branch") or "") != expected_branch:
            raise AutonomyError("01:21 hole recovery branch identity drift")
        if str(manifest.get("source_protected_head") or "") != source:
            raise AutonomyError("01:21 hole recovery source-head identity drift")
        matches.append((pull, manifest))

    if len(matches) > 1:
        raise AutonomyError("duplicate exact 01:21 hole recovery candidate")
    return matches


def advance_completion_state(
    current: dict[str, Any],
    receipt: dict[str, Any],
    protected_record_merge: str,
    base: Callable[[dict[str, Any], dict[str, Any], str], dict[str, Any]] = base_advance_completion_state,
) -> dict[str, Any]:
    """Insert only the exact #515 historical receipt behind a later frontier."""

    control = load_control()
    _require_control(control)
    occurrence = control["occurrence"]
    target_due = str(occurrence["due_at_utc"])
    procedure_id = str(occurrence["procedure_id"])
    receipt_due = str(receipt.get("scheduled_due_at") or "")
    receipt_procedure = str(receipt.get("procedure_id") or "")

    if receipt_procedure != procedure_id or receipt_due != target_due:
        return base(current, receipt, protected_record_merge)
    if not _target_receipt(receipt, control):
        raise AutonomyError("01:21 historical receipt identity drift")
    if completion_has_receipt(current, receipt):
        return current

    completion = copy.deepcopy(current)
    procedure = completion.get("procedures", {}).get(procedure_id)
    if not isinstance(procedure, dict):
        raise AutonomyError("01:21 hole recovery ledger procedure is absent")
    frontier_raw = procedure.get("completed_through_utc")
    if not frontier_raw:
        raise AutonomyError("01:21 hole recovery completion frontier is absent")
    target = parse_datetime(target_due)
    frontier = parse_datetime(str(frontier_raw))
    if frontier <= target:
        raise AutonomyError(
            "01:21 historical receipt backfill requires a later protected frontier"
        )

    receipts = list(procedure.get("receipts", []))
    if any(
        str(item.get("scheduled_due_at") or "") == target_due
        for item in receipts
    ):
        raise AutonomyError("conflicting exact 01:21 historical receipt")
    receipts.append(copy.deepcopy(receipt))
    receipts.sort(
        key=lambda item: (
            parse_datetime(str(item["scheduled_due_at"])),
            str(item["record_path"]),
        )
    )
    procedure["receipts"] = receipts
    procedure["receipt_count"] = len(receipts)
    procedure["completed_through_utc"] = str(frontier_raw)
    completion["derived_from_protected_head"] = protected_record_merge
    errors = validate_completion_state(completion, current)
    if errors:
        raise AutonomyError("; ".join(errors))
    return completion


def wait_mirror_sync(
    observability: Any,
    evidence: Any,
    repo: str,
    merge_sha: str,
    procedure_id: str,
    due: str,
    runtime: dict[str, Any],
    base: MirrorWaiter = base_wait_mirror_sync,
) -> int:
    """Bind the exact backfill to mirrors of the preserved current frontier."""

    control = load_control()
    _require_control(control)
    occurrence = control["occurrence"]
    target_due = str(occurrence["due_at_utc"])
    target_procedure = str(occurrence["procedure_id"])
    if procedure_id != target_procedure or due != target_due:
        return base(
            observability,
            evidence,
            repo,
            merge_sha,
            procedure_id,
            due,
            runtime,
        )

    completion = json_content(evidence, repo, STATE_PATH, "main")
    if completion is None:
        raise AutonomyError("01:21 mirror readback completion ledger is absent")
    procedure = completion.get("procedures", {}).get(target_procedure, {})
    receipts = procedure.get("receipts", [])
    matches = [item for item in receipts if _target_receipt(item, control)]
    if len(matches) != 1:
        raise AutonomyError(
            "01:21 mirror readback requires exactly one protected historical receipt"
        )
    frontier_raw = str(procedure.get("completed_through_utc") or "")
    if not frontier_raw:
        raise AutonomyError("01:21 mirror readback frontier is absent")
    if parse_datetime(frontier_raw) <= parse_datetime(target_due):
        raise AutonomyError(
            "01:21 mirror readback did not preserve the later completion frontier"
        )
    return base(
        observability,
        evidence,
        repo,
        merge_sha,
        procedure_id,
        frontier_raw,
        runtime,
    )
