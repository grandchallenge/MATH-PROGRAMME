from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

# The pinned 44,980-byte Q-row expression is a deeply left-associated arithmetic
# tree.  Both independent evaluators intentionally traverse that exact parsed
# tree; increase only the interpreter stack ceiling so the source shape, rather
# than Python's default recursion limit, controls the replay.
sys.setrecursionlimit(max(sys.getrecursionlimit(), 10000))

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_012_B"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3012BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = producer.build()

    def test_projection_probe_is_explicitly_discovery_only(self) -> None:
        result = self.result
        self.assertEqual(
            result["terminal"],
            "COUPLED_RECOMBINATION_PROJECTION_VIABILITY_PROBE_COMPLETE__EXACT_FUNCTIONAL_MAP_PENDING",
        )
        self.assertEqual(result["probe_semantics"]["status"], "DISCOVERY_ONLY")
        self.assertTrue(result["probe_semantics"]["not_a_functional_recombination_certificate"])
        self.assertFalse(result["probe_semantics"]["finite_sampling_used"])
        self.assertTrue(result["probe_semantics"]["exact_Q_linear_algebra"])
        self.assertFalse(result["actual_source_locked_recombination_map_reconstructed"])
        self.assertFalse(result["residual_sum_zero_proved"])
        self.assertEqual(result["proof_effect"], "NONE")
        self.assertEqual(result["promotion_effect"], "NONE")
        self.assertEqual(result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_protected_c_negative_frontier_is_reconstructed(self) -> None:
        result = self.result
        expected = {
            "n1": (116, 67, 68),
            "n2": (116, 67, 68),
            "n3": (116, 67, 68),
            "k1": (158, 110, 111),
        }
        for channel, triple in expected.items():
            row = result["protected_c_channel_ranks"][channel]
            self.assertEqual(
                (row["unknown_count"], row["coefficient_rank"], row["augmented_rank"]),
                triple,
            )

    def test_source_functional_interior_probe_is_source_locked(self) -> None:
        row = self.result["producer_source_functional_interior_probe"]
        self.assertEqual(row["source"]["git_blob_sha1"], "61f12f412726887f506e1d423b7ee183a22116e5")
        self.assertEqual(row["source"]["byte_count"], 44980)
        self.assertTrue(row["strict_interior_only"])
        self.assertFalse(row["shell_regularization_enters_witness"])
        self.assertTrue(row["qrow_point_replay"])
        self.assertEqual(row["one_orientation_spatial_multiplier"], 2)
        self.assertEqual(row["unknown_count"], 506)

    def test_independent_projection_and_source_functional_replay(self) -> None:
        result = self.result
        replay = verifier.verify(result)
        self.assertTrue(replay["independent_projection_replay_complete"])
        self.assertTrue(replay["independent_source_functional_replay_complete"])
        self.assertFalse(replay["producer_projected_matrices_imported_as_authority"])
        self.assertFalse(replay["producer_source_jets_imported_as_authority"])
        self.assertEqual(replay["proof_effect"], "NONE")
        self.assertEqual(replay["promotion_effect"], "NONE")
        self.assertEqual(
            replay["source_functional_interior"]["coefficient_rank"],
            result["producer_source_functional_interior_probe"]["coefficient_rank"],
        )
        self.assertEqual(
            replay["source_functional_interior"]["augmented_rank"],
            result["producer_source_functional_interior_probe"]["augmented_rank"],
        )
        print(
            "T3_012_B_PROBE "
            + json.dumps(
                {
                    "terminal": result["terminal"],
                    "probes": [
                        {
                            "mode": row["mode"],
                            "unknown_count": row["unknown_count"],
                            "coefficient_rank": row["coefficient_rank"],
                            "augmented_rank": row["augmented_rank"],
                            "consistent": row["consistent"],
                            "target_coordinate_count": row["target_coordinate_count"],
                        }
                        for row in result["probes"]
                    ],
                    "source_functional_interior": {
                        key: result["producer_source_functional_interior_probe"][key]
                        for key in (
                            "samples", "unknown_count", "target_coordinate_count",
                            "coefficient_rank", "augmented_rank", "consistent", "nullity",
                        )
                    },
                    "independent_source_functional_replay_complete": replay["independent_source_functional_replay_complete"],
                    "proof_effect": result["proof_effect"],
                    "promotion_effect": result["promotion_effect"],
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
