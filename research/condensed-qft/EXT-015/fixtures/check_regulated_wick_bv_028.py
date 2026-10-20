#!/usr/bin/env python3
"""Exact finite-mode hostile tests for EXT-015D D14/028.

These finite rational computations exercise regulated BV square-zero, the
commutator with a smooth propagator, quantum Wick conjugation, scale cocycle,
and twisted factorization. They are NOT proofs for distribution spaces.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import factorial

N = 2
P1 = ((Fraction(1), Fraction(1, 3)),
      (Fraction(1, 3), Fraction(2)))
P2 = ((Fraction(2), Fraction(1, 5)),
      (Fraction(1, 5), Fraction(3)))
ZERO = (0, 0)


def add(*xs):
    z = {}
    for x in xs:
        for key, c in x.items():
            z[key] = z.get(key, Fraction(0)) + c
            if not z[key]:
                del z[key]
    return z


def scale(a, c):
    return {k: v * c for k, v in a.items() if v * c}


def single(exponents=ZERO, mask=0, h=0):
    return {(tuple(exponents), mask, h): Fraction(1)}


def d(term):
    """d theta_i=x_i; left Grassmann derivative."""
    out = {}
    for (e, mask, h), c in term.items():
        for i in range(N):
            if not mask & (1 << i):
                continue
            sign = (-1) ** ((mask & ((1 << i) - 1)).bit_count())
            v = list(e)
            v[i] += 1
            out = add(out, {(tuple(v), mask ^ (1 << i), h): c * sign})
    return out


def B(term, P=P1):
    """Even-even contraction with symmetric P, using 1/2 diagonal."""
    out = {}
    for (e, mask, h), c in term.items():
        for i in range(N):
            if e[i] >= 2:
                v = list(e)
                v[i] -= 2
                out = add(out, {(tuple(v), mask, h):
                                c * Fraction(e[i] * (e[i] - 1), 2) * P[i][i]})
            for j in range(i + 1, N):
                if not e[i] or not e[j]:
                    continue
                v = list(e)
                v[i] -= 1
                v[j] -= 1
                out = add(out, {(tuple(v), mask, h):
                                c * e[i] * e[j] * P[i][j]})
    return out


def Delta(term, P=P1):
    """Mixed even/odd contraction; D=identity, so K=P."""
    out = {}
    for (e, mask, h), c in term.items():
        for i in range(N):
            if not e[i]:
                continue
            for j in range(N):
                if not mask & (1 << j):
                    continue
                sign = (-1) ** ((mask & ((1 << j) - 1)).bit_count())
                v = list(e)
                v[i] -= 1
                out = add(out, {(tuple(v), mask ^ (1 << j), h):
                                c * e[i] * sign * P[i][j]})
    return out


def hshift(a, n):
    return {(e, mask, h + n): c for (e, mask, h), c in a.items()}


def dq(a, P=P1):
    return add(d(a), hshift(Delta(a, P), 1))


def Wick(a, P=P1, sign=1):
    result, cur = {}, a
    for n in range(32):
        if not cur:
            break
        result = add(result, scale(hshift(cur, n), Fraction(sign**n, factorial(n))))
        cur = B(cur, P)
    else:
        raise AssertionError("Wick operator did not terminate on polynomial")
    return result


def mul(left, right):
    out = {}
    for (e, m, h), a in left.items():
        for (f, n, k), b in right.items():
            if m & n:
                continue
            crossings = sum((m >> (j + 1)).bit_count()
                            for j in range(N) if n & (1 << j))
            sign = (-1) ** crossings
            key = (tuple(u + v for u, v in zip(e, f)), m | n, h + k)
            out = add(out, {key: a * b * sign})
    return out


def submatrix(P, index):
    return tuple(tuple(P[i][j] if i == j == index else Fraction(0)
                       for j in range(N)) for i in range(N))


def twisted_product(left, right, P=P1):
    # The first algebra lives in mode 0; the second lives in mode 1.
    l = Wick(left, submatrix(P, 0), -1)
    r = Wick(right, submatrix(P, 1), -1)
    return Wick(mul(l, r), P)


def check_bv_and_wick():
    checked = 0
    for e in product(range(3), repeat=N):
        for mask in range(1 << N):
            x = single(e, mask)
            assert d(d(x)) == {}
            assert Delta(Delta(x)) == {}
            assert add(d(Delta(x)), Delta(d(x))) == {}
            assert add(B(d(x)), scale(d(B(x)), -1)) == Delta(x)
            assert add(B(Delta(x)), scale(Delta(B(x)), -1)) == {}
            assert dq(Wick(x)) == Wick(d(x))
            assert Wick(Wick(x), sign=-1) == x
            assert Wick(Wick(x, P1), P2, sign=-1) == Wick(
                x,
                tuple(tuple(P1[i][j] - P2[i][j] for j in range(N))
                      for i in range(N)),
            )
            checked += 1
    print(f"BV_COMMUTATOR_WICK_SCALE_PASS basis={checked}")


def check_locality_and_twisted_factorization():
    # On disjoint modes, classical generator differentials remain local.
    # Nonzero off-diagonal K fails plain multiplication, but Wick twisting
    # restores the chain-map identity including those cross contractions.
    a = single((1, 0), 0)
    b = single((0, 0), 2)
    classical = mul(a, b)
    quantum_error = add(dq(classical),
                        scale(mul(dq(a), b), -1),
                        scale(mul(a, dq(b)), -1))
    assert quantum_error == {(ZERO, 0, 1): Fraction(1, 3)}

    checked = 0
    for e0, e1, m0, m1 in product(range(3), range(3), range(2), range(2)):
        l = single((e0, 0), m0)
        r = single((0, e1), m1 << 1)
        degree_l = -(m0.bit_count())
        sign = (-1) ** degree_l
        lhs = dq(twisted_product(l, r))
        rhs = add(twisted_product(dq(l), r),
                  scale(twisted_product(l, dq(r)), sign))
        assert lhs == rhs, (e0, e1, m0, m1, lhs, rhs)
        checked += 1
    print(f"LOCALITY_NO_GO_AND_TWISTED_FACTOR_PASS products={checked}")


if __name__ == "__main__":
    check_bv_and_wick()
    check_locality_and_twisted_factorization()
    print("EXT-015D-028 EXACT FINITE REGRESSIONS PASS (not infinite proofs)")
