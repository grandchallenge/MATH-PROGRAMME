#!/usr/bin/env python3
from __future__ import annotations

import copy
import json

from validate_workflow_coverage_v2 import ROOT, workflow_coverage_errors
from validate_workflow_coverage import workflow_texts


def require_error(texts: dict[str, str], evidence: dict, needle: str, *, registry=None) -> None:
    errors = workflow_coverage_errors(texts=texts, evidence=evidence, registry=registry)
    assert any(needle in error for error in errors), errors


def remove_registry_command(registry: dict, command: list[str]) -> dict:
    mutated = copy.deepcopy(registry)
    for entries in mutated.get("shards", {}).values():
        if command in entries:
            entries.remove(command)
            return mutated
    raise AssertionError(f"registry command not found: {command}")


def main() -> int:
    texts = workflow_texts()
    evidence = json.loads(
        (ROOT / "evidence/UC-WP02-MATHCERT.json").read_text(encoding="utf-8")
    )
    registry = json.loads(
        (ROOT / "governance/policy_shard_registry.json").read_text(encoding="utf-8")
    )
    assert not workflow_coverage_errors(texts=texts, evidence=evidence, registry=registry)

    missing_repository_route = remove_registry_command(
        registry, ["python3", "ci/validate_repository_execution.py"]
    )
    require_error(
        texts,
        evidence,
        "missing workflow coverage marker python3 ci/validate_repository_execution.py",
        registry=missing_repository_route,
    )

    missing_successor_route = remove_registry_command(
        registry, ["python3", "ci/validate_workflow_coverage_v2.py"]
    )
    require_error(
        texts,
        evidence,
        "missing workflow coverage marker python3 ci/validate_workflow_coverage.py",
        registry=missing_successor_route,
    )

    mutable_app = dict(texts)
    mutable_app["administrative-maintenance-candidate.yml"] = mutable_app[
        "administrative-maintenance-candidate.yml"
    ].replace(
        "actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1",
        "actions/create-github-app-token@v2",
        1,
    )
    require_error(mutable_app, evidence, "full commit SHA", registry=registry)

    referee_removed = dict(texts)
    referee_removed["administrative-maintenance-candidate.yml"] = referee_removed[
        "administrative-maintenance-candidate.yml"
    ].replace("REFEREE_TOKEN: ${{ github.token }}", "REFEREE_TOKEN: missing", 1)
    require_error(referee_removed, evidence, "Referee token", registry=registry)

    admin_scope_removed = dict(texts)
    admin_scope_removed["administrative-maintenance-candidate.yml"] = admin_scope_removed[
        "administrative-maintenance-candidate.yml"
    ].replace("permission-administration: write", "permission-administration: read", 1)
    require_error(admin_scope_removed, evidence, "administration-write", registry=registry)

    runtime_removed = dict(texts)
    runtime_removed["administrative-maintenance-candidate.yml"] = runtime_removed[
        "administrative-maintenance-candidate.yml"
    ].replace(
        "python ci/administrative_autonomy_runtime.py execute --report",
        "python -c 'print(0)' #",
        1,
    )
    require_error(runtime_removed, evidence, "runtime marker", registry=registry)

    permission_drift = dict(texts)
    permission_drift["administrative-maintenance-candidate.yml"] = permission_drift[
        "administrative-maintenance-candidate.yml"
    ].replace("      issues: write", "      issues: read", 1)
    require_error(permission_drift, evidence, "delegated Referee permissions drift", registry=registry)

    direct_push = dict(texts)
    direct_push["administrative-maintenance-candidate.yml"] += "\n# git push origin main\n"
    require_error(direct_push, evidence, "forbidden runtime capability", registry=registry)

    sync_v4_removed = dict(texts)
    sync_v4_removed["administrative-maintenance-synchronization.yml"] = sync_v4_removed[
        "administrative-maintenance-synchronization.yml"
    ].replace("synchronize_administrative_completion_v4.py", "synchronize_administrative_completion_v3.py", 1)
    require_error(sync_v4_removed, evidence, "bounded synchronization marker", registry=registry)

    arbitrary_manual_sha = dict(texts)
    arbitrary_manual_sha["administrative-maintenance-synchronization.yml"] += "\n# inputs.head_sha\n"
    require_error(arbitrary_manual_sha, evidence, "manual arbitrary-SHA", registry=registry)

    activation_permissions_drift = dict(texts)
    activation_permissions_drift["administrative-autonomy-activation.yml"] = activation_permissions_drift[
        "administrative-autonomy-activation.yml"
    ].replace("      pull-requests: write", "      pull-requests: read", 1)
    require_error(activation_permissions_drift, evidence, "activate job delegated permissions drift", registry=registry)

    activation_environment_removed = dict(texts)
    activation_environment_removed["administrative-autonomy-activation.yml"] = activation_environment_removed[
        "administrative-autonomy-activation.yml"
    ].replace("    environment: release-trust\n", "", 1)
    require_error(activation_environment_removed, evidence, "activate job must bind", registry=registry)

    print("workflow coverage v3 adversarial tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
