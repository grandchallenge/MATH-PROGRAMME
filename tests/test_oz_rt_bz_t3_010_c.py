from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from fractions import Fraction as Q
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


class T3010CSharedCoefficientExtractionTests(unittest.TestCase):
    def test_global_exact_compatibility_extraction_and_firewall(self):
        producer = load_module("t3_010_c", CAMPAIGN / "t3_010_c.py")
        verifier = load_module("verify_t3_010_c", CAMPAIGN / "verify_t3_010_c.py")
        contract = json.loads((CAMPAIGN / "T3_010_C_CONTRACT.json").read_text())

        c1 = {("cell", ("S", ("H_k_1",), ())): Q(1)}
        c2 = {("cell", ("S", ("H_k_1",), ())): Q(1)}
        ids = [("S", ("H_k_1",)), ("S", ("H_l_1",))]
        sol = producer.exact_particular_solution(ids, [c1, c2], c1)
        self.assertIsNotNone(sol)
        self.assertEqual(producer.apply_solution(ids, [c1, c2], sol), c1)

        missing = {("other", ("S", ("H_k_2",), ())): Q(1)}
        self.assertIsNone(producer.exact_particular_solution(ids, [c1, c2], missing))

        result = producer.build()
        self.assertEqual(result["stage"], contract["stage"])
        self.assertEqual(
            result["t3_010_b_checkpoint"]["validated_head"],
            contract["t3_010_b_checkpoint"]["validated_head"],
        )
        self.assertEqual(len(result["channel_systems"]), 4)
        self.assertEqual(
            result["globally_consistent_independent_channel_count"]
            + result["globally_inconsistent_independent_channel_count"],
            4,
        )
        for rec in result["channel_systems"]:
            self.assertEqual(
                rec["active_cell_count"] + rec["structural_zero_cell_count"], 100
            )
            self.assertEqual(
                rec["exact_solution_extracted"],
                rec["classification"].startswith("CONSISTENT_"),
            )
            if rec["exact_solution_extracted"]:
                self.assertEqual(
                    rec["exact_substitution_checks"], rec["active_cell_count"]
                )
                self.assertTrue(rec["solution_coefficients"])
            else:
                self.assertEqual(rec["exact_substitution_checks"], 0)
                self.assertEqual(rec["solution_coefficients"], [])

        self.assertFalse(result["local_consistency_promoted_to_certificate"])
        self.assertFalse(result["full_correction_layer_recombined"])
        self.assertFalse(result["full_symbolic_flux_identity_substituted"])
        self.assertFalse(result["finite_boundary_assembly_completed"])
        self.assertFalse(result["final_n_holonomic_search_run"])
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        replay = verifier.verify(result)
        self.assertEqual(
            replay["status"],
            "INDEPENDENT_T3_010_C_GLOBAL_EXACT_SOLUTION_REPLAY_COMPLETE",
        )
        self.assertEqual(replay["independent_channel_count"], 4)
        self.assertEqual(
            replay["globally_consistent_independent_channel_count"],
            result["globally_consistent_independent_channel_count"],
        )
        self.assertEqual(
            replay["globally_inconsistent_independent_channel_count"],
            result["globally_inconsistent_independent_channel_count"],
        )
        self.assertFalse(replay["producer_matrix_imported_as_authority"])

        bad_rank = copy.deepcopy(result)
        bad_rank["channel_systems"][0]["augmented_rank"] += 1
        with self.assertRaisesRegex(AssertionError, "independent C reconstruction drift"):
            verifier.verify(bad_rank)

        extracted = next(
            (x for x in result["channel_systems"] if x["exact_solution_extracted"]),
            None,
        )
        if extracted is not None:
            bad_solution = copy.deepcopy(result)
            target = next(
                x for x in bad_solution["channel_systems"]
                if x["channel"] == extracted["channel"]
            )
            target["solution_coefficients"][0][2] += 1
            with self.assertRaises(AssertionError):
                verifier.verify(bad_solution)

        inflated = copy.deepcopy(result)
        inflated["full_correction_layer_recombined"] = True
        with self.assertRaisesRegex(AssertionError, "claim-boundary inflation"):
            verifier.verify(inflated)

        recurrence = copy.deepcopy(result)
        recurrence["final_n_holonomic_search_run"] = True
        with self.assertRaisesRegex(AssertionError, "claim-boundary inflation"):
            verifier.verify(recurrence)

        self.assertEqual(contract["shared_coefficient_system"]["field"], "Q")
        self.assertEqual(contract["bounded_correction_class"]["coefficient_degree"], 0)
        self.assertFalse(contract["bounded_correction_class"]["adaptive_basis_growth"])
        self.assertFalse(contract["positive_boundary"]["final_n_holonomic_search"])


if __name__ == "__main__":
    unittest.main()
