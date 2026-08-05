from __future__ import annotations

import copy
from pathlib import Path

import validate_administrative_automation_v2 as routed

implementation = routed.implementation
ROOT = Path(__file__).resolve().parents[1]
_original_validate_workflows = implementation.validate_workflows
RUNTIME_EXTENSION_PATHS = [
    ROOT / "ci" / "prepare_administrative_candidate_v3.py",
    ROOT / "ci" / "synchronize_administrative_completion_v3.py",
]
FORBIDDEN_RUNTIME_CAPABILITIES = (
    "/merges",
    "merge_pull_request",
    "enable_auto_merge",
    "dismiss_pull_request_review",
    "branch_protection_rule",
)


def validate_workflows_v3(config: dict) -> list[str]:
    compatibility = copy.deepcopy(config)
    validation_permissions = compatibility["workflow_permissions"].pop("automation_validation")
    errors = _original_validate_workflows(compatibility)

    validation_text = (ROOT / ".github" / "workflows" / "administrative-maintenance-automation-validation.yml").read_text(encoding="utf-8")
    observed = implementation.workflow_permissions(validation_text)
    if observed != validation_permissions:
        errors.append(f"automation_validation: workflow permission drift: {observed} != {validation_permissions}")

    candidate = (ROOT / ".github" / "workflows" / "administrative-maintenance-candidate.yml").read_text(encoding="utf-8")
    synchronization = (ROOT / ".github" / "workflows" / "administrative-maintenance-synchronization.yml").read_text(encoding="utf-8")
    credential = config.get("credential_contract", {})
    for workflow_name, text in (("candidate", candidate), ("synchronization", synchronization)):
        for marker in (
            credential.get("action", ""),
            f"secrets.{credential.get('app_id_secret', '')}",
            f"secrets.{credential.get('private_key_secret', '')}",
        ):
            if not marker or marker not in text:
                errors.append(f"{workflow_name}: missing credential-contract marker {marker}")
        if "${{ github.token }}" in text:
            errors.append(f"{workflow_name}: write path may not use workflow token")

    for marker in (
        "EVIDENCE_GITHUB_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "repositories: MATH-PROGRAMME",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "python ci/prepare_administrative_candidate_v3.py --apply",
    ):
        if marker not in candidate:
            errors.append(f"candidate: missing split-token marker {marker}")

    for marker in (
        "repositories: INTELLECT",
        "CROSS_REPOSITORY_MAINTENANCE_TOKEN: ${{ steps.intellect-token.outputs.token }}",
        "permission-actions: read",
        "python ci/synchronize_administrative_completion_v3.py --apply",
    ):
        if marker not in synchronization:
            errors.append(f"synchronization: missing split-token marker {marker}")

    for path in RUNTIME_EXTENSION_PATHS:
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_RUNTIME_CAPABILITIES:
            if token in text:
                errors.append(f"{path.name}: forbidden authority capability token {token}")
    return errors


implementation.validate_workflows = validate_workflows_v3


if __name__ == "__main__":
    raise SystemExit(routed.main())
