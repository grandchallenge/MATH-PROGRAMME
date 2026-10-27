#!/usr/bin/env python3
"""Exact R2/061 filtered normal-jet insertion and quotient collision controls.

Standard library, rational arithmetic only. Radical factors Abar,Bbar are
carried as exact formal basis coordinates (1,sqrt(2),sqrt(3)), with common
pi^-2 extracted after the two-spoke quotient integration.
"""
from fractions import Fraction as F
from itertools import permutations, product

QINV=((F(1,2), F(1,4), F(1,4)),
      (F(1,4), F(1,2), F(1,4)),
      (F(1,4), F(1,4), F(1,2)))
A=(F(-3,4),F(5,48),F(1))
B=(F(0),-F(7,288),F(0))

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def scale(a,k):return tuple(x*F(k) for x in a)
def tr(q,m):
    return sum((q[i][j]*m[j][i] for i in range(len(q))
                for j in range(len(q))),F(0))
def effective(a,b):
    # relative source coordinates: y4=0, e4 is the zero vector
    d=[F(int(a==i)-int(b==i)) for i in (1,2,3)]
    return sum((d[i]*QINV[i][j]*d[j] for i in range(3)
                for j in range(3)),F(0))

for i in range(1,5):
    for j in range(i+1,5):
        assert effective(i,j)==F(1,2)

# For arbitrary edge multiplicities n1,...,n4 from K4 to one vertex 5,
# integrate the external coordinate t exactly. The effective quadratic
# form on internal source coordinates is
# S = diag(n1,n2,n3)-n*n^T/k, k=sum(n).
count=0
for n in product(range(5),repeat=4):
    k=sum(n)
    if not 1<=k<=6:continue
    m=[[F((n[i] if i==j else 0))-F(n[i]*n[j],k)
        for j in range(3)] for i in range(3)]
    t=tr(QINV,m)
    pair=sum((F(n[i]*n[j]) for i in range(4) for j in range(i+1,4)),F(0))
    assert t==pair/F(2*k),(n,t,pair)
    assert (t==0)==(sum(v>0 for v in n)==1)
    assert t>=0
    count+=1
assert count>100
def quotient_contact(n):
    k=sum(n)
    pairs=sum(n[i]*n[j] for i in range(4) for j in range(i+1,4))
    return F(pairs,2*k)
assert quotient_contact((2,0,0,0))==0
assert quotient_contact((1,1,0,0))==F(1,4)
assert quotient_contact((1,1,1,0))==F(1,2)
assert quotient_contact((2,1,0,0))==F(1,3)
assert quotient_contact((1,0,0,1))==F(1,4)

# Jet coefficients carry a polynomial in s=t/epsilon represented exactly
# by a dict {degree:Fraction}. Each f_j has a common non-polynomial factor
# kappa_epsilon(-t), kept out of the normalized jet.
def padd(p,q):
    out=dict(p)
    for n,v in q.items():out[n]=out.get(n,F(0))+v
    return {n:v for n,v in out.items() if v}
def pmul(p,q):
    out={}
    for i,a in p.items():
        for j,b in q.items():out[i+j]=out.get(i+j,F(0))+a*b
    return {n:v for n,v in out.items() if v}
def pscale(p,c):return {n:v*F(c) for n,v in p.items() if v*c}
Z={}
ONE={0:F(1)}
S={1:F(1)}
S2={2:F(1)}
def single(vertex):
    v=[S if i==vertex else Z for i in (1,2,3)]
    h=[[pscale(padd(S2,{0:-F(1)}),F(i==j==vertex))
        for j in (1,2,3)] for i in (1,2,3)]
    return (v,h)
def jprod(f,g):
    v,h=f;w,z=g
    return (
       [padd(v[i],w[i]) for i in range(3)],
       [[padd(padd(h[i][j],z[i][j]),
              padd(pmul(v[i],w[j]),pmul(w[i],v[j])))
              for j in range(3)] for i in range(3)]
    )
UNIT=([Z,Z,Z],[[Z for _ in range(3)] for _ in range(3)])
def jet_for(edges):
    acc=UNIT
    for j in edges:acc=jprod(acc,single(j))
    return acc
def direct_jet(edges):
    n=[edges.count(i) for i in (1,2,3)]
    v=[pscale(S,x) for x in n]
    h=[[padd(pscale(S2,n[i]*n[j]),{0:-F(n[i])} if i==j and n[i] else Z)
         for j in range(3)] for i in range(3)]
    return v,h

