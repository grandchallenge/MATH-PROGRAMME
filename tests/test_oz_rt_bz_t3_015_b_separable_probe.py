from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_015_B"
PRED = HERE.parent / "OZ_RT_BZ_T3_015_A"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred = _load(PRED / "producer.py", "oz_t3_015_a_for_separable_probe")
probe = _load(HERE / "separable_probe.py", "oz_t3_015_b_separable_probe")


class OzRtBzT3015BSeparableProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        evidence = pred.build()
        cls.module_sha256 = evidence["module_sha256"]
        cls.result = probe.probe(evidence["module"])

    def test_exact_module_lock(self) -> None:
        self.assertEqual(
            self.module_sha256,
            "cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da",
        )

    def test_probe_is_positive_candidate_or_nonconclusive_route_failure(self) -> None:
        self.assertIn(
            self.result["status"],
            {
                "SCALAR_SEPARATED_GLOBAL_RATIONAL_CERTIFICATE_CANDIDATE",
                "SCALAR_SEPARATED_ROUTE_BLOCKED",
            },
        )
        self.assertFalse(self.result["class_nonexistence_proved"])
        if self.result["status"] == "SCALAR_SEPARATED_GLOBAL_RATIONAL_CERTIFICATE_CANDIDATE":
            self.assertTrue(self.result["candidate_exact_scalarwise_replay"])
            self.assertEqual(self.result["module_sha256"], self.module_sha256)
            self.assertGreater(self.result["certificate_generator_count"], 0)
        else:
            self.assertIn(
                self.result["reason"],
                {
                    "UNSUPPORTED_TRIANGULAR_COORDINATE",
                    "UNIVARIATE_RATIONAL_ANTIDIFFERENCE_ABSENT",
                },
            )

    def test_emit_probe_result(self) -> None:
        print(
            "T3_015_B_SEPARABLE_PROBE "
            + json.dumps(probe.compact(self.result), sort_keys=True, separators=(",", ":")),
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
