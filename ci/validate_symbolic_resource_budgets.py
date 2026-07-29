#!/usr/bin/env python3
"""Discover and validate all registered expensive symbolic lanes."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterator

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = Path("governance/expensive_symbolic_lane_registry.json")
SCHEMA = Path("schemas/expensive_symbolic_lane_registry.schema.json")
STRUCTURED_SUFFIXES = {".json", ".yaml", ".yml"}

BUDGET_INTEGER_FIELDS = (
    "max_variables",
    "max_total_degree",
    "max_runtime_seconds",
    "max_basis_elements",
    "max_intermediate_terms",
)
BUDGET_TEXT_FIELDS = (
    "monomial_order",
    "backend",
    "backend_version",
    "fallback_route",
)
FAILURE_STATUSES = {
    "timeout",
    "degree_explosion",
    "basis_size_explosion",
    "memory_exhaustion",
    "unstable_modular_reconstruction",
    "unsuitable_monomial_order",
    "side_conditions_missing",
    "not_actually_algebraic",
    "cancelled_by_budget",
}


class SymbolicBudgetError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SymbolicBudgetError(message)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_structured(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    return yaml.safe_load(text)


def walk(value: Any) -> Iterator[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def validate_budget(lane_id: str, budget: Any) -> None:
    require(isinstance(budget, dict), f"{lane_id}: resource_budget must be an object")
    for field in BUDGET_INTEGER_FIELDS:
        value = budget.get(field)
        require(
            isinstance(value, int) and not isinstance(value, bool) and value > 0,
            f"{lane_id}: resource_budget.{field} must be a positive integer",
        )
    for field in BUDGET_TEXT_FIELDS:
        require(
            nonempty(budget.get(field)),
            f"{lane_id}: resource_budget.{field} is required",
        )


def validate_ledger(lane_id: str, ledger: Any) -> None:
    require(isinstance(ledger, dict), f"{lane_id}: run_ledger must be an object")
    execution = ledger.get("execution_status")
    termination = ledger.get("termination_status")
    failure = ledger.get("failure_status")
    failure_record = ledger.get("failure_record")
    result_artifact = ledger.get("result_artifact")
    recorded_at = ledger.get("recorded_at")

    require(
        execution in {"not_started", "completed", "failed"},
        f"{lane_id}: invalid execution_status",
    )
    if execution == "not_started":
        require(termination == "not_started", f"{lane_id}: unstarted lane has invalid termination_status")
        require(failure is None, f"{lane_id}: unstarted lane cannot carry failure_status")
        require(failure_record is None, f"{lane_id}: unstarted lane cannot carry failure_record")
        require(result_artifact is None, f"{lane_id}: unstarted lane cannot carry result_artifact")
        require(recorded_at is None, f"{lane_id}: unstarted lane cannot carry recorded_at")
    elif execution == "completed":
        require(termination == "success", f"{lane_id}: completed lane must terminate with success")
        require(failure is None and failure_record is None, f"{lane_id}: completed lane cannot carry failure evidence")
        require(nonempty(result_artifact), f"{lane_id}: completed lane requires result_artifact")
        require(nonempty(recorded_at), f"{lane_id}: completed lane requires recorded_at")
    else:
        require(termination in FAILURE_STATUSES, f"{lane_id}: failed lane needs controlled termination_status")
        require(failure == termination, f"{lane_id}: failure_status must equal termination_status")
        require(nonempty(failure_record), f"{lane_id}: failed lane requires a failure_record")
        require(result_artifact is None, f"{lane_id}: failed lane cannot claim result_artifact")
        require(nonempty(recorded_at), f"{lane_id}: failed lane requires recorded_at")


def validate_lane(lane: dict[str, Any], source: str) -> tuple[str, str]:
    lane_id = lane.get("lane_id")
    require(nonempty(lane_id), f"{source}: marked symbolic lane requires lane_id")
    require(
        lane.get("lane_class") == "expensive_symbolic",
        f"{lane_id}: lane_class must be expensive_symbolic",
    )
    validate_budget(lane_id, lane.get("resource_budget"))
    validate_ledger(lane_id, lane.get("run_ledger"))
    return source, lane_id


def discover(root: Path, scan_roots: list[str]) -> dict[tuple[str, str], dict[str, Any]]:
    discovered: dict[tuple[str, str], dict[str, Any]] = {}
    for relative_root in scan_roots:
        base = root / relative_root
        require(base.is_dir(), f"symbolic lane scan root is missing: {relative_root}")
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in STRUCTURED_SUFFIXES:
                continue
            text = path.read_text(encoding="utf-8")
            if "expensive_symbolic" not in text and "lane_class" not in text:
                continue
            relative = path.relative_to(root).as_posix()
            try:
                document = load_structured(path)
            except (OSError, ValueError, yaml.YAMLError) as exc:
                raise SymbolicBudgetError(f"{relative}: cannot parse marked symbolic document: {exc}") from exc
            for item in walk(document):
                if item.get("lane_class") != "expensive_symbolic":
                    continue
                key = validate_lane(item, relative)
                require(key not in discovered, f"duplicate symbolic lane declaration: {key[1]} in {relative}")
                discovered[key] = item
    return discovered


def validate(root: Path = ROOT) -> None:
    registry_path = root / REGISTRY
    schema_path = root / SCHEMA
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(registry),
        key=lambda error: list(error.path),
    )
    require(not errors, "; ".join(error.message for error in errors))

    entries = registry["entries"]
    registered = [(entry["path"], entry["lane_id"]) for entry in entries]
    require(len(registered) == len(set(registered)), "symbolic lane registry contains duplicate path/lane entries")
    lane_ids = [lane_id for _, lane_id in registered]
    require(len(lane_ids) == len(set(lane_ids)), "symbolic lane registry contains duplicate lane IDs")

    discovered = discover(root, registry["scan_roots"])
    registered_set = set(registered)
    discovered_set = set(discovered)
    missing = sorted(registered_set - discovered_set)
    orphaned = sorted(discovered_set - registered_set)
    require(not missing, f"registered symbolic lanes were not discovered: {missing}")
    require(not orphaned, f"unregistered expensive symbolic lanes discovered: {orphaned}")


def main() -> int:
    try:
        validate()
    except (SymbolicBudgetError, OSError, json.JSONDecodeError) as exc:
        print(f"symbolic resource-budget validation rejected: {exc}", file=sys.stderr)
        return 1
    print("symbolic resource budgets checked: all discovered lanes are registered, bounded, and ledgered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
