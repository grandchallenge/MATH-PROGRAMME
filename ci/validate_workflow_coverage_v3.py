#!/usr/bin/env python3
from __future__ import annotations

import sys
from typing import Any

import validate_workflow_coverage as legacy

ROOT = legacy.ROOT
MAINTENANCE_AUTOMATION_WORKFLOWS = {
    "administrative-maintenance-automation-validation.yml",
    "administrative-maintenance-candidate.yml",
    "administrative-maintenance-synchronization.yml",
}
ACTIVATION_WORKFLOW = "administrative-autonomy-activation.yml"
EXTRA_WORKFLOWS = MAINTENANCE_AUTOMATION_WORKFLOWS | {ACTIVATION_WORKFLOW}
legacy.EXPECTED_WORKFLOWS = set(legacy.EXPECTED_WORKFLOWS) | EXTRA_WORKFLOWS

APP_ACTION = "actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1"
APP_ID = "app-id: ${{ secrets.GCL_RELEASE_TRUST_APP_ID }}"
APP_KEY = "private-key: ${{ secrets.GCL_RELEASE_TRUST_PRIVATE_KEY }}"
PROTECTED_ENVIRONMENT = "release-trust"


def _trigger(workflow: dict[str, Any]) -> dict[str, Any]:
    value = workflow.get("on", {})
    return value if isinstance(value, dict) else {}


def _job(workflow: dict[str, Any], job_name: str) -> dict[str, Any]:
    jobs = workflow.get("jobs", {})
    if not isinstance(jobs, dict):
        return {}
    value = jobs.get(job_name, {})
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value is None:
        return []
    return [str(value)]


def candidate_workflow_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    text = texts.get("administrative-maintenance-candidate.yml")
    if text is None:
        return errors
    workflow = legacy.load_yaml_text(text)
    if set(_trigger(workflow)) != {"schedule", "workflow_dispatch"}:
        errors.append("administrative-maintenance-candidate.yml: triggers must be exactly schedule and workflow_dispatch")
    job = _job(workflow, "prepare")
    if job.get("environment") != PROTECTED_ENVIRONMENT:
        errors.append("administrative-maintenance-candidate.yml: write job must bind protected environment release-trust")
    expected_permissions = {
        "actions": "read",
        "checks": "read",
        "contents": "read",
        "issues": "write",
        "pull-requests": "write",
    }
    if job.get("permissions") != expected_permissions:
        errors.append("administrative-maintenance-candidate.yml: delegated Referee permissions drift")
    for marker in (
        APP_ACTION,
        APP_ID,
        APP_KEY,
        "id: write-token",
        "repositories: MATH-PROGRAMME",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "id: evidence-token",
        "MATHFORGE\n            MATHSOLVE\n            MATHCERT\n            INTELLECT",
        "permission-contents: read",
        "permission-issues: read",
        "permission-pull-requests: read",
        "permission-actions: read",
        "id: admin-token",
        "permission-administration: write",
        "EVIDENCE_GITHUB_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "python ci/prepare_administrative_candidate_v5.py --apply",
        "python ci/administrative_autonomy_runtime.py validate",
        "python ci/administrative_autonomy_runtime.py execute --report",
        "CANDIDATE_TOKEN: ${{ steps.write-token.outputs.token }}",
        "REFEREE_TOKEN: ${{ github.token }}",
        "ADMIN_TOKEN: ${{ steps.admin-token.outputs.token }}",
        "OBSERVABILITY_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "CANDIDATE_LOGIN: ${{ format('{0}[bot]', steps.write-token.outputs.app-slug) }}",
        "REFEREE_LOGIN: 'github-actions[bot]'",
        "CANDIDATE_APP_ID: ${{ secrets.GCL_RELEASE_TRUST_APP_ID }}",
        "REFEREE_APP_ID: '15368'",
        "AUTONOMOUS_RUNTIME_FAILED_CLOSED",
        "name: administrative-autonomy-runtime",
    ):
        if marker not in text:
            errors.append(f"administrative-maintenance-candidate.yml: missing runtime marker {marker}")
    if text.count(APP_ACTION) != 3:
        errors.append("administrative-maintenance-candidate.yml: exactly three separately scoped App tokens are required")
    if text.count("permission-administration: write") != 1:
        errors.append("administrative-maintenance-candidate.yml: exactly one administration-write token is required")
    if text.count("permission-contents: write") != 1:
        errors.append("administrative-maintenance-candidate.yml: exactly one contents-write token is required")
    if text.count("${{ github.token }}") != 1 or "REFEREE_TOKEN: ${{ github.token }}" not in text:
        errors.append("administrative-maintenance-candidate.yml: workflow token must be used only as the Referee token")
    for forbidden in (
        "pull_request_target:",
        "gh pr merge",
        "git push origin main",
        "/git/refs/heads/main",
        "permission-checks: write",
    ):
        if forbidden in text:
            errors.append(f"administrative-maintenance-candidate.yml: forbidden runtime capability {forbidden}")
    return errors


