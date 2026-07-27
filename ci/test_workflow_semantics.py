#!/usr/bin/env python3
"""Adversarial tests for semantic workflow and dependency contracts."""
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
    assert any("workflow names must be unique" in error for error in workflow_semantic_errors(workflows=duplicate_name))

    mutable_runner = copy.deepcopy(workflows)
    mutable_runner["ci.yml"]["jobs"]["validate-json"]["runs-on"] = "ubuntu-latest"
    assert any("runs-on must be pinned" in error for error in workflow_semantic_errors(workflows=mutable_runner))

    unpinned_install = copy.deepcopy(workflows)
    unpinned_install["pc-wp04.yml"]["jobs"]["pc-wp04-lean"]["steps"].append(
        {"run": "python -m pip install jsonschema"}
    )
    assert any("unpinned pip install is forbidden" in error for error in workflow_semantic_errors(workflows=unpinned_install))

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

    stale_pages = copy.deepcopy(workflows)
    stale_pages["pages.yml"]["concurrency"]["cancel-in-progress"] = "false"
    assert any("cancel stale" in error for error in workflow_semantic_errors(workflows=stale_pages))

    missing_freshness = copy.deepcopy(workflows)
    for step in missing_freshness["pages.yml"]["jobs"]["build"]["steps"]:
        run = str(step.get("run", ""))
        if "refs/heads/main:refs/remotes/origin/main" in run:
            step["run"] = "echo 'freshness omitted'"
            break
    assert any("current-main freshness check" in error for error in workflow_semantic_errors(workflows=missing_freshness))

    checkout_drift = copy.deepcopy(workflows)
    for step in checkout_drift["pages.yml"]["jobs"]["build"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/checkout@"):
            step["with"]["ref"] = "main"
    assert any("validated workflow_run.head_sha" in error for error in workflow_semantic_errors(workflows=checkout_drift))

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
