#!/usr/bin/env python3
from __future__ import annotations

import sys
from typing import Any

import validate_workflow_coverage as legacy

ROOT = legacy.ROOT
EXTRA_WORKFLOWS = {
    "administrative-maintenance-automation-validation.yml",
    "administrative-maintenance-candidate.yml",
    "administrative-maintenance-synchronization.yml",
}
legacy.EXPECTED_WORKFLOWS = set(legacy.EXPECTED_WORKFLOWS) | EXTRA_WORKFLOWS

APP_ACTION = "actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1"
APP_ID = "app-id: ${{ secrets.GCL_RELEASE_TRUST_APP_ID }}"
APP_KEY = "private-key: ${{ secrets.GCL_RELEASE_TRUST_PRIVATE_KEY }}"


def _trigger(workflow: dict[str, Any]) -> dict[str, Any]:
    value = workflow.get("on", {})
    return value if isinstance(value, dict) else {}


def automation_workflow_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    required = EXTRA_WORKFLOWS
    if not required <= set(texts):
        return errors

    parsed = {name: legacy.load_yaml_text(texts[name]) for name in required}
    candidate = parsed["administrative-maintenance-candidate.yml"]
    synchronization = parsed["administrative-maintenance-synchronization.yml"]
    validation = parsed["administrative-maintenance-automation-validation.yml"]
    candidate_text = texts["administrative-maintenance-candidate.yml"]
    synchronization_text = texts["administrative-maintenance-synchronization.yml"]
    validation_text = texts["administrative-maintenance-automation-validation.yml"]

    candidate_trigger = _trigger(candidate)
    if set(candidate_trigger) != {"schedule", "workflow_dispatch"}:
        errors.append("administrative-maintenance-candidate.yml: triggers must be exactly schedule and workflow_dispatch")
    synchronization_trigger = _trigger(synchronization)
    if set(synchronization_trigger) != {"workflow_run", "workflow_dispatch"}:
        errors.append("administrative-maintenance-synchronization.yml: triggers must be exactly workflow_run and workflow_dispatch")
    validation_trigger = _trigger(validation)
    if set(validation_trigger) != {"pull_request", "push", "workflow_dispatch"}:
        errors.append("administrative-maintenance-automation-validation.yml: triggers must cover pull_request, push, and workflow_dispatch only")

    for workflow_name, text in (
        ("administrative-maintenance-candidate.yml", candidate_text),
        ("administrative-maintenance-synchronization.yml", synchronization_text),
    ):
        for marker in (APP_ACTION, APP_ID, APP_KEY):
            if marker not in text:
                errors.append(f"{workflow_name}: missing scoped GitHub App marker {marker}")
        if "github.token" in text:
            errors.append(f"{workflow_name}: write path may not use the workflow GITHUB_TOKEN")
        for forbidden in (
            "merge_pull_request",
            "enable_auto_merge",
            "gh pr merge",
            "/merges",
            "permission-administration: write",
            "permission-checks: write",
        ):
            if forbidden in text:
                errors.append(f"{workflow_name}: forbidden merge or administration capability {forbidden}")

    candidate_markers = (
        "repositories: MATH-PROGRAMME",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "MATHFORGE\n            MATHSOLVE\n            MATHCERT\n            INTELLECT",
        "permission-contents: read",
        "permission-pull-requests: read",
        "EVIDENCE_GITHUB_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "python ci/prepare_administrative_candidate_v3.py --apply",
        "CANDIDATE_PREPARATION_FAILED_CLOSED",
    )
    for marker in candidate_markers:
        if marker not in candidate_text:
            errors.append(f"administrative-maintenance-candidate.yml: missing bounded candidate marker {marker}")
    if candidate_text.count("permission-contents: write") != 1:
        errors.append("administrative-maintenance-candidate.yml: exactly one repository-scoped contents write token is required")

    sync_markers = (
        "repositories: MATH-PROGRAMME",
        "permission-actions: read",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "repositories: INTELLECT",
        "CROSS_REPOSITORY_MAINTENANCE_TOKEN: ${{ steps.intellect-token.outputs.token }}",
        "github.event.workflow_run.head_branch == 'main'",
        "github.event.workflow_run.conclusion == 'success'",
        "python ci/synchronize_administrative_completion_v3.py --apply",
        "SYNCHRONIZATION_FAILED_CLOSED",
    )
    for marker in sync_markers:
        if marker not in synchronization_text:
            errors.append(f"administrative-maintenance-synchronization.yml: missing bounded synchronization marker {marker}")
    if synchronization_text.count("permission-contents: write") != 1:
        errors.append("administrative-maintenance-synchronization.yml: exactly one MATH-PROGRAMME contents write token is required")
    if synchronization_text.count("permission-issues: write") != 2:
        errors.append("administrative-maintenance-synchronization.yml: issue writes must be split between MATH-PROGRAMME and INTELLECT tokens")

    for marker in (
        "python ci/validate_administrative_automation_v3.py",
        "python ci/validate_workflow_coverage_v2.py",
        "python ci/test_workflow_coverage_v2.py",
        "tests.test_administrative_automation",
        "tests.test_administrative_receipts",
        "tests.test_administrative_synchronization_wait",
    ):
        if marker not in validation_text:
            errors.append(f"administrative-maintenance-automation-validation.yml: missing validation marker {marker}")

    return errors


def workflow_coverage_errors(root=legacy.ROOT, texts=None, evidence=None):
    texts = legacy.workflow_texts(root) if texts is None else texts
    errors = legacy.workflow_coverage_errors(root=root, texts=texts, evidence=evidence)
    errors.extend(automation_workflow_errors(texts))
    return errors


def main() -> int:
    errors = workflow_coverage_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"workflow coverage v2 validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("workflow coverage v2: registered read-only workflows, scoped app tokens, manual authority gates, and protected receipt paths are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
