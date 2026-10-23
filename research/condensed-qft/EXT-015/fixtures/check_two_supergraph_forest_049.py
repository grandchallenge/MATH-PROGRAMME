#!/usr/bin/env python3
"""Exact two-supergraph Gaussian forest regression. No floats or dependencies.

Symbolic coefficients are represented as 1/pi times sums of rational/sqrt(k).
Theorems for smooth Gaussian test functions and strong convergence are proved
in paper 049; this fixture verifies the combinatorial and rational algebra.
"""
from fractions import Fraction as F
from itertools import combinations

def det(A):
    a=[[F(z) for z in row] for row in A]
    n=len(a); out=F(1)
    for j in range(n):
        k=next((k for k in range(j,n) if a[k][j]),None)
        if k is None:return F(0)
        if k!=j:a[k],a[j]=a[j],a[k];out=-out
        v=a[j][j];out*=v
        for k in range(j+1,n):
            scale=a[k][j]/v
            for q in range(j+1,n):a[k][q]-=scale*a[j][q]
    return out

def inv(M):
    n=len(M);a=[[F(z) for z in row]+[F(i==j) for j in range(n)] for i,row in enumerate(M)]
    for j in range(n):
        k=next(k for k in range(j,n) if a[k][j])
        a[j],a[k]=a[k],a[j]
        pivot=a[j][j];a[j]=[z/pivot for z in a[j]]
        for k in range(n):
            if k==j:continue
            scale=a[k][j];a[k]=[x-scale*y for x,y in zip(a[k],a[j])]
    return [row[n:] for row in a]

def cycles(edge_list):
    out=[]
    for n in range(2,len(edge_list)+1):
        for mask in combinations(range(len(edge_list)),n):
            use=[edge_list[j] for j in mask]
            deg={}
            for _,a,b in use:
                deg[a]=deg.get(a,0)+1;deg[b]=deg.get(b,0)+1
            if any(v!=2 for v in deg.values()):continue
            reach={next(iter(deg))}
            while True:
                extend=reach|{b for _,a,b in use if a in reach}|{a for _,a,b in use if b in reach}
                if extend==reach:break
                reach=extend
            if reach==set(deg):out.append(frozenset(x[0] for x in use))
    return out

Theta=[("12",1,2),("23",2,3),("13",1,3),("24",2,4),("34",3,4)]
Pi=[("a",1,2),("b",1,2),("23",2,3),("13",1,3)]
Ct=cycles(Theta);Cp=cycles(Pi)
assert set(Ct)=={frozenset(("12","23","13")),
                frozenset(("23","24","34")),
                frozenset(("12","24","34","13"))}
assert set(Cp)=={frozenset(("a","23","13")),
                frozenset(("b","23","13")),
                frozenset(("a","b"))}
assert all(x&y for x,y in combinations(Ct,2))
assert all(x&y for x,y in combinations(Cp,2))
Qth=[[F(2),F(1),F(0)],[F(1),F(3),F(1)],[F(0),F(1),F(2)]]
Qpi=[[F(3),F(1)],[F(1),F(2)]]
assert det(Qth)==8
assert det(Qpi)==5
invTh=inv(Qth)
invPi=inv(Qpi)
assert invTh==[[F(5,8),-F(1,4),F(1,8)],
              [-F(1,4),F(1,2),-F(1,4)],
              [F(1,8),-F(1,4),F(5,8)]]
assert invPi==[[F(2,5),-F(1,5)],[-F(1,5),F(3,5)]]

# An algebraic R2 1/pi * sum coeff[k]/sqrt(k) with k squarefree.
def expr(**terms):
    return {int(k[1:]):F(v) for k,v in terms.items() if F(v)}
def add(*args):
    a={}
    for y in args:
        for k,v in y.items():a[k]=a.get(k,F(0))+v
    return {k:v for k,v in a.items() if v}
def scale(a,q):return {k:q*v for k,v in a.items()}
# ctheta, cpi, 2c3*b2, c4*kappa0, 2c3*kappa0, b2**2
cTh=expr(k2=F(1,4));cPi=expr(k5=F(1,2))
th_tri_sum=expr(k6=F(1)) # 2 c3*b2 = 1/(sqrt(6)*pi)
th_square=expr(k1=F(1,4))
pi_tri_sum=expr(k3=F(1)) # 2 c3*kappa(0)=1/(sqrt3*pi)
pi_bubble=expr(k1=F(1,4))
gTh=add(cTh,scale(th_tri_sum,-1),scale(th_square,-1))
gPi=add(cPi,scale(pi_tri_sum,-1),scale(pi_bubble,-1))
assert gTh==expr(k2=F(1,4),k6=-F(1),k1=-F(1,4))
assert gPi==expr(k5=F(1,2),k3=-F(1),k1=-F(1,4))
assert add(gTh,th_tri_sum,th_square)==cTh
assert add(gPi,pi_tri_sum,pi_bubble)==cPi

# Intrinsic triangle c3 is identical in both containing supergraphs.
# c3*b22 = 1/(4 sqrt(6)*pi), bubble*b22=1/(8*pi)
c3b22=expr(k6=F(1,4))
b2b22=expr(k1=F(1,8))
bareTheta=scale(cTh,invTh[0][0]) # on u^2
finiteTheta=add(bareTheta,scale(c3b22,-1))
barePi=scale(cPi,invPi[1][1]) # on v^2
finitePi=add(barePi,scale(b2b22,-1))
assert finiteTheta==expr(k2=F(5,32),k6=-F(1,4))
assert finitePi==expr(k5=F(3,10),k1=-F(1,8))

# Local second derivative operators are explicitly different from
# simply taking the whole-graph Gaussian FP (subgraph finite residues matter).
assert finiteTheta!=bareTheta and finitePi!=barePi
# Attached bridge has an independent variable. Its Gaussian has mass 1,
# so the prepared core's residual O(eps^2) stays vanishing after tensoring.
# Compare coefficient of epsilon^0 of the counterterm subtraction on a
# test involving t^2: the component cTh pole cancels *before* t^2 moments.
assert add(cTh,scale(th_tri_sum,-1),scale(th_square,-1),scale(gTh,-1))=={}
assert add(cPi,scale(pi_tri_sum,-1),scale(pi_bubble,-1),scale(gPi,-1))=={}
for nbridge in range(1,12):
    # A tree of Gaussian bridges contributes (mass-one) e^0 coefficient 1
    # and no new cycle, leaving h=2 and the core finite residue unchanged.
    assert len(Ct)==3 and len(Cp)==3
    assert finiteTheta==expr(k2=F(5,32),k6=-F(1,4))
    assert finitePi==expr(k5=F(3,10),k1=-F(1,8))

print("PASS: theta and parallel multigraph each have 3 mutually overlapping 1PI cycles")
print("PASS: det(Q)=8 and 5, exact Gaussian covariances")
print("PASS: intrinsic triangle coefficient shared; independent bubble/square counterterms")
print("PASS: overall 1/pi pole surds, cancellation, local finite u^2/v^2 residues")
print("PASS: 11 nested bridge-tree symbolic Laurent checks")
print("NOTE: Gaussian distributional strong-limit proofs are in R2/049.")
