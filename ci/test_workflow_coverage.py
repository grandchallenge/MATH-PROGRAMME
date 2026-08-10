#!/usr/bin/env python3
"""Adversarial rejection tests for workflow and cross-repository coverage."""
from __future__ import annotations

import copy
import json

from test_rh_continuity import main as run_rh_continuity_tests
from validate_workflow_coverage import ROOT, workflow_texts
from validate_workflow_coverage_v2 import workflow_coverage_errors


def require_error(texts: dict[str, str], evidence: dict, needle: str, *, registry: dict) -> None:
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

    missing_policy = dict(texts)
    missing_policy.pop("ci.yml")
    require_error(missing_policy, evidence, "missing governed workflow ci.yml", registry=registry)

    missing_concurrency = dict(texts)
    missing_concurrency["ci.yml"] = missing_concurrency["ci.yml"].replace(
        "concurrency:\n", "concurrency-disabled:\n", 1
    )
    require_error(missing_concurrency, evidence, "explicit concurrency control is required", registry=registry)

    overprivileged_policy = dict(texts)
    overprivileged_policy["ci.yml"] = overprivileged_policy["ci.yml"].replace(
        "permissions:\n  contents: read\n",
        "permissions:\n  contents: read\n  actions: write\n",
        1,
    )
    require_error(overprivileged_policy, evidence, "top-level permissions must be exactly contents: read", registry=registry)

    direct_pages_push = dict(texts)
    direct_pages_push["pages.yml"] = direct_pages_push["pages.yml"].replace(
        "  workflow_run:\n", "  push:\n    branches: [main]\n  workflow_run:\n", 1
    )
    require_error(direct_pages_push, evidence, "triggered only by workflow_run", registry=registry)

    bypass_success = dict(texts)
    bypass_success["pages.yml"] = bypass_success["pages.yml"].replace(
        "github.event.workflow_run.conclusion == 'success'", "true", 1
    )
    require_error(bypass_success, evidence, "missing publication gate", registry=registry)

    overprivileged_build = dict(texts)
    overprivileged_build["pages.yml"] = overprivileged_build["pages.yml"].replace(
        "    permissions:\n      actions: read\n      contents: read\n      pages: write\n",
        "    permissions:\n      actions: read\n      contents: read\n      pages: write\n      id-token: write\n",
        1,
    )
    require_error(overprivileged_build, evidence, "build permissions must be exactly", registry=registry)

    missing_artifact_read = dict(texts)
    missing_artifact_read["pages.yml"] = missing_artifact_read["pages.yml"].replace(
        "      actions: read\n", "", 1
    )
    require_error(missing_artifact_read, evidence, "build permissions must be exactly", registry=registry)

    missing_deploy_token = dict(texts)
    missing_deploy_token["pages.yml"] = missing_deploy_token["pages.yml"].replace(
        "      id-token: write\n", "", 1
    )
    require_error(missing_deploy_token, evidence, "deploy permissions must be exactly", registry=registry)

    mutable_action = dict(texts)
    mutable_action["pages.yml"] = mutable_action["pages.yml"].replace(
        "actions/configure-pages@45bfe0192ca1faeb007ade9deae92b16b8254a0d",
        "actions/configure-pages@v5",
        1,
    )
    require_error(mutable_action, evidence, "action reference must use a full commit SHA", registry=registry)

    missing_exact_artifact = dict(texts)
    missing_exact_artifact["pages.yml"] = missing_exact_artifact["pages.yml"].replace(
        'artifact.get("name") == "validated-site"',
        'artifact.get("name") == "some-other-artifact"',
        1,
    )
    require_error(missing_exact_artifact, evidence, "missing publication gate", registry=registry)

    missing_inner_digest = dict(texts)
    missing_inner_digest["pages.yml"] = missing_inner_digest["pages.yml"].replace(
        "validated-site inner digest mismatch", "inner verification removed", 1
    )
    require_error(missing_inner_digest, evidence, "missing publication gate", registry=registry)

    missing_repository_route = remove_registry_command(
        registry, ["python3", "ci/validate_repository_execution.py"]
    )
    require_error(
        texts,
        evidence,
        "validate_repository_execution.py",
        registry=missing_repository_route,
    )

    dynamic_external_repository = dict(texts)
    dynamic_external_repository["ci.yml"] = dynamic_external_repository["ci.yml"].replace(
        "          repository: grandchallenge/MATHCERT\n",
        "          repository: ${{ steps.external-evidence.outputs.repository }}\n",
        1,
    )
    require_error(dynamic_external_repository, evidence, "external checkout repository must match", registry=registry)

    mismatched_external_ref = dict(texts)
    mismatched_external_ref["ci.yml"] = mismatched_external_ref["ci.yml"].replace(
        "          ref: d59173899dcd1a67dbe8f31de0b9f0917cd1459a\n",
        "          ref: 0000000000000000000000000000000000000000\n",
        1,
    )
    require_error(mismatched_external_ref, evidence, "external checkout ref must match", registry=registry)

    missing_replay_route = remove_registry_command(
        registry, ["python3", "ci/validate_campaign_replays.py"]
    )
    require_error(
        texts,
        evidence,
        "validate_campaign_replays.py",
        registry=missing_replay_route,
    )

    unpinned_evidence = copy.deepcopy(evidence)
    unpinned_evidence["commit"] = "main"
    require_error(texts, unpinned_evidence, "does not match", registry=registry)

    incomplete_evidence = copy.deepcopy(evidence)
    incomplete_evidence["paths"].remove("ci/replay_certificates.py")
    require_error(
        texts,
        incomplete_evidence,
        "required formal and bounded replay paths are incomplete",
        registry=registry,
    )

    assert run_rh_continuity_tests() == 0

    print("workflow, routed-policy, exact-artifact, repository-execution, and RH rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
