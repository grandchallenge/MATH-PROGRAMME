from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
ISSUE = 964
OPERATION = "OZ-RT-BZ-T3-016-A"
STAGE = "T3_016_A_ORDER7_SOURCE_PREFLIGHT"
PROTECTED_BASE = "a05c16d2988a9a0c73f9c62b482c96777a49c5ea"
PREDECESSOR_TERMINAL = "GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED"
TERMINAL = "ORDER7_SOURCE_PREFLIGHT_REPLAYED__POPOV_REDUCTION_REQUIRED"

SOURCE_REPOSITORY = "rain-1/-odd-zeta-values-moremath"
SOURCE_COMMIT = "6cc0bf07137815ceeef0d9f340559f85352391e5"
SOURCE_BLOBS = {
    "work/Z5CF_TELESCOPER.md": "a634b070d5d95d09749137c26bc51012f318683b",
    "work/Z5CF_LIFT.md": "f1c48b2ce0951ef4a4aefa1d449e53fe33ce5cc5",
    "work/Z5CF_LINALG.md": "637ecaa7f3ee941a87932de390eb7336d7fde677",
    "work/z5la/z5cf_order7_partial.json": "d6024c7244a4a45ac759b455f65fca6d377b735d",
    "work/z5la/a_lift.json": "564fc9637f31b870d85dab293d6cbb5cfe52bae0",
    "work/z5la/o_scan.py": "bc6e9a59a48b15eddbab8e80ad4e5063972582d2",
    "work/z5la/o_csweep.py": "b506b9d6fbd405e6ac36fc790aa354196df20938",
    "work/z5la/solve.py": "478b15ce7584b5e8af6caaf5326d99c85a7b55bf",
}
EXPECTED_MONOMIALS = [
    "u2*xk", "u2*xl", "u2*yk", "u2*yl", "u2*zk", "u2*zl", "u2", "u3",
    "xk", "xl", "yk", "yl", "zk", "zl", "1",
]


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


def _poly_from_desc(values, var):
    return sp.Poly.from_list([int(x) for x in values], gens=var, domain=sp.ZZ)


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
    a_polys = [_poly_from_desc(row, n) for row in lift["a"]]
    if len(a_polys) != 5 or any(poly.degree() != 58 for poly in a_polys):
        raise AssertionError("A must contain five exact degree-58 integer polynomials")

    a0 = 41218 * n**3 + 198849 * n**2 + 320790 * n + 173057
    f4 = _poly_from_desc(lift["F4"], n)
    f4_shift2 = _poly_from_desc(lift["F4_shift2"], n)
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
            "interpretation": "structured discrete-curl syzygy; quotient before degree minimization",
        },
        "reported_residual_geometry": {
            "cofactor_columns": 1624,
            "generic_rank": 1106,
            "kernel_dimension": 518,
            "authority": "SOURCE_REPORTED_PENDING_GENERIC_CHAR0_REPLAY",
        },
        "terminal": TERMINAL,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    print(json.dumps(build_preflight(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
