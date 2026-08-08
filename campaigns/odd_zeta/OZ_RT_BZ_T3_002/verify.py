#!/usr/bin/env python3
from __future__ import annotations
import json
from fractions import Fraction as Q
from pathlib import Path
import target
HERE=Path(__file__).resolve().parent
RESULT=HERE/'SEARCH_RESULT.json'

def mons(d): return [(i,j) for i in range(d+1) for j in range(d+1-i)]

def exact_rank(rows):
    a=[r[:] for r in rows]
    if not a: return 0
    nr=0; nc=len(a[0])
    for c in range(nc):
        pivot=None
        for i in range(nr,len(a)):
            if a[i][c] != 0:
                pivot=i; break
        if pivot is None: continue
        a[nr],a[pivot]=a[pivot],a[nr]
        pv=a[nr][c]
        for j in range(c,nc): a[nr][j] /= pv
        for i in range(len(a)):
            if i==nr or a[i][c]==0: continue
            f=a[i][c]
            for j in range(c,nc): a[i][j]-=f*a[nr][j]
        nr+=1
        if nr==len(a): break
    return nr

def matrix(d):
    mm=mons(d); out=[]
    for n in range(1,11):
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
    if data.get('search_class')!='FIRST_ORDER_FIBRE_RATIONAL_TELESCOPER_G_EQUALS_Q_TIMES_V': errors.append('search class drift')
    if data.get('proof_effect')!='NONE' or data.get('terminal')!='NO_CERTIFICATE_IN_BOUNDED_CLASS': errors.append('result inflation')
    stages=data.get('stages',[])
    if [s.get('degree') for s in stages] != list(range(7)): errors.append('degree ladder drift')
    for s in stages:
        d=s.get('degree'); a=matrix(d); u=2*len(mons(d)); r=exact_rank(a)
        if s.get('equations')!=65 or s.get('unknowns')!=u or s.get('rank')!=r or s.get('nullity')!=u-r: errors.append(f'rank record drift d={d}')
        if r != u or s.get('classification')!='INCONSISTENT_ANSATZ': errors.append(f'bounded class not closed d={d}')
    return errors

def main():
    e=verify()
    if e:
        print('\n'.join(e)); return 1
    print('independent exact fibre-rational search verification passed')
    return 0
if __name__=='__main__': raise SystemExit(main())
