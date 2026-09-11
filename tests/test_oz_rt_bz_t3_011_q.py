from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_011_Q"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3011QTests(unittest.TestCase):
    def test_contract_binds_only_protected_active_zero_faces(self) -> None:
        contract = json.loads((HERE / "CONTRACT.json").read_text())
        self.assertEqual(contract["issue"], 939)
        self.assertEqual(contract["operation"], producer.OPERATION)
        self.assertEqual(contract["protected_base"], producer.PROTECTED_BASE)
        self.assertEqual(contract["predecessor"]["required_terminal"], producer.p.CLOSURE_TERMINAL)
        self.assertEqual(contract["partition"]["one_active_exponent_zero"]["sign_families"], ["++", "-+", "+-", "--"])
        self.assertTrue(contract["partition"]["not_claimed_by_Q"]["both_active_exponents_zero_with_nonzero_spectator"])

    def test_scope_rejects_every_widening(self) -> None:
        mutations = (
            {"shifted_poles": True},
            {"arbitrary_rational_functions": True},
            {"support_or_harmonic_enlargement": True},
            {"candidate_bank_or_scalar_namespace_widening": True},
            {"recurrence_widening": True},
            {"correction_recombination": True},
            {"candidate_linear_combinations": True},
            {"third_finite_difference_operator": True},
            {"source_or_representative_substitution": True},
            {"arbitrary_degree_cutoff": 1},
        )
        for kwargs in mutations:
            with self.assertRaises(AssertionError):
                producer.validate_scope(**kwargs)

    def test_producer_and_independent_verifier_close_or_bind_first_face_escape(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)

        self.assertEqual(result["terminal"], replay["terminal"])
        self.assertEqual(
            result["active_zero_face_partition"]["first_nonzero"],
            replay["first_nonzero"],
        )
        self.assertEqual(
            result["active_zero_face_partition"]["all_one_active_zero_sign_families_annihilated"],
            replay["all_one_active_zero_sign_families_annihilated"],
        )
        self.assertIn(result["terminal"], (producer.ESCAPE_TERMINAL, producer.CLOSURE_TERMINAL))

        if result["terminal"] == producer.ESCAPE_TERMINAL:
            self.assertIsNotNone(result["active_zero_face_partition"]["first_nonzero"])
            self.assertIsNone(result["remaining_lower_dimensional_seam"])
        else:
            self.assertIsNone(result["active_zero_face_partition"]["first_nonzero"])
            self.assertEqual(result["remaining_lower_dimensional_seam"], producer.REMAINING_SEAM)

        self.assertIsNone(result["full_coordinate_zero_laurent_algebra_corollary"])
        self.assertFalse(result["full_coordinate_zero_laurent_algebra_closed"])
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        print(
            "T3_011_Q_RESULT "
            + json.dumps(
                {
                    "terminal": result["terminal"],
                    "first_nonzero": result["active_zero_face_partition"]["first_nonzero"],
                    "all_one_active_zero_sign_families_annihilated": result["active_zero_face_partition"]["all_one_active_zero_sign_families_annihilated"],
                    "remaining_lower_dimensional_seam": result["remaining_lower_dimensional_seam"],
                    "face_families": result["active_zero_face_partition"]["families"],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
