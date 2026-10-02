from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_015_C"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


producer = _load(HERE / "producer.py", "oz_t3_015_c_producer_test")
verifier = _load(HERE / "verifier.py", "oz_t3_015_c_verifier_test")


class OzRtBzT3015CTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = producer.build()
        cls.replay = verifier.verify(cls.evidence)

    def test_exact_predecessor_module_lock(self) -> None:
        self.assertEqual(
            self.evidence["predecessor_module_sha256"],
            "cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da",
        )
        self.assertEqual(self.replay["module_sha256"], self.evidence["predecessor_module_sha256"])

    def test_forced_coordinate_is_unique(self) -> None:
        witness = self.evidence["witness"]
        self.assertEqual(witness["generator_index"], 59)
        self.assertEqual(witness["monomial"], ["H_k_2", "H_nk_1", "H_nkl_1"])
        self.assertEqual(witness["shift"], [0, 1, 0])
        self.assertTrue(witness["full_incoming_incidence_checked"])
        self.assertEqual(
            witness["incoming"],
            [
                {"generator_index": 59, "channel": "k1", "scalar": "SK", "side": "base", "coefficient": "-1"},
                {"generator_index": 59, "channel": "k1", "scalar": "SK", "side": "shifted", "coefficient": "1"},
            ],
        )
        self.assertEqual(witness["targets"], [{"scalar": "SK", "coefficient": "1/(k + l + 1)"}])

    def test_source_locked_scalar_is_nonzero(self) -> None:
        row = self.evidence["scalar_nonzero_witness"]
        self.assertEqual(row["scalar"], "SK")
        self.assertTrue(row["proves_nonzero_rational_function"])
        self.assertNotEqual(row["numerator"], 0)
        self.assertTrue(self.replay["independent_scalar_nonzero_replay"]["producer_sample_replayed"])

    def test_completeness_backed_discrete_residue_obstruction(self) -> None:
        obstruction = self.evidence["discrete_residue_obstruction"]
        self.assertTrue(obstruction["completeness_backed"])
        self.assertFalse(obstruction["bounded_ansatz_used"])
        self.assertIsNone(obstruction["degree_cutoff"])
        self.assertIsNone(obstruction["denominator_cutoff"])
        self.assertEqual(obstruction["target_discrete_residue"], {"numerator": 1, "denominator": 1})
        self.assertEqual(obstruction["forward_difference_orbit_residue"], {"numerator": 0, "denominator": 1})
        self.assertEqual(obstruction["target_orbit_sum"], 1)
        self.assertTrue(self.replay["discrete_residue_theorem_applied"])
        self.assertTrue(self.replay["complete_rational_nonexistence_verified"])
        self.assertTrue(self.evidence["class_nonexistence_proved"])

    def test_independent_reconstruction(self) -> None:
        self.assertTrue(self.replay["independent_module_reconstruction_complete"])
        self.assertFalse(self.replay["producer_module_imported_as_authority"])
        self.assertTrue(self.replay["full_incoming_incidence_replayed"])

    def test_terminal_and_claim_firewall(self) -> None:
        self.assertEqual(
            self.evidence["terminal"],
            "GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED",
        )
        self.assertFalse(self.evidence["global_certificate_constructed"])
        self.assertFalse(self.evidence["residual_sum_zero_proved"])
        self.assertEqual(self.evidence["proof_effect"], "NONE")
        self.assertEqual(self.evidence["promotion_effect"], "NONE")
        self.assertEqual(self.evidence["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_emit_result(self) -> None:
        print(
            "T3_015_C_RESULT "
            + json.dumps(producer.compact_result(self.evidence), sort_keys=True, separators=(",", ":")),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
