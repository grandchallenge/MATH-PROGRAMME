from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"
MOD=HERE/"one_body_structure.py"
spec=importlib.util.spec_from_file_location("t3_009_one_body_structure",MOD)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-009 one-body structure producer")
ob=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ob)


class T3009OneBodyStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=ob.build()
        print("T3-009 one-body residual module summary:",cls.result)

    def test_no_nested_atoms_remain(self):
        self.assertEqual(self.result["nested_atoms_remaining"],0)
        self.assertGreater(self.result["union_one_body_atom_count"],0)

    def test_all_original_and_abel_channels_present(self):
        self.assertEqual(set(self.result["canonical_weight_difference_one_body"]),{"n1","n2","n3","k1","l1"})
        self.assertEqual(set(self.result["abel_transfer_differences"]),{
            "Delta_k_N11","Delta_l_N11","Delta_k_N12k","Delta_l_N12k","Delta_k_N12l","Delta_l_N12l"})

    def test_no_promotion(self):
        self.assertFalse(self.result["residual_sum_zero_proved"])
        self.assertEqual(self.result["proof_effect"],"NONE")
        self.assertEqual(self.result["promotion_effect"],"NONE")
        self.assertEqual(self.result["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")


if __name__=="__main__":
    unittest.main()
