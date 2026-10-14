#!/usr/bin/env python3
"""Exact finite tests for #879 G(n) and #880 first-stage restricted addition."""
import json
from functools import lru_cache
from itertools import combinations,groupby
from math import gcd,isqrt

def primes(n):
    return [p for p in range(2,n+1) if all(p%d for d in range(2,isqrt(p)+1))]

def G(n,limit=None):
    if n==1:return 1,[1]
    ps=primes(n)
    active=[p for p in ps if p*2<=n]
    forced=[p for p in ps if p*2>n]
    W={}
    for x in range(2,n+1):
        if any(x%p==0 for p in forced):
            assert x in forced
            continue
        support=sum(1<<i for i,p in enumerate(active) if x%p==0)
        assert support
        if limit is not None and support.bit_count()>=limit:continue
        W[support]=max(W.get(support,0),x)
    @lru_cache(None)
    def solve(mask):
        if not mask:return (0,())
        bit=mask&-mask
        best=solve(mask^bit)
        sub=mask
        while sub:
            if sub&bit and sub in W:
                v,choices=solve(mask^sub)
                if W[sub]+v>best[0]:
                    best=(W[sub]+v,(W[sub],)+choices)
            sub=(sub-1)&mask
        return best
    _,choice=solve((1<<len(active))-1)
    w=sorted([1]+forced+list(choice))
    assert all(gcd(a,b)==1 for a,b in combinations(w,2))
    assert all(1<=a<=n for a in w)
    return sum(w),w

def direct(n):
    best=0
    for bits in range(1<<n):
        w=[i+1 for i in range(n) if bits>>i&1]
        if sum(w)<=best:continue
        if all(gcd(a,b)==1 for a,b in combinations(w,2)):
            best=sum(w)
    return best

def H(n):
    ps=primes(n)
    return sum(p for p in ps if p<n)+n*sum(p<=isqrt(n) for p in ps)

def first_block(h):
    x=h
    y=(3*2**(h-2)-1)*x*x+h*x
    A={0}|{x+t for t in range(x*x)}|{x+2**j*x*x for j in range(h-1)}
    ordinary={0}
    for _ in range(h):ordinary={a+b for a in ordinary for b in A}
    assert all(t in ordinary for t in range(x,y))
    restricted=set()
    for j in range(1,h+1):
        restricted.update(map(sum,combinations(sorted(A),j)))
    holes=[t for t in range(x,y) if t not in restricted]
    assert holes and holes[0]==(45 if h==3 else 144)
    assert holes[-1]==y-1
    gap=max(len(list(group)) for _,group in groupby(enumerate(holes),key=lambda t:t[1]-t[0]))
    return dict(h=h,interval=[x,y],hole_count=len(holes),first=holes[0],last=holes[-1],largest_gap=gap)

def main():
    rows=[]
    for n in range(1,71):
        value,w=G(n)
        restricted,_=G(n,limit=2)
        expected=1
        for p in primes(n):
            q=p
            while q*p<=n:q*=p
            expected+=q
        assert restricted==expected,(n,restricted,expected)
        if n<=14:assert value==direct(n),n
        rows.append(dict(n=n,G=value,H=H(n),witness=w,G_one_prime_support=restricted))
    assert rows[29]['G']==193 and rows[29]['H']==219 and rows[29]['G_one_prime_support']==188
    assert rows[59]['G']==594 and rows[59]['H']==680
    count=0
    for bits in range(1<<9):
        A=[i+1 for i in range(9) if bits>>i&1]
        sums={a+b for a in A for b in A}
        distinct={a+b for a,b in combinations(A,2)}
        assert {s for s in sums if s%2}<=distinct
        count+=1
    out=dict(record_type='EC_BULK_006_879_880_FINITE/1',authority='EXACT_FINITE_ONLY',
             G_by_n=rows,G_brute_crosscheck_up_to=14,
             order2_parity_cases=count,first_stages=[first_block(h) for h in (3,4)])
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
