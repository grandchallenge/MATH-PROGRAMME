from __future__ import annotations
import copy, importlib.util, json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'campaigns/odd_zeta/OZ_RT_BZ_T3_002'
spec=importlib.util.spec_from_file_location('t3v',P/'validate.py'); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod)
class T3SearchTests(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((P/'OZ_RT_BZ_T3_002.json').read_text()); self.s=json.loads((P/'SEARCH_RESULT.json').read_text())
    def test_valid(self): self.assertEqual(mod.errors(self.r,self.s),[])
    def test_proof_inflation(self):
        b=copy.deepcopy(self.r); b['disposition']['proof_found']=True; self.assertTrue(mod.errors(b,self.s))
    def test_rank_mutation(self):
        s=copy.deepcopy(self.s); s['stages'][-1]['rank']=55; self.assertTrue(mod.errors(self.r,s))
    def test_source_drift(self):
        b=copy.deepcopy(self.r); b['authority']['source_loci']['weights']['blob']='0'*40; self.assertTrue(mod.errors(b,self.s))
    def test_representative_substitution(self):
        b=copy.deepcopy(self.r); b['target_lock']['normalized_zero_form']=b['target_lock']['normalized_zero_form'].replace('w5_sym','w5_I'); self.assertTrue(mod.errors(b,self.s))
    def test_degree_ladder_drift(self):
        b=copy.deepcopy(self.r); b['search_execution']['degree_ladder']=[0,1,2]; self.assertTrue(mod.errors(b,self.s))
    def test_finite_promotion(self):
        b=copy.deepcopy(self.r); b['target_lock']['finite_evidence_theorem_effect']='PROOF'; self.assertTrue(mod.errors(b,self.s))
    def test_nonclaim_promotion(self):
        b=copy.deepcopy(self.r); b['nonclaims']['t3_proved']=True; self.assertTrue(mod.errors(b,self.s))
if __name__=='__main__': unittest.main()
