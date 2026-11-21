#!/usr/bin/env python3
"""Exact integer-chain audit for partial Breen-Deligne degree-three coherences.

D2 maps Z[A^3] + Z[A^2] to Z[A^2], using associativity and commutativity.
D3 maps Z[A^4] + Z[A^3] + Z[A^2] (+ Z[A] when selected) to F2,
using pentagon, hexagon, symmetry-involution (+ strict diagonal).
Smith normal form gives *integral*, not merely rational, H2 invariants.
This is finite-cyclic evidence only: it does not prove general exactness.
Requires sympy; no network or randomness.
"""
import argparse
import itertools
import json
from collections import Counter
from sympy import zeros
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ


def build(n, diagonal):
    if n < 1:
        raise ValueError("n must be positive")
    a = tuple(range(n))
    pairs = list(itertools.product(a, repeat=2))
    triples = list(itertools.product(a, repeat=3))
    quads = list(itertools.product(a, repeat=4))
    idx2 = {v: i for i, v in enumerate(pairs)}
    idx3 = {v: i for i, v in enumerate(triples)}
    m2, m3, m4 = n**2, n**3, n**4
    d1 = zeros(n, m2)
    d2 = zeros(m2, m3 + m2)
    d3 = zeros(m3 + m2, m4 + m3 + m2 + (n if diagonal else 0))
    plus = lambda x, y: (x+y) % n

    def assoc(x, y, z):
        return ((y,z,1),(plus(x,y),z,-1),(x,plus(y,z),1),(x,y,-1))

    def comm(x, y):
        return ((x,y,1),(y,x,-1))

    for j,(x,y) in enumerate(pairs):
        d1[plus(x,y),j] += 1
        d1[x,j] -= 1
        d1[y,j] -= 1
        for u,v,c in comm(x,y):
            d2[idx2[u,v],m3+j] += c
        # Symmetry-involution: [x,y]_C + [y,x]_C
        d3[m3+idx2[x,y],m4+m3+j] += 1
        d3[m3+idx2[y,x],m4+m3+j] += 1

    for j,(x,y,z) in enumerate(triples):
        for u,v,c in assoc(x,y,z):
            d2[idx2[u,v],j] += c
        # Hexagon A(x,y,z) - A(y,x,z) + A(y,z,x)
        for (aa,bb,cc),sgn in (((x,y,z),1),((y,x,z),-1),((y,z,x),1)):
            d3[idx3[aa,bb,cc],m4+j] += sgn
        # ... -C(x,y+z) + C(x,y) + C(x,z)
        for (u,v),sgn in (((x,plus(y,z)),-1),((x,y),1),((x,z),1)):
            d3[m3+idx2[u,v],m4+j] += sgn

    for j,(x,y,z,w) in enumerate(quads):
        # Five-face associativity pentagon
        for (aa,bb,cc),sgn in (
            ((y,z,w),1),
            ((plus(x,y),z,w),-1),
            ((x,plus(y,z),w),1),
            ((x,y,plus(z,w)),-1),
            ((x,y,z),1)
        ):
            d3[idx3[aa,bb,cc],j] += sgn

    if diagonal:
        for x in a:
            # Strict symmetry: C(x,x)=0 (not merely 2*C(x,x)=0)
            d3[m3+idx2[x,x],m4+m3+m2+x] += 1

    assert d1*d2 == zeros(n, m3+m2), "d1*d2 is not zero"
    assert d2*d3 == zeros(m2, d3.cols), "d2*d3 is not zero"
    return d2,d3


def audit(n, diagonal):
    d2,d3 = build(n, diagonal)
    r2 = d2.rank()
    diag = smith_normal_form(d3,domain=ZZ)
    factors = [abs(int(diag[i,i])) for i in range(min(diag.shape))
               if diag[i,i] != 0]
    torsion = {str(k):v for k,v in sorted(Counter(factors).items()) if k > 1}
    free = d2.cols - r2 - len(factors)
    if free < 0:
        raise AssertionError("negative homology rank")
    return {"cyclic_order":n,"diagonal_included":diagonal,
            "d2_shape":list(d2.shape),"d3_shape":list(d3.shape),
            "d2_rank_Q":r2,"d3_rank_Q":len(factors),
            "H2_free_rank":free,"H2_torsion":torsion,
            "chain_identity":"PASS"}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--sizes",nargs="+",type=int,default=[1,2,3])
    args=ap.parse_args()
    for n in args.sizes:
        before=audit(n,False)
        after=audit(n,True)
        if n==2:
            assert before["H2_free_rank"]==0
            assert before["H2_torsion"]=={"2":1}
            assert after["H2_free_rank"]==0
            assert after["H2_torsion"]=={}
        if n in (1,3):
            assert before["H2_free_rank"]==0
            assert before["H2_torsion"]=={}
            assert after["H2_free_rank"]==0
            assert after["H2_torsion"]=={}
        print(json.dumps({"without_diagonal":before,"with_diagonal":after},
                         sort_keys=True))


if __name__=="__main__":
    main()
