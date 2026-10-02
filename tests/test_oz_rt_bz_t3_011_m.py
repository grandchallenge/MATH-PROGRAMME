from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_011_M"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3011MTests(unittest.TestCase):
    def test_scope_rejects_every_extra_widening(self) -> None:
        mutations = (
            {"reciprocal_active_axes": 0},
            {"reciprocal_active_axes": 2},
            {"reciprocal_spectator": True},
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

    def test_exact_signed_solver_finite_octant(self) -> None:
        status, rows, seed, ray = producer.solve_signed_tridegrees(
            (),
            (("a", -1),),
            (("b", 1),),
            (("e", 1),),
            (("a", -1), ("b", 1), ("e", 1)),
        )
        self.assertEqual(status, "finite")
        self.assertEqual(rows, ((1, 1, 1),))
        self.assertIsNone(seed)
        self.assertIsNone(ray)

    def test_exact_signed_solver_detects_support_recession(self) -> None:
        status, rows, seed, ray = producer.solve_signed_tridegrees(
            (),
            (("a", -1),),
            (("b", 1),),
            (("a", 1),),
            (("b", 1),),
        )
        self.assertEqual(status, "unbounded")
        self.assertEqual(rows, ())
        self.assertIsNotNone(seed)
        self.assertIsNotNone(ray)
        self.assertGreaterEqual(min(seed), 1)
        self.assertTrue(producer._solution_matches(
            (), (("a", -1),), (("b", 1),), (("a", 1),), (("b", 1),), seed
        ))
        self.assertTrue(producer._ray_matches(
            (("a", -1),), (("b", 1),), (("a", 1),), ray
        ))

    def test_independent_solver_agrees_on_finite_and_unbounded_examples(self) -> None:
        cases = (
            (
                (), (("a", -1),), (("b", 1),), (("e", 1),),
                (("a", -1), ("b", 2), ("e", 3)),
            ),
            (
                (), (("a", -1),), (("b", 1),), (("a", 1),),
                (("b", 1),),
            ),
            (
                (("a", 2),), (("a", -1),), (("b", 1),), (("e", 1),),
                (("a", 1), ("b", 1), ("e", 1)),
            ),
        )
        for case in cases:
            self.assertEqual(
                producer.solve_signed_tridegrees(*case),
                verifier.independent_solve(*case),
            )

    def test_producer_and_independent_verifier_agree_on_exact_terminal(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)
        allowed = {
            producer.ESCAPE_TERMINAL,
            producer.CLOSURE_TERMINAL,
            producer.AMBIGUITY_TERMINAL,
            producer.BLOCKER_TERMINAL,
        }

        self.assertIn(result["terminal"], allowed)
        self.assertEqual(replay["terminal"], result["terminal"])
        self.assertEqual(result["possible_record_count"], producer.POSSIBLE_RECORD_COUNT)
        self.assertEqual(replay["possible_record_count"], producer.POSSIBLE_RECORD_COUNT)
        self.assertEqual(replay["tested_record_count"], result["tested_record_count"])
        self.assertTrue(replay["finite_solver_uses_signature_derived_bounds_only"])
        self.assertFalse(replay["arbitrary_degree_cutoff_used"])

        if result["terminal"] == producer.CLOSURE_TERMINAL:
            self.assertEqual(result["tested_record_count"], producer.POSSIBLE_RECORD_COUNT)
            self.assertIsNone(result["characterized_blocker"])
            self.assertIsNone(result["semantic_functional_ambiguity"])
            self.assertIsNone(result["first_cokernel_breaking_direction"])
            self.assertTrue(result[
                "all_single_reciprocal_active_trivariate_responses_cokernel_invisible"
            ])
        elif result["terminal"] == producer.BLOCKER_TERMINAL:
            self.assertIsNotNone(result["characterized_blocker"])
            self.assertEqual(replay["characterized_blocker"], result["characterized_blocker"])
        elif result["terminal"] == producer.AMBIGUITY_TERMINAL:
            self.assertIsNotNone(result["semantic_functional_ambiguity"])
            self.assertIsNotNone(replay["semantic_functional_ambiguity"])
        elif result["terminal"] == producer.ESCAPE_TERMINAL:
            self.assertIsNotNone(result["first_cokernel_breaking_direction"])
            self.assertIsNotNone(replay["first_cokernel_breaking_direction"])

        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        print(
            "T3_011_M_RESULT "
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
                    "all_single_reciprocal_active_trivariate_responses_cokernel_invisible": result[
                        "all_single_reciprocal_active_trivariate_responses_cokernel_invisible"
                    ],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
