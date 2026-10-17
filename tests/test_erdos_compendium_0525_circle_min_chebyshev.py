"""Exact Laurent autocorrelation to real Chebyshev polynomial for #525.

Finite identities do not prove Cook--Nguyen's distributional limit.
"""
from itertools import product
from fractions import Fraction as F
import sympy as S
U,Z=S.symbols('u z')


def autocorr(eps):
    n=len(eps)-1
    return [None]+[sum(eps[k]*eps[k+j] for k in range(n+1-j)) for j in range(1,n+1)]


def ws(n):
    out=[S.Integer(2), U]
    for j in range(1,n):
        out.append(S.expand(U*out[-1]-out[-2]))
    return out[:n+1]


def norm_square_poly(eps):
    n=len(eps)-1
    C=autocorr(eps)
    W=ws(n)
    return S.Poly(n+1+sum(C[j]*W[j] for j in range(1,n+1)),U)


def _check_test_525_autocorrelation_chebyshev_identity_all_signs():
    for n in range(1,8):
        for eps in product((-1,1),repeat=n+1):
            H=norm_square_poly(eps).as_expr()
            p=sum(a*Z**k for k,a in enumerate(eps))
            # Formally z^-1 represents complex conjugation on |z|=1.
            laurent=S.expand(p*p.subs(Z,1/Z))
            via_cheb=S.expand(H.subs(U,Z+1/Z))
            assert S.cancel(via_cheb-laurent)==0
            assert all(c==int(c) for c in norm_square_poly(eps).all_coeffs())


def _check_test_525_exact_zero_circle_minimum_plus_polynomial():
    H=norm_square_poly((1,1,1))
    assert S.factor(H.as_expr())==(U+1)**2
    assert H.eval(-1)==0
    assert H.eval(2)==9  # z=1 gives |1+1+1|²=9.
    assert H.eval(-2)==1 # z=-1 gives |1-1+1|²=1.


def _check_test_525_exact_strictly_positive_example():
    H=norm_square_poly((1,1,-1))
    assert S.expand(H.as_expr())==5-U**2
    # On [-2,2], min H=1, so min |P| =1 and m<1 is FALSE.
    assert H.eval(-2)==H.eval(2)==1
    assert H.eval(0)==5


def _check_test_525_two_exponential_normalizations_are_not_identical():
    # Cook--Nguyen normalize a degree 2r polynomial by 1/sqrt(2r+1);
    # sqrt(N)*unscaled_min ~ 2r*normalized_min for N=2r.
    for r in range(1,20):
        N=2*r
        factor_squared=F(N*(2*r+1),r*r)
        assert factor_squared>4
        assert factor_squared == 4+F(2,r)
    # If survival of r*normalized_min has rate lambda=2sqrt(pi/3),
    # survival of sqrt(N)*unscaled_min has rate lambda/2.


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_525_autocorrelation_chebyshev_identity_all_signs(self):
        _check_test_525_autocorrelation_chebyshev_identity_all_signs()

    def test_525_exact_zero_circle_minimum_plus_polynomial(self):
        _check_test_525_exact_zero_circle_minimum_plus_polynomial()

    def test_525_exact_strictly_positive_example(self):
        _check_test_525_exact_strictly_positive_example()

    def test_525_two_exponential_normalizations_are_not_identical(self):
        _check_test_525_two_exponential_normalizations_are_not_identical()
