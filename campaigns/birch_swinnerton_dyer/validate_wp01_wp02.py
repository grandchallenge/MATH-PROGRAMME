#!/usr/bin/env python3
"""Cross-validate BSD-WP01 fixtures and BSD-WP02 theorem interfaces."""
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


def validation_errors(
    atlas: dict[str, Any],
    sources: dict[str, Any],
    theorems: dict[str, Any],
    gate: dict[str, Any],
) -> list[str]:
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
    if len(fixture_ids) != 18:
        errors.append(f"expected 18 false-proof fixtures, found {len(fixture_ids)}")

    required = set(theorems.get("required_fields", []))
    noncomposable_ids: set[str] = set()
    for record in records:
        record_id = str(record.get("id", "<unknown>"))
        missing = required - set(record)
        if missing:
            errors.append(f"{record_id}: incomplete record; missing {sorted(missing)}")
        unknown_sources = set(record.get("source_ids", [])) - source_ids
        if unknown_sources:
            errors.append(f"{record_id}: unknown sources {sorted(unknown_sources)}")
        if str(record.get("composition_state", "")).startswith("NONCOMPOSABLE"):
            noncomposable_ids.add(record_id)
            if not record.get("hypotheses"):
                errors.append(f"{record_id}: noncomposable interface lacks hypotheses")
            if not record.get("residual_hypotheses"):
                errors.append(f"{record_id}: noncomposable interface lacks residual hypotheses")
            locator = str(record.get("source_locator", "")).lower()
            if not any(marker in locator for marker in ("required", "pending", "per-use")):
                errors.append(
                    f"{record_id}: noncomposable source locator must state required, pending, or per-use extraction"
                )

    expected_noncomposable = {"BSD-T-140", "BSD-T-150"}
    if noncomposable_ids != expected_noncomposable:
        errors.append(
            "noncomposable interface set drifted: "
            f"expected {sorted(expected_noncomposable)}, found {sorted(noncomposable_ids)}"
        )

    debt_text = " ".join(str(item.get("description", "")) for item in gate.get("debts", [])).lower()
    for marker in ("kato", "zeta-element", "theorem-level"):
        if marker not in debt_text:
            errors.append(f"dependency debt does not preserve noncomposable-interface marker {marker}")

    for fixture in fixtures:
        fixture_id = str(fixture.get("id", "<unknown>"))
        unknown_interfaces = set(fixture.get("wp02_interfaces", [])) - theorem_ids
        if unknown_interfaces:
            errors.append(f"{fixture_id}: unknown theorem interfaces {sorted(unknown_interfaces)}")

    for edge in gate.get("edges", []):
        source = edge.get("from")
        target = edge.get("to")
        if source not in theorem_ids:
            errors.append(f"dependency edge has unknown theorem source {source}")
        if target not in theorem_ids | fixture_ids:
            errors.append(f"dependency edge has unknown target {target}")

    gate_state = gate.get("gate", {})
    for field in ("mechanism_generation", "restricted_target_selection", "novelty_claims"):
        if gate_state.get(field) != "CLOSED":
            errors.append(f"BSD WP02 gate {field} must remain CLOSED")
    return errors


def main() -> int:
    atlas, sources, theorems, gate = map(load, (ATLAS, SOURCES, THEOREMS, GATE))
    errors = validation_errors(atlas, sources, theorems, gate)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"BSD WP01/WP02 validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        f"BSD WP01/WP02 validation passed: {len(atlas['fixtures'])} fixtures, "
        f"{len(theorems['records'])} theorem interfaces, {len(sources['sources'])} sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
