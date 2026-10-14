#!/usr/bin/env python3
"""Exact support-mask optimization for Erdős #878; finite evidence only."""
import json
from functools import lru_cache
from math import gcd

def factor_primes(n):
    primes=[]
    k=n
    p=2
    while p*p<=k:
        if k%p==0:
            primes.append(p)
            while k%p==0:k//=p
        p+=1
    if k>1:primes.append(k)
    return primes

def f(n):
    if n==1:return 0
    result=0
    for p in factor_primes(n):
        power=p
        while power*p<=n:power*=p
        result+=power
    return result

def candidates(n,primes):
    P=set(primes)
    D={}
    for x in range(2,n+1):
        q=x
        mask=0
        for j,p in enumerate(primes):
            if q%p==0:
                mask|=1<<j
                while q%p==0:q//=p
        if q==1 and mask:
            if x>D.get(mask,0):D[mask]=x
    return D

def exact_F(n):
    ps=factor_primes(n)
    weights=candidates(n,ps)
    @lru_cache(None)
    def solve(available):
        if available==0:return (0,())
        v=available&-available
        best=solve(available^v)
        sub=available
        while sub:
            if sub&v and sub in weights:
                other=solve(available^sub)
                candidate=(weights[sub]+other[0],(weights[sub],)+other[1])
                if candidate[0]>best[0]:best=candidate
            sub=(sub-1)&available
        return best
    mx,witness=solve((1<<len(ps))-1)
    witness=tuple(sorted((1,)+witness))
    assert sum(witness)==mx+1
    assert all(gcd(a,b)==1 for i,a in enumerate(witness) for b in witness[i+1:])
    assert all(1<=a<=n for a in witness)
    return mx+1,witness

def independent_brute(n):
    ps=factor_primes(n)
    opts=[1]+[x for x in range(2,n+1) if set(factor_primes(x))<=set(ps)]
    # All x>1 are represented by an inclusion choice. Search via prime mask
    # using a completely different recursion from support-subset dynamic programming.
    best=0
    def visit(i,selected,score):
        nonlocal best
        if i==len(opts):
            best=max(best,score)
            return
        visit(i+1,selected,score)
        x=opts[i]
        if all(gcd(x,y)==1 for y in selected):
            visit(i+1,selected+[x],score+x)
    visit(0,[],0)
    return best

def main():
    cases=[]
    for n in range(1,251):
        fval=f(n)
        F,witness=exact_F(n)
        assert F>=fval if n>1 else F==1
        if n<=25:
            assert F==independent_brute(n),(n,F,independent_brute(n))
        cases.append({'n':n,'f':fval,'F':F,'F_witness':witness})
    assert next(x for x in cases if x['n']==210)['f']==383
    v=next(x for x in cases if x['n']==210)
    assert v['F']>=443
    assert max(x['f'] for x in cases[:210])==383
    print(json.dumps({'record_type':'EC_BULK_006_878_FINITE/1',
                      'scope':'finite exact n=1..250; no asymptotic certification',
                      'direct_gcd_brute_crosscheck':'n<=25',
                      'max_f_up_to_210':383,
                      'n210':v,
                      'n_with_F_gt_f':sum(x['F']>x['f'] for x in cases[1:]),
                      'cases':cases},indent=2))
if __name__=='__main__':main()
