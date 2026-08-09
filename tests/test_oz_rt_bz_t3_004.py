from __future__ import annotations
import copy, importlib.util, json, unittest
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]/'campaigns'/'odd_zeta'/'OZ_RT_BZ_T3_004'
spec=importlib.util.spec_from_file_location('oz_t3_004_validate',HERE/'validate.py'); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod)
record=json.loads((HERE/'OZ_RT_BZ_T3_004.json').read_text()); result=json.loads((HERE/'SEARCH_RESULT.json').read_text())
def mutated(path,value):
    x=copy.deepcopy(record); cur=x
    for key in path[:-1]: cur=cur[key]
    cur[path[-1]]=value; return x
class T3ParameterDependentAuxTests(unittest.TestCase):
    def test_valid_package(self): self.assertEqual(mod.errors(),[])
    def test_reject_source_drift(self): self.assertTrue(mod.errors(mutated(['authority','admitted_source_head'],'deadbeef'),result))
    def test_reject_t_dimension_collapse(self): self.assertTrue(mod.errors(mutated(['parameter_parent','explicit_auxiliary_t_dimension'],False),result))
    def test_reject_parameter_drop(self): self.assertTrue(mod.errors(mutated(['parameter_parent','eta_coefficient_degree'],0),result))
    def test_reject_component_drop(self): self.assertTrue(mod.errors(mutated(['parameter_parent','components'],['U_R1']),result))
    def test_reject_l_boundary_drift(self): self.assertTrue(mod.errors(mutated(['search_execution','ql_boundary_factor'],'1'),result))
    def test_reject_t_boundary_drift(self): self.assertTrue(mod.errors(mutated(['search_execution','qt_boundary_factor'],'1'),result))
    def test_reject_rank_mutation(self):
        y=copy.deepcopy(result); y['search']['strongest_frontier']['rank']=1209; self.assertTrue(mod.errors(record,y))
    def test_reject_search_proof_inflation(self):
        y=copy.deepcopy(result); y['proof_effect']='T3_PROVED'; self.assertTrue(mod.errors(record,y))
    def test_reject_refutation_inflation(self): self.assertTrue(mod.errors(mutated(['disposition','characterized_blocker','not_a_refutation'],False),result))
    def test_reject_partial_to_full_certificate(self): self.assertTrue(mod.errors(mutated(['coverage','full_t3_certificate'],True),result))
    def test_reject_nonclaim_promotion(self): self.assertTrue(mod.errors(mutated(['nonclaims','t3_proved'],True),result))
if __name__=='__main__': unittest.main()
