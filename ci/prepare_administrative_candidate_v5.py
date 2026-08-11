from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import administrative_automation as automation
import prepare_administrative_candidate_v4 as v4

implementation = v4.implementation
ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = ROOT / "governance" / "administrative_transition_recovery_candidate_control.json"

_original_preparation_occurrences = implementation.preparation_occurrences
_original_candidate_mutation_allowed = implementation.candidate_mutation_allowed

UTC = timezone.utc


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def observed_utc(now: datetime) -> datetime:
    if now.tzinfo is None:
        raise automation.AutomationError("transition-recovery evaluation time must include an offset")
    return now.astimezone(UTC)


def successor_record_active(control: dict[str, Any]) -> bool:
    path = ROOT / control["successor"]["record_path"]
    if not path.exists():
        return False
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        record.get("successor_id") == control["successor"]["successor_id"]
        and record.get("status") == control["successor"]["required_status"]
        and record.get("cadence_anchor_utc") == "2026-08-01T01:21:00Z"
    )


def successor_merge_ancestral(control: dict[str, Any]) -> bool:
    merge = str(control["successor"]["protected_merge"])
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", merge, "HEAD"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def completion_absent(completion: dict[str, Any], control: dict[str, Any]) -> bool:
    due = automation.parse_datetime(control["occurrence"]["scheduled_due_at"])
    state = completion.get("procedures", {}).get("structural_sweep", {})
    completed_raw = state.get("completed_through_utc")
    if completed_raw and automation.parse_datetime(str(completed_raw)) >= due:
        return False
    for receipt in state.get("receipts", []):
        if receipt.get("scheduled_due_at") == control["occurrence"]["scheduled_due_at"]:
            return False
    return True


