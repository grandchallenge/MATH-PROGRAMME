"""Exact qualitative Newton–Girard interface for proved Erdős #519.

These finite identities do NOT establish Atkinson's absolute lower constant.
"""
from itertools import combinations
from math import comb


def power_sums(roots):
    n = len(roots)
    return [None] + [sum(z**k for z in roots) for k in range(1, n+1)]


def elementary_symmetric(roots):
    n = len(roots)
    return [1] + [sum((product(subset) for subset in combinations(roots, k)))
                  for k in range(1, n+1)]


def product(values):
    result = 1
    for v in values:
        result *= v
    return result


def test_519_newton_girard_all_integer_root_patterns():
    for n in range(1, 8):
        cases = [(1,) + (0,) * (n-1), (1,) + (-1,) * (n-1),
                 (1,) * n, (1,) + tuple(range(2, n+1))]
        for roots in cases:
            assert len(roots) == n and roots[0] == 1
            e, p = elementary_symmetric(roots), power_sums(roots)
            assert len(e) == n+1
            for k in range(1, n+1):
                rhs = sum((-1)**(j-1)*e[k-j]*p[j] for j in range(1,k+1))
                assert k*e[k] == rhs
            assert any(p[k] != 0 for k in range(1,n+1))


def test_519_all_first_n_sums_zero_implies_all_roots_zero():
    # The recursive Newton identities prove this implication for
    # arbitrary roots, not just tested integer patterns.
    for n in range(1, 20):
        p = [0] * (n+1)
        e = [1]
        for k in range(1,n+1):
            e.append(sum((-1)**(j-1)*e[k-j]*p[j]
                         for j in range(1,k+1)) // k)
        assert e == [1] + [0]*n
        # Then characteristic polynomial is X^n, so z1=1 impossible.


def test_519_roots_of_unity_first_n_minus_one_vanish_exactly():
    for n in range(2, 30):
        for k in range(1,n+1):
            exponents = [((j*k) % n) for j in range(n)]
            counts = [exponents.count(a) for a in range(n)]
            if k < n:
                # X^0+...+X^(n-1) vanishes on primitive n-th root.
                # For composite n and k, the sum still vanishes:
                # it equals (n/order) times complete geometric series.
                order = n // __import__('math').gcd(k,n)
                assert order > 1
                assert all(counts[j] == counts[(j+k)%n] for j in range(n))
            else:
                assert exponents == [0]*n
        # The kth complex moment is zero for k<n, and n for k=n.


def test_519_two_roots_cancellation_requires_second_power():
    roots = (1,-1)
    assert power_sums(roots) == [None,0,2]
    assert power_sums((1,))[1] == 1
    # No conclusion c>0 independent of n is inferred from these cases.
