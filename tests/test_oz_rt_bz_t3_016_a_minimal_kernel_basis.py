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
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


producer = _load(HERE / "minimal_kernel_basis.py", "mkb_producer")
verifier = _load(HERE / "minimal_kernel_basis_verifier.py", "mkb_verifier")


class MinimalKernelBasisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = producer.build_minimal_kernel_basis()
        cls.replay = verifier.verify_minimal_kernel_basis()

    def test_exact_saturation(self):
        ev = self.evidence
        self.assertEqual(ev["raw_kernel_basis_dimension"], 576)
        self.assertEqual(ev["raw_total_column_degree"], 3456)
        self.assertEqual(ev["saturation"]["pivot_matrix_determinant"], 1)
        self.assertEqual(ev["saturation"]["replacement_columns"], 8)
        self.assertEqual(ev["saturation"]["replacement_column_degree"], 5)
        self.assertEqual(ev["saturation"]["final_total_column_degree"], 3448)
        self.assertTrue(ev["minimal_polynomial_kernel_basis"])
        self.assertTrue(all(rank == 576 for rank in ev["witness"]["saturated_exceptional_ranks"].values()))
        self.assertEqual(ev["witness"]["leading_matrix_rank"], 576)

    def test_independent_replay(self):
        rp = self.replay
        self.assertTrue(rp["fixed_fiber_divisor_orbit_argument_replayed"])
        self.assertEqual(rp["pivot_matrix_determinant"], 1)
        self.assertTrue(all(rank == 576 for rank in rp["saturated_exceptional_ranks"].values()))
        self.assertEqual(rp["leading_rank"], 576)
        self.assertTrue(rp["minimal_polynomial_kernel_basis"])

    def test_claim_firewall(self):
        for result in (self.evidence, self.replay):
            self.assertEqual(result["proof_effect"], "NONE")
            self.assertEqual(result["promotion_effect"], "NONE")
            self.assertFalse(result["t3_proved"])
            self.assertFalse(result["t3_refuted"])
            self.assertFalse(result["global_certificate_constructed"])


if __name__ == "__main__":
    unittest.main()
