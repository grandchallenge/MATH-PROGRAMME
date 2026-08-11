from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"


def load_module(name: str, path: Path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ds=load_module("t3_009_deformation_span",HERE/"deformation_span.py")
ls=load_module("t3_009_letter_split",HERE/"letter_split.py")


class T3009DeformationAndLetterSplitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deformation=ds.result()
        cls.deformation_retained=json.loads((HERE/"DEFORMATION_SPAN_RESULT.json").read_text(encoding="utf-8"))
        cls.letter=ls.result()
        cls.letter_retained=json.loads((HERE/"LETTER_SPLIT_RESULT.json").read_text(encoding="utf-8"))

    def test_eight_dimensional_weight1_tangent_space(self):
        self.assertEqual(self.deformation["gamma_deformation"]["weight1_tangent_rank"],8)
        self.assertEqual(self.deformation["dimension_obstruction"]["rank"],8)
        self.assertEqual(self.deformation["gamma_deformation"]["parameter_count_to_generate_full_weight1_tangent_space"],8)

    def test_fixed_qrow_automatic_differentiation_is_exactly_obstructed(self):
        obs=self.deformation["fixed_qrow_operator_obstruction"]
        self.assertEqual(obs["Y_n_0_through_3"],["0","16","3564","3214312/3"])
        self.assertEqual(obs["recurrence_coefficients_at_n0"],[1467828,-2206008156,-100515858678,420528510])
        self.assertEqual(obs["exact_LBZ_Y_at_n0"],"92296128886152")
        self.assertTrue(obs["nonzero"])
        self.assertEqual(self.deformation["status"],"SMALL_PARAMETER_QROW_AUTOMATIC_DIFFERENTIATION_ROUTE_REJECTED")
        self.assertEqual(self.deformation["next_route"],"STRUCTURED_ONE_BODY_LETTER_SPLIT_HOLONOMIC_001")

    def test_deformation_retained_result_matches_builder(self):
        self.assertEqual(self.deformation_retained,self.deformation)

    def test_letter_split_exact_symmetry_quotient_and_rank(self):
        self.assertEqual(self.letter["input_atom_count"],22)
        self.assertEqual(self.letter["k_l_symmetry_orbit_representative_count"],13)
        self.assertEqual([len(self.letter["weight_blocks"][k]) for k in ("weight1","weight2","weight3","weight4")],[5,4,2,2])
        diag=self.letter["diagnostic_defect_matrix"]
        self.assertEqual(diag["exact_rank_over_Q"],12)
        self.assertFalse(diag["finite_samples_used_as_global_zero_proof"])

    def test_weight1_sampled_null_direction_is_not_promoted(self):
        x=self.letter["unique_sampled_null_direction"]
        self.assertEqual(x["coordinates_first_five_weight1_columns"],[-3,-1,1,2,1])
        self.assertEqual(x["identification"],"partial_k log(T)")
        self.assertTrue(x["global_zero_not_claimed_from_sampling"])
        self.assertEqual(self.letter["first_lane"],"WEIGHT1_FIVE_ORBIT_SEPARATED_LETTER_CERT_001")

    def test_letter_split_retained_result_matches_builder(self):
        self.assertEqual(self.letter_retained,self.letter)

    def test_claim_firewall(self):
        for x in (self.deformation,self.deformation_retained,self.letter,self.letter_retained):
            self.assertEqual(x["proof_effect"],"NONE")
            self.assertEqual(x["promotion_effect"],"NONE")
            self.assertEqual(x["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")


if __name__=="__main__":
    unittest.main()
