from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_011_O"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3011OTests(unittest.TestCase):
    def test_contract_binds_exact_octants_and_boundaries(self) -> None:
        contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["issue"], 931)
        self.assertEqual(contract["operation"], producer.OPERATION)
        self.assertEqual(contract["predecessor"]["reviewed_head"], producer.N_REVIEWED_HEAD)
        self.assertEqual(contract["predecessor"]["merge_commit"], producer.N_MERGE_COMMIT)
        self.assertEqual(contract["predecessor"]["required_terminal"], producer.N_REQUIRED_TERMINAL)
        scope = contract["active_spectator_double_reciprocal_trivariate_class"]
        self.assertEqual(scope["reciprocal_active_axis_count"], 1)
        self.assertTrue(scope["reciprocal_spectator"])
        self.assertFalse(scope["all_reciprocal_trivariate_octant_authorized"])
        self.assertTrue(scope["spectator_reciprocal_degree_zero_boundary_must_match_protected_M"])
        self.assertTrue(scope["reciprocal_active_degree_zero_boundary_must_match_protected_L"])
        self.assertTrue(scope["positive_active_degree_zero_is_direct_response_anchor_only"])
        self.assertEqual(
            contract["boundary_predecessors"]["positive_active_degree_zero"]["anchor"],
            "DIRECT_RESPONSE_ONLY_NOT_T3_011_I",
        )

    def test_scope_rejects_every_extra_or_missing_widening(self) -> None:
        mutations = (
            {"reciprocal_active_axes": 0},
            {"reciprocal_active_axes": 2},
            {"reciprocal_spectator": False},
            {"all_reciprocal_trivariate": True},
            {"shifted_spectator": True},
            {"shifted_poles": True},
            {"arbitrary_rational_functions": True},
            {"support_or_harmonic_enlargement": True},
            {"candidate_bank_or_scalar_namespace_widening": True},
            {"recurrence_widening": True},
            {"correction_recombination": True},
            {"candidate_linear_combinations": True},
            {"third_finite_difference_operator": True},
            {"arbitrary_degree_cutoff": 1},
        )
        for kwargs in mutations:
            with self.assertRaises(AssertionError):
                producer.validate_scope(**kwargs)

    def test_exact_signed_solver_handles_o_octant(self) -> None:
        case = (
            (),
            (("a", -1),),
            (("b", 1),),
            (("e", -1),),
            (("a", -1), ("b", 2), ("e", -3)),
        )
        expected = ("finite", ((1, 2, 3),), None, None)
        self.assertEqual(producer.solve_signed_tridegrees(*case), expected)
        self.assertEqual(verifier.independent_solve(*case), expected)

    def test_exact_solvers_detect_support_feasible_recession(self) -> None:
        case = (
            (),
            (("a", -1),),
            (("b", 1),),
            (("b", -1),),
            (("a", -1),),
        )
        p = producer.solve_signed_tridegrees(*case)
        v = verifier.independent_solve(*case)
        self.assertEqual(p, v)
        status, rows, seed, ray = p
        self.assertEqual(status, "unbounded")
        self.assertEqual(rows, ())
        self.assertIsNotNone(seed)
        self.assertIsNotNone(ray)
        self.assertGreaterEqual(min(seed), 1)
        self.assertTrue(producer._solution_matches(*case[:-1], case[-1], seed))
        self.assertTrue(producer._ray_matches(case[1], case[2], case[3], ray))

    def test_producer_and_independent_verifier_pin_empty_overlap_closure(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)

        self.assertEqual(result["terminal"], producer.CLOSURE_TERMINAL)
        self.assertEqual(replay["terminal"], producer.CLOSURE_TERMINAL)
        self.assertEqual(result["possible_record_count"], 2564)
        self.assertEqual(result["tested_record_count"], 2564)
        self.assertEqual(replay["possible_record_count"], 2564)
        self.assertEqual(replay["tested_record_count"], 2564)
        self.assertEqual(result["domain_analysis"]["support_signature_pairs_inspected"], 0)
        self.assertEqual(replay["support_signature_pairs_inspected"], 0)
        self.assertTrue(replay["finite_solver_uses_signature_derived_bounds_only"])
        self.assertFalse(replay["arbitrary_degree_cutoff_used"])
        self.assertIsNone(result["characterized_blocker"])
        self.assertIsNone(result["semantic_functional_ambiguity"])
        self.assertIsNone(result["first_cokernel_breaking_direction"])
        self.assertTrue(
            result["all_active_spectator_double_reciprocal_trivariate_responses_cokernel_invisible"]
        )
        self.assertTrue(
            replay["all_active_spectator_double_reciprocal_trivariate_responses_cokernel_invisible"]
        )

        for record in result["tested_records"]:
            self.assertEqual(record["finite_overlap_tridegrees"], [])
            self.assertEqual(record["pairing_rows"], [])
            self.assertEqual(record["nonzero_pairings"], [])
            self.assertTrue(record["spectator_reciprocal_degree_zero_semantics_exactly_match_M"])
            self.assertTrue(record["reciprocal_active_degree_zero_semantics_exactly_match_L"])
            self.assertEqual(
                record["positive_active_degree_zero_anchor_kind"],
                "DIRECT_RESPONSE_ONLY_NOT_T3_011_I",
            )

        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        print(
            "T3_011_O_RESULT "
            + json.dumps(
                {
                    "terminal": result["terminal"],
                    "possible_record_count": result["possible_record_count"],
                    "tested_record_count": result["tested_record_count"],
                    "support_signature_pairs_inspected": replay[
                        "support_signature_pairs_inspected"
                    ],
                    "characterized_blocker": result["characterized_blocker"],
                    "semantic_functional_ambiguity": result[
                        "semantic_functional_ambiguity"
                    ],
                    "first_cokernel_breaking_direction": result[
                        "first_cokernel_breaking_direction"
                    ],
                    "all_active_spectator_double_reciprocal_trivariate_responses_cokernel_invisible": result[
                        "all_active_spectator_double_reciprocal_trivariate_responses_cokernel_invisible"
                    ],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
