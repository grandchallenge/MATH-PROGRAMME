from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_010"
if str(CAMPAIGN) not in sys.path:
    sys.path.insert(0, str(CAMPAIGN))

import t3_011_g as producer  # noqa: E402
import verify_t3_011_g as verifier  # noqa: E402


class T3011GMixedPolynomialClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = producer.build()
        cls.replay = verifier.verify(cls.result)
        print(json.dumps({
            "operation": producer.OPERATION,
            "terminal": cls.result["terminal"],
            "candidate_record_count": cls.result["candidate_record_count"],
            "finite_nonzero_multidegree_residue": cls.result["finite_nonzero_multidegree_residue"],
            "semantic_functional_ambiguity": cls.result["semantic_functional_ambiguity"],
            "all_mixed_polynomial_multipliers_cokernel_invisible": cls.result["all_mixed_polynomial_multipliers_cokernel_invisible"],
        }, sort_keys=True, separators=(",", ":")))

    def test_terminal_and_independent_replay_agree(self):
        self.assertIn(self.result["terminal"], {
            producer.CLOSURE_TERMINAL,
            producer.FINITE_TERMINAL,
            producer.AMBIGUITY_TERMINAL,
            producer.BLOCKER_TERMINAL,
        })
        self.assertEqual(self.replay["terminal"], self.result["terminal"])
        self.assertEqual(self.replay["candidate_record_count"], self.result["candidate_record_count"])
        self.assertEqual(
            self.replay["finite_nonzero_multidegree_residue"],
            self.result["finite_nonzero_multidegree_residue"],
        )

    def test_exact_genuinely_mixed_domain(self):
        cls = self.result["mixed_polynomial_class"]
        self.assertEqual(cls["monomial_domain"], "x_c^r*x_d^s with integers r>=1,s>=1")
        self.assertTrue(cls["pure_axes_excluded_as_E_closed"])
        self.assertTrue(cls["same_coordinate_pairs_excluded_as_E_reducible"])
        self.assertTrue(cls["finite_support_overlap_derived_without_degree_cutoff"])
        for left, right in producer.ADMITTED_PAIRS:
            self.assertNotEqual(producer.CHANNEL_COORDINATE[left], producer.CHANNEL_COORDINATE[right])

    def test_scope_mutations_fail_closed(self):
        with self.assertRaises(AssertionError):
            producer.validate_scope(pairs=tuple(reversed(producer.ADMITTED_PAIRS)))
        with self.assertRaises(AssertionError):
            producer.validate_scope(arbitrary_degree_cutoff=3)
        with self.assertRaises(AssertionError):
            producer.validate_scope(pure_axis_terms=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(same_coordinate_pairs=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(support_enlargement=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(rational_prefactors=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(recurrence_widening=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(correction_recombination=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(candidate_linear_combinations=True)

    def test_multidegree_solver_handles_degenerate_shared_factor_exactly(self):
        factor = (1, 0, 0, 0)
        base = ()
        left = ((factor, 1),)
        right = ((factor, 1),)
        target = ((factor, 4),)
        self.assertEqual(
            producer._solve_multidegrees(base, left, right, target),
            [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)],
        )

    def test_f_source_lock_mutation_fails_closed(self):
        name = "t3_011_f.py"
        old = producer.F_BLOBS[name]
        try:
            producer.F_BLOBS[name] = "0" * 40
            with self.assertRaises(AssertionError):
                producer.assert_f_locks()
        finally:
            producer.F_BLOBS[name] = old
        producer.assert_f_locks()

    def test_degree_1_1_exactly_replays_f_for_every_record(self):
        for rec in self.result["candidate_records"]:
            self.assertTrue(rec["degree_1_1_semantics_exactly_match_f"])
            self.assertEqual(rec["degree_1_1_pairing"], rec["f_degree_1_1_pairing"])

    def test_finite_support_proof_route_is_total(self):
        self.assertEqual(self.result["candidate_record_count"], producer.F_EXPECTED_RECORDS)
        for rec in self.result["candidate_records"]:
            self.assertIsInstance(rec["finite_overlap_multidegrees"], list)
            for r, s in rec["finite_overlap_multidegrees"]:
                self.assertGreaterEqual(r, 1)
                self.assertGreaterEqual(s, 1)
            if rec["all_genuinely_mixed_monomial_degrees_annihilated"]:
                self.assertEqual(rec["nonzero_pairings"], [])

    def test_claim_firewall_unchanged(self):
        self.assertFalse(self.result["residual_sum_zero_proved"])
        self.assertEqual(self.result["proof_effect"], "NONE")
        self.assertEqual(self.result["promotion_effect"], "NONE")
        self.assertEqual(self.result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")
        cls = self.result["mixed_polynomial_class"]
        for forbidden in (
            "support_or_harmonic_enlargement_admitted",
            "rational_prefactors_admitted",
            "recurrence_search_admitted",
            "correction_layer_work_admitted",
            "candidate_linear_combinations_admitted",
        ):
            self.assertFalse(cls[forbidden])


if __name__ == "__main__":
    unittest.main()
