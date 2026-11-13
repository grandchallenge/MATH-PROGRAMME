#!/usr/bin/env python3
"""Exact finite Green/moment regression for EXT-015 REACH/153.

This models lattice second differences, not distributional wavefronts or 150.L.
No nonstandard dependencies, networking, or high-memory computation.
"""
from fractions import Fraction
from itertools import product

Q = Fraction


def green(n: int) -> Fraction:
    return Q(abs(n), 2)


# Sum b0=1, sum n*b0=0; sum b1=0, sum n*b1=1.
B0 = {-1: Q(1, 2), 1: Q(1, 2)}
B1 = {-1: Q(-1, 2), 1: Q(1, 2)}


def moment(v: dict[int, Fraction], degree: int) -> Fraction:
    return sum((Q(n**degree) * c for n, c in v.items()), Q(0))


def corrected(v: dict[int, Fraction]) -> dict[int, Fraction]:
    m0, m1 = moment(v, 0), moment(v, 1)
    w = dict(v)
    for n in (-1, 1):
        w[n] = w.get(n, Q(0)) - m0 * B0[n] - m1 * B1[n]
    return {n: c for n, c in w.items() if c != 0}


def primitive(w: dict[int, Fraction], n: int) -> Fraction:
    return sum((green(n - j) * c for j, c in w.items()), Q(0))


def check(v: dict[int, Fraction]) -> None:
    w = corrected(v)
    assert moment(w, 0) == 0
    assert moment(w, 1) == 0
    if not w:
        return
    left, right = min(w), max(w)
    for n in range(left - 4, right + 5):
        h = primitive(w, n)
        assert (primitive(w, n + 1) - 2 * h + primitive(w, n - 1)
                == w.get(n, Q(0)))
        if n < left or n > right:
            assert h == 0, (v, n, h)


def main() -> None:
    assert moment(B0, 0) == 1 and moment(B0, 1) == 0
    assert moment(B1, 0) == 0 and moment(B1, 1) == 1
    assert all(green(n + 1) - 2 * green(n) + green(n - 1)
               == (1 if n == 0 else 0) for n in range(-20, 21))
    count = 0
    for coefficients in product((-1, 0, 1), repeat=5):
        v = {n - 2: Q(c) for n, c in enumerate(coefficients) if c}
        if v:
            check(v)
            count += 1
    assert count == 242
    print("PASS: 242 rational five-site inputs; two moments, compact support, second-difference identity")
    print("SCOPE: finite analogue only; no wavefront, PHG, derived liquid, or 150.L certification")


if __name__ == "__main__":
    main()
