from __future__ import annotations

import base64
import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from administrative_automation import parse_datetime, validate_completion_state
from administrative_autonomy_receipt_stage import (
    STATE_PATH,
    advance_completion_state as ordinary_advance_completion_state,
    completion_has_receipt,
)
from administrative_autonomy_runtime_contract import record_path_for, validate_record
from administrative_autonomy_runtime_github import list_directory_names
from administrative_autonomy_runtime_mirror_sync import (
    wait_mirror_sync as ordinary_wait_mirror_sync,
)
from administrative_autonomy_runtime_structural_0121_recovery import (
    default_ancestry_checker,
    default_completion_loader,
    eligible_candidates as existing_eligible_candidates,
)
from autonomy_github import AutonomyError, content, json_content

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = (
    ROOT
    / "governance"
    / "administrative_structural_1809_late_recovery_control.json"
)
UTC = timezone.utc

EligibleFunction = Callable[
    [Any, str, dict[str, Any], datetime],
    list[tuple[dict[str, Any], dict[str, Any]]],
]
CompletionLoader = Callable[[Any, str], dict[str, Any]]
AncestryChecker = Callable[[Any, str, str], bool]
SyncEligibleFunction = Callable[
    [Any, str, dict[str, Any], dict[str, Any], int],
    dict[str, Any] | None,
]
MirrorWaiter = Callable[[Any, Any, str, str, str, str, dict[str, Any]], int]


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def _require_control(control: dict[str, Any]) -> None:
    if control.get("control_id") != "MP-ADMIN-STRUCTURAL-1809-COLLISION-RECOVERY-001":
        raise AutonomyError("18:09 collision recovery control identity drift")
    if control.get("issue") != 546:
        raise AutonomyError("18:09 collision recovery issue identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        raise AutonomyError("18:09 collision recovery control is not active")
    if control.get("protected_base_at_opening") != "52f16242b992b0326ca3f6e039b84debe126c17e":
        raise AutonomyError("18:09 collision recovery protected-base binding drift")
    correction = control.get("correction", {})
    required = {
        "global_recovery_window_minutes_unchanged": 180,
        "exact_occurrence_only": True,
        "protected_same_date_occupant_required": True,
        "stale_branch_collision_removal_allowed_for_exact_target": True,
        "ordinary_behind_sync_required_after_collision_removal": True,
        "allocator_derived_identity_required": True,
        "allocator_expected_record_id": "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-15-002",
        "exact_receipt_absence_is_recovery_condition": True,
        "later_completion_frontier_preserved": True,
        "historical_receipt_backfill_allowed_for_exact_occurrence": True,
        "mirror_current_frontier_preserved": True,
        "source_ancestry_required": True,
        "deadline_reset": False,
        "cadence_anchor_reset": False,
        "general_same_date_renumbering_authority_created": False,
        "intervening_occurrences_superseded": False,
    }
    for key, expected in required.items():
        if correction.get(key) != expected:
            raise AutonomyError(f"18:09 collision recovery control drift: {key}")
    authority = control.get("authority_boundary", {})
    if authority.get("human_steward_exact_head_authorization_required") is not True:
        raise AutonomyError("18:09 collision recovery Human Steward gate drift")
    prohibited = (
        "candidate_branch_is_authority",
        "stale_branch_artifact_is_authority",
        "bypass_created",
        "emergency_authority_created",
        "required_checks_weakened",
        "referee_gate_weakened",
        "direct_protected_push_authorized",
        "general_late_recovery_authority_created",
        "general_identity_rewrite_authority_created",
        "issue_522_or_pr_523_authority_created",
    )
    if any(authority.get(key) is not False for key in prohibited):
        raise AutonomyError("18:09 collision recovery authority boundary drift")
    claims = control.get("claim_boundaries", {})
    if not claims or any(value is not False for value in claims.values()):
        raise AutonomyError("18:09 collision recovery claim boundary drift")


def _occurrence(control: dict[str, Any]) -> dict[str, Any]:
    return control["occurrence"]


def _is_target_pair(
    pull: dict[str, Any], manifest: dict[str, Any], control: dict[str, Any]
) -> bool:
    occurrence = _occurrence(control)
    return (
        int(pull.get("number") or 0) == int(occurrence["candidate_pull_request"])
        and int(manifest.get("issue_number") or 0) == int(occurrence["candidate_issue"])
        and int(manifest.get("pull_request_number") or 0)
        == int(occurrence["candidate_pull_request"])
        and str(manifest.get("occurrence_key") or "") == str(occurrence["occurrence_key"])
        and str(manifest.get("procedure_id") or "") == str(occurrence["procedure_id"])
        and str(manifest.get("scheduled_due_at") or "") == str(occurrence["due_at_utc"])
        and str(manifest.get("branch") or "") == str(occurrence["candidate_branch"])
        and str(manifest.get("manifest_path") or "") == str(occurrence["manifest_path"])
        and str(manifest.get("source_protected_head") or "")
        == str(occurrence["original_source_protected_head"])
    )


def _require_protected_occupant(
    client: Any, repo: str, control: dict[str, Any]
) -> dict[str, Any]:
    collision = control["collision"]
    raw = content(client, repo, str(collision["stale_record_path"]), "main")
    if raw is None:
        raise AutonomyError("18:09 protected same-date occupant is absent")
    if str(raw.get("sha") or "") != str(collision["protected_occupant_blob_sha"]):
        raise AutonomyError("18:09 protected same-date occupant blob drift")
    protected = json.loads(base64.b64decode(raw["content"]))
    source = protected.get("source_candidate", {})
    if (
        str(protected.get("record_id") or "") != str(collision["stale_record_id"])
        or str(protected.get("scheduled_due_at") or "")
        != str(collision["protected_occupant_due_at_utc"])
        or str(source.get("occurrence_key") or "")
        != str(collision["protected_occupant_occurrence_key"])
        or int(source.get("issue_number") or 0)
        != int(collision["protected_occupant_issue"])
        or int(source.get("pull_request_number") or 0)
        != int(collision["protected_occupant_pull_request"])
    ):
        raise AutonomyError("18:09 protected same-date occupant identity drift")
    return protected


def _canonical_target_identity(
    client: Any,
    repo: str,
    runtime: dict[str, Any],
    manifest: dict[str, Any],
    control: dict[str, Any],
) -> tuple[str, str]:
    layout = runtime["record_layout"][manifest["procedure_id"]]
    names = list_directory_names(client, repo, layout["directory"])
    record_id, record_path = record_path_for(runtime, manifest, names)
    collision = control["collision"]
    if (
        record_id != str(collision["canonical_record_id"])
        or record_path != str(collision["canonical_record_path"])
    ):
        raise AutonomyError(
            f"18:09 allocator drift: derived {record_id} at {record_path}"
        )
    return record_id, record_path


def exact_receipt_absent(
    completion: dict[str, Any], control: dict[str, Any]
) -> bool:
    _require_control(control)
    occurrence = _occurrence(control)
    procedure = completion.get("procedures", {}).get(
        str(occurrence["procedure_id"]), {}
    )
    target = parse_datetime(str(occurrence["due_at_utc"]))
    frontier_raw = procedure.get("completed_through_utc")
    if not frontier_raw:
        raise AutonomyError("18:09 collision recovery completion frontier is absent")
    frontier = parse_datetime(str(frontier_raw))
    if frontier <= target:
        raise AutonomyError(
            "18:09 collision recovery requires a protected frontier later than the target"
        )
    due_raw = str(occurrence["due_at_utc"])
    matches = [
        item
        for item in procedure.get("receipts", [])
        if str(item.get("scheduled_due_at") or "") == due_raw
    ]
    if len(matches) > 1:
        raise AutonomyError("duplicate 18:09 completion receipts")
    return not matches


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
            "18:09 collision recovery control does not match protected ordinary recovery window"
        )
    if bounded <= ordinary:
        raise AutonomyError(
            "18:09 collision recovery continuation does not extend beyond ordinary recovery"
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
    """Admit only the exact #520 historical collision target.

    Ordinary and previously protected exact-recovery lanes retain precedence.
    The global recovery window remains unchanged; a temporary horizon is
    replayed and filtered to #520 / #521. The ordinary allocator must derive
    the canonical same-date identity from protected main.
    """

    ordinary = base(candidate, repo, runtime, now)
    if ordinary:
        return ordinary
    if now.tzinfo is None:
        raise AutonomyError("18:09 collision recovery evaluation time must include an offset")
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
            "18:09 collision recovery source is not ancestral to protected main"
        )
    _require_protected_occupant(candidate, repo, control)
    widened = copy.deepcopy(runtime)
    widened["scope"]["recovery_window_minutes_after_due"] = bounded_recovery_minutes(
        runtime, control
    )
    replayed = base(candidate, repo, widened, observed)
    matches: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for pull, manifest in replayed:
        if str(manifest.get("occurrence_key") or "") != str(
            control["occurrence"]["occurrence_key"]
        ):
            continue
        if not _is_target_pair(pull, manifest, control):
            raise AutonomyError("18:09 collision recovery target identity drift")
        _canonical_target_identity(candidate, repo, runtime, manifest, control)
        matches.append((pull, manifest))
    if len(matches) > 1:
        raise AutonomyError("duplicate exact 18:09 collision recovery candidate")
    return matches


