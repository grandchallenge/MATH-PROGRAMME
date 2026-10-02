from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_015_A"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verifier


class OzRtBzT3015ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = producer.build()
        cls.replay = verifier.verify(cls.evidence)

    def test_exact_predecessor_and_source_locks(self) -> None:
        locks = self.evidence["source_locks"]
        self.assertEqual(
            locks["predecessor"]["CONTRACT.json"],
            "ebb244851395b7d72f9932cc9d1d8190faf305f1",
        )
        self.assertEqual(
            locks["declarations"]["work/Z5T3_BRIDGE.md"]["git_blob_sha1"],
            "002c96d28123e5949c38656f26677ae5a723ee93",
        )
        self.assertEqual(
            locks["declarations"]["work/Z5CF_LINALG.md"]["git_blob_sha1"],
            "637ecaa7f3ee941a87932de390eb7336d7fde677",
        )
        self.assertEqual(
            locks["scalar_authority"]["git_blob_sha1"],
            "5682d61997499eccefddc15c6967dc907c091af4",
        )
        self.assertEqual(
            locks["qrow"]["git_blob_sha1"],
            "61f12f412726887f506e1d423b7ee183a22116e5",
        )

    def test_global_module_is_exact_and_untruncated(self) -> None:
        module = self.evidence["module"]
        self.assertEqual(module["coefficient_field"], "Q(n,k,l)")
        self.assertEqual(module["generator_count"], 506)
        self.assertEqual(
            module["channel_counts"],
            {"n1": 116, "n2": 116, "n3": 116, "k1": 158},
        )
        self.assertEqual(
            module["scalar_namespace"],
            ["TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK"],
        )
        self.assertTrue(module["global_shift_module_only"])
        self.assertFalse(module["finite_sample_grid_used"])
        self.assertIsNone(module["rational_degree_cutoff"])
        self.assertIsNone(module["denominator_cutoff"])
        self.assertGreater(module["coordinate_monomial_count"], 0)
        self.assertGreater(module["target_record_count"], 0)

    def test_every_generator_has_exact_shifted_and_base_terms(self) -> None:
        module = self.evidence["module"]
        self.assertEqual(len(module["generators"]), 506)
        for index, row in enumerate(module["generators"]):
            self.assertEqual(row["index"], index)
            self.assertIn(row["channel"], module["channel_counts"])
            self.assertIn(row["scalar"], module["scalar_namespace"])
            self.assertEqual(len(row["shift"]), 3)
            self.assertEqual(row["base_term"]["monomial"], row["support_monomial"])
            self.assertTrue(row["base_term"]["coefficient"])
            self.assertTrue(row["shifted_terms"])

    def test_independent_reconstruction_matches_byte_stable_module_digest(self) -> None:
        self.assertTrue(self.replay["independent_global_module_replay_complete"])
        self.assertFalse(self.replay["producer_module_imported_as_authority"])
        self.assertEqual(self.replay["module_sha256"], self.evidence["module_sha256"])
        self.assertEqual(self.replay["generator_count"], 506)
        self.assertEqual(
            self.replay["channel_counts"],
            {"n1": 116, "n2": 116, "n3": 116, "k1": 158},
        )

    def test_terminal_and_claim_firewall(self) -> None:
        self.assertEqual(
            self.evidence["terminal"],
            "GLOBAL_RATIONAL_DELTA_DIFFERENCE_MODULE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED",
        )
        self.assertFalse(self.evidence["global_certificate_constructed"])
        self.assertFalse(self.evidence["residual_sum_zero_proved"])
        self.assertEqual(self.evidence["proof_effect"], "NONE")
        self.assertEqual(self.evidence["promotion_effect"], "NONE")
        self.assertEqual(self.evidence["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_emit_result(self) -> None:
        module = self.evidence["module"]
        print(
            "T3_015_A_RESULT "
            + json.dumps(
                {
                    "terminal": self.evidence["terminal"],
                    "module_sha256": self.evidence["module_sha256"],
                    "generator_count": module["generator_count"],
                    "channel_counts": module["channel_counts"],
                    "coordinate_monomial_count": module["coordinate_monomial_count"],
                    "target_record_count": module["target_record_count"],
                    "finite_sample_grid_used": module["finite_sample_grid_used"],
                    "rational_degree_cutoff": module["rational_degree_cutoff"],
                    "denominator_cutoff": module["denominator_cutoff"],
                    "independent_global_module_replay_complete": self.replay[
                        "independent_global_module_replay_complete"
                    ],
                    "global_certificate_constructed": self.evidence[
                        "global_certificate_constructed"
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
