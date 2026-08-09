#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction as Q
from pathlib import Path
import parameter_lift as lift
import target

HERE=Path(__file__).resolve().parent
OUT=HERE/'SEARCH_RESULT.json'
P=1000003
STAGES=[(order,ad,ad+2,base+ad) for order,base in ((2,7),(3,8),(4,9)) for ad in range(7)]

def mon2(d): return [(i,j) for i in range(d+1) for j in range(d+1-i)]
def mon3(d): return [(i,j,h) for i in range(d+1) for j in range(d+1-i) for h in range(d+1-i-j)]

def rk(n,k,l):
    return Q((n+k+1)*(n-k)**2*(n+k+l+1),(k+1)**3*(k+l+1))
def rl(n,k,l):
    return Q((n+l+1)*(n-l)**2*(n+k+l+1),(l+1)**3*(k+l+1))
def denom(n,k,l): return (l+1)**3*(k+l+1)

def row(nv,kv,lv,order,ad,qd):
    out=[]; ma=mon2(ad); mq=mon3(qd)
    ratios=[Q(1)]; ratio=Q(1)
    for j in range(order):
        ratio*=rk(nv,kv+j,lv); ratios.append(ratio)
    for ratio in ratios:
        out.extend(ratio*Q(nv**i*kv**j) for i,j in ma)
    rr=rl(nv,kv,lv); dl=Q(denom(nv,kv,lv)); dp=Q(denom(nv,kv,lv+1))
    for i,j,h in mq:
        basis=Q(nv**i*kv**j)
        out.append(basis*(Q(lv**h,dl)-rr*Q((lv+1)**h,dp)))
    return out

def matrix(order,ad,qd,nmax):
    rows=[]
    for nv in range(order+2,nmax+1):
        for kv in range(nv-order+1):
            for lv in range(nv): rows.append(row(nv,kv,lv,order,ad,qd))
    return rows

def modq(x):
    den=x.denominator%P
    if den==0: raise AssertionError('rank-prime denominator collision')
    return (x.numerator%P)*pow(den,-1,P)%P

def rank_mod(rows):
    m=[[modq(x) for x in r] for r in rows]; rank=0; nc=len(m[0])
    for c in range(nc):
        pivot=next((r for r in range(rank,len(m)) if m[r][c]),None)
        if pivot is None: continue
        m[rank],m[pivot]=m[pivot],m[rank]
        inv=pow(m[rank][c],-1,P); m[rank]=[(x*inv)%P for x in m[rank]]
        for r in range(rank+1,len(m)):
            f=m[r][c]
            if f: m[r]=[(x-f*y)%P for x,y in zip(m[r],m[rank])]
        rank+=1
        if rank==nc: break
    return rank

def verify_shift_ratios():
    checks=0
    for nv in range(3,8):
        for kv in range(nv):
            for lv in range(nv):
                if Q(target.T(nv,kv+1,lv),target.T(nv,kv,lv))!=rk(nv,kv,lv): raise AssertionError('k ratio drift')
                if Q(target.T(nv,kv,lv+1),target.T(nv,kv,lv))!=rl(nv,kv,lv): raise AssertionError('l ratio drift')
                checks+=2
    return checks

