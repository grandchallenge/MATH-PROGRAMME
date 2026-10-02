#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import analyze_wp02

HERE = Path(__file__).resolve().parent


def main() -> int:
    result = analyze_wp02.build_results()
    retained = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert result == retained

    inverse = result["global_quotient_inverse"]
    assert inverse["free_parameter_ids"] == [
        "F01|F02",
        "F07|F02",
        "F03|F04",
        "F03|F08",
        "F07|F04",
        "F05|F04",
        "F05|F06",
        "F07|F08",
    ]
    assert inverse["baseline_max_abs_inverse_reconstruction_error"] < 1e-12
    assert inverse["baseline_max_abs_extractor_jacobian_identity_error"] < 1e-12
    assert inverse["global_smallest_singular_value_lower_bound"] > 0.42
    assert inverse["global_condition_number_upper_bound"] < 28.0

    screen = result["wide_numerical_screen"]
    assert screen["minimum_rank"] == 8
    assert screen["minimum_smallest_singular_value"] > 0.62
    assert screen["maximum_condition_number"] < 9.24
    assert screen["maximum_abs_extractor_jacobian_identity_error"] < 1e-12
    assert screen["maximum_abs_inverse_reconstruction_error"] < 1e-12

    inverse_design = result["inverse_design"]
    assert inverse_design["feasible_max_abs_parameter_recovery_error"] < 1e-12
    assert inverse_design["feasible_max_abs_response_replay_error"] < 1e-12
    probe = inverse_design["infeasible_probe"]
    assert probe["largest_residual_minor"] == "125"
    assert probe["recovered_parameter_max_abs_change"] < 1e-12
    assert 0.099999999999 < probe["forward_consistency_max_abs_residual"] < 0.100000000001

    assert all(value == "not established" for value in result["claim_boundary"].values())
    print("VGSE-ENG-WP02 tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