def _branch_record(
    client: Any, repo: str, path: str, branch: str
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    raw = content(client, repo, path, branch)
    if raw is None:
        return None
    value = json.loads(base64.b64decode(raw["content"]))
    return raw, value


def _target_record_identity(
    record: dict[str, Any], control: dict[str, Any], *, canonical: bool
) -> bool:
    occurrence = control["occurrence"]
    collision = control["collision"]
    source = record.get("source_candidate", {})
    expected_record_id = (
        collision["canonical_record_id"] if canonical else collision["stale_record_id"]
    )
    return (
        str(record.get("record_id") or "") == str(expected_record_id)
        and str(record.get("scheduled_due_at") or "") == str(occurrence["due_at_utc"])
        and str(source.get("occurrence_key") or "") == str(occurrence["occurrence_key"])
        and int(source.get("issue_number") or 0) == int(occurrence["candidate_issue"])
        and int(source.get("pull_request_number") or 0)
        == int(occurrence["candidate_pull_request"])
        and str(source.get("branch") or "") == str(occurrence["candidate_branch"])
        and str(source.get("manifest_path") or "") == str(occurrence["manifest_path"])
        and str(source.get("source_protected_head") or "")
        == str(occurrence["original_source_protected_head"])
    )


def _put_canonical_record(
    candidate: Any,
    repo: str,
    branch: str,
    path: str,
    record: dict[str, Any],
) -> str:
    payload = {
        "message": (
            "Normalize exact #520 autonomous record to allocator-derived same-date identity"
        ),
        "content": base64.b64encode(
            (json.dumps(record, indent=2) + "\n").encode("utf-8")
        ).decode("ascii"),
        "branch": branch,
    }
    result = candidate.put(f"/repos/{repo}/contents/{path}", payload)
    commit_sha = str((result or {}).get("commit", {}).get("sha") or "")
    if len(commit_sha) != 40:
        raise AutonomyError("18:09 canonical record write readback failed")
    return commit_sha


def normalize_target_collision(
    candidate: Any,
    repo: str,
    runtime: dict[str, Any],
    pull: dict[str, Any],
    manifest: dict[str, Any],
) -> dict[str, Any] | None:
    """Move only the stale #520 record to its allocator-derived path.

    The historical record body is preserved. Only ``record_id`` changes, from
    stale colliding ``...-001`` to protected allocator result ``...-002``.
    The old branch artifact is then removed before ordinary protected-main sync.
    """

    control = load_control()
    _require_control(control)
    if not _is_target_pair(pull, manifest, control):
        return None
    _require_protected_occupant(candidate, repo, control)
    _canonical_target_identity(candidate, repo, runtime, manifest, control)
    collision = control["collision"]
    stale_path = str(collision["stale_record_path"])
    canonical_path = str(collision["canonical_record_path"])
    branch = str(control["occurrence"]["candidate_branch"])
    stale_value = _branch_record(candidate, repo, stale_path, branch)
    canonical_value = _branch_record(candidate, repo, canonical_path, branch)
    if stale_value is None:
        if canonical_value is None or not _target_record_identity(
            canonical_value[1], control, canonical=True
        ):
            raise AutonomyError(
                "18:09 collision normalization lost stale record without canonical replacement"
            )
        return None
    stale_raw, stale_record = stale_value
    stale_source = stale_record.get("source_candidate", {})
    if (
        str(stale_record.get("record_id") or "") == str(collision["stale_record_id"])
        and str(stale_record.get("scheduled_due_at") or "")
        == str(collision["protected_occupant_due_at_utc"])
        and str(stale_source.get("occurrence_key") or "")
        == str(collision["protected_occupant_occurrence_key"])
        and int(stale_source.get("issue_number") or 0)
        == int(collision["protected_occupant_issue"])
        and int(stale_source.get("pull_request_number") or 0)
        == int(collision["protected_occupant_pull_request"])
    ):
        if canonical_value is None or not _target_record_identity(
            canonical_value[1], control, canonical=True
        ):
            raise AutonomyError(
                "18:09 inherited protected occupant lacks normalized canonical target record"
            )
        return None
    if (
        str(stale_raw.get("sha") or "") != str(collision["stale_branch_blob_sha"])
        or not _target_record_identity(stale_record, control, canonical=False)
    ):
        raise AutonomyError("18:09 stale target-branch collision identity drift")
    canonical_record = copy.deepcopy(stale_record)
    canonical_record["record_id"] = str(collision["canonical_record_id"])
    errors = validate_record(canonical_record)
    if errors:
        raise AutonomyError(
            "18:09 canonicalized historical record invalid: " + "; ".join(errors)
        )
    canonical_write_commit = ""
    if canonical_value is None:
        canonical_write_commit = _put_canonical_record(
            candidate, repo, branch, canonical_path, canonical_record
        )
    elif canonical_value[1] != canonical_record:
        raise AutonomyError("18:09 canonical target record already exists with drift")
    result = candidate.call(
        "DELETE",
        f"/repos/{repo}/contents/{stale_path}",
        {
            "message": (
                "Remove exact #520 stale same-date record collision before protected-main synchronization"
            ),
            "sha": str(stale_raw["sha"]),
            "branch": branch,
        },
    )
    removal_commit = str((result or {}).get("commit", {}).get("sha") or "")
    if len(removal_commit) != 40:
        raise AutonomyError("18:09 collision removal commit readback failed")
    return {
        "pull_request": int(control["occurrence"]["candidate_pull_request"]),
        "removed_path": stale_path,
        "removed_blob_sha": str(stale_raw["sha"]),
        "canonical_record_id": str(collision["canonical_record_id"]),
        "canonical_record_path": canonical_path,
        "canonical_write_commit": canonical_write_commit or None,
        "normalization_commit": removal_commit,
        "historical_record_body_preserved": True,
        "protected_authority_created": False,
    }


def synchronize_eligible_candidate(
    candidate: Any,
    repo: str,
    runtime: dict[str, Any],
    behind_control: dict[str, Any],
    attempt: int,
    *,
    base: SyncEligibleFunction,
) -> dict[str, Any] | None:
    """Normalize exact #520 collision, then invoke ordinary BEHIND sync."""

    eligible = eligible_candidates(candidate, repo, runtime, datetime.now(UTC))
    if len(eligible) > 1:
        raise AutonomyError(
            "multiple frozen maintenance candidates require fail-closed triage"
        )
    normalization = None
    if eligible:
        pull, manifest = eligible[0]
        control = load_control()
        if _is_target_pair(pull, manifest, control):
            normalization = normalize_target_collision(
                candidate, repo, runtime, pull, manifest
            )
    event = base(candidate, repo, runtime, behind_control, attempt)
    if normalization is None:
        return event
    if event is None:
        return {
            "trigger": "EXACT_1809_IDENTITY_COLLISION_NORMALIZATION",
            **normalization,
            "ordinary_behind_sync_event": None,
        }
    return {
        "trigger": "EXACT_1809_IDENTITY_COLLISION_NORMALIZATION_AND_BEHIND",
        **normalization,
        "ordinary_behind_sync_event": event,
    }


def _target_receipt(receipt: dict[str, Any], control: dict[str, Any]) -> bool:
    occurrence = control["occurrence"]
    collision = control["collision"]
    return (
        str(receipt.get("procedure_id") or "") == str(occurrence["procedure_id"])
        and str(receipt.get("scheduled_due_at") or "") == str(occurrence["due_at_utc"])
        and str(receipt.get("record_path") or "") == str(collision["canonical_record_path"])
        and int(receipt.get("pull_request") or 0)
        == int(occurrence["candidate_pull_request"])
    )


def advance_completion_state(
    current: dict[str, Any],
    receipt: dict[str, Any],
    protected_record_merge: str,
    base: Callable[
        [dict[str, Any], dict[str, Any], str], dict[str, Any]
    ] = ordinary_advance_completion_state,
) -> dict[str, Any]:
    """Insert only the exact corrected #520 receipt behind a later frontier."""

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
        raise AutonomyError("18:09 historical receipt identity drift")
    if completion_has_receipt(current, receipt):
        return current
    completion = copy.deepcopy(current)
    procedure = completion.get("procedures", {}).get(procedure_id)
    if not isinstance(procedure, dict):
        raise AutonomyError("18:09 collision recovery ledger procedure is absent")
    frontier_raw = procedure.get("completed_through_utc")
    if not frontier_raw:
        raise AutonomyError("18:09 collision recovery completion frontier is absent")
    target = parse_datetime(target_due)
    frontier = parse_datetime(str(frontier_raw))
    if frontier <= target:
        raise AutonomyError(
            "18:09 historical receipt backfill requires a later protected frontier"
        )
    receipts = list(procedure.get("receipts", []))
    if any(
        str(item.get("scheduled_due_at") or "") == target_due
        for item in receipts
    ):
        raise AutonomyError("conflicting exact 18:09 historical receipt")
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
    base: MirrorWaiter = ordinary_wait_mirror_sync,
) -> int:
    """Bind exact #520 backfill to mirrors of the preserved current frontier."""

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
        raise AutonomyError("18:09 mirror readback completion ledger is absent")
    procedure = completion.get("procedures", {}).get(target_procedure, {})
    matches = [
        item for item in procedure.get("receipts", []) if _target_receipt(item, control)
    ]
    if len(matches) != 1:
        raise AutonomyError(
            "18:09 mirror readback requires exactly one corrected protected receipt"
        )
    frontier_raw = str(procedure.get("completed_through_utc") or "")
    if not frontier_raw:
        raise AutonomyError("18:09 mirror readback frontier is absent")
    if parse_datetime(frontier_raw) <= parse_datetime(target_due):
        raise AutonomyError(
            "18:09 mirror readback did not preserve the later completion frontier"
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
