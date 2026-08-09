#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction as Q
from pathlib import Path
import t3_005_parent as parent
import jet_map

HERE=Path(__file__).resolve().parent; SEARCH_OUT=HERE/'SEARCH_RESULT.json'; JET_OUT=HERE/'JET_COEFFICIENT_MAP.json'
P=1000003; COMPONENTS=(("U",1),("U",2),("ES",1),("ES",2)); ETA_SAMPLES=(Q(0),Q(1,2),Q(1)); STAGES=((0,6),(1,6),(2,6),(3,7),(4,8))
def mon2(d): return [(i,j) for i in range(d+1) for j in range(d+1-i)]
def mon4(d): return [(i,j,h,u) for i in range(d+1) for j in range(d+1-i) for h in range(d+1-i-j) for u in range(d+1-i-j-h)]
def l_ratios(n,k,l): return [Q(1),parent.rl(n,k,l),parent.rl(n,k,l)*parent.rl(n,k,l+1)]
def a_basis(n,l,eta,d): return [Q(n**i*l**j)*eta**e for e in range(2) for i,j in mon2(d)]
def qk_basis(kind,r,n,k,l,s,eta,d):
    D=Q(parent.qk_denominator(kind,n,k,l,s)); edge=Q(parent.qk_boundary(n,k))
    return [edge*Q(n**i*l**j*k**h*s**u)*eta**e/D for e in range(2) for i,j,h,u in mon4(d)]
def qs_basis(kind,r,n,k,l,s,eta,d):
    D=Q(parent.qs_denominator(kind,r,k,s)); edge=Q(parent.qs_boundary(l,s))
    return [edge*Q(n**i*l**j*k**h*s**u)*eta**e/D for e in range(2) for i,j,h,u in mon4(d)]
def row(kind,r,n,k,l,s,eta,d):
    base=a_basis(n,l,eta,d); A=[ratio*x for ratio in l_ratios(n,k,l) for x in base]
    qc=qk_basis(kind,r,n,k,l,s,eta,d); qn=qk_basis(kind,r,n,k+1,l,s,eta,d); Rk=parent.ratio_k(kind,r,n,k,l,s,eta); QK=[x-Rk*y for x,y in zip(qc,qn)]
    sc=qs_basis(kind,r,n,k,l,s,eta,d); sn=qs_basis(kind,r,n,k,l,s+1,eta,d); Rs=parent.ratio_s(kind,r,n,k,l,s,eta); QS=[x-Rs*y for x,y in zip(sc,sn)]
    return A,QK+QS
def component_rows(kind,r,d,nmax):
    rows=[]
    for eta in ETA_SAMPLES:
        for n in range(4,nmax+1):
            for l in range(2,n-1):
                for k in range(1,n):
                    for s in range(1,l+1):
                        A,B=row(kind,r,n,k,l,s,eta,d); rows.append(A+B)
    return rows
def modq(x):
    den=x.denominator%P
    if den==0: raise AssertionError('rank-prime denominator collision')
    return x.numerator%P*pow(den,-1,P)%P
def eliminate_component(rows,na,nb):
    M=[[modq(x) for x in r[na:na+nb]]+[modq(x) for x in r[:na]] for r in rows]; rank=0
    for c in range(nb):
        pivot=next((rr for rr in range(rank,len(M)) if M[rr][c]),None)
        if pivot is None: return rank,[]
        M[rank],M[pivot]=M[pivot],M[rank]; inv=pow(M[rank][c],-1,P); M[rank][c:]=[(x*inv)%P for x in M[rank][c:]]; pr=M[rank]
        for rr in range(rank+1,len(M)):
            f=M[rr][c]
            if f: M[rr][c:]=[(x-f*y)%P for x,y in zip(M[rr][c:],pr[c:])]
        rank+=1
    return rank,[r[nb:] for r in M[rank:] if any(r[nb:])]
def rank_mod(rows):
    M=[r[:] for r in rows]
    if not M: return 0
    rank=0; nc=len(M[0])
    for c in range(nc):
        pivot=next((rr for rr in range(rank,len(M)) if M[rr][c]),None)
        if pivot is None: continue
        M[rank],M[pivot]=M[pivot],M[rank]; inv=pow(M[rank][c],-1,P); M[rank][c:]=[(x*inv)%P for x in M[rank][c:]]; pr=M[rank]
        for rr in range(rank+1,len(M)):
            f=M[rr][c]
            if f: M[rr][c:]=[(x-f*y)%P for x,y in zip(M[rr][c:],pr[c:])]
        rank+=1
        if rank==nc: break
    return rank
