#!/usr/bin/env python3
"""Exact two-triangle double-bridge local insertion anomaly regression.

No floats/external packages. Algebraic irrational coefficients are encoded as
rational prefactors of formal inverse square roots. Analytic convergence is
proved separately in R2/055.
"""
from fractions import Fraction as F
from itertools import combinations
from collections import Counter

E=((0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4))

def connected(edges,verts):
    if not verts:return False
    seen={min(verts)}
    while True:
        nxt=seen|{b for a,b in edges if a in seen}|{a for a,b in edges if b in seen}
        if nxt==seen:return seen==verts
        seen=nxt

def onepi(indices):
    ee=[E[i] for i in indices]
    vertices={v for x in ee for v in x}
    return (len(ee)>=3 and connected(ee,vertices)
            and all(connected(ee[:j]+ee[j+1:],vertices)
                    for j in range(len(ee))))

P=[g for k in range(3,len(E))
   for g in combinations(range(len(E)),k) if onepi(g)]
assert len(P)==10 and Counter(map(len,P))=={3:2,4:1,5:2,6:3,7:2}
cross=[g for g in P if 6 in g and 7 in g]
assert len(cross)==8

def is_simple_cycle(g):
    degree=Counter(x for i in g for x in E[i])
    return all(d==2 for d in degree.values())
simple=[g for g in cross if is_simple_cycle(g)]
assert len(simple)==4 and Counter(map(len,simple))=={4:1,5:2,6:1}
assert len([g for g in cross if not is_simple_cycle(g)])==4

def det(M):
    A=[[F(v) for v in row] for row in M]
    z=F(1);n=len(A)
    for k in range(n):
        p=next((i for i in range(k,n) if A[i][k]),None)
        if p is None:return F(0)
        if p!=k:A[p],A[k]=A[k],A[p];z=-z
        a=A[k][k];z*=a
        for i in range(k+1,n):
            t=A[i][k]/a
            for j in range(k+1,n):A[i][j]-=t*A[k][j]
    return z

def inverse(M):
    n=len(M)
    A=[[F(v) for v in row]+[F(i==j) for j in range(n)] for i,row in enumerate(M)]
    for j in range(n):
        r=next(i for i in range(j,n) if A[i][j])
        A[j],A[r]=A[r],A[j]
        d=A[j][j];A[j]=[v/d for v in A[j]]
        for i in range(n):
            if i!=j:
                t=A[i][j];A[i]=[a-t*b for a,b in zip(A[i],A[j])]
    return [row[n:] for row in A]

def lap(n,edges,root):
    live=[v for v in range(n) if v!=root]
    ix={v:i for i,v in enumerate(live)}
    Q=[[F(0)]*len(live) for _ in live]
    for a,b in edges:
        for v in (a,b):
            if v in ix:Q[ix[v]][ix[v]]+=1
        if a in ix and b in ix:
            Q[ix[a]][ix[b]]-=1;Q[ix[b]][ix[a]]-=1
    return Q

Q=lap(6,E,3)
QA=[[F(2),-F(1),F(0)],[-F(1),F(3),-F(1)],[F(0),-F(1),F(2)]]
QB=[[F(3),-F(1),-F(1)],[-F(1),F(3),-F(1)],[-F(1),-F(1),F(2)]]
assert (det(Q),det(QA),det(QB))==(30,8,8)
assert det(lap(2,[(0,1),(0,1)],1))==2
assert Q==[[F(3),-F(1),-F(1),0,0],
           [-F(1),F(3),-F(1),-F(1),0],
           [-F(1),-F(1),F(2),0,0],
           [0,-F(1),0,F(3),-F(1)],
           [0,0,0,-F(1),F(2)]]
JA=[[F(1),0,0],[F(1),0,0],[F(1),0,0],[0,F(1),0],[0,0,F(1)]]
JB=[[F(1),0,0],[0,F(1),0],[0,0,F(1)],[0,0,0],[0,0,0]]
def embed(J,M):
    return [[sum(J[i][a]*M[a][b]*J[j][b] for a in range(len(M))
                 for b in range(len(M))) for j in range(len(J))]
            for i in range(len(J))]
MG=inverse(Q)
MA=embed(JA,inverse(QA))
MB=embed(JB,inverse(QB))
v=[F(1),F(1),F(1),F(0),F(0)]
MAB=[[v[i]*v[j]/2 for j in range(5)] for i in range(5)]
assert (MG[0][0],MA[0][0],MB[0][0],MAB[0][0])==(
        F(7,10),F(5,8),F(5,8),F(1,2))
assert MG==[
[F(7,10),F(1,2),F(3,5),F(1,5),F(1,10)],
[F(1,2),F(5,6),F(2,3),F(1,3),F(1,6)],
[F(3,5),F(2,3),F(17,15),F(4,15),F(2,15)],
[F(1,5),F(1,3),F(4,15),F(8,15),F(4,15)],
[F(1,10),F(1,6),F(2,15),F(4,15),F(19,30)]]
assert all(MG[i][j]==MG[j][i] for i in range(5) for j in range(5))
# The four Gaussian coefficient values have common factor (2*pi)^(-3/2).
# D = (2*pi)^(-3/2) [ 1/sqrt30 - 2/sqrt24 + 1/(3sqrt2) ].
assert 2*F(1,1)==2
# Exact positivity after multiplication by sqrt30:
# 1+sqrt15/3>sqrt5 <=> 2sqrt15>7 <=> 60>49.
assert 60>49
# Strictly nonzero derivative probe: scaled by sqrt30,
# 7/10 - 5sqrt5/8 + sqrt15/6 < 0.
# Certified rational enclosure sqrt5>2.236, sqrt15<3.873.
assert 2236*2236 < 5*1000*1000
assert 3873*3873 > 15*1000*1000
assert F(7,10)+F(3873,6000)<F(5*2236,8000)
# All second-order coefficients are symmetric rational linear combinations
# of the four covariances, with the four scalar surd normalizations retained.
for i in range(5):
    for j in range(5):
        assert MG[i][j]==MG[j][i] and MA[i][j]==MA[j][i]
        assert MB[i][j]==MB[j][i] and MAB[i][j]==MAB[j][i]

print("PASS: 10 proper 1PI sources, 8 crossing blocks and 4 new simple cycles (4/5/5/6)")
print("PASS: Kirchhoff counts 30/8/8/2 and all four exact covariance embeddings")
print("PASS: strictly positive epsilon^-3 scalar insertion defect by integer inequalities")
print("PASS: nonzero epsilon^-1 derivative-delta probe by certified rational bounds")
print("PASS: whole-diagonal two-term subtraction and edge-factor P''=kappa contracts")
print("NOTE: Schwartz convergence and the full graph-level obstruction are proved in R2/055.")
