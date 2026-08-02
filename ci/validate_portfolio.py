#!/usr/bin/env python3
"""Validate the bounded GCL portfolio pilot and its generated view."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from render_portfolio import advisory_interval, render

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "portfolio" / "pilot_registry.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "gcl_portfolio_registry.schema.json"
DEFAULT_VIEW = ROOT / "docs" / "governance" / "GCL_PORTFOLIO_VIEW.md"

EXPECTED = {
    "GCL-PORTFOLIO-WP00": 190,
    "GCL-SYNTHESIS-WP00": 191,
    "GCL-ASSURANCE-PRODUCT-WP00": 192,
    "GCL-DISCLOSURE-WP00": 193,
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(
    registry_path: Path = DEFAULT_REGISTRY,
    schema_path: Path = DEFAULT_SCHEMA,
    view_path: Path = DEFAULT_VIEW,
) -> list[str]:
    errors: list[str] = []
    try:
        registry = load_json(registry_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"registry load failed: {exc}"]
    try:
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"schema load failed: {exc}"]

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(registry), key=lambda item: list(item.path)):
        location = "/".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema {location}: {error.message}")
    if errors:
        return errors

    if set(registry["activation"]["required_conditions"]) != {
        "external_exact_head_review",
        "human_steward_release",
        "protected_merge",
    }:
        errors.append(
            "activation conditions must be the exact external review, Human release, and protected merge set"
        )

    records = registry["records"]
    record_ids = [record["portfolio_record_id"] for record in records]
    work_ids = [record["work_package_id"] for record in records]
    issue_numbers = [record["issue_number"] for record in records]
    if len(records) != 4:
        errors.append("portfolio pilot must contain exactly four records")
    if len(record_ids) != len(set(record_ids)):
        errors.append("portfolio_record_id values must be unique")
    if len(work_ids) != len(set(work_ids)):
        errors.append("work_package_id values must be unique")
    if len(issue_numbers) != len(set(issue_numbers)):
        errors.append("issue_number values must be unique")
    if set(work_ids) != set(EXPECTED):
        errors.append("portfolio pilot must cover exactly GCL work packages #190 through #193")

    issue_for = {record["work_package_id"]: record["issue_number"] for record in records}
    for work_id, expected_issue in EXPECTED.items():
        if issue_for.get(work_id) != expected_issue:
            errors.append(f"{work_id}: expected issue {expected_issue}")

    by_work = {record["work_package_id"]: record for record in records}
    intervals: list[tuple[float, float]] = []
    unknown_metric_seen = False
    for record in records:
        work_id = record["work_package_id"]
        state = record["state"]
        readiness = record["execution_readiness"]
        dependencies = record["dependencies"]
        disposition = record["disposition"]

        if work_id in dependencies:
            errors.append(f"{work_id}: work package cannot depend on itself")
        for dependency in dependencies:
            if dependency not in by_work:
                errors.append(f"{work_id}: unknown dependency {dependency}")
            elif by_work[dependency]["issue_number"] >= record["issue_number"]:
                errors.append(f"{work_id}: dependency order must point to an earlier umbrella package")

        if state == "active":
            if dependencies:
                errors.append(f"{work_id}: active record must not retain blocking dependencies")
            if disposition["status"] != "authorized_tranche_execution":
                errors.append(f"{work_id}: active record requires authorized_tranche_execution disposition")
            if readiness == "unknown" or readiness < 2:
                errors.append(f"{work_id}: active record requires explicit nontrivial execution readiness")
        else:
            if not dependencies:
                errors.append(f"{work_id}: non-active record requires at least one dependency")
            if disposition["status"] != "blocked_by_ordered_dependency":
                errors.append(f"{work_id}: blocked pilot record requires blocked_by_ordered_dependency disposition")
            if readiness == "unknown" or readiness > 1:
                errors.append(f"{work_id}: blocked record readiness must be explicit and at most one")

        freshness = record["evidence_freshness"]
        if freshness["status"] == "current" and freshness["refresh_obligation"] is not None:
            errors.append(f"{work_id}: current evidence must not carry a refresh obligation")
        if freshness["status"] in {"stale", "unknown"} and not freshness["refresh_obligation"]:
            errors.append(f"{work_id}: stale or unknown evidence requires a refresh obligation")

        if record["reversibility"]["irreversible_commitment"]:
            errors.append(f"{work_id}: portfolio pilot cannot encode irreversible commitment")
        if disposition["automated"] or disposition["machine_action"] is not None:
            errors.append(f"{work_id}: automated disposition is prohibited")
        if not disposition["advisory_only"]:
            errors.append(f"{work_id}: disposition must remain advisory only")
        if any(record["claim_boundaries"].values()):
            errors.append(f"{work_id}: claim-boundary promotion is prohibited")

        metric_values = [
            record["scientific_importance"],
            record["execution_readiness"],
            record["institutional_leverage"],
            record["expected_information_gain"],
            *record["cost"].values(),
            *record["risk"].values(),
            *record["decisive_falsification"].values(),
            record["transfer_value"],
            record["publication_value"],
            record["product_value"],
        ]
        unknown_metric_seen = unknown_metric_seen or "unknown" in metric_values

        lower, upper = advisory_interval(record, registry["model"])
        intervals.append((lower, upper))
        if not all(math.isfinite(value) and value >= 0 for value in (lower, upper)):
            errors.append(f"{work_id}: advisory interval must be finite and nonnegative")
        if lower > upper:
            errors.append(f"{work_id}: advisory interval bounds are reversed")
        if readiness == 0 and (lower != 0 or upper != 0):
            errors.append(f"{work_id}: zero readiness must force a zero advisory interval")

    if not unknown_metric_seen:
        errors.append("portfolio pilot must preserve at least one explicit unknown metric")
    if not any(lower < upper for lower, upper in intervals):
        errors.append("portfolio pilot must expose at least one nontrivial sensitivity interval")

    active = [record for record in records if record["state"] == "active"]
    if [record["work_package_id"] for record in active] != ["GCL-PORTFOLIO-WP00"]:
        errors.append("only GCL-PORTFOLIO-WP00 may be active in Tranche 1")

    graph = {record["work_package_id"]: set(record["dependencies"]) for record in records}
    for start in graph:
        stack: list[tuple[str, tuple[str, ...]]] = [(start, ())]
        while stack:
            current, path = stack.pop()
            if current in path:
                errors.append("dependency cycle detected: " + " -> ".join((*path, current)))
                break
            stack.extend((dependency, (*path, current)) for dependency in graph.get(current, set()))

    if any(registry["claim_boundaries"].values()):
        errors.append("registry claim-boundary promotion is prohibited")

    expected_view = render(registry)
    try:
        actual_view = view_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"generated view load failed: {exc}")
    else:
        if actual_view != expected_view:
            errors.append("generated portfolio view does not match protected records")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"portfolio validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("portfolio pilot registry is valid: 4 records, advisory intervals only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
