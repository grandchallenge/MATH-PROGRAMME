"""Exact finite LCM-triangle interface for OPEN Erdős #536.

Do not infer f(N)=o(N) from exhaustive n<=12 arithmetic checks.
"""
from itertools import combinations, product
from math import gcd, lcm
from sympy import factorint


def is_lcm_triangle(a,b,c):
    return lcm(a,b)==lcm(a,c)==lcm(b,c)


def via_prime_valuation(a,b,c):
    pf=set(factorint(a))|set(factorint(b))|set(factorint(c))
    for p in pf:
        x,y,z=(factorint(t).get(p,0) for t in (a,b,c))
        m=max(x,y,z)
        if (x==m)+(y==m)+(z==m)<2:return False
    return True


def via_gcd_formula(a,b,c):
    x=a*b//gcd(a,b)
    y=a*c//gcd(a,c)
    z=b*c//gcd(b,c)
    return x==y==z


def avoid_max_bitmask(N):
    bad=[sum(1<<(v-1) for v in t) for t in combinations(range(1,N+1),3)
         if is_lcm_triangle(*t)]
    return max(mask.bit_count() for mask in range(1<<N)
               if all(mask&b!=b for b in bad))


def avoid_max_recursive(N):
    hyper={n:[] for n in range(1,N+1)}
    for t in combinations(range(1,N+1),3):
        if is_lcm_triangle(*t):hyper[t[-1]].append(set(t[:-1]))
    best=0
    def visit(n,seen):
        nonlocal best
        if len(seen)+N-n+1<=best:return
        if n>N:
            best=max(best,len(seen));return
        if all(not e.issubset(seen) for e in hyper[n]):
            visit(n+1,seen|{n})
        visit(n+1,seen)
    visit(1,set())
    return best


def test_536_all_short_triples_prime_valuation_equivalence():
    for a,b,c in combinations(range(1,101),3):
        assert is_lcm_triangle(a,b,c)==via_prime_valuation(a,b,c)
        assert is_lcm_triangle(a,b,c)==via_gcd_formula(a,b,c)


def test_536_bad_and_good_gcd_contrasting_triples():
    assert is_lcm_triangle(6,10,15)
    assert not is_lcm_triangle(6,10,14)
    assert {gcd(a,b) for a,b in combinations((6,10,14),2)}=={2}
    assert not is_lcm_triangle(4,8,16)
    assert lcm(6,10)==lcm(6,15)==lcm(10,15)==30


def test_536_independent_finite_extremal_computations():
    for N in range(3,13):
        assert avoid_max_bitmask(N)==avoid_max_recursive(N)
        assert 1<=avoid_max_bitmask(N)<=N


def test_536_disjoint_prime_bins_give_finite_avoiding_family():
    bins=((2,3),(5,7),(11,13))
    for k in (1,2,3):
        values=tuple(sorted(set(__import__('math').prod(v) for v in product(*bins[:k]))))
        assert len(values)==2**k
        assert all(not is_lcm_triangle(*triple)
                   for triple in combinations(values,3))
    # No claim of positive natural density is made for these finite bins.
