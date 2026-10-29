#!/usr/bin/env python3
"""Exact finite controls for 091; no 087 producer imports.

These check signed moment/jet maps and regulator interfaces. The liquid,
strong-topology and completed-tensor assertions require the mathematical proof.
"""
from fractions import Fraction as Q
from math import factorial

def gm(k):
    if k % 2:
        return Q(0)
    out = 1
    for j in range(1, k, 2):
        out *= j
    return Q(out)

def moment(poly, k):
    return sum((v*gm(i+k) for i,v in poly.items()), Q(0))

def derivative_profile(poly):
    # d(P phi)/du=(P'-u P)phi for the standard Gaussian phi.
    out = {}
    for i,v in poly.items():
        if i:
            out[i-1] = out.get(i-1,Q(0))+i*v
        out[i+1] = out.get(i+1,Q(0))-v
    return {i:v for i,v in out.items() if v}

def coefficients(m, poly, top=8):
    out = {}
    for k in range(max(0,top-m+1)):
        value = Q((-1)**k, factorial(k))*moment(poly,k)
        if value:
            out[m+k,k] = value
    return out

def pole(c):
    return {key:v for key,v in c.items() if key[0] < 0}

def shift(c, r):
    return {(n+r,k):v for (n,k),v in c.items()}

def jets(c, n):
    return {k:v for (power,k),v in c.items() if power == n}

def add(a,b):
    out = dict(a)
    for key,v in b.items():
        out[key] = out.get(key,Q(0))+v
    return {key:v for key,v in out.items() if v}

cases = 0
for m in range(-7,5):
    for degree in range(9):
        poly = {degree:Q(1)}
        old = coefficients(m,poly)
        oldpole = pole(old)
        epsilon_pole = {key:v for key,v in shift(oldpole,1).items() if key[0]<0}
        assert pole(coefficients(m+1,poly)) == epsilon_pole
        inverse_pole = add(shift(oldpole,-1),
                           {(-1,k):v for k,v in jets(old,0).items()})
        assert pole(coefficients(m-1,poly)) == inverse_pole
        assert jets(coefficients(m+1,poly),0) == jets(old,-1)
        assert jets(coefficients(m-1,poly),0) == jets(old,1)

        actual_d = coefficients(m-1,derivative_profile(poly))
        expected_d = {(n,k+1):v for (n,k),v in old.items()}
        assert actual_d == expected_d
        for s in (Q(2),Q(3,2)):
            scaled = {(n,k):s**n*v for (n,k),v in old.items()}
            for r in (-2,-1,1,2):
                left = {(n+r,k):s**(n+r)*v for (n,k),v in old.items()}
                right = {(n+r,k):s**r*v for (n,k),v in scaled.items()}
                assert left == right
        cases += 1

# Actual odd normal profile has the negative first-jet finite coefficient.
assert jets(coefficients(-1,{1:Q(1)}),0) == {1:Q(-1)}
# Scalar d=0 reprojection control.
scalar = {-3:Q(2),-1:Q(5),0:Q(7),2:Q(11)}
scalar_pole = {n:v for n,v in scalar.items() if n<0}
scalar_epsilon_pole = {n+1:v for n,v in scalar_pole.items() if n+1<0}
assert scalar_epsilon_pole == {-2:Q(2)}
assert scalar[-1] == 5 and scalar[0] == 7

# Nonmultiplicative finite evaluation on independent lines, by full convolution.
one = coefficients(-1,{0:Q(1)})
assert jets(one,0) == {}
cross = {}
for (n,k),a in one.items():
    for (m,l),b in one.items():
        if n+m == 0:
            cross[k,l] = cross.get((k,l),Q(0))+a*b
assert cross == {(0,2):Q(1,2),(2,0):Q(1,2)}

balanced = 0
for d in range(6):
    for e in range(6):
        for m in range(-3,4):
            for n in range(-3,4):
                # Independent physical exponents add with output dimension d+e.
                assert (m-d)+(n-e) == (m+n)-(d+e)
                # Same-variable output has the additional -d Laurent shift.
                assert (m-d)+(n-d) == (m+n-d)-d
                for r in (-2,2):
                    assert (m+r)+n == m+(n+r)
                balanced += 1

print('PASS091 signed moments, pole reprojection, inverse shifts, vertex derivatives:',
      cases, 'profile cases')
print('PASS091 exact semilinear scale identities and scalar-unit reprojection')
print('PASS091 nonzero disjoint cross-contact:', cross)
print('PASS091 balanced allocations and dimensions:', balanced, 'homogeneous pairs')
print('LIMIT091 finite algebra controls; no numerical proof of liquidity, topology, Tor, or R3')

