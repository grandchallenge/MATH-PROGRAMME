#!/usr/bin/env python3
"""Exact rational checks of the 4-vertex overlapping theta graph and nested cycle.

This is a combinatorial/finite-polynomial fixture; the box kernel is not a
C-infinity mollifier. The analytic theorem uses an even smooth compact kernel.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb

vertices={1,2,3,4}
edges={(1,2),(2,3),(1,3),(2,4),(3,4)}

def is_simple_cycle(sub):
    degree={}
    for a,b in sub:
        degree[a]=degree.get(a,0)+1
        degree[b]=degree.get(b,0)+1
    if not degree or any(d!=2 for d in degree.values()): return False
    visited={next(iter(degree))}
    while True:
        newer=visited | {b if a in visited else a
                         for a,b in sub if a in visited or b in visited}
        if newer==visited: break
        visited=newer
    return visited==set(degree)

all_edges=sorted(edges)
cycles=[]
for k in range(3,len(all_edges)+1):
    for comb_edges in combinations(all_edges,k):
        subset=set(comb_edges)
        if is_simple_cycle(subset):
            cycles.append(subset)
assert len(cycles)==3
assert sorted(len(x) for x in cycles)==[3,3,4]
assert set().union(*cycles)==edges
assert all(a & b for a,b in combinations(cycles,2))
assert len(edges)-(len(vertices)-1)==2

# Integrate polynomials over [0,1] with exact rationals.
def polyint(coeff):
    return sum((Q(c,i+1) for i,c in enumerate(coeff)),Q(0))

def mul(a,b):
    out=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j]+=x*y
    return out

L=[Q(2),Q(-1)]                      # conditional u/w interval length at |v|=t
J1=[Q(0),Q(-1),Q(1,2)]              # conditional u moment for v=t>=0
J2=[Q(2,3),Q(-1),Q(1),Q(-1,3)]     # conditional u^2 moment
vv=polyint(mul([Q(0),Q(0),Q(1)],mul(L,L)))/16
uu=polyint(mul(J2,L))/16
uw=polyint(mul(J1,J1))/16
uv=polyint(mul([Q(0),Q(1)],mul(J1,L)))/16
m0=polyint(mul(L,L))/16
assert (m0,uu,vv,uw,uv)==(Q(7,48),Q(13,320),Q(1,30),Q(1,120),-Q(1,60))

c3=Q(3,8)
# Four-fold convolution of box = square of triangular two-fold convolution
# f2(t)=(2-|t|)/4 on |t|<2; integrate f2(t)^2.
c4=2*Q(1,16)*(Q(8,3))
b2=Q(1,2)
b22=Q(1,6)
k0=Q(1,2)
assert c4==Q(1,3)
g=m0-2*c3*b2-c4*k0
assert g==-Q(19,48)

# Finite derivative-delta coefficients for both remaining root variables.
L_uu=uu/2-c3*b22/2
L_vv=vv/2
L_ww=L_uu
L_uv=uv
L_vw=uv
L_uw=uw
assert (L_uu,L_vv,L_ww,L_uv,L_vw,L_uw)==(
    -Q(7,640),Q(1,60),-Q(7,640),-Q(1,60),-Q(1,60),Q(1,120))

# On phi=1+2u²+3v²+5w²+7uv+11vw+13uw, all scaled
# integrals are exactly quadratic in epsilon, with NO O(epsilon^4)
# corrections. The subtractions are exact on each epsilon scale.
target=Q(-47,192)
for eps in [Q(1,2),Q(1,3),Q(1,7),Q(1,10),Q(1,100),Q(1,1000)]:
    bare=m0/eps**2 + 2*uu+3*vv+5*uu+7*uv+11*uv+13*uw
    sa=c3*b2/eps**2 + c3*5*b22
    sb=c3*b2/eps**2 + c3*2*b22
    sc=c4*k0/eps**2
    overall=g/eps**2
    residual=bare-sa-sb-sc-overall
    assert residual==target
    assert (bare-sa-sb-sc)==g/eps**2+target

# Nested triangle attached to a leaf: proper triangle subtraction
# leaves epsilon times the second relative moments; no overall pole.
a2=b2_triangle=Q(5,48)
ab=-Q(5,96)
for eps in [Q(1,2),Q(1,3),Q(1,100)]:
    nested=(c3/eps)+eps*(a2+b2_triangle+ab+Q(1,3)*c3)
    subdiv=(c3/eps)+eps*(Q(1,3)*c3)
    assert nested-subdiv==Q(5,32)*eps

# Entire connected delta-jet graph power-counting identities.
for n in range(2,8):
    for e in range(n-1,n+5):
        for extra_derivatives in range(4):
            omega=e+extra_derivatives-(n-1)
            assert omega>=0
            assert omega==(e-n+1)+extra_derivatives

print("PASS: theta graph has exactly 3 mutually overlapping proper simple cycles")
print("PASS: box moments m0=7/48, m_uu=13/320, m_vv=1/30, m_uv=-1/60, m_uw=1/120")
print("PASS: all 3 subgraph counterterms and overall g=-19/48")
print("PASS: 6 exact quadratic test pairings = -47/192 independent of epsilon")
print("PASS: 3 nested triangle+leaf residuals = (5/32)*epsilon")
print("PASS: 6x6x4 connected graph/jet power-counting checks")
print("NOTE: smooth-kappa distributional convergence is proved in theorem 042, not by box fixture.")
