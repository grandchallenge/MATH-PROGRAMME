#!/usr/bin/env python3
from __future__ import annotations

import json

import test_workflow_coverage as legacy_tests
from validate_workflow_coverage_v2 import ROOT, workflow_coverage_errors
from validate_workflow_coverage import workflow_texts


def main() -> int:
    assert legacy_tests.main() == 0
    texts = workflow_texts()
    evidence = json.loads((ROOT / "evidence/UC-WP02-MATHCERT.json").read_text(encoding="utf-8"))
    assert not workflow_coverage_errors(texts=texts, evidence=evidence)

    mutable_app = dict(texts)
    mutable_app["administrative-maintenance-candidate.yml"] = mutable_app["administrative-maintenance-candidate.yml"].replace(
        "actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1",
        "actions/create-github-app-token@v2",
        1,
    )
    assert any("full commit SHA" in error or "missing scoped GitHub App marker" in error for error in workflow_coverage_errors(texts=mutable_app, evidence=evidence))

    workflow_token_write = dict(texts)
    workflow_token_write["administrative-maintenance-candidate.yml"] = workflow_token_write["administrative-maintenance-candidate.yml"].replace(
        "${{ steps.write-token.outputs.token }}",
        "${{ github.token }}",
        1,
    )
    assert any("workflow GITHUB_TOKEN" in error for error in workflow_coverage_errors(texts=workflow_token_write, evidence=evidence))

    pull_request_execution = dict(texts)
    pull_request_execution["administrative-maintenance-candidate.yml"] = pull_request_execution["administrative-maintenance-candidate.yml"].replace(
        "  workflow_dispatch:\n",
        "  workflow_dispatch:\n  pull_request:\n",
        1,
    )
    assert any("triggers must be exactly" in error for error in workflow_coverage_errors(texts=pull_request_execution, evidence=evidence))

    broad_candidate_scope = dict(texts)
    broad_candidate_scope["administrative-maintenance-candidate.yml"] = broad_candidate_scope["administrative-maintenance-candidate.yml"].replace(
        "          repositories: MATH-PROGRAMME\n",
        "          repositories: |\n            MATH-PROGRAMME\n            INTELLECT\n",
        1,
    )
    assert any("bounded candidate marker" in error or "exactly one repository-scoped" in error for error in workflow_coverage_errors(texts=broad_candidate_scope, evidence=evidence))

    candidate_environment_removed = dict(texts)
    candidate_environment_removed["administrative-maintenance-candidate.yml"] = candidate_environment_removed["administrative-maintenance-candidate.yml"].replace(
        "    environment: release-trust\n",
        "",
        1,
    )
    assert any("write job must bind protected environment release-trust" in error for error in workflow_coverage_errors(texts=candidate_environment_removed, evidence=evidence))

    synchronization_environment_renamed = dict(texts)
    synchronization_environment_renamed["administrative-maintenance-synchronization.yml"] = synchronization_environment_renamed["administrative-maintenance-synchronization.yml"].replace(
        "    environment: release-trust\n",
        "    environment: production\n",
        1,
    )
    assert any("write job must bind protected environment release-trust" in error for error in workflow_coverage_errors(texts=synchronization_environment_renamed, evidence=evidence))

    removed_main_gate = dict(texts)
    removed_main_gate["administrative-maintenance-synchronization.yml"] = removed_main_gate["administrative-maintenance-synchronization.yml"].replace(
        "github.event.workflow_run.head_branch == 'main'",
        "true",
        1,
    )
    assert any("bounded synchronization marker" in error for error in workflow_coverage_errors(texts=removed_main_gate, evidence=evidence))

    removed_push_gate = dict(texts)
    removed_push_gate["administrative-maintenance-synchronization.yml"] = removed_push_gate["administrative-maintenance-synchronization.yml"].replace(
        "github.event.workflow_run.event == 'push'",
        "true",
        1,
    )
    assert any("bounded synchronization marker" in error for error in workflow_coverage_errors(texts=removed_push_gate, evidence=evidence))

    removed_repository_gate = dict(texts)
    removed_repository_gate["administrative-maintenance-synchronization.yml"] = removed_repository_gate["administrative-maintenance-synchronization.yml"].replace(
        "github.event.workflow_run.head_repository.full_name == github.repository",
        "true",
        1,
    )
    assert any("bounded synchronization marker" in error for error in workflow_coverage_errors(texts=removed_repository_gate, evidence=evidence))

    arbitrary_manual_sha = dict(texts)
    arbitrary_manual_sha["administrative-maintenance-synchronization.yml"] = arbitrary_manual_sha["administrative-maintenance-synchronization.yml"].replace(
        "  workflow_dispatch:\n",
        "  workflow_dispatch:\n    inputs:\n      head_sha:\n        required: false\n        type: string\n",
        1,
    ) + "\n# inputs.head_sha\n"
    assert any("manual arbitrary-SHA checkout is forbidden" in error for error in workflow_coverage_errors(texts=arbitrary_manual_sha, evidence=evidence))

    merge_capability = dict(texts)
    merge_capability["administrative-maintenance-synchronization.yml"] += "\n# gh pr merge --auto\n"
    assert any("forbidden merge or administration capability" in error for error in workflow_coverage_errors(texts=merge_capability, evidence=evidence))

    missing_intellect_split = dict(texts)
    missing_intellect_split["administrative-maintenance-synchronization.yml"] = missing_intellect_split["administrative-maintenance-synchronization.yml"].replace(
        "          repositories: INTELLECT\n",
        "          repositories: MATH-PROGRAMME\n",
        1,
    )
    assert any("bounded synchronization marker" in error for error in workflow_coverage_errors(texts=missing_intellect_split, evidence=evidence))

    activation_permissions_drift = dict(texts)
    activation_permissions_drift["administrative-autonomy-activation.yml"] = activation_permissions_drift["administrative-autonomy-activation.yml"].replace(
        "      pull-requests: write\n",
        "      pull-requests: read\n",
        1,
    )
    assert any("activate job delegated permissions drift" in error for error in workflow_coverage_errors(texts=activation_permissions_drift, evidence=evidence))

    activation_environment_removed = dict(texts)
    activation_environment_removed["administrative-autonomy-activation.yml"] = activation_environment_removed["administrative-autonomy-activation.yml"].replace(
        "    environment: release-trust\n",
        "",
        1,
    )
    assert any("activate job must bind protected environment release-trust" in error for error in workflow_coverage_errors(texts=activation_environment_removed, evidence=evidence))

    activation_admin_scope_removed = dict(texts)
    activation_admin_scope_removed["administrative-autonomy-activation.yml"] = activation_admin_scope_removed["administrative-autonomy-activation.yml"].replace(
        "permission-administration: write",
        "permission-administration: read",
        1,
    )
    assert any("missing activation control marker" in error or "exactly one administration-write token" in error for error in workflow_coverage_errors(texts=activation_admin_scope_removed, evidence=evidence))

    activation_main_gate_removed = dict(texts)
    activation_main_gate_removed["administrative-autonomy-activation.yml"] = activation_main_gate_removed["administrative-autonomy-activation.yml"].replace(
        "    branches: [main]\n",
        "    branches: [development]\n",
        1,
    )
    assert any("push trigger must cover main" in error for error in workflow_coverage_errors(texts=activation_main_gate_removed, evidence=evidence))

    print("workflow coverage v2 adversarial tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
