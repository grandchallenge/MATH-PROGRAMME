from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from administrative_automation import parse_datetime
from administrative_autonomy_runtime_structural_2033_recovery import (
    default_ancestry_checker,
    default_completion_loader,
    eligible_candidates as existing_eligible_candidates,
)
from autonomy_github import AutonomyError

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = (
    ROOT
    / "governance"
    / "administrative_structural_2257_late_recovery_control.json"
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


def completion_absent(
    completion: dict[str, Any], control: dict[str, Any]
) -> bool:
    occurrence = str(control["occurrence"]["occurrence_key"])
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


def bounded_recovery_minutes(
    runtime: dict[str, Any], control: dict[str, Any]
) -> int:
    due = parse_datetime(control["occurrence"]["due_at_utc"])
    expires = parse_datetime(
        control["occurrence"]["bounded_recovery_expires_at_utc"]
    )
    bounded = int((expires - due).total_seconds() // 60)
    ordinary = int(runtime["scope"]["recovery_window_minutes_after_due"])
    declared = int(
        control["correction"]["global_recovery_window_minutes_unchanged"]
    )
    if ordinary != declared:
        raise AutonomyError(
            "22:57 recovery control does not match protected ordinary "
            "recovery window"
        )
    if bounded <= ordinary:
        raise AutonomyError(
            "22:57 recovery continuation does not extend beyond ordinary "
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
    """Admit only the queue-starved 22:57 structural candidate.

    Ordinary protected eligibility and every earlier exact-occurrence recovery
    always win. This wrapper never changes the protected global recovery
    window. It replays the existing checks with a temporary horizon only for
    issue #479 / PR #480 and only until the next anchored structural locus.
    """

    ordinary = base(candidate, repo, runtime, now)
    if ordinary:
        return ordinary

    if now.tzinfo is None:
        raise AutonomyError("22:57 recovery evaluation time must include an offset")
    observed = now.astimezone(UTC)
    control = load_control()
    if (
        control.get("control_id")
        != "MP-ADMIN-STRUCTURAL-2257-LATE-RECOVERY-001"
    ):
        raise AutonomyError("22:57 recovery control identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        return []

    ordinary_expiry = parse_datetime(
        control["occurrence"]["ordinary_recovery_expires_at_utc"]
    )
    bounded_expiry = parse_datetime(
        control["occurrence"]["bounded_recovery_expires_at_utc"]
    )
    if observed <= ordinary_expiry or observed >= bounded_expiry:
        return []

    completion = completion_loader(candidate, repo)
    if not completion_absent(completion, control):
        return []

    source = str(control["occurrence"]["original_source_protected_head"])
    if not ancestry_checker(candidate, repo, source):
        raise AutonomyError(
            "22:57 recovery source is not ancestral to protected main"
        )

    widened = copy.deepcopy(runtime)
    widened["scope"]["recovery_window_minutes_after_due"] = (
        bounded_recovery_minutes(runtime, control)
    )
    replayed = base(candidate, repo, widened, observed)

    expected_occurrence = str(control["occurrence"]["occurrence_key"])
    expected_issue = int(control["occurrence"]["candidate_issue"])
    expected_pr = int(control["occurrence"]["candidate_pull_request"])
    expected_branch = str(control["occurrence"]["candidate_branch"])
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for pull, manifest in replayed:
        if str(manifest.get("occurrence_key") or "") != expected_occurrence:
            continue
        if int(manifest.get("issue_number") or 0) != expected_issue:
            raise AutonomyError("22:57 recovery issue identity drift")
        if int(manifest.get("pull_request_number") or 0) != expected_pr:
            raise AutonomyError("22:57 recovery manifest PR identity drift")
        if int(pull.get("number") or 0) != expected_pr:
            raise AutonomyError("22:57 recovery pull-request identity drift")
        if str(manifest.get("branch") or "") != expected_branch:
            raise AutonomyError("22:57 recovery branch identity drift")
        if str(manifest.get("source_protected_head") or "") != source:
            raise AutonomyError("22:57 recovery source-head identity drift")
        matches.append((pull, manifest))

    if len(matches) > 1:
        raise AutonomyError("duplicate exact 22:57 recovery candidate")
    return matches
