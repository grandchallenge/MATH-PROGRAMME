#!/usr/bin/env python3
"""LFO-010 exact finite LF-output/jet boundary controls.

Finite arithmetic fixtures, not a proof of the infinite analytic theorems.
No external packages.  Uses rational numbers only.
"""
from fractions import Fraction as Q
from math import factorial


def finite_jet_right_inverse(n: int):
    """Jet matrix diag(j!), polynomial right inverse diag(1/j!)."""
    jet = [[Q(factorial(i)) if i == j else Q(0) for j in range(n)]
           for i in range(n)]
    section = [[Q(1, factorial(i)) if i == j else Q(0) for j in range(n)]
               for i in range(n)]
    result = [[sum((jet[i][k] * section[k][j] for k in range(n)), Q(0))
               for j in range(n)] for i in range(n)]
    identity = [[Q(i == j) for j in range(n)] for i in range(n)]
    return result == identity


def polynomial_jet(coefficients):
    return tuple(Q(factorial(j)) * coefficients[j] for j in range(len(coefficients)))


def finite_section(a):
    return tuple(Q(value, factorial(j)) for j, value in enumerate(a))


def compact_support_identity(source_stage, target_stage):
    """A finite-support identity factors through target stage iff k<=L."""
    return source_stage <= target_stage


def kernel_pairing(a, b):
    """Finite witness of the smooth/bounded but not jointly LF-continuous kernel.

    a[j] = jth derivative of first test function at zero;
    b[j] = second function's value at the integer j.
    """
    return sum((Q(-1 if j % 2 else 1) * Q(a.get(j, 0)) * Q(b.get(j, 0))
                for j in set(a) & set(b) if j >= 1), Q(0))


def test_finite_jets():
    for n in (1, 2, 3, 5, 9, 16, 24):
        assert finite_jet_right_inverse(n)
        a = tuple(Q((-1) ** j * (j + 1), j + 2) for j in range(n))
        assert polynomial_jet(finite_section(a)) == a


def test_no_uniform_support():
    for fixed_target in range(1, 20):
        for source in range(1, fixed_target + 1):
            assert compact_support_identity(source, fixed_target)
        assert not compact_support_identity(fixed_target + 1, fixed_target)
    # Every individual source stage factors into SOME target stage.
    assert all(compact_support_identity(k, k) for k in range(1, 50))


def test_nonuniform_jet_semicontinuity():
    # For the canonical finite-order polynomial jet section, every column
    # has a nonzero C^0 value at x=1/2 near the origin; a genuinely
    # continuous map from the *infinite product* into C^0 must kill all
    # but finitely many input coordinate vectors in that seminorm.
    # This is only a finite consistency control, not the universal theorem.
    for cutoff in (1, 2, 4, 8, 16):
        for j in range(cutoff, cutoff + 15):
            canonical_column_at_half = Q(1, (2 ** j) * factorial(j))
            assert canonical_column_at_half > 0


def test_multilinear_kernel():
    for n in range(1, 16):
        a = {j: Q(j, 3) for j in range(1, n + 1)}
        b = {j: Q(1, j + 1) for j in range(1, n + 1)}
        val = kernel_pairing(a, b)
        expected = sum((Q(-1 if j % 2 else 1) * a[j] * b[j]
                        for j in range(1, n + 1)), Q(0))
        assert val == expected
        # Values supported beyond the output stage do not contribute.
        for outside in range(n + 1, n + 5):
            a2 = dict(a)
            a2[outside] = Q(97)
            assert kernel_pairing(a2, b) == val


def main():
    test_finite_jets()
    test_no_uniform_support()
    test_nonuniform_jet_semicontinuity()
    test_multilinear_kernel()
    print('LFO-010 strict LF target, jet and multilinear finite controls: PASS')


if __name__ == '__main__':
    main()
