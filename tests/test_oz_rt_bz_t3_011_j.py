from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_011_J"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3011JTests(unittest.TestCase):
    def test_scope_rejects_widening(self) -> None:
        for kwargs in (
            {"shifted_poles": True},
            {"arbitrary_rational_functions": True},
            {"support_or_harmonic_enlargement": True},
            {"candidate_bank_or_scalar_namespace_widening": True},
            {"recurrence_widening": True},
            {"correction_recombination": True},
            {"candidate_linear_combinations": True},
            {"trivariate_spectator_multipliers": True},
        ):
            with self.assertRaises(AssertionError):
                producer.validate_scope(**kwargs)

    def test_signed_solver_distinguishes_finite_and_unbounded(self) -> None:
        finite = producer._solve_mixed_sign_bidegrees(
            (), (("a", 1),), (("b", -1),), (("a", 2), ("b", -3))
        )
        self.assertEqual(finite, ("finite", ((2, 3),)))
        finite_independent = verifier._independent_mixed_sign_solutions(
            (), (("a", 1),), (("b", -1),), (("a", 2), ("b", -3))
        )
        self.assertEqual(finite_independent, finite)

        unbounded = producer._solve_mixed_sign_bidegrees(
            (), (("a", 1),), (("a", -1),), ()
        )
        independent = verifier._independent_mixed_sign_solutions(
            (), (("a", 1),), (("a", -1),), ()
        )
        self.assertEqual(unbounded[0], "unbounded")
        self.assertEqual(independent, unbounded)
        base_degree, direction = unbounded[1]
        self.assertEqual(
            producer._combine_sig(
                (), (("a", 1),), (("a", -1),), *base_degree
            ),
            (),
        )
        next_degree = (
            base_degree[0] + direction[0],
            base_degree[1] + direction[1],
        )
        self.assertGreaterEqual(next_degree[0], 1)
        self.assertGreaterEqual(next_degree[1], 1)
        self.assertEqual(
            producer._combine_sig(
                (), (("a", 1),), (("a", -1),), *next_degree
            ),
            (),
        )

    def test_producer_and_independent_verifier(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)

        self.assertEqual(replay["terminal"], result["terminal"])
        self.assertIn(
            result["terminal"],
            {
                producer.ESCAPE_TERMINAL,
                producer.CLOSURE_TERMINAL,
                producer.AMBIGUITY_TERMINAL,
                producer.UNBOUNDED_TERMINAL,
                producer.BLOCKER_TERMINAL,
            },
        )
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        if result["terminal"] == producer.ESCAPE_TERMINAL:
            self.assertIsNotNone(result["first_cokernel_breaking_direction"])
            self.assertFalse(
                result["all_mixed_sign_laurent_responses_cokernel_invisible"]
            )
            self.assertIsNone(result["semantic_functional_ambiguity"])
        elif result["terminal"] == producer.CLOSURE_TERMINAL:
            self.assertIsNone(result["first_cokernel_breaking_direction"])
            self.assertIsNone(result["characterized_blocker"])
            self.assertTrue(
                result["all_mixed_sign_laurent_responses_cokernel_invisible"]
            )
            self.assertEqual(
                result["tested_record_count"], result["possible_record_count"]
            )
        elif result["terminal"] == producer.AMBIGUITY_TERMINAL:
            self.assertIsNotNone(result["semantic_functional_ambiguity"])
        elif result["terminal"] == producer.UNBOUNDED_TERMINAL:
            self.assertIsNotNone(result["characterized_blocker"])
            self.assertTrue(
                result["characterized_blocker"]["mixed_admissible_family_exists"]
            )
            self.assertFalse(
                result["all_mixed_sign_laurent_responses_cokernel_invisible"]
            )
        else:
            self.assertTrue(result["characterized_blocker"])

        print(
            "T3_011_J_RESULT "
            + json.dumps(
                {
                    "terminal": result["terminal"],
                    "possible_record_count": result["possible_record_count"],
                    "tested_record_count": result["tested_record_count"],
                    "semantic_functional_ambiguity": result[
                        "semantic_functional_ambiguity"
                    ],
                    "first_cokernel_breaking_direction": result[
                        "first_cokernel_breaking_direction"
                    ],
                    "characterized_blocker": result.get("characterized_blocker"),
                    "all_mixed_sign_laurent_responses_cokernel_invisible": result[
                        "all_mixed_sign_laurent_responses_cokernel_invisible"
                    ],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
