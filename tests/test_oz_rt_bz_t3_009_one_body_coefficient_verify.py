from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
MOD=HERE/"one_body_coefficient_verify.py"
spec=importlib.util.spec_from_file_location("t3_009_one_body_coefficient_verify",MOD)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-009 independent coefficient verifier")
verify_mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify_mod)


class T3009IndependentCoefficientReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=verify_mod.verify()
        print("T3-009 independent pole-free coefficient replay:",cls.result)

    def test_exact_canonical_binding(self):
        self.assertEqual(self.result["status"],"INDEPENDENT_FULL_POLE_FREE_ONE_BODY_COEFFICIENT_REPLAY_COMPLETE")
        self.assertEqual(self.result["monomials"],122)
        self.assertEqual(self.result["atoms"],22)
        self.assertEqual(self.result["max_atomic_arity"],3)
        self.assertEqual(self.result["scalar_basis_size"],11)
        self.assertEqual(self.result["sha256"],"90d067ae59790fab8648d006635c14950359b66eb8b57361e61d5b47b2b3af40")

    def test_shell_and_abel_replay(self):
        self.assertEqual(self.result["protected_factor_count"],8)
        self.assertEqual(self.result["exact_atom_shift_checks"],38950)
        self.assertEqual(self.result["exact_full_target_shift_checks"],950)
        self.assertEqual(self.result["checks_touching_moving_shell"],800)
        self.assertEqual(self.result["nested_skeleton_channels_verified"],5)
        self.assertEqual(self.result["abel_exact_checks"],9)
        self.assertTrue(self.result["full_rows_reconstructed_independently"])

    def test_no_promotion(self):
        self.assertFalse(self.result["finite_sampling_used_as_sum_proof"])
        self.assertEqual(self.result["proof_effect"],"NONE")
        self.assertEqual(self.result["promotion_effect"],"NONE")
        self.assertEqual(self.result["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")


if __name__=="__main__":
    unittest.main()
