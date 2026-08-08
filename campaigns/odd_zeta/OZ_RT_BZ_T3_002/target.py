#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction as Q
from functools import lru_cache
from math import comb

@lru_cache(None)
def H(m: int, r: int) -> Q:
    if m <= 0:
        return Q(0)
    return H(m - 1, r) + Q(1, m ** r)

@lru_cache(None)
def ES(x: int, r: int, m: int) -> Q:
    return sum((H(t, m) / Q(t ** r) for t in range(1, x + 1)), Q(0))

@lru_cache(None)
def U(a: int, b: int, r: int, m: int) -> Q:
    return sum((H(t + b, m) / Q(t ** r) for t in range(1, a + 1)), Q(0))

def T(n: int, k: int, l: int) -> int:
    return (comb(n + k, n) * comb(n, k) ** 2 * comb(n + l, n)
            * comb(n, l) ** 2 * comb(n + k + l, n))

def A(n: int, x: int, r: int) -> Q:
    return H(n + x, r) - H(x, r)

def B(n: int, x: int, r: int) -> Q:
    return H(n - x, r) - H(x, r)

def C(n: int, k: int, l: int, r: int) -> Q:
    return H(n + k + l, r) - H(k + l, r)

def L(n: int, k: int, l: int, x: int) -> Q:
    return -A(n, x, 1) - C(n, k, l, 1) - 2 * B(n, x, 1)

def r11(k: int, l: int) -> Q:
    return ((H(k + l, 1) - H(k, 1) - H(l, 1)) * (H(k, 2) + H(l, 2))
            - H(k, 3) - H(l, 3) + U(k, l, 1, 2) + U(l, k, 1, 2))

def r12(k: int, l: int) -> Q:
    return (-2 * (H(k, 1) + H(l, 1) - H(k + l, 1)) * H(l, 3)
            + H(k, 2) * H(k + l, 2) - H(l, 2) ** 2 / 2
            + H(k + l, 2) * H(l, 2) - Q(5, 2) * H(l, 4)
            + 2 * ES(l, 1, 3) - U(k, l, 2, 2))

def r22(k: int, l: int) -> Q:
    return (-2 * (H(k, 2) + H(l, 2)) * (H(k, 3) + H(l, 3))
            + 2 * H(k + l, 3) * (H(k, 2) + H(l, 2))
            + 2 * H(k + l, 2) * (H(k, 3) + H(l, 3))
            - 2 * H(k, 5) - 2 * H(l, 5)
            - 6 * ES(k, 1, 4) - 6 * ES(l, 1, 4)
            - 2 * ES(k, 2, 3) - 2 * ES(l, 2, 3)
            + 6 * U(k, l, 1, 4) + 6 * U(l, k, 1, 4)
            + 2 * U(k, l, 2, 3) + 2 * U(l, k, 2, 3))

def W1(n: int, k: int, l: int) -> Q:
    lk = L(n, k, l, k)
    ll = L(n, k, l, l)
    return r22(k, l) + lk * r12(k, l) + ll * r12(l, k) + (lk * ll - C(n, k, l, 2)) * r11(k, l)

def w5(n: int, k: int, l: int) -> Q:
    alpha = A(n, k, 1) - A(n, l, 1)
    beta = B(n, k, 1) - B(n, l, 1)
    psi = alpha / 2 + beta
    cc = (A(n, k, 2) + A(n, l, 2)) / 4 - alpha * psi / 2
    return H(n + k, 5) + (alpha - beta) * H(n + k, 4) / 2 + cc * H(n + k, 3)

def w5sym(n: int, k: int, l: int) -> Q:
    return (w5(n, k, l) + w5(n, l, k)) / 2

def cell(n: int, k: int, l: int) -> Q:
    return Q(T(n, k, l)) * (W1(n, k, l) + 2 * w5sym(n, k, l))

def V(n: int, k: int) -> Q:
    return sum((cell(n, k, l) for l in range(n + 1)), Q(0))

def fibre_values(n: int) -> list[Q]:
    return [V(n, k) for k in range(n + 1)]

def t3_sum(n: int) -> Q:
    return sum(fibre_values(n), Q(0))
