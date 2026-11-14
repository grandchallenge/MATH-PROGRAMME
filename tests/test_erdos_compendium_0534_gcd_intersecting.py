"""Finite, exact gcd-intersecting family checks for solved Erdős #534.

The 1996 Ahlswede--Khachatrian optimality theorem is external;
small exact instances and admissibility do not re-prove it.
"""
from itertools import combinations
from math import gcd,prod
import networkx as nx
import sympy as sp

SAMPLES=(2,3,4,6,10,12,15,18,20,21,24,30,35,36,42)


def candidates(N):
    q=sorted(sp.factorint(N))
    return [
        frozenset(x for x in range(1,N+1) if any(
            x%d==0 for d in [*(2*p for p in q[:j]),prod(q[:j])]))
        for j in range(1,len(q)+1)
    ]


def gcd_graph(N):
    v=[x for x in range(1,N+1) if gcd(x,N)>1]
    G=nx.Graph()
    G.add_nodes_from(v)
    G.add_edges_from((a,b) for i,a in enumerate(v)
                     for b in v[i+1:] if gcd(a,b)>1)
    return G


def independent_bounded_clique(N):
    vertices=[x for x in range(1,N) if gcd(x,N)>1]
    adj={x:{y for y in vertices if x!=y and gcd(x,y)>1}
         for x in vertices}
    best=1
    def search(chosen,rest):
        nonlocal best
        if chosen+len(rest)<=best:return
        if not rest:
            best=max(best,chosen)
            return
        x=rest[0]
        search(chosen+1,[y for y in rest[1:] if y in adj[x]])
        search(chosen,rest[1:])
    search(1,vertices)
    return best


def _check_test_534_family_feasibility_and_contains_N():
    for N in SAMPLES:
        for A in candidates(N):
            assert N in A and A and max(A)<=N
            assert all(gcd(a,b)>1 for a,b in combinations(A,2))


def _check_test_534_two_independent_exact_optimality_algorithms():
    for N in SAMPLES:
        G=gcd_graph(N)
        best=max(map(len,nx.find_cliques(G)))
        assert best==max(map(len,candidates(N)))
        if N<=21:
            assert best==independent_bounded_clique(N)


def _check_test_534_prime_and_even_edge_cases():
    for N in (2,3,5,7,11,13,17,19):
        assert candidates(N)==[frozenset({N})]
        assert independent_bounded_clique(N)==1
    for N in (4,6,8,10,12,18,20,24,30,36,42):
        assert max(len(A) for A in candidates(N)) >= N//2
    assert max(len(A) for A in candidates(30))==15


def _check_test_534_original_gcd_one_typo_not_same_predicate():
    # Including N=6, {2,3,6} is NOT pairwise noncoprime,
    # despite each of 2,3 individually sharing a gcd with N.
    assert gcd(2,3)==1 and gcd(2,6)>1 and gcd(3,6)>1
    # And the original (t,N)=1 condition for even candidates is not
    # the maintained (2t,N)>1 condition. E.g. N=6,t=2.
    assert gcd(2,6)>1 and gcd(2*2,6)>1
    assert gcd(1,6)==1 and gcd(2,6)>1


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_534_family_feasibility_and_contains_N(self):
        _check_test_534_family_feasibility_and_contains_N()

    def test_534_two_independent_exact_optimality_algorithms(self):
        _check_test_534_two_independent_exact_optimality_algorithms()

    def test_534_prime_and_even_edge_cases(self):
        _check_test_534_prime_and_even_edge_cases()

    def test_534_original_gcd_one_typo_not_same_predicate(self):
        _check_test_534_original_gcd_one_typo_not_same_predicate()
