#!/usr/bin/env python3
"""Validate that every executable CI policy script is reachable from a governed workflow."""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

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
from validate_negative_knowledge import validate as validate_negative_knowledge
from validate_portfolio import validate as validate_portfolio
from validate_synthesis import validate as validate_synthesis

ROOT = Path(__file__).resolve().parents[1]
PYTHON_COMMAND = re.compile(r"(?:^|[;&|({\s])python(?:3)?\s+([A-Za-z0-9_./-]+\.py)(?=\s|$)")
MAIN_GUARD = re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:")
TOOLING_CONTROL_PATHS = (
    "ci/gcl.py",
    "governance/gcl_tooling_command_contract.json",
    "schemas/gcl_tooling_command_contract.schema.json",
    "schemas/gcl_local_identity_manifest.schema.json",
)
NEGATIVE_KNOWLEDGE_CONTROL_PATHS = (
    "ci/validate_negative_knowledge.py",
    "negative_knowledge/pilot_registry.json",
    "schemas/negative_knowledge_registry.schema.json",
)
PORTFOLIO_CONTROL_PATHS = (
    "ci/render_portfolio.py",
    "ci/validate_portfolio.py",
    "portfolio/pilot_registry.json",
    "schemas/gcl_portfolio_registry.schema.json",
    "docs/governance/GCL_PORTFOLIO_VIEW.md",
)
SYNTHESIS_CONTROL_PATHS = (
    "ci/render_synthesis.py",
    "ci/validate_synthesis.py",
    "synthesis/pilot_registry.json",
    "schemas/gcl_synthesis_registry.schema.json",
    "docs/governance/GCL_SYNTHESIS_REPORT.md",
    "docs/governance/GCL_SYNTHESIS_REVIEW_PACKET.md",
)


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
    return {path.stem: path.relative_to(root).as_posix() for path in sorted((root / "ci").glob("*.py")) if path.is_file()}


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
    graph = {relative: imported_ci_paths(root / relative, modules) for relative in modules.values()}
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


def conditional_control_errors(root: Path, label: str, paths: tuple[str, ...], validate_control) -> list[str]:
    present = [relative for relative in paths if (root / relative).is_file()]
    if not present:
        return []
    missing = [relative for relative in paths if relative not in present]
    if missing:
        return [f"{label}: incomplete control surface; missing " + ", ".join(missing)]
    return [f"{label}: {error}" for error in validate_control()]


def tooling_control_errors(root: Path) -> list[str]:
    return conditional_control_errors(root, "GCL work-package tooling", TOOLING_CONTROL_PATHS, lambda: validate_tooling(root))


def negative_knowledge_control_errors(root: Path) -> list[str]:
    return conditional_control_errors(
        root,
        "GCL negative knowledge",
        NEGATIVE_KNOWLEDGE_CONTROL_PATHS,
        lambda: validate_negative_knowledge(root / "negative_knowledge" / "pilot_registry.json", root / "schemas" / "negative_knowledge_registry.schema.json"),
    )


def portfolio_control_errors(root: Path) -> list[str]:
    return conditional_control_errors(
        root,
        "GCL portfolio",
        PORTFOLIO_CONTROL_PATHS,
        lambda: validate_portfolio(root / "portfolio" / "pilot_registry.json", root / "schemas" / "gcl_portfolio_registry.schema.json", root / "docs" / "governance" / "GCL_PORTFOLIO_VIEW.md"),
    )


def synthesis_control_errors(root: Path) -> list[str]:
    return conditional_control_errors(
        root,
        "GCL synthesis",
        SYNTHESIS_CONTROL_PATHS,
        lambda: validate_synthesis(
            root / "synthesis" / "pilot_registry.json",
            root / "schemas" / "gcl_synthesis_registry.schema.json",
            root / "docs" / "governance" / "GCL_SYNTHESIS_REPORT.md",
            root / "docs" / "governance" / "GCL_SYNTHESIS_REVIEW_PACKET.md",
        ),
    )


def policy_reachability_errors(root: Path = ROOT) -> list[str]:
    reachable, errors = reachable_ci_scripts(root)
    executable = executable_ci_scripts(root)
    for path in sorted(executable - reachable):
        errors.append(f"CI policy reachability: executable script is unreachable from workflows: {path}")
    for error in validate_administrative_maintenance_control(ADMINISTRATIVE_MAINTENANCE_CONTROL, ADMINISTRATIVE_MAINTENANCE_SCHEMA):
        errors.append(f"administrative maintenance control: {error}")
    for error in validate_gcl_truth_spine(GCL_TRUTH_SPINE_REGISTRY, GCL_TRUTH_SPINE_REGISTRY_SCHEMA, GCL_TRUTH_SPINE_MATRIX, GCL_TRUTH_SPINE_MATRIX_SCHEMA):
        errors.append(f"GCL truth spine: {error}")
    errors.extend(tooling_control_errors(root))
    errors.extend(negative_knowledge_control_errors(root))
    errors.extend(portfolio_control_errors(root))
    errors.extend(synthesis_control_errors(root))
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
