#!/usr/bin/env python3
"""Cross-validate PNP-WP01 fixtures and PNP-WP02 theorem interfaces."""
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
EXPECTED_FIXTURES, EXPECTED_SOURCES, EXPECTED_RECORDS = 46, 36, 31
EXPECTED_TERMINAL = {"PNP-T-130"}
EXPECTED_CURRENT_FRONTIER = {"PNP-T-260", "PNP-T-270", "PNP-T-280", "PNP-T-310"}
LOCKED_GATE_FIELDS = (
    "mechanism_generation", "restricted_target_selection",
    "large_scale_experiments", "novelty_claims",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_indexed(index_path: Path, file_key: str, item_key: str) -> dict[str, Any]:
    index = load(index_path)
    items: list[dict[str, Any]] = []
    for relative in index.get(file_key, []):
        items.extend(load(index_path.parent / relative).get(item_key, []))
    return {**index, item_key: items}


def load_all() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        load_indexed(ATLAS, "fixture_files", "fixtures"),
        load(SOURCES),
        load_indexed(THEOREMS, "record_files", "records"),
        load(GATE),
    )


def duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    repeated: set[str] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return repeated


def validation_errors(
    atlas: dict[str, Any], sources: dict[str, Any],
    theorems: dict[str, Any], gate: dict[str, Any],
) -> list[str]:
    errors: list[str] = []
    fixtures, source_items, records = (
        atlas.get("fixtures", []), sources.get("sources", []), theorems.get("records", [])
    )
    for label, actual, expected in (
        ("fixtures", len(fixtures), EXPECTED_FIXTURES),
        ("sources", len(source_items), EXPECTED_SOURCES),
        ("theorem interfaces", len(records), EXPECTED_RECORDS),
    ):
        if actual != expected:
            errors.append(f"expected {expected} {label}, found {actual}")
    if atlas.get("fixture_count") != EXPECTED_FIXTURES:
        errors.append("atlas index fixture_count drifted")
    if theorems.get("record_count") != EXPECTED_RECORDS:
        errors.append("theorem index record_count drifted")

    fixture_ids_list = [str(item.get("id", "")) for item in fixtures]
    source_ids_list = [str(item.get("id", "")) for item in source_items]
    record_ids_list = [str(item.get("id", "")) for item in records]
    for label, values in (("fixture", fixture_ids_list), ("source", source_ids_list), ("theorem", record_ids_list)):
        for value in sorted(duplicates(values)):
            errors.append(f"duplicate {label} id {value}")
    fixture_ids, source_ids, record_ids = set(fixture_ids_list), set(source_ids_list), set(record_ids_list)

    fixture_required = set(atlas.get("fixture_contract", {}).get("required", []))
    allowed_decisions = set(atlas.get("fixture_contract", {}).get("allowed_decisions", []))
    for fixture in fixtures:
        fixture_id = str(fixture.get("id", "<unknown>"))
        missing = fixture_required - set(fixture)
        if missing:
            errors.append(f"{fixture_id}: missing fields {sorted(missing)}")
        if fixture.get("decision") not in allowed_decisions:
            errors.append(f"{fixture_id}: invalid decision")
        unknown = set(fixture.get("wp02_interfaces", [])) - record_ids
        if unknown:
            errors.append(f"{fixture_id}: unknown theorem interfaces {sorted(unknown)}")
        if not str(fixture.get("missing_obligation", "")).strip():
            errors.append(f"{fixture_id}: missing obligation is empty")
        if not str(fixture.get("remediation", "")).strip():
            errors.append(f"{fixture_id}: remediation is empty")

    source_required = {"id", "citation", "year", "kind", "locator", "audit_state", "url"}
    audit_year = int(str(sources.get("audit_date", "0"))[:4] or 0)
    current_source_ids: set[str] = set()
    for source in source_items:
        source_id = str(source.get("id", "<unknown>"))
        missing = source_required - set(source)
        if missing:
            errors.append(f"{source_id}: missing source fields {sorted(missing)}")
        year = int(source.get("year", 0))
        if year > audit_year:
            errors.append(f"{source_id}: source year {year} exceeds audit year {audit_year}")
        if year >= 2025:
            current_source_ids.add(source_id)
            if "CURRENT_FRONTIER" not in str(source.get("audit_state", "")):
                errors.append(f"{source_id}: current source lacks CURRENT_FRONTIER audit state")

    theorem_required = set(theorems.get("required_fields", []))
    terminal_ids: set[str] = set()
    frontier_ids: set[str] = set()
    for record in records:
        record_id = str(record.get("id", "<unknown>"))
        missing = theorem_required - set(record)
        if missing:
            errors.append(f"{record_id}: missing theorem fields {sorted(missing)}")
        unknown_sources = set(record.get("source_ids", [])) - source_ids
        if unknown_sources:
            errors.append(f"{record_id}: unknown sources {sorted(unknown_sources)}")
        unknown_fixtures = set(record.get("wp01_fixtures", [])) - fixture_ids
        if unknown_fixtures:
            errors.append(f"{record_id}: unknown fixtures {sorted(unknown_fixtures)}")
        if record.get("composition_state") == "OPEN_TERMINAL":
            terminal_ids.add(record_id)
            if record.get("kind") != "OPEN_TARGET":
                errors.append(f"{record_id}: terminal record must be OPEN_TARGET")
        if record.get("kind") == "CURRENT_FRONTIER":
            frontier_ids.add(record_id)
            if not set(record.get("source_ids", [])) & current_source_ids and record_id != "PNP-T-310":
                errors.append(f"{record_id}: current frontier lacks a current source")
            residual = " ".join(map(str, record.get("residual_hypotheses", []))).lower()
            if record_id in {"PNP-T-260", "PNP-T-270", "PNP-T-280"} and not any(
                marker in residual for marker in ("preprint", "publication", "source")
            ):
                errors.append(f"{record_id}: current frontier lacks source-maturity debt")
        if record.get("kind") == "BARRIER" and record.get("composition_state") not in {
            "BARRIER_ONLY", "CURRENT_FRONTIER_BARRIER"
        }:
            errors.append(f"{record_id}: barrier record has terminal or composable state")
    if terminal_ids != EXPECTED_TERMINAL:
        errors.append(f"terminal set drifted: expected {sorted(EXPECTED_TERMINAL)}, found {sorted(terminal_ids)}")
    if frontier_ids != EXPECTED_CURRENT_FRONTIER:
        errors.append(
            f"current-frontier set drifted: expected {sorted(EXPECTED_CURRENT_FRONTIER)}, found {sorted(frontier_ids)}"
        )

    for edge in gate.get("edges", []):
        source, target = str(edge.get("from", "")), str(edge.get("to", ""))
        if source not in record_ids:
            errors.append(f"dependency edge has unknown source {source}")
        if target not in record_ids and target not in fixture_ids:
            errors.append(f"dependency edge has unknown target {target}")
    debt_text = " ".join(str(item.get("description", "")) for item in gate.get("debts", [])).lower()
    for marker in ("unrestricted lower-bound", "polynomial-time sat decider", "current-frontier"):
        if marker not in debt_text:
            errors.append(f"dependency debt lacks marker {marker}")
    for field in LOCKED_GATE_FIELDS:
        if gate.get("gate", {}).get(field) != "CLOSED":
            errors.append(f"PNP gate {field} must remain CLOSED")
    return errors


def main() -> int:
    atlas, sources, theorems, gate = load_all()
    errors = validation_errors(atlas, sources, theorems, gate)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"PNP WP01/WP02 validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        f"PNP WP01/WP02 validation passed: {len(atlas['fixtures'])} fixtures, "
        f"{len(theorems['records'])} theorem interfaces, {len(sources['sources'])} sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
