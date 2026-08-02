#!/usr/bin/env python3
"""Validate that every executable CI policy script is reachable from a governed workflow."""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from gcl import validate_tooling
from validate_administrative_maintenance_control import (
    DEFAULT_CONTROL as ADMINISTRATIVE_MAINTENANCE_CONTROL,
    DEFAULT_SCHEMA as ADMINISTRATIVE_MAINTENANCE_SCHEMA,
    validate as validate_administrative_maintenance_control,
)
from validate_gcl_truth_spine import (
    DEFAULT_MATRIX as GCL_TRUTH_SPINE_MATRIX,
    DEFAULT_MATRIX_SCHEMA as GCL_TRUTH_SPINE_MATRIX_SCHEMA,
    DEFAULT_REGISTRY as GCL_TRUTH_SPINE_REGISTRY,
    DEFAULT_REGISTRY_SCHEMA as GCL_TRUTH_SPINE_REGISTRY_SCHEMA,
    validate as validate_gcl_truth_spine,
)

ROOT = Path(__file__).resolve().parents[1]
PYTHON_COMMAND = re.compile(r"(?:^|[;&|({\s])python(?:3)?\s+([A-Za-z0-9_./-]+\.py)(?=\s|$)")
MAIN_GUARD = re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:")


def workflow_python_roots(root: Path = ROOT) -> set[str]:
    roots: set[str] = set()
    workflow_dir = root / ".github" / "workflows"
    for path in sorted(workflow_dir.glob("*.y*ml")):
        workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        if not isinstance(workflow, dict):
            continue
        for job in workflow.get("jobs", {}).values():
            for step in job.get("steps", []):
                run = str(step.get("run", ""))
                roots.update(match.group(1) for match in PYTHON_COMMAND.finditer(run))
    registry_path = root / "ci" / "campaign_replay_registry.json"
    if registry_path.is_file():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for entry in registry.get("entries", []):
            command = entry.get("command", [])
            if len(command) >= 2 and command[0] in {"python", "python3"}:
                roots.add(str(command[1]))
    return roots


def ci_modules(root: Path = ROOT) -> dict[str, str]:
    return {
        path.stem: path.relative_to(root).as_posix()
        for path in sorted((root / "ci").glob("*.py"))
        if path.is_file()
    }


def imported_ci_paths(path: Path, modules: dict[str, str]) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError:
        return set()
    imported: set[str] = set()
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names.extend(alias.name.split(".", 1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module.split(".", 1)[0])
        for name in names:
            if name in modules:
                imported.add(modules[name])
    return imported


def executable_ci_scripts(root: Path = ROOT) -> set[str]:
    scripts: set[str] = set()
    for path in sorted((root / "ci").glob("*.py")):
        text = path.read_text(encoding="utf-8")
        if text.startswith("#!") or MAIN_GUARD.search(text):
            scripts.add(path.relative_to(root).as_posix())
    return scripts


def reachable_ci_scripts(root: Path = ROOT) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    modules = ci_modules(root)
    roots = workflow_python_roots(root)
    graph: dict[str, set[str]] = {}
    for relative in modules.values():
        graph[relative] = imported_ci_paths(root / relative, modules)

    reachable: set[str] = set()
    stack = [path for path in roots if path.startswith("ci/")]
    for path in sorted(roots):
        if path.endswith(".py") and not (root / path).is_file():
            errors.append(f"workflow or replay registry invokes missing Python script {path}")
    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        stack.extend(sorted(graph.get(current, set()) - reachable))
    return reachable, errors


def policy_reachability_errors(root: Path = ROOT) -> list[str]:
    reachable, errors = reachable_ci_scripts(root)
    executable = executable_ci_scripts(root)
    for path in sorted(executable - reachable):
        errors.append(f"CI policy reachability: executable script is unreachable from workflows: {path}")

    for error in validate_administrative_maintenance_control(
        ADMINISTRATIVE_MAINTENANCE_CONTROL,
        ADMINISTRATIVE_MAINTENANCE_SCHEMA,
    ):
        errors.append(f"administrative maintenance control: {error}")

    for error in validate_gcl_truth_spine(
        GCL_TRUTH_SPINE_REGISTRY,
        GCL_TRUTH_SPINE_REGISTRY_SCHEMA,
        GCL_TRUTH_SPINE_MATRIX,
        GCL_TRUTH_SPINE_MATRIX_SCHEMA,
    ):
        errors.append(f"GCL truth spine: {error}")

    for error in validate_tooling(root):
        errors.append(f"GCL work-package tooling: {error}")
    return errors


def main() -> int:
    errors = policy_reachability_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"CI policy reachability failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("every executable CI policy script is reachable from a governed workflow")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
