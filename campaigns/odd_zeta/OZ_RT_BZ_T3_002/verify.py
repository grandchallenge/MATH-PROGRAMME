#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction as Q
from pathlib import Path
import target
HERE=Path(__file__).resolve().parent
RESULT=HERE/'SEARCH_RESULT.json'
STAGES=[(d,10) for d in range(7)]+[(7,12),(8,14),(9,15)]
P=1000003

def mons(d): return [(i,j) for i in range(d+1) for j in range(d+1-i)]

def to_mod(x:Q)->int:
    den=x.denominator%P
    if den==0: raise AssertionError(f'denominator divisible by {P}')
    return (x.numerator%P)*pow(den,P-2,P)%P

def independent_mod_rank(rows):
    a=[[to_mod(x) for x in row] for row in rows]
    if not a:return 0
    rank=0; cols=len(a[0])
    for col in range(cols):
        pivot=-1
        for rr in range(rank,len(a)):
            if a[rr][col]: pivot=rr; break
        if pivot<0: continue
        a[rank],a[pivot]=a[pivot],a[rank]
        inv=pow(a[rank][col],P-2,P)
        for rr in range(len(a)):
            if rr==rank: continue
            factor=a[rr][col]*inv%P
            if not factor: continue
            a[rr]=[(x-factor*y)%P for x,y in zip(a[rr],a[rank])]
        rank+=1
        if rank==cols: break
    return rank

def matrix(d,n_max):
    mm=mons(d); out=[]
    for n in range(1,n_max+1):
        vals=target.fibre_values(n); g=Q(0)
        for k,v in enumerate(vals):
            p=[Q(n**i*k**j) for i,j in mm]
            out.append([v*x for x in p]+[-g*x for x in p])
            g += v
        if g != 0:
            raise AssertionError(f'finite T3 replay drift at n={n}')
    return out

def verify(data=None):
    data=json.loads(RESULT.read_text()) if data is None else data
    errors=[]
    rc=data.get('rank_certificate',{})
    if rc.get('prime')!=P or rc.get('implication')!='full column rank after reduction mod p certifies full column rank over Q via a nonzero square minor': errors.append('rank certificate drift')
    if data.get('search_class')!='FIRST_ORDER_FIBRE_RATIONAL_TELESCOPER_G_EQUALS_Q_TIMES_V': errors.append('search class drift')
    if data.get('proof_effect')!='NONE' or data.get('terminal')!='NO_CERTIFICATE_IN_BOUNDED_CLASS': errors.append('result inflation')
    stages=data.get('stages',[])
    if [(s.get('degree'),s.get('n_max')) for s in stages] != STAGES: errors.append('degree/sample ladder drift')
    for s in stages:
        d=s.get('degree'); n_max=s.get('n_max'); a=matrix(d,n_max); u=2*len(mons(d)); r=independent_mod_rank(a)
        expected_eq=sum(n+1 for n in range(1,n_max+1))
        if s.get('equations')!=expected_eq or s.get('unknowns')!=u or s.get('rank')!=r or s.get('nullity')!=u-r: errors.append(f'rank record drift d={d}')
        if s.get('rank_certificate')!='FULL_COLUMN_RANK_MOD_P_IMPLIES_FULL_COLUMN_RANK_OVER_Q': errors.append(f'rank certificate label drift d={d}')
        if r != u or s.get('classification')!='INCONSISTENT_ANSATZ': errors.append(f'bounded class not closed d={d}')
    return errors

def main():
    e=verify()
    if e:
        print('\n'.join(e)); return 1
    print('independent modular nonzero-minor verification certifies exact Q full rank through degree 9')
    return 0
if __name__=='__main__': raise SystemExit(main())
