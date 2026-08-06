from __future__ import annotations

import base64
import json
from typing import Any

import administrative_automation as automation
import prepare_administrative_candidate_v3 as v3

implementation = v3.implementation
_original_apply_occurrence = implementation.apply_occurrence


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
    if automation.candidate_mutation_allowed(occurrence, now):
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