def synchronization_workflow_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    text = texts.get("administrative-maintenance-synchronization.yml")
    if text is None:
        return errors
    workflow = legacy.load_yaml_text(text)
    if set(_trigger(workflow)) != {"workflow_run", "workflow_dispatch"}:
        errors.append("administrative-maintenance-synchronization.yml: triggers must be exactly workflow_run and workflow_dispatch")
    job = _job(workflow, "synchronize")
    if job.get("environment") != PROTECTED_ENVIRONMENT:
        errors.append("administrative-maintenance-synchronization.yml: write job must bind protected environment release-trust")
    for marker in (
        APP_ACTION,
        APP_ID,
        APP_KEY,
        "repositories: MATH-PROGRAMME",
        "permission-actions: read",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "repositories: INTELLECT",
        "CROSS_REPOSITORY_MAINTENANCE_TOKEN: ${{ steps.intellect-token.outputs.token }}",
        "github.event.workflow_run.event == 'push'",
        "github.event.workflow_run.head_branch == 'main'",
        "github.event.workflow_run.head_repository.full_name == github.repository",
        "github.event.workflow_run.conclusion == 'success'",
        "github.event_name == 'workflow_run' && github.event.workflow_run.head_sha || 'refs/heads/main'",
        "github.event_name == 'workflow_run' && github.event.workflow_run.head_sha || github.sha",
        "python ci/synchronize_administrative_completion_v4.py --apply",
        "SYNCHRONIZATION_FAILED_CLOSED",
    ):
        if marker not in text:
            errors.append(f"administrative-maintenance-synchronization.yml: missing bounded synchronization marker {marker}")
    if "github.token" in text:
        errors.append("administrative-maintenance-synchronization.yml: write path may not use workflow GITHUB_TOKEN")
    if "inputs.head_sha" in text:
        errors.append("administrative-maintenance-synchronization.yml: manual arbitrary-SHA checkout is forbidden")
    for forbidden in (
        "merge_pull_request",
        "enable_auto_merge",
        "gh pr merge",
        "/merges",
        "permission-administration: write",
        "permission-checks: write",
    ):
        if forbidden in text:
            errors.append(f"administrative-maintenance-synchronization.yml: forbidden merge or administration capability {forbidden}")
    if text.count("permission-contents: write") != 1:
        errors.append("administrative-maintenance-synchronization.yml: exactly one MATH-PROGRAMME contents write token is required")
    if text.count("permission-issues: write") != 2:
        errors.append("administrative-maintenance-synchronization.yml: issue writes must remain split")
    return errors


