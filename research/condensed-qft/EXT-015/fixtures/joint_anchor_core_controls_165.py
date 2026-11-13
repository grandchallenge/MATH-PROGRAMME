#!/usr/bin/env python3
"""EXT-015 / 165 exact finite source-equivalence and matched-partition controls.

Uses only Fraction and itertools. This is finite algebra, not certification of
all-corner asymptotics, source completion, R1 wavefronts, or full 150.L.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial

S=range(-2,3)
X=range(-7,8)
B0={-2:F(1,2),2:F(1,2)}
B1={-2:F(-1,4),2:F(1,4)}
D={0:F(1)}
U={z:D.get(z,F(0))-B0.get(z,F(0)) for z in S}

def e(x):
    return F(abs(x),2)

def moment(w,j):
    return sum((F(z**j)*v for z,v in w.items()),F(0))

def C(j,x):
    bump=(B0,B1)[j]
    return sum((e(x-y)*v for y,v in bump.items()),F(0))

def g(x):
    return e(x)-C(0,x)

def q(w,x):
    return sum((e(x-z)*v for z,v in w.items()),F(0))

def chi(x):
    return F(abs(x)<=3)

def d2(f,x):
    return f(x+1)-2*f(x)+f(x-1)

def normal_gauss_moment(n):
    return F(0) if n%2 else F(factorial(n),2**(n//2)*factorial(n//2))

def main():
    assert (moment(B0,0),moment(B0,1))==(1,0)
    assert (moment(B1,0),moment(B1,1))==(0,1)
    assert (moment(U,0),moment(U,1))==(0,0)
    assert all(g(x)==0 for x in X if abs(x)>=3)
    inputs=0
    pairings=0
    derivative_pairs=0
    nonzero=0
    for vals in product((-1,0,1),repeat=len(S)):
        if not any(vals):
            continue
        w={z:F(a) for z,a in zip(S,vals)}
        m0,m1=moment(w,0),moment(w,1)
        wc={z:w[z]-B0.get(z,F(0))*m0-B1.get(z,F(0))*m1 for z in S}
        assert moment(wc,0)==moment(wc,1)==0
        nonzero+=any(wc.values())
        for x in X:
            ex,gx,cx,c1x=e(x),g(x),C(0,x),C(1,x)
            qx=q(w,x)
            hx=q(wc,x)
            assert hx==qx-cx*m0-c1x*m1
            for z in S:
                a=chi(x)*ex*w[z]
                b=chi(x)*qx*D.get(z,F(0))
                rlab=-chi(x)*cx*wc[z]-chi(x)*ex*(B0.get(z,F(0))*m0+B1.get(z,F(0))*m1)
                rsym=(rlab-chi(x)*qx*B0.get(z,F(0))
                      -chi(x)*(cx*m0+c1x*m1)*U[z])/2
                flab=gx*wc[z]
                fsym=(gx*wc[z]+hx*U[z])/2
                assert flab==a+rlab
                assert fsym==(a+b)/2+rsym
                pairings+=2
        # Matched-partition order-zero jets reproduce both anchor arms:
        # d2(e(x)w(z))=delta_0(x)w(z), d2(Q(x)delta(z))=w(x)delta(z)
        # at the joint chart |x|<=1, where chi=1 throughout the stencil.
        for x,z in product((-1,0,1),S):
            da=d2(lambda t:chi(t)*e(t)*w[z],x)
            db=d2(lambda t:chi(t)*q(w,t)*D.get(z,F(0)),x)
            assert da==D.get(x,F(0))*w[z]
            assert db==w.get(x,F(0))*D.get(z,F(0))
            derivative_pairs+=2
        inputs+=1
    # Exact Wick-even-moment identities used in the two normal arms.
    gaussian_moments=0
    for n in range(16):
        m=normal_gauss_moment(n)
        if n%2:
            assert m==0
        else:
            k=n//2
            assert m==F(factorial(2*k),2**k*factorial(k))
        gaussian_moments+=1
    assert inputs==242 and pairings==36300 and derivative_pairs==7260
    assert nonzero==234 and gaussian_moments==16
    print(f"PASS: {inputs} core inputs, {pairings} exact two-core decompositions, "
          f"{derivative_pairs} legal matched-anchor finite-difference checks, "
          f"{nonzero} nonzero projected inputs, {gaussian_moments} Gaussian moments")

if __name__=="__main__":
    main()
