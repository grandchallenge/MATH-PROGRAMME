#!/usr/bin/env python3
from __future__ import annotations

import json
from typing import Any

import validate_workflow_coverage_v3 as v3

RECOVERY_FAILOVER_WORKFLOW = "administrative-maintenance-0813-recovery-failover.yml"
QUALIFICATION_ONLY_WORKFLOW = "administrative-protected-receipt-live-qualification.yml"

v3.legacy.EXPECTED_WORKFLOWS = set(v3.legacy.EXPECTED_WORKFLOWS) | {
    "aether-controls-admin.yml",
    "cmdg-nat-concordance.yml",
    "cmdg-euclid-bridge.yml",
    "cmdg-vertical-spine-v0.yml",
    "cmdg-condensed-cm1.yml",
    "cmdg-condensed-cm2.yml",
    "cmdg-condensed-cm3.yml",
    "cmdg-solid-c05.yml",
    "cmdg-condensed-cm4.yml",
    "cmdg-condensed-cm4-p2.yml",
    "cmdg-condensed-cm4-p2-d.yml",
    "cmdg-condensed-cm4-p2-e.yml",
    "cmdg-condensed-cm4-p3.yml",
    "cmdg-postmerge.yml",
    "visual-pedagogy-representation-repair.yml",
    "pr-visual-status-advisory.yml",
    RECOVERY_FAILOVER_WORKFLOW,
    QUALIFICATION_ONLY_WORKFLOW,
}

ROOT = v3.ROOT
POLICY_SHARD_REGISTRY = "governance/policy_shard_registry.json"
ROUTED_MARKER_SUCCESSORS = {
    "python3 ci/validate_workflow_coverage.py": "python3 ci/validate_workflow_coverage_v2.py",
    "python3 ci/test_workflow_coverage.py": "python3 ci/test_workflow_coverage_v2.py",
    "python -m unittest discover -s tests -p 'test_*.py'": (
        "python3 ci/run_unittest_modules.py --discover-root tests --pattern test_*.py "
        "--report-json repository-regression-timing.json"
    ),
}


def _normalize_command(command: str) -> str:
    return (
        command.strip()
        .replace("'test_*.py'", "test_*.py")
        .replace('"test_*.py"', "test_*.py")
    )


def _registry_commands(root=ROOT, registry=None) -> set[str]:
    if registry is None:
        path = root / POLICY_SHARD_REGISTRY
        if not path.is_file():
            return set()
        try:
            registry = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return set()
    if not isinstance(registry, dict):
        return set()
    commands: set[str] = set()
    shards = registry.get("shards", {})
    if not isinstance(shards, dict):
        return commands
    for entries in shards.values():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, list) and entry and all(isinstance(part, str) for part in entry):
                commands.add(_normalize_command(" ".join(entry)))
    return commands


def _trigger(workflow: dict[str, Any]) -> dict[str, Any]:
    value = workflow.get("on", {})
    return value if isinstance(value, dict) else {}


def _job(workflow: dict[str, Any], name: str) -> dict[str, Any]:
    jobs = workflow.get("jobs", {})
    if not isinstance(jobs, dict):
        return {}
    value = jobs.get(name, {})
    return value if isinstance(value, dict) else {}


