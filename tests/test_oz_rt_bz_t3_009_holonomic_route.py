from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"


class T3009HolonomicRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.route=json.loads((HERE/"HOLONOMIC_ROUTE.json").read_text(encoding="utf-8"))

    def test_route_follows_deformation_negative(self):
        self.assertEqual(cls_route := self.route["predecessor_negative"],"campaigns/odd_zeta/OZ_RT_BZ_T3_009/DEFORMATION_SPAN_RESULT.json")
        self.assertEqual(self.route["status"],"STRUCTURED_HOLONOMIC_ROUTE_LOCKED_AFTER_DEFORMATION_REJECTION")

    def test_symmetry_reduced_channel_and_letter_blocks(self):
        self.assertEqual(self.route["channel_decomposition"]["symmetry_reduced_channels"],["n1","n2","n3","k1"])
        self.assertEqual(self.route["letter_decomposition"]["k_l_orbit_representatives"],13)
        self.assertEqual(self.route["letter_decomposition"]["weight_block_sizes"],[5,4,2,2])

    def test_oversplitting_and_generic_reopen_are_forbidden(self):
        self.assertIn("Do not require each letter",self.route["anti_oversplitting_rule"])
        policy=self.route["bounded_search_policy"]
        self.assertTrue(policy["generic_198_raw_jet_reopen_forbidden"])
        self.assertTrue(policy["unbounded_creative_telescoping_forbidden_as_first_move"])
        self.assertTrue(policy["support_or_rank_viability_probe_required"])
        self.assertTrue(policy["finite_sampling_is_not_proof"])

    def test_next_boundary_and_claim_firewall(self):
        self.assertEqual(self.route["next_execution_boundary"],"FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_001")
        self.assertEqual(self.route["proof_effect"],"NONE")
        self.assertEqual(self.route["promotion_effect"],"NONE")
        self.assertEqual(self.route["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")


if __name__=="__main__":
    unittest.main()
