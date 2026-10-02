#!/usr/bin/env python3
"""Adversarial tests for semantic policy, formal-routing, and publication contracts."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from validate_workflow_semantics import (
    REPOSITORY_REGRESSION_COMMAND,
    ROOT,
    load_workflows,
    workflow_semantic_errors,
)


def copy_root_contracts(root: Path) -> None:
    (root / "requirements").mkdir(parents=True)
    for name in ("policy.txt", "docs.txt"):
        (root / "requirements" / name).write_text(
            (ROOT / "requirements" / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    (root / "governance").mkdir(parents=True)
    (root / "governance" / "policy_shard_registry.json").write_text(
        (ROOT / "governance" / "policy_shard_registry.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )


def errors(workflows):
    return workflow_semantic_errors(workflows=workflows)


def main() -> int:
    workflows = load_workflows()
    baseline = errors(workflows)
    assert not baseline, baseline

    name_drift = copy.deepcopy(workflows)
    name_drift["formal-validation.yml"]["name"] = "campaign-specific-formal-replay"
    assert any("workflow name must be exactly" in error for error in errors(name_drift))

    mutable_runner = copy.deepcopy(workflows)
    mutable_runner["ci.yml"]["jobs"]["validate-json"]["runs-on"] = "ubuntu-latest"
    assert any("runs-on must be pinned" in error for error in errors(mutable_runner))

    python_line_drift = copy.deepcopy(workflows)
    for step in python_line_drift["ci.yml"]["jobs"]["policy-shard"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/setup-python@"):
            step["with"]["python-version"] = "3.x"
            break
    assert any("setup-python must use governed minor line" in error for error in errors(python_line_drift))

    unpinned_install = copy.deepcopy(workflows)
    unpinned_install["pc-wp04.yml"]["jobs"]["replay"]["steps"].append(
        {"run": "python -m pip install jsonschema"}
    )
    assert any("unpinned pip install is forbidden" in error for error in errors(unpinned_install))

    missing_classifier = copy.deepcopy(workflows)
    for step in missing_classifier["ci.yml"]["jobs"]["impact"]["steps"]:
        if "policy_impact.py classify" in str(step.get("run", "")):
            step["run"] = "echo classifier omitted"
            break
    assert any("impact classifier" in error for error in errors(missing_classifier))

    shallow_policy_classifier = copy.deepcopy(workflows)
    for step in shallow_policy_classifier["ci.yml"]["jobs"]["impact"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/checkout@"):
            step["with"]["fetch-depth"] = "1"
            break
    assert any("full-history checkout" in error for error in errors(shallow_policy_classifier))

    static_policy_matrix = copy.deepcopy(workflows)
    static_policy_matrix["ci.yml"]["jobs"]["policy-shard"]["strategy"]["matrix"]["shard"] = ["core"]
    assert any("classifier-produced dynamic shard matrix" in error for error in errors(static_policy_matrix))

    missing_shard_runner = copy.deepcopy(workflows)
    for step in missing_shard_runner["ci.yml"]["jobs"]["policy-shard"]["steps"]:
        if "run_policy_shard.py" in str(step.get("run", "")):
            step["run"] = "echo shard execution omitted"
            break
    assert any("shard registry runner" in error for error in errors(missing_shard_runner))

    missing_aggregate = copy.deepcopy(workflows)
    missing_aggregate["ci.yml"]["jobs"]["validate-json"]["needs"] = ["impact"]
    assert any("aggregate impact and policy-shard" in error for error in errors(missing_aggregate))

    unsafe_aggregate = copy.deepcopy(workflows)
    unsafe_aggregate["ci.yml"]["jobs"]["validate-json"]["if"] = "success()"
    assert any("run under always()" in error for error in errors(unsafe_aggregate))

    retired_formal_job = copy.deepcopy(workflows)
    retired_formal_job["ci.yml"]["jobs"]["log-gcd-lean"] = {
        "runs-on": "ubuntu-24.04",
        "steps": [{"run": "echo obsolete substantive lane"}],
    }
    assert any("retired campaign-specific formal job" in error for error in errors(retired_formal_job))

    policy_owns_formal_cron = copy.deepcopy(workflows)
    policy_owns_formal_cron["ci.yml"]["on"]["schedule"].append({"cron": "17 */6 * * *"})
    assert any("policy workflow must own only" in error for error in errors(policy_owns_formal_cron))

    missing_formal_classifier = copy.deepcopy(workflows)
    for step in missing_formal_classifier["formal-validation.yml"]["jobs"]["impact"]["steps"]:
        if "formal_validation.py classify" in str(step.get("run", "")):
            step["run"] = "echo formal classifier omitted"
            break
    assert any("material formal classifier" in error for error in errors(missing_formal_classifier))

    shallow_formal_classifier = copy.deepcopy(workflows)
    for step in shallow_formal_classifier["formal-validation.yml"]["jobs"]["impact"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/checkout@"):
            step["with"]["fetch-depth"] = "1"
            break
    assert any("impact must use full-history checkout" in error for error in errors(shallow_formal_classifier))

    static_formal_matrix = copy.deepcopy(workflows)
    static_formal_matrix["formal-validation.yml"]["jobs"]["formal-lane"]["strategy"]["matrix"] = {
        "lane": ["log-gcd"]
    }
    assert any("dynamic matrix" in error for error in errors(static_formal_matrix))

    missing_formal_runner = copy.deepcopy(workflows)
    for step in missing_formal_runner["formal-validation.yml"]["jobs"]["formal-lane"]["steps"]:
        if "formal_validation.py run" in str(step.get("run", "")):
            step["run"] = "echo formal runner omitted"
            break
    assert any("generic lane runner" in error for error in errors(missing_formal_runner))

    renamed_formal_aggregate = copy.deepcopy(workflows)
    renamed_formal_aggregate["formal-validation.yml"]["jobs"]["formal-validation"]["name"] = "all-formal-campaigns"
    assert any("required aggregate job name drift" in error for error in errors(renamed_formal_aggregate))

    reintroduced_alias = copy.deepcopy(workflows)
    reintroduced_alias["formal-validation.yml"]["jobs"]["legacy-log-gcd-context"] = {
        "name": "Replay LOG-GCD-001 in Lean",
        "needs": "formal-validation",
        "runs-on": "ubuntu-24.04",
        "steps": [{"run": "echo retired compatibility alias"}],
    }
    assert any(
        "retired compatibility alias must remain absent" in error
        for error in errors(reintroduced_alias)
    )

    pc_pr_trigger = copy.deepcopy(workflows)
    pc_pr_trigger["pc-wp04.yml"]["on"]["pull_request"] = {}
    assert any("promotion replay triggers" in error for error in errors(pc_pr_trigger))

    short_retention = copy.deepcopy(workflows)
    for step in short_retention["ci.yml"]["jobs"]["policy-shard"]["steps"]:
        if step.get("with", {}).get("name") == "validated-site":
            step["with"]["retention-days"] = "2"
            break
    assert any("retention must be exactly one day" in error for error in errors(short_retention))

    stale_pages = copy.deepcopy(workflows)
    stale_pages["pages.yml"]["concurrency"]["cancel-in-progress"] = "false"
    assert any("cancel stale" in error for error in errors(stale_pages))

    checkout_drift = copy.deepcopy(workflows)
    for step in checkout_drift["pages.yml"]["jobs"]["build"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/checkout@"):
            step["with"]["ref"] = "main"
            break
    assert any("workflow_run.head_sha" in error for error in errors(checkout_drift))

    pages_rebuild = copy.deepcopy(workflows)
    pages_rebuild["pages.yml"]["jobs"]["build"]["steps"].append({"run": "mkdocs build --strict"})
    assert any("without rebuilding documentation" in error for error in errors(pages_rebuild))

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        copy_root_contracts(root)
        (root / "requirements" / "policy.txt").write_text(
            "jsonschema\nPyYAML==6.0.3\n", encoding="utf-8"
        )
        assert any(
            "exact governed policy pins" in error
            for error in workflow_semantic_errors(root=root, workflows=workflows)
        )

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        copy_root_contracts(root)
        registry_path = root / "governance" / "policy_shard_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        regression_command = REPOSITORY_REGRESSION_COMMAND.split()
        registry["shards"]["repository-regression"].remove(regression_command)
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        current = workflow_semantic_errors(root=root, workflows=workflows)
        assert any("repository-regression shard is missing" in error for error in current), current

        registry["shards"]["contracts"].append(regression_command)
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        current = workflow_semantic_errors(root=root, workflows=workflows)
        assert any("owned only by repository-regression" in error for error in current), current

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        copy_root_contracts(root)
        registry_path = root / "governance" / "policy_shard_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["shards"]["core"] = [
            command
            for command in registry["shards"]["core"]
            if command != ["python3", "ci/test_formal_validation.py"]
        ]
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        current = workflow_semantic_errors(root=root, workflows=workflows)
        assert any("missing executable coverage command python3 ci/test_formal_validation.py" in error for error in current), current

    print("workflow semantic material-routing rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