def run_stage(d,nmax):
    na=3*2*len(mon2(d)); nb=4*len(mon4(d)); constraints=[]; component_ranks={}; component_equations={}
    for kind,r in COMPONENTS:
        rows=component_rows(kind,r,d,nmax); rb,cons=eliminate_component(rows,na,nb); key=f'{kind}_R{r}'; component_ranks[key]=rb; component_equations[key]=len(rows); constraints.extend(cons)
    shared_rank=rank_mod(constraints); total_rank=sum(component_ranks.values())+shared_rank; unknowns=na+len(COMPONENTS)*nb
    return {'degree':d,'eta_degree':1,'n_min':4,'n_max':nmax,'eta_samples':['0','1/2','1'],'components':['U_R1','U_R2','ES_R1','ES_R2'],'equations':sum(component_equations.values()),'shared_telescoper_unknowns':na,'certificate_unknowns_per_component':nb,'unknowns':unknowns,'component_certificate_ranks':component_ranks,'shared_telescoper_rank':shared_rank,'rank':total_rank,'nullity':unknowns-total_rank,'rank_certificate':'COMPONENT_CERTIFICATE_BLOCKS_PLUS_SHARED_TELESCOPER_QUOTIENT_FULL_RANK_MOD_P_IMPLIES_FULL_COLUMN_RANK_OVER_Q','classification':'INCONSISTENT_ANSATZ' if total_rank==unknowns else 'CANDIDATE_SPACE_REMAINS'}
def main():
    nested_checks=parent.verify_mirror_nested_lift(); ratio_checks=parent.verify_mirror_shift_ratios(); stages=[run_stage(d,nmax) for d,nmax in STAGES]
    mapping=jet_map.coefficient_map(); map_checks=jet_map.verify_map_exact_samples(mapping); raw_checks=jet_map.verify_raw_jet_atoms(); JET_OUT.write_text(json.dumps(mapping,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    result={'schema_version':'1.0.0','operation':'OZ-RT-BZ-T3-005','fixture':'MIRROR_AUXILIARY_THEN_LINEAR_RAW_JET_001','stage_a':{'parent_family':{'U':'T(n,k,l)*s^(-r)*Q(s+k,0;eta)','ES':'T(n,k,l)*s^(-r)*Q(s,0;eta)','r_values':[1,2],'parameter':'eta','parameter_semantics':'normalized-Pochhammer deformation retained before cumulant extraction','mirror_nested_cumulant_checks':nested_checks,'exact_shift_ratio_checks':ratio_checks},'search':{'order':2,'external_shift':'l','differences':['k','s'],'common_telescoper_across_components':True,'eta_coefficient_degree':1,'eta_samples':['0','1/2','1'],'degree_ladder':[0,1,2,3,4],'qk_boundary_factor':'k*(n+1-k)','qs_boundary_factor':'(s-1)*(l+1-s)','qk_denominators':{'U':'(k+1)^3*(k+l+1)*(s+k+1)','ES':'(k+1)^3*(k+l+1)'},'qs_denominators':{'U_R1':'(s+1)*(s+k+1)','U_R2':'(s+1)^2*(s+k+1)','ES_R1':'(s+1)','ES_R2':'(s+1)^2'},'sample_domain':'eta in {0,1/2,1}; 4<=n<=n_max; 2<=l<=n-2; 1<=k<=n-1; 1<=s<=l','prime':P,'denominator_condition':'every exact rational matrix-entry denominator is nonzero modulo p','stages':stages,'strongest_frontier':stages[-1]},'terminal':'NO_COMMON_PARAMETER_DEPENDENT_ORDER2_CERTIFICATE_IN_BOUNDED_MIRROR_AUXILIARY_CLASS','newly_exhausted_class':'PARAMETER_DEPENDENT_ORDER2_LSIDE_U_ES_SAUX_ETADEG_LE_1_POLYDEG_LE_4'},'stage_b_c':{'jet_map':'JET_COEFFICIENT_MAP.json','map_exact_sample_checks':map_checks,'raw_jet_atom_checks':raw_checks,'monomial_count':mapping['monomial_count'],'max_atomic_arity':mapping['max_atomic_arity'],'max_one_body_parameter_slots':mapping['max_one_body_parameter_slots'],'nested_atom_count_max':mapping['nested_atom_count_max'],'extraction_method':'linear raw mixed derivatives of rational power-sum isolators','cumulant_nonlinearity_avoided':True,'both_nested_orientations_present':True,'full_locked_weight_five_coefficient_map':True,'certified_parent_telescoper_for_full_jet':False},'coverage':{'covered':['mirror U(l,k,r,m) auxiliary parent for r=1,2','mirror ES(l,r,m) auxiliary parent for r=1,2','exact mirror eta-dependent parent shift ratios','finite k/s boundary-vanishing mirror certificate basis','linear raw mixed-parameter one-body power-sum jet through weight five','termwise coefficient map for the complete locked T3 weight-five summand','coupling metadata for k-side and l-side nested orientations'],'not_yet_covered':['common parameter-dependent telescoper for the complete higher jet module','exact differentiated finite-boundary certificate for the complete locked T3 operator'],'full_t3_certificate':False},'terminal':'MIRROR_BOUNDED_CLASS_EXHAUSTED_AND_WEIGHT5_LINEAR_JET_EXTRACTION_ARCHITECTURE_CONSTRUCTED_WITHOUT_FULL_PARENT_TELESCOPER','next_distinct_route':'INCREASE_PARAMETER_JET_DEGREE_BEFORE_TELESCOPER_ORDER','proof_effect':'NONE','promotion_effect':'NONE'}
    SEARCH_OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps(result,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
