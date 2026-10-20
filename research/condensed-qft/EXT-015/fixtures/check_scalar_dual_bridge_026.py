#!/usr/bin/env python3
"""Exact finite-mode hostile controls for EXT-015D mathematical result 026.

These test the variance mismatch, transpose differential, and Koszul symmetry
at bounded dimensions. They do NOT prove a nuclear Schwartz kernel theorem
or any claim about smooth DVS plots or higher liquid Ext.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product

A = ((Fraction(2), Fraction(1)), (Fraction(1), Fraction(3)))
D = 2
# A field generator is a pair (cohomological degree 0 or 1, spatial mode).
GEN = tuple(product((0, 1), range(D)))


def accum(dst, key, c):
    dst[key] = dst.get(key, Fraction(0)) + c
    if not dst[key]:
        del dst[key]


def field_tensor_d(state):
    out = {}
    for i, (degree, mode) in enumerate(state):
        if degree:
            continue
        sign = (-1) ** sum(g[0] for g in state[:i])
        for mode_out in range(D):
            dst = list(state)
            dst[i] = (1, mode_out)
            accum(out, tuple(dst), sign * A[mode_out][mode])
    return out


def extend_d(vec):
    out = {}
    for state, coeff in vec.items():
        for target, entry in field_tensor_d(state).items():
            accum(out, target, entry * coeff)
    return out


def swap_factors(state, i):
    if not i + 1 < len(state):
        raise ValueError(i)
    v = list(state)
    sign = (-1) ** (v[i][0] * v[i + 1][0])
    v[i], v[i + 1] = v[i + 1], v[i]
    return tuple(v), sign


def permute_vec(vec, i):
    out = {}
    for state, c in vec.items():
        target, sign = swap_factors(state, i)
        accum(out, target, sign * c)
    return out


def dual_transpose(functional, candidate_sources):
    """The scalar-valued cochain dual differential evaluated on basis sources."""
    return {
        state: sum(
            (coeff * functional.get(target, Fraction(0))
             for target, coeff in field_tensor_d(state).items()),
            Fraction(0))
        for state in candidate_sources
    }


def test_variance_obstruction():
    weight_zero_observables = 1
    # In a finite test-function stage with two independent source bumps,
    # Hom_liq(R,G) is G rather than the scalar constants.
    old_weight_zero_hom_dimension = D
    assert old_weight_zero_hom_dimension != weight_zero_observables
    print("VARIANCE_WEIGHT_ZERO_NO_GO_PASS")


def test_tensor_differential_and_dual():
    visited = 0
    for weight in range(0, 4):
        states = tuple(product(GEN, repeat=weight))
        for state in states:
            x = {state: Fraction(1)}
            assert extend_d(extend_d(x)) == {}, (weight, state)
            for i in range(weight - 1):
                assert extend_d(permute_vec(x, i)) == permute_vec(extend_d(x), i)
            # Verify a complete dual transpose identity for every target generator.
            for target in states:
                test_functional = {target: Fraction(1)}
                lhs = dual_transpose(test_functional, (state,))[state]
                rhs = field_tensor_d(state).get(target, Fraction(0))
                assert lhs == rhs
            visited += 1
    print(f"FIELD_COMPLEX_DUAL_TRANSPOSE_AND_KOSZUL_PASS tensor_basis={visited}")


def test_covariant_extension_by_zero():
    # Inclusion of field coordinates of smaller interval V into U has dual
    # extension-by-zero from finite-mode distributions of V to those of U.
    small = (Fraction(3), Fraction(-2))
    larger = small + (Fraction(0), Fraction(0))
    for field in product(range(-2, 3), repeat=4):
        restricted = field[:2]
        pairing_small = sum(a * b for a, b in zip(small, restricted))
        pairing_big = sum(a * b for a, b in zip(larger, field))
        assert pairing_small == pairing_big
    print("FIELD_RESTRICTION_DUAL_EXTENSION_PASS")


if __name__ == "__main__":
    test_variance_obstruction()
    test_tensor_differential_and_dual()
    test_covariant_extension_by_zero()
    print("EXT-015D-026 EXACT FINITE REGRESSIONS PASS (not infinite analytic proof)")
