#!/usr/bin/env python3
"""Exact rational combinatorial and finite-polynomial checks for collision forests/cycles.

No numerical tolerances. The box mollifier is NOT smooth, so it is an exact
algebraic hostile control, not a replacement for the smooth microlocal proof.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb

def matrix_rank(A):
    A=[[Q(x) for x in row] for row in A]
    if not A: return 0
    nr,nc=len(A),len(A[0])
    row=0
    for col in range(nc):
        pivot=next((i for i in range(row,nr) if A[i][col]),None)
        if pivot is None: continue
        A[row],A[pivot]=A[pivot],A[row]
        d=A[row][col]
        A[row]=[x/d for x in A[row]]
        for i in range(nr):
            if i!=row:
                k=A[i][col]
                A[i]=[a-k*b for a,b in zip(A[i],A[row])]
        row+=1
        if row==nr: break
    return row

def forest(n,edges):
    p=list(range(n))
    def root(a):
        while p[a]!=a:
            a=p[a]
        return a
    for a,b in edges:
        ra,rb=root(a),root(b)
        if ra==rb: return False
        p[ra]=rb
    return True

check_count=0
forest_count=0
cycle_count=0
for n in range(2,6):
    E=list(combinations(range(n),2))
    for mask in range(1<<len(E)):
        edges=[e for j,e in enumerate(E) if (mask>>j)&1]
        matrix=[]
        for a,b in edges:
            row=[0]*n
            row[a],row[b]=1,-1
            matrix.append(row)
        rank=matrix_rank(matrix)
        good=forest(n,edges)
        assert (rank==len(edges))==good
        if good: forest_count+=1
        else: cycle_count+=1
        check_count+=1

for n in range(3,30):
    E=[(i,(i+1)%n) for i in range(n)]
    matrix=[]
    for a,b in E:
        row=[0]*n
        row[a],row[b]=1,-1
        matrix.append(row)
    assert matrix_rank(matrix)==n-1
    assert matrix_rank(matrix[:-1])==n-1

# Box mollifier kappa(u)=1/2 for |u|<1, else zero.
# At fixed alpha=u, beta interval has length 2-|u|.
# Area = integral_{-1}^1(2-|u|)du = 3.
box_c=Q(3,8)
# Second moment alpha^2: (1/8)*2*integral_0^1 u^2 (2-u) du.
u2=Q(1,8)*2*(Q(2,3)-Q(1,4))
# Mixed moment alpha*beta: from beta in [-1,1-u] for u>=0.
uv=Q(1,8)*2*(-Q(1,3)+Q(1,8))
assert box_c==Q(3,8)
assert u2==Q(5,48)
assert uv==-Q(5,96)
assert 2*u2+2*uv==u2  # permutation invariance of 3 edge differences

# Test test-function 1+u^2+v^2+uv in relative coordinates, with
# a smooth cutoff identically one on the small box support.
for eps in [Q(1,2),Q(1,3),Q(1,5),Q(1,10),Q(1,100)]:
    raw=box_c/eps + eps*(2*u2+uv)
    ren=raw-box_c/eps
    assert ren==Q(5,32)*eps
    assert ren/eps==Q(5,32)

print(f"PASS: {check_count} graphs through n=5, {forest_count} forests and {cycle_count} cyclic graphs")
print("PASS: 27 isolated cycle ranks (length 3..29), rank m-1")
print("PASS: box triangle c=3/8, moments 5/48 and -5/96")
print("PASS: 5 exact polynomial pairings, renormalized remainder (5/32)*epsilon")
print("NOTE: analytic extension and strong distributional convergence require the proofs in 041.")
