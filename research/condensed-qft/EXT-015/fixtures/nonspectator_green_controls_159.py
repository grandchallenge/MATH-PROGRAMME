#!/usr/bin/env python3
"""EXT-015/159 exact finite controls; NOT a microlocal or source-lift certificate.

All tests use Fraction arithmetic. Finite lattice Green/moment calculations
are analogues of continuous distribution identities, not analytic proofs.
Polynomial Gaussian moment checks are exact Wick identities.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial


B0 = {-2: F(1, 2), 2: F(1, 2)}
B1 = {-2: F(-1, 4), 2: F(1, 4)}
BUMPS = (B0, B1)
SITES = range(-2, 3)
OUTPUT = range(-5, 6)


def green(x):
    return F(abs(x), 2)


def moment(w, k):
    return sum((F(z**k) * value for z, value in w.items()), F(0))


def projected(w):
    m = [moment(w, j) for j in (0, 1)]
    return {
        z: w.get(z, F(0)) - sum(BUMPS[j].get(z, F(0)) * m[j] for j in (0, 1))
        for z in SITES
    }


def G(x):
    return green(x) - sum((green(x - y) * v for y, v in B0.items()), F(0))


def difference2(f, x):
    return f(x + 1) - 2 * f(x) + f(x - 1)


def gaussian_even_moment(n):
    if n % 2:
        return 0
    return factorial(n) // (2 ** (n // 2) * factorial(n // 2))


def polynomial_product(a, b):
    c = {}
    for i, va in a.items():
        for j, vb in b.items():
            c[i+j] = c.get(i+j, F(0)) + va*vb
    return c


def main():
    assert moment(B0, 0) == 1 and moment(B0, 1) == 0
    assert moment(B1, 0) == 0 and moment(B1, 1) == 1
    assert all(
        difference2(G, x) == F(x == 0) - B0.get(x, F(0))
        for x in range(-5, 6)
    )
    assert all(G(x) == 0 for x in [-8,-7,-6,-5,5,6,7,8])

    samples = 0
    pairings = 0
    nonzero_w = 0
    fy = {0: F(1), -2: F(-1, 2), 2: F(-1, 2)}
    assert moment(fy, 0) == moment(fy, 1) == 0

    for coeffs in product((-1, 0, 1), repeat=5):
        if not any(coeffs):
            continue
        w = {z: F(value) for z, value in zip(SITES, coeffs)}
        r = projected(w)
        assert moment(r, 0) == moment(r, 1) == 0
        # The labelled four affine moments vanish. Its ordinary
        # degree-zero slot average is the genuine symmetric residual input.
        for a, b in product((0, 1), repeat=2):
            assert moment(fy, a)*moment(r, b) == 0
        sym = {
            (y, z): (fy.get(y, F(0))*r[z] + r[y]*fy.get(z, F(0)))/2
            for y in SITES for z in SITES
        }
        assert all(sym[y,z] == sym[z,y] for y in SITES for z in SITES)
        for a, b in product((0, 1), repeat=2):
            assert sum((F(y**a*z**b)*sym[y,z]
                        for y in SITES for z in SITES), F(0)) == 0
        nonzero_w += bool(any(r.values()))
        for x in OUTPUT:
            hr = sum((green(x-y)*r[y] for y in SITES), F(0))
            for z in SITES:
                labelled = sum(
                    (green(x-y)*value*r[z] for y, value in fy.items()), F(0)
                )
                assert labelled == G(x)*r[z]
                symmetric = sum(
                    (green(x-y)*sym[y,z] for y in SITES), F(0)
                )
                assert symmetric == (G(x)*r[z]+hr*fy.get(z, F(0)))/2
                pairings += 2
        samples += 1

    # Polynomial Wick identity: integrate normal N(0,eps^2)
    # against rho(z)*phi(z). The coefficient of eps^(2n) is
    # (rho*phi)^(2n)(0) / (2^n n!) exactly.
    rho = {0: F(1), 1: F(2), 2: F(3)}
    gaussian_tests = 0
    for coeffs in product((-1,0,1), repeat=4):
        phi = dict(enumerate(map(F, coeffs)))
        p = polynomial_product(rho, phi)
        by_moments = {
            n: p.get(2*n, F(0))*gaussian_even_moment(2*n)
            for n in range(4)
        }
        by_taylor = {
            n: p.get(2*n, F(0))*F(factorial(2*n), 2**n*factorial(n))
            for n in range(4)
        }
        assert by_moments == by_taylor
        gaussian_tests += 1

    assert samples == 242 and pairings == 26620
    assert nonzero_w == 234 and gaussian_tests == 81
    print(
        f"PASS: {samples} finite W inputs, {pairings} exact Green pairings, "
        f"{nonzero_w} nonzero W samples, {gaussian_tests} Gaussian Wick jets"
    )


if __name__ == "__main__":
    main()
