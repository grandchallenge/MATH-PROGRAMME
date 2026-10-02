from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_e as e
import t3_011_f as f

semantic = f.semantic
p = f.p
c = f.c
a = f.a

OPERATION = "OZ-RT-BZ-T3-011-G"
STAGE = "T3_011_G_MIXED_POLYNOMIAL_COKERNEL_CLOSURE_AUDIT"
ISSUE = 906
F_REVIEWED_HEAD = "bc67c0e6b3b2e521569339798d879f4a3a4448bf"
F_MERGE_COMMIT = "81296b7cce3c741597ae86e991cb59e2d1835fcb"
F_REQUIRED_TERMINAL = "MIXED_CHANNEL_QUADRATIC_RESPONSE_CLASS_COKERNEL_INVISIBLE"
F_EXPECTED_RECORDS = 1282
F_BLOBS = {
    "t3_011_f.py": "8141fff1332a91ac50bdf3f9eb2751a7be0ba87f",
    "T3_011_F_CONTRACT.json": "e9a7ae84e2a0fc89cd2d15240e73b257e070cb3c",
    "verify_t3_011_f.py": "02a68736024ee5812bac10398dd98c44dff30d63",
}
ADMITTED_PAIRS = tuple(f.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(f.CHANNEL_COORDINATE)
CLOSURE_TERMINAL = "MIXED_POLYNOMIAL_MULTIPLIER_COKERNEL_CLOSURE_CERTIFIED"
FINITE_TERMINAL = "MIXED_POLYNOMIAL_CLOSURE_REDUCES_TO_FINITE_MULTIDEGREE_SET"
AMBIGUITY_TERMINAL = "MIXED_POLYNOMIAL_CLOSURE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
BLOCKER_TERMINAL = "MIXED_POLYNOMIAL_CLOSURE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def assert_f_locks() -> dict[str, str]:
    got = {}
    for name, want in F_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"T3-011-F source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_011_F_CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-F":
        raise AssertionError("T3-011-F contract operation drift")
    if contract.get("terminals", {}).get("negative") != F_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-F terminal drift")
    return got


def validate_scope(
    pairs=ADMITTED_PAIRS,
    min_left_degree: int = 1,
    min_right_degree: int = 1,
    arbitrary_degree_cutoff: int | None = None,
    pure_axis_terms: bool = False,
    same_coordinate_pairs: bool = False,
    support_enlargement: bool = False,
    rational_prefactors: bool = False,
    recurrence_widening: bool = False,
    correction_recombination: bool = False,
    candidate_linear_combinations: bool = False,
) -> None:
    pairs = tuple(tuple(x) for x in pairs)
    if pairs != ADMITTED_PAIRS:
        raise AssertionError("T3-011-G admitted pair order drift")
    if min_left_degree != 1 or min_right_degree != 1:
        raise AssertionError("T3-011-G admits exactly the genuinely mixed quadrant r,s>=1")
    if arbitrary_degree_cutoff is not None:
        raise AssertionError("T3-011-G forbids arbitrary degree cutoffs")
    if pure_axis_terms:
        raise AssertionError("T3-011-G pure-axis terms are E-closed and excluded")
    if same_coordinate_pairs:
        raise AssertionError("T3-011-G same-coordinate pairs are E-reducible and excluded")
    if support_enlargement or rational_prefactors or recurrence_widening:
        raise AssertionError("T3-011-G forbidden search-class widening")
    if correction_recombination or candidate_linear_combinations:
        raise AssertionError("T3-011-G forbidden correction/candidate recombination")
    for left, right in pairs:
        if CHANNEL_COORDINATE[left] == CHANNEL_COORDINATE[right]:
            raise AssertionError("T3-011-G requires distinct coordinate axes")


def _sig_dict(sig) -> dict:
    return {factor: int(exp) for factor, exp in sig if exp}


def _combine_sig(base_sig, left_sig, right_sig, r: int, s: int):
    powers = _sig_dict(base_sig)
    for factor, exp in left_sig:
        powers[factor] = powers.get(factor, 0) + r * int(exp)
        if not powers[factor]:
            del powers[factor]
    for factor, exp in right_sig:
        powers[factor] = powers.get(factor, 0) + s * int(exp)
        if not powers[factor]:
            del powers[factor]
    return tuple(sorted(powers.items()))


@lru_cache(maxsize=None)
def _solve_multidegrees(base_sig, left_sig, right_sig, target_sig) -> tuple[tuple[int, int], ...]:
    base = _sig_dict(base_sig)
    left = _sig_dict(left_sig)
    right = _sig_dict(right_sig)
    target = _sig_dict(target_sig)
    for label, step in (("left", left), ("right", right)):
        if not step:
            raise AssertionError(f"{label} coordinate specialization became constant")
        if any(exp < 0 for exp in step.values()):
            raise AssertionError(f"{label} coordinate specialization has negative Laurent power")
    diffs = {
        factor: target.get(factor, 0) - base.get(factor, 0)
        for factor in set(base) | set(left) | set(right) | set(target)
    }
    if any(diff < 0 for diff in diffs.values()):
        return ()

    def upper(step: dict) -> int:
        bounds = [diffs[factor] // exp for factor, exp in step.items() if exp > 0]
        if not bounds:
            raise AssertionError("coordinate specialization has no positive exponent")
        return min(bounds)

    rmax = upper(left)
    smax = upper(right)
    out = []
    for r in range(rmax + 1):
        for s in range(smax + 1):
            if _combine_sig(base_sig, left_sig, right_sig, r, s) == target_sig:
                out.append((r, s))
    return tuple(out)


def _base_index(vec: dict):
    out = {}
    for (cell_id, coord), coeff in vec.items():
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(coeff)))
    return out


