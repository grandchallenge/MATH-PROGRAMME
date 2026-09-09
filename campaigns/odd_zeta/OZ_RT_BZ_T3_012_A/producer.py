from __future__ import annotations

import hashlib
import json
import math
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
T3_009_DIR = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_009"

OPERATION = "OZ-RT-BZ-T3-012-A"
STAGE = "T3_012_A_RECURRENCE_OPERATOR_TANGENT_DEFORMATION_VIABILITY_GATE"
ISSUE = 925
PROTECTED_INTAKE = "5accb4c59db6e0495476a08afed87fb62c196a20"
PRIME = 1000003
MAX_DEGREE = 9
EXTRA_ROWS = 8
FIXED_OBSTRUCTION = 92296128886152
CLOSURE_TERMINAL = "NORMALIZED_RECURRENCE_OPERATOR_TANGENT_POLY_DEG_LE_9_EXHAUSTED"
CANDIDATE_TERMINAL = "RECURRENCE_OPERATOR_TANGENT_CANDIDATE_FOUND__LOCAL_CERTIFICATE_REQUIRED"
BLOCKER_TERMINAL = "RECURRENCE_OPERATOR_TANGENT_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"

T3_009_BLOBS = {
    "deformation_span.py": "bddf470b146fd7c4983934ec90fafc9527318092",
    "DEFORMATION_SPAN_RESULT.json": "e9840614d86ab9ba627c69bfaf1d0dbd12ce38a4",
    "qrow_replay.wl": "8881e656642c8d1a3b8309750d4bb7152f73f5da",
    "BASELINE_RESULT.json": "0849bd3c41d9d89652e2c895515a78e4a8b3542e",
}

def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()

def source_locks() -> dict[str, str]:
    got = {}
    for name, want in T3_009_BLOBS.items():
        value = git_blob_sha1(T3_009_DIR / name)
        if value != want:
            raise AssertionError(f"T3-009 source lock drift: {name}: {value} != {want}")
        got[name] = value
    prior = json.loads((T3_009_DIR / "DEFORMATION_SPAN_RESULT.json").read_text())
    obs = prior["fixed_qrow_operator_obstruction"]
    if obs["tested_direction"] != "H_k_1":
        raise AssertionError("protected tangent direction drift")
    if int(obs["exact_LBZ_Y_at_n0"]) != FIXED_OBSTRUCTION or not obs["nonzero"]:
        raise AssertionError("protected fixed-operator obstruction drift")
    scope = prior["scope"]
    if "parameter-dependent recurrence coefficients" not in scope:
        raise AssertionError("protected operator-deformation scope anchor missing")
    return got

def validate_scope(
    recurrence_order: int = 3,
    max_polynomial_degree: int = 9,
    rational_coefficient_family: bool = False,
    recurrence_fitting: bool = False,
    multiplier_widening: bool = False,
    support_or_harmonic_widening: bool = False,
    correction_recombination: bool = False,
    theorem_promotion: bool = False,
) -> None:
    if recurrence_order != 3:
        raise AssertionError("new recurrence order not authorized")
    if max_polynomial_degree != 9:
        raise AssertionError("arbitrary recurrence-coefficient degree widening not authorized")
    if rational_coefficient_family:
        raise AssertionError("rational recurrence-coefficient family not authorized")
    if recurrence_fitting:
        raise AssertionError("fitted recurrence substitution not authorized")
    if multiplier_widening:
        raise AssertionError("multiplier widening not authorized")
    if support_or_harmonic_widening:
        raise AssertionError("support/harmonic widening not authorized")
    if correction_recombination:
        raise AssertionError("correction-layer recombination not authorized")
    if theorem_promotion:
        raise AssertionError("theorem promotion not authorized")

@lru_cache(maxsize=None)
def harmonic(k: int) -> Q:
    return sum((Q(1, j) for j in range(1, k + 1)), Q(0))

def kernel(n: int, k: int, l: int) -> int:
    return (
        comb(n + k, n) * comb(n, k) ** 2
        * comb(n + l, n) * comb(n, l) ** 2
        * comb(n + k + l, n)
    )

@lru_cache(maxsize=None)
def y0(n: int) -> int:
    return sum(kernel(n, k, l) for k in range(n + 1) for l in range(n + 1))

@lru_cache(maxsize=None)
def yhk(n: int) -> Q:
    total = Q(0)
    for k in range(n + 1):
        hk = harmonic(k)
        for l in range(n + 1):
            total += kernel(n, k, l) * hk
    return total

def a0(n: int) -> int:
    return 41218*n**3 + 198849*n**2 + 320790*n + 173057

def b8(n: int) -> int:
    return (
        3874492*n**8 + 59373972*n**7 + 394148190*n**6
        + 1481084196*n**5 + 3447878810*n**4 + 5095855458*n**3
        + 4673546679*n**2 + 2433871008*n + 551502039
    )

def b9(n: int) -> int:
    return (
        48802112*n**9 + 967468896*n**8 + 8488000862*n**7
        + 43246197636*n**6 + 140983768422*n**5 + 304912330849*n**4
        + 437406946975*n**3 + 401272692378*n**2
        + 213593890911*n + 50257929339
    )

def recurrence_coefficients(n: int) -> tuple[int, int, int, int]:
    return (
        (n + 1)**5 * (n + 2) * a0(n + 1),
        -2 * (n + 2) * b8(n),
        -2 * b9(n),
        2 * (n + 3)**5 * (2*n + 5) * a0(n),
    )

