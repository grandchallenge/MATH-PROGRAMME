from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

# The pinned 44,980-byte Q-row expression is a deeply left-associated arithmetic
# tree. Both independent evaluators intentionally traverse that exact parsed
# tree; increase only the interpreter stack ceiling so the source shape, rather
# than Python's default recursion limit, controls the replay.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_012_B"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import terminal
import verifier


class OzRtBzT3012BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = producer.build()
        cls.replay = verifier.verify(cls.evidence)
        cls.result = terminal.build()

    def test_protected_c_negative_frontier_is_reconstructed(self) -> None:
        expected = {
            "n1": (116, 67, 68),
            "n2": (116, 67, 68),
            "n3": (116, 67, 68),
            "k1": (158, 110, 111),
        }
        for channel, triple in expected.items():
            row = self.evidence["protected_c_channel_ranks"][channel]
            self.assertEqual(
                (row["unknown_count"], row["coefficient_rank"], row["augmented_rank"]),
                triple,
            )

    def test_diagnostic_projection_defect_survives_all_quotients(self) -> None:
        expected = {
            "erase_partition_only": (311, 312),
            "erase_scalar_labels": (303, 304),
            "retain_shell_erase_rational_labels": (155, 156),
            "erase_rational_coefficient_labels": (57, 58),
        }
        for row in self.evidence["probes"]:
            self.assertEqual(
                (row["coefficient_rank"], row["augmented_rank"]),
                expected[row["mode"]],
            )
            self.assertFalse(row["consistent"])
            self.assertEqual(row["unknown_count"], 506)

    def test_source_functional_negative_witness_is_exact_and_independent(self) -> None:
        row = self.result["source_functional_interior"]
        self.assertEqual(row["source"]["git_blob_sha1"], "61f12f412726887f506e1d423b7ee183a22116e5")
        self.assertEqual(row["source"]["byte_count"], 44980)
        self.assertEqual(row["samples"], [[8, 1, 2], [9, 2, 1]])
        self.assertTrue(row["strict_interior_only"])
        self.assertFalse(row["shell_regularization_enters_witness"])
        self.assertTrue(row["qrow_point_replay"])
        self.assertEqual(row["one_orientation_spatial_multiplier"], 2)
        self.assertEqual(row["unknown_count"], 506)
        self.assertEqual(row["target_coordinate_count"], 298)
        self.assertEqual(row["coefficient_rank"], 84)
        self.assertEqual(row["augmented_rank"], 85)
        self.assertFalse(row["consistent"])
        self.assertEqual(row["nullity"], 422)
        self.assertTrue(self.result["independent_source_functional_replay_complete"])
        self.assertFalse(self.result["producer_source_jets_imported_by_verifier_as_authority"])
        self.assertFalse(self.result["producer_projected_matrices_imported_by_verifier_as_authority"])

    def test_negative_terminal_is_narrow_and_fail_closed_on_claims(self) -> None:
        result = self.result
        self.assertEqual(
            result["terminal"],
            "SUPPORT_LOCKED_DEGREE0_COUPLED_CORRECTION_RECOMBINATION_INCOMPATIBLE",
        )
        self.assertEqual(
            result["terminal_basis"],
            "EXACT_SOURCE_LOCKED_STRICT_INTERIOR_NECESSARY_SUBSYSTEM_INCONSISTENCY",
        )
        self.assertTrue(result["source_locked_recombination_restriction_reconstructed"])
        self.assertFalse(result["actual_source_locked_global_recombination_map_fully_reconstructed"])
        self.assertTrue(result["global_solution_implies_subsystem_solution"])
        self.assertTrue(result["finite_specialization_used_as_nonexistence_witness"])
        self.assertFalse(result["finite_sampling_used_as_identity_proof"])
        self.assertEqual(
            result["class_excluded"],
            "SUPPORT_LOCKED_ORIENTED_ONE_BODY_DEGREE0_WEIGHT_CORRECTION_001",
        )
        self.assertTrue(result["scope_exclusion_only"])
        self.assertFalse(result["broader_correction_classes_excluded"])
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_emit_terminal_record(self) -> None:
        result = self.result
        row = result["source_functional_interior"]
        print(
            "T3_012_B_RESULT "
            + json.dumps(
                {
                    "terminal": result["terminal"],
                    "terminal_basis": result["terminal_basis"],
                    "source_git_blob_sha1": row["source"]["git_blob_sha1"],
                    "samples": row["samples"],
                    "unknown_count": row["unknown_count"],
                    "target_coordinate_count": row["target_coordinate_count"],
                    "coefficient_rank": row["coefficient_rank"],
                    "augmented_rank": row["augmented_rank"],
                    "consistent": row["consistent"],
                    "nullity": row["nullity"],
                    "independent_source_functional_replay_complete": result["independent_source_functional_replay_complete"],
                    "global_solution_implies_subsystem_solution": result["global_solution_implies_subsystem_solution"],
                    "shell_regularization_enters_witness": row["shell_regularization_enters_witness"],
                    "finite_specialization_used_as_nonexistence_witness": result["finite_specialization_used_as_nonexistence_witness"],
                    "finite_sampling_used_as_identity_proof": result["finite_sampling_used_as_identity_proof"],
                    "residual_sum_zero_proved": result["residual_sum_zero_proved"],
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
