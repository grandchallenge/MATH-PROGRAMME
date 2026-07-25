#!/usr/bin/env python3
"""Cross-validate RH-WP01 fixtures and RH-WP02 theorem interfaces."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "WP01_FALSE_PROOF_ATLAS" / "01_ATLAS.json"
SOURCES = ROOT / "WP02_THEOREM_LEDGER" / "01_SOURCE_REGISTRY.json"
THEOREMS = ROOT / "WP02_THEOREM_LEDGER" / "02_THEOREM_LEDGER.json"
GATE = ROOT / "WP02_THEOREM_LEDGER" / "04_DEPENDENCY_DEBT_GATE.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    atlas, sources, theorems, gate = map(load, (ATLAS, SOURCES, THEOREMS, GATE))
    source_ids = {item["id"] for item in sources["sources"]}
    records = theorems["records"]
    theorem_ids = {item["id"] for item in records}
    fixture_ids = {item["id"] for item in atlas["fixtures"]}

    assert len(source_ids) == len(sources["sources"]), "duplicate source id"
    assert len(theorem_ids) == len(records), "duplicate theorem id"
    assert len(fixture_ids) == 20, "fixture count drift"
    assert "RH-T-000" in theorem_ids, "canonical target missing"

    required = set(theorems["required_fields"])
    for record in records:
        assert required <= set(record), f"{record['id']}: incomplete record"
        assert set(record["source_ids"]) <= source_ids, f"{record['id']}: unknown source"
        if record["composition_state"].startswith("NONCOMPOSABLE"):
            assert any(debt["blocked"] == record["id"] for debt in gate["proof_debt"]), (
                f"{record['id']}: noncomposable without debt"
            )

    for fixture in atlas["fixtures"]:
        assert set(fixture["wp02_interfaces"]) <= theorem_ids, f"{fixture['id']}: unknown interface"

    for edge in gate["edges"]:
        assert edge["from"] in theorem_ids
        assert edge["to"] in theorem_ids | fixture_ids

    assert gate["gate"]["mechanism_generation"] == "CLOSED"
    assert gate["gate"]["restricted_target_selection"] == "CLOSED"
    assert gate["gate"]["claimed_proof_promotion"] == "CLOSED"

    print(
        "RH WP01/WP02 validation passed: "
        f"{len(fixture_ids)} fixtures, {len(theorem_ids)} theorem interfaces, "
        f"{len(source_ids)} sources, {len(gate['proof_debt'])} debt records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
