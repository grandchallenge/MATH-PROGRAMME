#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    subprocess.run([sys.executable, str(HERE / "analyze_wp01.py"), "--check"], check=True)
    data = json.loads((HERE / "RESULTS.json").read_text(encoding="utf-8"))

    assert data["canonical_object"]["almost_perfect_matching_count"] == 31
    assert data["canonical_object"]["supported_projective_minor_count"] == 19
    assert data["canonical_object"]["absent_minor"] == "123"
    assert data["forward_map"]["exact_baseline_matches_target"] is True
    assert data["forward_map"]["raw_jacobian_rank"] == 8
    assert data["forward_map"]["raw_jacobian_nullity"] == 8
    assert data["forward_map"]["gauge_generator_rank"] == 8
    assert data["forward_map"]["max_abs_J_times_gauge"] < 1e-12
    assert data["canonical_gauge"]["jacobian_rank"] == 8
    assert len(data["canonical_gauge"]["sensitivity_by_parameter"]) == 8
    assert data["candidate_invariant_screen"]["falsification_attempt"]["lost_supported_minors"] == ["345"]
    assert data["inverse_design"]["local_kernel_exhausted_at_baseline"] is True
    assert data["inverse_design"]["solve_to_cert_representative_gauge_equivalence"]["max_abs_canonical_weight_discrepancy"] < 1e-12
    assert data["inverse_design"]["explicit_gauge_move"]["max_abs_response_error"] < 1e-12
    assert data["robustness"]["support_count_range"] == [19, 19]
    assert data["robustness"]["canonical_rank_range"] == [8, 8]
    assert data["robustness"]["max_observed_edge_fraction"] <= 0.05 + 1e-12
    print("VGSE-ENG-WP01 tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
