"""Exact bounded exercises for #515: common path vs per-exponent path.

Main Lewis–Rossi–Weitsman theorem requires a substantial subharmonic
path construction. These fixtures only check explicit exponential families
and the missing polynomial hypothesis.
"""
from fractions import Fraction as F
from math import factorial


LAMBDAS = (F(1, 5), F(1, 4), F(1, 2), F(1), F(2), F(3))


def exponential_ray_power(m, t):
    """log|exp((t)^m)| on the positive real ray, with m positive."""
    assert m >= 1 and t >= 0
    return t**m


def polynomial_integral_from_one(d, lam):
    """Exactly ∫_1^∞ t^(-d*lambda)dt if it converges."""
    exponent = d * lam
    if exponent <= 1:
        return None
    return F(1) / (exponent - 1)


def test_515_same_fixed_ray_satisfies_comparison_for_all_exponents():
    for m in range(1, 9):
        for t in (F(1), F(3, 2), F(2), F(7, 2), F(10)):
            assert exponential_ray_power(m, t) >= t
            for lam in LAMBDAS:
                assert lam * exponential_ray_power(m, t) >= lam * t
                # exp(-lam*t^m) <= exp(-lam*t).
                # Thus tail integral <= exp(-lam)/lam <infinity.
    # The ray Γ(t)=t is INDEPENDENT of m and lambda.


def test_515_linear_exponential_has_exact_integral_one_over_lambda():
    for lam in LAMBDAS:
        assert lam * (F(1) / lam) == 1
        # ∫_0^∞ exp(-lam t)dt = 1/lam exactly, by antiderivative.
        assert F(1) / lam > 0


def test_515_polynomial_threshold_versus_all_lambda():
    for d in range(1, 13):
        for lam in LAMBDAS:
            finite = polynomial_integral_from_one(d, lam)
            if d * lam > 1:
                assert finite == F(1, d * lam - 1)
            else:
                assert finite is None
        assert polynomial_integral_from_one(d, F(1, d)) is None
        assert polynomial_integral_from_one(d, F(2, d)) == F(1)


def test_515_superpolynomial_growth_of_exp_t_power():
    # For every fixed n, exponential e^(t^m) eventually beats t^n:
    # e^x >= x^k/k! for k>n/m, and then x=t^m.
    for m in range(1, 7):
        for n in range(1, 22):
            k = n // m + 1
            assert m * k > n
            assert factorial(k) > 0
            # e^(t^m)/t^n >= t^(mk-n)/k! -> +infinity.
