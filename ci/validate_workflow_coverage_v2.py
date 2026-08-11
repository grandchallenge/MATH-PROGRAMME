#!/usr/bin/env python3
from __future__ import annotations

import json

import validate_workflow_coverage_v3 as v3

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
    "visual-pedagogy-representation-repair.yml",
}

ROOT = v3.ROOT
POLICY_SHARD_REGISTRY = "governance/policy_shard_registry.json"
ROUTED_MARKER_SUCCESSORS = {
    "python3 ci/validate_workflow_coverage.py": "python3 ci/validate_workflow_coverage_v2.py",
    "python3 ci/test_workflow_coverage.py": "python3 ci/test_workflow_coverage_v2.py",
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


def workflow_coverage_errors(root=ROOT, texts=None, evidence=None, registry=None):
    errors = v3.workflow_coverage_errors(root=root, texts=texts, evidence=evidence)
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
        "protected exact-head merge, mirror-only synchronization, manual control-plane gates, "
        "and claim boundaries are valid"
    )
    return 0


__all__ = ["ROOT", "workflow_coverage_errors", "main"]

if __name__ == "__main__":
    raise SystemExit(main())
