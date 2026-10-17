"""Exact finite product-probability checks for #520.

They are NOT evidence of almost-sure asymptotic convergence.
"""
from fractions import Fraction as F
from itertools import product
from math import isqrt


PRIMES = (2,3,5,7,11,13,17,19)
LIMIT = 19


def is_squarefree(n):
    if n == 1:
        return True
    for p in range(2,isqrt(n)+1):
        if n % (p*p) == 0:
            return False
    return True


def rademacher_value(n, signs):
    if n == 1:
        return 1
    if not is_squarefree(n):
        return 0
    v = 1
    r = n
    for p in PRIMES:
        if r % p == 0:
            v *= signs[p]
            r //= p
    assert r == 1
    return v


def assignments():
    for picks in product((-1,1), repeat=len(PRIMES)):
        yield dict(zip(PRIMES, picks))


def _check_test_520_probability_model_and_prime_squares():
    models = tuple(assignments())
    assert len(models) == 2**len(PRIMES)
    for signs in models:
        assert rademacher_value(1, signs) == 1
        for p in PRIMES:
            assert rademacher_value(p, signs) == signs[p]
            if p*p <= LIMIT:
                assert rademacher_value(p*p, signs) == 0
        assert rademacher_value(6, signs) == signs[2]*signs[3]
        assert rademacher_value(12, signs) == 0


def _check_test_520_exact_orthogonality_and_expectation():
    models = tuple(assignments())
    count = len(models)
    table = [[rademacher_value(m, a) for m in range(1,LIMIT+1)]
             for a in models]
    for m in range(1,LIMIT+1):
        mean = F(sum(row[m-1] for row in table),count)
        assert mean == (1 if m == 1 else 0)
        for n in range(1,LIMIT+1):
            cross = F(sum(row[m-1]*row[n-1] for row in table),count)
            assert cross == (1 if m == n and is_squarefree(m) else 0)


def _check_test_520_exact_second_moment_and_variance():
    models = tuple(assignments())
    count = len(models)
    for N in range(1,LIMIT+1):
        sums = [sum(rademacher_value(m, signs) for m in range(1,N+1))
                for signs in models]
        Q = sum(is_squarefree(m) for m in range(1,N+1))
        assert F(sum(sums),count) == 1
        assert F(sum(s*s for s in sums),count) == Q
        assert F(sum((s-1)**2 for s in sums),count) == Q-1


def _check_test_520_2026_bound_implies_normalized_ratio_zero_conditionally():
    # If almost surely |M_f(N)| <= C sqrt(N) (loglog N)^(1/4+eps),
    # choose eps=1/8 and divide by sqrt(N loglog N).
    exponent = F(1,4) + F(1,8) - F(1,2)
    assert exponent == F(-1,8)
    assert exponent < 0
    # Therefore (loglog N)^exponent -> 0 as N -> infinity.
    # This tests exponent bookkeeping, NOT Durkan–Pearce-Crump's proof.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_520_probability_model_and_prime_squares(self):
        _check_test_520_probability_model_and_prime_squares()

    def test_520_exact_orthogonality_and_expectation(self):
        _check_test_520_exact_orthogonality_and_expectation()

    def test_520_exact_second_moment_and_variance(self):
        _check_test_520_exact_second_moment_and_variance()

    def test_520_2026_bound_implies_normalized_ratio_zero_conditionally(self):
        _check_test_520_2026_bound_implies_normalized_ratio_zero_conditionally()
