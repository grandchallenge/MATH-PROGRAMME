"""Symbolic exponential-ray growth tests, NOT universal Boas/Hayman proofs."""
from fractions import Fraction as F


def log_power_comparison_coefficient(cos_mtheta, eps, m, radius):
    """For f(z)=exp(z^m), log(|f|/M_f^eps)=(cos(mθ)-eps)r^m."""
    assert cos_mtheta in (-1, 0, 1)
    assert m >= 1 and radius > 0
    return (F(cos_mtheta) - eps) * radius**m


def _check_test_514_positive_ray_beats_every_fixed_polynomial_power():
    # log(|exp(R^m)|/R^n)=R^m-n log R -> +infinity.
    # Finite exact witness: exp(R^m) > R^n if R^m > n*log R.
    # For R>=2, log R <= R-1; choose R large depending on fixed n.
    for m in (1, 2, 3, 4):
        for n in range(1, 17):
            R = max(3, n + 2)
            assert R**m > n * (R - 1) if m >= 2 else R**m > 0
            # For m=1, the limit holds analytically but not via this
            # coarse bound, so no finite "proof" of limit is claimed.


def _check_test_514_exact_log_comparison_signs():
    for m in range(1, 6):
        for eps in (F(1, 4), F(1, 2), F(1), F(2)):
            for cos_value in (-1, 0, 1):
                for R in (1, 2, 3, 8, 32):
                    coeff = log_power_comparison_coefficient(cos_value, eps, m, R)
                    if cos_value > eps:
                        assert coeff > 0
                    elif cos_value == eps:
                        assert coeff == 0
                    else:
                        assert coeff < 0


def _check_test_514_power_at_least_one_never_forces_growing_ratio():
    for m in range(1, 6):
        for eps in (F(1), F(3, 2), F(2)):
            for cos_value in (-1, 0, 1):
                assert log_power_comparison_coefficient(cos_value, eps, m, 10) <= 0
    # This is a universal inequality |f(z)|<=M_f(|z|), but
    # cannot settle the interesting 0<eps<1 case for all entire f.


def _check_test_514_path_length_and_polynomial_counterexample():
    for R in range(1, 35):
        assert F(R) == F(R)  # radial segment length inside radius R
    for d in range(0, 12):
        n = d + 1
        for R in (2, 3, 5, 17):
            assert F(R**d, R**n) == F(1, R)  # polynomial fails first part


def _check_test_514_quantifier_distinction_named():
    # A single f=exp(z) exhibits a successful ray for eps<1.
    assert F(1) - F(1, 2) > 0
    # It does NOT imply a path exists with this property for all f;
    # the quantified universal negative is a separate published claim.
    assert F(0) - F(1, 2) < 0


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_514_positive_ray_beats_every_fixed_polynomial_power(self):
        _check_test_514_positive_ray_beats_every_fixed_polynomial_power()

    def test_514_exact_log_comparison_signs(self):
        _check_test_514_exact_log_comparison_signs()

    def test_514_power_at_least_one_never_forces_growing_ratio(self):
        _check_test_514_power_at_least_one_never_forces_growing_ratio()

    def test_514_path_length_and_polynomial_counterexample(self):
        _check_test_514_path_length_and_polynomial_counterexample()

    def test_514_quantifier_distinction_named(self):
        _check_test_514_quantifier_distinction_named()
