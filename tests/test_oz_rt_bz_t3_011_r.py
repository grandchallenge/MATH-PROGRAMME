from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_011_R"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3011RTests(unittest.TestCase):
    def test_contract_binds_only_protected_spectator_axis(self) -> None:
        contract = json.loads((HERE / "CONTRACT.json").read_text())
        self.assertEqual(contract["issue"], 944)
        self.assertEqual(contract["operation"], producer.OPERATION)
        self.assertEqual(contract["protected_base"], producer.PROTECTED_BASE)
        self.assertEqual(
            contract["predecessor"]["required_terminal"],
            producer.Q_REQUIRED_TERMINAL,
        )
        self.assertEqual(
            contract["predecessor"]["required_remaining_seam"],
            producer.Q_REQUIRED_REMAINING_SEAM,
        )
        self.assertEqual(
            contract["spectator_only_axis"]["positive_parent_paths"],
            list(producer.POSITIVE_PATHS),
        )
        self.assertEqual(
            contract["spectator_only_axis"]["reciprocal_parent_paths"],
            list(producer.RECIPROCAL_PATHS),
        )

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

    def test_producer_and_independent_verifier_agree_exactly(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)

        self.assertEqual(result["terminal"], replay["terminal"])
        self.assertEqual(
            result["spectator_only_axis_audit"]["first_nonzero"],
            replay["first_nonzero"],
        )
        self.assertEqual(
            result["spectator_only_axis_audit"]["semantic_path_ambiguity"],
            replay["semantic_path_ambiguity"],
        )
        self.assertEqual(
            result["spectator_only_axis_audit"]["characterized_blocker"],
            replay["characterized_blocker"],
        )
        self.assertEqual(
            result["spectator_only_axis_audit"]["coverage_complete"],
            replay["coverage_complete"],
        )
        self.assertIn(
            result["terminal"],
            (
                producer.ESCAPE_TERMINAL,
                producer.CLOSURE_TERMINAL,
                producer.AMBIGUITY_TERMINAL,
                producer.BLOCKER_TERMINAL,
            ),
        )

        if result["terminal"] == producer.CLOSURE_TERMINAL:
            self.assertTrue(
                result["spectator_only_axis_audit"]["all_parent_paths_agree"]
            )
            self.assertTrue(
                result["spectator_only_axis_audit"][
                    "all_spectator_only_responses_annihilated"
                ]
            )
            self.assertTrue(result["full_coordinate_zero_laurent_algebra_closed"])
            self.assertEqual(
                result["full_coordinate_zero_laurent_algebra_corollary"],
                producer.FULL_ALGEBRA_COROLLARY,
            )
            for sign in producer.SIGNS:
                self.assertEqual(
                    result["spectator_only_axis_audit"]["signs"][sign][
                        "record_count"
                    ],
                    producer.EXPECTED_RECORDS_PER_SIGN,
                )
        else:
            self.assertFalse(result["full_coordinate_zero_laurent_algebra_closed"])
            self.assertIsNone(
                result["full_coordinate_zero_laurent_algebra_corollary"]
            )

        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

        print(
            "T3_011_R_RESULT "
            + json.dumps(
                {
                    "terminal": result["terminal"],
                    "expected_records_per_sign":
                        result["spectator_only_axis_audit"][
                            "expected_records_per_sign"
                        ],
                    "signs": {
                        sign: {
                            "record_count": data["record_count"],
                            "row_count": data["row_count"],
                            "record_sha256": data["record_sha256"],
                            "all_paths_agree": data["all_paths_agree"],
                        }
                        for sign, data
                        in result["spectator_only_axis_audit"]["signs"].items()
                    },
                    "first_nonzero":
                        result["spectator_only_axis_audit"]["first_nonzero"],
                    "semantic_path_ambiguity":
                        result["spectator_only_axis_audit"][
                            "semantic_path_ambiguity"
                        ],
                    "characterized_blocker":
                        result["spectator_only_axis_audit"][
                            "characterized_blocker"
                        ],
                    "full_coordinate_zero_laurent_algebra_corollary":
                        result["full_coordinate_zero_laurent_algebra_corollary"],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
