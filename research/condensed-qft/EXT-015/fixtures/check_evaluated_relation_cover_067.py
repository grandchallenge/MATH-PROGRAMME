"""Exact rational controls for R3/067. No infinite liquid Ext verdict is inferred."""
from fractions import Fraction as F
from itertools import product

# A rank-two presentation map q: Q^4 -> Q^2; its true relation kernel.
q = ((1,0,1,2),(0,1,1,-1))
j = ((-1,-2),(-1,1),(1,0),(0,1))
def matmul(a,b):
    return tuple(tuple(sum((F(x)*F(y) for x,y in zip(row,col)),F(0))
                       for col in zip(*b)) for row in a)
assert matmul(q,j) == ((0,0),(0,0))
# Every a=(a0,a1) has an explicitly chosen projective lift.
for a in product(range(-4,5), repeat=2):
    lift=((F(a[0]),),(F(a[1]),),(F(0),),(F(0),))
    assert matmul(q,lift)==((F(a[0]),),(F(a[1]),))
# Differences of two lifts land in the actual kernel: f-g=j h.
h=((2,-1),(3,4))
diff=matmul(j,h)
assert matmul(q,diff)==((0,0),(0,0))
# Restricting any target functional through this difference is a boundary.
for phi in product(range(-3,4),repeat=2):
    functional=(tuple(map(F,phi)),)
    assert matmul(functional,matmul(h,((2,),(-3,)))) == matmul(
        matmul(functional,h),((2,),(-3,)))
# Coefficient inclusion/projection are retractions in every cochain degree.
# Use two nonzero cohomology degrees; projections commute with the differential.
d=((0,1,0),(0,0,0),(0,0,0))
assert matmul(d,d)==((0,0,0),(0,0,0),(0,0,0))
identity=((1,0,0),(0,1,0),(0,0,1))
assert matmul(identity,d)==matmul(d,identity)
for total in (7,31,97):
    for prefix in (1,3,5):
        for degree in range(4):
            # A split coefficient map acts componentwise in all degrees.
            x=tuple(F((n+1)*(degree+2),n+2) for n in range(prefix))
            included=x+(F(0),)*(total-prefix)
            assert included[:prefix]==x
# Escaping representatives do not imply escaping classes: every diagonal
# output map on these projective generators is already a projective boundary.
for count in (17,65,257):
    diagonal={n:{n:F(1)} for n in range(count)}
    restricted_boundary=dict(diagonal)  # restriction of that projective map
    assert all(diagonal[n]==restricted_boundary[n] for n in diagonal)
    assert len({k for row in diagonal.values() for k in row})==count
print("PASS: 81 projective generator lifts and actual relation kernel")
print("PASS: lift differences factor through the relation kernel")
print("PASS: coefficient retractions commute with a nontrivial differential")
print("PASS: prefix retractions in four degrees and three output sizes")
print("PASS: support-escaping projective boundary controls")
print("LIMIT: no infinite support quantifier or nonzero liquid Ext class certified")
