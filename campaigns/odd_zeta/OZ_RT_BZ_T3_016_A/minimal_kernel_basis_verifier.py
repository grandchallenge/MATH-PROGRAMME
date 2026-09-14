from __future__ import annotations

import hashlib
from collections import defaultdict
from math import comb

import numpy as np

P = 4194301
DIM = 576
E1_COLUMNS = 1624
R_MONS = tuple((a, b) for a in range(1, 29) for b in range(29))
S_MONS = tuple((a, b) for a in range(29) for b in range(1, 29))
R_INDEX = {m: i for i, m in enumerate(R_MONS)}
S_INDEX = {m: len(R_MONS) + i for i, m in enumerate(S_MONS)}
PIVOTS = tuple((21, 20 - j) for j in range(8))
PIVOT_COLUMNS = tuple(a * 24 + b for a, b in PIVOTS)
EXPECTED_LEADING_SHA256 = "90dfe904b4c5150793607c12f1a829f35090e540a287b9dddbb3102ee390a142"
EXPECTED_FIBER_SHA256 = {
    0: "cd400bf88ab15c023df273d72bff5b7e1e979c421e29cdf70c7c50a77c222552",
    -1: "1314f0db35b0b909deddfb08116fff58ef772397eb37b560028e3b8516e72c24",
    -2: "0f00fe339faa2d9da62018ae70bd7396422ea80fb0f4901b1dcb57c0502270fc",
    -3: "54fc0579a2aba25a3ce8c68d225d778f0ddfb7cbe9b1603fd6308e2c4a1dd5e6",
    -4: "f047477838ef5d6a21de77df19fe776c5e344a68d7d7a3ec7101338b0d1eae01",
    -5: "5baf2519947cc3b92f5be04d3c36de6204b97ccfb6d9aff4db0777fee72749c4",
    -6: "1282acf87904cdfb159e479251171a5d9ff107a8bcb2ce9bbbe7e128260adf0a",
    -7: "b60522e738d2a8d082787e504fe57e5f4ab2c67a46ad494e44185a0706d9ef04",
}


def _clean(d):
    return {k: int(v) for k, v in d.items() if v}


def _mul2(a, b):
    out = defaultdict(int)
    for (i, j), x in a.items():
        for (u, v), y in b.items():
            out[(i + u, j + v)] += x * y
    return _clean(out)


def _shift(poly, direction):
    out = defaultdict(int)
    for (a, b), value in poly.items():
        degree = b if direction == "l" else a
        for t in range(degree + 1):
            key = (a, t) if direction == "l" else (t, b)
            out[key] += value * comb(degree, t)
    return _clean(out)


def _root_poly(roots):
    out = [1]
    for root in roots:
        nxt = [0] * (len(out) + 1)
        for i, c in enumerate(out):
            nxt[i] -= root * c
            nxt[i + 1] += c
        out = nxt
    return out


def _kernel_potential(j):
    orders = defaultdict(int)
    orders[0] += 2
    orders[-1] += 1
    orders[j - 7] += 1
    orders[7 - j] -= 2
    orders[j - 1] -= 2
    cur = 0
    roots = []
    for point in range(min(orders) - 2, max(orders) + 3):
        if cur < 0:
            raise AssertionError("invalid vertical divisor")
        roots.extend([point] * cur)
        cur += orders[point]
    if cur:
        raise AssertionError("vertical divisor does not terminate")
    u = _root_poly(roots)
    v = _root_poly([-s for s in range(-j + 1, 2)])
    uk = {(a, 0): c for a, c in enumerate(u) if c}
    ul = {(0, b): c for b, c in enumerate(u) if c}
    diagonal = defaultdict(int)
    for degree, c in enumerate(v):
        for a in range(degree + 1):
            diagonal[(a, degree - a)] += c * comb(degree, a)
    return _mul2(_mul2(uk, ul), _clean(diagonal))


def _mul3(a, b):
    out = defaultdict(int)
    for (an, ak, al), x in a.items():
        for (bn, bk, bl), y in b.items():
            out[(an + bn, ak + bk, al + bl)] += x * y
    return _clean(out)


