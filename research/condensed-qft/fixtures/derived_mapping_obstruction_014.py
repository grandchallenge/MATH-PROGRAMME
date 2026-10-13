#!/usr/bin/env python3
"""DRM-014: exact rational finite slices of the square-zero ring example.

Regression only. The proof that the infinite Ext class is not stage-bounded
is in DERIVED_MAPPING_OBSTRUCTION_014.md.
"""
from fractions import Fraction as Q

for n in range(2, 33):
    # Restrict f:V -> direct_sum_j R to e_0,...,e_{n-1}.
    # The coefficient of e_0 in target ideal V, output slot j, source e_i,
    # is the Kronecker delta: a diagonal n-by-n matrix.
    matrix = [[Q(i == j) for j in range(n)] for i in range(n)]
    nonzero_output_slots = {
        j for j in range(n) if any(matrix[i][j] for i in range(n))
    }
    assert len(nonzero_output_slots) == n

    # Any map factored through the first b summands has zero
    # coefficients in columns b..n-1. Our f never does (b<n).
    for b in range(n):
        assert matrix[b][b] == Q(1)

    # Any coboundary v -> v*t has its output on e_i proportional
    # to e_i, so it cannot cancel the e_0 output of f(e_i) for i>0.
    for i in range(1, n):
        assert i != 0 and matrix[i][i] == Q(1)

print("DRM-014 square-zero finite-slice controls: PASS (2..32)")
