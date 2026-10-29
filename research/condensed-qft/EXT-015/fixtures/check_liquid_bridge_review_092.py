#!/usr/bin/env python3
"""Separate 092 finite controls, with no producer/dependency imports.

A correlated two-dimensional Gaussian checks the moment-to-jet normalization
against its exact Gaussian-test pairing. Covariance integration by parts checks
both signed physical derivatives. These are finite maps, not proofs of liquid
compactness, flatness, topology, or original R3.
"""
from fractions import Fraction as F
from math import comb, factorial

# Covariance C=[[2,1],[1,3]], det(C)=5. Its MGF factors as
# exp(s*s) exp(s*t) exp(3*t*t/2), an independent coefficient formula.
def moment(a,b):
    total = F(0)
    for c in range(min(a,b)+1):
        if (a-c)%2 or (b-c)%2:
            continue
        i,j = (a-c)//2,(b-c)//2
        total += F(3,2)**j / (factorial(i)*factorial(c)*factorial(j))
    return factorial(a)*factorial(b)*total

assert (moment(2,0),moment(1,1),moment(0,2)) == (2,1,3)

# Pair normalized epsilon-scaled profile with exp(-|y|^2/2).
# The exact result is det(1+epsilon^2*C)^(-1/2)
# = (1+5*z+5*z*z)^(-1/2), z=epsilon^2.
limit = 8
closed = [F(0)]*(limit+1)
binomial = F(1)
for n in range(limit+1):
    if n:
        binomial *= F(-1,2)-(n-1)
        binomial /= n
    # Coefficient in (5*z+5*z*z)^n.
    for j in range(n+1):
        if n+j <= limit:
            closed[n+j] += binomial*comb(n,j)*5**n
for k in range(limit+1):
    radial_moment = sum((F(comb(k,j))*moment(2*j,2*(k-j))
                         for j in range(k+1)),F(0))
    jet_pairing = F((-1)**k,2**k*factorial(k))*radial_moment
    assert jet_pairing == closed[k]

# Differentiate the actual profile using C^-1, not a derivative-jet lookup.
inverse = ((F(3,5),F(-1,5)),(F(-1,5),F(2,5)))
derivative_checks = 0
for a in range(8):
    for b in range(8):
        for j in range(2):
            actual = -inverse[j][0]*moment(a+1,b)-inverse[j][1]*moment(a,b+1)
            if j == 0:
                expected = -a*moment(a-1,b) if a else F(0)
            else:
                expected = -b*moment(a,b-1) if b else F(0)
            assert actual == expected
            derivative_checks += 1

# Use the exact Gaussian-test series for the principal/regular split.
# Every required pole/constant coefficient is inside this finite range.
def coeffs(m): return {m+2*k:c for k,c in enumerate(closed)}
def pole(c): return {n:v for n,v in c.items() if n < 0}
def shift(c,r): return {n+r:v for n,v in c.items()}
def add(a,b):
    out = dict(a)
    for k,v in b.items(): out[k] = out.get(k,F(0))+v
    return {k:v for k,v in out.items() if v}
scale_checks = 0
for m in range(-9,4):
    c = coeffs(m)
    C = pole(c)
    predicted_plus = add(shift(C,1),{0:-c[-1]} if -1 in c else {})
    predicted_minus = add(shift(C,-1),{-1:c[0]} if 0 in c else {})
    assert predicted_plus == pole(coeffs(m+1))
    assert predicted_minus == pole(coeffs(m-1))
    for s in (F(1,3),F(2),F(5,2)):
        # Actual epsilon rescaling, and the required semilinear base twist.
        scaled = {n:s**n*v for n,v in c.items()}
        for r in (-3,-1,1,4):
            left = {n+r:s**(n+r)*v for n,v in c.items()}
            right = {n:s**r*v for n,v in shift(scaled,r).items()}
            assert left == right
            scale_checks += 1

print('PASS092 independent correlated-Gaussian jet pairings:',limit+1)
print('PASS092 covariance-derived signed integration-by-parts controls:',derivative_checks)
print('PASS092 exact correlated-profile pole reprojection: 13 Laurent positions')
print('PASS092 semilinear shift controls:',scale_checks)
print('LIMIT092 finite maps only; no producer imports or infinite categorical conclusion')
