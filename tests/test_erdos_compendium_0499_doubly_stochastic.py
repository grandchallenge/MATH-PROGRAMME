"""Exact finite tests for Erdős #499, not a universal proof of permanent inequality."""

from fractions import Fraction
from itertools import permutations
from math import factorial


def matrix_from_permutations(n, perms, weights):
    assert len(perms) == len(weights)
    assert all(w >= 0 for w in weights) and sum(weights) == 1
    a = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    for perm, w in zip(perms, weights):
        assert sorted(perm) == list(range(n))
        for i, j in enumerate(perm):
            a[i][j] += w
    return a


def products(a):
    n = len(a)
    return [
        __import__("math").prod((a[i][p[i]] for i in range(n)), start=Fraction(1))
        for p in permutations(range(n))
    ]


def test_499_uniform_and_permutation_extremes_exact():
    for n in range(1, 7):
        uniform = [[Fraction(1, n) for _ in range(n)] for _ in range(n)]
        diagonals = products(uniform)
        assert len(diagonals) == factorial(n)
        assert set(diagonals) == {Fraction(1, n**n)}
        identity = matrix_from_permutations(
            n, [tuple(range(n))], [Fraction(1)]
        )
        terms = products(identity)
        assert sum(terms) == 1
        assert max(terms) == 1


def test_499_convex_combinations_of_permutations():
    for n in range(1, 6):
        ps = list(permutations(range(n)))
        for offset in range(0, min(len(ps), 14)):
            chosen = [ps[offset], ps[(offset + 1) % len(ps)], ps[(offset + 2) % len(ps)]]
            weights = [Fraction(1, 6), Fraction(1, 3), Fraction(1, 2)]
            a = matrix_from_permutations(n, chosen, weights)
            assert all(sum(row) == 1 for row in a)
            assert all(sum(a[i][j] for i in range(n)) == 1 for j in range(n))
            assert all(v >= 0 for row in a for v in row)
            terms = products(a)
            assert max(terms) >= Fraction(1, n**n)
            assert max(terms) >= sum(terms) / factorial(n)


def test_499_n2_proof_special_and_nonstrict_inequality():
    for k in range(101):
        t = Fraction(k, 100)
        a = [[t, 1 - t], [1 - t, t]]
        terms = products(a)
        assert set(terms) == {t**2, (1 - t)**2}
        assert max(terms) >= Fraction(1, 4)


def test_499_missing_stochastic_hypothesis_invalidates_claim():
    # A zero matrix is NOT doubly stochastic, and has zero diagonal products.
    z = [[Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)]]
    assert max(products(z)) < Fraction(1, 4)
    assert all(sum(row) != 1 for row in z)
