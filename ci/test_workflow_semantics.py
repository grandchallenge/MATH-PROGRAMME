#!/usr/bin/env python3
"""Adversarial tests for semantic workflow, execution, and artifact contracts."""
from __future__ import annotations

import copy
import tempfile
from pathlib import Path

from validate_workflow_semantics import ROOT, load_workflows, workflow_semantic_errors


def copy_requirements(root: Path) -> None:
    (root / "requirements").mkdir(parents=True)
    for name in ("policy.txt", "docs.txt"):
        (root / "requirements" / name).write_text(
            (ROOT / "requirements" / name).read_text(encoding="utf-8"), encoding="utf-8"
        )


def main() -> int:
    workflows = load_workflows()
    assert not workflow_semantic_errors(workflows=workflows)

    duplicate_name = copy.deepcopy(workflows)
    duplicate_name["pages.yml"]["name"] = duplicate_name["ci.yml"]["name"]
    assert any(
        "workflow names must be unique" in error
        for error in workflow_semantic_errors(workflows=duplicate_name)
    )

    mutable_runner = copy.deepcopy(workflows)
    mutable_runner["ci.yml"]["jobs"]["validate-json"]["runs-on"] = "ubuntu-latest"
    assert any(
        "runs-on must be pinned" in error
        for error in workflow_semantic_errors(workflows=mutable_runner)
    )

    python_line_drift = copy.deepcopy(workflows)
    for step in python_line_drift["ci.yml"]["jobs"]["validate-json"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/setup-python@"):
            step["with"]["python-version"] = "3.x"
            break
    assert any(
        "setup-python must use governed minor line" in error
        for error in workflow_semantic_errors(workflows=python_line_drift)
    )

    unpinned_install = copy.deepcopy(workflows)
    unpinned_install["pc-wp04.yml"]["jobs"]["pc-wp04-lean"]["steps"].append(
        {"run": "python -m pip install jsonschema"}
    )
    assert any(
        "unpinned pip install is forbidden" in error
        for error in workflow_semantic_errors(workflows=unpinned_install)
    )

    comment_spoof = copy.deepcopy(workflows)
    for step in comment_spoof["ci.yml"]["jobs"]["validate-json"]["steps"]:
        run = str(step.get("run", ""))
        if "python3 ci/validate_policy_reachability.py" in run:
            step["run"] = run.replace(
                "python3 ci/validate_policy_reachability.py",
                "echo '# python3 ci/validate_policy_reachability.py'",
                1,
            )
            break
    assert any(
        "validate_policy_reachability.py" in error
        for error in workflow_semantic_errors(workflows=comment_spoof)
    )

    missing_unit_tests = copy.deepcopy(workflows)
    for step in missing_unit_tests["ci.yml"]["jobs"]["validate-json"]["steps"]:
        if step.get("name") == "Run repository unit tests":
            step["run"] = "echo tests skipped"
    assert any(
        "unittest discover" in error
        for error in workflow_semantic_errors(workflows=missing_unit_tests)
    )

    short_retention = copy.deepcopy(workflows)
    for step in short_retention["ci.yml"]["jobs"]["validate-json"]["steps"]:
        if step.get("with", {}).get("name") == "validated-site":
            step["with"]["retention-days"] = "2"
    assert any(
        "retention must be exactly one day" in error
        for error in workflow_semantic_errors(workflows=short_retention)
    )

    stale_pages = copy.deepcopy(workflows)
    stale_pages["pages.yml"]["concurrency"]["cancel-in-progress"] = "false"
    assert any(
        "cancel stale" in error
        for error in workflow_semantic_errors(workflows=stale_pages)
    )

    missing_freshness = copy.deepcopy(workflows)
    for step in missing_freshness["pages.yml"]["jobs"]["build"]["steps"]:
        run = str(step.get("run", ""))
        if "refs/heads/main:refs/remotes/origin/main" in run:
            step["run"] = "echo 'freshness omitted'"
            break
    assert any(
        "exact-artifact publication check" in error
        for error in workflow_semantic_errors(workflows=missing_freshness)
    )

    checkout_drift = copy.deepcopy(workflows)
    for step in checkout_drift["pages.yml"]["jobs"]["build"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/checkout@"):
            step["with"]["ref"] = "main"
    assert any(
        "validated workflow_run.head_sha" in error
        for error in workflow_semantic_errors(workflows=checkout_drift)
    )

    pages_rebuild = copy.deepcopy(workflows)
    pages_rebuild["pages.yml"]["jobs"]["build"]["steps"].append(
        {"run": "mkdocs build --strict"}
    )
    assert any(
        "without resolving dependencies or rebuilding" in error
        for error in workflow_semantic_errors(workflows=pages_rebuild)
    )

    missing_artifact_digest = copy.deepcopy(workflows)
    for step in missing_artifact_digest["pages.yml"]["jobs"]["build"]["steps"]:
        run = str(step.get("run", ""))
        if "hashlib.sha256(artifact_zip)" in run:
            step["run"] = run.replace(
                "hashlib.sha256(artifact_zip)",
                "hashlib.md5(artifact_zip)",
                1,
            )
    assert any(
        "hashlib.sha256(artifact_zip)" in error
        for error in workflow_semantic_errors(workflows=missing_artifact_digest)
    )

    missing_deployment_id = copy.deepcopy(workflows)
    for step in missing_deployment_id["pages.yml"]["jobs"]["deploy"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/deploy-pages@"):
            step.pop("id", None)
    assert any(
        "must have id deployment" in error
        for error in workflow_semantic_errors(workflows=missing_deployment_id)
    )

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        copy_requirements(root)
        (root / "requirements" / "policy.txt").write_text(
            "jsonschema\nPyYAML==6.0.3\n", encoding="utf-8"
        )
        assert any(
            "exact governed policy pins" in error
            for error in workflow_semantic_errors(root=root, workflows=workflows)
        )

    print("workflow semantic rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