def _add3(a, b, sign=1):
    out = dict(a)
    for key, value in b.items():
        new = out.get(key, 0) + sign * value
        if new:
            out[key] = new
        elif key in out:
            del out[key]
    return out


def _linear(c=0, n=0, k=0, l=0):
    out = {}
    if c:
        out[(0, 0, 0)] = c
    if n:
        out[(1, 0, 0)] = n
    if k:
        out[(0, 1, 0)] = k
    if l:
        out[(0, 0, 1)] = l
    return out


def _power(poly, exponent):
    out = {(0, 0, 0): 1}
    for _ in range(exponent):
        out = _mul3(out, poly)
    return out


def _embed(poly):
    return {(0, a, b): c for (a, b), c in poly.items()}


def _curl(poly):
    h = _embed(poly)
    hl = _embed(_shift(poly, "l"))
    hk = _embed(_shift(poly, "k"))
    nr = _mul3(
        _mul3(_power(_linear(k=1), 2), _mul3(_linear(c=1, k=1), _linear(c=7, n=1, k=1))),
        _add3(
            _mul3(
                _mul3(_power(_linear(c=7, n=1, l=-1), 2), _power(_linear(c=1, n=1, l=1), 2)),
                _mul3(_linear(c=1, n=1, k=1, l=1), hl),
            ),
            _mul3(
                _mul3(_power(_linear(l=1), 2), _linear(c=1, l=1)),
                _mul3(_linear(c=2, k=1, l=1), _mul3(_linear(c=7, n=1, l=1), h)),
            ),
            sign=-1,
        ),
    )
    ns = _mul3(
        _mul3(_power(_linear(l=1), 2), _mul3(_linear(c=1, l=1), _linear(c=7, n=1, l=1))),
        _add3(
            _mul3(
                _mul3(_power(_linear(k=1), 2), _linear(c=1, k=1)),
                _mul3(_linear(c=2, k=1, l=1), _mul3(_linear(c=7, n=1, k=1), h)),
            ),
            _mul3(
                _mul3(_power(_linear(c=7, n=1, k=-1), 2), _power(_linear(c=1, n=1, k=1), 2)),
                _mul3(_linear(c=1, n=1, k=1, l=1), hk),
            ),
            sign=-1,
        ),
    )
    return nr, ns


def _eval(poly, n_value):
    out = defaultdict(int)
    nv = n_value % P
    for (dn, dk, dl), c in poly.items():
        out[(dk, dl)] = (out[(dk, dl)] + (c % P) * pow(nv, dn, P)) % P
    return _clean(out)


def _derivative_eval(poly, n_value):
    out = defaultdict(int)
    nv = n_value % P
    for (dn, dk, dl), c in poly.items():
        if dn:
            out[(dk, dl)] = (out[(dk, dl)] + (c * dn % P) * pow(nv, dn - 1, P)) % P
    return _clean(out)


def _leading(poly, degree):
    return {(dk, dl): c % P for (dn, dk, dl), c in poly.items() if dn == degree and c % P}


def _pair_vector(r, s):
    out = np.zeros(E1_COLUMNS, dtype=np.int64)
    for monomial, value in r.items():
        out[R_INDEX[monomial]] = value % P
    for monomial, value in s.items():
        out[S_INDEX[monomial]] = value % P
    return out


def _rank(matrix):
    a = np.asarray(matrix, dtype=np.int64).copy() % P
    rank = 0
    for column in range(a.shape[1]):
        nz = np.flatnonzero(a[rank:, column])
        if nz.size == 0:
            continue
        pivot = rank + int(nz[0])
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        a[rank, column:] = a[rank, column:] * pow(int(a[rank, column]), P - 2, P) % P
        targets = np.flatnonzero(a[rank + 1 :, column]) + rank + 1
        if targets.size:
            f = a[targets, column].copy()
            a[targets, column:] = (a[targets, column:] - f[:, None] * a[rank, column:]) % P
        rank += 1
        if rank == a.shape[1]:
            break
    return rank


def _digest(matrix):
    return hashlib.sha256(np.asarray(matrix, dtype="<i8", order="C").tobytes(order="C")).hexdigest()


