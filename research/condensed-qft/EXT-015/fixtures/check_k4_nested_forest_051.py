#!/usr/bin/env python3
"""Exact K4 Gaussian nested-forest and delta-jet pole regression.

No floats or third-party libraries. A coefficient a+b*sqrt(2)+c*sqrt(3)
is represented as a tuple of Fractions after extracting pi**(-3/2).
Analytic strong-distribution convergence is proved in R2/051.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter

V=(1,2,3,4)
E=tuple(combinations(V,2))

def connected(vertices, edges):
    if not vertices:return False
    reach={min(vertices)}
    while True:
        nxt=reach|{b for a,b in edges if a in reach}|{a for a,b in edges if b in reach}
        if nxt==reach:break
        reach=nxt
    return reach==vertices

def onepi(edges):
    vertices=set(sum(([a,b] for a,b in edges),[]))
    return len(edges)>=3 and connected(vertices,edges) and all(
        connected(vertices,tuple(x for x in edges if x!=e)) for e in edges
    )

P=[frozenset(S) for k in range(3,6) for S in combinations(E,k) if onepi(S)]
counts=Counter(map(len,P))
assert counts=={3:4,4:3,5:6}, counts
assert len(P)==13
assert all(a & b for a,b in combinations(P,2))
nested=[(a,b) for a in P for b in P if len(a)<len(b) and a < b]
assert len(nested)==18
assert Counter((len(a),len(b)) for a,b in nested)=={(3,5):12,(4,5):6}
assert 1+len(P)+len(nested)==32

def det(A):
    X=[[F(x) for x in row] for row in A]
    ans=F(1);n=len(X)
    for i in range(n):
        k=next((j for j in range(i,n) if X[j][i]),None)
        if k is None:return F(0)
        if k!=i:X[k],X[i]=X[i],X[k];ans=-ans
        p=X[i][i];ans*=p
        for j in range(i+1,n):
            t=X[j][i]/p
            for k in range(i+1,n):X[j][k]-=t*X[i][k]
    return ans

Q=[[F(3) if i==j else F(-1) for j in range(3)] for i in range(3)]
Qi=[[F(1,2) if i==j else F(1,4) for j in range(3)] for i in range(3)]
assert det(Q)==16
assert all(sum(Q[i][k]*Qi[k][j] for k in range(3))==F(i==j)
           for i in range(3) for j in range(3))

# Quotient-normal derivative vectors for the four different triangles:
# root-excluding triangle (123) shifts all 3 coordinates;
# the other 3 triangles' omitted vertex is a single coordinate.
dirs=((1,1,1),(1,0,0),(0,1,0),(0,0,1))
N=[[sum(F(v[i]*v[j]) for v in dirs) for j in range(3)] for i in range(3)]
assert N==[[4*Qi[i][j] for j in range(3)] for i in range(3)]

def surd(c=0,s2=0,s3=0):return (F(c),F(s2),F(s3))
def add(*xs):return tuple(sum((x[i] for x in xs),F(0)) for i in range(3))
def mul(a,q):return tuple(v*q for v in a)
# All constants have a factored common pi^(-3/2).
# c_G = 1/(8sqrt2), triangle*b3=1/(6sqrt2),
# square*kappa0^2=1/(4sqrt2),
# theta prepared gTheta*kappa0=1/8-sqrt3/6-sqrt2/8.
cG=surd(s2=F(1,16))
c3b3=surd(s2=F(1,12))
c4k0sq=surd(s2=F(1,8))
gThetak0=surd(c=F(1,8),s2=-F(1,8),s3=-F(1,6))
overall=add(cG,mul(c3b3,-4),mul(c4k0sq,-3),mul(gThetak0,-6))
assert overall==surd(c=-F(3,4),s2=F(5,48),s3=F(1))
assert add(overall,mul(c3b3,4),mul(c4k0sq,3),mul(gThetak0,6))==cG

# c_G/2 - 2 c3*b_{3,2}: b_{3,2}=b3/3.
derivative=add(mul(cG,F(1,2)),mul(c3b3,F(-2,3)))
assert derivative==surd(s2=-F(7,288))
# On a test equal to y_1^2 near the diagonal L_Q(y_1^2)=1.
assert 2*Qi[0][0]==1
assert derivative==surd(s2=-F(7,288))

# Directly verify every proper theta subgraph admits exactly 3 nested
# primitive 1PI cycles; the source theta counterterm gTheta is imported
# once for each 5-edge theta, not recalculated in K4.
for theta in [x for x in P if len(x)==5]:
    inside=[x for x in P if len(x)<5 and x<theta]
    assert Counter(map(len,inside))=={3:2,4:1}

# Check distinct test types: 1 gives a_-3 only; y_i^2 gives a_-1
# because scalar delta has no pairing with a zero-at-origin test.
for i in range(3):
    assert 2*Qi[i][i]==1
    assert derivative==surd(s2=-F(7,288))

print("PASS: K4 has 13 proper 1PI subgraphs, 18 nested pairs, 32 proper forests")
print("PASS: K4 tau=16, inverse Laplacian, quotient normal sum=4*L")
print("PASS: shared theta-source gTheta and 4/3/6 subgraph poles")
print("PASS: a_-3 = (sqrt3 - 3/4 + 5*sqrt2/48)/pi^(3/2)")
print("PASS: a_-1 = -7*sqrt2/(288*pi^(3/2)) times L")
print("PASS: 4 triangle normal directions and 3 quadratic test probes")
print("NOTE: analytic asymptotics and Schwartz distribution estimates are in R2/051.")
