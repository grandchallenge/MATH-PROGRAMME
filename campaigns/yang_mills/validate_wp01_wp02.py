#!/usr/bin/env python3
"""Cross-validate YM-WP01 fixtures and YM-WP02 theorem interfaces."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "WP01_FALSE_PROOF_ATLAS" / "01_ATLAS.json"
SOURCES = ROOT / "WP02_THEOREM_LEDGER" / "01_SOURCE_REGISTRY.json"
THEOREMS = ROOT / "WP02_THEOREM_LEDGER" / "02_THEOREM_LEDGER.json"
GATE = ROOT / "WP02_THEOREM_LEDGER" / "04_DEPENDENCY_DEBT_GATE.json"

EXPECTED_NONCOMPOSABLE = {
    "YM-T-000", "YM-T-060", "YM-T-090", "YM-T-120", "YM-T-140",
    "YM-T-150", "YM-T-160", "YM-T-170", "YM-T-180", "YM-T-190",
}
UNVERIFIED_SOURCES = {"YM-SRC-017", "YM-SRC-018"}
REQUIRED_GATES = (
    "mechanism_generation", "numerical_experimentation",
    "restricted_target_selection", "novelty_claims",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def duplicate_values(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def validation_errors(atlas: dict[str, Any], sources: dict[str, Any],
                      theorems: dict[str, Any], gate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    source_items = sources.get("sources", [])
    records = theorems.get("records", [])
    fixtures = atlas.get("fixtures", [])
    source_ids = {str(item.get("id", "")) for item in source_items}
    theorem_ids = {str(item.get("id", "")) for item in records}
    fixture_ids = {str(item.get("id", "")) for item in fixtures}

    for duplicate in sorted(duplicate_values([str(item.get("id", "")) for item in source_items])):
        errors.append(f"duplicate source id {duplicate}")
    for duplicate in sorted(duplicate_values([str(item.get("id", "")) for item in records])):
        errors.append(f"duplicate theorem id {duplicate}")
    for duplicate in sorted(duplicate_values([str(item.get("id", "")) for item in fixtures])):
        errors.append(f"duplicate fixture id {duplicate}")

    if len(fixtures) != 20:
        errors.append(f"expected 20 false-proof fixtures, found {len(fixtures)}")
    if "YM-T-000" not in theorem_ids or "YM-T-200" not in theorem_ids:
        errors.append("terminal target and current-status records are required")

    source_required = set(sources.get("required_fields", []))
    for source in source_items:
        source_id = str(source.get("id", "<unknown>"))
        missing = source_required - set(source)
        if missing:
            errors.append(f"{source_id}: incomplete source record; missing {sorted(missing)}")

    required = set(theorems.get("required_fields", []))
    noncomposable_ids: set[str] = set()
    record_by_id = {str(record.get("id", "")): record for record in records}
    for record in records:
        record_id = str(record.get("id", "<unknown>"))
        missing = required - set(record)
        if missing:
            errors.append(f"{record_id}: incomplete record; missing {sorted(missing)}")
        unknown_sources = set(map(str, record.get("source_ids", []))) - source_ids
        if unknown_sources:
            errors.append(f"{record_id}: unknown sources {sorted(unknown_sources)}")
        state = str(record.get("composition_state", ""))
        if state.startswith("NONCOMPOSABLE") or state.startswith("OPEN_NOT_COMPOSABLE"):
            noncomposable_ids.add(record_id)
            if not record.get("residual_hypotheses"):
                errors.append(f"{record_id}: noncomposable interface lacks residual hypotheses")
            locator = str(record.get("source_locator", "")).lower()
            markers = ("required", "pending", "audit", "official", "problem statement", "theorem", "no complete")
            if not any(marker in locator for marker in markers):
                errors.append(f"{record_id}: noncomposable source locator must state audit, pending, required, or official scope")

    if noncomposable_ids != EXPECTED_NONCOMPOSABLE:
        errors.append("noncomposable interface set drifted: "
                      f"expected {sorted(EXPECTED_NONCOMPOSABLE)}, found {sorted(noncomposable_ids)}")

    for source_id in UNVERIFIED_SOURCES:
        source = next((item for item in source_items if item.get("id") == source_id), None)
        if source is None or source.get("audit_state") != "UNVERIFIED_COMPLETE_SOLUTION_CLAIM":
            errors.append(f"{source_id}: complete-solution claim must remain unverified")

    for record_id in ("YM-T-170", "YM-T-180"):
        record = record_by_id.get(record_id, {})
        if record.get("status") != "UNVERIFIED_COMPLETE_SOLUTION_CLAIM":
            errors.append(f"{record_id}: must remain an unverified complete-solution claim")
        if not str(record.get("composition_state", "")).startswith("NONCOMPOSABLE"):
            errors.append(f"{record_id}: unverified claim must remain noncomposable")

    current = record_by_id.get("YM-T-200", {})
    if current.get("status") != "INSTITUTIONAL_STATUS":
        errors.append("YM-T-200 must remain an institutional-status record")
    current_conclusion = str(current.get("conclusion", "")).lower()
    if not any(marker in current_conclusion for marker in ("no accepted solution", "remains listed as unsolved")):
        errors.append("YM-T-200 must preserve the current no-accepted-solution status")

    for fixture in fixtures:
        fixture_id = str(fixture.get("id", "<unknown>"))
        unknown = set(map(str, fixture.get("wp02_interfaces", []))) - theorem_ids
        if unknown:
            errors.append(f"{fixture_id}: unknown theorem interfaces {sorted(unknown)}")

    debt_nodes = {str(item.get("blocked_node", "")) for item in gate.get("debts", [])}
    for required_node in ("YM-T-000", "YM-T-120", "YM-T-140", "YM-T-150", "YM-T-160", "YM-T-170", "YM-T-180", "YM-T-190"):
        if required_node not in debt_nodes:
            errors.append(f"dependency debt does not cover {required_node}")

    for edge in gate.get("edges", []):
        source = edge.get("from")
        target = edge.get("to")
        if source not in theorem_ids:
            errors.append(f"dependency edge has unknown theorem source {source}")
        if target not in theorem_ids | fixture_ids:
            errors.append(f"dependency edge has unknown target {target}")

    gate_state = gate.get("gate", {})
    for field in REQUIRED_GATES:
        if gate_state.get(field) != "CLOSED":
            errors.append(f"YM-WP02 gate {field} must remain CLOSED")
    atlas_gates = atlas.get("gate_state", {})
    for field in REQUIRED_GATES:
        if atlas_gates.get(field) != gate_state.get(field):
            errors.append(f"WP01/WP02 gate mismatch for {field}")
    return errors


def main() -> int:
    atlas, sources, theorems, gate = map(load, (ATLAS, SOURCES, THEOREMS, GATE))
    errors = validation_errors(atlas, sources, theorems, gate)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"YM-WP01/WP02 validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"YM-WP01/WP02 validation passed: {len(atlas['fixtures'])} fixtures, "
          f"{len(theorems['records'])} theorem interfaces, {len(sources['sources'])} sources; "
          "mechanism and numerical gates closed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
