"""Exact Fabry/Fejér logical distinction for open Erdős #517.

No finite coefficient experiment certifies the infinite-value conjecture.
"""
from fractions import Fraction as F
from math import factorial


def bitlen(k):
    assert k >= 1
    return k.bit_length()


def exponent(k):
    return k * bitlen(k)


def test_517_fabry_exponents_strict_and_unbounded_ratio():
    previous = 0
    for k in range(1, 1025):
        n = exponent(k)
        assert n > previous
        assert F(n, k) == bitlen(k)
        previous = n
    for J in range(1, 11):
        assert F(exponent(2 ** J), 2 ** J) == J + 1
    # Ratio tends to infinity as bit length tends to infinity.


def test_517_dyadic_block_reciprocal_lower_bound():
    for j in range(10):
        start, stop = 2 ** j, 2 ** (j + 1)
        block = sum((F(1, exponent(k)) for k in range(start, stop)), F(0))
        assert block >= F(1, 2 * (j + 1))
        assert all(bitlen(k) == j + 1 for k in range(start, stop))
    # Summing over j gives at least half a divergent harmonic series.
    # Thus the Fabry condition does not imply sum(1/n_k)<infinity.


def test_517_factorial_coefficient_subseries_exact_domination():
    for r in (F(0), F(1, 2), F(1), F(2), F(3)):
        # k<=12 is an exact SUBSUM of the exponential Taylor series.
        ks = range(1, 13)
        selected = sum((r ** exponent(k) / factorial(exponent(k)) for k in ks), F(0))
        all_degrees = sum((r ** m / factorial(m) for m in range(0, exponent(12) + 1)), F(0))
        assert 0 <= selected <= all_degrees
        assert len({exponent(k) for k in ks}) == 12
    # Infinite extension follows by termwise domination by exp(|z|).


def test_517_an_omitted_value_example_is_not_fabry():
    for m in (1, 2, 3, 5, 13):
        assert all(F(m*k, k) == m for k in range(1, 100))
        # exp(z^m) omits zero but does not have n_k/k -> infinity.
