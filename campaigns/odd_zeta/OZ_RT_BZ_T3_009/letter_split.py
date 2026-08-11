#!/usr/bin/env python3
from __future__ import annotations

import json
from fractions import Fraction
from functools import lru_cache
from math import comb

# Representatives after exact k<->l symmetry at the sequence level.
ORBIT_REPRESENTATIVES = [
    ("k",1), ("kl",1), ("nk",1), ("nmk",1), ("nkl",1),
    ("k",2), ("kl",2), ("nk",2), ("nkl",2),
    ("k",3), ("nk",3),
    ("k",4), ("nk",4),
]

WEIGHT_BLOCKS = {
    "weight1": ["H_k_1", "H_kl_1", "H_nk_1", "H_nmk_1", "H_nkl_1"],
    "weight2": ["H_k_2", "H_kl_2", "H_nk_2", "H_nkl_2"],
    "weight3": ["H_k_3", "H_nk_3"],
    "weight4": ["H_k_4", "H_nk_4"],
}


@lru_cache(maxsize=None)
def harmonic(m: int, r: int) -> Fraction:
    return sum((Fraction(1, j**r) for j in range(1, m + 1)), Fraction(0))


@lru_cache(maxsize=None)
def kernel(n: int, k: int, l: int) -> int:
    return (
        comb(n + k, n) * comb(n, k) ** 2
        * comb(n + l, n) * comb(n, l) ** 2
        * comb(n + k + l, n)
    )


@lru_cache(maxsize=None)
def recurrence_coefficients(n: int) -> tuple[int, int, int, int]:
    a0 = lambda x: 41218*x**3 + 198849*x**2 + 320790*x + 173057
    b8 = lambda x: (
        3874492*x**8 + 59373972*x**7 + 394148190*x**6 + 1481084196*x**5
        + 3447878810*x**4 + 5095855458*x**3 + 4673546679*x**2
        + 2433871008*x + 551502039
    )
    b9 = lambda x: (
        48802112*x**9 + 967468896*x**8 + 8488000862*x**7 + 43246197636*x**6
        + 140983768422*x**5 + 304912330849*x**4 + 437406946975*x**3
        + 401272692378*x**2 + 213593890911*x + 50257929339
    )
    return (
        (n + 1)**5 * (n + 2) * a0(n + 1),
        -2 * (n + 2) * b8(n),
        -2 * b9(n),
        2 * (n + 3)**5 * (2*n + 5) * a0(n),
    )


def letter_value(n: int, k: int, l: int, family: str, r: int) -> Fraction:
    m = {
        "k": k,
        "kl": k + l,
        "nk": n + k,
        "nmk": n - k,
        "nkl": n + k + l,
    }[family]
    return harmonic(m, r)


@lru_cache(maxsize=None)
def sequence(n: int, family: str, r: int) -> Fraction:
    total = Fraction(0)
    for k in range(n + 1):
        for l in range(n + 1):
            total += kernel(n, k, l) * letter_value(n, k, l, family, r)
    return total


@lru_cache(maxsize=None)
def defect(n: int, family: str, r: int) -> Fraction:
    return sum(
        Fraction(c) * sequence(n + j, family, r)
        for j, c in enumerate(recurrence_coefficients(n))
    )


def rref_rank(rows: list[list[Fraction]]) -> int:
    a = [row[:] for row in rows]
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][c]
        a[r] = [x/q for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [x-q*y for x,y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r


def result() -> dict:
    rows = [
        [defect(n, family, r) for family, r in ORBIT_REPRESENTATIVES]
        for n in range(13)
    ]
    rank = rref_rank(rows)
    assert rank == 12
    candidate = [-3,-1,1,2,1] + [0]*8
    candidate_samples = [sum(Fraction(a)*x for a,x in zip(candidate,row)) for row in rows]
    assert all(x == 0 for x in candidate_samples)
    return {
        "operation": "OZ-RT-BZ-T3-009",
        "route": "DIRECT_T3_DISCRETE_RESIDUAL_CERT_001",
        "subroute": "STRUCTURED_ONE_BODY_LETTER_SPLIT_HOLONOMIC_001",
        "status": "ONE_BODY_SYMMETRY_QUOTIENT_AND_WEIGHT_BLOCKS_CONSTRUCTED",
        "input_atom_count": 22,
        "k_l_symmetry_orbit_representative_count": 13,
        "weight_blocks": WEIGHT_BLOCKS,
        "diagnostic_defect_matrix": {
            "rows_n": list(range(13)),
            "columns": [f"H_{f}_{r}" for f,r in ORBIT_REPRESENTATIVES],
            "exact_rank_over_Q": rank,
            "rank_is_lower_bound_on_functional_defect_dimension": True,
            "finite_samples_used_as_global_zero_proof": False,
        },
        "unique_sampled_null_direction": {
            "coordinates_first_five_weight1_columns": candidate[:5],
            "expression": "-3*H_k_1-H_kl_1+H_nk_1+2*H_nmk_1+H_nkl_1",
            "identification": "partial_k log(T)",
            "sampled_defect_zero_n_0_through_12": True,
            "global_zero_not_claimed_from_sampling": True,
        },
        "search_order": ["weight1", "weight2", "weight3", "weight4"],
        "certificate_architecture": "Use the reverified regularized Q-row fluxes as the base. For each small harmonic-letter block, exploit rational shift increments of its letters and solve only the correction flux needed to cancel the resulting rational residual; preserve k<->l symmetry. Do not reopen the exhausted generic 198-dimensional raw-jet ansatz.",
        "first_lane": "WEIGHT1_FIVE_ORBIT_SEPARATED_LETTER_CERT_001",
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


if __name__ == "__main__":
    print(json.dumps(result(), indent=2, sort_keys=True))
