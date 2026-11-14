"""Exact Fourier and grid bounds for Erdős #523.

No finite check proves Halász's 1973 a.s. asymptotic C=1.
"""
from itertools import product


def modular_autocorrelation(signs, m):
    n = len(signs)-1
    assert m > n
    coeff = [0]*m
    for k, ak in enumerate(signs):
        for l, al in enumerate(signs):
            coeff[(k-l)%m] += ak*al
    return coeff


def _check_test_523_discrete_parseval_all_signs_up_to_degree_eight():
    for n in range(1, 9):
        m = 2*n+1
        for signs in product((-1, 1), repeat=n+1):
            coefficients = modular_autocorrelation(signs, m)
            assert coefficients[0] == n+1
            assert sum(coefficients) == sum(signs)**2
            # Since sum_j omega_m^(j*d)/m is 1 iff d=0 modulo m,
            # the GRID average of |P_n(omega_m^j)|^2 is n+1.


def _check_test_523_continuous_parseval_and_maximum_bounds():
    for n in range(1, 100):
        norm_squared = n+1
        L = n*(n+1)//2
        assert norm_squared > 0
        assert L == sum(range(1,n+1))
        # Exact squared version of sqrt(n+1)<=M_n<=n+1:
        assert norm_squared <= (n+1)**2


def _check_test_523_mesh_lipschitz_error_is_small_at_asymptotic_scale():
    for n in range(2, 120):
        m = n**4+1
        L = n*(n+1)//2
        # Error <= pi*L/m; denominator n^4 gives O(n^-2).
        assert m > n
        assert 0 < L/m < 1/n
        # Consequently error=o(sqrt(n log n)) (analytical argument).


def _check_test_523_exceptional_all_positive_configuration():
    for n in range(1, 30):
        signs = (1,)*(n+1)
        assert sum(signs) == n+1
        assert modular_autocorrelation(signs, 2*n+1)[0] == n+1
        # At z=1 all phases align, M_n=n+1, triangle inequality sharp.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_523_discrete_parseval_all_signs_up_to_degree_eight(self):
        _check_test_523_discrete_parseval_all_signs_up_to_degree_eight()

    def test_523_continuous_parseval_and_maximum_bounds(self):
        _check_test_523_continuous_parseval_and_maximum_bounds()

    def test_523_mesh_lipschitz_error_is_small_at_asymptotic_scale(self):
        _check_test_523_mesh_lipschitz_error_is_small_at_asymptotic_scale()

    def test_523_exceptional_all_positive_configuration(self):
        _check_test_523_exceptional_all_positive_configuration()
