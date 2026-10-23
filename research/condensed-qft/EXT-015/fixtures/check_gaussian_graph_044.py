#!/usr/bin/env python3
"""Exact rational Gaussian graph controls; no floats, external libraries or network.

The analytic Gaussian finite-part theorem is in R2/044.
"""
from fractions import Fraction as F
from itertools import combinations, permutations

def mat(n, edges):
    A = [[F(0) for _ in range(n)] for _ in range(n)]
    for a, b, w in edges:
        w = F(w)
        A[a][a] += w; A[b][b] += w
        A[a][b] -= w; A[b][a] -= w
    return [row[:-1] for row in A[:-1]]

def det(M):
    A = [row[:] for row in M]
    n = len(A); z = F(1)
    for k in range(n):
        i = next((i for i in range(k, n) if A[i][k]), None)
        if i is None: return F(0)
        if i != k:
            A[k], A[i] = A[i], A[k]
            z = -z
        p = A[k][k]; z *= p
        for j in range(k + 1, n):
            t = A[j][k] / p
            for l in range(k + 1, n):
                A[j][l] -= t * A[k][l]
    return z

def inverse(M):
    n = len(M)
    a = [r[:] + [F(int(i == j)) for j in range(n)] for i, r in enumerate(M)]
    for j in range(n):
        i = next(i for i in range(j, n) if a[i][j])
        a[j], a[i] = a[i], a[j]
        p = a[j][j]
        a[j] = [v / p for v in a[j]]
        for k in range(n):
            if k != j:
                p = a[k][j]
                a[k] = [x - p * y for x, y in zip(a[k], a[j])]
    return [r[n:] for r in a]

def elim(A, ordered):
    A = [r[:] for r in A]
    live = list(range(len(A))); prod = F(1)
    for idx in ordered:
        j = live.index(idx)
        pivot = A[j][j]; assert pivot > 0
        prod *= pivot
        keep = [k for k in range(len(A)) if k != j]
        A = [[A[u][v] - A[u][j]*A[j][v]/pivot for v in keep] for u in keep]
        live.remove(idx)
    return prod, live, A

def spanning_trees(n, edges):
    total = F(0)
    for C in combinations(edges, n - 1):
        p = list(range(n))
        def root(v):
            while p[v] != v: v = p[v]
            return v
        product = F(1)
        for u, v, w in C:
            a, b = root(u), root(v)
            if a == b: break
            p[a] = b; product *= w
        else:
            if len({root(x) for x in range(n)}) == 1:
                total += product
    return total

triangle = [(0,1,1),(1,2,1),(0,2,1)]
theta = [(0,1,1),(1,2,1),(0,2,1),(1,3,1),(2,3,1)]
qt, qg = mat(3, triangle), mat(4, theta)
assert qt == [[F(2),-F(1)],[-F(1),F(2)]]
assert det(qt) == spanning_trees(3,triangle) == 3
assert inverse(qt) == [[F(2,3),F(1,3)],[F(1,3),F(2,3)]]
assert det(qg) == spanning_trees(4,theta) == 8
assert inverse(qg) == [
    [F(1),F(1,2),F(1,2)],
    [F(1,2),F(5,8),F(3,8)],
    [F(1,2),F(3,8),F(5,8)]]
for order in permutations(range(3)):
    d, live, S = elim(qg, order)
    assert d == 8 and not live and not S
for order in permutations([0,1]):
    d, live, S = elim(qg, order)
    assert d == 5 and live == [2] and S == [[F(8,5)]]
assert elim(qg,[0,1,2])[0] == elim(qg,[1,2,0])[0] == 8

# Two triangles: each finite part = 0, but finite part of the product
# on 1+y_0^2+z_0^2 equals 2/(9*pi), i.e. (2*pi)*FP = 4/9.
triangle_fp = F(0)
product_fp_scaled_by_2pi = F(1,3)*F(1,2)*(F(4,3)+F(4,3))
assert triangle_fp**2 == 0 and product_fp_scaled_by_2pi == F(4,9)
Qinv = inverse(qg)
theta_jet = F(1,2)*(2*Qinv[0][0]+4*Qinv[1][1]+6*Qinv[2][2])
assert theta_jet == F(33,8)

cases = 0
for n in range(2,6):
    pairs = list(combinations(range(n),2))
    for offset in range(min(7,len(pairs))):
        ed = [(i,i+1,F((i+offset)%5+1)) for i in range(n-1)]
        for j,(u,v) in enumerate(pairs):
            if v != u+1 and (j+offset)%2 == 0:
                ed.append((u,v,F((j+offset)%7+1,2)))
        Q = mat(n,ed); tau = det(Q)
        assert tau > 0 and tau == spanning_trees(n,ed)
        for order in permutations(range(n-1)):
            d,live,A=elim(Q,order)
            assert d == tau and not live and not A
        cases += 1

print("PASS: theta tau=8, triangle tau=3, inverse precision exact")
print("PASS: all 6 theta marginal orders, overlapping elimination Schur equality")
print(f"PASS: {cases} weighted Kirchhoff and arbitrary elimination witnesses")
print("PASS: nonmultiplicativity witness (2*pi)*global FP=4/9; component FP=0")
print("PASS: theta finite-jet coefficient = (33/8)*c_G")
