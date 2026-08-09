from __future__ import annotations
import copy, importlib.util, json
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]/'campaigns'/'odd_zeta'/'OZ_RT_BZ_T3_003'
spec=importlib.util.spec_from_file_location('oz_t3_003_validate',HERE/'validate.py')
mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod)
record=json.loads((HERE/'OZ_RT_BZ_T3_003.json').read_text())
result=json.loads((HERE/'SEARCH_RESULT.json').read_text())

def mutated(path,value):
    x=copy.deepcopy(record); cur=x
    for key in path[:-1]: cur=cur[key]
    cur[path[-1]]=value
    return x

def test_valid_package(): assert mod.errors()==[]
def test_reject_source_head_drift(): assert mod.errors(mutated(['authority','admitted_source_head'],'deadbeef'),result)
def test_reject_t1_substitution_firewall_removal(): assert mod.errors(mutated(['target_lock','t1top_substitution_forbidden'],False),result)
def test_reject_parameter_lift_support_drift(): assert mod.errors(mutated(['parameter_lift','supported_atoms'],['H']),result)
def test_reject_l_shift_tautology_orientation(): assert mod.errors(mutated(['search_execution','relation'],'sum a_j F(n,k,l+j) = Delta_l R'),result)
def test_reject_rank_mutation():
    y=copy.deepcopy(result); y['strongest_frontier']['rank']=128; assert mod.errors(record,y)
def test_reject_proof_inflation():
    y=copy.deepcopy(result); y['proof_effect']='T3_PROVED'; assert mod.errors(record,y)
def test_reject_disposition_inflation(): assert mod.errors(mutated(['disposition','proof_found'],True),result)
def test_reject_refutation_inflation(): assert mod.errors(mutated(['disposition','characterized_blocker','not_a_refutation'],False),result)
def test_reject_nonclaim_promotion(): assert mod.errors(mutated(['nonclaims','t3_proved'],True),result)