def validation_workflow_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    text = texts.get("administrative-maintenance-automation-validation.yml")
    if text is None:
        return errors
    workflow = legacy.load_yaml_text(text)
    if set(_trigger(workflow)) != {"pull_request", "push", "workflow_dispatch"}:
        errors.append("administrative-maintenance-automation-validation.yml: triggers must cover pull_request, push, and workflow_dispatch only")
    for marker in (
        "python ci/validate_administrative_automation_v4.py",
        "python ci/administrative_autonomy.py validate",
        "python ci/administrative_autonomy_runtime.py validate",
        "python ci/validate_workflow_coverage_v2.py",
        "python ci/test_workflow_coverage_v2.py",
        "tests.test_administrative_autonomy_runtime",
        "tests.test_administrative_automation",
        "tests.test_administrative_steady_state",
        "tests.test_administrative_transition_recovery_candidate",
        "tests.test_administrative_receipts",
        "tests.test_administrative_synchronization_wait",
    ):
        if marker not in text:
            errors.append(f"administrative-maintenance-automation-validation.yml: missing validation marker {marker}")
    return errors


def activation_workflow_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    text = texts.get(ACTIVATION_WORKFLOW)
    if text is None:
        return errors
    workflow = legacy.load_yaml_text(text)
    trigger = _trigger(workflow)
    if set(trigger) != {"push", "workflow_dispatch"}:
        errors.append(f"{ACTIVATION_WORKFLOW}: triggers must be exactly push and workflow_dispatch")
    push = trigger.get("push", {})
    if "main" not in _as_list(push.get("branches")):
        errors.append(f"{ACTIVATION_WORKFLOW}: push trigger must cover main")
    job = _job(workflow, "activate")
    if job.get("environment") != PROTECTED_ENVIRONMENT:
        errors.append(f"{ACTIVATION_WORKFLOW}: activate job must bind protected environment release-trust")
    expected_permissions = {
        "actions": "read",
        "checks": "read",
        "contents": "read",
        "issues": "write",
        "pull-requests": "write",
    }
    if job.get("permissions") != expected_permissions:
        errors.append(f"{ACTIVATION_WORKFLOW}: activate job delegated permissions drift")
    for marker in (
        APP_ACTION,
        APP_ID,
        APP_KEY,
        "repositories: MATH-PROGRAMME",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "id: admin-token",
        "permission-administration: write",
        "CANDIDATE_TOKEN: ${{ steps.candidate-token.outputs.token }}",
        "REFEREE_TOKEN: ${{ github.token }}",
        "ADMIN_TOKEN: ${{ steps.admin-token.outputs.token }}",
        "CANDIDATE_APP_ID: ${{ secrets.GCL_RELEASE_TRUST_APP_ID }}",
        "REFEREE_APP_ID: '15368'",
        "AUTONOMY_RULESET_ID: '17137629'",
        "python ci/administrative_autonomy.py validate",
        "python ci/administrative_autonomy.py activate",
        "name: administrative-autonomy-activation",
        "retention-days: 90",
    ):
        if marker not in text:
            errors.append(f"{ACTIVATION_WORKFLOW}: missing activation control marker {marker}")
    return errors


def workflow_coverage_errors(root=legacy.ROOT, texts=None, evidence=None):
    texts = legacy.workflow_texts(root) if texts is None else texts
    errors = legacy.workflow_coverage_errors(root=root, texts=texts, evidence=evidence)
    delegated = {
        f"{ACTIVATION_WORKFLOW}:activate: non-Pages job permissions may not exceed contents: read",
        "administrative-maintenance-candidate.yml:prepare: non-Pages job permissions may not exceed contents: read",
    }
    errors = [error for error in errors if error not in delegated]
    errors.extend(candidate_workflow_errors(texts))
    errors.extend(synchronization_workflow_errors(texts))
    errors.extend(validation_workflow_errors(texts))
    errors.extend(activation_workflow_errors(texts))
    return errors


def main() -> int:
    errors = workflow_coverage_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"workflow coverage v3 validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("workflow coverage v3: active bounded administrative runtime, separated Candidate and Referee identities, protected exact-head merge, mirror-only synchronization, manual control-plane gates, and claim boundaries are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
