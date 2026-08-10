from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"
MOD=HERE/"one_body_structure.py"
RETAINED=HERE/"ONE_BODY_STRUCTURE_RESULT.json"
spec=importlib.util.spec_from_file_location("t3_009_one_body_structure",MOD)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-009 one-body structure builder")
ob=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ob)

EXPECTED_ONE={
    "n1":(86,21,3,"80169c4f5fc44fe7308f6ea76f6020fbdcb0691b366f5d4cf6147048fd3baae9"),
    "n2":(86,21,3,"cd2717299b445ceed30f7c1c1a21b9645ea43a29bea2fa1fda2a43463aad02e2"),
    "n3":(86,21,3,"8cce2095a1778726596bf72646a8ed7b330bb0540eb7d061ad094d764c8e2746"),
    "k1":(118,22,3,"be8a0d4cef62e5b1edcb90550effd634d3d5347c94356061f25aff9123912a4f"),
    "l1":(118,22,3,"58178071899ad5ccb3d2043f2308b05cb80b749d389d416aa4f6ae153b72436f"),
}
EXPECTED_TRANSFER={
    "Delta_k_N11":(5,4,1,"711c4333436a1adcf98af9bfe4743325d8a186de8a00dafe9bec7ddf241f4a7a"),
    "Delta_l_N11":(5,4,1,"26253f0590043819f3124894bea8337492a9bf748c6f5da7267e015db0adfe95"),
    "Delta_k_N12k":(2,1,1,"0d0f27a5d0d0e086954639e8632ef29b6e951f0024bed5aef822c5c2974b9762"),
    "Delta_l_N12k":(8,7,1,"d16b61c8440ecc2c95a6a6bcf7d42d17d1e55b3b8dfd7c574bfd1244401f490f"),
    "Delta_k_N12l":(8,7,1,"78fbc01b3996ef5dc258eb1e3df22bcfad3e47ed43a40609f3825d128582547b"),
    "Delta_l_N12l":(2,1,1,"6945e74ffd98dddf10287c9c4ed5f56bd4f1178020f7edbcd7070d2300329dd8"),
}
EXPECTED_ATOMS=[
    "A_k_1","A_k_2","A_l_1","A_l_2","B_k_1","B_l_1","C_1","C_2",
    "H_k_1","H_k_2","H_k_3","H_k_4","H_kl_1","H_kl_2",
    "H_l_1","H_l_2","H_l_3","H_l_4","H_nk_3","H_nk_4","H_nl_3","H_nl_4",
]


def compact_profile(x):
    return (x["monomials"],x["atoms"],x["max_atomic_arity"],x["sha256"])


class T3009OneBodyStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=ob.build()
        cls.retained=json.loads(RETAINED.read_text(encoding="utf-8"))
        print("T3-009 one-body residual module summary:",cls.result)

    def test_exact_one_body_profiles_are_locked(self):
        self.assertEqual({k:compact_profile(v) for k,v in self.result["canonical_weight_difference_one_body"].items()},EXPECTED_ONE)
        self.assertEqual({k:compact_profile(v) for k,v in self.result["abel_transfer_differences"].items()},EXPECTED_TRANSFER)

    def test_retained_result_matches_builder(self):
        self.assertEqual(self.retained["producer"]["git_blob_sha1"],"62f83f765cbacf12e14fdc544c163c525f40c221")
        self.assertEqual({k:compact_profile(v) for k,v in self.retained["canonical_weight_difference_one_body"].items()},EXPECTED_ONE)
        self.assertEqual({k:compact_profile(v) for k,v in self.retained["abel_transfer_differences"].items()},EXPECTED_TRANSFER)

    def test_no_nested_atoms_remain_and_atom_universe_is_exact(self):
        self.assertEqual(self.result["nested_atoms_remaining"],0)
        self.assertEqual(self.result["union_one_body_atom_count"],22)
        self.assertEqual(self.result["union_one_body_atoms"],EXPECTED_ATOMS)
        self.assertEqual(self.retained["union_one_body_atoms"],EXPECTED_ATOMS)
        self.assertEqual(self.retained["nested_atoms_remaining"],0)

    def test_no_promotion(self):
        self.assertFalse(self.result["residual_sum_zero_proved"])
        self.assertFalse(self.retained["residual_sum_zero_proved"])
        for x in (self.result,self.retained):
            self.assertEqual(x["proof_effect"],"NONE")
            self.assertEqual(x["promotion_effect"],"NONE")
            self.assertEqual(x["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")


if __name__=="__main__":
    unittest.main()
