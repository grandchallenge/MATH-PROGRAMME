from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_010"
if str(CAMPAIGN) not in sys.path:
    sys.path.insert(0, str(CAMPAIGN))

import t3_011_f as producer  # noqa: E402
import verify_t3_011_f as verifier  # noqa: E402


class T3011FMixedChannelAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = producer.build()
        cls.replay = verifier.verify(cls.result)
        print(json.dumps({
            "operation": producer.OPERATION,
            "terminal": cls.result["terminal"],
            "tested_record_count": cls.result["tested_record_count"],
            "expected_full_record_count": cls.result["expected_full_record_count"],
            "first_cokernel_breaking_direction": cls.result["first_cokernel_breaking_direction"],
            "first_semantic_functional_ambiguity": cls.result["first_semantic_functional_ambiguity"],
            "predecessor_channel_ledgers_exactly_matched": cls.result["predecessor_checkpoint"]["channel_ledgers_exactly_matched"],
            "predecessor_channel_ledgers_sha256": cls.result["predecessor_checkpoint"]["channel_ledgers_sha256"],
        }, sort_keys=True, separators=(",", ":")))

    def test_terminal_and_independent_replay_agree(self):
        allowed = {
            producer.POSITIVE_TERMINAL,
            producer.NEGATIVE_TERMINAL,
            producer.AMBIGUITY_TERMINAL,
        }
        self.assertIn(self.result["terminal"], allowed)
        self.assertEqual(self.replay["terminal"], self.result["terminal"])
        self.assertEqual(self.replay["tested_record_count"], self.result["tested_record_count"])
        self.assertTrue(self.replay["predecessor_channel_ledgers_exactly_matched"])
        self.assertEqual(
            self.replay["predecessor_channel_ledgers_sha256"],
            self.result["predecessor_checkpoint"]["channel_ledgers_sha256"],
        )

    def test_admitted_pair_class_is_exactly_the_genuinely_mixed_degree_two_class(self):
        self.assertEqual(
            producer.ADMITTED_PAIRS,
            (
                ("n1", "k1"), ("n1", "l1"),
                ("n2", "k1"), ("n2", "l1"),
                ("n3", "k1"), ("n3", "l1"),
                ("k1", "l1"),
            ),
        )
        for left, right in producer.ADMITTED_PAIRS:
            self.assertNotEqual(producer.CHANNEL_COORDINATE[left], producer.CHANNEL_COORDINATE[right])
        mixed = self.result["mixed_class"]
        self.assertEqual(mixed["total_degree"], 2)
        self.assertEqual(mixed["multiplier"], "x_c*x_d")
        self.assertTrue(mixed["same_coordinate_pairs_excluded_as_E_reducible"])
        self.assertTrue(mixed["endpoint_anchored_candidate_banks"])

    def test_scope_mutations_fail_closed(self):
        with self.assertRaises(AssertionError):
            producer.validate_scope(pairs=(("n1", "n2"),) + producer.ADMITTED_PAIRS[1:])
        with self.assertRaises(AssertionError):
            producer.validate_scope(pairs=tuple(reversed(producer.ADMITTED_PAIRS)))
        with self.assertRaises(AssertionError):
            producer.validate_scope(total_degree=3)
        with self.assertRaises(AssertionError):
            producer.validate_scope(square_terms=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(arbitrary_bivariate=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(linear_combinations=True)
        with self.assertRaises(AssertionError):
            producer.validate_scope(support_enlargement=True)

    def test_affine_factor_translation_is_exact(self):
        rat = producer.rc.r_factor((1, 1, 0, 0), exponent=-2)
        moved_n2 = producer.translate_rat(rat, producer.a.pcl.SHIFTS["n2"])
        moved_k1 = producer.translate_rat(rat, producer.a.pcl.SHIFTS["k1"])
        self.assertEqual(moved_n2, producer.rc.r_factor((1, 1, 0, 2), exponent=-2))
        self.assertEqual(moved_k1, producer.rc.r_factor((1, 1, 0, 1), exponent=-2))

        tagged = (producer.a.pcl.PINV_TAG, 1, -1, 0, 0)
        protected = producer.rc.r_factor(tagged, exponent=-2)
        protected_n2 = producer.translate_rat(protected, producer.a.pcl.SHIFTS["n2"])
        protected_k1 = producer.translate_rat(protected, producer.a.pcl.SHIFTS["k1"])
        self.assertEqual(
            protected_n2,
            producer.rc.r_factor((producer.a.pcl.PINV_TAG, 1, -1, 0, 2), exponent=-2),
        )
        self.assertEqual(
            protected_k1,
            producer.rc.r_factor((producer.a.pcl.PINV_TAG, 1, -1, 0, -1), exponent=-2),
        )

    def test_e_source_lock_mutation_fails_closed(self):
        name = "t3_011_e.py"
        old = producer.E_BLOBS[name]
        try:
            producer.E_BLOBS[name] = "0" * 40
            with self.assertRaises(AssertionError):
                producer.assert_e_locks()
        finally:
            producer.E_BLOBS[name] = old
        producer.assert_e_locks()

    def test_predecessor_channel_ledger_mutation_fails_closed(self):
        rows = [
            {"channel": channel, **ledger}
            for channel, ledger in self.result["bank_ledgers"].items()
        ]
        synthetic = {"channel_ledgers": rows}
        digest = producer.assert_predecessor_channel_ledgers(
            synthetic,
            self.result["bank_ledgers"],
        )
        self.assertEqual(
            digest,
            self.result["predecessor_checkpoint"]["channel_ledgers_sha256"],
        )
        mutated_rows = [dict(row) for row in rows]
        mutated_rows[0]["candidate_count"] += 1
        with self.assertRaises(AssertionError):
            producer.assert_predecessor_channel_ledgers(
                {"channel_ledgers": mutated_rows},
                self.result["bank_ledgers"],
            )

    def test_terminal_stop_rule_and_semantic_functional_gate(self):
        records = self.result["tested_records"]
        self.assertEqual(len(records), self.result["tested_record_count"])
        if self.result["terminal"] == producer.POSITIVE_TERMINAL:
            self.assertTrue(records[-1]["normalized_cokernel_pairing_nonzero"])
            self.assertIs(self.result["first_cokernel_breaking_direction"], records[-1])
            self.assertIsNone(self.result["first_semantic_functional_ambiguity"])
            for rec in records:
                self.assertIsNone(rec["semantic_ambiguity_kind"])
                self.assertTrue(rec["pairing_representation_invariant"])
        elif self.result["terminal"] == producer.NEGATIVE_TERMINAL:
            self.assertEqual(len(records), self.result["expected_full_record_count"])
            self.assertIsNone(self.result["first_cokernel_breaking_direction"])
            self.assertIsNone(self.result["first_semantic_functional_ambiguity"])
            for rec in records:
                self.assertFalse(rec["normalized_cokernel_pairing_nonzero"])
                self.assertTrue(rec["direct_equals_product_rule"])
                self.assertTrue(rec["compound_shift_orders_commute_semantically"])
                self.assertTrue(rec["pairing_representation_invariant"])
        else:
            self.assertIs(self.result["first_semantic_functional_ambiguity"], records[-1])
            self.assertIsNotNone(records[-1]["semantic_ambiguity_kind"])
            self.assertIsNone(self.result["first_cokernel_breaking_direction"])

    def test_claim_firewall_unchanged(self):
        self.assertFalse(self.result["residual_sum_zero_proved"])
        self.assertEqual(self.result["proof_effect"], "NONE")
        self.assertEqual(self.result["promotion_effect"], "NONE")
        self.assertEqual(self.result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")
        for forbidden in (
            "square_terms_admitted",
            "degree_gt_2_admitted",
            "arbitrary_bivariate_polynomials_admitted",
            "linear_combinations_admitted",
            "support_or_harmonic_enlargement_admitted",
            "rational_prefactors_admitted",
            "recurrence_search_admitted",
            "correction_layer_work_admitted",
        ):
            self.assertFalse(self.result["mixed_class"][forbidden])


if __name__ == "__main__":
    unittest.main()
