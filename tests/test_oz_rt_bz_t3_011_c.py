from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_010"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class T3011CResponseGeneratorSemanticsAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.producer = load_module("t3_011_c", CAMPAIGN / "t3_011_c.py")
        cls.verifier = load_module("verify_t3_011_c", CAMPAIGN / "verify_t3_011_c.py")
        cls.contract = json.loads((CAMPAIGN / "T3_011_C_CONTRACT.json").read_text())
        cls.result = cls.producer.build()
        cls.replay = cls.verifier.verify(cls.result)

    def test_exact_frozen_bank_and_certified_concordance(self):
        self.assertEqual(self.result["independent_candidate_count"], 311)
        self.assertEqual(self.result["mirror_l1_audit"]["candidate_count"], 110)
        self.assertEqual(
            {x["channel"]: x["candidate_count"] for x in self.result["channel_audits"]},
            {"n1": 67, "n2": 67, "n3": 67, "k1": 110},
        )
        self.assertEqual(self.result["independent_mismatch_count"], 0)
        self.assertEqual(self.result["mirror_l1_audit"]["mismatch_count"], 0)
        self.assertTrue(self.result["all_frozen_responses_concordant"])
        self.assertEqual(self.result["terminal"], "T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_CERTIFIED")
        self.assertEqual(self.replay["status"], "INDEPENDENT_T3_011_C_RESPONSE_GENERATOR_SEMANTICS_AUDIT_REPLAY_COMPLETE")
        self.assertEqual(self.replay["mismatch_count"], 0)

    def test_all_421_response_checks_are_exactly_concordant(self):
        rows = []
        for rec in self.result["channel_audits"]:
            rows.extend(rec["candidates"])
        rows.extend(self.result["mirror_l1_audit"]["candidates"])
        self.assertEqual(len(rows), 421)
        for row in rows:
            self.assertTrue(row["direct_finite_difference_equals_product_rule"])
            self.assertTrue(row["direct_equals_t3_011_b_producer"])
            self.assertTrue(row["direct_equals_t3_011_b_verifier"])
            self.assertEqual(row["direct_finite_difference_sha256"], row["direct_product_rule_sha256"])
            self.assertEqual(row["direct_finite_difference_sha256"], row["t3_011_b_producer_sha256"])
            self.assertEqual(row["direct_finite_difference_sha256"], row["t3_011_b_verifier_sha256"])

    def test_direct_authority_is_source_independent(self):
        evidence = self.verifier.assert_direct_authority_independence()
        self.assertEqual(evidence["forbidden_helper_overlap"], [])
        self.assertNotIn("import t3_011_c", (CAMPAIGN / "verify_t3_011_c.py").read_text())

    def test_mutated_shared_authority_helper_fails_closed(self):
        synthetic = 'def direct_bad():\n    return b.primitive_shift_atom("H_k_1", (0, 1, 0))\n'
        with self.assertRaises(AssertionError):
            self.verifier.assert_direct_authority_independence(synthetic)

    def test_mutated_coordinate_increment_changes_raw_semantics(self):
        first = self.result["channel_audits"][0]["candidates"][0]["candidate"]
        mon = tuple(first[1])
        correct = self.producer.direct_finite_difference_poly(mon, "n1")
        mutated = self.producer.direct_finite_difference_poly(mon, "n1", increment_override=2)
        self.assertNotEqual(correct, mutated)

    def test_mutated_shell_semantics_digest_fails_closed(self):
        mutated = copy.deepcopy(self.result)
        mutated["direct_reconstruction"]["strata_semantics_sha256"] = "0" * 64
        with self.assertRaises(AssertionError):
            self.verifier.verify(mutated)

    def test_mutated_support_or_harmonic_candidate_fails_closed(self):
        mutated = copy.deepcopy(self.result)
        mutated["channel_audits"][0]["candidates"][0]["candidate"][1].append("__MUTATED_HARMONIC_MONOMIAL__")
        with self.assertRaises(AssertionError):
            self.verifier.verify(mutated)

    def test_mutated_mirror_marker_fails_closed(self):
        mutated = copy.deepcopy(self.result)
        mutated["mirror_l1_audit"]["candidate_count"] = 109
        with self.assertRaises(AssertionError):
            self.verifier.verify(mutated)

    def test_mutated_predecessor_lock_fails_closed(self):
        mutated = copy.deepcopy(self.result)
        mutated["predecessor_checkpoint"]["source_blobs"]["t3_011_b.py"] = "0" * 40
        with self.assertRaises(AssertionError):
            self.verifier.verify(mutated)

    def test_claim_firewall_inflation_fails_closed(self):
        mutated = copy.deepcopy(self.result)
        mutated["theorem_promotion_authorized"] = True
        with self.assertRaises(AssertionError):
            self.verifier.verify(mutated)

    def test_contract_preserves_no_widening_boundary(self):
        firewall = self.contract["claim_firewall"]
        for key in (
            "new_candidates_authorized", "pairs_or_two_lifts_authorized",
            "arbitrary_linear_combination_search_authorized", "generic_degree1_envelope_authorized",
            "support_or_harmonic_enlargement_authorized", "rational_prefactors_authorized",
            "adaptive_basis_growth_authorized", "raw_jet_reopening_authorized",
            "recurrence_search_authorized", "correction_layer_recombination_authorized",
            "theorem_promotion_authorized", "residual_sum_zero_proved",
        ):
            self.assertFalse(firewall[key])
        self.assertEqual(firewall["proof_effect"], "NONE")
        self.assertEqual(firewall["promotion_effect"], "NONE")
        self.assertEqual(firewall["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_registry_contains_governed_replays(self):
        registry = json.loads((ROOT / "ci" / "campaign_replay_registry.json").read_text())
        ids = {x["id"] for x in registry["entries"]}
        self.assertIn("OZ-RT-BZ-T3-011-C-PRODUCER", ids)
        self.assertIn("OZ-RT-BZ-T3-011-C-VERIFIER", ids)


if __name__ == "__main__":
    unittest.main()
