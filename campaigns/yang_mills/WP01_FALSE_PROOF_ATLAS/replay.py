#!/usr/bin/env python3
"""Replay the YM-WP01 false-proof atlas contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "01_ATLAS.json"
THEOREMS = ROOT.parent / "WP02_THEOREM_LEDGER" / "02_THEOREM_LEDGER.json"

EXPECTED_IDS = [f"YM-F{i:03d}" for i in range(1, 21)]
REQUIRED_GATES = (
    "mechanism_generation",
    "numerical_experimentation",
    "restricted_target_selection",
    "novelty_claims",
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def replay_errors(atlas: dict[str, Any], theorems: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    fixtures = atlas.get("fixtures", [])
    contract = atlas.get("fixture_contract", {})
    required = set(contract.get("required", []))
    allowed = set(contract.get("allowed_decisions", []))
    theorem_ids = {str(record.get("id", "")) for record in theorems.get("records", [])}
    ids = [str(fixture.get("id", "")) for fixture in fixtures]

    if atlas.get("protected_claims") != ["YM-T-000"]:
        errors.append("protected_claims must be exactly ['YM-T-000']")
    if len(fixtures) != 20:
        errors.append(f"expected 20 fixtures, found {len(fixtures)}")
    if ids != EXPECTED_IDS:
        errors.append("fixture IDs must be the ordered sequence YM-F001 through YM-F020")
    if len(set(ids)) != len(ids):
        errors.append("fixture IDs are not unique")
    if allowed != {"REJECT", "NARROW"}:
        errors.append(f"allowed decisions drifted: {sorted(allowed)}")

    for fixture in fixtures:
        fixture_id = str(fixture.get("id", "<unknown>"))
        missing = required - set(fixture)
        if missing:
            errors.append(f"{fixture_id}: missing fields {sorted(missing)}")
        for field in required - {"wp02_interfaces"}:
            value = fixture.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{fixture_id}: {field} must be nonempty text")
        if fixture.get("decision") not in allowed:
            errors.append(f"{fixture_id}: invalid decision {fixture.get('decision')!r}")
        interfaces = fixture.get("wp02_interfaces")
        if not isinstance(interfaces, list) or not interfaces:
            errors.append(f"{fixture_id}: wp02_interfaces must be a nonempty list")
        else:
            unknown = set(map(str, interfaces)) - theorem_ids
            if unknown:
                errors.append(f"{fixture_id}: unknown WP02 interfaces {sorted(unknown)}")

    gates = atlas.get("gate_state", {})
    for gate in REQUIRED_GATES:
        if gates.get(gate) != "CLOSED":
            errors.append(f"YM-WP01 gate {gate} must remain CLOSED")

    return errors


def main() -> int:
    errors = replay_errors(load(ATLAS), load(THEOREMS))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"YM-WP01 replay failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("YM-WP01 replay passed: 20 fixtures, resolved WP02 links, downstream gates closed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
