#!/usr/bin/env python3
"""Adversarial tests for semantic workflow, routing, replay, and artifact contracts."""
from __future__ import annotations

import copy
import json
import tempfile
from pathlib import Path

from validate_workflow_semantics import ROOT, load_workflows, workflow_semantic_errors


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


def main() -> int:
    workflows = load_workflows()
    assert not workflow_semantic_errors(workflows=workflows)

    duplicate_name = copy.deepcopy(workflows)
    duplicate_name["pages.yml"]["name"] = duplicate_name["ci.yml"]["name"]
    assert any("workflow names must be unique" in error for error in workflow_semantic_errors(workflows=duplicate_name))

    mutable_runner = copy.deepcopy(workflows)
    mutable_runner["ci.yml"]["jobs"]["validate-json"]["runs-on"] = "ubuntu-latest"
    assert any("runs-on must be pinned" in error for error in workflow_semantic_errors(workflows=mutable_runner))

    python_line_drift = copy.deepcopy(workflows)
    for step in python_line_drift["ci.yml"]["jobs"]["policy-shard"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/setup-python@"):
            step["with"]["python-version"] = "3.x"
            break
    assert any("setup-python must use governed minor line" in error for error in workflow_semantic_errors(workflows=python_line_drift))

    unpinned_install = copy.deepcopy(workflows)
    unpinned_install["pc-wp04.yml"]["jobs"]["pc-wp04-lean"]["steps"].append(
        {"run": "python -m pip install jsonschema"}
    )
    assert any("unpinned pip install is forbidden" in error for error in workflow_semantic_errors(workflows=unpinned_install))

    missing_classifier = copy.deepcopy(workflows)
    for step in missing_classifier["ci.yml"]["jobs"]["impact"]["steps"]:
        if "policy_impact.py classify" in str(step.get("run", "")):
            step["run"] = "echo classifier omitted"
            break
    assert any("impact classifier" in error for error in workflow_semantic_errors(workflows=missing_classifier))

    shallow_classifier = copy.deepcopy(workflows)
    for step in shallow_classifier["ci.yml"]["jobs"]["impact"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/checkout@"):
            step["with"]["fetch-depth"] = "1"
            break
    assert any("full-history checkout" in error for error in workflow_semantic_errors(workflows=shallow_classifier))

    missing_shard = copy.deepcopy(workflows)
    missing_shard["ci.yml"]["jobs"]["policy-shard"]["strategy"]["matrix"]["shard"] = [
        "core", "fixtures", "cmdg", "administrative", "campaigns", "contracts"
    ]
    assert any("every governed shard" in error for error in workflow_semantic_errors(workflows=missing_shard))

    missing_shard_runner = copy.deepcopy(workflows)
    for step in missing_shard_runner["ci.yml"]["jobs"]["policy-shard"]["steps"]:
        if "run_policy_shard.py" in str(step.get("run", "")):
            step["run"] = "echo shard execution omitted"
            break
    assert any("shard registry runner" in error for error in workflow_semantic_errors(workflows=missing_shard_runner))

    missing_noop = copy.deepcopy(workflows)
    for step in missing_noop["ci.yml"]["jobs"]["policy-shard"]["steps"]:
        if "VERIFIED_POLICY_SHARD_NO_OP" in str(step.get("run", "")):
            step["run"] = "echo skipped"
            break
    assert any("irrelevant shard no-op" in error for error in workflow_semantic_errors(workflows=missing_noop))

    missing_aggregate = copy.deepcopy(workflows)
    missing_aggregate["ci.yml"]["jobs"]["validate-json"]["needs"] = ["impact"]
    assert any("aggregate impact and policy-shard" in error for error in workflow_semantic_errors(workflows=missing_aggregate))

    unsafe_aggregate = copy.deepcopy(workflows)
    unsafe_aggregate["ci.yml"]["jobs"]["validate-json"]["if"] = "success()"
    assert any("run under always()" in error for error in workflow_semantic_errors(workflows=unsafe_aggregate))

    missing_formal_gate = copy.deepcopy(workflows)
    for step in missing_formal_gate["ci.yml"]["jobs"]["log-gcd-lean"]["steps"]:
        if "formal_replay_gate.py decide" in str(step.get("run", "")):
            step["run"] = str(step["run"]).replace(
                "formal_replay_gate.py decide", "formal_replay_attestation.py decide"
            )
            break
    assert any("formal replay impact-gate" in error for error in workflow_semantic_errors(workflows=missing_formal_gate))

    missing_full_replay = copy.deepcopy(workflows)
    for step in missing_full_replay["ci.yml"]["jobs"]["pc-wp04-lean"]["steps"]:
        if "lake build" in str(step.get("run", "")):
            step["run"] = "echo replay removed"
            break
    assert any("retain full Lean replay path" in error for error in workflow_semantic_errors(workflows=missing_full_replay))

    short_retention = copy.deepcopy(workflows)
    for step in short_retention["ci.yml"]["jobs"]["policy-shard"]["steps"]:
        if step.get("with", {}).get("name") == "validated-site":
            step["with"]["retention-days"] = "2"
            break
    assert any("retention must be exactly one day" in error for error in workflow_semantic_errors(workflows=short_retention))

    stale_pages = copy.deepcopy(workflows)
    stale_pages["pages.yml"]["concurrency"]["cancel-in-progress"] = "false"
    assert any("cancel stale" in error for error in workflow_semantic_errors(workflows=stale_pages))

    missing_freshness = copy.deepcopy(workflows)
    for step in missing_freshness["pages.yml"]["jobs"]["build"]["steps"]:
        if "refs/heads/main:refs/remotes/origin/main" in str(step.get("run", "")):
            step["run"] = "echo freshness omitted"
            break
    assert any("exact-artifact publication check" in error for error in workflow_semantic_errors(workflows=missing_freshness))

    checkout_drift = copy.deepcopy(workflows)
    for step in checkout_drift["pages.yml"]["jobs"]["build"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/checkout@"):
            step["with"]["ref"] = "main"
            break
    assert any("validated workflow_run.head_sha" in error for error in workflow_semantic_errors(workflows=checkout_drift))

    pages_rebuild = copy.deepcopy(workflows)
    pages_rebuild["pages.yml"]["jobs"]["build"]["steps"].append({"run": "mkdocs build --strict"})
    assert any("without resolving dependencies or rebuilding" in error for error in workflow_semantic_errors(workflows=pages_rebuild))

    missing_artifact_digest = copy.deepcopy(workflows)
    for step in missing_artifact_digest["pages.yml"]["jobs"]["build"]["steps"]:
        run = str(step.get("run", ""))
        if "hashlib.sha256(artifact_zip)" in run:
            step["run"] = run.replace("hashlib.sha256(artifact_zip)", "hashlib.md5(artifact_zip)", 1)
            break
    assert any("hashlib.sha256(artifact_zip)" in error for error in workflow_semantic_errors(workflows=missing_artifact_digest))

    missing_deployment_id = copy.deepcopy(workflows)
    for step in missing_deployment_id["pages.yml"]["jobs"]["deploy"]["steps"]:
        if str(step.get("uses", "")).startswith("actions/deploy-pages@"):
            step.pop("id", None)
            break
    assert any("must have id deployment" in error for error in workflow_semantic_errors(workflows=missing_deployment_id))

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        copy_root_contracts(root)
        (root / "requirements" / "policy.txt").write_text(
            "jsonschema\nPyYAML==6.0.3\n", encoding="utf-8"
        )
        assert any("exact governed policy pins" in error for error in workflow_semantic_errors(root=root, workflows=workflows))

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        copy_root_contracts(root)
        registry_path = root / "governance" / "policy_shard_registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["shards"]["contracts"] = [
            command
            for command in registry["shards"]["contracts"]
            if not (command[:4] == ["python", "-m", "unittest", "discover"] and "test_*.py" in command)
        ]
        registry_path.write_text(json.dumps(registry), encoding="utf-8")
        assert any("unittest discover" in error for error in workflow_semantic_errors(root=root, workflows=workflows))

    print("workflow semantic rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
