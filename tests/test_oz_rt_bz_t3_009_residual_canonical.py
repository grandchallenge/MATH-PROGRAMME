from __future__ import annotations

import importlib.util
import unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"
MOD=HERE/"residual_canonical.py"
spec=importlib.util.spec_from_file_location("t3_009_residual_canonical",MOD)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-009 residual canonicalizer")
rc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

EXPECTED={
    "n1":(102,27,3,"ad46afea7d769dcba9d9c8a7b7842bcf72adfa1df0ae05f0734ec25432772655"),
    "n2":(102,27,3,"9c7a4849b95b1ab33670bbc8c2eb218df883cbf19add702f9228b4503b6b2b0e"),
    "n3":(102,27,3,"1e6f8e8ce6cf37b71dd741299c2ce5d1927225c5f08927b66c832a1687814a69"),
    "k1":(134,28,3,"ba7fa0176dc782b6c0747a71a9a0e13c3c5cf3d0c6077efe6f99c2a461c34780"),
    "l1":(134,28,3,"4fd7277655900f62a9f3676fd1d54614205cf8142cf26c04a4ef74eb8dfdc4c6"),
}
NESTED={
    "U_k_l_1_2","U_l_k_1_2","U_k_l_2_2","U_l_k_2_2","ES_k_1_3","ES_l_1_3",
    "U_k_l_1_4","U_l_k_1_4","U_k_l_2_3","U_l_k_2_3","ES_k_1_4","ES_l_1_4","ES_k_2_3","ES_l_2_3",
}
SURVIVING={"U_k_l_1_2","U_l_k_1_2","U_k_l_2_2","U_l_k_2_2","ES_k_1_3","ES_l_1_3"}


def scaled_rat(x,c):
    c=Q(c)
    return {s:c*v for s,v in x.items() if c*v}


def nested_projection(poly,name):
    out={}
    for mon,coeff in poly.items():
        if name not in mon:
            continue
        if sum(1 for a in mon if a in NESTED) != 1:
            raise AssertionError(f"more than one nested atom in {mon}")
        rest=list(mon); rest.remove(name); rest=tuple(rest)
        if rest in out:
            raise AssertionError(f"duplicate nested projection monomial {name}:{rest}")
        out[rest]=coeff
    return out


class T3009ResidualCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result, cls.deltas = rc.build_all()
        print("T3-009 residual canonical summary:", cls.result)

    def test_all_five_certificate_shifts_are_digest_locked(self):
        self.assertEqual(set(self.result["shifts"]),set(EXPECTED))
        for label,exp in EXPECTED.items():
            row=self.result["shifts"][label]
            self.assertEqual((row["canonical_monomials"],row["atom_count"],row["max_atomic_arity"],row["sha256"]),exp)

    def test_exact_replay_count_is_locked(self):
        self.assertEqual(self.result["exact_independent_checks"],840)
        self.assertEqual(self.result["bundle_sha256"],"a8b2bc4f905f58d03f0151e19e28e4ff0c1e217fbeb5721d38fe09bcd697b0e1")

    def test_no_theorem_promotion(self):
        self.assertEqual(self.result["proof_effect"],"NONE")
        self.assertEqual(self.result["promotion_effect"],"NONE")
        self.assertEqual(self.result["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_original_atom_system_is_closed(self):
        self.assertEqual(self.result["closure_only_atoms"],[])
        self.assertEqual(self.result["protected_atom_count"],41)
        self.assertEqual(len(self.result["protected_atoms"]),41)
        self.assertEqual(max(x["max_atomic_arity"] for x in self.result["shifts"].values()),3)

    def test_nested_sector_is_exact_three_combination_skeleton(self):
        # Every canonical shift difference has nested coordinates only in
        # N11=Ukl12+Ulk12,
        # N12k=2*ESl13-Ukl22,
        # N12l=2*ESk13-Ulk22.
        for label,poly in self.deltas.items():
            present={a for mon in poly for a in mon if a in NESTED}
            self.assertTrue(present <= SURVIVING, label)
            p_ukl12=nested_projection(poly,"U_k_l_1_2")
            p_ulk12=nested_projection(poly,"U_l_k_1_2")
            self.assertEqual(p_ukl12,p_ulk12,label)
            p_ukl22=nested_projection(poly,"U_k_l_2_2")
            p_esl13=nested_projection(poly,"ES_l_1_3")
            self.assertEqual(p_esl13,{m:scaled_rat(c,-2) for m,c in p_ukl22.items()},label)
            p_ulk22=nested_projection(poly,"U_l_k_2_2")
            p_esk13=nested_projection(poly,"ES_k_1_3")
            self.assertEqual(p_esk13,{m:scaled_rat(c,-2) for m,c in p_ulk22.items()},label)


if __name__ == "__main__":
    unittest.main()
