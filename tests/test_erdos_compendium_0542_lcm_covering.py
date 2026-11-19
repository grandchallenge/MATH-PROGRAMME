"""Exact bounded checks for #542, including a genuine catalogue wording conflict.

Original 1973: m NOT DIVISIBLE by any a, meaning no a|m.
Modern catalogue: m DIVIDES no a, meaning no m|a. NOT equivalent.
Full Schinzel--Szekeres 1959 proof is NOT a finite enumeration.
"""
from fractions import Fraction as F
from itertools import combinations
from math import gcd


def lcm(a,b):
    return a//gcd(a,b)*b


def admissible(A,N):
    return all(lcm(a,b)>N for a,b in combinations(A,2))


def mass(A):
    return sum((F(1,a) for a in A),F(0))


def original_uncovered(A,N):
    return {m for m in range(1,N+1) if not any(m%a==0 for a in A)}


def reversed_uncovered(A,N):
    return {m for m in range(1,N+1) if not any(a%m==0 for a in A)}


def max_mass_branch(N):
    incompatible={a:{b for b in range(a+1,N+1) if lcm(a,b)<=N}
                  for a in range(1,N+1)}
    best=F(0)
    winners=[]
    def visit(i,chosen,weight):
        nonlocal best,winners
        if i>N:
            if weight>best:best,winners=weight,[chosen]
            elif weight==best:winners.append(chosen)
            return
        if not any(i in incompatible.get(a,set()) for a in chosen):
            visit(i+1,chosen+(i,),weight+F(1,i))
        visit(i+1,chosen,weight)
    visit(1,(),F(0))
    return best,winners


def max_mass_mask(N):
    bad=[(1<<(a-1))|(1<<(b-1)) for a,b in combinations(range(1,N+1),2)
         if lcm(a,b)<=N]
    best=F(0)
    winners=[]
    for mask in range(1<<N):
        if any((mask&edge)==edge for edge in bad):
            continue
        A=tuple(a for a in range(1,N+1) if mask & (1<<(a-1)))
        weight=mass(A)
        if weight>best:best,winners=weight,[A]
        elif weight==best:winners.append(A)
    return best,winners


def test_542_exact_sharp_small_optima_by_two_algorithms():
    for N in range(2,14):
        b,B=max_mass_branch(N)
        c,C=max_mass_mask(N)
        assert b==c
        assert set(B)==set(C)
        assert b<=F(31,30)
        if b==F(31,30):
            assert N==5 and B==[(2,3,5)]
    for N in (14,15,16,17,18):
        b,_=max_mass_branch(N)
        assert b<F(31,30)


def test_542_unique_equality_and_other_large_reciprocal():
    assert admissible((2,3,5),5)
    assert mass((2,3,5))==F(31,30)
    A=(3,4,5,7,11)
    assert admissible(A,11)
    assert mass(A)==F(4699,4620)
    assert 1<mass(A)<F(31,30)
    assert not admissible((2,3,5),6)


def test_542_disjoint_multiples_and_original_uncovered():
    for N in range(2,13):
        for A in combinations(range(1,N+1),min(3,N)):
            if not admissible(A,N):continue
            covered={m for a in A for m in range(a,N+1,a)}
            assert len(covered)==sum(N//a for a in A)
            assert original_uncovered(A,N)==set(range(1,N+1))-covered


def test_542_catalogue_direction_reversal_has_all_N_counterexample():
    for N in range(2,201):
        A=tuple(range(N//2+1,N+1))
        assert admissible(A,N)
        assert reversed_uncovered(A,N)==set()
        assert original_uncovered(A,N)==set(range(1,N//2+1))
        for m in range(1,N+1):
            a=m*(N//m)
            assert N/2<a<=N and a%m==0
    assert reversed_uncovered((2,3,5),5) != original_uncovered((2,3,5),5)


# CI uses unittest discovery. Preserve the original bounded witness functions
# while explicitly exposing each as a standard unittest test method.
import unittest

class CompendiumWitnessTests(unittest.TestCase):
    def test_542_exact_sharp_small_optima_by_two_algorithms(self):
        test_542_exact_sharp_small_optima_by_two_algorithms()

    def test_542_unique_equality_and_other_large_reciprocal(self):
        test_542_unique_equality_and_other_large_reciprocal()

    def test_542_disjoint_multiples_and_original_uncovered(self):
        test_542_disjoint_multiples_and_original_uncovered()

    def test_542_catalogue_direction_reversal_has_all_N_counterexample(self):
        test_542_catalogue_direction_reversal_has_all_N_counterexample()
