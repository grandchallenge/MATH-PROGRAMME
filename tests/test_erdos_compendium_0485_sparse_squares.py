"""Exact finite arithmetic fixtures for Erdős #485.

Polynomials are sparse dictionaries exponent -> rational coefficient.
These tests check support semantics and cancellation, not Schinzel's
universal logarithmic bound or an uninspected external Lean proof.
"""

from fractions import Fraction
from math import log


def normalize(poly):
    return {e: c for e, c in poly.items() if c != 0}


def multiply(p, q):
    out = {}
    for a, ca in p.items():
        for b, cb in q.items():
            out[a + b] = out.get(a + b, Fraction(0)) + ca * cb
    return normalize(out)


def square(p):
    return multiply(p, p)


def count(p):
    return len(normalize(p))


def test_485_cancellation_requires_collecting_coefficients() -> None:
    p = {0: Fraction(1), 1: Fraction(1), 2: Fraction(-1, 2)}
    result = square(p)
    assert count(p) == 3
    assert result == {
        0: Fraction(1), 1: Fraction(2),
        3: Fraction(-1), 4: Fraction(1, 4),
    }
    assert count(result) == 4
    assert 2 not in result


def test_485_one_and_two_term_exact_values() -> None:
    for r in range(0, 8):
        p = {r: Fraction(-7, 3)}
        assert count(square(p)) == 1
        for s in range(r + 1, 9):
            q = {r: Fraction(-3, 4), s: Fraction(5, 7)}
            assert count(square(q)) == 3
            assert set(square(q)) == {2 * r, r + s, 2 * s}


def test_485_all_positive_dense_geometric_sum_has_two_k_minus_one_terms() -> None:
    for k in range(1, 30):
        p = {j: Fraction(1) for j in range(k)}
        squared = square(p)
        assert count(p) == k
        assert count(squared) == 2 * k - 1
        assert all(c > 0 for c in squared.values())


def test_485_support_cardinality_invariant_under_monomial_dilation_and_scaling() -> None:
    base = {0: Fraction(1), 4: Fraction(-3, 2), 11: Fraction(7, 4)}
    for d in (1, 2, 13, 97):
        for shift in (0, 1, 100):
            q = {shift + d * e: Fraction(-5, 3) * c for e, c in base.items()}
            assert count(q) == count(base)
            assert count(square(q)) == count(square(base))
            # Counts remain the same at arbitrarily large degree.


def test_485_published_logarithm_scope_in_finite_examples() -> None:
    # Schinzel-Zannier (2009) Theorem 1, l=2, characteristic 0:
    # t >= 2 + log(T - 1) / log(8), with T>=2.
    examples = [
        {0: Fraction(1), 1: Fraction(1), 2: Fraction(-1, 2)},
        {0: Fraction(1), 2: Fraction(-2), 9: Fraction(3), 31: Fraction(-4)},
        {0: Fraction(1), 1: Fraction(1), 4: Fraction(1), 11: Fraction(-1)},
    ]
    for p in examples:
        T = count(p)
        assert T >= 2
        t = count(square(p))
        assert t + 1e-12 >= 2 + log(T - 1) / log(8)
        assert t >= 2
    # k=1 is outside the theorem's hypothesis.
    assert count(square({91: Fraction(2)})) == 1
