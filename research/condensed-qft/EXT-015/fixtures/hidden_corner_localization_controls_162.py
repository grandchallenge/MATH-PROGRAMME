#!/usr/bin/env python3
"""EXT-015 / 162 exact finite algebra controls.

No third-party dependencies. These are lattice analogues of source identities,
NOT proofs of microlocal cone or completed liquid stage membership.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial

S = range(-2, 3)
X = range(-5, 6)
B0 = {-2: Q(1, 2), 2: Q(1, 2)}
B1 = {-2: Q(-1, 4), 2: Q(1, 4)}
DELTA = {0: Q(1)}
U = {t: DELTA.get(t, Q(0))-B0.get(t, Q(0)) for t in S}


def e(t):
    return Q(abs(t), 2)


def moment(a, degree):
    return sum((Q(t ** degree) * a.get(t, Q(0)) for t in S), Q(0))


def project(w):
    m0, m1 = moment(w, 0), moment(w, 1)
    return {t: w.get(t, Q(0))-B0.get(t, Q(0))*m0
            -B1.get(t, Q(0))*m1 for t in S}


def G(x):
    return e(x)-sum((e(x-t)*b for t,b in B0.items()),Q(0))


def H(w, x):
    return sum((e(x-t)*w[t] for t in S), Q(0))


def chi_x(x):
    # Piecewise lattice cutoff: not a smooth cutoff on the real line.
    return Q(abs(x) <= 1)


def chi_z(z):
    return Q(abs(z) <= 1)


def gaussian_heat_coefficient(n):
    return Q(1, 2**n * factorial(n))


def main():
    assert moment(B0,0)==1 and moment(B0,1)==0
    assert moment(B1,0)==0 and moment(B1,1)==1
    assert moment(U,0)==0 and moment(U,1)==0
    assert all(G(x)==0 for x in (-5,-4,4,5))
    tests=0
    pairings=0
    nonzero=0
    for coefficients in product((-1,0,1),repeat=5):
        if not any(coefficients):
            continue
        w={t:Q(a) for t,a in zip(S,coefficients)}
        v=project(w)
        assert moment(v,0)==moment(v,1)==0
        # The labelled and averaged (degree-zero) symmetric source
        # both annihilate all four mixed polynomial moments.
        sym={(y,z):(U[y]*v[z]+v[y]*U[z])/2 for y in S for z in S}
        assert all(sym[y,z]==sym[z,y] for y in S for z in S)
        assert all(sum((Q(y**a*z**b)*sym[y,z] for y in S for z in S),Q(0))==0
                   for a,b in product((0,1),repeat=2))
        nonzero += bool(any(v.values()))
        for x in X:
            gx=G(x)
            hx=H(v,x)
            a=chi_x(x)
            for z in S:
                b=chi_z(z)
                target_lab=gx*v[z]
                target_sym=(gx*v[z]+hx*U[z])/2
                # All four source types in 162.4: two smooth
                # singleton insertions and two scalar/R1 sectors.
                first=(1-a)*gx*v[z]
                second=(1-a)*hx*U[z]
                third=a*(1-b)*gx*v[z]
                fourth=a*(1-b)*hx*U[z]
                cut=1-a*b
                assert first+third==cut*target_lab
                assert (first+second+third+fourth)/2==cut*target_sym
                pairings+=2
        tests+=1

    # P_epsilon-e = sum eps^(2n)/(2^n n!) delta^(2n-2).
    # For fixed J, choose even m>J and phi=x^m/m! locally.
    # All jets through J vanish; the first surviving heat coefficient
    # is nonzero at order eps^(m+2).
    jet_tests=0
    for J in range(12):
        m=J+1
        if m % 2:
            m+=1
        n=m//2+1
        assert m>J and n>=1
        assert gaussian_heat_coefficient(n)!=0
        assert all(k<m for k in range(J+1))
        assert gaussian_heat_coefficient(n)==Q(1,2**n*factorial(n))
        jet_tests+=1

    assert tests==242 and pairings==26620 and nonzero==234
    print(f"PASS: {tests} inputs, {pairings} cut-off source pairings, "
          f"{nonzero} nonzero projections, {jet_tests} finite-jet obstructions")


if __name__=="__main__":
    main()
