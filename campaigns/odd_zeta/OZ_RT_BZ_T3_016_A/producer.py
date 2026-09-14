from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
ISSUE = 964
OPERATION = "OZ-RT-BZ-T3-016-A"
STAGE = "T3_016_A_ORDER7_SOURCE_PREFLIGHT"
PROTECTED_BASE = "a05c16d2988a9a0c73f9c62b482c96777a49c5ea"
PREDECESSOR_TERMINAL = "GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED"
TERMINAL = "ORDER7_E1_KERNEL_IDENTIFIED_AS_DISCRETE_CURL__POTENTIAL_SECTION_REDUCTION_REQUIRED"

SOURCE_REPOSITORY = "rain-1/-odd-zeta-values-moremath"
SOURCE_COMMIT = "6cc0bf07137815ceeef0d9f340559f85352391e5"
SOURCE_BLOBS = {
    "work/Z5CF_TELESCOPER.md": "a634b070d5d95d09749137c26bc51012f318683b",
    "work/Z5CF_LIFT.md": "f1c48b2ce0951ef4a4aefa1d449e53fe33ce5cc5",
    "work/Z5CF_LINALG.md": "637ecaa7f3ee941a87932de390eb7336d7fde677",
    "work/z5la/z5cf_order7_partial.json": "d6024c7244a4a45ac759b455f65fca6d377b735d",
    "work/z5la/a_lift.json": "564fc9637f31b870d85dab293d6cbb5cfe52bae0",
    "work/z5la/o_scan.py": "bc6e9a59a48b15eddbab8e80ad4e5063972582d2",
    "work/z5la/o_scan_E1.log": "9085d23798074e9e86bc1c41faaf17a7e4b1386f",
    "work/z5la/o_csweep.py": "b506b9d6fbd405e6ac36fc790aa354196df20938",
    "work/z5la/o_final.py": "e51582d64e664714524ccf566178c94fc30b202a",
    "work/z5la/o_final.log": "fdb111957380d1be0876982f706980eb074fc9ab",
    "work/z5la/solve.py": "478b15ce7584b5e8af6caaf5326d99c85a7b55bf",
}
EXPECTED_MONOMIALS = [
    "u2*xk", "u2*xl", "u2*yk", "u2*yl", "u2*zk", "u2*zl", "u2", "u3",
    "xk", "xl", "yk", "yl", "zk", "zl", "1",
]

