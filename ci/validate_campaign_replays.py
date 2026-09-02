#!/usr/bin/env python3
"""Validate and execute governed campaign replay contracts with transition-aware routing."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "ci" / "campaign_replay_registry.json"
REGISTRY_RELATIVE = "ci/campaign_replay_registry.json"
SCHEMA_PATH = ROOT / "schemas" / "campaign_replay_registry.schema.json"
MAIN_GUARD = re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:")
ZERO_SHA = "0" * 40


class ReplayRoutingError(RuntimeError):
    """Raised when transition-aware replay selection cannot be established safely."""


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


def is_executable_python(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return text.startswith("#!") or bool(MAIN_GUARD.search(text))


def discovered_campaign_scripts(root: Path = ROOT) -> set[str]:
    """Discover executable campaign Python files independently of the registry."""
    return {
        path.relative_to(root).as_posix()
        for path in (root / "campaigns").rglob("*.py")
        if path.is_file() and is_executable_python(path)
    }


def registry_errors(registry: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    schema = load_json(root / "schemas" / "campaign_replay_registry.schema.json")
    validator = Draft202012Validator(schema)
    errors.extend(
        f"campaign replay registry{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(registry), key=lambda item: list(item.path))
    )

    entries = registry.get("entries", [])
    exemptions = registry.get("exemptions", [])
    ids = [str(entry.get("id", "")) for entry in entries]
    command_paths = [
        str(entry.get("command", ["", ""])[1])
        for entry in entries
        if len(entry.get("command", [])) >= 2
    ]
    exemption_paths = [str(entry.get("path", "")) for entry in exemptions]
    for duplicate in sorted(duplicate_values(ids)):
        errors.append(f"campaign replay registry: duplicate id {duplicate}")
    for duplicate in sorted(duplicate_values(command_paths)):
        errors.append(f"campaign replay registry: duplicate command path {duplicate}")
    for duplicate in sorted(duplicate_values(exemption_paths)):
        errors.append(f"campaign replay registry: duplicate exemption path {duplicate}")

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

    exempted_scripts: set[str] = set()
    for exemption in exemptions:
        script = str(exemption.get("path", ""))
        path = root / script
        if Path(script).is_absolute() or ".." in Path(script).parts:
            errors.append(f"campaign replay exemption path must be repository-relative: {script}")
        if not path.is_file():
            errors.append(f"campaign replay exemption target is missing: {script}")
        elif not is_executable_python(path):
            errors.append(f"campaign replay exemption target is not executable Python: {script}")
        exempted_scripts.add(script)

    overlap = registered_campaign_scripts & exempted_scripts
    for script in sorted(overlap):
        errors.append(f"campaign replay script may not be both registered and exempt: {script}")

    discovered = discovered_campaign_scripts(root)
    governed = registered_campaign_scripts | exempted_scripts
    for script in sorted(discovered - governed):
        errors.append(f"campaign replay discovery: unregistered executable {script}")
    for script in sorted(registered_campaign_scripts - discovered):
        errors.append(f"campaign replay registry: campaign script is outside executable discovery {script}")
    for script in sorted(exempted_scripts - discovered):
        errors.append(f"campaign replay registry: exemption is outside executable discovery {script}")
    return errors


def entry_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(entry.get("id", "")): entry
        for entry in registry.get("entries", [])
        if isinstance(entry, dict) and entry.get("id")
    }


def campaign_root(path: str) -> str | None:
    parts = Path(path).parts
    if len(parts) < 2 or parts[0] != "campaigns":
        return None
    return parts[1]


def entry_campaign_root(entry: dict[str, Any]) -> str | None:
    command = entry.get("command", [])
    if not isinstance(command, list) or len(command) < 2:
        return None
    return campaign_root(str(command[1]))


def changed_registry_entry_ids(
    base_registry: dict[str, Any], head_registry: dict[str, Any]
) -> set[str]:
    base_entries = entry_map(base_registry)
    head_entries = entry_map(head_registry)
    return {
        label
        for label, entry in head_entries.items()
        if label not in base_entries or base_entries[label] != entry
    }


def affected_replay_ids(
    registry: dict[str, Any],
    changed_paths: list[str],
    *,
    base_registry: dict[str, Any] | None = None,
) -> set[str]:
    """Return the exact registered replay IDs affected by one repository transition."""
    entries = entry_map(registry)
    roots = {
        root
        for path in changed_paths
        if (root := campaign_root(path)) is not None
    }
    selected = {
        label
        for label, entry in entries.items()
        if entry_campaign_root(entry) in roots
    }

    if REGISTRY_RELATIVE in changed_paths:
        if base_registry is None:
            raise ReplayRoutingError(
                "campaign replay registry changed but predecessor registry is unavailable"
            )
        selected.update(changed_registry_entry_ids(base_registry, registry))

    uncovered_roots = {
        root
        for root in roots
        if not any(entry_campaign_root(entry) == root for entry in entries.values())
    }
    if uncovered_roots:
        joined = ", ".join(sorted(uncovered_roots))
        raise ReplayRoutingError(
            f"changed campaign root has no registered replay entries: {joined}"
        )
    return selected


def run_git(args: list[str], root: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def ensure_commit(commit: str, root: Path = ROOT) -> None:
    if not commit or commit == ZERO_SHA:
        raise ReplayRoutingError("transition commit is unavailable")
    present = run_git(["cat-file", "-e", f"{commit}^{{commit}}"], root=root)
    if present.returncode == 0:
        return
    fetched = run_git(["fetch", "--no-tags", "--depth=1", "origin", commit], root=root)
    if fetched.returncode != 0:
        raise ReplayRoutingError(
            f"unable to fetch transition commit {commit}: {fetched.stderr.strip()}"
        )


def git_changed_paths(base: str, head: str, root: Path = ROOT) -> list[str]:
    ensure_commit(base, root=root)
    ensure_commit(head, root=root)
    result = run_git(["diff", "--name-only", base, head, "--"], root=root)
    if result.returncode != 0:
        raise ReplayRoutingError(f"git diff failed: {result.stderr.strip()}")
    return sorted({line.strip() for line in result.stdout.splitlines() if line.strip()})


def registry_at_ref(ref: str, root: Path = ROOT) -> dict[str, Any]:
    ensure_commit(ref, root=root)
    result = run_git(["show", f"{ref}:{REGISTRY_RELATIVE}"], root=root)
    if result.returncode != 0:
        raise ReplayRoutingError(
            f"unable to read predecessor campaign replay registry: {result.stderr.strip()}"
        )
    try:
        value = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ReplayRoutingError("predecessor campaign replay registry is not valid JSON") from exc
    if not isinstance(value, dict):
        raise ReplayRoutingError("predecessor campaign replay registry must be an object")
    return value


def transition_refs_from_event(
    event_name: str | None = None,
    event_path: str | None = None,
) -> tuple[str, str] | None:
    event_name = event_name or os.environ.get("GITHUB_EVENT_NAME", "")
    event_path = event_path or os.environ.get("GITHUB_EVENT_PATH")
    if event_name not in {"pull_request", "push"}:
        return None
    if not event_path:
        raise ReplayRoutingError(f"{event_name} replay routing requires GITHUB_EVENT_PATH")
    try:
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReplayRoutingError(f"unable to read GitHub event payload: {exc}") from exc
    if event_name == "pull_request":
        pull_request = event.get("pull_request") or {}
        base = str((pull_request.get("base") or {}).get("sha") or "")
        head = str((pull_request.get("head") or {}).get("sha") or "")
    else:
        base = str(event.get("before") or "")
        head = str(event.get("after") or os.environ.get("GITHUB_SHA") or "")
    if not base or not head or base == ZERO_SHA:
        raise ReplayRoutingError(f"{event_name} transition base/head is unavailable")
    return base, head


def execute_replays(
    registry: dict[str, Any],
    root: Path = ROOT,
    *,
    only_ids: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    for entry in registry["entries"]:
        label = entry["id"]
        if only_ids is not None and label not in only_ids:
            continue
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
    mode = "coverage"
    replay_ids: set[str] | None = set()

    if not errors and not args.check_only:
        try:
            transition = transition_refs_from_event()
            if transition is None:
                replay_ids = None
                mode = "coverage and full execution"
            else:
                base, head = transition
                changed_paths = git_changed_paths(base, head)
                base_registry = (
                    registry_at_ref(base) if REGISTRY_RELATIVE in changed_paths else None
                )
                replay_ids = affected_replay_ids(
                    registry,
                    changed_paths,
                    base_registry=base_registry,
                )
                mode = f"coverage and affected execution ({len(replay_ids)} replay(s))"
        except ReplayRoutingError as exc:
            errors.append(f"campaign replay routing: {exc}")

    if not errors and not args.check_only:
        errors.extend(execute_replays(registry, only_ids=replay_ids))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"campaign replay validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"governed campaign replay {mode} is complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
