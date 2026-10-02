from __future__ import annotations

import hashlib
import json
from fractions import Fraction as Q
from functools import lru_cache
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
T3_009_DIR = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_009"

ISSUE = 925
OPERATION = "OZ-RT-BZ-T3-012-A"
PRIME = 1000003
MAX_DEGREE = 9
EXTRA_ROWS = 8
FIXED_OBSTRUCTION = Q(92296128886152)
CLOSURE_TERMINAL = "NORMALIZED_RECURRENCE_OPERATOR_TANGENT_POLY_DEG_LE_9_EXHAUSTED"

SOURCE_BLOBS = {
    "deformation_span.py": "bddf470b146fd7c4983934ec90fafc9527318092",
    "DEFORMATION_SPAN_RESULT.json": "e9840614d86ab9ba627c69bfaf1d0dbd12ce38a4",
    "qrow_replay.wl": "8881e656642c8d1a3b8309750d4bb7152f73f5da",
    "BASELINE_RESULT.json": "0849bd3c41d9d89652e2c895515a78e4a8b3542e",
}

def _git_blob(path: Path) -> str:
    data = path.read_bytes()
    payload = b"blob " + str(len(data)).encode() + b"\0" + data
    return hashlib.sha1(payload).hexdigest()

def _locks() -> dict[str, str]:
    got = {}
    for name, want in SOURCE_BLOBS.items():
        value = _git_blob(T3_009_DIR / name)
        if value != want:
            raise AssertionError(f"independent source lock drift: {name}")
        got[name] = value
    protected = json.loads((T3_009_DIR / "DEFORMATION_SPAN_RESULT.json").read_text())
    fixed = protected.get("fixed_qrow_operator_obstruction", {})
    if fixed.get("tested_direction") != "H_k_1":
        raise AssertionError("independent tangent lock drift")
    if Q(int(fixed.get("exact_LBZ_Y_at_n0", "0"))) != FIXED_OBSTRUCTION:
        raise AssertionError("independent protected obstruction drift")
    return got

def _choose(n: int, r: int) -> int:
    if r < 0 or r > n:
        return 0
    r = min(r, n-r)
    return factorial(n) // (factorial(r) * factorial(n-r))

def _kernel(n: int, k: int, l: int) -> int:
    return (
        _choose(n+k, n) * _choose(n, k) * _choose(n, k)
        * _choose(n+l, n) * _choose(n, l) * _choose(n, l)
        * _choose(n+k+l, n)
    )

@lru_cache(maxsize=None)
def _harmonic(k: int) -> Q:
    value = Q(0)
    for r in range(k, 0, -1):
        value += Q(1, r)
    return value

@lru_cache(maxsize=None)
def _sequences(n: int) -> tuple[int, Q]:
    base = 0
    tangent = Q(0)
    hk = [_harmonic(k) for k in range(n+1)]
    for l in range(n, -1, -1):
        for k in range(n, -1, -1):
            term = _kernel(n, k, l)
            base += term
            tangent += Q(term) * hk[k]
    return base, tangent

def _coeffs(n: int) -> tuple[int, int, int, int]:
    aa = 41218*n**3 + 198849*n**2 + 320790*n + 173057
    aa1 = 41218*(n+1)**3 + 198849*(n+1)**2 + 320790*(n+1) + 173057
    bb8 = (
        3874492*n**8 + 59373972*n**7 + 394148190*n**6
        + 1481084196*n**5 + 3447878810*n**4 + 5095855458*n**3
        + 4673546679*n**2 + 2433871008*n + 551502039
    )
    bb9 = (
        48802112*n**9 + 967468896*n**8 + 8488000862*n**7
        + 43246197636*n**6 + 140983768422*n**5 + 304912330849*n**4
        + 437406946975*n**3 + 401272692378*n**2
        + 213593890911*n + 50257929339
    )
    return (
        (n+1)**5 * (n+2) * aa1,
        -2*(n+2)*bb8,
        -2*bb9,
        2*(n+3)**5*(2*n+5)*aa,
    )

def _residual(n: int) -> Q:
    cc = _coeffs(n)
    return sum((Q(cc[j]) * _sequences(n+j)[1] for j in range(4)), Q(0))

def _columns(degree: int) -> tuple[tuple[int, int], ...]:
    values = []
    for j in range(4):
        for m in range(degree + 1):
            if degree == 9 and j == 3 and m == 9:
                continue
            values.append((j, m))
    return tuple(values)

