#!/usr/bin/env python3
"""Validate repository-wide experiment and unit-test execution coverage."""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
UNIT_TEST_COMMAND = "python -m unittest discover -s tests -p test_*.py"
MAIN_GUARD = re.compile(r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:")


def normalize_command(value: str) -> str:
    return (
        value.strip()
        .replace("'test_*.py'", "test_*.py")
        .replace('"test_*.py"', "test_*.py")
    )


def load_workflow(root: Path = ROOT) -> dict[str, Any]:
    path = root / ".github" / "workflows" / "ci.yml"
    if not path.is_file():
        return {}
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    return value if isinstance(value, dict) else {}


def workflow_commands(root: Path = ROOT) -> set[str]:
    workflow = load_workflow(root)
    commands: set[str] = set()
    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            run = str(step.get("run", ""))
            commands.update(
                normalize_command(line)
                for line in run.splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            )
    registry_path = root / "governance" / "policy_shard_registry.json"
    if registry_path.is_file():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        for shard_commands in registry.get("shards", {}).values():
            for command in shard_commands:
                if isinstance(command, list) and command:
                    commands.add(normalize_command(" ".join(str(part) for part in command)))
    return commands


def python_module_name(path: Path, root: Path) -> str:
    relative = path.relative_to(root).with_suffix("")
    return ".".join(relative.parts)


def parse_python(path: Path) -> tuple[ast.Module | None, str | None]:
    try:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path)), None
    except SyntaxError as exc:
        return None, f"{path.as_posix()}: invalid Python syntax: {exc.msg}"


def imported_experiment_modules(tree: ast.Module) -> set[str]:
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("experiments."):
                    imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.module.startswith("experiments."):
                imported.add(node.module)
    return imported


def test_contract_errors(path: Path, tree: ast.Module) -> list[str]:
    errors: list[str] = []
    test_methods = 0
    test_cases = 0
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        is_test_case = any(
            (isinstance(base, ast.Attribute) and isinstance(base.value, ast.Name) and base.value.id == "unittest" and base.attr == "TestCase")
            or (isinstance(base, ast.Name) and base.id == "TestCase")
            for base in node.bases
        )
        if not is_test_case:
            continue
        test_cases += 1
        test_methods += sum(
            isinstance(member, (ast.FunctionDef, ast.AsyncFunctionDef)) and member.name.startswith("test")
            for member in node.body
        )
    if test_cases == 0 or test_methods == 0:
        errors.append(
            f"{path.as_posix()}: each discovered unit-test module must define a unittest.TestCase with test methods"
        )
    return errors


def repository_execution_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    commands = workflow_commands(root)
    for required in (
        UNIT_TEST_COMMAND,
        "python3 ci/validate_repository_execution.py",
        "python3 ci/test_repository_execution.py",
    ):
        if normalize_command(required) not in commands:
            errors.append(
                f"governed policy execution is missing repository execution command {required}"
            )

    tests_root = root / "tests"
    test_paths = sorted(tests_root.rglob("test_*.py")) if tests_root.is_dir() else []
    if not test_paths:
        errors.append("repository execution: no tests/test_*.py modules are present")

    experiment_root = root / "experiments"
    experiment_paths = (
        sorted(
            path
            for path in experiment_root.rglob("*.py")
            if path.is_file() and path.name != "__init__.py"
        )
        if experiment_root.is_dir()
        else []
    )
    if not experiment_paths:
        errors.append("repository execution: no governed experiment modules are present")

    module_paths = {python_module_name(path, root): path for path in experiment_paths}
    graph: dict[str, set[str]] = {name: set() for name in module_paths}
    roots: set[str] = set()

    for path in experiment_paths:
        text = path.read_text(encoding="utf-8")
        if text.startswith("#!") or MAIN_GUARD.search(text):
            errors.append(
                f"{path.relative_to(root).as_posix()}: experiment modules must be library-only and exercised through tests"
            )
        tree, syntax_error = parse_python(path)
        if syntax_error:
            errors.append(syntax_error)
            continue
        assert tree is not None
        module = python_module_name(path, root)
        for imported in imported_experiment_modules(tree):
            if imported in module_paths:
                graph[module].add(imported)
            else:
                errors.append(
                    f"{path.relative_to(root).as_posix()}: imports missing governed experiment module {imported}"
                )

    for path in test_paths:
        tree, syntax_error = parse_python(path)
        if syntax_error:
            errors.append(syntax_error)
            continue
        assert tree is not None
        errors.extend(test_contract_errors(path.relative_to(root), tree))
        for imported in imported_experiment_modules(tree):
            if imported in module_paths:
                roots.add(imported)
            else:
                errors.append(
                    f"{path.relative_to(root).as_posix()}: imports missing governed experiment module {imported}"
                )

    reachable: set[str] = set()
    stack = list(roots)
    while stack:
        module = stack.pop()
        if module in reachable:
            continue
        reachable.add(module)
        stack.extend(sorted(graph.get(module, set()) - reachable))

    for module in sorted(set(module_paths) - reachable):
        errors.append(
            "repository execution: experiment module is unreachable from discovered tests: "
            + module_paths[module].relative_to(root).as_posix()
        )
    return errors


def main() -> int:
    errors = repository_execution_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(
            f"repository execution validation failed with {len(errors)} error(s)",
            file=sys.stderr,
        )
        return 1
    print("repository tests and experiment modules have complete governed execution routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
