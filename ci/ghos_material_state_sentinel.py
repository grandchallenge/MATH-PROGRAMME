"""Detect GHOS estate-membership drift without mutating governed state.

This module is deliberately library-only. It classifies a caller-supplied live
repository snapshot against the frozen estate in the protected GHOS campaign.
It creates no authority, performs no network access, and makes no repository or
ruleset changes.
"""
from __future__ import annotations

from typing import Any

SCHEMA_VERSION = "1.0.0"
DETECTOR_ID = "GHOS_ESTATE_MEMBERSHIP_SENTINEL"

UNCHANGED = "UNCHANGED"
NEW_ESTATE_MEMBER = "NEW_ESTATE_MEMBER_SUCCESSOR_ADMISSION_REQUIRED"
ESTATE_MEMBER_REMOVED_OR_ARCHIVED = "ESTATE_MEMBER_REMOVED_OR_ARCHIVED"
UNKNOWN_FAIL_CLOSED = "UNKNOWN_FAIL_CLOSED"

ROUTES = {
    UNCHANGED: "REUSE_MATERIALLY_UNCHANGED_ESTATE_MEMBERSHIP_EVIDENCE",
    NEW_ESTATE_MEMBER: "OPEN_SUCCESSOR_ESTATE_ADMISSION_TRANSACTION",
    ESTATE_MEMBER_REMOVED_OR_ARCHIVED: "OPEN_SUCCESSOR_ESTATE_MEMBERSHIP_DISPOSITION",
    UNKNOWN_FAIL_CLOSED: "INVESTIGATE_IDENTITY_OR_SNAPSHOT_AMBIGUITY_BEFORE_TRANSITION",
}

AUTHORITY_BOUNDARY = {
    "detect_only": True,
    "may_modify_terminal_ghos_evidence": False,
    "may_admit_repository": False,
    "may_modify_workflows_or_routing": False,
    "may_modify_rulesets_or_protection": False,
    "may_expand_controller_authority": False,
    "may_authorize_mathematical_or_certification_claims": False,
    "may_authorize_publication_or_external_claims": False,
}


def _repository_entry(value: Any, *, live: bool) -> tuple[dict[str, Any] | None, str | None]:
    if not isinstance(value, dict):
        return None, "repository entry must be an object"
    repository = value.get("repository")
    repository_id = value.get("repository_id")
    if not isinstance(repository, str) or "/" not in repository:
        return None, "repository entry requires owner/name repository"
    if not isinstance(repository_id, int) or isinstance(repository_id, bool) or repository_id <= 0:
        return None, f"{repository}: repository_id must be a positive integer"
    entry: dict[str, Any] = {
        "repository": repository,
        "repository_id": repository_id,
    }
    if live:
        archived = value.get("archived", False)
        if not isinstance(archived, bool):
            return None, f"{repository}: archived must be boolean"
        entry["archived"] = archived
    return entry, None


def _normalise_entries(values: Any, *, live: bool) -> tuple[list[dict[str, Any]], list[str]]:
    if not isinstance(values, list):
        return [], ["repository population must be an array"]
    entries: list[dict[str, Any]] = []
    errors: list[str] = []
    names: set[str] = set()
    ids: set[int] = set()
    for index, value in enumerate(values):
        entry, error = _repository_entry(value, live=live)
        if error:
            errors.append(f"entry {index}: {error}")
            continue
        assert entry is not None
        name = str(entry["repository"])
        repository_id = int(entry["repository_id"])
        if name in names:
            errors.append(f"duplicate repository name: {name}")
        if repository_id in ids:
            errors.append(f"duplicate repository_id: {repository_id}")
        names.add(name)
        ids.add(repository_id)
        entries.append(entry)
    return entries, errors


