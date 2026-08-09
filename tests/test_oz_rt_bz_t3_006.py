from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_006" / "validate.py"
spec = importlib.util.spec_from_file_location("oz_t3_006_validate", PATH)
assert spec is not None and spec.loader is not None
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


def has(errors, text):
    return any(text in e for e in errors)


def test_baseline_is_valid():
    assert v.errors() == []


def test_rejects_dropped_weight_five_monomial():
    s = copy.deepcopy(v.S)
    s["basis"]["monomial_count"] = 197
    assert has(v.errors(result=s), "basis cardinality")


def test_rejects_nested_orientation_collapse():
    s = copy.deepcopy(v.S)
    s["basis"]["one_nested_atom_count"] = 20
    s["mirror_status"] = "ONE_ORIENTATION_ONLY"
    e = v.errors(result=s)
    assert has(e, "basis cardinality") and has(e, "mirror-equivalence")


def test_rejects_certificate_denominator_drift():
    s = copy.deepcopy(v.S)
    s["certificate_denominator"] = "(l+1)^2*(k+l+1)"
    assert has(v.errors(result=s), "certificate denominator")


def test_rejects_scalar_sample_grid_contraction():
    s = copy.deepcopy(v.S)
    s["stage_a_scalar_envelope"]["stages"][-1]["equations"] -= 1
    assert has(v.errors(result=s), "scalar sample-grid contraction")


def test_rejects_module_sample_grid_contraction():
    s = copy.deepcopy(v.S)
    s["stage_b_full_weight5_module"]["stages"][-1]["rank_witness_rows"] -= 1
    assert has(v.errors(result=s), "weight-five sample-grid contraction")


def test_rejects_rank_inflation_or_nullity_drift():
    s = copy.deepcopy(v.S)
    s["stage_b_full_weight5_module"]["stages"][-1]["rank"] = 1997
    s["stage_b_full_weight5_module"]["stages"][-1]["nullity"] = 1
    assert has(v.errors(result=s), "module rank")


def test_rejects_proof_inflation():
    r = copy.deepcopy(v.R)
    r["disposition"]["proof_found"] = True
    r["disposition"]["status"] = "T3_PROVED"
    e = v.errors(record=r)
    assert has(e, "disposition inflation") or has(e, "proof/refutation inflation")


def test_rejects_refutation_inflation():
    r = copy.deepcopy(v.R)
    r["disposition"]["counterexample_found"] = True
    r["nonclaims"]["t3_refuted"] = True
    e = v.errors(record=r)
    assert has(e, "proof/refutation inflation") and has(e, "nonclaim promoted")


def test_rejects_next_route_drift():
    r = copy.deepcopy(v.R)
    r["disposition"]["next_distinct_route"] = "UNCONTROLLED_SEARCH"
    assert has(v.errors(record=r), "next-route drift")