def fixed_tangent_residual(n: int) -> Q:
    c = recurrence_coefficients(n)
    return sum((Q(c[j]) * yhk(n + j) for j in range(4)), Q(0))

def qjson(q: Q) -> list[int]:
    return [q.numerator, q.denominator]

def mod_q(q: Q, prime: int) -> int:
    den = q.denominator % prime
    if den == 0:
        raise ZeroDivisionError(f"rational denominator vanishes modulo {prime}")
    return (q.numerator % prime) * pow(den, -1, prime) % prime

def stage_columns(degree: int) -> tuple[tuple[int, int], ...]:
    if not 0 <= degree <= MAX_DEGREE:
        raise AssertionError("degree outside declared ladder")
    cols = []
    for shift in range(4):
        for power in range(degree + 1):
            if degree == 9 and shift == 3 and power == 9:
                continue
            cols.append((shift, power))
    return tuple(cols)

def row_count(degree: int) -> int:
    return len(stage_columns(degree)) + EXTRA_ROWS

def stage_matrix(degree: int) -> tuple[list[list[int]], list[int], dict]:
    cols = stage_columns(degree)
    rows = []
    rhs = []
    denominator_checks = 0
    for n in range(row_count(degree)):
        row = [(y0(n + shift) % PRIME) * pow(n, power, PRIME) % PRIME
               for shift, power in cols]
        residual = fixed_tangent_residual(n)
        rhs.append(mod_q(-residual, PRIME))
        denominator_checks += 1
        rows.append(row)
    return rows, rhs, {
        "degree": degree,
        "coefficient_columns": [[j, m] for j, m in cols],
        "unknown_count": len(cols),
        "row_count": len(rows),
        "prime": PRIME,
        "rational_denominator_nonzero_mod_prime_checks": denominator_checks,
    }

def rank_mod(rows: list[list[int]], prime: int = PRIME) -> tuple[int, list[int]]:
    if not rows:
        return 0, []
    a = [[x % prime for x in row] for row in rows]
    m, n = len(a), len(a[0])
    r = 0
    pivots = []
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], -1, prime)
        a[r] = [(x * inv) % prime for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [(x - f*y) % prime for x, y in zip(a[i], a[r])]
        pivots.append(c)
        r += 1
        if r == m:
            break
    return r, pivots

def stage_result(degree: int) -> dict:
    matrix, rhs, meta = stage_matrix(degree)
    coeff_rank, coeff_pivots = rank_mod(matrix)
    augmented = [row + [value] for row, value in zip(matrix, rhs)]
    aug_rank, aug_pivots = rank_mod(augmented)
    exact_inconsistent = (
        coeff_rank == meta["unknown_count"]
        and aug_rank == meta["unknown_count"] + 1
    )
    meta.update({
        "coefficient_rank_mod_prime": coeff_rank,
        "augmented_rank_mod_prime": aug_rank,
        "coefficient_pivot_columns": coeff_pivots,
        "augmented_pivot_columns": aug_pivots,
        "exact_inconsistency_over_Q_certified": exact_inconsistent,
        "matrix_sha256": hashlib.sha256(
            json.dumps([matrix, rhs], separators=(",", ":")).encode()
        ).hexdigest(),
    })
    return meta

def build() -> dict:
    validate_scope()
    locks = source_locks()
    baseline_y = [yhk(i) for i in range(4)]
    if baseline_y != [Q(0), Q(16), Q(3564), Q(3214312, 3)]:
        raise AssertionError("H_k tangent baseline drift")
    obstruction = fixed_tangent_residual(0)
    if obstruction != Q(FIXED_OBSTRUCTION):
        raise AssertionError("fixed-operator tangent obstruction mismatch")

    stages = [stage_result(d) for d in range(MAX_DEGREE + 1)]
    all_negative = all(s["exact_inconsistency_over_Q_certified"] for s in stages)
    if all_negative:
        terminal = CLOSURE_TERMINAL
        blocker = None
    else:
        first = next(s for s in stages if not s["exact_inconsistency_over_Q_certified"])
        terminal = BLOCKER_TERMINAL
        blocker = {
            "kind": "DECLARED_STAGE_NOT_EXACTLY_EXCLUDED",
            "degree": first["degree"],
            "coefficient_rank_mod_prime": first["coefficient_rank_mod_prime"],
            "augmented_rank_mod_prime": first["augmented_rank_mod_prime"],
        }

    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "protected_intake": PROTECTED_INTAKE,
        "source_locks": locks,
        "tangent_direction": "H_k_1",
        "Y_Hk_0_through_3": [qjson(x) for x in baseline_y],
        "fixed_operator_tangent_obstruction_at_n0": qjson(obstruction),
        "fixed_operator_tangent_obstruction_nonzero": bool(obstruction),
        "operator_deformation": {
            "order": 3,
            "coefficient_field": "Q",
            "polynomial_degree_ladder": list(range(MAX_DEGREE + 1)),
            "gauge": "delta_c -> delta_c + q(n)*c; at degree 9 fix coeff(n^9,delta_c3)=0",
            "degree9_gauge_dimension_removed": 1,
            "rational_coefficient_family_admitted": False,
            "new_recurrence_order_admitted": False,
        },
        "rank_logic": (
            "full coefficient-column rank modulo p plus augmented rank one higher "
            "exhibits exact inconsistency over Q for the declared rational row system"
        ),
        "stages": stages,
        "terminal": terminal,
        "characterized_blocker": blocker,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
