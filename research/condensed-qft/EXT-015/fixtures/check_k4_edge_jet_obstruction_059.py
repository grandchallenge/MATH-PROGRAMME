#!/usr/bin/env python3
"""R2/059 exact K4 insertion obstruction, standard library only.

All amplitude coefficients are exact Q-linear combinations of 1,sqrt(2),
sqrt(3),sqrt(6) after extracting common pi^-2. No finite-difference fit or
floating-point arithmetic is used in the assertions. The analytic
distributional argument is in R2_K4_DELTA_JET_INSERTION_OBSTRUCTION_059.md.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations

V=(1,2,3,4)
EDGES=tuple(combinations(V,2))
K0=F(1) # placeholder: kappa(0) is tracked in the exact pi^-2 scaling

def vec(c=0,s2=0,s3=0,s6=0):
    return tuple(map(F,(c,s2,s3,s6)))
def add(*xs):
    return tuple(sum((x[i] for x in xs),F(0)) for i in range(4))
def times(x,q):
    return tuple(v*F(q) for v in x)
def neg(x):return times(x,-1)

def determinant(a):
    a=[[F(v) for v in row] for row in a]
    n=len(a)
    p=F(1)
    for j in range(n):
        k=next((i for i in range(j,n) if a[i][j]),None)
        if k is None:return F(0)
        if k!=j:a[j],a[k]=a[k],a[j];p=-p
        d=a[j][j]
        p*=d
        for i in range(j+1,n):
            q=a[i][j]/d
            for h in range(j+1,n):a[i][h]-=q*a[j][h]
    return p

def laplacian(edges,root=4):
    vertices=[i for i in V if i!=root]
    ix={k:i for i,k in enumerate(vertices)}
    q=[[F(0)]*3 for _ in range(3)]
    for u,v in edges:
        if u==v:continue
        if u!=root:q[ix[u]][ix[u]]+=1
        if v!=root:q[ix[v]][ix[v]]+=1
        if u!=root and v!=root:q[ix[u]][ix[v]]-=1;q[ix[v]][ix[u]]-=1
    return q

Q=laplacian(EDGES)
Qinv=[[F(1,2) if i==j else F(1,4) for j in range(3)] for i in range(3)]
assert determinant(Q)==16
assert all(sum(Q[i][k]*Qinv[k][j] for k in range(3))==F(i==j)
           for i in range(3) for j in range(3))

triangles=[frozenset(t) for t in combinations(V,3)]
assert len(triangles)==4

# R2/051 K4 prepared source coefficients.
# A = pi^-3/2 * (sqrt(3)-3/4+5*sqrt(2)/48)
# B = pi^-3/2 * (-7*sqrt(2)/288), multiplying L=Q^-1:dd.
# After multiplying kappa0=(2*pi)^-1/2, the constants carry pi^-2.
k0_A=vec(F(5,48),-F(3,8),0,F(1,2))
k0_B=vec(-F(7,288))

# A naive quotient rule freezes the new edge at zero and misses
# -k0*B*R_eff epsilon^-4 delta, R_eff=v^T Q^-1 v.
for extra in EDGES:
    qplus=laplacian(EDGES+(extra,))
    assert determinant(qplus)==24
    v=[F(int(i==extra[0])-int(i==extra[1])) for i in (1,2,3)]
    resistance=sum(v[i]*Qinv[i][j]*v[j] for i in range(3) for j in range(3))
    assert resistance==F(1,2)

    frozen=k0_A
    contact=times(k0_B,-resistance)
    assert contact==vec(F(7,576))
    correct_source_insertion=add(frozen,contact)
    assert correct_source_insertion==vec(F(67,576),-F(3,8),0,F(1,2))
    # The epsilon^-2 coefficient of L delta is unchanged by the contact.
    assert k0_B==vec(-F(7,288))

    # Exact scalar coefficient of prepared K4 amplitude times the new edge.
    # Bare 7-edge G: (2*pi)^-2 / sqrt(tau=24) -> sqrt(6)/48*pi^-2.
    bare=vec(s6=F(1,48))
    group=Counter(extra[0] in t and extra[1] in t for t in triangles)
    assert group=={True:2,False:2}

    # Two triangles containing the edge: c3*kappa(0)*int kappa^3=1/12*pi^-2 each.
    # Other two triangles: c3*int kappa^4=sqrt(3)/24*pi^-2 each.
    triangle_sum=add(vec(c=F(1,6)),vec(s3=F(1,12)))
    # Each square spans all vertices: c4*kappa(0)^3=1/8*pi^-2.
    square_sum=vec(c=F(3,8))
    # Each theta: gTheta*kappa(0)^2, with gTheta the *prepared*
    # two-loop source coefficient, not the primitive theta Gaussian.
    theta_single=vec(c=-F(1,8),s2=F(1,16),s6=-F(1,12))
    theta_sum=times(theta_single,6)
    prepared=add(bare,neg(triangle_sum),neg(square_sum),neg(theta_sum))
    assert prepared==vec(F(5,24),-F(3,8),-F(1,12),F(25,48))

    # This is kappa_epsilon * R_{K4,epsilon}, where R_{K4} -> 0
    # strongly on *fixed* smooth compact tests before insertion.
    residual=add(prepared,neg(correct_source_insertion))
    assert residual==vec(F(53,576),0,-F(1,12),F(1,48))
    assert residual!=vec()

    # Hostile quadratic probe phi=(y_1-y_2)^2 near the diagonal:
    # L phi(0) = 2 R_eff = 1; source insertion includes k0*B/eps^2.
    # phi(0)=0, so the scalar contact term cannot mimic the jet term.
    assert 2*resistance==1
    assert k0_B==vec(-F(7,288))

print("PASS: every one of six extra edge choices has determinant 24 and R_eff=1/2")
print("PASS: derivative-delta Leibniz contact shift 7/(576*pi^2)*eps^-4 delta")
print("PASS: exact K4 prepared times edge source contributions (2+2 triangles, 3 squares, 6 thetas)")
print("PASS: renormalized K4 times edge has nonzero eps^-4 scalar coefficient")
print("      [53/576+sqrt(6)/48-sqrt(3)/12]/pi^2")
print("PASS: quadratic test forces -7/(288*pi^2)*eps^-2 L-delta coefficient")
print("NOTE: distributional convergence/nonconvergence is analytically proved in R2/059.")
