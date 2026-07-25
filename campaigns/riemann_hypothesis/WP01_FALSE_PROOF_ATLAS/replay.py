#!/usr/bin/env python3
"""Validate the RH-WP01 false-proof atlas."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATLAS = ROOT / "01_ATLAS.json"


def main() -> int:
    data = json.loads(ATLAS.read_text(encoding="utf-8"))
    fixtures = data["fixtures"]
    required = set(data["fixture_contract"]["required"])
    allowed = set(data["fixture_contract"]["allowed_decisions"])
    ids = [item["id"] for item in fixtures]
    assert len(fixtures) == 20, f"expected 20 fixtures, found {len(fixtures)}"
    assert len(ids) == len(set(ids)), "duplicate fixture id"
    assert ids == [f"RH-F{i:03d}" for i in range(1, 21)], "fixture sequence drift"
    for item in fixtures:
        assert required <= set(item), f"{item.get('id')}: incomplete fixture"
        assert item["decision"] in allowed, f"{item['id']}: invalid decision"
        assert item["wp02_interfaces"], f"{item['id']}: no WP02 interface"
        for field in ("invalid_inference", "missing_obligation", "witness", "remediation", "does_not_rule_out"):
            assert len(item[field].strip()) >= 20, f"{item['id']}: weak {field}"
    print(f"RH-WP01 replay passed: {len(fixtures)} fixtures fail closed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
