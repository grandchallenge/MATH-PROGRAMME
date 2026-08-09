#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction as Q
from functools import lru_cache
from math import comb, factorial
from pathlib import Path
HERE=Path(__file__).resolve().parent; RESULT=HERE/'SEARCH_RESULT.json'; P=1000003
COMPONENTS=(("ES",2),("ES",1),("U",2),("U",1)); ETA_SAMPLES=(Q(1),Q(1,2),Q(0))
@lru_cache(None)
def hsum(m,r): return sum((Q(1,j**r) for j in range(1,m+1)),Q(0))
def poch(length,eta):
    out=Q(1)
    for j in range(length,0,-1): out*=(Q(j)+eta)/Q(j)
    return out
def cumulant(length,order): return Q((-1)**(order-1)*factorial(order-1))*hsum(length,order)
def atom(length,order): return Q((-1)**(order-1),factorial(order-1))*cumulant(length,order)
def kernel(n,k,l): return comb(n+k,n)*comb(n,k)**2*comb(n+l,n)*comb(n,l)**2*comb(n+k+l,n)
def Rk(n,k,l): return Q((n+k+1)*(n-k)**2*(n+k+l+1),(k+1)**3*(k+l+1))
def Rl(kind,n,k,l,t,eta):
    x=Q((n+l+1)*(n-l)**2*(n+k+l+1),(l+1)**3*(k+l+1))
    if kind=="U": x*=(Q(t+l+1)+eta)/Q(t+l+1)
    return x
def Rt(kind,r,l,t,eta):
    x=Q(t**r,(t+1)**r); z=t+l+1 if kind=="U" else t+1
    return x*(Q(z)+eta)/Q(z)
def pval(kind,r,n,k,l,t,eta):
    length=t+l if kind=="U" else t
    return Q(kernel(n,k,l),t**r)*poch(length,eta)
def check_parent():
    nested=0
    for k in range(1,6):
        for l in range(6):
            for r in (1,2):
                for m in (2,3,4):
                    u=sum((atom(t+l,m)/Q(t**r) for t in range(1,k+1)),Q(0)); ud=sum((hsum(t+l,m)/Q(t**r) for t in range(1,k+1)),Q(0))
                    e=sum((atom(t,m)/Q(t**r) for t in range(1,k+1)),Q(0)); ed=sum((hsum(t,m)/Q(t**r) for t in range(1,k+1)),Q(0))
                    if u!=ud or e!=ed: return False,nested,0
                    nested+=2
    shifts=0
    for kind,r in COMPONENTS:
        for eta in ETA_SAMPLES:
            for n in range(4,7):
                for k in range(2,n-1):
                    for l in range(1,n):
                        for t in range(1,k+1):
                            g=pval(kind,r,n,k,l,t,eta)
                            if pval(kind,r,n,k+1,l,t,eta)/g!=Rk(n,k,l): return False,nested,shifts
                            if pval(kind,r,n,k,l+1,t,eta)/g!=Rl(kind,n,k,l,t,eta): return False,nested,shifts
                            if pval(kind,r,n,k,l,t+1,eta)/g!=Rt(kind,r,l,t,eta): return False,nested,shifts
                            shifts+=3
    return True,nested,shifts
def mon2(d): return [(i,j) for i in range(d,-1,-1) for j in range(d-i,-1,-1)]
def mon4(d):
    out=[]
    for i in range(d,-1,-1):
        for j in range(d-i,-1,-1):
            for h in range(d-i-j,-1,-1):
                for u in range(d-i-j-h,-1,-1): out.append((i,j,h,u))
    return out
def abasis(n,k,eta,d): return [Q(n**i*k**j)*eta**e for e in (1,0) for i,j in mon2(d)]
def qlbasis(kind,n,k,l,t,eta,d):
    D=(l+1)**3*(k+l+1)*((t+l+1) if kind=="U" else 1); edge=l*(n+1-l)
    return [Q(edge*n**i*k**j*l**h*t**u,D)*eta**e for e in (1,0) for i,j,h,u in mon4(d)]
def qtbasis(kind,r,n,k,l,t,eta,d):
    D=(t+1)**r*((t+l+1) if kind=="U" else 1); edge=(t-1)*(k+1-t)
    return [Q(edge*n**i*k**j*l**h*t**u,D)*eta**e for e in (1,0) for i,j,h,u in mon4(d)]
