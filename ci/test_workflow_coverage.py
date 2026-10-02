#!/usr/bin/env python3
"""Adversarial rejection tests for workflow, formal-routing, and cross-repository coverage."""
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
    evidence = json.loads((ROOT / "evidence/UC-WP02-MATHCERT.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "governance/policy_shard_registry.json").read_text(encoding="utf-8"))
    baseline = workflow_coverage_errors(texts=texts, evidence=evidence, registry=registry)
    assert not baseline, baseline

    missing_policy = dict(texts)
    missing_policy.pop("ci.yml")
    require_error(missing_policy, evidence, "missing governed workflow ci.yml", registry=registry)

    missing_formal = dict(texts)
    missing_formal.pop("formal-validation.yml")
    require_error(
        missing_formal,
        evidence,
        "missing governed workflow formal-validation.yml",
        registry=registry,
    )

    unregistered_workflow = dict(texts)
    unregistered_workflow["unregistered-formal.yml"] = texts["formal-validation.yml"]
    require_error(unregistered_workflow, evidence, "unregistered workflow unregistered-formal.yml", registry=registry)

    missing_concurrency = dict(texts)
    missing_concurrency["formal-validation.yml"] = missing_concurrency["formal-validation.yml"].replace(
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

    retired_formal_job = dict(texts)
    retired_formal_job["ci.yml"] += "\n  # log-gcd-lean:\n"
    # A mere comment is inert; use a YAML mutation for the actual rejection path.
    ci = retired_formal_job["ci.yml"].replace(
        "  validate-json:\n",
        "  log-gcd-lean:\n    runs-on: ubuntu-24.04\n    timeout-minutes: 5\n    steps:\n      - run: echo retired\n\n  validate-json:\n",
        1,
    )
    retired_formal_job["ci.yml"] = ci
    require_error(retired_formal_job, evidence, "retired substantive formal job remains", registry=registry)

    formal_direct_push = dict(texts)
    formal_direct_push["formal-validation.yml"] = formal_direct_push["formal-validation.yml"].replace(
        "  pull_request:\n", "  push:\n    branches: [main]\n  pull_request:\n", 1
    )
    require_error(formal_direct_push, evidence, "direct push trigger is forbidden", registry=registry)

    formal_classifier_removed = dict(texts)
    original_formal = formal_classifier_removed["formal-validation.yml"]
    mutated_formal = original_formal.replace(
        "python3 ci/formal_validation.py classify",
        "python3 -c 'raise SystemExit(0)'",
        1,
    )
    assert mutated_formal != original_formal, "formal classifier mutation did not apply"
    formal_classifier_removed["formal-validation.yml"] = mutated_formal
    require_error(formal_classifier_removed, evidence, "missing formal routing marker", registry=registry)

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
    print("workflow, routed-policy, material-formal, exact-artifact, repository-execution, and RH rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