def _potential_pivot_matrix(potentials):
    return [[potentials[column].get(PIVOTS[row], 0) for column in range(8)] for row in range(8)]


def _det8(matrix):
    a = [row[:] for row in matrix]
    det = 1
    for c in range(8):
        pivot = next((r for r in range(c, 8) if a[r][c]), None)
        if pivot is None:
            return 0
        if pivot != c:
            a[c], a[pivot] = a[pivot], a[c]
            det = -det
        pv = a[c][c]
        det *= pv
        for r in range(c + 1, 8):
            if not a[r][c]:
                continue
            if a[r][c] % pv:
                raise AssertionError("unexpected nonintegral pivot elimination")
            q = a[r][c] // pv
            for d in range(c, 8):
                a[r][d] -= q * a[c][d]
    return det


def verify_minimal_kernel_basis():
    potentials = [_kernel_potential(j) for j in range(8)]
    pivot_matrix = _potential_pivot_matrix(potentials)
    if _det8(pivot_matrix) != 1:
        raise AssertionError("independent pivot determinant failure")

    raw = [_curl({(a, b): 1}) for a in range(24) for b in range(24)]
    exceptional_pairs = [_curl(h) for h in potentials]

    for j, pair in enumerate(exceptional_pairs):
        if _eval(pair[0], -j) or _eval(pair[1], -j):
            raise AssertionError(f"exceptional kernel vector failed at n={-j}")

    final_hashes = {}
    final_ranks = {}
    for m in range(8):
        alpha = -m
        matrix = np.zeros((E1_COLUMNS, DIM), dtype=np.int64)
        for column, pair in enumerate(raw):
            matrix[:, column] = _pair_vector(_eval(pair[0], alpha), _eval(pair[1], alpha))
        for j, column in enumerate(PIVOT_COLUMNS):
            pair = exceptional_pairs[j]
            if j == m:
                r = _derivative_eval(pair[0], alpha)
                s = _derivative_eval(pair[1], alpha)
            else:
                inverse = pow((alpha + j) % P, P - 2, P)
                r = {key: value * inverse % P for key, value in _eval(pair[0], alpha).items()}
                s = {key: value * inverse % P for key, value in _eval(pair[1], alpha).items()}
            matrix[:, column] = _pair_vector(r, s)
        rank = _rank(matrix)
        digest = _digest(matrix)
        if rank != DIM or digest != EXPECTED_FIBER_SHA256[alpha]:
            raise AssertionError(f"independent saturated fiber replay failed at n={alpha}")
        final_ranks[str(alpha)] = rank
        final_hashes[str(alpha)] = digest

    leading = np.zeros((E1_COLUMNS, DIM), dtype=np.int64)
    pivot_to_j = {column: j for j, column in enumerate(PIVOT_COLUMNS)}
    for column, pair in enumerate(raw):
        if column in pivot_to_j:
            pair = exceptional_pairs[pivot_to_j[column]]
            leading[:, column] = _pair_vector(_leading(pair[0], 6), _leading(pair[1], 6))
        else:
            leading[:, column] = _pair_vector(_leading(pair[0], 6), _leading(pair[1], 6))
    leading_rank = _rank(leading)
    leading_digest = _digest(leading)
    if leading_rank != DIM or leading_digest != EXPECTED_LEADING_SHA256:
        raise AssertionError("independent leading-column replay failed")

    return {
        "fixed_fiber_divisor_orbit_argument_replayed": True,
        "noninteger_fiber_excluded_by_integer_shift_orbit_balance": True,
        "integer_fibers_ge_1_excluded_by_negative_vertical_multiplicity": True,
        "integer_fibers_le_neg8_excluded_by_negative_vertical_multiplicity": True,
        "exceptional_fibers": [0, -1, -2, -3, -4, -5, -6, -7],
        "exceptional_kernel_dimension": 1,
        "pivot_matrix_determinant": 1,
        "saturated_exceptional_ranks": final_ranks,
        "saturated_exceptional_sha256": final_hashes,
        "leading_rank": leading_rank,
        "leading_sha256": leading_digest,
        "minimal_polynomial_kernel_basis": True,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_proved": False,
        "t3_refuted": False,
        "global_certificate_constructed": False,
    }
