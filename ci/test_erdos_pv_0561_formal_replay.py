#!/usr/bin/env python3
"""Adversarial actual receipt integrity and independent integer semantics."""
import copy
import json
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import erdos_pv_0561_formal_replay as v
from erdos_pv_0561_factor_gate import Graph, cut_condition, explicit_partition

class Formal0561Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=v.verify()
        cls.out=v.LOG.read_text()

    def test_exact_source_compiler_toolchain_and_types(self):
        self.assertEqual(self.r['source_sha256'],v.source_contract())
        self.assertTrue(self.r['lean_version'].startswith('Lean (version 4.33.0'))
        self.assertEqual(self.r['import_closure'],['Init'])
        self.assertEqual(self.r['positive_exit_code'],0)
        self.assertEqual(len(self.r['types_sha256']),11)
        self.assertTrue(all(len(h)==64 for h in self.r['types_sha256'].values()))

    def test_axioms_and_no_proof_holes(self):
        ax,types=v.parse(self.out)
        self.assertEqual(ax,self.r['axioms'])
        self.assertEqual(types,self.r['types_sha256'])
        self.assertEqual(set(ax),set(v.THEOREMS))
        self.assertTrue(all(set(a)<=v.ALLOWED for a in ax.values()))
        self.assertNotIn('sorryAx',self.out)

    def test_all_five_hostile_targets_genuinely_rejected(self):
        self.assertEqual(set(self.r['hostile']),set(v.NEGATIVES))
        self.assertTrue(all(x['exit_code']!=0 for x in self.r['hostile'].values()))
        self.assertTrue(all('error:' in x['diagnostic'] for x in self.r['hostile'].values()))

    def test_hole_import_and_new_axiom_rejected(self):
        original=v.SRC.read_text()
        for injection in ('\nexample : False := by sorry\n',
                          '\naxiom evil : False\n',
                          '\nimport Mathlib\n',
                          '\nexample : False := by native_decide\n'):
            with TemporaryDirectory() as td:
                tmp=Path(td)/'Erdos561Core.lean'
                tmp.write_text(original+injection)
                with patch.object(v,'SRC',tmp),self.assertRaises(ValueError):
                    v.source_contract()

    def test_substituted_axiom_report_rejected(self):
        self.assertIn('Classical.choice',self.out)
        changed=self.out.replace('Classical.choice','Classical.magic')
        with self.assertRaises(ValueError):
            v.parse(changed)

    def test_missing_exact_theorem_type_is_rejected(self):
        self.assertIn('ErdosPV0561.large_component_impossible (alpha beta D A B r : Nat)',self.out)
        bad=self.out.replace('ErdosPV0561.large_component_impossible (alpha beta D A B r : Nat)',
                             'ErdosPV0561.large_component_impossible (alpha beta D A B r : Int)')
        ax,t=v.parse(bad)
        self.assertNotEqual(t,self.r['types_sha256'])
        with self.assertRaises(ValueError):
            v.parse(self.out.replace(
                'ErdosPV0561.large_component_impossible (alpha beta D A B r : Nat)',''))

    def test_missing_ax_report_rejected(self):
        lines=[line for line in self.out.splitlines(keepends=True)
               if not line.startswith("'ErdosPV0561.factor_bounds'")]
        with self.assertRaises(ValueError):
            v.parse(''.join(lines))

    def test_false_successful_hostile_claim_rejected(self):
        fake=copy.deepcopy(self.r)
        fake['hostile']['omitted_edge_to_T_parity']['exit_code']=0
        with TemporaryDirectory() as td:
            file=Path(td)/'C_LEAN_CORE_REPLAY_001.json'
            file.write_text(json.dumps(fake))
            with patch.object(v,'RECEIPT',file),self.assertRaises(ValueError):
                v.verify()

    def test_no_full_factor_or_starforest_certification(self):
        for f in ('full_factor_theorem_kernel_checked',
                  'star_center_structural_hypotheses_kernel_checked',
                  'full_you_theorem_1_2_kernel_checked',
                  'original_erdos_561_conjecture_solved',
                  'mathcert_certified'):
            self.assertIs(self.r[f],False)
        self.assertIs(self.r['formalization_work_required'],True)

    def test_arithmetic_bridges_independent_integer_oracle(self):
        checked=0
        for alpha in range(2,11):
            for beta in range(2*(alpha+1),27):
                D=alpha+beta
                self.assertLess(D,alpha*beta)
                for r in range(1,25):
                    self.assertGreater(beta*(D+r-2)+2,beta*(r-1))
                    checked+=1
        self.assertGreater(checked,2500)

    def test_min_budget_identity_for_all_small_degrees(self):
        for d in range(60):
            for beta in range(60):
                g=max(0,d-beta)
                self.assertEqual(d-g,min(d,beta))
                for alpha in range(1,9):
                    if d<=alpha+beta:
                        self.assertEqual(g==alpha,d==alpha+beta)
                        for j in range(d+1):
                            self.assertEqual(g<=j<=alpha,
                                             j<=alpha and d-j<=beta)

    def test_odd_regular_n13_obstructs_false_unconditional_factor(self):
        n=13
        g=Graph(n,tuple((u,w) for u in range(n) for w in range(u+1,n)))
        self.assertEqual(g.degrees,(12,)*n)
        self.assertEqual(13*3%2,1)
        # Direct graph factor criterion has empty-cut parity obstruction.
        cut_ok,witness=cut_condition(g,3,9)
        self.assertFalse(cut_ok)
        self.assertEqual(witness[0],())
        self.assertEqual(witness[1],())
        self.assertEqual(witness[2]['q_D'],1)

if __name__ == '__main__':
    unittest.main()
