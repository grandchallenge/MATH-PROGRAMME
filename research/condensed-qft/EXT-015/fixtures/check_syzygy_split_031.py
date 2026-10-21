#!/usr/bin/env python3
"""Exact finite-rank shadow of a categorical split syzygy; not a liquid Ext computation."""
from fractions import Fraction as Q

def matmul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),Q(0)) for j in range(len(b[0]))] for i in range(len(a))]

for n in range(1,21):
    # One singleton summand at v and two further at 2iv and (2i+1)v.
    m=1+2*n
    eps=[Q(1)]+[Q(0)]*(m-1)
    S=[[Q(0)]*n for _ in range(m)]
    Qmap=[[Q(0)]*m for _ in range(n)]
    for j in range(n):
        even,odd=1+2*j,2+2*j
        eps[even],eps[odd]=Q(2*(j+1)),Q(2*(j+1)+1)
        S[even][j],S[0][j],S[odd][j]=Q(1),Q(1),Q(-1)
        Qmap[j][even]=Q(1)
    assert all(sum(eps[i]*S[i][j] for i in range(m))==0 for j in range(n))
    assert matmul(Qmap,S)==[[Q(int(i==j)) for j in range(n)] for i in range(n)]
print("PASS: 20 rational finite-rank shadows; eps*S=0 and q*S=I")
print("NOTE: categorical proof uses actual singleton liquid coproduct summands.")
