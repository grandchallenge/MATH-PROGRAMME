#!/usr/bin/env python3
"""Adversarial mutation tests for the PNP-WP01/WP02 package."""
from __future__ import annotations

import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from validate_wp01_wp02 import load_all, validation_errors  # noqa: E402


def has(errors: list[str], marker: str) -> bool:
    return any(marker in error for error in errors)


def main() -> int:
    atlas, sources, theorems, gate = load_all()
    assert not validation_errors(atlas, sources, theorems, gate)

    mutated = copy.deepcopy(atlas)
    mutated["fixtures"][1]["id"] = mutated["fixtures"][0]["id"]
    assert has(validation_errors(mutated, sources, theorems, gate), "duplicate fixture id")

    mutated = copy.deepcopy(atlas)
    mutated["fixtures"][0]["wp02_interfaces"] = ["PNP-T-MISSING"]
    assert has(validation_errors(mutated, sources, theorems, gate), "unknown theorem interfaces")

    mutated = copy.deepcopy(theorems)
    mutated["records"][0]["source_ids"] = ["PNP-SRC-MISSING"]
    assert has(validation_errors(atlas, sources, mutated, gate), "unknown sources")

    mutated = copy.deepcopy(theorems)
    record = next(item for item in mutated["records"] if item["id"] == "PNP-T-260")
    record["composition_state"], record["kind"] = "OPEN_TERMINAL", "OPEN_TARGET"
    assert has(validation_errors(atlas, sources, mutated, gate), "terminal set drifted")

    mutated = copy.deepcopy(gate)
    mutated["gate"]["mechanism_generation"] = "OPEN"
    assert has(validation_errors(atlas, sources, theorems, mutated), "mechanism_generation must remain CLOSED")

    mutated = copy.deepcopy(theorems)
    record = next(item for item in mutated["records"] if item["id"] == "PNP-T-270")
    record["residual_hypotheses"] = ["All theorem hypotheses remain."]
    assert has(validation_errors(atlas, sources, mutated, gate), "source-maturity debt")

    mutated = copy.deepcopy(theorems)
    record = next(item for item in mutated["records"] if item["id"] == "PNP-T-170")
    record["composition_state"] = "COMPOSABLE_TERMINAL"
    assert has(validation_errors(atlas, sources, mutated, gate), "barrier record has terminal or composable state")

    mutated = copy.deepcopy(atlas)
    mutated["fixtures"][0]["missing_obligation"] = ""
    assert has(validation_errors(mutated, sources, theorems, gate), "missing obligation is empty")

    print("PNP WP01/WP02 adversarial mutation tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
