#!/usr/bin/env python3
"""Independent fail-closed checks of the actual core-kernel replay receipt."""
import copy, json, re, sys, unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parent))
import erdos_pv_0560_formal_replay as v

class Formal0560Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=v.verify()
        cls.stdout=v.LOG.read_text()

    def test_exact_kernel_source_and_toolchain(self):
        self.assertEqual(cls_source_hash := v.source_contract(),self.r["source_sha256"])
        self.assertEqual(len(cls_source_hash),64)
        self.assertTrue(self.r["lean_version"].startswith("Lean (version 4.33.0"))
        self.assertEqual(self.r["imports"],["Init"])
        self.assertEqual(self.r["positive_exit_code"],0)

    def test_all_twelve_types_and_axioms(self):
        self.assertEqual(len(self.r["axioms"]),12)
        self.assertEqual(self.r["axioms"],v.parse_axioms(self.stdout))
        self.assertNotIn("sorryAx",self.stdout)
        self.assertNotIn("error:",self.stdout)
        self.assertTrue(all(set(ax) <= {"propext","Quot.sound"}
                            for ax in self.r["axioms"].values()))

    def test_actual_three_hostile_rejections(self):
        self.assertEqual(set(self.r["hostile"]),set(v.NEGATIVES))
        self.assertTrue(all(x["exit_code"] != 0 for x in self.r["hostile"].values()))
        self.assertTrue(all("error:" in x["diagnostic"] for x in self.r["hostile"].values()))

    def test_substituted_axiom_is_rejected(self):
        fake=self.stdout.replace("Quot.sound","Classical.choice")
        with self.assertRaises(ValueError):
            v.parse_axioms(fake)

    def test_missing_type_or_ax_report_is_rejected(self):
        bad=self.stdout.replace(
           "'ErdosPV0560.strict_gate_all' depends on axioms: [propext, Quot.sound]","")
        with self.assertRaises(ValueError):
            v.parse_axioms(bad)
        with self.assertRaises(ValueError):
            v.parse_axioms(self.stdout.replace(
                "ErdosPV0560.strict_gate_all (t : Nat)","ErdosPV0560.strict_gate_all (t : Int)"))

    def test_injected_hole_source_is_rejected(self):
        original=v.SRC.read_text()
        self.assertNotIn("sorryAx",original)
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as td:
            p=Path(td)/"Injected.lean"
            p.write_text(original+"\nexample : False := by sorry\n")
            with patch.object(v,"SRC",p):
                with self.assertRaises(ValueError):
                    v.source_contract()

    def test_exact_auxiliary_arithmetic_by_independent_rationals(self):
        for s in range(2,23):
            for a in range(2,16):
                factor=(Fraction(s-1,a-1)*
                        Fraction(s,s-1)**a)
                self.assertLessEqual(factor,2**(s+a))
        self.assertFalse(2*18**2 < 25**2)
        self.assertTrue(all(2*18**t <25**t for t in range(4,75)))

    def test_exact_held_claim_and_worker_result_comment(self):
        path=v.EV/'C_RETURN_BINDING_001.json'
        r=json.loads(path.read_text())
        self.assertEqual(r['claim_sha'],'8b6a32fa6fc8fd037051835fa54542f81ecca50e')
        self.assertEqual(r['return_comment_id'],6947981217)
        self.assertEqual(r['return_body_sha256'],
                         '7ac16b9c6ebfdc9c7c549ec0708af0d83af1b1da57aee7371b88dc4eedfa659a')
        self.assertIs(r['single_result_readback'],True)
        self.assertIs(r['whole_size_ramsey_proved'],False)

    def test_scope_and_followup_boundary(self):
        self.assertIs(self.r["whole_size_ramsey_proved"],False)
        self.assertIs(self.r["formalization_work_required"],True)
        self.assertIs(self.r["mathlib_semantic_equivalence_kernel_checked"],False)
        self.assertIs(self.r["mathcert_certified"],False)
        self.assertEqual(self.r["predecessor_main"],
                         "123701f543f32c7bf92197f77f39405a3702f8f4")
        self.assertEqual(self.r["claim_sha"],
                         "8b6a32fa6fc8fd037051835fa54542f81ecca50e")

    def test_noninduced_vs_induced_K7_counterexample(self):
        import erdos_pv_bipartite_count_0560 as b
        g=b.neighbors(7,2**21-1)
        self.assertEqual(b.oracle(g,2,4),105)
        self.assertEqual(b.producer(g,2,4)[0],105)
        # Every 2-side and 4-side of K7 contains internal host edges.
        induced=0
        from itertools import combinations
        for left in combinations(range(7),2):
            for right in combinations((x for x in range(7) if x not in left),4):
                inside=any((g[u]>>w)&1 for S in (left,right)
                           for u,w in combinations(S,2))
                induced+=not inside
        self.assertEqual(induced,0)

    def test_shared_edge_copy_events_are_not_independent(self):
        from fractions import Fraction
        left=(0,1)
        t1=(2,3,4,5)
        t2=(2,3,4,6)
        E1={frozenset((a,b)) for a in left for b in t1}
        E2={frozenset((a,b)) for a in left for b in t2}
        self.assertEqual((len(E1),len(E2),len(E1&E2),len(E1|E2)),
                         (8,8,6,10))
        one=Fraction(2,2**8)
        joint=Fraction(2,2**len(E1|E2))
        self.assertNotEqual(joint,one**2)
        self.assertEqual(joint/(one**2),32)

    def test_equal_partitions_are_not_unique_orientation(self):
        import erdos_pv_bipartite_count_0560 as b
        g=b.neighbors(4,2**6-1)
        # Source requires s<t; with s=t=2 the side-swap is distinct.
        from itertools import combinations
        copies={(S,tuple(x for x in range(4) if x not in S))
                 for S in combinations(range(4),2)}
        self.assertEqual(len(copies),6)
        self.assertEqual(len({frozenset((frozenset(a),frozenset(c)))
                              for a,c in copies}),3)

if __name__=="__main__":
    unittest.main()
