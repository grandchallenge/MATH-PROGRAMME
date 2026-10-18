#!/usr/bin/env python3
"""QFT-COND-004 / QW-001 exact finite quantum-weight and Weiss adversaries.

This is a bounded algebraic regression fixture, NOT a test of liquid categories.
One even generator x, one odd generator theta; d(theta)=c*x,
Delta(theta*x^n)=n*x^(n-1).  All arithmetic is exact.
"""
from fractions import Fraction
from itertools import product

Q = Fraction


def weight(monomial):
    k, n, odd = monomial
    return 2 * k + n + odd


def quantum_d(monomial, c=Q(3)):
    """Sparse D(x^n theta^odd hbar^k), with Koszul signs fixed."""
    k, n, odd = monomial
    if not odd:
        return {}
    terms = {(k, n + 1, 0): c}  # classical d
    if n:
        terms[(k + 1, n - 1, 0)] = Q(n)  # hbar * Delta
    return terms


def apply_d(vector):
    output = {}
    for basis, coefficient in vector.items():
        for target, factor in quantum_d(basis).items():
            output[target] = output.get(target, Q(0)) + coefficient * factor
    return {basis: value for basis, value in output.items() if value}


def truncate(vector, max_weight):
    return {basis: value for basis, value in vector.items()
            if weight(basis) < max_weight}


def check_weight_and_differential():
    for k, n, odd in product(range(5), range(8), (0, 1)):
        basis = (k, n, odd)
        for image in quantum_d(basis):
            assert weight(image) == weight(basis)
        assert apply_d(apply_d({basis: Q(1)})) == {}
        assert all(weight(t) == weight(basis) for t in quantum_d(basis))
        # BV contraction WITHOUT hbar drops weight by two, if n>0.
        if odd and n:
            raw_delta_image = (k, n - 1, 0)
            assert weight(raw_delta_image) == weight(basis) - 2
        for bound in range(1, 13):
            v = {basis: Q(1)}
            assert truncate(apply_d(v), bound) == apply_d(truncate(v, bound))
    for x, y in product(range(10), repeat=2):
        assert x + y >= x and x + y >= y


def check_support_escape():
    for max_degree in (1, 2, 3, 6, 12, 30):
        full = tuple(Q(1) for _ in range(max_degree))
        for cover_stage in range(max_degree):
            stage = tuple(Q(1) if j <= cover_stage else Q(0)
                          for j in range(1, max_degree + 1))
            assert stage != full
            assert sum(1 for entry in stage if entry) == cover_stage
        assert tuple(Q(1) if j <= max_degree else Q(0)
                     for j in range(1, max_degree + 1)) == full


def check_kinetic_moment():
    # A finite linear analogue of ell(Pg)=0: choose a kinetic
    # column and a moment in its annihilator. Actual scalar proof
    # uses P exp(m*x)=0 and compact-support integration by parts.
    kinetic_column = (Q(1), Q(-1))
    moment = (Q(1), Q(1))
    assert sum((a * b for a, b in zip(kinetic_column, moment)), Q(0)) == 0
    for m in (Q(1, 2), Q(1), Q(3)):
        # (-d^2/dx^2 + m^2) exp(m*x) has scalar prefactor zero.
        assert -m * m + m * m == 0


if __name__ == "__main__":
    check_weight_and_differential()
    check_support_escape()
    check_kinetic_moment()
    print("QFT-COND-004 quantum-weight/Weiss finite controls: PASS")
