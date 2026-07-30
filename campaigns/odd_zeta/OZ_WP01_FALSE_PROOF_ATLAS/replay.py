#!/usr/bin/env python3
"""Replay every OZ-WP01 false-proof atlas case."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

from engine import evaluate

ROOT = Path(__file__).resolve().parents[3]
ATLAS_PATH = Path(__file__).with_name("ATLAS.yaml")
EXPECTED_FAMILIES = {
    "APERY_BROW",
    "THEOREM_LB",
    "BZ_COMPACT",
    "SHARP12",
    "NOVELTY",
    "IRRATIONALITY",
    "ZETA7_OPERATOR",
    "ZETA_DISJUNCTION",
}


def load_atlas(path: Path = ATLAS_PATH) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("atlas root must be a mapping")
    return data


def replay(path: Path = ATLAS_PATH) -> list[str]:
    atlas = load_atlas(path)
    errors: list[str] = []
    if atlas.get("atlas_id") != "OZ-WP01":
        errors.append("wrong atlas_id")
    cases = atlas.get("cases")
    if not isinstance(cases, list):
        return errors + ["cases must be a list"]

    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(set(ids)):
        errors.append("duplicate case IDs")

    families = {case.get("family") for case in cases if isinstance(case, dict)}
    missing_families = EXPECTED_FAMILIES - families
    if missing_families:
        errors.append(f"missing controlled families: {sorted(missing_families)}")

    required_codes = set(atlas.get("required_reason_codes", []))
    observed_codes: set[str] = set()
    accepted = 0
    rejected = 0

    for case in cases:
        case_id = case.get("id", "<missing>")
        expected = case.get("expected", {})
        reasons = evaluate(case.get("packet", {}))
        observed_codes.update(reasons)
        verdict = "REJECT" if reasons else "ACCEPT"
        if verdict == "ACCEPT":
            accepted += 1
        else:
            rejected += 1
        if verdict != expected.get("verdict"):
            errors.append(f"{case_id}: verdict {verdict}, expected {expected.get('verdict')}")
        expected_reasons = sorted(expected.get("reasons", []))
        if reasons != expected_reasons:
            errors.append(f"{case_id}: reasons {reasons}, expected {expected_reasons}")

    if observed_codes != required_codes:
        errors.append(
            f"reason-code coverage mismatch: observed={sorted(observed_codes)} required={sorted(required_codes)}"
        )
    if accepted < 5:
        errors.append("at least five positive controls are required")
    if rejected < 12:
        errors.append("at least twelve false-proof fixtures are required")

    print(f"OZ-WP01 replay: {accepted} accepted controls, {rejected} rejected false-proof packets")
    for case in cases:
        reasons = evaluate(case.get("packet", {}))
        print(f"{case['id']} {'REJECT' if reasons else 'ACCEPT'} {','.join(reasons) if reasons else '-'}")
    return errors


def main() -> int:
    errors = replay()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"OZ-WP01 replay failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("OZ-WP01 executable false-proof atlas passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
