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


gauge_domain = _load(HERE / "gauge_domain.py", "oz_t3_016_a_gauge_domain_test")
gauge_domain_verifier = _load(
    HERE / "gauge_domain_verifier.py", "oz_t3_016_a_gauge_domain_verifier_test"
)


class OzRtBzT3016AGaugeDomainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = gauge_domain.build_gauge_domain()
        cls.replay = gauge_domain_verifier.verify_gauge_domain()

    def test_exact_global_integer_gauge_domain(self) -> None:
        evidence = self.evidence
        self.assertEqual(evidence["matrix_dimension"], 24)
        self.assertEqual(evidence["determinant_degree"], 144)
        self.assertEqual(evidence["forced_factor_degree"], 50)
        self.assertEqual(evidence["residual_degree"], 94)
        self.assertTrue(evidence["residual_monic"])
        self.assertEqual(evidence["residual_shift"], 9)
        self.assertTrue(evidence["residual_shift9_all_coefficients_positive"])
        self.assertTrue(all(value != 0 for value in evidence["residual_values_n_1_through_8"]))
        self.assertEqual(evidence["singular_nonnegative_integer_fibers"], [0])
        self.assertEqual(evidence["canonical_gauge_nonsingular_for_all_integers_n_gte"], 1)
        self.assertEqual(evidence["full_gauge_dimension"], 576)
        self.assertEqual(evidence["full_gauge_block_count"], 24)
        self.assertEqual(evidence["witness"]["n"], 5)
        self.assertEqual(evidence["witness"]["prime"], 4194301)
        self.assertEqual(evidence["witness"]["block_determinant_mod_prime"], 2300711)

    def test_independent_reconstruction(self) -> None:
        replay = self.replay
        self.assertEqual(replay["determinant_degree_bound_replayed"], 144)
        self.assertEqual(replay["determinant_degree"], 144)
        self.assertEqual(
            replay["factor_multiplicities_verified"],
            {"0": 1, "1": 7, "2": 2, "3": 2, "4": 2, "5": 2, "6": 2, "7": 31, "8": 1},
        )
        self.assertEqual(replay["residual_degree"], 94)
        self.assertTrue(replay["residual_shift9_positive"])
        self.assertTrue(replay["residual_n_1_through_8_nonzero"])
        self.assertTrue(replay["canonical_gauge_nonsingular_for_all_integer_n_gte_1"])
        self.assertEqual(replay["only_nonnegative_integer_singular_fiber"], 0)
        self.assertEqual(replay["governed_witness_replayed"], 2300711)
        self.assertFalse(replay["finite_sampling_used_as_global_proof"])

    def test_claim_firewall(self) -> None:
        for result in (self.evidence, self.replay):
            self.assertEqual(result["proof_effect"], "NONE")
            self.assertEqual(result["promotion_effect"], "NONE")
            self.assertFalse(result["t3_proved"])
            self.assertFalse(result["global_certificate_constructed"])


if __name__ == "__main__":
    unittest.main()