def _witness_index(witness: dict):
    out = {}
    for (cell_id, coord), weight in witness.items():
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(weight)))
    return out


def _stratum_id(cell_id: str) -> str:
    return cell_id.split(":", 2)[2]


def bivariate_moment_ledger(
    witness_index: dict,
    base_index: dict,
    left_factors: dict,
    left_kind: str,
    right_factors: dict,
    right_kind: str,
) -> dict:
    aggregate: dict[tuple[int, int], Q] = {}
    possible: set[tuple[int, int]] = set()
    matches = []
    first_evidence = {}
    for base_key in sorted(set(witness_index) & set(base_index), key=repr):
        cell_id, scalar, mon = base_key
        sid = _stratum_id(cell_id)
        left_sig, left_coeff = left_factors[sid][left_kind]
        right_sig, right_coeff = right_factors[sid][right_kind]
        for target_sig, weight in witness_index[base_key]:
            for base_sig, coeff in base_index[base_key]:
                for r, s in _solve_multidegrees(base_sig, left_sig, right_sig, target_sig):
                    possible.add((r, s))
                    contribution = weight * coeff * (left_coeff ** r) * (right_coeff ** s)
                    aggregate[(r, s)] = aggregate.get((r, s), Q(0)) + contribution
                    row = [
                        r,
                        s,
                        cell_id,
                        scalar,
                        list(mon),
                        qjson(weight),
                        qjson(coeff),
                        qjson(contribution),
                    ]
                    matches.append(row)
                    first_evidence.setdefault((r, s), row)
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [[r, s, *qjson(aggregate[(r, s)])] for r, s in sorted(aggregate)]
    return {
        "possible_multidegrees": [[r, s] for r, s in sorted(possible)],
        "nonzero_multidegrees": [[r, s] for r, s in sorted(aggregate)],
        "coefficient_rows": rows,
        "coefficient_sha256": sha(rows),
        "match_count": len(matches),
        "match_sha256": sha(matches),
        "first_evidence": {
            f"{r},{s}": first_evidence[(r, s)] for r, s in sorted(first_evidence)
        },
        "_aggregate": aggregate,
    }


def _strip_internal(ledger: dict) -> dict:
    return {key: value for key, value in ledger.items() if not key.startswith("_")}


def _cached_vector_index(
    endpoint,
    uid,
    shifts,
    strata,
    bank,
    poly_cache,
    vector_cache,
):
    scalar, mon = uid
    poly_key = (mon, tuple(shifts))
    poly = poly_cache.get(poly_key)
    if poly is None:
        poly = semantic.direct_original_monomial(mon)
        for channel in shifts:
            poly = f.shift_poly(poly, channel)
        poly_cache[poly_key] = poly
    vector_key = (endpoint, uid, tuple(shifts))
    cached = vector_cache.get(vector_key)
    if cached is None:
        vec = semantic.direct_global_column_from_poly(
            poly, scalar, endpoint, strata, bank["active"]
        )
        cached = (vec, _base_index(vec))
        vector_cache[vector_key] = cached
    return cached


