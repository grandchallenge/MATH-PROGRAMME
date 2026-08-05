from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

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
ATTESTATION_PATH = ROOT / "governance" / "administrative_maintenance_automation_post_merge_attestation.json"
ATTESTATION_SCHEMA_PATH = ROOT / "schemas" / "administrative_maintenance_automation_post_merge_attestation.schema.json"


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
    environment = credential.get("environment", "")
    if environment != "release-trust":
        errors.append(f"credential_contract: protected environment drift: {environment!r} != 'release-trust'")
    for workflow_name, text in (("candidate", candidate), ("synchronization", synchronization)):
        for marker in (
            credential.get("action", ""),
            f"secrets.{credential.get('app_id_secret', '')}",
            f"secrets.{credential.get('private_key_secret', '')}",
            f"environment: {environment}",
        ):
            if not marker or marker not in text:
                errors.append(f"{workflow_name}: missing credential-contract marker {marker}")
        if text.count(f"environment: {environment}") != 1:
            errors.append(f"{workflow_name}: protected environment must occur exactly once")
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


def validate_post_merge_attestation() -> list[str]:
    errors: list[str] = []
    try:
        schema = json.loads(ATTESTATION_SCHEMA_PATH.read_text(encoding="utf-8"))
        record = json.loads(ATTESTATION_PATH.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for failure in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
            location = ".".join(str(part) for part in failure.absolute_path) or "$"
            errors.append(f"post_merge_attestation:{location}: {failure.message}")
        detail = record.get("failure_detail", "")
        if "release-trust" not in detail or "GCL_RELEASE_TRUST_APP_ID" not in detail:
            errors.append("post_merge_attestation: failure detail must bind the protected environment and unavailable App ID")
        if record.get("remediation_state") != "PENDING_PROTECTED_REMEDIATION_MERGE":
            errors.append("post_merge_attestation: pre-merge remediation record may not declare protected completion")
        if record.get("protected_completion_declared") is not False:
            errors.append("post_merge_attestation: protected completion must remain false before corrective protected merge and replay")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"post_merge_attestation: unreadable record or schema: {exc}")
    return errors


validate_workflows = validate_workflows_v3
implementation.validate_workflows = validate_workflows_v3


def main() -> int:
    result = routed.main()
    if result:
        return result
    errors = validate_post_merge_attestation()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"administrative automation post-merge attestation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("administrative automation post-merge attestation is valid and remains pending protected remediation merge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