def recovery_failover_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    text = texts.get(RECOVERY_FAILOVER_WORKFLOW)
    if text is None:
        return errors
    workflow = v3.legacy.load_yaml_text(text)
    trigger = _trigger(workflow)
    if set(trigger) != {"pull_request"}:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: trigger must be exactly pull_request")
    pull_request = trigger.get("pull_request", {})
    types = pull_request.get("types", []) if isinstance(pull_request, dict) else []
    if types != ["closed"]:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: pull_request trigger must be closed only")

    job = _job(workflow, "recover")
    if job.get("environment") != v3.PROTECTED_ENVIRONMENT:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: recover job must bind protected environment release-trust")
    expected_permissions = {
        "actions": "read",
        "checks": "read",
        "contents": "read",
        "issues": "write",
        "pull-requests": "write",
    }
    if job.get("permissions") != expected_permissions:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: delegated Referee permissions drift")

    required_markers = (
        "github.event.pull_request.merged == true",
        "startsWith(github.event.pull_request.head.ref, 'control/mp-admin-0813-')",
        v3.APP_ACTION,
        v3.APP_ID,
        v3.APP_KEY,
        "id: write-token",
        "repositories: MATH-PROGRAMME",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "id: evidence-token",
        "MATHFORGE\n            MATHSOLVE\n            MATHCERT\n            INTELLECT",
        "permission-actions: read",
        "permission-contents: read",
        "permission-issues: read",
        "permission-pull-requests: read",
        "id: admin-token",
        "permission-administration: write",
        "ref: refs/heads/main",
        "persist-credentials: false",
        "CANDIDATE_TOKEN: ${{ steps.write-token.outputs.token }}",
        "EVIDENCE_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "OBSERVABILITY_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "REFEREE_TOKEN: ${{ github.token }}",
        "ADMIN_TOKEN: ${{ steps.admin-token.outputs.token }}",
        "CANDIDATE_LOGIN: ${{ format('{0}[bot]', steps.write-token.outputs.app-slug) }}",
        "REFEREE_LOGIN: 'github-actions[bot]'",
        "CANDIDATE_APP_ID: ${{ secrets.GCL_RELEASE_TRUST_APP_ID }}",
        "REFEREE_APP_ID: '15368'",
        "Restore exact PR-only Administration actor",
        "from autonomy_github import AutonomyError, Client, identity, install_bypass",
        "ruleset_id = 17137629",
        "administrator.app_id != 4423678",
        '"bypass_mode": "pull_request"',
        "administrative-autonomy-0813-ruleset-actor-restore.json",
        "python ci/administrative_autonomy_0813_closure_preflight.py",
        "--apply",
        "administrative-autonomy-0813-pr-close-recovery.json",
        "retention-days: 90",
    )
    for marker in required_markers:
        if marker not in text:
            errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: missing bounded recovery marker {marker}")

    restore_index = text.find("Restore exact PR-only Administration actor")
    preflight_index = text.find("python ci/administrative_autonomy_0813_closure_preflight.py")
    if restore_index < 0 or preflight_index < 0 or restore_index > preflight_index:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: exact Administration actor restoration must precede exact Aug13 preflight")

    if text.count(v3.APP_ACTION) != 3:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: exactly three separately scoped App tokens are required")
    if text.count("permission-administration: write") != 1:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: exactly one administration-write token is required")
    if text.count("permission-contents: write") != 1:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: exactly one contents-write token is required")
    if text.count("${{ github.token }}") != 1:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: workflow token must be used only as the Referee token")

    for forbidden in (
        "workflow_dispatch:",
        "schedule:",
        "push:",
        "pull_request_target:",
        "administrative_autonomy_runtime.py execute",
        "administrative_maintenance_completion_state.json",
        "gh pr merge",
        "git push origin main",
        "/git/refs/heads/main",
        "permission-checks: write",
    ):
        if forbidden in text:
            errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: forbidden recovery capability {forbidden}")
    return errors


def remediation_envelope_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    text = texts.get(QUALIFICATION_ONLY_WORKFLOW)
    if text is None:
        return errors
    workflow = v3.legacy.load_yaml_text(text)
    trigger = _trigger(workflow)
    if set(trigger) != {"workflow_dispatch", "pull_request_target"}:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: trigger must be workflow_dispatch plus pull_request_target")
    pull_request_target = trigger.get("pull_request_target", {})
    types = pull_request_target.get("types", []) if isinstance(pull_request_target, dict) else []
    expected_types = ["closed", "opened", "reopened", "synchronize", "ready_for_review"]
    if types != expected_types:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: pull_request_target trigger set drift")

    admit = _job(workflow, "admit")
    qualify = _job(workflow, "qualify")
    expected_admit_permissions = {
        "checks": "read",
        "contents": "read",
        "issues": "write",
    }
    if admit.get("permissions") != expected_admit_permissions:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: delegated Referee admission permissions drift")
    if admit.get("environment") != v3.PROTECTED_ENVIRONMENT:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: admit job must bind protected environment release-trust")
    expected_qualify_permissions = {"contents": "read", "issues": "write"}
    if qualify.get("permissions") != expected_qualify_permissions:
        errors.append(
            f"{QUALIFICATION_ONLY_WORKFLOW}: qualification job permissions must be contents-read plus issue-status-write only"
        )
    if qualify.get("environment") != v3.PROTECTED_ENVIRONMENT:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: qualify job must bind protected environment release-trust")

    required_markers = (
        "github.event_name == 'pull_request_target'",
        "github.event.action != 'closed'",
        "github.event.pull_request.draft == false",
        "startsWith(github.event.pull_request.head.ref, 'remediation/mp-admin-')",
        "Mint bounded Candidate merge-executor token",
        "id: candidate-merge-token",
        "permission-contents: write",
        "permission-pull-requests: write",
        "permission-administration: read",
        "Check out trusted protected implementation",
        "ref: refs/heads/main",
        "REFEREE_TOKEN: ${{ github.token }}",
        "ADMIN_READ_TOKEN: ${{ steps.admin-read-token.outputs.token }}",
        "CANDIDATE_MERGE_TOKEN: ${{ steps.candidate-merge-token.outputs.token }}",
        "CANDIDATE_LOGIN: ${{ format('{0}[bot]', steps.candidate-merge-token.outputs.app-slug) }}",
        "administrative_remediation_envelope.py admit-pull-request",
        '--pr "${{ github.event.pull_request.number }}"',
        '--head "${{ github.event.pull_request.head.sha }}"',
        "administrative-remediation-admission.json",
        "permission-contents: read",
        "permission-pull-requests: read",
        "permission-issues: read",
        "permission-administration: write",
        "administrative_remediation_envelope.py reconcile-actor",
        "administrative_protected_receipt_live.py qualify",
        "--control-id MP-ADMIN-REMEDIATION-ENVELOPE-001",
        "--control-issue 615",
        "--authorization-comment-id 5349149366",
        "--receipt-pr 596",
        "--integration-merge 8ff752b4f2ac28d87575d4f4ef48f564fb18837b",
        "Publish durable remediation result",
        "STATUS_TOKEN: ${{ github.token }}",
        "https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/issues/615/comments",
        "DELEGATED REMEDIATION RUN RESULT — MP-ADMIN-REMEDIATION-ENVELOPE-001",
        "Safety readback: no #596 mutation",
        "retention-days: 90",
    )
    for marker in required_markers:
        if marker not in text:
            errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: missing remediation envelope marker {marker}")

    if text.count(v3.APP_ACTION) != 6:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly six separately scoped App tokens are required")
    if text.count("${{ github.token }}") != 2:
        errors.append(
            f"{QUALIFICATION_ONLY_WORKFLOW}: workflow token must be used exactly for Referee admission and durable status publication"
        )
    if text.count("permission-administration: write") != 1:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly one actor-reconciliation administration-write token is required")
    if text.count("permission-administration: read") != 2:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly two separately minted administration-read observation tokens are required")
    if text.count("permission-contents: write") != 1:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly one Candidate contents-write merge token is required")
    if text.count("permission-pull-requests: write") != 1:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly one Candidate pull-request-write merge token is required")
    if "permission-issues: write" in text:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: App tokens may not receive issues-write")

    admission_index = text.find("administrative_remediation_envelope.py admit-pull-request")
    reconciliation_index = text.find("administrative_remediation_envelope.py reconcile-actor")
    qualification_index = text.find("administrative_protected_receipt_live.py qualify")
    status_index = text.find("Publish durable remediation result")
    evidence_index = text.find("Preserve remediation and qualification evidence")
    if min(admission_index, reconciliation_index, qualification_index, status_index, evidence_index) < 0:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: remediation sequence is incomplete")
    elif not admission_index < reconciliation_index < qualification_index < status_index < evidence_index:
        errors.append(
            f"{QUALIFICATION_ONLY_WORKFLOW}: Referee admission must precede actor reconciliation, qualification, durable status, and retained evidence"
        )

    for forbidden in (
        "schedule:",
        "push:",
        "workflow_run:",
        "repository_dispatch:",
        "pull_request:\n",
        "permission-checks: write",
        "administrative_autonomy_runtime.py execute",
        "administrative_autonomy_0813_closure_preflight.py",
        "administrative_maintenance_completion_state.json",
        "gh pr merge",
        "git push origin main",
        "/git/refs/heads/main",
    ):
        if forbidden in text:
            errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: forbidden remediation capability {forbidden}")
    return errors


