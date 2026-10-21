#!/usr/bin/env python3
"""Exact difference-quotient obstruction for |a-b|/2; no floating point."""
from fractions import Fraction as Q
for k in range(1,101):
    h=Q(1, 2**k)
    positive=(abs(h)/2)/h
    negative=(abs(-h)/2)/(-h)
    assert positive == Q(1,2)
    assert negative == -Q(1,2)
# No scalar assignment at zero can change the two off-diagonal one-sided limits.
print("PASS: 100 exact rational approach scales, opposite slopes +1/2 and -1/2")
print("NOTE: any continuous extension forces the diagonal value to zero.")