def row(kind,r,n,k,l,t,eta,d):
    b=abasis(n,k,eta,d); ratios=[Q(1),Rk(n,k,l),Rk(n,k,l)*Rk(n,k+1,l)]; A=[ratio*x for ratio in ratios for x in b]
    qc=qlbasis(kind,n,k,l,t,eta,d); qn=qlbasis(kind,n,k,l+1,t,eta,d); q=[x-Rl(kind,n,k,l,t,eta)*y for x,y in zip(qc,qn)]
    sc=qtbasis(kind,r,n,k,l,t,eta,d); sn=qtbasis(kind,r,n,k,l,t+1,eta,d); s=[x-Rt(kind,r,l,t,eta)*y for x,y in zip(sc,sn)]
    return A,q+s
def modq(x):
    den=x.denominator%P
    if den==0: raise AssertionError('verifier prime collision')
    return x.numerator%P*pow(den,-1,P)%P
def elim_local(rows,na,nb):
    M=[[modq(x) for x in reversed(r[na:])]+[modq(x) for x in reversed(r[:na])] for r in rows]; rank=0
    for c in range(nb):
        pivot=next((rr for rr in range(rank,len(M)) if M[rr][c]),None)
        if pivot is None: return rank,[]
        M[rank],M[pivot]=M[pivot],M[rank]; inv=pow(M[rank][c],-1,P); M[rank][c:]=[(x*inv)%P for x in M[rank][c:]]; pr=M[rank]
        for rr in range(rank+1,len(M)):
            f=M[rr][c]
            if f: M[rr][c:]=[(x-f*y)%P for x,y in zip(M[rr][c:],pr[c:])]
        rank+=1
    return rank,[r[nb:] for r in M[rank:] if any(r[nb:])]
def rank_rows(rows):
    M=[r[:] for r in rows]; rank=0
    if not M: return 0
    nc=len(M[0])
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
def stage(d,nmax):
    na=3*2*len(mon2(d)); nb=4*len(mon4(d)); cons=[]; cr={}; eq=0
    for kind,r in COMPONENTS:
        rows=[]
        for eta in ETA_SAMPLES:
            for n in range(4,nmax+1):
                for k in range(2,n-1):
                    for l in range(1,n):
                        for t in range(1,k+1):
                            A,B=row(kind,r,n,k,l,t,eta,d); rows.append(A+B)
        rb,c=elim_local(rows,na,nb); cr[f'{kind}_R{r}']=rb; eq+=len(rows); cons+=c
    sr=rank_rows(cons); total=sum(cr.values())+sr; unknowns=na+4*nb
    return {'n_max':nmax,'equations':eq,'shared_telescoper_unknowns':na,'certificate_unknowns_per_component':nb,'component_certificate_ranks':cr,'shared_telescoper_rank':sr,'rank':total,'unknowns':unknowns,'nullity':unknowns-total}
def verify(result):
    errors=[]; ok,nested,shifts=check_parent()
    if not ok: errors.append('independent parent/lift reconstruction failed')
    p=result.get('parent_family',{})
    if p.get('nested_cumulant_checks')!=nested: errors.append('retained nested cumulant count drift')
    if p.get('exact_shift_ratio_checks')!=shifts: errors.append('retained shift-ratio count drift')
    nmax={0:6,1:6,2:6,3:7,4:8}; stages=result.get('search',{}).get('stages',[])
    if len(stages)!=5: return errors+['stage count drift']
    for got in stages:
        d=got.get('degree'); exp=stage(d,nmax[d])
        for key in ('n_max','equations','shared_telescoper_unknowns','certificate_unknowns_per_component','shared_telescoper_rank','rank','unknowns','nullity'):
            if got.get(key)!=exp[key]: errors.append(f'stage {d} {key} mismatch')
        if got.get('component_certificate_ranks')!=exp['component_certificate_ranks']: errors.append(f'stage {d} component rank mismatch')
    return errors
def main():
    result=json.loads(RESULT.read_text(encoding='utf-8')); e=verify(result)
    if e: print('\n'.join(e)); return 1
    print('independent OZ-RT-BZ-T3-004 auxiliary parameter-dependent order-2 replay valid'); return 0
if __name__=='__main__': raise SystemExit(main())
