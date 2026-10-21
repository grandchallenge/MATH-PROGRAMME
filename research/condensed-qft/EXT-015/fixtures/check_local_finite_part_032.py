#!/usr/bin/env python3
"""Exact rational algebraic controls for the finite-part extension; not an analytic proof."""
from fractions import Fraction as Q
from math import comb

def cutoff_difference(m):
    # chi_(m+1)-chi_m = -z^2 (1-z^2)^m for |z|<1.
    return -2 * sum((Q((-1)**k*comb(m,k), 2*k+2) for k in range(m+1)), Q(0))

for m in range(1,15):
    assert cutoff_difference(m) == -Q(1,m+1)
assert cutoff_difference(4) == -Q(1,5)
print("PASS: 14 exact finite-polynomial cutoff variations; m=4 gives -1/5")
print("NOTE: finite-polynomial cutoffs are not C-infinity at their boundaries.")
