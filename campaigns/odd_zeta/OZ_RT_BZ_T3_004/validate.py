#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator
HERE=Path(__file__).resolve().parent
RECORD=HERE/'OZ_RT_BZ_T3_004.json'; SCHEMA=HERE/'OZ_RT_BZ_T3_004.schema.json'; RESULT=HERE/'SEARCH_RESULT.json'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def canonical_sha256(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def errors(record=None,result=None):
    record=load(RECORD) if record is None else record; result=load(RESULT) if result is None else result
    out=[f'schema{e.json_path}: {e.message}' for e in Draft202012Validator(load(SCHEMA)).iter_errors(record)]
    a=record.get('authority',{})
    exp={'issue':332,'programme_base_commit':'f38dfe5ffc212dadb70ecc5fec0bdf48366e3a35','predecessor_merge':'f38dfe5ffc212dadb70ecc5fec0bdf48366e3a35','admitted_source_head':'6cc0bf07137815ceeef0d9f340559f85352391e5','admitted_source_tree':'be780558454b704bdd016a3070d698c2e106e2b8'}
    for k,v in exp.items():
        if a.get(k)!=v: out.append(f'authority drift: {k}')
    blobs={'statement':'da46db62471fbed81d861772c1d2d03d80782e23','bridge':'002c96d28123e5949c38656f26677ae5a723ee93','finite_verifier':'be458d969e1f8c989c8007a2b181506f84fd7f48','recurrence':'9495275bc31e5a8f535c68f027f3b24d12c07ae1'}
    for k,v in blobs.items():
        if a.get('source_loci',{}).get(k,{}).get('blob')!=v: out.append(f'source blob drift: {k}')
    t=record.get('target_lock',{})
    if 'W1(k,l)+2*w5_sym(n,k,l)' not in t.get('normalized_zero_form',''): out.append('T3 representative drift')
    if not t.get('t1top_substitution_forbidden'): out.append('T1-top substitution firewall removed')
    if t.get('finite_evidence_theorem_effect')!='NONE': out.append('finite evidence promoted')
    pp=record.get('parameter_parent',{})
    if pp.get('parameter')!='eta' or pp.get('eta_coefficient_degree')!=1: out.append('parameter-dependence drift')
    if not pp.get('explicit_auxiliary_t_dimension'): out.append('auxiliary t dimension collapsed')
    if pp.get('components')!=['U_R1','U_R2','ES_R1','ES_R2']: out.append('auxiliary component coverage drift')
    if pp.get('nested_cumulant_checks')!=360 or pp.get('exact_shift_ratio_checks')!=2556: out.append('parent replay count drift')
    if pp.get('proof_effect')!='NONE': out.append('parameter parent promoted')
    s=record.get('search_execution',{})
    if s.get('result_sha256')!=canonical_sha256(result): out.append('search result digest drift')
    if s.get('order')!=2 or s.get('external_shift')!='k' or s.get('differences')!=['l','t']: out.append('telescoper orientation drift')
    if s.get('degree_ladder')!=[0,1,2,3,4] or s.get('eta_samples')!=['0','1/2','1']: out.append('bounded ladder drift')
    if s.get('ql_boundary_factor')!='l*(n+1-l)' or s.get('qt_boundary_factor')!='(t-1)*(k+1-t)': out.append('finite-boundary factor drift')
    if s.get('rank_prime')!=1000003 or s.get('stage_count')!=5: out.append('rank protocol drift')
    if s.get('search_class')!='PARAMETER_DEPENDENT_ORDER2_KSIDE_U_ES_TAUX_ETADEG_LE_1_POLYDEG_LE_4': out.append('search-class drift')
    frontier={'degree':4,'eta_degree':1,'n_min':4,'n_max':8,'eta_samples':['0','1/2','1'],'components':['U_R1','U_R2','ES_R1','ES_R2'],'equations':3540,'shared_telescoper_unknowns':90,'certificate_unknowns_per_component':280,'unknowns':1210,'component_certificate_ranks':{'U_R1':280,'U_R2':280,'ES_R1':280,'ES_R2':280},'shared_telescoper_rank':90,'rank':1210,'nullity':0,'rank_certificate':'COMPONENT_CERTIFICATE_BLOCKS_PLUS_SHARED_TELESCOPER_QUOTIENT_FULL_RANK_MOD_P_IMPLIES_FULL_COLUMN_RANK_OVER_Q','classification':'INCONSISTENT_ANSATZ'}
    if s.get('strongest_frontier')!=frontier: out.append('strongest frontier drift')
    search=result.get('search',{})
    if len(search.get('stages',[]))!=5: out.append('retained stage ledger drift')
    if search.get('strongest_frontier')!=frontier: out.append('retained result frontier drift')
    if result.get('terminal')!='NO_COMMON_PARAMETER_DEPENDENT_ORDER2_CERTIFICATE_IN_BOUNDED_K_SIDE_AUXILIARY_CLASS': out.append('search terminal drift')
    if result.get('newly_exhausted_class')!='PARAMETER_DEPENDENT_ORDER2_KSIDE_U_ES_TAUX_ETADEG_LE_1_POLYDEG_LE_4': out.append('result exhausted-class drift')
    if result.get('next_distinct_route')!='MIRROR_TRIANGULAR_AUXILIARY_MODULE_THEN_ONE_BODY_JET_COUPLING': out.append('result next-route drift')
    if result.get('proof_effect')!='NONE' or result.get('promotion_effect')!='NONE': out.append('search effect inflation')
    cov=record.get('coverage',{})
    if cov.get('full_t3_certificate'): out.append('partial auxiliary module promoted to full T3 certificate')
    if len(cov.get('not_yet_covered',[]))<3: out.append('coverage blockers erased')
    d=record.get('disposition',{}); b=d.get('characterized_blocker',{})
    if d.get('status')!='OPEN_WITH_CHARACTERIZED_BLOCKER' or d.get('proof_found') or d.get('counterexample_found'): out.append('disposition inflation')
    if d.get('proof_effect')!='NONE' or d.get('promotion_effect')!='NONE': out.append('disposition effect inflation')
    if b.get('newly_exhausted_class')!='PARAMETER_DEPENDENT_ORDER2_KSIDE_U_ES_TAUX_ETADEG_LE_1_POLYDEG_LE_4': out.append('blocker class drift')
    if b.get('next_distinct_route')!='MIRROR_TRIANGULAR_AUXILIARY_MODULE_THEN_ONE_BODY_JET_COUPLING': out.append('blocker next-route drift')
    if not b.get('not_a_refutation'): out.append('negative search inflated toward refutation')
    if any(record.get('nonclaims',{}).values()): out.append('nonclaim promoted')
    if out: return out
    spec=importlib.util.spec_from_file_location('oz_t3_004_verify',HERE/'verify.py'); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod)
    return ['independent verifier: '+x for x in mod.verify(result)]
def main():
    e=errors()
    if e: print('\n'.join(e),file=sys.stderr); return 1
    print('OZ-RT-BZ-T3-004 parameter-dependent auxiliary-t frontier and independent verification are valid'); return 0
if __name__=='__main__': raise SystemExit(main())
