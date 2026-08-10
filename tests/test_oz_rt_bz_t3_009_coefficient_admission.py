from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_009"
COEFF = HERE / "ONE_BODY_COEFFICIENT_LAYER.json"
ROUTE = HERE / "HOLONOMIC_ROUTE.json"
DIGEST = "90d067ae59790fab8648d006635c14950359b66eb8b57361e61d5b47b2b3af40"
NEXT = "SYMMETRY_REDUCED_CHANNEL_HARMONIC_BLOCK_WITH_SHELL_STRATA_001"


class T3009CoefficientAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.coeff = json.loads(COEFF.read_text(encoding="utf-8"))
        cls.route = json.loads(ROUTE.read_text(encoding="utf-8"))

    def test_independent_replay_is_admitted(self):
        c = self.coeff
        self.assertEqual(c["execution_boundary"], "FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_001")
        self.assertEqual(c["status"], "FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_INDEPENDENTLY_REPLAYED")
        self.assertEqual(c["independent_replay_status"], "INDEPENDENT_FULL_POLE_FREE_ONE_BODY_COEFFICIENT_REPLAY_COMPLETE")
        self.assertTrue(c["holonomic_search_admitted"])
        self.assertEqual(c["final_layer"]["monomials"], 122)
        self.assertEqual(c["final_layer"]["atoms"], 22)
        self.assertEqual(c["final_layer"]["max_atomic_arity"], 3)
        self.assertEqual(c["final_layer"]["scalar_basis_size"], 11)
        self.assertEqual(c["final_layer"]["sha256"], DIGEST)
        r = c["independent_replay"]
        self.assertEqual(r["sha256"], DIGEST)
        self.assertEqual(r["protected_factor_count"], 8)
        self.assertEqual(r["exact_atom_shift_checks"], 38950)
        self.assertEqual(r["exact_full_target_shift_checks"], 950)
        self.assertEqual(r["checks_touching_moving_shell"], 800)
        self.assertEqual(r["nested_skeleton_channels_verified"], 5)
        self.assertEqual(r["abel_exact_checks"], 9)
        self.assertTrue(r["full_rows_reconstructed_independently"])
        self.assertFalse(r["producer_module_imported"])

    def test_successor_preserves_shell_semantics(self):
        r = self.route
        self.assertEqual(r["status"], "STRUCTURED_HOLONOMIC_ROUTE_ADMITTED_AFTER_INDEPENDENT_POLE_FREE_COEFFICIENT_REPLAY")
        self.assertEqual(r["exact_prerequisite"]["status"], "SATISFIED")
        self.assertEqual(r["exact_prerequisite"]["sha256"], DIGEST)
        self.assertEqual(r["next_execution_boundary"], NEXT)
        self.assertTrue(r["shell_stratification"]["required"])
        self.assertEqual(len(r["shell_stratification"]["protected_factors"]), 8)
        self.assertTrue(r["shell_stratification"]["shell_terms_must_be_recombined"])
        self.assertTrue(r["bounded_search_policy"]["shell_semantics_must_be_preserved"])
        self.assertTrue(r["bounded_search_policy"]["support_or_rank_viability_probe_required"])
        self.assertTrue(r["bounded_search_policy"]["unbounded_creative_telescoping_forbidden_as_first_move"])

    def test_claim_boundary_remains_closed(self):
        for obj in (self.coeff, self.route):
            self.assertEqual(obj["proof_effect"], "NONE")
            self.assertEqual(obj["promotion_effect"], "NONE")
            self.assertEqual(obj["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")
        self.assertFalse(self.coeff["residual_sum_zero_proved"])
        self.assertFalse(self.coeff["finite_sampling_used_as_sum_proof"])


if __name__ == "__main__":
    unittest.main()
