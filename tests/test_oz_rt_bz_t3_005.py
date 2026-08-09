#!/usr/bin/env python3
from __future__ import annotations
import copy,importlib.util,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; HERE=ROOT/'campaigns'/'odd_zeta'/'OZ_RT_BZ_T3_005'; sys.path.insert(0,str(HERE))
spec=importlib.util.spec_from_file_location('v',HERE/'validate.py'); v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
R=json.loads((HERE/'OZ_RT_BZ_T3_005.json').read_text()); S=json.loads((HERE/'SEARCH_RESULT.json').read_text()); J=v.jet_map.coefficient_map()
def reject(r=None,s=None,j=None):
    assert v.errors(R if r is None else r,S if s is None else s,J if j is None else j,run_independent=False)
class T3005MutationFirewall(unittest.TestCase):
    def test_mutation_firewall(self):
        self.assertEqual(v.errors(R,S,J,run_independent=False),[])
        x=copy.deepcopy(R); x['target_lock']['normalized_zero_form']='T1-top substituted'; reject(r=x)
        x=copy.deepcopy(R); x['stage_a_mirror_auxiliary']['external_shift']='k'; reject(r=x)
        x=copy.deepcopy(R); x['stage_a_mirror_auxiliary']['qk_boundary_factor']='1'; reject(r=x)
        x=copy.deepcopy(R); x['stage_a_mirror_auxiliary']['strongest_frontier']['rank']=1209; reject(r=x)
        x=copy.deepcopy(R); x['stage_b_one_body_linear_jet']['isolator']='nonlinear cumulant'; reject(r=x)
        x=copy.deepcopy(R); x['stage_c_nested_orientation_coupling']['both_nested_orientations_present']=False; reject(r=x)
        x=copy.deepcopy(R); x['stage_c_nested_orientation_coupling']['certified_parent_telescoper_for_full_jet']=True; reject(r=x)
        x=copy.deepcopy(R); x['nonclaims']['t3_proved']=True; reject(r=x)
        x=copy.deepcopy(R); x['disposition']['proof_effect']='T3_PROVED'; reject(r=x)
        j=copy.deepcopy(J); j['monomials'][0]['coefficient']='999'; reject(j=j)
        s=copy.deepcopy(S); s['stage_a']['search']['strongest_frontier']['nullity']=1; reject(s=s)
if __name__=='__main__': unittest.main()
