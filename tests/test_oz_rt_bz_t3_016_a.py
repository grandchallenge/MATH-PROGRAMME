from __future__ import annotations

import importlib.util
import json
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
affine_probe = _load(HERE / "affine_probe.py", "oz_t3_016_a_affine_probe_test")


class OzRtBzT3016ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = producer.build_preflight()
        cls.replay = verifier.verify()

    def test_exact_source_lock(self) -> None:
        cls_source = self.evidence["source"]["commit"]
        self.assertEqual(cls_source, producer.SOURCE_COMMIT)
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

    def test_exact_e1_kernel_geometry(self) -> None:
        geom = self.evidence["residual_geometry"]
        self.assertEqual(geom["potential_bidegree"], [23, 23])
        self.assertEqual(geom["potential_dimension"], 576)
        self.assertEqual(geom["e1_numerator_bidegree_bound"], [28, 28])
        self.assertTrue(geom["numerator_formula_exact"])
        self.assertEqual(geom["generic_rank"], 1048)
        self.assertEqual(geom["generic_kernel_dimension"], 576)
        self.assertEqual(geom["curl_image_dimension"], 576)
        self.assertTrue(geom["curl_image_equals_generic_kernel"])
        self.assertEqual(geom["witness"]["operator_modular_rank"], 1048)
        self.assertEqual(geom["witness"]["curl_eval_modular_rank"], 576)

        self.assertTrue(self.replay["e1_operator_reconstructed_independently"])
        self.assertEqual(self.replay["operator_modular_rank_witness"], 1048)
        self.assertTrue(self.replay["curl_coefficients_reconstructed_independently"])
        self.assertEqual(self.replay["curl_modular_rank_witness"], 576)
        self.assertTrue(self.replay["operator_annihilates_curl_coefficients"])
        self.assertTrue(self.replay["curl_image_equals_generic_kernel"])

    def test_source_1106_rank_reconciles_with_unforced_scan(self) -> None:
        reported = self.evidence["source_reported_residual_geometry"]
        self.assertEqual(reported["generic_rank"], 1106)
        self.assertEqual(reported["kernel_dimension"], 518)
        self.assertEqual(reported["unforced_scan_columns"], 1682)
        self.assertEqual(reported["unforced_scan_rank"], 1106)
        self.assertEqual(reported["unforced_scan_kernel_dimension"], 576)
        self.assertEqual(reported["boundary_forced_columns"], 1624)
        self.assertEqual(reported["boundary_forced_reconstructed_rank"], 1048)
        self.assertEqual(reported["boundary_forced_kernel_dimension"], 576)
        self.assertEqual(
            reported["disposition"],
            "RECONCILED_AS_MIXED_ANSATZ_DIMENSION_ACCOUNTING",
        )
        self.assertFalse(self.replay["source_rank_1106_kernel_518_promoted"])
        self.assertTrue(self.replay["source_geometry_reconciled"])
        self.assertEqual(self.replay["source_unforced_scan_columns"], 1682)
        self.assertEqual(self.replay["source_unforced_scan_rank"], 1106)
        self.assertEqual(self.replay["source_unforced_scan_kernel_dimension"], 576)

    def test_canonical_potential_gauge_affine_probe(self) -> None:
        sample = affine_probe.probe(5, prime=4194301, fresh_points=16)
        print("OZ_T3_016_A_AFFINE_SAMPLE=" + json.dumps(sample, sort_keys=True), flush=True)
        self.assertEqual(sample["n"], 5)
        self.assertEqual(sample["prime"], 4194301)
        self.assertEqual(sample["e1_columns"], 1624)
        self.assertEqual(sample["gauge_coordinates"], 576)
        self.assertEqual(sample["augmented_rank"], 1624)
        self.assertEqual(sample["solver_nbad"], 0)
        self.assertEqual(sample["fresh_points"], 16)
        self.assertEqual(sample["fresh_violations"], 0)
        self.assertEqual(sample["gauge_violations"], 0)
        self.assertEqual(len(sample["standalone_blocks"]), 7)
        self.assertEqual(len(sample["section_nonzero_coefficients_by_block"]), 7)
        self.assertEqual(len(sample["section_sha256"]), 64)

    def test_terminal_and_firewall(self) -> None:
        self.assertEqual(
            self.evidence["terminal"],
            "ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED",
        )
        self.assertEqual(self.replay["terminal"], self.evidence["terminal"])
        self.assertEqual(self.evidence["proof_effect"], "NONE")
        self.assertEqual(self.evidence["promotion_effect"], "NONE")
        self.assertEqual(self.evidence["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")


if __name__ == "__main__":
    unittest.main()
