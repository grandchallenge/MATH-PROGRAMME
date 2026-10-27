"""Exact controls for the arity-two global-LCS/refined-plot obstruction."""
from fractions import Fraction as F

def wedge(v,w):return v[0]*w[1]-v[1]*w[0]
def orbit(v):
    return (v,(-v[0],-v[1]),(v[1],v[0]),(-v[1],-v[0]))

rays=[(1+F(1,2**m),F(-1)) for m in range(1,41)]
for v in rays:
    assert sum(v)>0  # every pair conormal has total sum zero
    assert all(sum(w)!=0 for w in orbit(v))
for j,v in enumerate(rays):
    for w in rays[j+1:]:
        for x in orbit(v):
            for y in orbit(w):
                assert wedge(x,y)!=0  # no cancellation at equal conic rays
assert sum((F(1),F(-1)))==0

for m in range(1,101):
    t=F(1,2**m);d=t/8
    t_next=t/2;d_next=t_next/8
    assert 0<t-d<t+d<1
    assert t_next+d_next<t-d

controls=0
for k in range(9):
    for r in range(9):
        for m in range(4*(k+r+1),4*(k+r+1)+33):
            exponent=-m*m+(m+3)*k+m*r
            assert 2*exponent<=-m*m
            controls+=1

print("PASS: 40 admissible real symmetric sign/permutation ray orbits are disjoint")
print("PASS: forbidden pair-normal boundary and 100 disjoint positive bump intervals")
print("PASS:",controls,"exact quadratic flatness exponent bounds")
print("LIMIT: finite controls do not prove bounded-sequence existence or topology")
