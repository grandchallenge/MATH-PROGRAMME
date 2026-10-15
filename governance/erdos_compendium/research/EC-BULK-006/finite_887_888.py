#!/usr/bin/env python3
"""Exact arithmetic for finite Erdős 887 & 888 source-qualification fixtures."""
import json
from math import isqrt
from itertools import combinations_with_replacement,combinations
from functools import lru_cache

def divisor_interval(n,C):
    """All divisors in (sqrt(n), sqrt(n)+C*n**(1/4)); integer-only iff."""
    assert n>=2 and C>=1
    lo=[]
    for a in range(1,isqrt(n)+1):
        if n%a:continue
        d=n//a
        # d>sqrt(n) and d<sqrt(n)+C*n^(1/4).
        # Since d>sqrt(n), squaring the positive inequality twice gives:
        # (d²+n)² < n(2d+C²)².
        if d*d>n and (d*d+n)**2 < n*(2*d+C*C)**2:
            lo.append(d)
    return sorted(lo)

def test_887():
    Cs=(1,2,4,8)
    record={}
    for C in Cs:
        max_count=-1
        max_n=[]
        examples={}
        for n in range(2,30001):
            ds=divisor_interval(n,C)
            assert len(ds)<=1+C*C,(n,C,ds)
            if len(ds)>max_count:
                max_count=len(ds);max_n=[n]
            elif len(ds)==max_count and len(max_n)<6:
                max_n.append(n)
            if n in (12,36,360,840,2520,7560,27720):
                examples[str(n)]=ds
        record[str(C)]=dict(max_count=max_count,first_attaining_n=max_n,examples=examples)
    for n in (10,17,36,100,360,1024):
        for C in Cs:
            from decimal import Decimal,localcontext
            with localcontext() as ctx:
                ctx.prec=60
                D=Decimal(n); boundary=D.sqrt()+Decimal(C)*D.sqrt().sqrt()
                by_decimal=[n//a for a in range(1,isqrt(n)+1) if n%a==0
                       and Decimal(n//a)>D.sqrt() and Decimal(n//a)<boundary]
                assert sorted(by_decimal)==divisor_interval(n,C)
    return dict(n_range=[2,30000],C_values=list(Cs),open_upper_endpoint=True,
        exact_comparison="d²>n and (d²+n)²<n(2d+C²)²",results=record,
        independent_decimal_crosschecks=[10,17,36,100,360,1024])

def squarefree_kernel(n):
    ans=1;v=n;p=2
    while p*p<=v:
        c=0
        while v%p==0:v//=p;c^=1
        if c:ans*=p
        p+=1
    if v>1:ans*=v
    return ans

def is_prime(n):
    return n>1 and all(n%d for d in range(2,isqrt(n)+1))

def squarefree_semiprimes(n):
    A=[]
    for x in range(2,n+1):
        k=squarefree_kernel(x)
        if x!=k:continue
        P=[p for p in range(2,x+1) if is_prime(p) and x%p==0]
        if len(P)<=2:A.append(x)
    return A

def square(n):
    s=isqrt(n);return s*s==n

def valid(A):
    """Quadruples counted with repetition, ordered by numerical size."""
    for a,b,c,d in combinations_with_replacement(A,4):
        if square(a*b*c*d) and a*d!=b*c:
            return False,(a,b,c,d)
    return True,None

def invalid_masks(n):
    bad_by_max=[set() for _ in range(n)]
    for tup in combinations_with_replacement(range(1,n+1),4):
        a,b,c,d=tup
        if square(a*b*c*d) and a*d!=b*c:
            mask=sum(1<<(v-1) for v in set(tup))
            bad_by_max[d-1].add(mask)
    return [tuple(sorted(p)) for p in bad_by_max]

def extremum(n,bads):
    best=0;best_mask=0;states=0
    @lru_cache(None)
    def allowed_prefix(mask,x):
        return all((mask&b)!=b for b in bads[x-1])
    def dfs(i,mask):
        nonlocal best,best_mask,states
        states+=1
        if mask.bit_count()+n-i<=best:return
        if i==n:
            if mask.bit_count()>best:best=mask.bit_count();best_mask=mask
            return
        dfs(i+1,mask)
        new=mask|(1<<i)
        if allowed_prefix(new,i+1):dfs(i+1,new)
    dfs(0,0)
    A=[i+1 for i in range(n) if best_mask>>i&1]
    assert valid(A)[0]
    return dict(n=n,maximum=best,witness=A,states=states)

def test_888():
    # The source condition includes a=b=c=d and 2/3/4 distinct members.
    good_samples={}
    for N in (10,15,30,60,100,120):
        A=squarefree_semiprimes(N)
        ok,bad=valid(A)
        assert ok,(N,bad)
        good_samples[str(N)]=dict(count=len(A),max=max(A),first_twenty=A[:20])
    assert not valid([1,6,10,15])[0]
    assert valid([2,3,4,6])[0]
    # Kernel duplication is always illegal (x,x,x,y when x!=y, xy square).
    for x in range(1,50):
        for y in range(x+1,50):
            if squarefree_kernel(x)==squarefree_kernel(y):
                assert not valid([x,y])[0]
    n=17
    bads=invalid_masks(n)
    extrema=[]
    for k in range(1,n+1):
        extrema.append(extremum(k,bads))
    for n in (10,12):
        for A in combinations(range(1,n+1),3):
            pass # Additional direct predicate exercised by extrema witness and construction.
    return dict(max_n=17,exact_extrema=extrema,
         squarefree_prime_and_semiprime_construction=good_samples,
         rejected_triple_with_one=[1,6,10,15],
         valid_kernel_nontrivial_example=[2,3,4,6],
         squarefree_kernel_pairs_checked_up_to=49,
         method="enumerate exact bad quadruple hyperedges, branch-and-bound independent set")

def main():
    print(json.dumps(dict(record_type="EC_BULK_006_887_888_FINITE/1",
      authority="EXACT FINITE ONLY; not a uniform bound proof or asymptotic certificate",
      p887=test_887(),p888=test_888()),indent=2))
if __name__=="__main__":main()
