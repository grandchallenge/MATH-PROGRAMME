#!/usr/bin/env python3
"""Exact finite-mode BV and finite-Weiss-cover checks for research result 024.

No numerical approximation and no external packages. These bounded checks are
hostile controls, NOT proofs of smooth infinite-dimensional Weiss descent.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product

DIM = 2
# A is the symmetric finite-mode kinetic operator.
A = ((Fraction(2), Fraction(1)), (Fraction(1), Fraction(3)))


def basis(exponents: tuple[int, ...], mask: int, h: int = 0):
    return (tuple(exponents), mask, h)


def accum(out, key, coefficient):
    out[key] = out.get(key, Fraction(0)) + coefficient
    if out[key] == 0:
        del out[key]


def d_cl(term):
    out = {}
    for (e, mask, h), c in term.items():
        for i in range(DIM):
            if not (mask & (1 << i)):
                continue
            sign = (-1) ** ((mask & ((1 << i) - 1)).bit_count())
            for j in range(DIM):
                ee = list(e)
                ee[j] += 1
                accum(out, basis(tuple(ee), mask ^ (1 << i), h),
                      c * sign * A[i][j])
    return out


def delta(term):
    out = {}
    for (e, mask, h), c in term.items():
        for i in range(DIM):
            if not (mask & (1 << i)) or e[i] == 0:
                continue
            ee = list(e)
            ee[i] -= 1
            sign = (-1) ** ((mask & ((1 << i) - 1)).bit_count())
            accum(out, basis(tuple(ee), mask ^ (1 << i), h),
                  c * sign * e[i])
    return out


def add(*terms):
    out = {}
    for term in terms:
        for key, value in term.items():
            accum(out, key, value)
    return out


def d_quantum(term):
    quantum = {basis(e, mask, h + 1): c
               for (e, mask, h), c in delta(term).items()}
    return add(d_cl(term), quantum)


def multiply(left, right):
    out = {}
    for (e1, m1, h1), a in left.items():
        for (e2, m2, h2), b in right.items():
            if m1 & m2:
                continue
            inversions = sum((m1 >> (j + 1)).bit_count()
                             for j in range(DIM) if m2 & (1 << j))
            sign = (-1) ** inversions
            accum(out,
                  basis(tuple(x + y for x, y in zip(e1, e2)),
                        m1 | m2, h1 + h2),
                  sign * a * b)
    return out


def test_square_zero():
    count = 0
    for e in product(range(3), repeat=DIM):
        for mask in range(1 << DIM):
            for h in range(3):
                monomial = {basis(e, mask, h): Fraction(1)}
                assert d_cl(d_cl(monomial)) == {}, (e, mask, h, "dcl")
                assert delta(delta(monomial)) == {}, (e, mask, h, "delta")
                assert add(d_cl(delta(monomial)),
                           delta(d_cl(monomial))) == {}, (e, mask, h, "anticommute")
                assert d_quantum(d_quantum(monomial)) == {}, (e, mask, h, "dq")
                count += 1
    print(f"FREE_BV_DIFFERENTIAL_PASS exact_monomials={count}")


def test_disjoint_factorization():
    # A disjoint-open test uses a diagonal kinetic operator; the local
    # delta pairing still has no mixed contractions across supports.
    global A
    original = A
    A = ((Fraction(2), Fraction(0)), (Fraction(0), Fraction(3)))
    count = 0
    try:
        for e1, e2 in product(range(3), repeat=2):
            for m1, m2 in product(range(2), repeat=2):
                left = {basis((e1, 0), m1): Fraction(1)}
                right = {basis((0, e2), m2 << 1): Fraction(1)}
                lhs = d_quantum(multiply(left, right))
                sign = (-1) ** m1
                rhs = add(
                    multiply(d_quantum(left), right),
                    {key: sign * val for key, val in
                     multiply(left, d_quantum(right)).items()},
                )
                assert lhs == rhs, (e1, e2, m1, m2, lhs, rhs)
                count += 1
    finally:
        A = original
    x0xi1 = {basis((1, 0), 1 << 1): Fraction(1)}
    assert delta(x0xi1) == {}, "cross-support BV contraction must vanish"
    x0xi0 = {basis((1, 0), 1 << 0): Fraction(1)}
    assert delta(x0xi0) == {basis((0, 0), 0): Fraction(1)}
    print(f"DISJOINT_FACTOR_BV_PASS exact_products={count}")


def test_weiss_configuration_criterion():
    # A finite point set is *only* a toy slice of the Weiss condition.
    # Every finite n-tuple must be contained in one member of a Weiss
    # cover. This finite fixture is not a proof of smooth Cech descent.
    points = tuple(range(6))
    all_finite_subsets = [
        frozenset(v for v in points if mask & (1 << v))
        for mask in range(1, 1 << len(points))
    ]
    count = 0
    for n in range(1, 5):
        for tup in product(points, repeat=n):
            assert any(set(tup) <= U for U in all_finite_subsets)
            count += 1
    print(f"WEISS_FINITE_CONFIGURATION_PASS tuples={count}")


if __name__ == "__main__":
    test_square_zero()
    test_disjoint_factorization()
    test_weiss_configuration_criterion()
    print("EXT-015D-024 EXACT BOUNDED REGRESSIONS PASS (not infinite proof)")
