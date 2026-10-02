from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_013_A"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3013ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = producer.build()
        cls.replay = verifier.verify(cls.evidence)

    def test_current_admitted_source_is_bound_exactly(self) -> None:
        gate = self.evidence["gate"]
        self.assertEqual(gate["source"]["commit"], "6cc0bf07137815ceeef0d9f340559f85352391e5")
        self.assertEqual(gate["source"]["git_blob_sha1"], "61f12f412726887f506e1d423b7ee183a22116e5")
        self.assertEqual(gate["source"]["byte_count"], 44980)
        self.assertTrue(gate["qrow_point_replay"])
        self.assertTrue(gate["source_nonmonomial_rational_denominator_detected"])

    def test_predecessor_obstruction_is_embedded_without_target_drift(self) -> None:
        gate = self.evidence["gate"]
        self.assertEqual(gate["coefficient_basis"], ["one", "rho", "sigma"])
        self.assertEqual(gate["samples"], [[8, 1, 2], [9, 2, 1]])
        self.assertTrue(gate["sample_set_inherited_exactly_from_t3_012_b"])
        self.assertEqual(gate["protected_base_unknown_count"], 506)
        self.assertEqual(gate["weighted_unknown_count"], 1518)
        self.assertEqual(gate["target_coordinate_count"], 298)
        self.assertEqual(gate["embedded_predecessor_coefficient_rank"], 84)
        self.assertEqual(gate["embedded_predecessor_augmented_rank"], 85)

    def test_independent_weighted_replay_matches(self) -> None:
        self.assertTrue(self.replay["independent_source_weighted_replay_complete"])
        self.assertFalse(self.replay["producer_weighted_matrix_imported_as_authority"])
        self.assertFalse(self.replay["producer_source_evaluator_imported_as_authority"])
        got = self.replay["gate"]
        expected = self.evidence["gate"]
        for field in (
            "coefficient_rank",
            "augmented_rank",
            "consistent",
            "nullity",
            "nonzero_weighted_column_count",
        ):
            self.assertEqual(got[field], expected[field])

    def test_terminal_tracks_exact_rank_result_and_claims_fail_closed(self) -> None:
        gate = self.evidence["gate"]
        if gate["consistent"]:
            self.assertEqual(
                self.evidence["terminal"],
                "QROW_CERTIFICATE_WEIGHTED_PREDECESSOR_OBSTRUCTION_ESCAPED__GLOBAL_CERTIFICATE_REQUIRED",
            )
        else:
            self.assertEqual(
                self.evidence["terminal"],
                "QROW_CERTIFICATE_WEIGHTED_STRICT_INTERIOR_SUBSYSTEM_INCONSISTENT",
            )
        self.assertFalse(self.evidence["global_certificate_constructed"])
        self.assertFalse(self.evidence["residual_sum_zero_proved"])
        self.assertEqual(self.evidence["proof_effect"], "NONE")
        self.assertEqual(self.evidence["promotion_effect"], "NONE")
        self.assertEqual(self.evidence["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_emit_result(self) -> None:
        gate = self.evidence["gate"]
        print(
            "T3_013_A_RESULT "
            + json.dumps(
                {
                    "terminal": self.evidence["terminal"],
                    "source_commit": gate["source"]["commit"],
                    "source_blob": gate["source"]["git_blob_sha1"],
                    "coefficient_basis": gate["coefficient_basis"],
                    "samples": gate["samples"],
                    "protected_base_unknown_count": gate["protected_base_unknown_count"],
                    "weighted_unknown_count": gate["weighted_unknown_count"],
                    "target_coordinate_count": gate["target_coordinate_count"],
                    "embedded_predecessor_rank": [
                        gate["embedded_predecessor_coefficient_rank"],
                        gate["embedded_predecessor_augmented_rank"],
                    ],
                    "weighted_rank": [gate["coefficient_rank"], gate["augmented_rank"]],
                    "consistent": gate["consistent"],
                    "nullity": gate["nullity"],
                    "independent_source_weighted_replay_complete": self.replay[
                        "independent_source_weighted_replay_complete"
                    ],
                    "residual_sum_zero_proved": self.evidence["residual_sum_zero_proved"],
                    "proof_effect": self.evidence["proof_effect"],
                    "promotion_effect": self.evidence["promotion_effect"],
                    "t3_status": self.evidence["t3_status"],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