def protected_record_exists_for_occurrence(control: dict[str, Any]) -> bool:
    due = control["occurrence"]["scheduled_due_at"]
    for path in sorted((ROOT / "governance" / "administrative_structural_sweeps").glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if record.get("scheduled_due_at") != due:
            continue
        status = str(record.get("status", ""))
        if status.startswith("COMPLETE") or status.startswith("PROTECTED_"):
            return True
    return False


def within_reconstruction_window(now: datetime, control: dict[str, Any]) -> bool:
    observed = observed_utc(now)
    not_before = automation.parse_datetime(control["occurrence"]["reconstruction_not_before_utc"])
    expires = automation.parse_datetime(control["occurrence"]["reconstruction_expires_at_utc"])
    return not_before < observed < expires


def transition_reconstruction_allowed(
    now: datetime,
    completion: dict[str, Any],
    control: dict[str, Any] | None = None,
) -> bool:
    value = load_control() if control is None else control
    if value.get("control_id") != "MP-ADMIN-TRANSITION-RECOVERY-CANDIDATE-001":
        return False
    if value.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        return False
    if not within_reconstruction_window(now, value):
        return False
    if not successor_record_active(value) or not successor_merge_ancestral(value):
        return False
    if not completion_absent(completion, value):
        return False
    if protected_record_exists_for_occurrence(value):
        return False
    return True


def transition_reconstruction_occurrence(
    config: dict[str, Any],
    registry: dict[str, Any],
    completion: dict[str, Any],
    now: datetime,
) -> Any | None:
    control = load_control()
    if not transition_reconstruction_allowed(now, completion, control):
        return None

    procedure_id = control["occurrence"]["procedure_id"]
    registry_row = next(
        (row for row in registry["procedures"] if row.get("id") == procedure_id),
        None,
    )
    if registry_row is None:
        raise automation.AutomationError("transition-recovery procedure missing from trigger registry")

    due = automation.parse_datetime(control["occurrence"]["scheduled_due_at"])
    completed_raw = completion.get("procedures", {}).get(procedure_id, {}).get("completed_through_utc")
    completed = automation.parse_datetime(completed_raw) if completed_raw else None
    if due not in set(automation.iter_due_occurrences(registry_row, completed)):
        raise automation.AutomationError("transition-recovery occurrence is not on the protected cadence")

    occurrence = automation.build_occurrence(config, procedure_id, due)
    expected = control["occurrence"]
    if (
        occurrence.occurrence_key != expected["occurrence_key"]
        or automation.iso_z(occurrence.prepare_at) != expected["original_prepare_at"]
        or automation.iso_z(occurrence.freeze_at) != expected["original_freeze_at"]
    ):
        raise automation.AutomationError("transition-recovery occurrence identity drift")
    return occurrence


def preparation_occurrences(
    config: dict[str, Any],
    registry: dict[str, Any],
    completion: dict[str, Any],
    now: datetime,
) -> list[Any]:
    ordinary = list(_original_preparation_occurrences(config, registry, completion, now))
    recovery = transition_reconstruction_occurrence(config, registry, completion, now)
    if recovery and all(item.occurrence_key != recovery.occurrence_key for item in ordinary):
        ordinary.append(recovery)
    return sorted(ordinary, key=lambda item: (item.due_at, item.procedure_id))


def candidate_artifact_snapshot(client: Any, repository: str, occurrence: Any) -> tuple[Any, Any, Any, Any]:
    marker = implementation.issue_marker(occurrence.occurrence_key)
    issue = implementation.find_issue(client, repository, marker)
    branch = implementation.get_branch(client, repository, occurrence.branch_name)
    pull_request = implementation.find_pull_request(client, repository, occurrence.branch_name)
    manifest = None
    if branch:
        manifest = implementation.get_content(
            client,
            repository,
            occurrence.manifest_path,
            occurrence.branch_name,
        )
    return issue, branch, pull_request, manifest


def transition_reconstruction_mutation_allowed(occurrence: Any, now: datetime) -> bool:
    control = load_control()
    if occurrence.occurrence_key != control["occurrence"]["occurrence_key"]:
        return False
    if not within_reconstruction_window(now, control):
        return False
    if not successor_record_active(control) or not successor_merge_ancestral(control):
        return False
    if protected_record_exists_for_occurrence(control):
        return False
    return True


def reconstruct_missing_candidate(
    client: Any,
    repository: str,
    occurrence: Any,
    now: datetime,
    state: list[dict[str, Any]],
) -> dict[str, Any]:
    issue, branch, pull_request, manifest = candidate_artifact_snapshot(
        client, repository, occurrence
    )
    present = tuple(item is not None for item in (issue, branch, pull_request, manifest))
    if any(present):
        if not all(present):
            raise automation.AutomationError(
                f"{occurrence.occurrence_key}: partial transition-recovery candidate artifacts"
            )
        return v4.frozen_occurrence_snapshot(client, repository, occurrence)

    original_predicate = implementation.candidate_mutation_allowed

    def bounded_predicate(candidate_occurrence: Any, observed: datetime) -> bool:
        if candidate_occurrence.occurrence_key == occurrence.occurrence_key:
            return transition_reconstruction_mutation_allowed(candidate_occurrence, observed)
        return original_predicate(candidate_occurrence, observed)

    implementation.candidate_mutation_allowed = bounded_predicate
    try:
        result = v4._original_apply_occurrence(
            client,
            repository,
            occurrence,
            now,
            state,
        )
    finally:
        implementation.candidate_mutation_allowed = original_predicate

    result.update(
        {
            "transition_reconstruction": True,
            "reconstruction_control_id": "MP-ADMIN-TRANSITION-RECOVERY-CANDIDATE-001",
            "reconstructed_at": automation.iso_z(observed_utc(now)),
            "original_deadline_preserved": True,
            "lateness_preserved": True,
        }
    )
    return result


def apply_occurrence(
    client: Any,
    repository: str,
    occurrence: Any,
    now: datetime,
    state: list[dict[str, Any]],
) -> dict[str, Any]:
    if transition_reconstruction_mutation_allowed(occurrence, now):
        return reconstruct_missing_candidate(client, repository, occurrence, now, state)
    return v4.apply_occurrence(client, repository, occurrence, now, state)


implementation.preparation_occurrences = preparation_occurrences
implementation.apply_occurrence = apply_occurrence


if __name__ == "__main__":
    raise SystemExit(implementation.main())
