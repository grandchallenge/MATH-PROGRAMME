from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_012_B"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3012BTests(unittest.TestCase):
    def test_projection_probe_is_explicitly_discovery_only(self) -> None:
        result = producer.build()
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
        result = producer.build()
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

    def test_independent_projection_replay(self) -> None:
        result = producer.build()
        replay = verifier.verify(result)
        self.assertTrue(replay["independent_projection_replay_complete"])
        self.assertFalse(replay["producer_projected_matrices_imported_as_authority"])
        self.assertEqual(replay["proof_effect"], "NONE")
        self.assertEqual(replay["promotion_effect"], "NONE")
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