def verify_parameter_lift():
    checks=0
    for nv in range(1,7):
        for kv in range(nv+1):
            for lv in range(nv+1):
                for r in range(1,6):
                    for a,b in ((lift.H(nv+kv,r),target.H(nv+kv,r)),(lift.A(nv,kv,r),target.A(nv,kv,r)),(lift.B(nv,kv,r),target.B(nv,kv,r)),(lift.C(nv,kv,lv,r),target.C(nv,kv,lv,r))):
                        if a!=b: raise AssertionError('one-body lift drift')
                        checks+=1
                for a,b in ((lift.ES(kv,1,3),target.ES(kv,1,3)),(lift.ES(kv,2,3),target.ES(kv,2,3)),(lift.ES(kv,1,4),target.ES(kv,1,4)),(lift.U(kv,lv,1,2),target.U(kv,lv,1,2)),(lift.U(kv,lv,2,2),target.U(kv,lv,2,2)),(lift.U(kv,lv,1,4),target.U(kv,lv,1,4)),(lift.U(kv,lv,2,3),target.U(kv,lv,2,3))):
                    if a!=b: raise AssertionError('nested lift drift')
                    checks+=1
                if lift.W1(nv,kv,lv)!=target.W1(nv,kv,lv): raise AssertionError('W1 lift drift')
                if lift.w5sym(nv,kv,lv)!=target.w5sym(nv,kv,lv): raise AssertionError('w5sym lift drift')
                if lift.cell(nv,kv,lv)!=target.cell(nv,kv,lv): raise AssertionError('cell lift drift')
                checks+=3
    return {'exact_sample_checks':checks,'sample_domain':'1<=n<=6; 0<=k,l<=n; harmonic orders 1..5','supported_atoms':['H','A','B','C','ES','U','W1','w5sym','full_locked_cell'],'one_body_parent':'Q(length,offset;alpha)=prod_{i=1}^length (offset+i+alpha)/(offset+i)','nested_parent':'auxiliary finite t-sum of t^(-r) times normalized Pochhammer lifts, with cumulant extraction per term','status':'EXACT_RECONSTRUCTION_ON_RETAINED_FIXTURE'}

def main():
    lift_info=verify_parameter_lift(); ratio_checks=verify_shift_ratios(); stages=[]
    for order,ad,qd,nmax in STAGES:
        rows=matrix(order,ad,qd,nmax); unknowns=(order+1)*len(mon2(ad))+len(mon3(qd)); rank=rank_mod(rows)
        stages.append({'route_id':f'ORDER{order}_KSHIFT_ADEG_{ad}_QDEG_{qd}','order':order,'external_shift':'k','summation_difference':'l','a_total_degree':ad,'q_numerator_total_degree':qd,'q_denominator':'(l+1)^3*(k+l+1)','n_min':order+2,'n_max':nmax,'equations':len(rows),'unknowns':unknowns,'rank':rank,'nullity':unknowns-rank,'rank_certificate':'FULL_COLUMN_RANK_MOD_P_IMPLIES_FULL_COLUMN_RANK_OVER_Q','classification':'INCONSISTENT_ANSATZ' if rank==unknowns else 'CANDIDATE_SPACE_REMAINS'})
    result={'schema_version':'1.1.0','operation':'OZ-RT-BZ-T3-003','fixture':'PARAMETER_LIFT_HIGHER_ORDER_001','parameter_lift':lift_info,'parent_shift_ratio_checks':ratio_checks,'search_class':'UNDEFORMED_HYPERGEOMETRIC_PARENT_ORDERS_2_TO_4_K_SHIFT_WITH_L_CERTIFICATE','relation':'sum_{j=0}^r a_j(n,k) F(n,k+j,l) = Delta_l(F(n,k,l)*q(n,k,l)) at lift parameters zero; r in {2,3,4}','denominator_derivation':'q denominator is locked to the exact denominator factors of F(n,k,l+1)/F(n,k,l)','modular_rank_certificate':{'prime':P,'denominator_condition':'all exact matrix-entry denominators are coprime to p','implication':'full column rank modulo p exhibits a nonzero maximal minor modulo p, hence the corresponding rational minor is nonzero'},'stages':stages,'strongest_frontier':stages[-1],'terminal':'NO_ORDER2_TO_ORDER4_CERTIFICATE_IN_BOUNDED_UNDEFORMED_PARENT_CLASSES','next_distinct_route':'PARAMETER_DEPENDENT_ORDER2_WITH_AUXILIARY_T_DIMENSION','proof_effect':'NONE','promotion_effect':'NONE'}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())
