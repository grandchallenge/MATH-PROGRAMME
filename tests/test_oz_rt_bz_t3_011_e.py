from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_010"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_e as producer
import t3_011_e_factors as factor_adapter
import verify_t3_011_e as verifier

producer._coordinate_factors = lambda channel, strata: factor_adapter.producer_factor_map(
    producer, channel, strata
)
verifier._factor_map = lambda channel, strata: factor_adapter.verifier_factor_map(
    verifier, channel, strata
)


class T3011EPolynomialClosureAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = producer.build()
        cls.verified = verifier.verify(cls.result)
        print(
            "T3_011_E_TERMINAL_SUMMARY="
            + repr(
                {
                    "terminal": cls.result["terminal"],
                    "semantic_functional_ambiguity": cls.result["semantic_functional_ambiguity"],
                    "higher_degree_set": cls.result["higher_degree_set"],
                    "first_unresolved_degree": cls.result["first_unresolved_degree"],
                    "candidate_record_count": cls.result["candidate_record_count"],
                    "all_single_channel_polynomial_multipliers_cokernel_invisible": cls.result[
                        "all_single_channel_polynomial_multipliers_cokernel_invisible"
                    ],
                }
            )
        )

    def test_terminal_and_firewall(self):
        self.assertIn(
            self.result["terminal"],
            {
                producer.CLOSURE_TERMINAL,
                producer.FINITE_TERMINAL,
                producer.AMBIGUITY_TERMINAL,
                producer.BLOCKER_TERMINAL,
            },
        )
        self.assertEqual(self.result["candidate_record_count"], 421)
        self.assertFalse(self.result["proof_route"]["direct_higher_degree_response_scan_used"])
        self.assertFalse(self.result["proof_route"]["polynomial_sampling_used"])
        self.assertFalse(self.result["residual_sum_zero_proved"])
        self.assertEqual(self.result["proof_effect"], "NONE")
        self.assertEqual(self.result["promotion_effect"], "NONE")
        self.assertEqual(self.result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_independent_terminal_agreement(self):
        self.assertEqual(self.verified["terminal"], self.result["terminal"])
        self.assertEqual(self.verified["candidate_record_count"], 421)
        self.assertEqual(
            self.verified["all_single_channel_polynomial_multipliers_cokernel_invisible"],
            self.result["all_single_channel_polynomial_multipliers_cokernel_invisible"],
        )

    def test_certified_prefix_is_exactly_zero(self):
        for rec in self.result["candidate_records"]:
            self.assertEqual(
                rec["certified_semantic_lambda_0_2"],
                [[0, 0, 1], [1, 0, 1], [2, 0, 1]],
            )

    def test_no_blind_higher_degree_scan_authority(self):
        with self.assertRaises(AssertionError):
            producer.validate_scope(direct_higher_degree_scan=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(polynomial_sampling=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(pair_search=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(mixed_channels=True)

    def test_result_mutation_fails_closed(self):
        bad = copy.deepcopy(self.result)
        bad["candidate_records"][0]["shifted_x_moments"]["possible_degrees"] = [999]
        with self.assertRaises(AssertionError):
            verifier.verify(bad)

    def test_terminal_mutation_fails_closed(self):
        bad = copy.deepcopy(self.result)
        bad["terminal"] = producer.CLOSURE_TERMINAL if self.result["terminal"] != producer.CLOSURE_TERMINAL else producer.FINITE_TERMINAL
        with self.assertRaises(AssertionError):
            verifier.verify(bad)

    def test_higher_degree_set_is_structural_only(self):
        if self.result["terminal"] == producer.FINITE_TERMINAL:
            self.assertTrue(self.result["higher_degree_set"])
            self.assertGreaterEqual(self.result["first_unresolved_degree"], 3)
        if self.result["terminal"] == producer.CLOSURE_TERMINAL:
            self.assertEqual(self.result["higher_degree_set"], [])
            self.assertIsNone(self.result["first_unresolved_degree"])


if __name__ == "__main__":
    unittest.main()
