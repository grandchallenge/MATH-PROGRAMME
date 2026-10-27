#!/usr/bin/env python3
"""R2/063: exact two-external-vertex Gaussian quotient and differentiated K4 jet.

All assertions use rational arithmetic (Fractions). Formal A,B stand for
the intrinsic K4 overall scalar and second-normal-derivative coefficients
from protected R2/051; no floats and no re-fitting to a supergraph.
"""
from fractions import Fraction as F
from itertools import product

H=[[F(1,2) if i==j else F(1,4) for j in range(3)] for i in range(3)]
ZERO=F(0)
def matmul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),ZERO)
             for j in range(len(b[0]))] for i in range(len(a))]
def transp(a):return [list(x) for x in zip(*a)]
def sub(a,b):return [[a[i][j]-b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def trprod(a,b):
    return sum((a[i][j]*b[j][i] for i in range(len(a)) for j in range(len(a))),ZERO)
def inverse2(m):
    d=m[0][0]*m[1][1]-m[0][1]*m[1][0]
    assert d>0
    return [[m[1][1]/d,-m[0][1]/d],[-m[1][0]/d,m[0][0]/d]],d
def energy(edges):
    # source 1,2,3 and root 4; external vertices 5 and 6
    D=[[ZERO for _ in range(3)] for _ in range(3)]
    C=[[ZERO for _ in range(2)] for _ in range(3)]
    M=[[ZERO for _ in range(2)] for _ in range(2)]
    for a,b in edges:
        if a<=4 and b>=5:
            j=b-5
            M[j][j]+=1
            if a!=4:
                D[a-1][a-1]+=1
                C[a-1][j]+=1
        elif a==5 and b==6:
            M[0][0]+=1;M[1][1]+=1
            M[0][1]-=1;M[1][0]-=1
        else:
            raise ValueError((a,b))
    Minv,det=inverse2(M)
    S=sub(D,matmul(matmul(C,Minv),transp(C)))
    return D,C,M,Minv,det,S,trprod(H,S)

edges=((1,5),(2,5),(5,6),(3,6))
D,C,M,Minv,det,S,theta=energy(edges)
assert M==[[F(3),-F(1)],[-F(1),F(2)]]
assert det==5
assert Minv==[[F(2,5),F(1,5)],[F(1,5),F(3,5)]]
assert S==[[F(3,5),-F(2,5),-F(1,5)],
          [-F(2,5),F(3,5),-F(1,5)],
          [-F(1,5),-F(1,5),F(2,5)]]
assert theta==F(2,5)

# Schur complement two legal quotient orders.
# Eliminate t=x5-x4 then s=x6-x4, or s first then t.
def dotH(u):
    return sum((u[i]*H[i][j]*u[j] for i in range(3) for j in range(3)),ZERO)
ct=[C[i][0] for i in range(3)]
cs=[C[i][1] for i in range(3)]
def eliminate(first,second):
    a=M[first][first]
    b=M[first][second]
    d=M[second][second]
    c1=[C[i][first] for i in range(3)]
    c2=[C[i][second] for i in range(3)]
    d2=d-b*b/a
    effective=[c2[i]-b*c1[i]/a for i in range(3)]
    first_loss=dotH(c1)/a
    second_loss=dotH(effective)/d2
    return first_loss,second_loss,a*d2
tfirst=eliminate(0,1)
sfirst=eliminate(1,0)
assert tfirst==(F(1,2),F(3,5),F(5))
assert sfirst==(F(1,4),F(17,20),F(5))
assert trprod(H,D)-sum(tfirst[:2])==theta
assert trprod(H,D)-sum(sfirst[:2])==theta

# Quotient-integrated source jet coefficients:
# K=1/(2*pi*sqrt(5)), scalars A and B unchanged.
# K[(A-2B/5)*eps^-5 delta + B*eps^-3 L delta].
assert theta==F(2,5)
# Missing frozen-value scalar contact is (-B)*2/5*K*eps^-5.
# B=-7*sqrt(2)/(288*pi^(3/2)), so contact
# +7*sqrt(10)/(7200*pi^(5/2))*eps^-5.
assert F(7,288)*theta/F(2)==F(7,1440) # coefficient sqrt(2/5)
# On compact tests agreeing locally with y1*t and y1*s, coefficient
# is K*B*eps^-3 times 2*(H C M^-1)[0][0 or 1].
HCMinv=matmul(matmul(H,C),Minv)
assert HCMinv[0]==[F(7,20),F(3,10)]
assert 2*HCMinv[0][0]==F(7,10)
assert 2*HCMinv[0][1]==F(3,5)
assert 2*H[0][0]==1  # y1^2 probe yields K*B*eps^-3

# Exhaustive hostile controls: all 2^9 simple-edge attachment schemes
# with two external vertices, each externally connected component anchored.
possible=[(i,j) for i in (1,2,3,4) for j in (5,6)]+[(5,6)]
tested=zero_cases=positive_cases=0
for flags in product((0,1),repeat=len(possible)):
    ee=tuple(e for e,x in zip(possible,flags) if x)
    linked=(5,6) in ee
    if linked:
        anchored=any(a<=4 for a,b in ee)
        comp=[{a for a,b in ee if a<=4}]
        if not anchored:continue
    else:
        comp=[{a for a,b in ee if b==k} for k in (5,6)]
        if not all(comp):continue
    D,C,M,Minv,det,S,th=energy(ee)
    expected_zero=all(len(c)==1 for c in comp)
    assert (th==0)==expected_zero,(ee,th,comp)
    assert th>=0
    assert all(S[i][i]>=0 for i in range(3))
    tested+=1
    if th==0:zero_cases+=1
    else:positive_cases+=1
assert tested>250 and zero_cases>0 and positive_cases>0

print("PASS: graph with K4 + four external edges has quotient determinant 5 and contact theta=2/5")
print("PASS: t-first losses (1/2,3/5) and s-first losses (1/4,17/20) agree")
print("PASS: missing contact +7*sqrt(10)/(7200*pi^(5/2))*eps^-5 delta")
print("PASS: mixed probes y1*t and y1*s give distinct 7/10 and 3/5 B*K coefficients")
print(f"PASS: {tested} external-network patterns ({zero_cases} zero, {positive_cases} positive) meet the sharp zero-contact criterion")
