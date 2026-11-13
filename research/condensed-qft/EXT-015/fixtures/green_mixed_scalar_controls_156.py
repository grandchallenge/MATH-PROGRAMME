#!/usr/bin/env python3
"""EXT-015/156 exact finite controls, not microlocal/source certification.

No third-party dependencies. Only exact Fraction arithmetic is used.

1. Verify moment-normalized discrete Green and the FULL scalar commutator
   for all 242 nonzero ternary five-site inputs and 11 output points.
2. Detect failure of naive scalar/Green commutation.
3. Verify nonsingular finite Gaussian-width rational evaluation matrices.
"""
from fractions import Fraction as Q
from itertools import product

INPUT = range(-2, 3)
OUTPUT = range(-5, 6)
B0 = {-2: Q(1, 2), 2: Q(1, 2)}
B1 = {-2: Q(-1, 4), 2: Q(1, 4)}

def green(t):
    return Q(abs(t), 2)

def bump_moment(bump, degree):
    return sum((Q(y**degree)*value for y,value in bump.items()), Q(0))

def c(j, x):
    bump = B0 if j == 0 else B1
    return sum((green(x-y)*value for y,value in bump.items()), Q(0))

def moment(v, j):
    return sum((Q(y**j)*value for y,value in v.items()), Q(0))

def h(v, x):
    return (sum((green(x-y)*value for y,value in v.items()), Q(0))
            - c(0,x)*moment(v,0) - c(1,x)*moment(v,1))

def a(y):
    return Q(1) + 2*y + y*y

def commutator_rhs(v, x):
    av = {y:a(y)*w for y,w in v.items()}
    return (sum((green(x-y)*(a(y)-a(x))*value for y,value in v.items()), Q(0))
            - c(0,x)*(moment(av,0)-a(x)*moment(v,0))
            - c(1,x)*(moment(av,1)-a(x)*moment(v,1)))

def determinant(rows):
    mat = [list(row) for row in rows]
    ans = Q(1)
    n = len(mat)
    for col in range(n):
        pivot = next((r for r in range(col,n) if mat[r][col]), None)
        if pivot is None:
            return Q(0)
        if pivot != col:
            mat[col],mat[pivot] = mat[pivot],mat[col]
            ans = -ans
        val = mat[col][col]
        ans *= val
        for row in range(col+1,n):
            factor = mat[row][col]/val
            for k in range(col+1,n):
                mat[row][k] -= factor*mat[col][k]
            mat[row][col] = Q(0)
    return ans

def main():
    assert (bump_moment(B0,0),bump_moment(B0,1)) == (1,0)
    assert (bump_moment(B1,0),bump_moment(B1,1)) == (0,1)
    assert all(green(t+1)-2*green(t)+green(t-1)==(1 if t==0 else 0)
               for t in range(-9,10))
    cases = 0
    identities = 0
    for coeffs in product((-1,0,1), repeat=5):
        if all(c == 0 for c in coeffs):
            continue
        v = {k:Q(c) for k,c in zip(INPUT,coeffs)}
        av = {y:a(y)*w for y,w in v.items()}
        for x in OUTPUT:
            if abs(x)>2:
                assert h(v,x)==0 and h(av,x)==0
            assert h(av,x)-a(x)*h(v,x) == commutator_rhs(v,x)
            identities += 1
        cases += 1
    # Moment bumps at +/-2 leave a genuinely nonzero delta primitive at x=1.
    delta = {0:Q(1)}
    assert h({0:Q(0)},1)==0
    assert a(1)*h(delta,1) != 0
    assert h({0:a(0)*Q(1)},1) != a(1)*h(delta,1)
    # Gaussian rates lambda_m=m*log(2)/c^2 and sample points
    # (y_k-z0)^2=k*c^2: exp(-lambda_m*(y_k-z0)^2)=2^(-m*k).
    checked = 0
    for n in range(1,10):
        mat = [[Q(1,2**(m*k)) for m in range(1,n+1)]
               for k in range(1,n+1)]
        assert determinant(mat) != 0
        checked += 1
    print(f"PASS: {cases} exhaustive inputs; {identities} exact pairings; "
          f"{checked} Gaussian-width rank controls; noncommutation PASS")

if __name__ == "__main__":
    main()
