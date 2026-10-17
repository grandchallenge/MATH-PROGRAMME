"""Exact weighted prime-representation checks for OPEN Erdős #538.

Finite optimization does not accept the July 2026 pending
matching-order claim or certify its external Lean imports.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from sympy import primerange
from math import gcd


def primes_upto(N):
    return tuple(int(p) for p in primerange(2,N+1))


def multiplicities(A,N):
    d=defaultdict(set)
    for a in A:
        for p in primes_upto(N):
            d[p*a].add((p,a))
    return d


def admissible(A,N,r):
    return all(len(v)<=r for v in multiplicities(A,N).values())


def mass(A):
    return sum((F(1,a) for a in A),F())


def harmonic(n):
    return sum((F(1,k) for k in range(1,n+1)),F())


def exact_maximum(N,r):
    best=F()
    winners=[]
    for bits in range(1<<N):
        A=tuple(a for a in range(1,N+1) if bits & (1<<(a-1)))
        if admissible(A,N,r):
            s=mass(A)
            if s>best:
                best,winners=s,[A]
            elif s==best:
                winners.append(A)
    return best,winners


def independent_maximum(N,r):
    p=primes_upto(N)
    product_edges=defaultdict(set)
    for a in range(1,N+1):
        for q in p:
            product_edges[q*a].add(a)
    bad_edges=[
        frozenset(v)
        for v in product_edges.values() if len(v)>r
    ]
    best=F()
    def visit(a,chosen,score):
        nonlocal best
        if a>N:
            best=max(best,score)
            return
        possible=chosen|{a}
        if all(not any(B.issubset(possible) for B in combinations(v,r+1))
               for v in bad_edges):
            visit(a+1,possible,score+F(1,a))
        visit(a+1,chosen,score)
    visit(1,set(),F())
    return best


def test_538_weighted_double_count_exact_fraction():
    for N in (5,8,12,20,30):
        p=primes_upto(N)
        for A in ((),(N,),(2,3,5),
                  tuple(a for a in range(N//2+1,N+1) if gcd(a,N)==1)):
            assert all(1<=a<=N for a in A)
            counts=multiplicities(A,N)
            left=mass(A)*sum((F(1,x) for x in p),F())
            right=sum((F(len(v),m) for m,v in counts.items()),F())
            assert left==right
            if admissible(A,N,2):
                assert right<=2*harmonic(N*N)


def test_538_exact_small_optimum_two_methods():
    for N in (3,4,5,6,7,8,9,10):
        for r in (2,3):
            best,witnesses=exact_maximum(N,r)
            assert best==independent_maximum(N,r)
            assert witnesses and all(admissible(A,N,r) for A in witnesses)


def test_538_two_distinct_representations_force_primes_upto_N():
    for N in (6,12,18,30):
        ps=tuple(int(p) for p in primerange(2,2*N*N+1))
        for m in range(2,2*N*N+1):
            representations=((p,m//p) for p in ps
                             if m%p==0 and 1<=m//p<=N)
            vals=tuple(representations)
            if len(vals)>=2:
                assert all(p<=N for p,a in vals)
    # Thus any cap violation (at least r+1>=2 reps) is caught p<=N.


def test_538_examples_and_harmonic_constraint():
    A=(2,3,5)
    assert mass(A)==F(31,30)
    assert admissible(A,6,2)
    assert multiplicities(A,6)[6]=={(2,3),(3,2)}
    assert multiplicities(A,6)[10]=={(2,5),(5,2)}
    assert multiplicities(A,6)[15]=={(3,5),(5,3)}
    for N in (6,8,10):
        for r in (2,3):
            best,_=exact_maximum(N,r)
            assert best*sum((F(1,p) for p in primes_upto(N)),F()) <= r*harmonic(N*N)
