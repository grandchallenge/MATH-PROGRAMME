"""Exact dyadic variance examples for proved Erdős #527.

Finite orthogonality is not a proof of a random Hausdorff-dimension-one
set of convergence points.
"""
from fractions import Fraction as F
from itertools import product


def bitlog(n):
    assert n>=1
    return n.bit_length()-1


def coefficient_squared(n):
    return F(1,n*(1+bitlog(n)))


def multiply_i_power(a,k):
    # Exact Gaussian rational pair for a*i^k.
    k%=4
    if k==0:return (a,F(0))
    if k==1:return (F(0),a)
    if k==2:return (-a,F(0))
    return (F(0),-a)


def _check_test_527_non_square_summable_dyadic_coefficient_example():
    for j in range(0,10):
        start,stop=2**j,2**(j+1)
        block=sum((coefficient_squared(n) for n in range(start,stop)),F(0))
        assert block>=F(1,2*(j+1))
        assert all(bitlog(n)==j for n in range(start,stop))
    # a_n^2 = 1/[n(1+floor(log2 n))],
    # sqrt(n)|a_n| = [1+floor(log2 n)]^(-1/2) ->0.
    # Block energy lower bound diverges as harmonic series.


def _check_test_527_exact_complex_rademacher_variance():
    weights=[F(1,n+1) for n in range(1,9)]
    variance=sum((a*a for a in weights),F(0))
    for mode in ('one','minus_one','i'):
        totals=[]
        for eps in product((-1,1),repeat=len(weights)):
            real=imag=F(0)
            for n,(a,e) in enumerate(zip(weights,eps),start=1):
                if mode=='one': x,y=(a,F(0))
                elif mode=='minus_one':x,y=(a*(-1)**n,F(0))
                else:x,y=multiply_i_power(a,n)
                real+=e*x
                imag+=e*y
            totals.append((real,imag))
        count=len(totals)
        assert sum((r for r,i in totals),F(0))==0
        assert sum((i for r,i in totals),F(0))==0
        average_norm=sum((r*r+i*i for r,i in totals),F(0))/count
        assert average_norm==variance


def _check_test_527_existence_quantifiers_do_not_swap():
    # In the divergent-square-sum regime, any FIXED z diverges a.s.
    # Yet 2025 theorem asserts (almost surely) EXISTS z that converges.
    for j in range(1,20):
        assert F(1,j+1)>0
    assert F(1,2)+F(1,3)>F(1,2)
    # These exact bounded checks are deliberately not a stochastic proof.


def _check_test_527_monotonicity_not_part_of_main_theorem():
    # Coefficients can be zero on arbitrary indices, or oscillate in
    # magnitude, provided sqrt(n)*abs(a_n)->0.
    # Example squared magnitudes b_n = (1 or 2)/[n(1+floor(log2 n))]
    # for even/odd n, still satisfy both target statements.
    for j in range(1,10):
        n=2**j
        b_even=coefficient_squared(n)
        b_next=2*coefficient_squared(n+1)
        assert b_even>0 and b_next>0
        assert n*b_even==F(1,j+1)
        assert (n+1)*b_next==F(2,j+1)


import unittest


class CompendiumFiniteQA(unittest.TestCase):
    def test_527_non_square_summable_dyadic_coefficient_example(self):
        _check_test_527_non_square_summable_dyadic_coefficient_example()

    def test_527_exact_complex_rademacher_variance(self):
        _check_test_527_exact_complex_rademacher_variance()

    def test_527_existence_quantifiers_do_not_swap(self):
        _check_test_527_existence_quantifiers_do_not_swap()

    def test_527_monotonicity_not_part_of_main_theorem(self):
        _check_test_527_monotonicity_not_part_of_main_theorem()