def classify_estate_membership(
    campaign: dict[str, Any],
    live_snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Classify live estate membership against the frozen GHOS campaign population."""
    errors: list[str] = []
    if not isinstance(campaign, dict):
        campaign = {}
        errors.append("campaign must be a JSON object")
    if not isinstance(live_snapshot, dict):
        live_snapshot = {}
        errors.append("live snapshot must be a JSON object")

    campaign_id = campaign.get("campaign_id")
    if not isinstance(campaign_id, str) or not campaign_id:
        errors.append("campaign_id is required")

    if live_snapshot.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"live snapshot schema_version must be {SCHEMA_VERSION}")

    baseline, baseline_errors = _normalise_entries(campaign.get("estate"), live=False)
    observed, observed_errors = _normalise_entries(
        live_snapshot.get("repositories"),
        live=True,
    )
    errors.extend(f"baseline: {error}" for error in baseline_errors)
    errors.extend(f"live: {error}" for error in observed_errors)

    baseline_by_id = {int(item["repository_id"]): item for item in baseline}
    baseline_by_name = {str(item["repository"]): item for item in baseline}
    observed_by_id = {int(item["repository_id"]): item for item in observed}
    observed_by_name = {str(item["repository"]): item for item in observed}

    for name, baseline_entry in baseline_by_name.items():
        live_entry = observed_by_name.get(name)
        if live_entry is not None and live_entry["repository_id"] != baseline_entry["repository_id"]:
            errors.append(
                f"repository identity mismatch for {name}: "
                f"baseline id {baseline_entry['repository_id']}, "
                f"live id {live_entry['repository_id']}"
            )
    for repository_id, baseline_entry in baseline_by_id.items():
        live_entry = observed_by_id.get(repository_id)
        if live_entry is not None and live_entry["repository"] != baseline_entry["repository"]:
            errors.append(
                f"repository rename/replacement ambiguity for id {repository_id}: "
                f"baseline {baseline_entry['repository']}, live {live_entry['repository']}"
            )

    new_members = sorted(
        (
            item
            for repository_id, item in observed_by_id.items()
            if repository_id not in baseline_by_id
        ),
        key=lambda item: (str(item["repository"]), int(item["repository_id"])),
    )
    missing_members = sorted(
        (
            item
            for repository_id, item in baseline_by_id.items()
            if repository_id not in observed_by_id
        ),
        key=lambda item: (str(item["repository"]), int(item["repository_id"])),
    )
    archived_members = sorted(
        (
            {
                "repository": baseline_by_id[repository_id]["repository"],
                "repository_id": repository_id,
            }
            for repository_id, item in observed_by_id.items()
            if repository_id in baseline_by_id and bool(item.get("archived", False))
        ),
        key=lambda item: (str(item["repository"]), int(item["repository_id"])),
    )

    composite_membership_change = bool(new_members and (missing_members or archived_members))
    if composite_membership_change:
        errors.append(
            "simultaneous new and removed/archived membership requires fail-closed disposition"
        )

    if errors:
        result = UNKNOWN_FAIL_CLOSED
    elif new_members:
        result = NEW_ESTATE_MEMBER
    elif missing_members or archived_members:
        result = ESTATE_MEMBER_REMOVED_OR_ARCHIVED
    else:
        result = UNCHANGED

    active_count = sum(not bool(item.get("archived", False)) for item in observed)
    return {
        "schema_version": SCHEMA_VERSION,
        "detector_id": DETECTOR_ID,
        "campaign_id": campaign_id,
        "result": result,
        "route": ROUTES[result],
        "baseline": {
            "repository_count": len(baseline),
        },
        "observed": {
            "repository_count": len(observed),
            "active_unarchived_repository_count": active_count,
        },
        "findings": {
            "new_repositories": new_members,
            "missing_baseline_repositories": missing_members,
            "archived_baseline_repositories": archived_members,
            "errors": errors,
        },
        "historical_terminal_rewrite_permitted": False,
        "authority_boundary": dict(AUTHORITY_BOUNDARY),
    }
