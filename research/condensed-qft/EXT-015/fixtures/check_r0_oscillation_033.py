#!/usr/bin/env python3
"""Exact finite diagonal benchmark for R0 Theorem 33.1, not a smooth-family proof."""
from fractions import Fraction as Q
from math import comb

# Finite-regularity polynomial surrogate rho=x^3(1-x)^3 supported on [0,1].
rho = {3+k: Q((-1)**k*comb(3,k)) for k in range(4)}
rho2 = {}
for i,a in rho.items():
    for j,b in rho.items():
        rho2[i+j] = rho2.get(i+j,Q(0)) + a*b
diagonal = sum((v/Q(k+1) for k,v in rho2.items()),Q(0))
assert diagonal == Q(1,12012)
assert diagonal > 0
# For every t !=0 the oscillatory phase cos((x-y)/t) equals 1 on x=y,
# while the t=0 kernel is identically zero. Discontinuity is exact.
assert diagonal != Q(0)
print("PASS: oscillatory diagonal jumps from 0 to 1/12012 (exact rational control)")
print("NOTE: proof of strong distributional smoothness uses nonstationary phase, not this fixture.")
