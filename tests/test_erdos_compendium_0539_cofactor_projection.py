"""Bounded exact cofactor/positive-orthant checks for OPEN #539.

The ProofCouncil 2026 paper formally verifies only the power exponent,
not its sharper explicit subexponential upper bound.
"""
from itertools import combinations, product
from math import gcd,prod
from sympy import factorint, primerange


def positive_part(x):
    return tuple(max(0,a) for a in x)


def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))


def proj_differences(F):
    return {positive_part(sub(a,b)) for a in F for b in F}


def usual_differences(F):
    return {sub(a,b) for a in F for b in F}


def cofactors(A):
    return {a//gcd(a,b) for a in A for b in A}


def exponents(A):
    P=sorted(set().union(*(factorint(a) for a in A)))
    return {tuple(factorint(a).get(p,0) for p in P) for a in A}


def integer_embed(F):
    d=len(next(iter(F)))
    ps=tuple(int(p) for p in primerange(2,50))[:d]
    shift=tuple(-min(x[j] for x in F) for j in range(d))
    return {prod(p**(x+z) for p,x,z in zip(ps,v,shift)) for v in F}


def base_strip(W):
    L=W*W
    return {(i,j) for i in range(L+1) for j in range(L+1)
            if L<=i+j<=L+W-1}


def suspension(F,K):
    d=len(next(iter(F)))
    R=usual_differences(F)
    M=1+max(abs(x) for vec in R for x in vec)
    return {(j,*(x[t]+j*M for t in range(d)),
                *(y[t]-j*M for t in range(d)))
            for j in range(K) for x in F for y in F}


def _check_test_539_integer_quotient_prime_projection_exact():
    examples=((6,10,15),(1,2,4),(4,6,9),(12,18,30),(2,3,5,7))
    for A in examples:
        assert all(a>0 for a in A)
        assert len(cofactors(A))==len(proj_differences(exponents(A)))
        assert 1 in cofactors(A)
    assert cofactors((6,10,15))=={1,2,3,5}


def _check_test_539_arbitrary_vector_configuration_prime_model():
    Fs=(
        {(0,0),(1,0),(0,1)},
        {(0,0),(2,-1),(-1,3)},
        {(1,-2),(0,5),(3,3),(2,2)},
    )
    for F in Fs:
        A=integer_embed(F)
        assert len(A)==len(F)
        assert all(a>0 for a in A)
        assert len(cofactors(A))==len(proj_differences(F))


def _check_test_539_universal_refined_sqrt_lower_count():
    for N in range(1,10):
        for tup in combinations(range(1,13),N):
            q=len(cofactors(tup))
            assert 2*N-1<=q*(q-1)+1
            # h(n) >= (1+sqrt(8n-7))/2 exactly equivalent.
            if N>=5:break
    for F in ({(0,0),(1,0),(0,1)}, {(1,2),(4,3),(0,4),(3,0)}):
        D=proj_differences(F)
        assert usual_differences(F).issubset(
            {sub(a,b) for a in D for b in D})
        q=len(D)
        assert 2*len(F)-1<=q*(q-1)+1


def _check_test_539_antidiagonal_strip_bounds():
    for W in (1,2,3):
        F=base_strip(W)
        D=proj_differences(F)
        diffs=usual_differences(F)
        assert 2*len(F)>=W**3
        assert len(D)<=3*W*W
        assert len(diffs)<=6*W**3
        assert all(0<=i<=W*W and 0<=j<=W*W for i,j in F)


def _check_test_539_separated_suspension_exact_lemma():
    families=(
        {(0,0),(1,0)},
        {(0,0),(1,0),(0,1)},
        {(1,3),(-1,0),(0,2)},
    )
    for F in families:
        for K in (1,2,3):
            S=suspension(F,K)
            m,q,t=len(F),len(proj_differences(F)),len(usual_differences(F))
            assert len(S)==K*m*m
            assert len(proj_differences(S))<=q*q+2*(K-1)*t
            assert len(usual_differences(S))==(2*K-1)*t*t
    # These finite checks are not a full iteration or asymptotic proof.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_539_integer_quotient_prime_projection_exact(self):
        _check_test_539_integer_quotient_prime_projection_exact()

    def test_539_arbitrary_vector_configuration_prime_model(self):
        _check_test_539_arbitrary_vector_configuration_prime_model()

    def test_539_universal_refined_sqrt_lower_count(self):
        _check_test_539_universal_refined_sqrt_lower_count()

    def test_539_antidiagonal_strip_bounds(self):
        _check_test_539_antidiagonal_strip_bounds()

    def test_539_separated_suspension_exact_lemma(self):
        _check_test_539_separated_suspension_exact_lemma()
