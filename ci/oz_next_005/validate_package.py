#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2] / "campaigns" / "odd_zeta" / "OZ_WP00_SOURCE_NORMALIZATION_EQUIVALENCE" / "review" / "OZ_NEXT_005"


def load(name: str):
    return yaml.safe_load((ROOT / name).read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    sharp = load("SHARP12_RECONCILIATION.yaml")
    comp = load("COMPUTATION_REPLAY_REGISTRY.yaml")
    prior = load("PRIOR_ART_ACQUISITION.yaml")
    lean = load("LEAN_QUARANTINE.yaml")

    require(sharp["headline"]["effective_status"] == "STATED_ONLY", "sharp-12 must fail closed")
    require(sharp["promotion"]["eligible"] is False, "sharp-12 promotion must be false")
    require(len(comp["lanes"]) == 3, "three normalized computation lanes required")
    require(prior["novelty_disposition"]["prohibition"].startswith("NEW_AFTER_AUDIT"), "novelty gate missing")
    require(len(lean["quarantined_targets"]) == 5, "five quarantine targets required")

    for source in prior["sources"]:
        require(re.fullmatch(r"OZ-LIT-EXT-\d{3}", source["id"]) is not None, "invalid external source ID")
        if prior["acquisition_status"] == "CONTENT_ADDRESSED":
            require(isinstance(source["bytes"], int) and source["bytes"] > 0, "missing byte length")
            require(re.fullmatch(r"[0-9a-f]{64}", source["sha256"]) is not None, "missing SHA-256")

    print("OZ-NEXT-005 package is structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
