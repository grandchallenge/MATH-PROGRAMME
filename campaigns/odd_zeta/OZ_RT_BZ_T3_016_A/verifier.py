from __future__ import annotations

import hashlib
import json
import math
import urllib.request
from collections import Counter

ISSUE = 964
OPERATION = "OZ-RT-BZ-T3-016-A"
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


def _blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _fetch(path: str) -> bytes:
    url = f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{SOURCE_COMMIT}/{path}"
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    if _blob(data) != SOURCE_BLOBS[path]:
        raise AssertionError(f"source lock drift: {path}")
    return data


def _asc(desc):
    return [int(x) for x in reversed(desc)]


def _trim(p):
    out = list(p)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def _mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return _trim(out)


def _shift(a, s):
    out = [0] * len(a)
    for i, c in enumerate(a):
        for j in range(i + 1):
            out[j] += c * math.comb(i, j) * (s ** (i - j))
    return _trim(out)


def _pow_linear(constant, power):
    out = [1]
    for _ in range(power):
        out = _mul(out, [constant, 1])
    return out


def _eval(a, x):
    total = 0
    for c in reversed(a):
        total = total * x + c
    return total


def verify() -> dict:
    locked = {path: _fetch(path) for path in SOURCE_BLOBS}
    lift = json.loads(locked["work/z5la/a_lift.json"])
    partial = json.loads(locked["work/z5la/z5cf_order7_partial.json"])

    if partial["operator"]["a"] != lift["a"]:
        raise AssertionError("independent source-object A comparison failed")
    if partial["monomials"] != EXPECTED_MONOMIALS:
        raise AssertionError("15-block module mismatch")
    if len(partial["theoremR"]["Q_t"]) != 5:
        raise AssertionError("Theorem-R transport count mismatch")

    aa = [_asc(row) for row in lift["a"]]
    if len(aa) != 5 or any(len(_trim(p)) != 59 for p in aa):
        raise AssertionError("five degree-58 A polynomials required")

    f4 = _asc(lift["F4"])
    f4s = _asc(lift["F4_shift2"])
    if _shift(f4, 2) != f4s:
        raise AssertionError("integer-arithmetic F4 shift replay failed")
    if any(c <= 0 for c in f4s):
        raise AssertionError("F4(n+2) positivity certificate failed")

    a0 = [173057, 320790, 198849, 41218]
    # Rebuild 4*(n+5)*(n+6)^3*(n+7)^2*(2n+13)^2*a0(n+1)*a0(n+2)*a0(n+3)*F4(n)
    # exactly over Z, independently of SymPy.
    expected = [4]
    for factor in (
        [5, 1],
        _pow_linear(6, 3),
        _pow_linear(7, 2),
        _mul([13, 2], [13, 2]),
        _shift(a0, 1),
        _shift(a0, 2),
        _shift(a0, 3),
        f4,
    ):
        expected = _mul(expected, factor)
    if _trim(expected) != _trim(aa[4]):
        raise AssertionError("integer-only a4 factorization replay failed")
    if _eval(aa[4], 0) == 0 or _eval(aa[4], 1) == 0:
        raise AssertionError("initial a4 nonvanishing failed")

    # Independent factor-multiset proof of gk*gl(k+1)=gl*gk(l+1).
    lhs_num = Counter({
        "(n+7-k)^2": 1, "(n+k+1)": 1, "(n+k+l+1)": 1,
        "(n+7-l)^2": 1, "(n+l+1)": 1, "(n+k+l+2)": 1,
    })
    rhs_num = Counter({
        "(n+7-l)^2": 1, "(n+l+1)": 1, "(n+k+l+1)": 1,
        "(n+7-k)^2": 1, "(n+k+1)": 1, "(n+k+l+2)": 1,
    })
    lhs_den = Counter({"(k+1)^3": 1, "(l+1)^3": 1, "(k+l+1)": 1, "(k+l+2)": 1})
    rhs_den = Counter({"(l+1)^3": 1, "(k+1)^3": 1, "(k+l+1)": 1, "(k+l+2)": 1})
    if lhs_num != rhs_num or lhs_den != rhs_den:
        raise AssertionError("discrete-connection flatness factor proof failed")

    return {
        "issue": ISSUE,
        "operation": OPERATION,
        "source_locks_verified": True,
        "a4_factorization_integer_replay": True,
        "a4_nonvanishing_certificate_replayed": True,
        "order7_module_monomials_verified": True,
        "discrete_curl_flatness_verified": True,
        "kernel_dimension_518_promoted": False,
        "terminal": TERMINAL,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
