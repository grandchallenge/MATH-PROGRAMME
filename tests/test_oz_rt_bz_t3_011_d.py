from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_010"
sys.path.insert(0, str(HERE))

import t3_011_d as d
import verify_t3_011_d as v


class T3011DPolynomialDegreeExtensionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = d.build()
        cls.verified = v.verify(cls.result)
        cls.contract = json.loads((HERE / "T3_011_D_CONTRACT.json").read_text())

    def test_terminal_answers_only_the_bounded_degree_question(self):
        self.assertIn(self.result["terminal"], (d.POSITIVE_TERMINAL, d.NEGATIVE_TERMINAL))
        self.assertEqual(self.verified["terminal"], self.result["terminal"])
        self.assertTrue(self.verified["pairing_representation_invariance_checked"])
        if self.result["terminal"] == d.POSITIVE_TERMINAL:
            self.assertIsNotNone(self.result["first_cokernel_breaking_direction"])
            self.assertTrue(self.result["polynomial_degree_alone_breaks_cokernel_obstruction"])
        else:
            self.assertEqual(self.result["tested_independent_prefix_count"], 311)
            self.assertEqual(self.result["mirror_l1"]["tested_prefix_count"], 110)
            self.assertFalse(self.result["polynomial_degree_alone_breaks_cokernel_obstruction"])

    def test_degree_drift_fails_closed(self):
        with self.assertRaises(AssertionError):
            d.validate_operation_parameters(degree=1)
        with self.assertRaises(AssertionError):
            d.validate_operation_parameters(degree=3)

    def test_increment_drift_fails_closed(self):
        bad = dict(d.CHANNEL_INCREMENT)
        bad["n2"] = 1
        with self.assertRaises(AssertionError):
            d.validate_operation_parameters(increments=bad)

    def test_pair_and_mixed_channel_admission_fail_closed(self):
        with self.assertRaises(AssertionError):
            d.validate_operation_parameters(pairs_admitted=True)
        with self.assertRaises(AssertionError):
            d.validate_operation_parameters(mixed_channels_admitted=True)

    def test_candidate_order_mutation_fails_closed(self):
        mutated = copy.deepcopy(self.result)
        rows = mutated["tested_independent_prefix"]
        if len(rows) >= 2:
            rows[0], rows[1] = rows[1], rows[0]
            with self.assertRaises(AssertionError):
                v.verify(mutated)

    def test_pairing_mutation_fails_closed(self):
        mutated = copy.deepcopy(self.result)
        rows = mutated["tested_independent_prefix"]
        self.assertTrue(rows)
        rows[0]["obstruction_pairing"] = [999, 1]
        with self.assertRaises(AssertionError):
            v.verify(mutated)

    def test_first_nonzero_stop_rule_is_canonical(self):
        first = self.result["first_cokernel_breaking_direction"]
        if first is not None:
            independent = self.result["tested_independent_prefix"]
            mirror = self.result["mirror_l1"]["tested_prefix"]
            self.assertTrue((independent and independent[-1] == first) or (mirror and mirror[-1] == first))
        else:
            self.assertEqual(len(self.result["tested_independent_prefix"]), 311)
            self.assertEqual(len(self.result["mirror_l1"]["tested_prefix"]), 110)

    def test_claim_firewall_is_unchanged(self):
        self.assertFalse(self.result["residual_sum_zero_proved"])
        self.assertEqual(self.result["proof_effect"], "NONE")
        self.assertEqual(self.result["promotion_effect"], "NONE")
        self.assertEqual(self.result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")
        firewall = self.contract["claim_firewall"]
        for key, value in firewall.items():
            if key.endswith("_authorized") or key == "residual_sum_zero_proved":
                self.assertFalse(value)
        self.assertEqual(firewall["proof_effect"], "NONE")
        self.assertEqual(firewall["promotion_effect"], "NONE")
        self.assertEqual(firewall["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_registry_contains_governed_replays(self):
        registry = json.loads((ROOT / "ci" / "campaign_replay_registry.json").read_text())
        ids = {entry["id"] for entry in registry["entries"]}
        self.assertIn("OZ-RT-BZ-T3-011-D-PRODUCER", ids)
        self.assertIn("OZ-RT-BZ-T3-011-D-VERIFIER", ids)


if __name__ == "__main__":
    unittest.main()
