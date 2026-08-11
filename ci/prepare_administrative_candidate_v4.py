from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

import administrative_automation as automation
import prepare_administrative_candidate_v3 as v3

implementation = v3.implementation
_original_apply_occurrence = implementation.apply_occurrence

ROOT = Path(__file__).resolve().parents[1]
SUCCESSOR_RECORD = ROOT / "governance" / "administrative_maintenance_steady_state_0_1.json"
TRANSITION_OCCURRENCE_KEY = "structural_sweep:2026-08-10T03:45:00Z"
SUCCESSOR_ID = "MP-ADMIN-STEADY-STATE-0.1-001"


def successor_transition_mutation_allowed(occurrence: Any, now: Any) -> bool:
    """Permit one bounded transition candidate after the ordinary freeze.

    The first post-pilot structural occurrence begins its normal preparation
    window before the pilot disposition can create successor authority.  Once
    the successor record is on protected main, allow that exact occurrence to
    be created/reconciled until its unchanged due time.  This does not alter
    its deadline, required checks, review, merge, or lateness accounting.
    """
    if occurrence.occurrence_key != TRANSITION_OCCURRENCE_KEY:
        return False
    if now >= occurrence.due_at or not SUCCESSOR_RECORD.exists():
        return False
    try:
        record = json.loads(SUCCESSOR_RECORD.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        record.get("successor_id") == SUCCESSOR_ID
        and record.get("status") == "ACTIVE_ON_PROTECTED_MERGE"
        and record.get("pilot_boundary_utc") == "2026-08-10T01:21:00Z"
        and record.get("cadence_anchor_utc") == "2026-08-01T01:21:00Z"
    )


def frozen_occurrence_snapshot(
    client: Any,
    repository: str,
    occurrence: Any,
) -> dict[str, Any]:
    marker = implementation.issue_marker(occurrence.occurrence_key)
    issue = implementation.find_issue(client, repository, marker)
    branch = implementation.get_branch(client, repository, occurrence.branch_name)
    pull_request = implementation.find_pull_request(client, repository, occurrence.branch_name)
    existing = implementation.get_content(
        client,
        repository,
        occurrence.manifest_path,
        occurrence.branch_name,
    )
    if not (issue and branch and pull_request and existing):
        raise automation.AutomationError(
            f"{occurrence.occurrence_key}: candidate missing after automated mutation freeze"
        )
    manifest = json.loads(base64.b64decode(existing["content"]).decode("utf-8"))
    errors = automation.validate_candidate_manifest(manifest, occurrence)
    if errors:
        raise automation.AutomationError("; ".join(errors))
    if (
        manifest.get("issue_number") != issue.get("number")
        or manifest.get("pull_request_number") != pull_request.get("number")
        or manifest.get("branch") != occurrence.branch_name
    ):
        raise automation.AutomationError(
            f"{occurrence.occurrence_key}: frozen candidate identity drift"
        )
    if pull_request.get("state") != "open":
        raise automation.AutomationError(
            f"{occurrence.occurrence_key}: frozen candidate pull request is not open"
        )
    return {
        "occurrence_key": occurrence.occurrence_key,
        "issue_number": issue["number"],
        "branch": occurrence.branch_name,
        "pull_request_number": pull_request["number"],
        "manifest_path": occurrence.manifest_path,
        "source_protected_head": manifest["source_protected_head"],
        "frozen": True,
        "manifest_changed": False,
        "runtime_finalization_pending": True,
        "pull_request_draft": bool(pull_request.get("draft")),
    }


def apply_occurrence(
    client: Any,
    repository: str,
    occurrence: Any,
    now: Any,
    state: list[dict[str, Any]],
) -> dict[str, Any]:
    if automation.candidate_mutation_allowed(occurrence, now) or successor_transition_mutation_allowed(occurrence, now):
        return _original_apply_occurrence(
            client,
            repository,
            occurrence,
            now,
            state,
        )
    return frozen_occurrence_snapshot(client, repository, occurrence)


implementation.apply_occurrence = apply_occurrence


if __name__ == "__main__":
    raise SystemExit(implementation.main())
