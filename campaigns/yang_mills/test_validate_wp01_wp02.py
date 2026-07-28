#!/usr/bin/env python3
"""Adversarial mutations for the YM-WP01/WP02 validator."""

from __future__ import annotations

import copy

from validate_wp01_wp02 import ATLAS, GATE, SOURCES, THEOREMS, load, validation_errors


def errors_for(atlas, sources, theorems, gate):
    return validation_errors(atlas, sources, theorems, gate)


def main() -> int:
    atlas, sources, theorems, gate = map(load, (ATLAS, SOURCES, THEOREMS, GATE))
    assert not errors_for(atlas, sources, theorems, gate)

    unknown_source = copy.deepcopy(theorems)
    unknown_source["records"][0]["source_ids"].append("YM-SRC-MISSING")
    assert any("unknown sources" in error for error in errors_for(atlas, sources, unknown_source, gate))

    unknown_interface = copy.deepcopy(atlas)
    unknown_interface["fixtures"][0]["wp02_interfaces"].append("YM-T-MISSING")
    assert any("unknown theorem interfaces" in error for error in errors_for(unknown_interface, sources, theorems, gate))

    opened_gate = copy.deepcopy(gate)
    opened_gate["gate"]["mechanism_generation"] = "OPEN"
    assert any("mechanism_generation must remain CLOSED" in error for error in errors_for(atlas, sources, theorems, opened_gate))

    opened_numerics = copy.deepcopy(gate)
    opened_numerics["gate"]["numerical_experimentation"] = "OPEN"
    assert any("numerical_experimentation must remain CLOSED" in error for error in errors_for(atlas, sources, theorems, opened_numerics))

    missing_debt = copy.deepcopy(theorems)
    record = next(item for item in missing_debt["records"] if item["id"] == "YM-T-150")
    record["residual_hypotheses"] = []
    assert any("YM-T-150: noncomposable interface lacks residual hypotheses" in error for error in errors_for(atlas, sources, missing_debt, gate))

    promoted_preprint = copy.deepcopy(theorems)
    record = next(item for item in promoted_preprint["records"] if item["id"] == "YM-T-170")
    record["status"] = "THEOREM"
    record["composition_state"] = "COMPOSABLE_STANDARD"
    assert any("YM-T-170" in error and ("unverified" in error or "noncomposable" in error) for error in errors_for(atlas, sources, promoted_preprint, gate))

    solved_status = copy.deepcopy(theorems)
    record = next(item for item in solved_status["records"] if item["id"] == "YM-T-200")
    record["conclusion"] = "An accepted solution exists."
    assert any("no-accepted-solution" in error for error in errors_for(atlas, sources, solved_status, gate))

    missing_source_audit = copy.deepcopy(sources)
    source = next(item for item in missing_source_audit["sources"] if item["id"] == "YM-SRC-018")
    source["audit_state"] = "AUDITED"
    assert any("YM-SRC-018" in error and "unverified" in error for error in errors_for(atlas, missing_source_audit, theorems, gate))

    print("YM-WP01/WP02 adversarial validator mutations rejected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
