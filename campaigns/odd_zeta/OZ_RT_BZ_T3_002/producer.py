#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction as Q
from pathlib import Path
import target

HERE = Path(__file__).resolve().parent
OUT = HERE / 'SEARCH_RESULT.json'

def monomials(d: int) -> list[tuple[int,int]]:
    return [(i,j) for i in range(d+1) for j in range(d+1-i)]

def row(n: int, k: int, v: Q, g: Q, d: int) -> list[Q]:
    mons = monomials(d)
    p = [Q(n**i * k**j) for i,j in mons]
    return [v*x for x in p] + [-g*x for x in p]

def rank(a: list[list[Q]]) -> int:
    m = [r[:] for r in a]
    if not m: return 0
    r = 0
    for c in range(len(m[0])):
        p = next((i for i in range(r, len(m)) if m[i][c]), None)
        if p is None: continue
        m[r], m[p] = m[p], m[r]
        inv = 1 / m[r][c]
        m[r] = [x*inv for x in m[r]]
        for i in range(r+1, len(m)):
            if m[i][c]:
                f = m[i][c]
                m[i] = [x-f*y for x,y in zip(m[i],m[r])]
        r += 1
        if r == len(m): break
    return r

def build_matrix(d: int, n_max: int=10) -> list[list[Q]]:
    rows=[]
    for n in range(1,n_max+1):
        g=Q(0)
        for k,v in enumerate(target.fibre_values(n)):
            rows.append(row(n,k,v,g,d))
            g += v
    return rows

def main() -> int:
    stages=[]
    for d in range(7):
        a=build_matrix(d)
        unknowns=2*len(monomials(d))
        rk=rank(a)
        stages.append({'route_id':f'FIBRE_Q_TOTAL_DEGREE_{d}','degree':d,'equations':len(a),'unknowns':unknowns,'rank':rk,'nullity':unknowns-rk,'classification':'INCONSISTENT_ANSATZ' if rk==unknowns else 'CANDIDATE_SPACE_REMAINS'})
    result={'schema_version':'1.0.0','search_class':'FIRST_ORDER_FIBRE_RATIONAL_TELESCOPER_G_EQUALS_Q_TIMES_V','sample_domain':{'n_min':1,'n_max':10,'k':'0..n'},'normalization':'homogeneous equation D(n,k)G(n,k)-N(n,k)V(n,k)=0; nonzero (N,D) required','stages':stages,'proof_effect':'NONE','terminal':'NO_CERTIFICATE_IN_BOUNDED_CLASS'}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
