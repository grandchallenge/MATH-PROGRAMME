#!/usr/bin/env python3
"""Deterministic PNP-WP01 semantic-fixture replay."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
INDEX = ROOT / "01_ATLAS.json"
REQUIRED = {
    "id", "name", "category", "invalid_inference", "missing_obligation",
    "witness", "decision", "remediation", "wp02_interfaces",
}
ALLOWED = {"REJECT", "NARROW"}
EXPECTED_COUNT = 46


def load_payload() -> dict[str, Any]:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    fixtures: list[dict[str, Any]] = []
    for relative in index.get("fixture_files", []):
        part = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        fixtures.extend(part.get("fixtures", []))
    return {**index, "fixtures": fixtures}


def replay_errors(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if payload.get("campaign_id") != "PNP-001":
        errors.append("campaign_id must be PNP-001")
    fixtures = payload.get("fixtures", [])
    if payload.get("fixture_count") != EXPECTED_COUNT or len(fixtures) != EXPECTED_COUNT:
        errors.append(f"expected {EXPECTED_COUNT} fixtures, found {len(fixtures)}")
    seen: set[str] = set()
    for fixture in fixtures:
        fixture_id = str(fixture.get("id", "<unknown>"))
        missing = REQUIRED - set(fixture)
        if missing:
            errors.append(f"{fixture_id}: missing {sorted(missing)}")
        if fixture_id in seen:
            errors.append(f"duplicate fixture id {fixture_id}")
        seen.add(fixture_id)
        if not fixture_id.startswith("PNP-FP-"):
            errors.append(f"{fixture_id}: invalid fixture identifier")
        if fixture.get("decision") not in ALLOWED:
            errors.append(f"{fixture_id}: invalid decision {fixture.get('decision')!r}")
        for field in ("invalid_inference", "missing_obligation", "witness", "remediation"):
            if not str(fixture.get(field, "")).strip():
                errors.append(f"{fixture_id}: empty {field}")
        interfaces = fixture.get("wp02_interfaces", [])
        if not interfaces:
            errors.append(f"{fixture_id}: no WP02 interface")
        if any(not str(item).startswith("PNP-T-") for item in interfaces):
            errors.append(f"{fixture_id}: malformed WP02 interface")
    return errors


def main() -> int:
    payload = load_payload()
    errors = replay_errors(payload)
    if errors:
        for error in errors:
            print(error)
        print(f"PNP-WP01 replay failed with {len(errors)} error(s)")
        return 1
    print(
        f"PNP-WP01 replay passed: {len(payload['fixtures'])} fixtures; "
        "all invalid routes are explicitly rejected or narrowed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
