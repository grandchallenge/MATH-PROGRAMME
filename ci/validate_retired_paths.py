#!/usr/bin/env python3
"""Validate retired repository paths and their bounded historical references."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
RETIRED_PATH = "DOMAIN_04_POINCARE_RECONSTRUCTION_MASTER_PLAN.md"
CANONICAL_PATH = "DOMAIN_05_POINCARE_RECONSTRUCTION_MASTER_PLAN.md"
CROSSWALK_PATH = "reviews/poincare/HISTORICAL_IDENTITY_CROSSWALK.yaml"
POLICY_SHARD_REGISTRY = "governance/policy_shard_registry.json"
REFERENCE_MARKERS = {
    "FILE_MANIFEST.md": "was removed in PR #96",
    "docs/REPOSITORY_DOCS.md": "was removed in PR #96",
    "docs/decisions/ADR-0006_POINCARE_RECONSTRUCTION_ARCHIVE.md": (
        "retired from the current tree"
    ),
    "docs/decisions/ADR-0011_FULL_WORKFLOW_COVERAGE.md": (
        "PR #96 removed the mislabelled"
    ),
}
POLICY_MARKERS = (
    "python3 ci/validate_retired_paths.py",
    "python3 ci/test_retired_paths.py",
)
ALLOWED_RELATIONS = {
    "canonical_retirement_notice",
    "version_history_provenance",
    "historical_alias_registry",
    "frozen_review_provenance",
}
SCAN_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py", ".toml"}
SELF_PATHS = {
    "ci/validate_retired_paths.py",
    "ci/test_retired_paths.py",
    CROSSWALK_PATH,
}


def repository_texts(root: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in SCAN_SUFFIXES:
            continue
        relative_path = path.relative_to(root)
        relative = relative_path.as_posix()
        if relative in SELF_PATHS or any(part.startswith(".") for part in relative_path.parts):
            continue
        texts[relative] = path.read_text(encoding="utf-8")
    return texts


def load_crosswalk(root: Path = ROOT) -> dict[str, Any]:
    path = root / CROSSWALK_PATH
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def load_policy_registry(root: Path = ROOT) -> dict[str, Any]:
    path = root / POLICY_SHARD_REGISTRY
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def policy_registry_commands(registry: dict[str, Any]) -> set[str]:
    commands: set[str] = set()
    shards = registry.get("shards", {})
    if not isinstance(shards, dict):
        return commands
    for entries in shards.values():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, list) and entry and all(isinstance(part, str) for part in entry):
                commands.add(" ".join(entry))
    return commands


def retired_path_errors(
    root: Path = ROOT,
    texts: dict[str, str] | None = None,
    policy_text: str | None = None,
    crosswalk: dict[str, Any] | None = None,
    policy_registry: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    texts = repository_texts(root) if texts is None else texts
    crosswalk = load_crosswalk(root) if crosswalk is None else crosswalk
    policy_registry = load_policy_registry(root) if policy_registry is None else policy_registry
    if policy_text is None:
        policy_path = root / ".github" / "workflows" / "ci.yml"
        policy_text = policy_path.read_text(encoding="utf-8") if policy_path.is_file() else ""
    policy_surface = policy_text + "\n" + "\n".join(sorted(policy_registry_commands(policy_registry)))

    if (root / RETIRED_PATH).exists():
        errors.append(f"retired path must not exist in current tree: {RETIRED_PATH}")
    if not (root / CANONICAL_PATH).is_file():
        errors.append(f"canonical replacement is missing: {CANONICAL_PATH}")

    if crosswalk.get("retired_path") != RETIRED_PATH:
        errors.append("historical identity crosswalk has the wrong retired_path")
    if crosswalk.get("canonical_path") != CANONICAL_PATH:
        errors.append("historical identity crosswalk has the wrong canonical_path")
    if crosswalk.get("governing_decision") != "ADR-0006":
        errors.append("historical identity crosswalk must be governed by ADR-0006")

    entries = crosswalk.get("references", [])
    if not isinstance(entries, list):
        errors.append("historical identity crosswalk references must be a list")
        entries = []
    crosswalk_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("historical identity crosswalk entry must be a mapping")
            continue
        relative = str(entry.get("path", ""))
        relation = str(entry.get("relation", ""))
        marker = str(entry.get("required_marker", ""))
        if not relative:
            errors.append("historical identity crosswalk entry is missing path")
            continue
        if relative in crosswalk_paths:
            errors.append(f"historical identity crosswalk has duplicate path {relative}")
        crosswalk_paths.add(relative)
        if relation not in ALLOWED_RELATIONS:
            errors.append(f"{relative}: unsupported historical identity relation {relation!r}")
        if relation == "frozen_review_provenance" and not relative.startswith(
            "reviews/poincare/"
        ):
            errors.append(f"{relative}: frozen review provenance must live under reviews/poincare/")
        text = texts.get(relative)
        if text is None:
            errors.append(f"historical identity crosswalk target is missing: {relative}")
            continue
        if RETIRED_PATH not in text:
            errors.append(f"{relative}: crosswalk target omits retired path identity")
        if not marker or marker not in text:
            errors.append(f"{relative}: crosswalk target is missing required marker {marker!r}")

    permitted = set(REFERENCE_MARKERS) | crosswalk_paths
    for relative, text in sorted(texts.items()):
        if RETIRED_PATH in text and relative not in permitted:
            errors.append(f"{relative}: ungoverned reference to retired path {RETIRED_PATH}")

    for relative, marker in REFERENCE_MARKERS.items():
        text = texts.get(relative)
        if text is None:
            errors.append(f"retired-path reference record is missing: {relative}")
            continue
        if RETIRED_PATH not in text:
            errors.append(f"{relative}: missing retired path identity {RETIRED_PATH}")
        if marker not in text:
            errors.append(f"{relative}: missing retirement marker {marker!r}")

    for marker in POLICY_MARKERS:
        if marker not in policy_surface:
            errors.append(f"global policy is missing retired-path check: {marker}")

    return errors


def main() -> int:
    errors = retired_path_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"retired-path validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        "retired path, canonical replacement, historical identity crosswalk, and global policy "
        "binding are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
