#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import analyze_wp03 as wp03

HERE = Path(__file__).resolve().parent

def main() -> int:
    generated = wp03.build_results()
    retained = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))
    assert generated == retained
    cert = generated["exact_feasibility_certificate"]
    assert cert["matching_count"] == 31
    assert cert["supported_minor_count"] == 19
    assert cert["absent_minor"] == "123"
    assert cert["relation_count"] == 10
    assert cert["residual_jacobian_rank_global"] == 10
    assert cert["completeness"] == "necessary_and_sufficient_on_positive_chart"
    assert all(cert["extractor_identity_checks"])
    assert all(cert["relation_identity_checks"].values())
    assert cert["baseline_jacobian_determinant"] == "23447265625/512"

    checker = generated["deterministic_target_checker"]
    assert checker["feasible_probe"]["status"] == "feasible"
    assert checker["feasible_probe"]["max_abs_parameter_recovery_error"] < 1e-12
    assert checker["feasible_probe"]["max_abs_log_response_residual"] < 1e-12
    assert all(
        probe["status"] == "inconsistent"
        for probe in checker["adversarial_single_dependent_coordinate_probes"].values()
    )
    assert all(
        probe["max_abs_recovered_theta_change"] < 1e-12
        for probe in checker["adversarial_single_dependent_coordinate_probes"].values()
    )
    assert checker["ambiguous_probe"]["status"] == "numerically_ambiguous"

    retract = generated["retraction"]
    assert retract["extractor_preservation_max_abs_error"] < 1e-12
    assert retract["idempotence_max_abs_error"] < 1e-12
    assert retract["nearest_point_claim"] == "not established"

    print("VGSE-ENG-WP03 tests: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
