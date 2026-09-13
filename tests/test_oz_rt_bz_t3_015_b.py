from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_015_B"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


producer = _load(HERE / "producer.py", "oz_t3_015_b_producer_test")
verifier = _load(HERE / "verifier.py", "oz_t3_015_b_verifier_test")
probe = _load(HERE / "separable_probe.py", "oz_t3_015_b_separable_probe_test")


class OzRtBzT3015BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence, module = producer.build_with_module()
        cls.replay = verifier.verify(cls.evidence)
        cls.probe_result = probe.probe(module)

    def test_exact_predecessor_module_lock(self) -> None:
        self.assertEqual(
            self.evidence["predecessor_module_sha256"],
            "cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da",
        )
        self.assertEqual(
            self.replay["module_sha256"], self.evidence["predecessor_module_sha256"]
        )

    def test_shift_module_is_exactly_n_k_and_strictly_lowering(self) -> None:
        structure = self.evidence["structure"]
        self.assertEqual(
            structure["shift_directions"],
            [[0, 1, 0], [1, 0, 0], [2, 0, 0], [3, 0, 0]],
        )
        self.assertFalse(structure["l_shift_present"])
        self.assertTrue(structure["strict_degree_lowering"])
        self.assertEqual(structure["degree_lowering_violations"], [])
        self.assertGreater(structure["nonself_dependency_edge_count"], 0)

    def test_scalar_partition_is_complete(self) -> None:
        structure = self.evidence["structure"]
        self.assertTrue(structure["scalar_partition_exact"])
        reports = structure["scalar_reports"]
        self.assertEqual(
            list(reports), ["TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK"]
        )
        self.assertEqual(sum(row["generator_count"] for row in reports.values()), 506)
        self.assertEqual(sum(row["target_record_count"] for row in reports.values()), 513)
        for row in reports.values():
            self.assertEqual(
                row["covered_target_monomial_count"] + row["uncovered_target_monomial_count"],
                row["target_monomial_count"],
            )

    def test_independent_structural_replay(self) -> None:
        self.assertTrue(self.replay["independent_structure_replay_complete"])
        self.assertFalse(self.replay["producer_structure_imported_as_authority"])
        self.assertEqual(
            self.replay["scalar_reports"], self.evidence["structure"]["scalar_reports"]
        )

    def test_scalar_separated_probe_is_positive_candidate_or_nonconclusive(self) -> None:
        self.assertIn(
            self.probe_result["status"],
            {
                "SCALAR_SEPARATED_GLOBAL_RATIONAL_CERTIFICATE_CANDIDATE",
                "SCALAR_SEPARATED_ROUTE_BLOCKED",
            },
        )
        self.assertFalse(self.probe_result["class_nonexistence_proved"])
        if self.probe_result["status"] == "SCALAR_SEPARATED_GLOBAL_RATIONAL_CERTIFICATE_CANDIDATE":
            self.assertTrue(self.probe_result["candidate_exact_scalarwise_replay"])
            self.assertEqual(
                self.probe_result["module_sha256"], self.evidence["predecessor_module_sha256"]
            )
            self.assertGreater(self.probe_result["certificate_generator_count"], 0)
        else:
            self.assertIn(
                self.probe_result["reason"],
                {
                    "UNSUPPORTED_TRIANGULAR_COORDINATE",
                    "UNIVARIATE_RATIONAL_ANTIDIFFERENCE_ABSENT",
                },
            )

    def test_terminal_and_claim_firewall(self) -> None:
        self.assertEqual(
            self.evidence["terminal"],
            "GLOBAL_RATIONAL_DELTA_SOLVER_STRUCTURE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED",
        )
        self.assertFalse(self.evidence["global_certificate_constructed"])
        self.assertFalse(self.evidence["residual_sum_zero_proved"])
        self.assertEqual(self.evidence["proof_effect"], "NONE")
        self.assertEqual(self.evidence["promotion_effect"], "NONE")
        self.assertEqual(self.evidence["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_emit_structure_and_probe(self) -> None:
        print(
            "T3_015_B_STRUCTURE "
            + json.dumps(producer.compact_result(self.evidence), sort_keys=True, separators=(",", ":")),
            flush=True,
        )
        print(
            "T3_015_B_SEPARABLE_PROBE "
            + json.dumps(probe.compact(self.probe_result), sort_keys=True, separators=(",", ":")),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
