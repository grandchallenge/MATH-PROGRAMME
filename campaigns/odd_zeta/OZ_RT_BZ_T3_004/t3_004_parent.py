from __future__ import annotations
from fractions import Fraction as Q
from functools import lru_cache
from math import comb, factorial

@lru_cache(None)
def H(m: int, r: int) -> Q:
    if m <= 0:
        return Q(0)
    return H(m - 1, r) + Q(1, m ** r)

def pochhammer(length: int, offset: int, eta: Q) -> Q:
    if length < 0 or offset < 0:
        raise ValueError("invalid normalized-Pochhammer indices")
    out = Q(1)
    for i in range(1, length + 1):
        out *= (Q(offset + i, 1) + eta) / Q(offset + i, 1)
    return out

def cumulant(length: int, offset: int, order: int) -> Q:
    if order < 1:
        raise ValueError("cumulant order must be positive")
    return Q((-1) ** (order - 1) * factorial(order - 1), 1) * (
        H(offset + length, order) - H(offset, order)
    )

def letter_from_cumulant(value: Q, order: int) -> Q:
    return Q((-1) ** (order - 1), factorial(order - 1)) * value

def T(n: int, k: int, l: int) -> int:
    return (
        comb(n + k, n) * comb(n, k) ** 2
        * comb(n + l, n) * comb(n, l) ** 2
        * comb(n + k + l, n)
    )

def rk(n: int, k: int, l: int) -> Q:
    return Q((n + k + 1) * (n - k) ** 2 * (n + k + l + 1),
             (k + 1) ** 3 * (k + l + 1))

def rl(n: int, k: int, l: int) -> Q:
    return Q((n + l + 1) * (n - l) ** 2 * (n + k + l + 1),
             (l + 1) ** 3 * (k + l + 1))

def parent(kind: str, r: int, n: int, k: int, l: int, t: int, eta: Q) -> Q:
    if kind not in {"U", "ES"} or r not in {1, 2} or t < 1:
        raise ValueError("invalid auxiliary parent")
    length = t + l if kind == "U" else t
    return Q(T(n, k, l), t ** r) * pochhammer(length, 0, eta)

def ratio_k(kind: str, r: int, n: int, k: int, l: int, t: int, eta: Q) -> Q:
    return rk(n, k, l)

def ratio_l(kind: str, r: int, n: int, k: int, l: int, t: int, eta: Q) -> Q:
    base = rl(n, k, l)
    if kind == "U":
        return base * (Q(t + l + 1, 1) + eta) / Q(t + l + 1, 1)
    return base

def ratio_t(kind: str, r: int, n: int, k: int, l: int, t: int, eta: Q) -> Q:
    base = Q(t ** r, (t + 1) ** r)
    shift = t + l + 1 if kind == "U" else t + 1
    return base * (Q(shift, 1) + eta) / Q(shift, 1)

def ql_denominator(kind: str, n: int, k: int, l: int, t: int) -> int:
    base = (l + 1) ** 3 * (k + l + 1)
    return base * (t + l + 1) if kind == "U" else base

def qt_denominator(kind: str, r: int, l: int, t: int) -> int:
    base = (t + 1) ** r
    return base * (t + l + 1) if kind == "U" else base

def ql_boundary(n: int, l: int) -> int:
    return l * (n + 1 - l)

def qt_boundary(k: int, t: int) -> int:
    return (t - 1) * (k + 1 - t)

def U_from_cumulants(k: int, l: int, r: int, m: int) -> Q:
    return sum(
        (letter_from_cumulant(cumulant(t + l, 0, m), m) / Q(t ** r)
         for t in range(1, k + 1)),
        Q(0),
    )

def ES_from_cumulants(k: int, r: int, m: int) -> Q:
    return sum(
        (letter_from_cumulant(cumulant(t, 0, m), m) / Q(t ** r)
         for t in range(1, k + 1)),
        Q(0),
    )

def direct_U(k: int, l: int, r: int, m: int) -> Q:
    return sum((H(t + l, m) / Q(t ** r) for t in range(1, k + 1)), Q(0))

def direct_ES(k: int, r: int, m: int) -> Q:
    return sum((H(t, m) / Q(t ** r) for t in range(1, k + 1)), Q(0))

def verify_nested_lift() -> int:
    checks = 0
    for k in range(1, 6):
        for l in range(0, 6):
            for r in (1, 2):
                for m in (2, 3, 4):
                    if U_from_cumulants(k, l, r, m) != direct_U(k, l, r, m):
                        raise AssertionError("U cumulant lift drift")
                    if ES_from_cumulants(k, r, m) != direct_ES(k, r, m):
                        raise AssertionError("ES cumulant lift drift")
                    checks += 2
    return checks

def verify_shift_ratios() -> int:
    checks = 0
    etas = (Q(0), Q(1, 2), Q(1))
    for kind in ("U", "ES"):
        for r in (1, 2):
            for eta in etas:
                for n in range(4, 7):
                    for k in range(2, n - 1):
                        for l in range(1, n):
                            for t in range(1, k + 1):
                                g = parent(kind, r, n, k, l, t, eta)
                                if parent(kind, r, n, k + 1, l, t, eta) / g != ratio_k(kind, r, n, k, l, t, eta):
                                    raise AssertionError("k-shift ratio drift")
                                if parent(kind, r, n, k, l + 1, t, eta) / g != ratio_l(kind, r, n, k, l, t, eta):
                                    raise AssertionError("l-shift ratio drift")
                                if parent(kind, r, n, k, l, t + 1, eta) / g != ratio_t(kind, r, n, k, l, t, eta):
                                    raise AssertionError("t-shift ratio drift")
                                checks += 3
    return checks
