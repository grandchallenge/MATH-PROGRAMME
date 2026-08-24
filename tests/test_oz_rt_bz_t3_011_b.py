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


class T3011BCokernelNonzeroResponseLiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.producer = load_module("t3_011_b", CAMPAIGN / "t3_011_b.py")
        cls.verifier = load_module("verify_t3_011_b", CAMPAIGN / "verify_t3_011_b.py")
        cls.contract = json.loads((CAMPAIGN / "T3_011_B_CONTRACT.json").read_text())
        cls.result = cls.producer.build()
        cls.replay = cls.verifier.verify(cls.result)

    def test_declared_bounded_class_and_exact_replay(self):
        self.assertEqual(
            self.result["bounded_correction_class"]["id"],
            "SUPPORT_LOCKED_SINGLE_CHANNEL_LINEAR_NONZERO_RESPONSE_LIFT_001",
        )
        self.assertEqual(self.result["independent_candidate_count"], 311)
        expected = {"n1": 67, "n2": 67, "n3": 67, "k1": 110}
        self.assertEqual(
            {x["channel"]: x["candidate_count"] for x in self.result["channel_systems"]},
            expected,
        )
        for rec in self.result["channel_systems"]:
            self.assertEqual(rec["candidate_count"], rec["base_coefficient_rank"])
            self.assertEqual(
                rec["candidate_count"] + rec["base_zero_global_columns"],
                rec["base_unknown_count"],
            )
            self.assertEqual(
                rec["candidate_bank"],
                "complete-global-response-nonzero C unknowns only",
            )
        self.assertEqual(
            self.replay["status"],
            "INDEPENDENT_T3_011_B_COKERNEL_NONZERO_RESPONSE_SINGLE_LIFT_REPLAY_COMPLETE",
        )
        self.assertFalse(self.replay["producer_matrix_imported_as_authority"])

    def test_every_cokernel_witness_is_normalized(self):
        for rec in self.result["channel_systems"]:
            self.assertEqual(rec["cokernel_target_pairing"], [1, 1])
            self.assertTrue(rec["cokernel_witness_rows"])
            self.assertEqual(
                self.producer.p.sha(rec["cokernel_witness_rows"]),
                rec["cokernel_witness_sha256"],
            )

    def test_candidate_ledger_is_exactly_311_one_lift_trials(self):
        total = 0
        for rec in self.result["channel_systems"]:
            self.assertEqual(len(rec["trials"]), rec["candidate_count"])
            candidates = []
            for trial in rec["trials"]:
                candidates.append((trial["candidate"][0], tuple(trial["candidate"][1])))
                self.assertIn(trial["lift_coordinate"], ("n", "k"))
                if trial["obstruction_pairing_nonzero"]:
                    self.assertTrue(trial["exact_rank_test_run"])
                else:
                    self.assertFalse(trial["exact_rank_test_run"])
                    self.assertEqual(trial["classification"], "REJECTED_BY_COKERNEL_WITNESS")
                    self.assertFalse(trial["rank_consistent"])
            self.assertEqual(len(candidates), len(set(candidates)))
            self.assertEqual(
                rec["rank_tested_candidate_count"],
                rec["nonzero_obstruction_pairing_candidate_count"],
            )
            total += len(rec["trials"])
        self.assertEqual(total, 311)

    def test_canonical_channel_disposition_matches_geometry(self):
        allowed = {
            "CANONICAL_SINGLE_LIFT_SURVIVOR",
            "COKERNEL_ACTIVE_SINGLE_LIFTS_EXACTLY_INCONSISTENT",
            "ALL_NONZERO_RESPONSE_SINGLE_LIFTS_COKERNEL_INVISIBLE",
        }
        for rec in self.result["channel_systems"]:
            self.assertIn(rec["canonical_channel_disposition"], allowed)
            if rec["canonical_selected_candidate"] is not None:
                self.assertEqual(rec["canonical_channel_disposition"], "CANONICAL_SINGLE_LIFT_SURVIVOR")
            elif rec["nonzero_obstruction_pairing_candidate_count"]:
                self.assertEqual(
                    rec["canonical_channel_disposition"],
                    "COKERNEL_ACTIVE_SINGLE_LIFTS_EXACTLY_INCONSISTENT",
                )
            else:
                self.assertEqual(
                    rec["canonical_channel_disposition"],
                    "ALL_NONZERO_RESPONSE_SINGLE_LIFTS_COKERNEL_INVISIBLE",
                )

    def test_mutated_witness_digest_fails_closed(self):
        rec = copy.deepcopy(self.result["channel_systems"][0])
        rec["cokernel_witness_rows"][0][2] += 1
        parsed = self.verifier.va.parse_witness_rows(rec["cokernel_witness_rows"])
        self.assertNotEqual(
            self.verifier.va.sha(self.verifier.va.witness_rows(parsed)),
            rec["cokernel_witness_sha256"],
        )

    def test_mutated_selected_solution_fails_digest_when_present(self):
        selected = next(
            (x for x in self.result["channel_systems"] if x["selected_solution_coefficients"]),
            None,
        )
        if selected is None:
            self.skipTest("bounded class has no selected solution to mutate")
        rows = copy.deepcopy(selected["selected_solution_coefficients"])
        rows[0][2] += 1
        self.assertNotEqual(self.producer.p.sha(rows), selected["selected_solution_sha256"])

    def test_forbidden_enlargements_and_claim_firewall(self):
        bounded = self.contract["bounded_correction_class"]
        for key in (
            "pairs_admitted",
            "arbitrary_linear_combinations_admitted",
            "mix_with_zero_response_bank",
            "new_harmonic_monomials",
            "full_degree1_envelope",
            "rational_prefactor_search",
            "adaptive_basis_growth",
            "generic_198_raw_jet_reopened",
            "recurrence_search",
        ):
            self.assertFalse(bounded[key])
        self.assertEqual(bounded["lifts_per_trial"], 1)
        self.assertFalse(self.result["full_correction_layer_recombined"])
        self.assertFalse(self.result["finite_boundary_assembly_completed"])
        self.assertFalse(self.result["final_n_holonomic_search_run"])
        self.assertFalse(self.result["residual_sum_zero_proved"])
        self.assertEqual(self.result["proof_effect"], "NONE")
        self.assertEqual(self.result["promotion_effect"], "NONE")
        self.assertEqual(self.result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_registry_contains_governed_replays(self):
        registry = json.loads((ROOT / "ci" / "campaign_replay_registry.json").read_text())
        ids = {x["id"] for x in registry["entries"]}
        self.assertIn("OZ-RT-BZ-T3-011-B-PRODUCER", ids)
        self.assertIn("OZ-RT-BZ-T3-011-B-VERIFIER", ids)


if __name__ == "__main__":
    unittest.main()