def workflow_coverage_errors(root=ROOT, texts=None, evidence=None, registry=None):
    texts = v3.legacy.workflow_texts(root) if texts is None else texts
    errors = v3.workflow_coverage_errors(root=root, texts=texts, evidence=evidence)
    delegated_permission_errors = {
        f"{RECOVERY_FAILOVER_WORKFLOW}:recover: non-Pages job permissions may not exceed contents: read",
        f"{QUALIFICATION_ONLY_WORKFLOW}:admit: non-Pages job permissions may not exceed contents: read",
        f"{QUALIFICATION_ONLY_WORKFLOW}:qualify: non-Pages job permissions may not exceed contents: read",
    }
    errors = [error for error in errors if error not in delegated_permission_errors]
    errors.extend(recovery_failover_errors(texts))
    errors.extend(remediation_envelope_errors(texts))

    commands = _registry_commands(root=root, registry=registry)
    prefix = "ci.yml: missing workflow coverage marker "
    retained: list[str] = []
    for error in errors:
        if not error.startswith(prefix):
            retained.append(error)
            continue
        marker = error[len(prefix) :]
        routed = ROUTED_MARKER_SUCCESSORS.get(marker, marker)
        if _normalize_command(routed) in commands:
            continue
        retained.append(error)
    return retained


def main() -> int:
    errors = workflow_coverage_errors()
    if errors:
        for error in errors:
            print(error, file=__import__("sys").stderr)
        print(
            f"workflow coverage v3 validation failed with {len(errors)} error(s)",
            file=__import__("sys").stderr,
        )
        return 1
    print(
        "workflow coverage v3: direct workflow and governed shard-registry execution roots, "
        "active bounded administrative runtime, separated Candidate and Referee identities, "
        "protected expected-head PR merge, exact Aug13 PR-close recovery failover, trusted-main "
        "delegated remediation Referee admission, Candidate expected-head merge, post-merge qualification, "
        "durable issue-status audit, mirror-only synchronization, manual control-plane gates, and claim boundaries are valid"
    )
    return 0


__all__ = [
    "ROOT",
    "RECOVERY_FAILOVER_WORKFLOW",
    "QUALIFICATION_ONLY_WORKFLOW",
    "recovery_failover_errors",
    "remediation_envelope_errors",
    "workflow_coverage_errors",
    "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
