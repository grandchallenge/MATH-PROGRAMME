from __future__ import annotations

import importlib.util
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_009"
MOD = HERE / "one_body_coefficient_layer.py"
spec = importlib.util.spec_from_file_location("t3_009_one_body_coefficient_layer", MOD)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-009 one-body coefficient layer")
layer_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(layer_mod)

EXPECTED_ATOMS = [
    "A_k_1", "A_k_2", "A_l_1", "A_l_2", "B_k_1", "B_l_1", "C_1", "C_2",
    "H_k_1", "H_k_2", "H_k_3", "H_k_4", "H_kl_1", "H_kl_2",
    "H_l_1", "H_l_2", "H_l_3", "H_l_4", "H_nk_3", "H_nk_4", "H_nl_3", "H_nl_4",
]
EXPECTED_DIRECT = {
    "n1": (86, 21, 3, "80169c4f5fc44fe7308f6ea76f6020fbdcb0691b366f5d4cf6147048fd3baae9"),
    "n2": (86, 21, 3, "cd2717299b445ceed30f7c1c1a21b9645ea43a29bea2fa1fda2a43463aad02e2"),
    "n3": (86, 21, 3, "8cce2095a1778726596bf72646a8ed7b330bb0540eb7d061ad094d764c8e2746"),
    "k1": (118, 22, 3, "be8a0d4cef62e5b1edcb90550effd634d3d5347c94356061f25aff9123912a4f"),
    "l1": (118, 22, 3, "58178071899ad5ccb3d2043f2308b05cb80b749d389d416aa4f6ae153b72436f"),
}
EXPECTED_TRANSFER = {
    "AK:N11:k": (5, 4, 1, "711c4333436a1adcf98af9bfe4743325d8a186de8a00dafe9bec7ddf241f4a7a"),
    "AL:N11:l": (5, 4, 1, "26253f0590043819f3124894bea8337492a9bf748c6f5da7267e015db0adfe95"),
    "LKK:N12k:k": (2, 1, 1, "0d0f27a5d0d0e086954639e8632ef29b6e951f0024bed5aef822c5c2974b9762"),
    "LKL:N12k:l": (8, 7, 1, "d16b61c8440ecc2c95a6a6bcf7d42d17d1e55b3b8dfd7c574bfd1244401f490f"),
    "LLK:N12l:k": (8, 7, 1, "78fbc01b3996ef5dc258eb1e3df22bcfad3e47ed43a40609f3825d128582547b"),
    "LLL:N12l:l": (2, 1, 1, "6945e74ffd98dddf10287c9c4ed5f56bd4f1178020f7edbcd7070d2300329dd8"),
}


def compact(profile):
    return (profile["monomials"], profile["atoms"], profile["max_atomic_arity"], profile["sha256"])


class T3009OneBodyCoefficientLayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.layer, cls.result = layer_mod.build_layer()
        summary = {
            "final": {k: v for k, v in cls.result["final_layer"].items() if k != "rows"},
            "nested_skeleton_exact_digests": cls.result["nested_skeleton_exact_digests"],
        }
        print("T3-009 full pole-free one-body coefficient layer summary:", json.dumps(summary, sort_keys=True))

    def test_execution_boundary_and_nonclaims(self):
        self.assertEqual(self.result["execution_boundary"], "FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_001")
        self.assertEqual(self.result["status"], "FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_CONSTRUCTED")
        self.assertFalse(self.result["residual_sum_zero_proved"])
        self.assertEqual(self.result["proof_effect"], "NONE")
        self.assertEqual(self.result["promotion_effect"], "NONE")
        self.assertEqual(self.result["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_exact_direct_one_body_profiles(self):
        self.assertEqual({k: compact(v) for k, v in self.result["direct_one_body_profiles"].items()}, EXPECTED_DIRECT)

    def test_exact_abel_transfer_profiles(self):
        self.assertEqual({k: compact(v) for k, v in self.result["abel_transfer_profiles"].items()}, EXPECTED_TRANSFER)

    def test_final_atom_universe_and_scalar_basis(self):
        final = self.result["final_layer"]
        self.assertEqual(final["atoms"], 22)
        self.assertEqual(final["atom_names"], EXPECTED_ATOMS)
        self.assertEqual(final["max_atomic_arity"], 3)
        self.assertEqual(final["scalar_basis_size"], 11)
        self.assertEqual(tuple(self.result["scalar_basis"]), layer_mod.SCALAR_ORDER)
        self.assertTrue(final["monomials"] > 100)

    def test_every_retained_coefficient_is_exact_and_nonempty(self):
        for mon, by_scalar in self.layer.items():
            self.assertTrue(by_scalar)
            for scalar, rat in by_scalar.items():
                self.assertIn(scalar, layer_mod.SCALARS)
                self.assertTrue(rat)
                for coeff in rat.values():
                    self.assertIsInstance(coeff, Fraction)
                    self.assertNotEqual(coeff, 0)

    def test_nested_skeleton_is_verified_for_all_five_channels(self):
        self.assertEqual(set(self.result["nested_skeleton_exact_digests"]), {"n1", "n2", "n3", "k1", "l1"})
        self.assertTrue(all(len(x) == 64 for x in self.result["nested_skeleton_exact_digests"].values()))


if __name__ == "__main__":
    unittest.main()