for seq in ((1,2),(1,2,3),(1,2,4),(1,2,2,4),(1,1,2,3)):
    expected=direct_jet(seq)
    for order in set(permutations(seq)):
        assert jet_for(order)==expected,(seq,order)
    assert jet_for(seq)==jet_for(tuple(reversed(seq)))

def moment(n):
    if n%2:return F(0)
    answer=F(1)
    for j in range(1,n,2):answer*=F(j,2)
    return answer
def expectation(p):
    return sum((v*moment(j) for j,v in p.items()),F(0))
def contract(h):
    out=Z
    for i in range(3):
        for j in range(3):out=padd(out,pscale(h[i][j],QINV[i][j]))
    return out

# Direct test-function pairing of two external Gaussians times the
# intrinsic K4 source counterterm. For a homogeneous monomial
# y1^p y2^q y3^r t^s with degree d, the result equals
# pi^-2 epsilon^(d-4) * (c0 + c2 sqrt(2) + c3 sqrt(3)).
def monomial_probe(alpha,edges=(1,2)):
    assert tuple(edges)==(1,2)
    ys=alpha[:3]
    tpow=alpha[3]
    ydeg=sum(ys)
    v,h=jet_for(edges)
    base={tpow:F(1)}
    zeroth=base if ydeg==0 else Z
    gradient=[base if ydeg==1 and ys[i]==1 else Z for i in range(3)]
    second=[[pscale(base,2) if i==j and ydeg==2 and ys[i]==2
             else base if i!=j and ydeg==2 and ys[i]==ys[j]==1
             else Z for j in range(3)] for i in range(3)]
    coefficient=pmul(contract(h),zeroth)
    for i in range(3):
        for j in range(3):
            coefficient=padd(coefficient,pscale(pmul(v[i],gradient[j]),2*QINV[i][j]))
    coefficient=padd(coefficient,contract(second))
    av=expectation(zeroth)
    bv=expectation(coefficient)
    # Integral of the two equal-center edges:
    # I0(epsilon)=1/(2 sqrt(pi) epsilon); common pi^-2 /2.
    result=scale(add(scale(A,av),scale(B,bv)),F(1,2))
    return result,sum(alpha)-4

a0,degree=monomial_probe((0,0,0,0))
assert degree==-4
assert a0==scale(add(A,scale(B,-F(1,4))),F(1,2))
assert a0==(F(-3,8),F(127,2304),F(1,2))
# The quotient-integrated missing contact is -B/(8 sqrt(pi)):
assert scale(B,-F(1,8))==(F(0),F(7,2304),F(0))
assert monomial_probe((0,0,0,2))==(scale(add(scale(A,F(1,2)),scale(B,F(5,8))),F(1,2)),-2)
assert monomial_probe((1,0,0,1))==(scale(B,F(3,8)),-2)
assert monomial_probe((0,1,0,1))==(scale(B,F(3,8)),-2)
assert monomial_probe((0,0,1,1))==(scale(B,F(1,4)),-2)
assert monomial_probe((2,0,0,0))==(scale(B,F(1,2)),-2)
assert monomial_probe((1,1,0,0))==(scale(B,F(1,4)),-2)
assert monomial_probe((1,0,0,1))==monomial_probe((0,1,0,1))
assert monomial_probe((0,0,0,4))==(scale(add(scale(A,F(3,4)),scale(B,F(33,16))),F(1,2)),0)

# A quotient-value-only rule has no y-gradient action. In particular,
# it predicts zero on y1*t and fails on the constant by this nonzero amount.
assert monomial_probe((1,0,0,1))[0]!= (F(0),)*3
assert scale(B,-F(1,8))!=(F(0),)*3

print("PASS: arbitrary attachment multiplicities (",count,") satisfy exact positive quotient energy")
print("PASS: contact is zero iff all external edges attach at one source vertex")
print("PASS: K4 multi-edge jets compose in every tested insertion order, including branching attachments")
print("PASS: two-spoke quotient contact +7*sqrt(2)/(2304*pi^2)*epsilon^-4 delta")
print("PASS: constant, t^2, y1*t, y3*t, y1^2, y1*y2 and t^4 polynomial probes")
print("PASS: positive-regulator source-jet action differs from frozen-complement insertion")
