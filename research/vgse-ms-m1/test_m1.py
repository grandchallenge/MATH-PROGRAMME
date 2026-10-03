#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("vgse_ms_m1_analyzer", HERE / "analyze_m1.py")
assert SPEC and SPEC.loader
m1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m1)


def main() -> int:
    data = m1.build()
    generated = m1.artifacts(data)

    audit = generated["MODEL_AUDIT.json"]
    assert audit["graph"]["panel_count"] == 8
    assert audit["graph"]["hinge_count"] == 10
    assert audit["graph"]["matrix_rows"] == 50
    assert audit["graph"]["matrix_columns_after_fixed_panel"] == 42
    assert audit["graph"]["panel_adjacency_connected"]
    assert audit["max_hinge_rate_projector_difference_across_fixed_panel_choices"] < 1e-10

    atlas = generated["MOBILITY_ATLAS.json"]["aggregate"]
    assert atlas["attempted_m0_samples"] == 41
    assert atlas["evaluated_valid_m0_realizations"] == 40
    assert atlas["excluded_without_m0_geometry"] == 1
    assert atlas["observed_ranks"] == [38]
    assert atlas["observed_mobilities"] == [4]
    assert atlas["observed_constraint_dependency_dimensions"] == [12]
    assert atlas["observed_hinge_rate_subspace_ranks"] == [4]
    assert atlas["minimum_smallest_nonzero_singular_value"] > 1e-3
    assert atlas["maximum_largest_null_singular_value"] < 1e-10

    branches = generated["BRANCH_COMPARISON.json"]
    assert len(branches["branches"]) == 5
    assert branches["same_mobility_dimension"]
    assert not branches["same_hinge_rate_subspace"]
    assert branches["minimum_pairwise_projector_difference"] > 1e-3

    results = generated["RESULTS.json"]
    assert results["disposition"] == "KINEMATIC_SEMANTICS_BRANCH_DEPENDENT"
    assert not any(results["claim_boundary"].values())

    m1.validate_retained(generated)
    print("VGSE-MS-M1 kinematic regression tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
