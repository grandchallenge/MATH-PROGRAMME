from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_007" / "validate.py"
spec = importlib.util.spec_from_file_location("oz_t3_007_validate", PATH)
assert spec is not None and spec.loader is not None
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

T3005 = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_005"
sys.path.insert(0, str(T3005))
import jet_map as protected_jet_map  # type: ignore


def has(errors, text):
    return any(text in e for e in errors)


class TestOZRTBZT3007(unittest.TestCase):
    def test_baseline_is_valid(self):
        self.assertEqual(v.errors(), [])

    def test_protected_raw_jet_normalization_is_invertible_mod_rank_prime(self):
        mapping = protected_jet_map.coefficient_map()
        multipliers = [item["raw_derivative_multiplier"] for item in mapping["monomials"]]
        self.assertEqual(len(multipliers), 198)
        self.assertTrue(all(isinstance(x, int) and x != 0 for x in multipliers))
        self.assertTrue(all(x % 1000003 != 0 for x in multipliers))

    def test_rejects_order_drift(self):
        s = copy.deepcopy(v.S)
        s["search_class"]["orders"] = [3, 5]
        self.assertTrue(has(v.errors(result=s), "order drift"))

    def test_rejects_unknown_count_drift(self):
        s = copy.deepcopy(v.S)
        s["order4_full_weight5_module"]["stages"][-1]["unknowns"] = 2009
        self.assertTrue(has(v.errors(result=s), "order-4 unknown-count drift"))

    def test_rejects_dropped_weight_five_monomial(self):
        s = copy.deepcopy(v.S)
        s["basis"]["monomial_count"] = 197
        self.assertTrue(has(v.errors(result=s), "basis cardinality"))

    def test_rejects_nested_orientation_collapse(self):
        s = copy.deepcopy(v.S)
        s["basis"]["one_nested_atom_count"] = 20
        s["mirror_status"] = "ONE_ORIENTATION_ONLY"
        e = v.errors(result=s)
        self.assertTrue(has(e, "basis cardinality") and has(e, "mirror-equivalence"))

    def test_rejects_normalization_drift(self):
        s = copy.deepcopy(v.S)
        s["coordinate_normalization"]["all_nonzero_mod_prime"] = False
        self.assertTrue(has(v.errors(result=s), "normalization invertibility"))

    def test_rejects_certificate_denominator_drift(self):
        s = copy.deepcopy(v.S)
        s["certificate_denominator"] = "(l+1)^2*(k+l+1)"
        self.assertTrue(has(v.errors(result=s), "certificate denominator"))

    def test_rejects_sample_grid_contraction(self):
        s = copy.deepcopy(v.S)
        s["order3_full_weight5_module"]["stages"][-1]["full_grid_rows"] -= 1
        self.assertTrue(has(v.errors(result=s), "order-3 sample-grid contraction"))

    def test_rejects_rank_or_nullity_drift(self):
        s = copy.deepcopy(v.S)
        s["order4_full_weight5_module"]["stages"][-1]["rank"] = 2009
        s["order4_full_weight5_module"]["stages"][-1]["nullity"] = 1
        self.assertTrue(has(v.errors(result=s), "module rank"))

    def test_rejects_proof_inflation(self):
        r = copy.deepcopy(v.R)
        r["disposition"]["proof_found"] = True
        r["disposition"]["status"] = "T3_PROVED"
        e = v.errors(record=r)
        self.assertTrue(has(e, "disposition inflation") or has(e, "proof/refutation inflation"))

    def test_rejects_refutation_inflation(self):
        r = copy.deepcopy(v.R)
        r["disposition"]["counterexample_found"] = True
        r["nonclaims"]["t3_refuted"] = True
        e = v.errors(record=r)
        self.assertTrue(has(e, "proof/refutation inflation") and has(e, "nonclaim promoted"))

    def test_rejects_successor_route_drift(self):
        r = copy.deepcopy(v.R)
        r["disposition"]["next_distinct_route"] = "UNCONTROLLED_SEARCH"
        self.assertTrue(has(v.errors(record=r), "next-route drift"))


if __name__ == "__main__":
    unittest.main()
