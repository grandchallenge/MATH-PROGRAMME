from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_008"

spec = importlib.util.spec_from_file_location("t3_008_validator", HERE / "validate.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-008 validator")
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

RESULT = json.loads((HERE / "SEARCH_RESULT.json").read_text(encoding="utf-8"))
RECORD = json.loads((HERE / "OZ_RT_BZ_T3_008.json").read_text(encoding="utf-8"))
SCHEMA = json.loads((HERE / "OZ_RT_BZ_T3_008.schema.json").read_text(encoding="utf-8"))
WITNESS = json.loads((HERE / "Q2_RANK_WITNESS.json").read_text(encoding="utf-8"))


class T3008ValidationTests(unittest.TestCase):
    def validate(self, result=None, record=None, witness=None):
        validator.validate_documents(copy.deepcopy(RESULT if result is None else result), copy.deepcopy(RECORD if record is None else record), copy.deepcopy(WITNESS if witness is None else witness), copy.deepcopy(SCHEMA), check_digests=False)

    def reject(self, result=None, record=None, witness=None):
        with self.assertRaises(AssertionError):
            self.validate(result=result, record=record, witness=witness)

    def test_baseline(self):
        self.validate()

    def test_dropped_monomial_rejected(self):
        r = copy.deepcopy(RESULT); r["basis"]["monomial_count"] = 197; self.reject(result=r)

    def test_nested_orientation_collapse_rejected(self):
        r = copy.deepcopy(RESULT); r["basis"]["one_nested_atom_count"] = 20; self.reject(result=r)

    def test_denominator_drift_rejected(self):
        r = copy.deepcopy(RESULT); r["flux"]["l_denominator"] = "(l+1)^2*(k+l+1)"; self.reject(result=r)

    def test_boundary_drift_rejected(self):
        r = copy.deepcopy(RESULT); r["flux"]["k_boundary_factor"] = "k*(n-k)"; self.reject(result=r)

    def test_broken_swap_closure_rejected(self):
        r = copy.deepcopy(RESULT); r["symmetry_completeness"]["denominator_swap_closed"] = False; self.reject(result=r)

    def test_preliminary_alias_promotion_rejected(self):
        r = copy.deepcopy(RESULT); r["preliminary_alias_grids"][0]["classification"] = "MODULAR_CANDIDATE_SPACE_REMAINS"; self.reject(result=r)

    def test_final_sample_grid_contraction_rejected(self):
        r = copy.deepcopy(RESULT); r["stages"][2]["n_max"] = 18; r["stages"][2]["full_grid_rows"] = 2465; self.reject(result=r)

    def test_coefficient_rank_drift_rejected(self):
        r = copy.deepcopy(RESULT); r["stages"][1]["coefficient_rank"] = 791; self.reject(result=r)

    def test_augmented_rank_drift_rejected(self):
        r = copy.deepcopy(RESULT); r["stages"][0]["augmented_rank"] = 198; self.reject(result=r)

    def test_witness_row_mutation_rejected(self):
        w = copy.deepcopy(WITNESS); w["coefficient_row_indices"][0] = w["coefficient_row_indices"][1]; self.reject(witness=w)

    def test_witness_extra_point_rejected(self):
        w = copy.deepcopy(WITNESS); w["augmented_extra_row_point"] = [21, 16, 15]; self.reject(witness=w)

    def test_proof_inflation_rejected(self):
        rec = copy.deepcopy(RECORD); rec["disposition"]["proof_found"] = True; self.reject(record=rec)

    def test_refutation_inflation_rejected(self):
        rec = copy.deepcopy(RECORD); rec["disposition"]["counterexample_found"] = True; self.reject(record=rec)

    def test_successor_route_drift_rejected(self):
        r = copy.deepcopy(RESULT); r["next_distinct_route"] = "SYMMETRIC_2D_RAW_JET_DIVERGENCE_002"; self.reject(result=r)

    def test_nonclaim_promotion_rejected(self):
        rec = copy.deepcopy(RECORD); rec["nonclaims"]["t3_proved"] = True; self.reject(record=rec)


if __name__ == "__main__":
    unittest.main()
