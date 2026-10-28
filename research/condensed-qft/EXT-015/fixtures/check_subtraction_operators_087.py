#!/usr/bin/env python3
"""Separate exact matrix/operator check for 087; no producer imports.

Polynomial keys (i,j) mean L_0^i D^j. The test verifies the entire
constant-coefficient marked Ward identity, rather than one scalar pairing.
"""
from fractions import Fraction as F
from math import factorial


def matrix_inverse(matrix):
    n = len(matrix)
    a = [[F(x) for x in row]+[F(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    det = F(1)
    for j in range(n):
        k = next(i for i in range(j, n) if a[i][j])
        if k != j:
            a[k], a[j] = a[j], a[k]
            det = -det
        pivot = a[j][j]
        det *= pivot
        a[j] = [x/pivot for x in a[j]]
        for i in range(n):
            if i != j:
                c = a[i][j]
                a[i] = [x-c*y for x, y in zip(a[i], a[j])]
    return det, [row[n:] for row in a]


edges = ((0,1),(0,2),(0,3),(1,2),(1,3),(2,3),(0,4),(1,4),(0,5),(1,5))
def laplacian(es):
    q = [[F(0)]*5 for _ in range(5)]
    for a,b in es:
        v = [F(int(i == b)-int(i == a)) for i in range(1,6)]
        for i in range(5):
            for j in range(5):
                q[i][j] += v[i]*v[j]
    return q
det0, cov0 = matrix_inverse(laplacian(edges))
det1, cov1 = matrix_inverse(laplacian(edges+((4,5),)))
w = [F(0),F(0),F(0),F(-1),F(1)]
z = [sum((cov0[i][j]*w[j] for j in range(5)), F(0)) for i in range(5)]
assert det0 == 96 and det1 == 192
assert z == [x/2 for x in w]
assert sum((w[i]*z[i] for i in range(5)), F(0)) == 1
assert cov1 == [[cov0[i][j]-z[i]*z[j]/2 for j in range(5)] for i in range(5)]


def add(a,b):
    c = dict(a)
    for k,v in b.items(): c[k] = c.get(k,F(0))+v
    return {k:v for k,v in c.items() if v}
def scale(a,c): return {k:v*c for k,v in a.items() if v*c}
def multiply(a,b):
    out = {}
    for (i,j),x in a.items():
        for (k,l),y in b.items(): out[i+k,j+l] = out.get((i+k,j+l), F(0))+x*y
    return {k:v for k,v in out.items() if v}
def power(a,n):
    out = {(0,0):F(1)}
    for _ in range(n): out = multiply(out,a)
    return out
def times_t(a):
    """t P(L,D)delta = -(2D partial_L + partial_D)P delta."""
    out = {}
    for (i,j),v in a.items():
        if i: out = add(out,{(i-1,j+1):-2*i*v})
        if j: out = add(out,{(i,j-1):-j*v})
    return out

L, D = {(1,0):F(1)}, {(0,1):F(1)}
L1 = add(L,scale(power(D,2),F(-1,2)))
delta6 = scale(power(L1,3),F(1,96))  # Common normalization is nu.
P4 = {(2,0):F(1,8),(1,2):F(1,8),(0,4):F(-1,96)}
Pprime7 = {(3,1):F(-1,96),(2,3):F(1,192),(1,5):F(-1,640),(0,7):F(1,5376)}
P8 = {(4,0):F(1,384),(3,2):F(1,192),(2,4):F(-1,768),(1,6):F(1,3840),(0,8):F(-1,43008)}
P6 = {(3,0):F(1,48),(2,2):F(1,32),(1,4):F(-1,192),(0,6):F(1,1920)}
rhs = add(add(delta6,scale(times_t(Pprime7),-2)),
          add(times_t(times_t(P8)),scale(P6,-1)))
lhs = multiply(power(D,2),P4)
assert lhs == rhs

def on_t_monomial(a,n):
    assert all(2*i+j == n for i,j in a)
    return factorial(n)*sum(a.values(),F(0))  # w.Cov_G.w=1 and Dt=1.
assert on_t_monomial(delta6,6) == F(15,16)
assert on_t_monomial(P4,4) == F(23,4)
assert on_t_monomial(times_t(Pprime7),6) == F(531,16)
assert on_t_monomial(times_t(times_t(P8)),6) == F(4353,16)
assert on_t_monomial(P6,6) == F(273,8)
assert on_t_monomial(lhs,6) == F(345,2)

# Whole-family epsilon-squared corrections, normalized by the same nu.
allocated_delta4 = scale(power(L1,2),F(1,16))
allocated_P2 = {(1,0):F(1,2),(0,2):F(1,4)}
assert on_t_monomial(allocated_delta4,4) == F(3,8)
assert on_t_monomial(allocated_P2,2) == F(3,2)

print('PASS087 operator: independent reduced matrices, determinants and covariance rank-one update')
print('PASS087 operator: complete marked Ward polynomial identity on every test')
print('PASS087 operator: all finite scalar constants and allocated-input normalizations')
print('LIMIT087 operator: finite identities, not the strong asymptotic theorem or global BV closure')
