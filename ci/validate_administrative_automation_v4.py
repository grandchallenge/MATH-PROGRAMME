from __future__ import annotations

import copy
import sys
from pathlib import Path

import validate_administrative_automation_v3 as legacy

implementation = legacy.implementation
ROOT = Path(__file__).resolve().parents[1]
_original_validate_workflows = legacy._original_validate_workflows


def validate_workflows_v4(config: dict) -> list[str]:
    compatibility = copy.deepcopy(config)
    validation_permissions = compatibility["workflow_permissions"].pop(
        "automation_validation"
    )
    errors = _original_validate_workflows(compatibility)

    validation_text = (
        ROOT
        / ".github"
        / "workflows"
        / "administrative-maintenance-automation-validation.yml"
    ).read_text(encoding="utf-8")
    observed = implementation.workflow_permissions(validation_text)
    if observed != validation_permissions:
        errors.append(
            "automation_validation: workflow permission drift: "
            f"{observed} != {validation_permissions}"
        )

    candidate_path = (
        ROOT
        / ".github"
        / "workflows"
        / "administrative-maintenance-candidate.yml"
    )
    synchronization_path = (
        ROOT
        / ".github"
        / "workflows"
        / "administrative-maintenance-synchronization.yml"
    )
    candidate = candidate_path.read_text(encoding="utf-8")
    synchronization = synchronization_path.read_text(encoding="utf-8")
    credential = config.get("credential_contract", {})
    environment = credential.get("environment", "")
    if environment != "release-trust":
        errors.append(
            "credential_contract: protected environment drift: "
            f"{environment!r} != 'release-trust'"
        )
    for workflow_name, text in (
        ("candidate", candidate),
        ("synchronization", synchronization),
    ):
        for marker in (
            credential.get("action", ""),
            f"secrets.{credential.get('app_id_secret', '')}",
            f"secrets.{credential.get('private_key_secret', '')}",
            f"environment: {environment}",
        ):
            if not marker or marker not in text:
                errors.append(
                    f"{workflow_name}: missing credential-contract marker {marker}"
                )
        if text.count(f"environment: {environment}") != 1:
            errors.append(
                f"{workflow_name}: protected environment must occur exactly once"
            )

    for marker in (
        "EVIDENCE_GITHUB_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "repositories: MATH-PROGRAMME",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "permission-administration: write",
        "REFEREE_TOKEN: ${{ github.token }}",
        "python ci/prepare_administrative_candidate_v4.py --apply",
        "python ci/administrative_autonomy_runtime.py execute --report",
    ):
        if marker not in candidate:
            errors.append(f"candidate: missing active-runtime marker {marker}")
    if candidate.count("${{ github.token }}") != 1:
        errors.append(
            "candidate: workflow token must be used exactly once as Referee token"
        )

    for marker in (
        "repositories: INTELLECT",
        "CROSS_REPOSITORY_MAINTENANCE_TOKEN: ${{ steps.intellect-token.outputs.token }}",
        "permission-actions: read",
        "python ci/synchronize_administrative_completion_v4.py --apply",
    ):
        if marker not in synchronization:
            errors.append(
                f"synchronization: missing active-runtime marker {marker}"
            )
    if "${{ github.token }}" in synchronization:
        errors.append(
            "synchronization: write path may not use workflow token"
        )

    runtime_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "ci").glob("administrative_autonomy_runtime*.py"))
    )
    required_runtime_markers = (
        "REFEREE_AGENT_APPROVED_EXACT_HEAD_ADMINISTRATIVE_MAINTENANCE",
        "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
        "required_pre_merge_state",
        "mergeStateStatus",
        "merge_method",
        "merged_by",
        "wait_mirror_sync",
        "human_steward_identity_asserted",
        "bypass_used",
    )
    for marker in required_runtime_markers:
        if marker not in runtime_text:
            errors.append(
                f"administrative_autonomy_runtime.py: missing control marker {marker}"
            )
    for forbidden in (
        "git push origin main",
        "/git/refs/heads/main",
        "HUMAN_STEWARD_AUTHORIZED",
    ):
        if forbidden in runtime_text:
            errors.append(
                "administrative_autonomy_runtime.py: forbidden authority token "
                f"{forbidden}"
            )

    frozen_wrapper = (
        ROOT / "ci" / "prepare_administrative_candidate_v4.py"
    ).read_text(encoding="utf-8")
    for marker in (
        "candidate_mutation_allowed",
        "frozen_occurrence_snapshot",
        "runtime_finalization_pending",
    ):
        if marker not in frozen_wrapper:
            errors.append(
                f"prepare_administrative_candidate_v4.py: missing freeze marker {marker}"
            )

    sync_wrapper = (
        ROOT / "ci" / "synchronize_administrative_completion_v4.py"
    ).read_text(encoding="utf-8")
    for marker in (
        "Routine bounded structural-sweep",
        "Human Steward disposition remains required for control-plane changes",
        "return None",
    ):
        if marker not in sync_wrapper:
            errors.append(
                f"synchronize_administrative_completion_v4.py: missing mirror marker {marker}"
            )
    return errors


legacy.validate_workflows_v3 = validate_workflows_v4
implementation.validate_workflows = validate_workflows_v4


def main() -> int:
    result = legacy.main()
    if result:
        return result
    print(
        "administrative autonomy runtime integration overlay is valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
