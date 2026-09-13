from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_014"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3014Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = producer.build()
        cls.replay = verifier.verify(cls.evidence)

    def test_source_declares_rational_delta_pivot_exactly(self) -> None:
        locks = self.evidence["source_declaration_locks"]
        self.assertEqual(
            locks["work/Z5T3_BRIDGE.md"]["git_blob_sha1"],
            "002c96d28123e5949c38656f26677ae5a723ee93",
        )
        self.assertEqual(
            locks["work/Z5CF_LINALG.md"]["git_blob_sha1"],
            "637ecaa7f3ee941a87932de390eb7336d7fde677",
        )
        self.assertEqual(
            self.evidence["gate"]["source_qrow"]["git_blob_sha1"],
            "61f12f412726887f506e1d423b7ee183a22116e5",
        )

    def test_predecessor_and_target_are_replayed_without_drift(self) -> None:
        gate = self.evidence["gate"]
        self.assertEqual(gate["samples"], [[8, 1, 2], [9, 2, 1]])
        self.assertTrue(gate["sample_set_inherited_exactly_from_t3_012_b"])
        self.assertEqual(gate["protected_base_unknown_count"], 506)
        self.assertEqual(gate["value_jet_unknown_count"], 2024)
        self.assertEqual(gate["target_coordinate_count"], 298)
        self.assertEqual(
            gate["predecessor_t3_013_a_terminal"],
            "QROW_CERTIFICATE_WEIGHTED_STRICT_INTERIOR_SUBSYSTEM_INCONSISTENT",
        )
        self.assertEqual(gate["embedded_t3_012_b_coefficient_rank"], 84)
        self.assertEqual(gate["embedded_t3_012_b_augmented_rank"], 85)

    def test_gate_has_no_hidden_degree_or_denominator_cutoff(self) -> None:
        gate = self.evidence["gate"]
        self.assertEqual(gate["coefficient_field"], "Q(n,k,l)")
        self.assertTrue(gate["finite_value_assignment_realizable_by_polynomial_interpolation"])
        self.assertTrue(gate["finite_value_jet_is_exact_restriction_not_relaxation"])
        self.assertIsNone(gate["rational_degree_cutoff"])
        self.assertIsNone(gate["denominator_cutoff"])

    def test_independent_rational_value_jet_replay_matches(self) -> None:
        self.assertTrue(self.replay["independent_rational_value_jet_replay_complete"])
        self.assertFalse(self.replay["producer_value_jet_matrix_imported_as_authority"])
        self.assertFalse(self.replay["producer_rank_result_imported_as_authority"])
        got = self.replay["gate"]
        expected = self.evidence["gate"]
        for field in (
            "coefficient_rank",
            "augmented_rank",
            "consistent",
            "nullity",
            "nonzero_value_jet_column_count",
            "unknown_identity_sha256",
            "target_sha256",
        ):
            self.assertEqual(got[field], expected[field])

    def test_terminal_tracks_exact_rank_result_and_claims_fail_closed(self) -> None:
        gate = self.evidence["gate"]
        if gate["consistent"]:
            self.assertEqual(
                self.evidence["terminal"],
                "RATIONAL_DELTA_LOCAL_JET_PREDECESSOR_OBSTRUCTION_ESCAPED__GLOBAL_RATIONAL_CERTIFICATE_REQUIRED",
            )
        else:
            self.assertEqual(
                self.evidence["terminal"],
                "RATIONAL_DELTA_CLASS_REFUTED_AT_INHERITED_NECESSARY_SUBSYSTEM",
            )
        self.assertFalse(self.evidence["global_certificate_constructed"])
        self.assertFalse(self.evidence["residual_sum_zero_proved"])
        self.assertEqual(self.evidence["proof_effect"], "NONE")
        self.assertEqual(self.evidence["promotion_effect"], "NONE")
        self.assertEqual(self.evidence["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_emit_result(self) -> None:
        gate = self.evidence["gate"]
        print(
            "T3_014_RESULT "
            + json.dumps(
                {
                    "terminal": self.evidence["terminal"],
                    "samples": gate["samples"],
                    "protected_base_unknown_count": gate["protected_base_unknown_count"],
                    "value_jet_unknown_count": gate["value_jet_unknown_count"],
                    "target_coordinate_count": gate["target_coordinate_count"],
                    "predecessor_t3_013_a_rank": [
                        gate["predecessor_t3_013_a_coefficient_rank"],
                        gate["predecessor_t3_013_a_augmented_rank"],
                    ],
                    "embedded_t3_012_b_rank": [
                        gate["embedded_t3_012_b_coefficient_rank"],
                        gate["embedded_t3_012_b_augmented_rank"],
                    ],
                    "rational_value_jet_rank": [gate["coefficient_rank"], gate["augmented_rank"]],
                    "consistent": gate["consistent"],
                    "nullity": gate["nullity"],
                    "independent_rational_value_jet_replay_complete": self.replay[
                        "independent_rational_value_jet_replay_complete"
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
