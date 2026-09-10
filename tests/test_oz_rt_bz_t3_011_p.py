from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_011_P"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3011PTests(unittest.TestCase):
    def test_contract_binds_only_final_laurent_octant(self) -> None:
        contract = json.loads((HERE / "CONTRACT.json").read_text(encoding="utf-8"))
        self.assertEqual(contract["issue"], 934)
        self.assertEqual(contract["operation"], producer.OPERATION)
        self.assertEqual(contract["predecessor"]["reviewed_head"], producer.O_REVIEWED_HEAD)
        self.assertEqual(contract["predecessor"]["merge_commit"], producer.O_MERGE_COMMIT)
        self.assertEqual(contract["predecessor"]["required_terminal"], producer.O_REQUIRED_TERMINAL)
        scope = contract["all_reciprocal_trivariate_class"]
        self.assertEqual(scope["reciprocal_active_axis_count"], 2)
        self.assertTrue(scope["reciprocal_spectator"])
        self.assertTrue(scope["all_reciprocal_trivariate_octant_authorized"])
        self.assertTrue(scope["spectator_reciprocal_degree_zero_boundary_must_match_protected_I"])
        self.assertTrue(scope["active_reciprocal_degree_zero_faces_are_direct_response_anchors_only"])
        self.assertEqual(
            contract["boundary_predecessors"]["active_reciprocal_degree_zero_faces"]["anchor"],
            "DIRECT_RESPONSE_ONLY_NO_PREDECESSOR_CLASS_PROMOTION",
        )

    def test_scope_rejects_every_extra_or_missing_widening(self) -> None:
        mutations = (
            {"reciprocal_active_axes": 0},
            {"reciprocal_active_axes": 1},
            {"reciprocal_spectator": False},
            {"all_reciprocal_trivariate": False},
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

    def test_exact_signed_solvers_handle_all_reciprocal_octant(self) -> None:
        case = (
            (),
            (("a", -1),),
            (("b", -1),),
            (("e", -1),),
            (("a", -2), ("b", -3), ("e", -4)),
        )
        expected = ("finite", ((2, 3, 4),), None, None)
        self.assertEqual(producer.solve_signed_tridegrees(*case), expected)
        self.assertEqual(verifier.independent_solve(*case), expected)

    def test_exact_solvers_detect_support_feasible_recession(self) -> None:
        case = (
            (),
            (("a", -1),),
            (("a", 1),),
            (("e", -1),),
            (("e", -1),),
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

    def test_producer_and_independent_verifier_replay_exact_class(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)

        admissible = {
            producer.ESCAPE_TERMINAL,
            producer.CLOSURE_TERMINAL,
            producer.AMBIGUITY_TERMINAL,
            producer.BLOCKER_TERMINAL,
        }
        self.assertIn(result["terminal"], admissible)
        self.assertEqual(replay["terminal"], result["terminal"])
        self.assertEqual(result["possible_record_count"], 1282)
        self.assertEqual(replay["possible_record_count"], 1282)
        self.assertEqual(replay["tested_record_count"], result["tested_record_count"])
        self.assertEqual(
            replay["support_signature_pairs_inspected"],
            result["domain_analysis"]["support_signature_pairs_inspected"],
        )
        self.assertTrue(replay["finite_solver_uses_signature_derived_bounds_only"])
        self.assertFalse(replay["arbitrary_degree_cutoff_used"])

        if result["terminal"] == producer.CLOSURE_TERMINAL:
            self.assertEqual(result["tested_record_count"], 1282)
            self.assertIsNone(result["characterized_blocker"])
            self.assertIsNone(result["semantic_functional_ambiguity"])
            self.assertIsNone(result["first_cokernel_breaking_direction"])
            self.assertTrue(result["all_all_reciprocal_trivariate_responses_cokernel_invisible"])
            self.assertTrue(replay["all_all_reciprocal_trivariate_responses_cokernel_invisible"])
            for record in result["tested_records"]:
                self.assertTrue(record["spectator_reciprocal_degree_zero_semantics_exactly_match_I"])
                self.assertEqual(
                    record["active_reciprocal_degree_zero_anchor_kind"],
                    "DIRECT_RESPONSE_ONLY_NO_PREDECESSOR_CLASS_PROMOTION",
                )

        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        print(
            "T3_011_P_RESULT "
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
                    "all_all_reciprocal_trivariate_responses_cokernel_invisible": result[
                        "all_all_reciprocal_trivariate_responses_cokernel_invisible"
                    ],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
