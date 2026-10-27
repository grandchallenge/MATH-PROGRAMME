"""Independent finite-moment checks; does not import the source fixture."""
from fractions import Fraction as F
from itertools import permutations

def determinant(matrix):
    n = len(matrix)
    total = F(0)
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i+1,n))
        term = F(-1 if inversions % 2 else 1)
        for i in range(n):
            term *= matrix[i][p[i]]
        total += term
    return total

diamond = [[3,-1,-1],[-1,2,0],[-1,0,2]]
five = [[4,-1,-1,-1],[-1,3,-1,0],[-1,-1,3,0],[-1,0,0,2]]
quotient = [[4,-1],[-1,2]]
def first_variance(matrix):
    minor = [row[1:] for row in matrix[1:]]
    return determinant(minor) / determinant(matrix)

assert determinant(diamond) == 8
assert first_variance(diamond) == F(1,2)
# m_D,11 = H11 / sqrt(8) = sqrt(2)/8.
assert first_variance(diamond) / 4 == F(1,8)
assert determinant(five) == 40 and first_variance(five) == F(2,5)
assert determinant(quotient) == 7 and first_variance(quotient) == F(2,7)
# Bare quartic: 3 H11^2 / sqrt(40) = (3/125) sqrt(10).
assert 3*first_variance(five)**2 / 20 == F(3,125)
# Each of triangles 023 and 123 contributes
# 3 (2/7)^2 / sqrt(3*7) = (4/343) sqrt(21).
per_triangle = 3*first_variance(quotient)**2 / 21
assert 2*per_triangle == F(8,343)
assert F(3,125)**2*10 != F(8,343)**2*21
print("PASS: independent Leibniz determinants and cofactor covariances")
print("PASS: diamond finite moment sqrt(2)/8")
print("PASS: F bare quartic minus exactly two triangle insertions")
print("PASS: F finite quartic 3sqrt(10)/125 - 8sqrt(21)/343 is nonzero")
