#!/usr/bin/env python3
from __future__ import annotations

import json
from typing import Any

import validate_workflow_coverage_v3 as v3

RECOVERY_FAILOVER_WORKFLOW = "administrative-maintenance-0813-recovery-failover.yml"

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
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: trigger must be exactly pull_request"
        )
    pull_request = trigger.get("pull_request", {})
    types = pull_request.get("types", []) if isinstance(pull_request, dict) else []
    if types != ["closed"]:
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: pull_request trigger must be closed only"
        )

    job = _job(workflow, "recover")
    if job.get("environment") != v3.PROTECTED_ENVIRONMENT:
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: recover job must bind protected environment release-trust"
        )
    expected_permissions = {
        "actions": "read",
        "checks": "read",
        "contents": "read",
        "issues": "write",
        "pull-requests": "write",
    }
    if job.get("permissions") != expected_permissions:
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: delegated Referee permissions drift"
        )

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
            errors.append(
                f"{RECOVERY_FAILOVER_WORKFLOW}: missing bounded recovery marker {marker}"
            )

    restore_index = text.find("Restore exact PR-only Administration actor")
    preflight_index = text.find(
        "python ci/administrative_autonomy_0813_closure_preflight.py"
    )
    if (
        restore_index < 0
        or preflight_index < 0
        or restore_index > preflight_index
    ):
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: exact Administration actor restoration must precede exact Aug13 preflight"
        )

    if text.count(v3.APP_ACTION) != 3:
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: exactly three separately scoped App tokens are required"
        )
    if text.count("permission-administration: write") != 1:
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: exactly one administration-write token is required"
        )
    if text.count("permission-contents: write") != 1:
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: exactly one contents-write token is required"
        )
    if text.count("${{ github.token }}") != 1:
        errors.append(
            f"{RECOVERY_FAILOVER_WORKFLOW}: workflow token must be used only as the Referee token"
        )

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
            errors.append(
                f"{RECOVERY_FAILOVER_WORKFLOW}: forbidden recovery capability {forbidden}"
            )
    return errors


def workflow_coverage_errors(root=ROOT, texts=None, evidence=None, registry=None):
    texts = v3.legacy.workflow_texts(root) if texts is None else texts
    errors = v3.workflow_coverage_errors(root=root, texts=texts, evidence=evidence)
    delegated_permission_error = (
        f"{RECOVERY_FAILOVER_WORKFLOW}:recover: "
        "non-Pages job permissions may not exceed contents: read"
    )
    errors = [error for error in errors if error != delegated_permission_error]
    errors.extend(recovery_failover_errors(texts))

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
        "protected exact-head merge, exact Aug13 PR-close recovery failover, mirror-only "
        "synchronization, manual control-plane gates, and claim boundaries are valid"
    )
    return 0


__all__ = [
    "ROOT",
    "RECOVERY_FAILOVER_WORKFLOW",
    "recovery_failover_errors",
    "workflow_coverage_errors",
    "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
