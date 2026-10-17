"""Exact rational petals for #511: source-semantics fixture, NOT Pommerenke's theorem."""
from fractions import Fraction as F


def radial_f_abs_squared(n, r):
    """For z=r*omega with omega^n=1: |z^n-1|^2 exactly."""
    return (r ** n - 1) ** 2


def _check_test_511_distinct_open_petals_have_length_more_than_one():
    for n in range(2, 97):
        r = F(1) + F(1, 4 * n)
        assert r > 1 and r ** n < 2
        assert radial_f_abs_squared(n, r) < 1
        assert radial_f_abs_squared(n, F(1)) == 0
        # Along each nth-root-of-unity ray, all 0<rho<2^(1/n)
        # lie in the strict lemniscate. The diameter >= r > 1.
        # There are n different angular sectors because Re(z^n)>0.


def _check_test_511_open_and_closed_boundary_at_zero_differ():
    for n in range(2, 80):
        assert radial_f_abs_squared(n, F(0)) == 1
        assert not radial_f_abs_squared(n, F(0)) < 1
        assert radial_f_abs_squared(n, F(0)) <= 1
        # Origin connects the closed petals, but is omitted by strict <1.


def _check_test_511_fixed_threshold_counterexample_not_proved_by_this_family():
    # 2^(1/n) --> 1. For every fixed epsilon>0, all sufficiently
    # large n have 2^(1/n) < 1+epsilon. Check exactly for examples.
    for epsilon in (F(1, 2), F(1, 4), F(1, 10)):
        n = 2
        while (1 + epsilon) ** n <= 2:
            n += 1
        assert (1 + epsilon) ** n > 2
        assert n <= 12  # checked concrete examples, not a uniform formula
        # The failed inference "n open petals >1 -> refutes fixed t>1"
        # is not allowed.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_511_distinct_open_petals_have_length_more_than_one(self):
        _check_test_511_distinct_open_petals_have_length_more_than_one()

    def test_511_open_and_closed_boundary_at_zero_differ(self):
        _check_test_511_open_and_closed_boundary_at_zero_differ()

    def test_511_fixed_threshold_counterexample_not_proved_by_this_family(self):
        _check_test_511_fixed_threshold_counterexample_not_proved_by_this_family()