def _mod(q: Q) -> int:
    den = q.denominator % PRIME
    if den == 0:
        raise AssertionError("independent denominator vanishes modulo rank prime")
    return (q.numerator % PRIME) * pow(den, -1, PRIME) % PRIME

def _rank_alt(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    a = [list(reversed([x % PRIME for x in row])) for row in reversed(rows)]
    m, n = len(a), len(a[0])
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, m):
            if a[row][col] % PRIME:
                pivot = row
                break
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        pv = a[rank][col] % PRIME
        inv = pow(pv, PRIME-2, PRIME)
        for row in range(rank+1, m):
            if not a[row][col]:
                continue
            factor = a[row][col] * inv % PRIME
            for c in range(col, n):
                a[row][c] = (a[row][c] - factor*a[rank][c]) % PRIME
        rank += 1
        if rank == m:
            break
    return rank

def _stage(degree: int) -> dict:
    columns = _columns(degree)
    count = len(columns) + EXTRA_ROWS
    matrix = []
    augmented = []
    denominator_checks = 0
    for n in range(count):
        row = []
        for j, power in columns:
            base = _sequences(n+j)[0]
            row.append((base % PRIME) * pow(n, power, PRIME) % PRIME)
        rhs = _mod(-_residual(n))
        denominator_checks += 1
        matrix.append(row)
        augmented.append(row + [rhs])
    rank = _rank_alt(matrix)
    aug_rank = _rank_alt(augmented)
    return {
        "degree": degree,
        "unknown_count": len(columns),
        "row_count": count,
        "coefficient_rank_mod_prime": rank,
        "augmented_rank_mod_prime": aug_rank,
        "denominator_checks": denominator_checks,
        "exact_inconsistency_over_Q_certified": (
            rank == len(columns) and aug_rank == len(columns)+1
        ),
    }

def verify(result: dict) -> dict:
    locks = _locks()
    if result.get("issue") != ISSUE or result.get("operation") != OPERATION:
        raise AssertionError("producer operation identity drift")
    if result.get("source_locks") != locks:
        raise AssertionError("producer source-lock evidence mismatch")
    ys = [_sequences(n)[1] for n in range(4)]
    if ys != [Q(0), Q(16), Q(3564), Q(3214312,3)]:
        raise AssertionError("independent H_k baseline drift")
    obstruction = _residual(0)
    if obstruction != FIXED_OBSTRUCTION:
        raise AssertionError("independent fixed-operator obstruction mismatch")

    got = []
    producer_stages = result.get("stages", [])
    if len(producer_stages) != MAX_DEGREE+1:
        raise AssertionError("producer degree ladder length drift")
    for degree in range(MAX_DEGREE+1):
        rec = _stage(degree)
        src = producer_stages[degree]
        for key in (
            "degree", "unknown_count", "row_count",
            "coefficient_rank_mod_prime", "augmented_rank_mod_prime",
            "exact_inconsistency_over_Q_certified",
        ):
            if src.get(key) != rec[key]:
                raise AssertionError(f"producer/verifier stage disagreement d={degree}: {key}")
        if src.get("rational_denominator_nonzero_mod_prime_checks") != rec["denominator_checks"]:
            raise AssertionError("denominator-check count disagreement")
        got.append(rec)

    if not all(x["exact_inconsistency_over_Q_certified"] for x in got):
        raise AssertionError("independent replay did not certify full bounded exhaustion")
    if result.get("terminal") != CLOSURE_TERMINAL:
        raise AssertionError("producer terminal disagrees with independent bounded exhaustion")
    if result.get("characterized_blocker") is not None:
        raise AssertionError("unexpected producer blocker on independently closed class")
    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("claim firewall drift")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("claim effect drift")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status drift")

    return {
        "status": "INDEPENDENT_RECURRENCE_OPERATOR_TANGENT_REPLAY_COMPLETE",
        "terminal": CLOSURE_TERMINAL,
        "stage_count": len(got),
        "degree9_unknown_count": got[-1]["unknown_count"],
        "degree9_coefficient_rank_mod_prime": got[-1]["coefficient_rank_mod_prime"],
        "degree9_augmented_rank_mod_prime": got[-1]["augmented_rank_mod_prime"],
        "fixed_operator_tangent_obstruction_at_n0": [obstruction.numerator, obstruction.denominator],
        "all_declared_stages_exactly_inconsistent_over_Q": True,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