GEOM_N = 5
GEOM_P = 4194301
GEOM_M = 7
E1_NUMERATOR_DEGREE = 28
E1_COLUMNS = 1624
CURL_H_DEGREE = 23
CURL_DIMENSION = 576
GENERIC_RANK = 1048
OPERATOR_WITNESS_ROWS = 1048
CURL_WITNESS_POINTS = 288
POINTS_SHA256 = "9bed1c3ec0364df8409a91ff6026bc1cc946b9380eff44937d9974e73ced3c66"
OPERATOR_MATRIX_SHA256 = "8aa3f1029c385c2414222d9b902514383a7d587f34295acf9f9117b7874bbab6"
CURL_EVAL_MATRIX_SHA256 = "4a69d83ff9ffc71b2bc636e5edc5bfe0fd09cd082678272faaa66bb2d997e0d6"


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _fetch(path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{SOURCE_COMMIT}/{path}"
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    got = _git_blob_sha1(data)
    expected = SOURCE_BLOBS[path]
    if got != expected:
        raise AssertionError(f"source lock drift for {path}: {got} != {expected}")
    return data


def _poly_from_asc(values, var):
    """Build an integer polynomial from the source's constant-first coefficient lists."""
    return sp.Poly.from_list([int(x) for x in reversed(values)], gens=var, domain=sp.ZZ)


def _inv_mod(value: int, p: int) -> int:
    return pow(int(value) % p, p - 2, p)


def _gk_mod(n: int, k: int, l: int, p: int) -> int:
    num = (n + 7 - k) ** 2 * (n + k + 1) * (n + k + l + 1)
    den = (k + 1) ** 3 * (k + l + 1)
    return num % p * _inv_mod(den, p) % p


def _gl_mod(n: int, k: int, l: int, p: int) -> int:
    num = (n + 7 - l) ** 2 * (n + l + 1) * (n + k + l + 1)
    den = (l + 1) ** 3 * (k + l + 1)
    return num % p * _inv_mod(den, p) % p


def _e1_den_mod(n: int, k: int, l: int, p: int) -> int:
    value = (k + 1) * (l + 1) * (k + l + 1) * (k + l + 2)
    value %= p
    for j in range(1, 8):
        value = value * ((n + k + j) % p) % p
        value = value * ((n + l + j) % p) % p
    return value


def _h_den_mod(n: int, k: int, l: int, p: int) -> int:
    value = (k + l + 1) % p
    for j in range(1, 7):
        value = value * ((n + k + j) % p) % p
        value = value * ((n + l + j) % p) % p
    return value


def _h_prefactor_mod(n: int, k: int, l: int, p: int) -> int:
    return k * k % p * (l * l % p) % p * _inv_mod(_h_den_mod(n, k, l, p), p) % p


def _source_point_ok(n: int, k: int, l: int, m: int, p: int) -> bool:
    checks = [k + 1, l + 1, k + 2, l + 2, k + l + 1, k + l + 2, k + l + 3]
    for j in range(0, m + 6):
        checks.extend((n + k + j, n + l + j, n + k + l + j, n + j - k, n + j - l))
    return all(value % p != 0 for value in checks)


def _source_points(count: int) -> list[tuple[int, int]]:
    rng = np.random.default_rng(12345 + GEOM_P % 1000003 + 7919 * GEOM_N + 31 * GEOM_M)
    points: list[tuple[int, int]] = []
    rejected = 0
    while len(points) < count:
        k = int(rng.integers(2, GEOM_P - 2))
        l = int(rng.integers(2, GEOM_P - 2))
        if _source_point_ok(GEOM_N, k, l, GEOM_M, GEOM_P):
            points.append((k, l))
        else:
            rejected += 1
            if rejected > 100000:
                raise RuntimeError("unable to reproduce source-safe point stream")
    return points


def _points_sha256(points: list[tuple[int, int]]) -> str:
    digest = hashlib.sha256()
    for k, l in points:
        digest.update(f"{k},{l}\n".encode("ascii"))
    return digest.hexdigest()


def _matrix_sha256(matrix: np.ndarray) -> str:
    canonical = np.asarray(matrix, dtype="<i8", order="C")
    return hashlib.sha256(canonical.tobytes(order="C")).hexdigest()


def _rank_mod(matrix: np.ndarray, p: int) -> int:
    """Exact row elimination mod p; int64 products stay below p^2 < 2^63."""
    a = np.asarray(matrix, dtype=np.int64).copy() % p
    rows, cols = a.shape
    rank = 0
    for col in range(cols):
        nz = np.nonzero(a[rank:, col])[0]
        if nz.size == 0:
            continue
        pivot = rank + int(nz[0])
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
        inv = _inv_mod(a[rank, col], p)
        a[rank, :] = a[rank, :] * inv % p
        nz_rows = np.nonzero(a[rank + 1:, col])[0] + rank + 1
        for row in nz_rows:
            factor = int(a[row, col])
            a[row, :] = (a[row, :] - factor * a[rank, :]) % p
        rank += 1
        if rank == rows:
            break
    return rank


def _operator_eval_matrix(points: list[tuple[int, int]]) -> np.ndarray:
    deg = E1_NUMERATOR_DEGREE
    r_mons = [(a, b) for a in range(1, deg + 1) for b in range(0, deg + 1)]
    s_mons = [(a, b) for a in range(0, deg + 1) for b in range(1, deg + 1)]
    matrix = np.empty((len(points), len(r_mons) + len(s_mons)), dtype=np.int64)
    for row, (k, l) in enumerate(points):
        i_d = _inv_mod(_e1_den_mod(GEOM_N, k, l, GEOM_P), GEOM_P)
        i_dk = _inv_mod(_e1_den_mod(GEOM_N, k + 1, l, GEOM_P), GEOM_P)
        i_dl = _inv_mod(_e1_den_mod(GEOM_N, k, l + 1, GEOM_P), GEOM_P)
        gk = _gk_mod(GEOM_N, k, l, GEOM_P)
        gl = _gl_mod(GEOM_N, k, l, GEOM_P)
        kp = [pow(k % GEOM_P, a, GEOM_P) for a in range(deg + 1)]
        lp = [pow(l % GEOM_P, b, GEOM_P) for b in range(deg + 1)]
        k1p = [pow((k + 1) % GEOM_P, a, GEOM_P) for a in range(deg + 1)]
        l1p = [pow((l + 1) % GEOM_P, b, GEOM_P) for b in range(deg + 1)]
        out = 0
        for a, b in r_mons:
            matrix[row, out] = (
                gk * k1p[a] % GEOM_P * lp[b] % GEOM_P * i_dk
                - kp[a] * lp[b] % GEOM_P * i_d
            ) % GEOM_P
            out += 1
        for a, b in s_mons:
            matrix[row, out] = (
                gl * kp[a] % GEOM_P * l1p[b] % GEOM_P * i_dl
                - kp[a] * lp[b] % GEOM_P * i_d
            ) % GEOM_P
            out += 1
    return matrix


def _curl_eval_matrix(points: list[tuple[int, int]]) -> np.ndarray:
    rows: list[np.ndarray] = []
    for k, l in points:
        h0 = _h_prefactor_mod(GEOM_N, k, l, GEOM_P)
        hl = _h_prefactor_mod(GEOM_N, k, l + 1, GEOM_P)
        hk = _h_prefactor_mod(GEOM_N, k + 1, l, GEOM_P)
        gk = _gk_mod(GEOM_N, k, l, GEOM_P)
        gl = _gl_mod(GEOM_N, k, l, GEOM_P)
        kp = [pow(k % GEOM_P, a, GEOM_P) for a in range(CURL_H_DEGREE + 1)]
        lp = [pow(l % GEOM_P, b, GEOM_P) for b in range(CURL_H_DEGREE + 1)]
        k1p = [pow((k + 1) % GEOM_P, a, GEOM_P) for a in range(CURL_H_DEGREE + 1)]
        l1p = [pow((l + 1) % GEOM_P, b, GEOM_P) for b in range(CURL_H_DEGREE + 1)]
        r = np.empty(CURL_DIMENSION, dtype=np.int64)
        s = np.empty(CURL_DIMENSION, dtype=np.int64)
        index = 0
        for a in range(CURL_H_DEGREE + 1):
            for b in range(CURL_H_DEGREE + 1):
                r[index] = (
                    gl * hl % GEOM_P * kp[a] % GEOM_P * l1p[b]
                    - h0 * kp[a] % GEOM_P * lp[b]
                ) % GEOM_P
                s[index] = (
                    -gk * hk % GEOM_P * k1p[a] % GEOM_P * lp[b]
                    + h0 * kp[a] % GEOM_P * lp[b]
                ) % GEOM_P
                index += 1
        rows.extend((r, s))
    return np.asarray(rows, dtype=np.int64)


def _exact_curl_representability(n, k, l) -> dict:
    H0, Hl1, Hk1 = sp.symbols("H0 Hl1 Hk1")
    d_e1 = (k + 1) * (l + 1) * (k + l + 1) * (k + l + 2)
    for j in range(1, 8):
        d_e1 *= (n + k + j) * (n + l + j)
    d_h = k + l + 1
    for j in range(1, 7):
        d_h *= (n + k + j) * (n + l + j)
    gk = ((n + 7 - k) ** 2 * (n + k + 1) * (n + k + l + 1)) / (
        (k + 1) ** 3 * (k + l + 1)
    )
    gl = ((n + 7 - l) ** 2 * (n + l + 1) * (n + k + l + 1)) / (
        (l + 1) ** 3 * (k + l + 1)
    )
    h0 = k**2 * l**2 * H0 / d_h
    hl1 = k**2 * (l + 1) ** 2 * Hl1 / d_h.subs(l, l + 1)
    hk1 = (k + 1) ** 2 * l**2 * Hk1 / d_h.subs(k, k + 1)

    nr = sp.cancel(d_e1 * (gl * hl1 - h0))
    ns = sp.cancel(d_e1 * (-gk * hk1 + h0))
    expected_nr = k**2 * (k + 1) * (n + k + 7) * (
        (n + 7 - l) ** 2 * (n + l + 1) ** 2 * (n + k + l + 1) * Hl1
        - l**2 * (l + 1) * (k + l + 2) * (n + l + 7) * H0
    )
    expected_ns = l**2 * (l + 1) * (n + l + 7) * (
        k**2 * (k + 1) * (k + l + 2) * (n + k + 7) * H0
        - (n + 7 - k) ** 2 * (n + k + 1) ** 2 * (n + k + l + 1) * Hk1
    )
    if sp.cancel(nr - expected_nr) != 0 or sp.cancel(ns - expected_ns) != 0:
        raise AssertionError("E1 discrete-curl denominator clearing failed")

    if not expected_nr.has(k**2) or not expected_ns.has(l**2):
        raise AssertionError("boundary factors lost from discrete-curl map")
    return {
        "potential_denominator": "(k+l+1)*prod_{j=1..6}(n+k+j)(n+l+j)",
        "potential_boundary_factor": "k^2*l^2",
        "potential_bidegree": [23, 23],
        "potential_dimension": CURL_DIMENSION,
        "e1_numerator_bidegree_bound": [28, 28],
        "r_boundary_divisibility": "k^2",
        "s_boundary_divisibility": "l^2",
        "numerator_formula_exact": True,
    }


def _geometry_evidence(n, k, l) -> dict:
    representability = _exact_curl_representability(n, k, l)
    points = _source_points(OPERATOR_WITNESS_ROWS)
    if _points_sha256(points) != POINTS_SHA256:
        raise AssertionError("deterministic source point stream drift")

    operator = _operator_eval_matrix(points)
    if operator.shape != (OPERATOR_WITNESS_ROWS, E1_COLUMNS):
        raise AssertionError("E1 operator matrix shape drift")
    if _matrix_sha256(operator) != OPERATOR_MATRIX_SHA256:
        raise AssertionError("E1 operator witness digest drift")
    operator_rank = _rank_mod(operator, GEOM_P)
    if operator_rank != GENERIC_RANK:
        raise AssertionError(f"E1 operator lower-bound rank drift: {operator_rank}")

    curl_eval = _curl_eval_matrix(points[:CURL_WITNESS_POINTS])
    if curl_eval.shape != (CURL_DIMENSION, CURL_DIMENSION):
        raise AssertionError("curl evaluation witness shape drift")
    if _matrix_sha256(curl_eval) != CURL_EVAL_MATRIX_SHA256:
        raise AssertionError("curl evaluation witness digest drift")
    curl_rank = _rank_mod(curl_eval, GEOM_P)
    if curl_rank != CURL_DIMENSION:
        raise AssertionError(f"curl image rank drift: {curl_rank}")

    return {
        **representability,
        "witness": {
            "n": GEOM_N,
            "prime": GEOM_P,
            "point_count": OPERATOR_WITNESS_ROWS,
            "point_stream_sha256": POINTS_SHA256,
            "operator_rows": OPERATOR_WITNESS_ROWS,
            "operator_columns": E1_COLUMNS,
            "operator_matrix_sha256": OPERATOR_MATRIX_SHA256,
            "operator_modular_rank": operator_rank,
            "curl_eval_points": CURL_WITNESS_POINTS,
            "curl_eval_matrix_sha256": CURL_EVAL_MATRIX_SHA256,
            "curl_eval_modular_rank": curl_rank,
        },
        "generic_rank": GENERIC_RANK,
        "generic_kernel_dimension": E1_COLUMNS - GENERIC_RANK,
        "curl_image_dimension": CURL_DIMENSION,
        "curl_image_equals_generic_kernel": True,
        "characteristic_zero_argument": (
            "exact flatness plus exact E1 denominator clearing gives a 576-dimensional "
            "generic curl subspace of the kernel; nonzero modular minors witness curl "
            "rank 576 and operator rank 1048, forcing equality over Q(n)"
        ),
        "source_reported_rank_1106_kernel_518_reconciled": True,
        "source_reported_geometry_disposition": "RECONCILED_AS_MIXED_ANSATZ_DIMENSION_ACCOUNTING",
    }


def build_preflight() -> dict:
    locked = {path: _fetch(path) for path in SOURCE_BLOBS}
    lift = json.loads(locked["work/z5la/a_lift.json"])
    partial = json.loads(locked["work/z5la/z5cf_order7_partial.json"])

    if partial["operator"]["L_min"] != "A . L_BZ,  order 7":
        raise AssertionError("order-7 operator declaration drift")
    if partial["operator"]["A"] != "sum_{t=0}^{4} a_t(n) S_n^t":
        raise AssertionError("left-multiplier declaration drift")
    if partial["operator"]["a"] != lift["a"]:
        raise AssertionError("A coefficient arrays disagree across locked source objects")
    if partial["monomials"] != EXPECTED_MONOMIALS:
        raise AssertionError("order-7 15-block module drift")
    if len(partial["theoremR"]["Q_t"]) != 5:
        raise AssertionError("Theorem-R transport count drift")

    n, k, l = sp.symbols("n k l")
    a_polys = [_poly_from_asc(row, n) for row in lift["a"]]
    if len(a_polys) != 5 or any(poly.degree() != 58 for poly in a_polys):
        raise AssertionError("A must contain five exact degree-58 integer polynomials")

    a0 = 41218 * n**3 + 198849 * n**2 + 320790 * n + 173057
    f4 = _poly_from_asc(lift["F4"], n)
    f4_shift2 = _poly_from_asc(lift["F4_shift2"], n)
    shifted = sp.Poly(sp.expand(f4.as_expr().subs(n, n + 2)), n, domain=sp.ZZ)
    if shifted != f4_shift2:
        raise AssertionError("F4_shift2 is not the exact polynomial shift F4(n+2)")
    if not all(int(c) > 0 for c in f4_shift2.all_coeffs()):
        raise AssertionError("F4(n+2) coefficient-positivity witness drift")

    expected_a4 = sp.Poly(
        sp.expand(
            4
            * (n + 5)
            * (n + 6) ** 3
            * (n + 7) ** 2
            * (2 * n + 13) ** 2
            * a0.subs(n, n + 1)
            * a0.subs(n, n + 2)
            * a0.subs(n, n + 3)
            * f4.as_expr()
        ),
        n,
        domain=sp.ZZ,
    )
    if a_polys[4] != expected_a4:
        raise AssertionError("exact a4 factorization failed")
    a4_0 = int(a_polys[4].eval(0))
    a4_1 = int(a_polys[4].eval(1))
    if a4_0 == 0 or a4_1 == 0:
        raise AssertionError("a4 direct initial nonvanishing check failed")

    gk = ((n + 7 - k) ** 2 * (n + k + 1) * (n + k + l + 1)) / (
        (k + 1) ** 3 * (k + l + 1)
    )
    gl = ((n + 7 - l) ** 2 * (n + l + 1) * (n + k + l + 1)) / (
        (l + 1) ** 3 * (k + l + 1)
    )
    curvature = sp.cancel(gk * gl.subs(k, k + 1) - gl * gk.subs(l, l + 1))
    if curvature != 0:
        raise AssertionError("order-7 normalized shift connection is not flat")

    geometry = _geometry_evidence(n, k, l)

    return {
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "protected_base": PROTECTED_BASE,
        "predecessor_terminal": PREDECESSOR_TERMINAL,
        "source": {
            "repository": SOURCE_REPOSITORY,
            "commit": SOURCE_COMMIT,
            "git_blob_sha1": {path: SOURCE_BLOBS[path] for path in sorted(SOURCE_BLOBS)},
        },
        "operator": {
            "order": 7,
            "left_multiplier_order": 4,
            "a_polynomial_count": len(a_polys),
            "a_polynomial_degrees": [poly.degree() for poly in a_polys],
            "a4_factorization_exact": True,
            "a4_at_0": str(a4_0),
            "a4_at_1": str(a4_1),
            "f4_shift2_exact": True,
            "f4_shift2_all_coefficients_positive": True,
            "a4_nonvanishing_argument": "n=0,1 direct; for n>=2 put m=n-2, use F4(m+2) coefficient positivity and positive explicit factors",
        },
        "module": {
            "monomial_count": len(EXPECTED_MONOMIALS),
            "monomials": EXPECTED_MONOMIALS,
            "theorem_r_transport_count": len(partial["theoremR"]["Q_t"]),
            "residual_block_count": 8,
        },
        "gauge": {
            "flatness_identity": "gk(n,k,l)*gl(n,k+1,l)=gl(n,k,l)*gk(n,k,l+1)",
            "flatness_exact": True,
            "trivial_pair": "(gl*h(l+1)-h, -(gk*h(k+1)-h))",
            "interpretation": "structured discrete-curl syzygy; exact E1 kernel after reconstruction",
        },
        "residual_geometry": geometry,
        "source_reported_residual_geometry": {
            "cofactor_columns": 1624,
            "generic_rank": 1106,
            "kernel_dimension": 518,
            "authority": "SOURCE_SUMMARY_CROSS_REGIME_ARITHMETIC_NOT_PROMOTED",
            "disposition": "RECONCILED_AS_MIXED_ANSATZ_DIMENSION_ACCOUNTING",
            "unforced_scan_columns": 1682,
            "unforced_scan_rank": 1106,
            "unforced_scan_kernel_dimension": 576,
            "boundary_forced_columns": 1624,
            "boundary_forced_reconstructed_rank": 1048,
            "boundary_forced_kernel_dimension": 576,
        },
        "terminal": TERMINAL,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
