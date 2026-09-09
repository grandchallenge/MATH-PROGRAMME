from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_012_A"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier

class OzRtBzT3012ATests(unittest.TestCase):
    def test_scope_rejects_old_or_broader_mechanisms(self) -> None:
        mutations = (
            {"recurrence_order": 4},
            {"max_polynomial_degree": 10},
            {"rational_coefficient_family": True},
            {"recurrence_fitting": True},
            {"multiplier_widening": True},
            {"support_or_harmonic_widening": True},
            {"correction_recombination": True},
            {"theorem_promotion": True},
        )
        for kwargs in mutations:
            with self.assertRaises(AssertionError):
                producer.validate_scope(**kwargs)

    def test_fixed_operator_tangent_obstruction_is_nonzero(self) -> None:
        self.assertEqual(
            [producer.yhk(n) for n in range(4)],
            [producer.Q(0), producer.Q(16), producer.Q(3564), producer.Q(3214312, 3)],
        )
        self.assertEqual(
            producer.fixed_tangent_residual(0),
            producer.Q(producer.FIXED_OBSTRUCTION),
        )
        self.assertNotEqual(producer.fixed_tangent_residual(0), 0)

    def test_reconstructed_base_sequence_satisfies_operator_on_all_gate_rows(self) -> None:
        for n in range(producer.row_count(9)):
            c = producer.recurrence_coefficients(n)
            self.assertEqual(sum(c[j] * producer.y0(n+j) for j in range(4)), 0)
            vc = verifier._coeffs(n)
            self.assertEqual(sum(vc[j] * verifier._sequences(n+j)[0] for j in range(4)), 0)

    def test_gauge_normalized_column_counts(self) -> None:
        for degree in range(9):
            self.assertEqual(len(producer.stage_columns(degree)), 4*(degree+1))
        columns = producer.stage_columns(9)
        self.assertEqual(len(columns), 39)
        self.assertNotIn((3, 9), columns)
        self.assertIn((0, 9), columns)
        self.assertIn((1, 9), columns)
        self.assertIn((2, 9), columns)

    def test_all_declared_operator_tangent_stages_are_exactly_inconsistent(self) -> None:
        result = producer.build()
        self.assertEqual(result["terminal"], producer.CLOSURE_TERMINAL)
        self.assertIsNone(result["characterized_blocker"])
        self.assertEqual(len(result["stages"]), 10)
        for degree, stage in enumerate(result["stages"]):
            self.assertEqual(stage["degree"], degree)
            self.assertEqual(stage["row_count"], stage["unknown_count"] + producer.EXTRA_ROWS)
            self.assertEqual(stage["coefficient_rank_mod_prime"], stage["unknown_count"])
            self.assertEqual(stage["augmented_rank_mod_prime"], stage["unknown_count"] + 1)
            self.assertTrue(stage["exact_inconsistency_over_Q_certified"])
            self.assertEqual(
                stage["rational_denominator_nonzero_mod_prime_checks"],
                stage["row_count"],
            )
        self.assertEqual(result["stages"][-1]["unknown_count"], 39)
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")

    def test_independent_verifier_reconstructs_exact_negative(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)
        self.assertEqual(replay["terminal"], result["terminal"])
        self.assertEqual(replay["degree9_unknown_count"], 39)
        self.assertEqual(replay["degree9_coefficient_rank_mod_prime"], 39)
        self.assertEqual(replay["degree9_augmented_rank_mod_prime"], 40)
        self.assertTrue(replay["all_declared_stages_exactly_inconsistent_over_Q"])
        self.assertFalse(replay["residual_sum_zero_proved"])
        print(
            "T3_012_A_RESULT "
            + json.dumps(
                {
                    "terminal": result["terminal"],
                    "degree9_unknown_count": 39,
                    "degree9_coefficient_rank": 39,
                    "degree9_augmented_rank": 40,
                    "fixed_operator_tangent_obstruction_at_n0":
                        result["fixed_operator_tangent_obstruction_at_n0"],
                    "proof_effect": result["proof_effect"],
                    "promotion_effect": result["promotion_effect"],
                    "t3_status": result["t3_status"],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )

if __name__ == "__main__":
    unittest.main()
