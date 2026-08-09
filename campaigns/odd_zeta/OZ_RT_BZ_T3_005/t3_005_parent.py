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
        out *= (Q(offset + i) + eta) / Q(offset + i)
    return out

def cumulant(length: int, offset: int, order: int) -> Q:
    if order < 1:
        raise ValueError("cumulant order must be positive")
    return Q((-1) ** (order - 1) * factorial(order - 1)) * (
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
    return Q(
        (n + k + 1) * (n - k) ** 2 * (n + k + l + 1),
        (k + 1) ** 3 * (k + l + 1),
    )

def rl(n: int, k: int, l: int) -> Q:
    return Q(
        (n + l + 1) * (n - l) ** 2 * (n + k + l + 1),
        (l + 1) ** 3 * (k + l + 1),
    )

# Stage A: mirror orientation. External recurrence shift is l; finite divergence
# directions are k and s with 1 <= s <= l.
def mirror_parent(kind: str, r: int, n: int, k: int, l: int, s: int, eta: Q) -> Q:
    if kind not in {"U", "ES"} or r not in {1, 2} or s < 1:
        raise ValueError("invalid mirror auxiliary parent")
    length = s + k if kind == "U" else s
    return Q(T(n, k, l), s ** r) * pochhammer(length, 0, eta)

def ratio_l(kind: str, r: int, n: int, k: int, l: int, s: int, eta: Q) -> Q:
    return rl(n, k, l)

def ratio_k(kind: str, r: int, n: int, k: int, l: int, s: int, eta: Q) -> Q:
    base = rk(n, k, l)
    if kind == "U":
        return base * (Q(s + k + 1) + eta) / Q(s + k + 1)
    return base

def ratio_s(kind: str, r: int, n: int, k: int, l: int, s: int, eta: Q) -> Q:
    base = Q(s ** r, (s + 1) ** r)
    shift = s + k + 1 if kind == "U" else s + 1
    return base * (Q(shift) + eta) / Q(shift)

def qk_denominator(kind: str, n: int, k: int, l: int, s: int) -> int:
    base = (k + 1) ** 3 * (k + l + 1)
    return base * (s + k + 1) if kind == "U" else base

def qs_denominator(kind: str, r: int, k: int, s: int) -> int:
    base = (s + 1) ** r
    return base * (s + k + 1) if kind == "U" else base

def qk_boundary(n: int, k: int) -> int:
    return k * (n + 1 - k)

def qs_boundary(l: int, s: int) -> int:
    return (s - 1) * (l + 1 - s)

def mirror_U_from_cumulants(l: int, k: int, r: int, m: int) -> Q:
    return sum(
        (letter_from_cumulant(cumulant(s + k, 0, m), m) / Q(s ** r)
         for s in range(1, l + 1)),
        Q(0),
    )

def mirror_ES_from_cumulants(l: int, r: int, m: int) -> Q:
    return sum(
        (letter_from_cumulant(cumulant(s, 0, m), m) / Q(s ** r)
         for s in range(1, l + 1)),
        Q(0),
    )

def direct_U_lk(l: int, k: int, r: int, m: int) -> Q:
    return sum((H(s + k, m) / Q(s ** r) for s in range(1, l + 1)), Q(0))

def direct_ES_l(l: int, r: int, m: int) -> Q:
    return sum((H(s, m) / Q(s ** r) for s in range(1, l + 1)), Q(0))

def verify_mirror_nested_lift() -> int:
    checks = 0
    for l in range(1, 6):
        for k in range(0, 6):
            for r in (1, 2):
                for m in (2, 3, 4):
                    if mirror_U_from_cumulants(l, k, r, m) != direct_U_lk(l, k, r, m):
                        raise AssertionError("mirror U cumulant lift drift")
                    if mirror_ES_from_cumulants(l, r, m) != direct_ES_l(l, r, m):
                        raise AssertionError("mirror ES cumulant lift drift")
                    checks += 2
    return checks

def verify_mirror_shift_ratios() -> int:
    checks = 0
    etas = (Q(0), Q(1, 2), Q(1))
    for kind in ("U", "ES"):
        for r in (1, 2):
            for eta in etas:
                for n in range(4, 7):
                    for l in range(2, n - 1):
                        for k in range(1, n):
                            for s in range(1, l + 1):
                                g = mirror_parent(kind, r, n, k, l, s, eta)
                                if mirror_parent(kind, r, n, k, l + 1, s, eta) / g != ratio_l(kind, r, n, k, l, s, eta):
                                    raise AssertionError("mirror l-shift ratio drift")
                                if mirror_parent(kind, r, n, k + 1, l, s, eta) / g != ratio_k(kind, r, n, k, l, s, eta):
                                    raise AssertionError("mirror k-shift ratio drift")
                                if mirror_parent(kind, r, n, k, l, s + 1, eta) / g != ratio_s(kind, r, n, k, l, s, eta):
                                    raise AssertionError("mirror s-shift ratio drift")
                                checks += 3
    return checks

# Stage B/C: raw-derivative power-sum isolator.
# P_r(length,offset;z)=prod_i [1-(-z/(offset+i))^r].
# Its r-th raw derivative at zero is (-1)^(r+1) r! times
# H_{offset+length}^{(r)}-H_offset^{(r)}. Unlike logarithmic
# cumulants, this is a linear differential extraction.
def power_sum_isolator(length: int, offset: int, order: int, z: Q) -> Q:
    if length < 0 or offset < 0 or order < 1:
        raise ValueError("invalid power-sum isolator indices")
    out = Q(1)
    sign = -((-1) ** order)
    for i in range(1, length + 1):
        d = Q(offset + i)
        out *= Q(1) + Q(sign) * (z / d) ** order
    return out

def raw_derivative_multiplier(order: int) -> int:
    return ((-1) ** (order + 1)) * factorial(order)

def interval_power_sum(length: int, offset: int, order: int) -> Q:
    return H(offset + length, order) - H(offset, order)

def isolator_rth_derivative_at_zero(length: int, offset: int, order: int) -> Q:
    return Q(raw_derivative_multiplier(order)) * interval_power_sum(length, offset, order)

def _interval_terms(atom_name: str, n: int, k: int, l: int):
    parts = atom_name.split("_")
    if atom_name.startswith("H_k_"): return int(parts[-1]), [(k, 0, 1)]
    if atom_name.startswith("H_l_"): return int(parts[-1]), [(l, 0, 1)]
    if atom_name.startswith("H_kl_"): return int(parts[-1]), [(k + l, 0, 1)]
    if atom_name.startswith("H_nk_"): return int(parts[-1]), [(n + k, 0, 1)]
    if atom_name.startswith("H_nl_"): return int(parts[-1]), [(n + l, 0, 1)]
    if atom_name.startswith("A_k_"): return int(parts[-1]), [(n, k, 1)]
    if atom_name.startswith("A_l_"): return int(parts[-1]), [(n, l, 1)]
    if atom_name.startswith("B_k_"): return int(parts[-1]), [(n - k, 0, 1), (k, 0, -1)]
    if atom_name.startswith("B_l_"): return int(parts[-1]), [(n - l, 0, 1), (l, 0, -1)]
    if atom_name.startswith("C_"): return int(parts[-1]), [(n, k + l, 1)]
    raise ValueError(f"not a one-body atom: {atom_name}")

def one_body_atom_value(atom_name: str, n: int, k: int, l: int) -> Q:
    order, terms = _interval_terms(atom_name, n, k, l)
    return sum((Q(sign) * interval_power_sum(length, offset, order)
                for length, offset, sign in terms), Q(0))

def one_body_isolator(atom_name: str, n: int, k: int, l: int, z: Q) -> Q:
    order, terms = _interval_terms(atom_name, n, k, l)
    out = Q(1)
    for length, offset, sign in terms:
        f = power_sum_isolator(length, offset, order, z)
        out = out * f if sign == 1 else out / f
    return out

def one_body_raw_derivative_at_zero(atom_name: str, n: int, k: int, l: int) -> Q:
    order, _ = _interval_terms(atom_name, n, k, l)
    return Q(raw_derivative_multiplier(order)) * one_body_atom_value(atom_name, n, k, l)

def nested_atom_parts(atom_name: str):
    p = atom_name.split("_")
    if atom_name.startswith("U_k_l_"): return "k_side", "U", int(p[-2]), int(p[-1])
    if atom_name.startswith("U_l_k_"): return "l_side", "U", int(p[-2]), int(p[-1])
    if atom_name.startswith("ES_k_"): return "k_side", "ES", int(p[-2]), int(p[-1])
    if atom_name.startswith("ES_l_"): return "l_side", "ES", int(p[-2]), int(p[-1])
    raise ValueError(f"not a nested atom: {atom_name}")

def nested_atom_value(atom_name: str, n: int, k: int, l: int) -> Q:
    orientation, kind, r, m = nested_atom_parts(atom_name)
    upper = k if orientation == "k_side" else l
    other = l if orientation == "k_side" else k
    out = Q(0)
    for u in range(1, upper + 1):
        length = u + other if kind == "U" else u
        out += interval_power_sum(length, 0, m) / Q(u ** r)
    return out

def nested_raw_derivative_sum(atom_name: str, n: int, k: int, l: int) -> Q:
    orientation, kind, r, m = nested_atom_parts(atom_name)
    upper = k if orientation == "k_side" else l
    other = l if orientation == "k_side" else k
    out = Q(0)
    for u in range(1, upper + 1):
        length = u + other if kind == "U" else u
        out += Q(T(n, k, l), u ** r) * isolator_rth_derivative_at_zero(length, 0, m)
    return out

def direct_atom_value(atom_name: str, n: int, k: int, l: int) -> Q:
    if atom_name.startswith(("U_", "ES_")):
        return nested_atom_value(atom_name, n, k, l)
    return one_body_atom_value(atom_name, n, k, l)
