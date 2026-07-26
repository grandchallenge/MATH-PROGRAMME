#!/usr/bin/env python3
"""Validate and execute every governed campaign replay contract."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "ci" / "campaign_replay_registry.json"
SCHEMA_PATH = ROOT / "schemas" / "campaign_replay_registry.schema.json"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def duplicate_values(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def discovered_campaign_scripts(registry: dict[str, Any], root: Path = ROOT) -> set[str]:
    discovered: set[str] = set()
    for pattern in registry.get("discovery_globs", []):
        discovered.update(
            path.relative_to(root).as_posix()
            for path in root.glob(pattern)
            if path.is_file()
        )
    return discovered


def registry_errors(registry: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    schema = load_json(root / "schemas" / "campaign_replay_registry.schema.json")
    validator = Draft202012Validator(schema)
    errors.extend(
        f"campaign replay registry{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(registry), key=lambda item: list(item.path))
    )

    entries = registry.get("entries", [])
    ids = [str(entry.get("id", "")) for entry in entries]
    command_paths = [
        str(entry.get("command", ["", ""])[1])
        for entry in entries
        if len(entry.get("command", [])) >= 2
    ]
    for duplicate in sorted(duplicate_values(ids)):
        errors.append(f"campaign replay registry: duplicate id {duplicate}")
    for duplicate in sorted(duplicate_values(command_paths)):
        errors.append(f"campaign replay registry: duplicate command path {duplicate}")

    registered_campaign_scripts: set[str] = set()
    for entry in entries:
        command = entry.get("command", [])
        label = entry.get("id", "<unknown>")
        if not command or command[0] not in {"python", "python3"}:
            errors.append(f"{label}: command must invoke Python directly without a shell")
            continue
        if len(command) < 2:
            errors.append(f"{label}: command is missing an executable script path")
            continue
        script = str(command[1])
        script_path = root / script
        if Path(script).is_absolute() or ".." in Path(script).parts:
            errors.append(f"{label}: script path must be repository-relative: {script}")
        if not script_path.is_file():
            errors.append(f"{label}: registered replay script is missing: {script}")
        if script.startswith("campaigns/"):
            registered_campaign_scripts.add(script)

    discovered = discovered_campaign_scripts(registry, root)
    for script in sorted(discovered - registered_campaign_scripts):
        errors.append(f"campaign replay discovery: unregistered executable {script}")
    for script in sorted(registered_campaign_scripts - discovered):
        errors.append(f"campaign replay registry: campaign script is outside discovery contract {script}")
    return errors


def execute_replays(registry: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for entry in registry["entries"]:
        label = entry["id"]
        command = entry["command"]
        timeout = entry["timeout_seconds"]
        print(f"::group::{label}")
        print(f"$ {' '.join(command)}")
        try:
            result = subprocess.run(
                command,
                cwd=root,
                text=True,
                capture_output=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            if exc.stdout:
                print(exc.stdout)
            if exc.stderr:
                print(exc.stderr, file=sys.stderr)
            errors.append(f"{label}: timed out after {timeout} seconds")
            print("::endgroup::")
            continue
        if result.stdout:
            print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
        if result.returncode != 0:
            errors.append(f"{label}: command exited with status {result.returncode}")
        print("::endgroup::")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    registry = load_json(REGISTRY_PATH)
    errors = registry_errors(registry)
    if not errors and not args.check_only:
        errors.extend(execute_replays(registry))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"campaign replay validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    mode = "coverage" if args.check_only else "coverage and execution"
    print(f"governed campaign replay {mode} is complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
