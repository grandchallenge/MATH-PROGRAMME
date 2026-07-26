#!/usr/bin/env python3
"""Adversarial rejection tests for BSD-WP01/WP02 cross-validation."""
from __future__ import annotations

import copy

from validate_wp01_wp02 import ATLAS, GATE, SOURCES, THEOREMS, load, validation_errors


def main() -> int:
    atlas, sources, theorems, gate = map(load, (ATLAS, SOURCES, THEOREMS, GATE))
    assert not validation_errors(atlas, sources, theorems, gate)

    missing_interface = copy.deepcopy(theorems)
    missing_interface["records"] = [
        record for record in missing_interface["records"] if record["id"] != "BSD-T-140"
    ]
    assert any(
        "noncomposable interface set drifted" in error
        for error in validation_errors(atlas, sources, missing_interface, gate)
    )

    composable_kato = copy.deepcopy(theorems)
    next(record for record in composable_kato["records"] if record["id"] == "BSD-T-140")[
        "composition_state"
    ] = "COMPOSABLE"
    assert any(
        "noncomposable interface set drifted" in error
        for error in validation_errors(atlas, sources, composable_kato, gate)
    )

    missing_residual = copy.deepcopy(theorems)
    next(record for record in missing_residual["records"] if record["id"] == "BSD-T-140")[
        "residual_hypotheses"
    ] = []
    assert any(
        "lacks residual hypotheses" in error
        for error in validation_errors(atlas, sources, missing_residual, gate)
    )

    missing_debt = copy.deepcopy(gate)
    missing_debt["debts"] = [
        debt for debt in missing_debt["debts"] if debt["id"] != "BSD-WP02-D002"
    ]
    assert any(
        "dependency debt does not preserve" in error
        for error in validation_errors(atlas, sources, theorems, missing_debt)
    )

    opened_gate = copy.deepcopy(gate)
    opened_gate["gate"]["mechanism_generation"] = "OPEN"
    assert any(
        "mechanism_generation must remain CLOSED" in error
        for error in validation_errors(atlas, sources, theorems, opened_gate)
    )

    print("BSD WP01/WP02 validator rejection tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
