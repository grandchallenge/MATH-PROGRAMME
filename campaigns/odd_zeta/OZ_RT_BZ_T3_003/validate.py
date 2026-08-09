#!/usr/bin/env python3
from __future__ import annotations
import hashlib, importlib.util, json, sys
from pathlib import Path
from jsonschema import Draft202012Validator

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
RECORD=HERE/'OZ_RT_BZ_T3_003.json'; SCHEMA=HERE/'OZ_RT_BZ_T3_003.schema.json'; RESULT=HERE/'SEARCH_RESULT.json'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def canonical_sha256(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def errors(record=None,result=None):
    record=load(RECORD) if record is None else record; result=load(RESULT) if result is None else result
    out=[f'schema{e.json_path}: {e.message}' for e in Draft202012Validator(load(SCHEMA)).iter_errors(record)]
    a=record.get('authority',{})
    expected={'issue':328,'programme_base_commit':'d9ddba678f22acdec13f016e08d8fe8a73e66dd3','predecessor_merge':'1f7953f0ab98f5ca578cfc8e42b0a7cfb30e5996','admitted_source_head':'6cc0bf07137815ceeef0d9f340559f85352391e5','admitted_source_tree':'be780558454b704bdd016a3070d698c2e106e2b8'}
    for k,v in expected.items():
        if a.get(k)!=v: out.append(f'authority drift: {k}')
    blobs={'statement':'da46db62471fbed81d861772c1d2d03d80782e23','bridge':'002c96d28123e5949c38656f26677ae5a723ee93','finite_verifier':'be458d969e1f8c989c8007a2b181506f84fd7f48','recurrence':'9495275bc31e5a8f535c68f027f3b24d12c07ae1'}
    for k,v in blobs.items():
        if a.get('source_loci',{}).get(k,{}).get('blob')!=v: out.append(f'source blob drift: {k}')
    t=record.get('target_lock',{})
    if 'W1(k,l)+2*w5_sym(n,k,l)' not in t.get('normalized_zero_form',''): out.append('T3 representative drift')
    if not t.get('t1top_substitution_forbidden'): out.append('T1-top substitution firewall removed')
    if t.get('finite_evidence_theorem_effect')!='NONE': out.append('finite evidence promoted')
    pl=record.get('parameter_lift',{})
    if pl.get('status')!='FULL_LOCKED_CELL_RECONSTRUCTED_ON_RETAINED_EXACT_FIXTURE': out.append('parameter-lift status drift')
    if pl.get('supported_atoms')!=['H','A','B','C','ES','U','W1','w5sym','full_locked_cell']: out.append('parameter-lift support drift')
    if pl.get('proof_effect')!='NONE': out.append('parameter-lift fixture promoted')
    search=record.get('search_execution',{})
    if search.get('result_sha256')!=canonical_sha256(result): out.append('search result digest drift')
    if search.get('search_class')!='UNDEFORMED_HYPERGEOMETRIC_PARENT_ORDER2_K_SHIFT_WITH_L_CERTIFICATE': out.append('search-class drift')
    if 'F(n,k+j,l)' not in search.get('relation','') or 'Delta_l' not in search.get('relation',''): out.append('creative-telescoping orientation drift')
    if search.get('q_denominator')!='(l+1)^3*(k+l+1)': out.append('denominator-family drift')
    expected_front={'a_total_degree':4,'q_numerator_total_degree':6,'n_max':11,'equations':432,'unknowns':129,'rank':129,'nullity':0}
    if search.get('strongest_frontier')!=expected_front: out.append('strongest frontier drift')
    if result.get('strongest_frontier',{}).get('rank')!=129 or result.get('strongest_frontier',{}).get('nullity')!=0: out.append('retained result frontier drift')
    if result.get('terminal')!='NO_ORDER2_CERTIFICATE_IN_BOUNDED_UNDEFORMED_PARENT_CLASS': out.append('search terminal drift')
    if result.get('proof_effect')!='NONE' or result.get('promotion_effect')!='NONE': out.append('search effect inflation')
    d=record.get('disposition',{}); blocker=d.get('characterized_blocker',{})
    if d.get('status')!='OPEN_WITH_CHARACTERIZED_BLOCKER' or d.get('proof_found') or d.get('counterexample_found'): out.append('disposition inflation')
    if blocker.get('newly_exhausted_class')!='UNDEFORMED_PARENT_ORDER2_K_SHIFT_DSHIFT_DENOM_ADEG_LE_4_QDEG_LE_6': out.append('exhausted-class drift')
    if not blocker.get('not_a_refutation'): out.append('negative search inflated toward refutation')
    if blocker.get('next_distinct_route')!='PARAMETER_DEPENDENT_ORDER2_WITH_AUXILIARY_T_DIMENSION_THEN_ORDER3_ORDER4': out.append('next-route drift')
    if d.get('proof_effect')!='NONE' or d.get('promotion_effect')!='NONE': out.append('disposition effect inflation')
    if any(record.get('nonclaims',{}).values()): out.append('nonclaim promoted')
    if out: return out
    spec=importlib.util.spec_from_file_location('oz_t3_003_verify',HERE/'verify.py'); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod)
    return ['independent verifier: '+x for x in mod.verify(result)]

def main():
    e=errors()
    if e: print('\n'.join(e),file=sys.stderr); return 1
    print('OZ-RT-BZ-T3-003 parameter lift, order-2 search frontier, and independent verification are valid'); return 0
if __name__=='__main__': raise SystemExit(main())
