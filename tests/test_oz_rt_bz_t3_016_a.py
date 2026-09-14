from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_016_A"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


producer = _load(HERE / "producer.py", "oz_t3_016_a_producer_test")
verifier = _load(HERE / "verifier.py", "oz_t3_016_a_verifier_test")


class OzRtBzT3016ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = producer.build_preflight()
        cls.replay = verifier.verify()

    def test_exact_source_lock(self) -> None:
        self.assertEqual(cls_source := self.evidence["source"]["commit"], producer.SOURCE_COMMIT)
        self.assertEqual(cls_source, verifier.SOURCE_COMMIT)
        self.assertEqual(
            self.evidence["source"]["git_blob_sha1"],
            {path: producer.SOURCE_BLOBS[path] for path in sorted(producer.SOURCE_BLOBS)},
        )
        self.assertTrue(self.replay["source_locks_verified"])

    def test_lift_and_a4_nonvanishing(self) -> None:
        op = self.evidence["operator"]
        self.assertEqual(op["order"], 7)
        self.assertEqual(op["left_multiplier_order"], 4)
        self.assertEqual(op["a_polynomial_count"], 5)
        self.assertEqual(op["a_polynomial_degrees"], [58, 58, 58, 58, 58])
        self.assertTrue(op["a4_factorization_exact"])
        self.assertTrue(op["f4_shift2_exact"])
        self.assertTrue(op["f4_shift2_all_coefficients_positive"])
        self.assertNotEqual(int(op["a4_at_0"]), 0)
        self.assertNotEqual(int(op["a4_at_1"]), 0)
        self.assertTrue(self.replay["a4_factorization_integer_replay"])
        self.assertTrue(self.replay["a4_nonvanishing_certificate_replayed"])

    def test_order7_module_shape(self) -> None:
        module = self.evidence["module"]
        self.assertEqual(module["monomial_count"], 15)
        self.assertEqual(module["theorem_r_transport_count"], 5)
        self.assertEqual(module["residual_block_count"], 8)
        self.assertTrue(self.replay["order7_module_monomials_verified"])

    def test_structured_gauge_flatness(self) -> None:
        gauge = self.evidence["gauge"]
        self.assertTrue(gauge["flatness_exact"])
        self.assertIn("discrete-curl", gauge["interpretation"])
        self.assertTrue(self.replay["discrete_curl_flatness_verified"])

    def test_source_reported_kernel_not_promoted(self) -> None:
        geom = self.evidence["reported_residual_geometry"]
        self.assertEqual(geom["cofactor_columns"], 1624)
        self.assertEqual(geom["generic_rank"], 1106)
        self.assertEqual(geom["kernel_dimension"], 518)
        self.assertEqual(geom["authority"], "SOURCE_REPORTED_PENDING_GENERIC_CHAR0_REPLAY")
        self.assertFalse(self.replay["kernel_dimension_518_promoted"])

    def test_terminal_and_firewall(self) -> None:
        self.assertEqual(
            self.evidence["terminal"],
            "ORDER7_SOURCE_PREFLIGHT_REPLAYED__POPOV_REDUCTION_REQUIRED",
        )
        self.assertEqual(self.replay["terminal"], self.evidence["terminal"])
        self.assertEqual(self.evidence["proof_effect"], "NONE")
        self.assertEqual(self.evidence["promotion_effect"], "NONE")
        self.assertEqual(self.evidence["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")


if __name__ == "__main__":
    unittest.main()