def _candidate_record(
    pair,
    endpoint,
    uid,
    strata,
    bank,
    f_record,
    witness_index,
    left_factors,
    right_factors,
    poly_cache,
    vector_cache,
):
    left, right = pair
    _vec_g, idx_g = _cached_vector_index(
        endpoint, uid, (), strata, bank, poly_cache, vector_cache
    )
    _vec_gc, idx_gc = _cached_vector_index(
        endpoint, uid, (left,), strata, bank, poly_cache, vector_cache
    )
    _vec_gd, idx_gd = _cached_vector_index(
        endpoint, uid, (right,), strata, bank, poly_cache, vector_cache
    )
    _vec_gcd, idx_gcd = _cached_vector_index(
        endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache
    )

    A = bivariate_moment_ledger(
        witness_index, idx_gcd, left_factors, "x1", right_factors, "x1"
    )
    B = bivariate_moment_ledger(
        witness_index, idx_gc, left_factors, "x1", right_factors, "x0"
    )
    C = bivariate_moment_ledger(
        witness_index, idx_gd, left_factors, "x0", right_factors, "x1"
    )
    D = bivariate_moment_ledger(
        witness_index, idx_g, left_factors, "x0", right_factors, "x0"
    )

    domain = (
        set(map(tuple, A["possible_multidegrees"]))
        | set(map(tuple, B["possible_multidegrees"]))
        | set(map(tuple, C["possible_multidegrees"]))
        | set(map(tuple, D["possible_multidegrees"]))
    )
    domain = {degree for degree in domain if degree[0] >= 1 and degree[1] >= 1}
    pairing_rows = []
    nonzero = []
    for r, s in sorted(domain):
        value = (
            A["_aggregate"].get((r, s), Q(0))
            - B["_aggregate"].get((r, s), Q(0))
            - C["_aggregate"].get((r, s), Q(0))
            + D["_aggregate"].get((r, s), Q(0))
        )
        pairing_rows.append([r, s, *qjson(value)])
        if value:
            nonzero.append([r, s, *qjson(value)])

    lambda_11 = next(
        (Q(num, den) for r, s, num, den in pairing_rows if (r, s) == (1, 1)),
        Q(0),
    )
    f_pair = Q(*f_record["normalized_cokernel_pairing"])
    semantic_match = lambda_11 == f_pair
    ambiguity = None if semantic_match else "DEGREE_1_1_PAIRING_DISAGREES_WITH_T3_011_F"

    return {
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "coordinate_pair": [CHANNEL_COORDINATE[left], CHANNEL_COORDINATE[right]],
        "finite_overlap_multidegrees": [[r, s] for r, s in sorted(domain)],
        "finite_overlap_sha256": sha([[r, s] for r, s in sorted(domain)]),
        "component_ledgers": {
            "ScSd": _strip_internal(A),
            "Sc": _strip_internal(B),
            "Sd": _strip_internal(C),
            "I": _strip_internal(D),
        },
        "pairing_rows": pairing_rows,
        "pairing_sha256": sha(pairing_rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_multidegree": nonzero[0][:2] if nonzero else None,
        "degree_1_1_pairing": qjson(lambda_11),
        "f_degree_1_1_pairing": f_record["normalized_cokernel_pairing"],
        "degree_1_1_semantics_exactly_match_f": semantic_match,
        "semantic_ambiguity_kind": ambiguity,
        "all_genuinely_mixed_monomial_degrees_annihilated": semantic_match and not nonzero,
    }


def build() -> dict:
    validate_scope()
    _solve_multidegrees.cache_clear()
    f_locks = assert_f_locks()
    predecessor = f.build()
    if predecessor.get("terminal") != F_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-G requires exact negative F terminal")
    if predecessor.get("tested_record_count") != F_EXPECTED_RECORDS:
        raise AssertionError("T3-011-G F record count drift")
    if predecessor.get("first_semantic_functional_ambiguity") is not None:
        raise AssertionError("T3-011-G requires F semantic ambiguity NONE")
    if predecessor.get("first_cokernel_breaking_direction") is not None:
        raise AssertionError("T3-011-G requires F cokernel-breaking direction NONE")

    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    f_records = predecessor["tested_records"]
    coordinate_factors = {
        channel: e._coordinate_factors(channel, strata)
        for channel in CHANNEL_COORDINATE
    }
    witness_indexes = {
        channel: _witness_index(bank["witness"])
        for channel, bank in banks.items()
    }
    poly_cache = {}
    vector_cache = {}

    records = []
    global_residue: set[tuple[int, int]] = set()
    first_residue = None
    first_ambiguity = None
    cursor = 0
    for pair_index, pair in enumerate(ADMITTED_PAIRS):
        left, right = pair
        left_factors = coordinate_factors[left]
        right_factors = coordinate_factors[right]
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            witness_index = witness_indexes[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                f_record = f_records[cursor]
                expected_identity = (list(pair), endpoint, unknown_json(uid))
                actual_identity = (
                    f_record.get("pair"),
                    f_record.get("endpoint"),
                    f_record.get("candidate"),
                )
                if actual_identity != expected_identity:
                    raise AssertionError(f"T3-011-G F deterministic record drift at {cursor}")
                rec = _candidate_record(
                    pair,
                    endpoint,
                    uid,
                    strata,
                    bank,
                    f_record,
                    witness_index,
                    left_factors,
                    right_factors,
                    poly_cache,
                    vector_cache,
                )
                rec.update(
                    {
                        "ordinal": cursor,
                        "pair_index": pair_index,
                        "endpoint_index": endpoint_index,
                        "candidate_index": candidate_index,
                    }
                )
                records.append(rec)
                if first_ambiguity is None and rec["semantic_ambiguity_kind"] is not None:
                    first_ambiguity = rec
                for r, s, _num, _den in rec["nonzero_pairings"]:
                    global_residue.add((r, s))
                    if first_residue is None:
                        first_residue = {
                            "pair": list(pair),
                            "endpoint": endpoint,
                            "candidate": rec["candidate"],
                            "multidegree": [r, s],
                        }
                cursor += 1

    if cursor != F_EXPECTED_RECORDS:
        raise AssertionError("T3-011-G exhaustive candidate traversal drift")

    if first_ambiguity is not None:
        terminal = AMBIGUITY_TERMINAL
    elif global_residue:
        terminal = FINITE_TERMINAL
    else:
        terminal = CLOSURE_TERMINAL

    cache_info = _solve_multidegrees.cache_info()
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "MIXED_POLYNOMIAL_COKERNEL_CLOSURE_AUDIT_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": F_REVIEWED_HEAD,
            "merge_commit": F_MERGE_COMMIT,
            "source_blobs": f_locks,
            "required_terminal": F_REQUIRED_TERMINAL,
            "tested_record_count": predecessor["tested_record_count"],
            "first_semantic_functional_ambiguity": predecessor[
                "first_semantic_functional_ambiguity"
            ],
            "first_cokernel_breaking_direction": predecessor[
                "first_cokernel_breaking_direction"
            ],
        },
        "mixed_polynomial_class": {
            "unordered_pair_order": [list(pair) for pair in ADMITTED_PAIRS],
            "monomial_domain": "x_c^r*x_d^s with integers r>=1,s>=1",
            "pure_axes_excluded_as_E_closed": True,
            "same_coordinate_pairs_excluded_as_E_reducible": True,
            "endpoint_anchored_candidate_banks": True,
            "finite_support_overlap_derived_without_degree_cutoff": True,
            "arbitrary_finite_bivariate_polynomials_follow_only_by_linearity_after_monomial_closure": True,
            "support_or_harmonic_enlargement_admitted": False,
            "rational_prefactors_admitted": False,
            "recurrence_search_admitted": False,
            "correction_layer_work_admitted": False,
            "candidate_linear_combinations_admitted": False,
        },
        "execution_ledger": {
            "coordinate_factor_maps": len(coordinate_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "multidegree_solver_cache_hits": cache_info.hits,
            "multidegree_solver_cache_misses": cache_info.misses,
        },
        "candidate_record_count": len(records),
        "candidate_records": records,
        "semantic_functional_ambiguity": first_ambiguity,
        "finite_nonzero_multidegree_residue": [
            [r, s] for r, s in sorted(global_residue)
        ],
        "first_nonzero_multidegree_witness": first_residue,
        "all_mixed_polynomial_multipliers_cokernel_invisible": terminal == CLOSURE_TERMINAL,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }


def main() -> int:
    print(json.dumps(build(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
