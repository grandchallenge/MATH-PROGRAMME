#!/usr/bin/env python3
"""Exact rational finite controls for D21/030; not a wavefront theorem."""
from fractions import Fraction as Q

# f=x^3(1-x)^3 and h=f'', supported formally on [0,1].
f = {3: Q(1), 4: Q(-3), 5: Q(3), 6: Q(-1)}
h = {i-2: c*i*(i-1) for i, c in f.items() if i >= 2}

def monomial_pair_int(a, b):
    """Integral over 0<x<y<1 of x^a y^b (y-x) dx dy."""
    return Q(1, (a+1)*(a+2)*(a+b+3))

def delta(p,q):
    return sum((a*b*Q(1,i+j+1) for i,a in p.items() for j,b in q.items()), Q(0))

def B0(p,q):
    return sum((a*b*(monomial_pair_int(i,j)+monomial_pair_int(j,i))/2
                for i,a in p.items() for j,b in q.items()),Q(0))

assert delta(f,f) == Q(1,12012)
assert B0(f,f) == Q(1,205920)
assert B0(f,h) == delta(f,f)

# (1,-1,-1,1) is not conormal to any single pair, but is conormal
# to the simultaneous collision partition {{0,1},{2,3}}.
xi = (1,-1,-1,1)
assert sum(z != 0 for z in xi) == 4
assert sum(xi[i] for i in (0,1)) == 0
assert sum(xi[i] for i in (2,3)) == 0
assert xi != (0,0,0,0)

print("PASS: delta = 1/12012; B0 = 1/205920; B0(f,f'') = delta")
print("PASS: pairwise transversality is not simultaneous-partition transversality")
