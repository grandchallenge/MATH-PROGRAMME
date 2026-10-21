#!/usr/bin/env python3
"""Rational shadows of the all-singleton relation splitting (not liquid Ext certification)."""
from fractions import Fraction as F

def matmul(A,B):
    return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0)) for j in range(len(B[0]))] for i in range(len(A))]

tests=0
for d in range(1,6):
    for m in range(1,9):
        coeff=[[F(((i+2)*(j+3))%11-5, (i+j)%5+1) for j in range(m)] for i in range(d)]
        width=d+m
        epsilon=[[F(int(k==i)) if k<d else coeff[i][k-d] for k in range(width)] for i in range(d)]
        S=[[(-coeff[i][j] if i<d else F(int(i-d==j))) for j in range(m)] for i in range(width)]
        Qmap=[[F(int(i==d+j)) for i in range(width)] for j in range(m)]
        QS=matmul(Qmap,S)
        assert QS==[[F(int(i==j)) for j in range(m)] for i in range(m)]
        SQ=matmul(S,Qmap)
        Pi=[[F(int(i==j))-SQ[i][j] for j in range(width)] for i in range(width)]
        assert matmul(Pi,Pi)==Pi
        assert matmul(epsilon,Pi)==epsilon
        assert all(v==0 for row in matmul(epsilon,S) for v in row)
        tests+=1
print(f"PASS: {tests} exact models; q*s=I, Pi^2=Pi, eps*Pi=eps, eps*s=0")
print("NOTE: infinite liquid coproduct/projectivity is proved categorically, not by the fixture.")
