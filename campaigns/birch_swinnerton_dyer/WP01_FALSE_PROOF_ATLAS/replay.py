#!/usr/bin/env python3
"""Deterministic BSD-WP01 semantic-fixture replay."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "01_ATLAS.json"
REQUIRED = {
    "id", "name", "invalid_inference", "missing_obligation",
    "witness", "decision", "remediation", "wp02_interfaces",
}
ALLOWED = {"REJECT", "NARROW"}


def main() -> int:
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0.0"
    assert payload["campaign_id"] == "BSD-001"
    assert payload["protected_claims"] == ["BSD-RANK-Q", "BSD-SHA-Q", "BSD-LEAD-Q"]
    ids: set[str] = set()
    for fixture in payload["fixtures"]:
        missing = REQUIRED - set(fixture)
        assert not missing, f"{fixture.get('id')}: missing {sorted(missing)}"
        assert fixture["id"] not in ids, f"duplicate {fixture['id']}"
        ids.add(fixture["id"])
        assert fixture["decision"] in ALLOWED
        assert fixture["wp02_interfaces"], f"{fixture['id']}: no theorem interface"
        assert all(item.startswith("BSD-T-") for item in fixture["wp02_interfaces"])
        assert fixture["missing_obligation"].strip()
        assert fixture["remediation"].strip()
    assert len(ids) == 18, f"expected 18 fixtures, found {len(ids)}"
    print(f"BSD-WP01 replay passed: {len(ids)} fixtures; all invalid routes rejected or narrowed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
