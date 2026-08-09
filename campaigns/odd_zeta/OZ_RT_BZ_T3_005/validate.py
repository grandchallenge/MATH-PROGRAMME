#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
from jsonschema import Draft202012Validator
import jet_map, verify_rank
HERE=Path(__file__).resolve().parent
R=json.loads((HERE/'OZ_RT_BZ_T3_005.json').read_text()); S=json.loads((HERE/'SEARCH_RESULT.json').read_text()); SC=json.loads((HERE/'OZ_RT_BZ_T3_005.schema.json').read_text())
def digest(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def errors(record=R,result=S,mapping=None,run_independent=True):
 out=[f'schema{e.json_path}: {e.message}' for e in Draft202012Validator(SC).iter_errors(record)]; mapping=jet_map.coefficient_map() if mapping is None else mapping
 a=record.get('authority',{}); exp={'issue':341,'predecessor_issue':332,'predecessor_pr':337,'predecessor_merge':'941fa3b2003327fc6f540d8da73b329baf7340ae','programme_base_commit':'941fa3b2003327fc6f540d8da73b329baf7340ae','programme_base_tree':'2353d13de3cf3a0fe28758da17204766344c52bf','admitted_source_head':'6cc0bf07137815ceeef0d9f340559f85352391e5','admitted_source_tree':'be780558454b704bdd016a3070d698c2e106e2b8'}
 for k,v in exp.items():
  if a.get(k)!=v: out.append(f'authority drift: {k}')
 t=record.get('target_lock',{})
 if 'W1(k,l)+2*w5_sym(n,k,l)' not in t.get('normalized_zero_form','') or not t.get('t1top_substitution_forbidden'): out.append('T3 target drift')
 A=record.get('stage_a_mirror_auxiliary',{})
 if A.get('external_shift')!='l' or A.get('differences')!=['k','s'] or A.get('degree_ladder')!=[0,1,2,3,4]: out.append('mirror orientation drift')
 if A.get('qk_boundary_factor')!='k*(n+1-k)' or A.get('qs_boundary_factor')!='(s-1)*(l+1-s)': out.append('mirror boundary drift')
 f=A.get('strongest_frontier',{})
 if (f.get('rank'),f.get('unknowns'),f.get('nullity'),f.get('equations'))!=(1210,1210,0,3540): out.append('mirror frontier drift')
 sa=result.get('stage_a',{}); sr=sa.get('search',{})
 if sa.get('newly_exhausted_class')!='PARAMETER_DEPENDENT_ORDER2_LSIDE_U_ES_SAUX_ETADEG_LE_1_POLYDEG_LE_4': out.append('mirror class drift')
 if sr.get('external_shift')!='l' or sr.get('differences')!=['k','s'] or sr.get('strongest_frontier')!=f: out.append('retained mirror result drift')
 if result.get('next_distinct_route')!='COUPLED_WEIGHT5_RAW_JET_ORDER2_SEARCH_001': out.append('next route drift')
 B=record.get('stage_b_one_body_linear_jet',{})
 if B.get('isolator')!='P_r(L,o;z)=prod_{i=1}^L(1-(-z/(o+i))^r)' or B.get('monomial_count')!=198: out.append('linear jet drift')
 if digest(mapping)!='c7408f49732c8bcdbabe83f442db3476153a4f99619dcab159236c0556e6edd2': out.append('jet map digest drift')
 if digest(result)!='690db8372fc054518d5c0ac8fe88e03f3a3424071562b7b7c68c3b138a33dd84': out.append('search digest drift')
 C=record.get('stage_c_nested_orientation_coupling',{})
 if not C.get('both_nested_orientations_present') or C.get('certified_parent_telescoper_for_full_jet') or C.get('differentiated_boundary_certificate_complete'): out.append('coupling/proof boundary drift')
 d=record.get('disposition',{})
 if d.get('status')!='OPEN_WITH_CHARACTERIZED_BLOCKER' or d.get('proof_effect')!='NONE' or d.get('promotion_effect')!='NONE' or d.get('proof_found') or d.get('counterexample_found'): out.append('disposition inflation')
 if d.get('characterized_blocker',{}).get('next_distinct_route')!='COUPLED_WEIGHT5_RAW_JET_ORDER2_SEARCH_001': out.append('record next route drift')
 if any(record.get('nonclaims',{}).values()): out.append('nonclaim promoted')
 if run_independent and not out:
  for got,(deg,nmax) in zip(sr.get('stages',[]),((0,6),(1,6),(2,6),(3,7),(4,8))):
   x=verify_rank.stage(deg,nmax)
   for key in ('equations','component_certificate_ranks','shared_telescoper_rank','rank','unknowns','nullity'):
    if got.get(key)!=x.get(key): out.append(f'independent rank replay drift: d={deg} {key}')
  if jet_map.verify_map_exact_samples(mapping)!=135 or jet_map.verify_raw_jet_atoms()!=3526: out.append('independent jet replay drift')
 return out
def main():
 e=errors()
 if e: print('\n'.join(e),file=sys.stderr); return 1
 print('OZ-RT-BZ-T3-005 mirror auxiliary exhaustion and linear weight-five jet coupling package are valid'); return 0
if __name__=='__main__': raise SystemExit(main())
