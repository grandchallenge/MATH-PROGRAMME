from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_g as producer
import verify_t3_011_f as vf

semantic = vf.semantic
a = vf.a
p = producer.p


def _assert_f_locks_independent() -> dict[str, str]:
    got = {}
    for name, want in producer.F_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"independent F source lock drift: {name}: {value} != {want}")
        got[name] = value
    return got


def _single_rat_monomial(rat, label: str):
    if len(rat) != 1:
        raise AssertionError(f"independent {label} is not a single Laurent monomial")
    (sig, coeff), = rat.items()
    coeff = Q(coeff)
    if not coeff:
        raise AssertionError(f"independent {label} specialized to zero")
    return sig, coeff


def _factor_map(channel: str, strata: list[dict]):
    x0_factor, x1_factor = p.channel_coordinate_factors(channel)
    out = {}
    for st in reversed(strata):
        x0 = a.specialize_rat(
            a.rc.r_factor(x0_factor, exponent=1),
            st["k_offset"],
            st["l_offset"],
        )
        x1 = a.specialize_rat(
            a.rc.r_factor(x1_factor, exponent=1),
            st["k_offset"],
            st["l_offset"],
        )
        out[st["id"]] = {
            "x0": _single_rat_monomial(x0, f"{channel}:{st['id']}:x0"),
            "x1": _single_rat_monomial(x1, f"{channel}:{st['id']}:x1"),
        }
    return out


def _as_dict(sig):
    return {factor: int(exp) for factor, exp in sig if exp}


def _compose(base_sig, left_sig, right_sig, r: int, s: int):
    out = _as_dict(base_sig)
    for factor, exp in reversed(left_sig):
        out[factor] = out.get(factor, 0) + r * int(exp)
        if out[factor] == 0:
            del out[factor]
    for factor, exp in reversed(right_sig):
        out[factor] = out.get(factor, 0) + s * int(exp)
        if out[factor] == 0:
            del out[factor]
    return tuple(sorted(out.items()))


@lru_cache(maxsize=None)
def _independent_solutions(base_sig, left_sig, right_sig, target_sig):
    base = _as_dict(base_sig)
    left = _as_dict(left_sig)
    right = _as_dict(right_sig)
    target = _as_dict(target_sig)
    if not left or not right:
        raise AssertionError("independent coordinate specialization became constant")
    if any(v < 0 for v in left.values()) or any(v < 0 for v in right.values()):
        raise AssertionError("independent coordinate specialization has negative Laurent power")
    factors = set(base) | set(left) | set(right) | set(target)
    diff = {
        factor: target.get(factor, 0) - base.get(factor, 0)
        for factor in factors
    }
    if any(value < 0 for value in diff.values()):
        return ()
    rbounds = [diff[factor] // exp for factor, exp in left.items() if exp]
    sbounds = [diff[factor] // exp for factor, exp in right.items() if exp]
    if not rbounds or not sbounds:
        raise AssertionError("independent finite multidegree bound unavailable")
    out = []
    for s in range(min(sbounds), -1, -1):
        for r in range(min(rbounds), -1, -1):
            if _compose(base_sig, left_sig, right_sig, r, s) == target_sig:
                out.append((r, s))
    return tuple(sorted(out))


def _base_index(vec: dict):
    out = {}
    for (cell_id, coord), coeff in reversed(list(vec.items())):
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(coeff)))
    return out


def _witness_index(witness: dict):
    out = {}
    for (cell_id, coord), weight in reversed(list(witness.items())):
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(weight)))
    return out


def _stratum_id(cell_id: str) -> str:
    return cell_id.split(":", 2)[2]


def _ledger(
    witness_index,
    base_index,
    left_factors,
    left_kind,
    right_factors,
    right_kind,
):
    aggregate = {}
    possible = set()
    matches = []
    first = {}
    for key in sorted(set(witness_index) & set(base_index), key=repr, reverse=True):
        cell_id, scalar, mon = key
        sid = _stratum_id(cell_id)
        left_sig, left_coeff = left_factors[sid][left_kind]
        right_sig, right_coeff = right_factors[sid][right_kind]
        for target_sig, weight in reversed(witness_index[key]):
            for base_sig, coeff in reversed(base_index[key]):
                for r, s in _independent_solutions(
                    base_sig,
                    left_sig,
                    right_sig,
                    target_sig,
                ):
                    possible.add((r, s))
                    value = weight * coeff * (left_coeff ** r) * (right_coeff ** s)
                    aggregate[(r, s)] = aggregate.get((r, s), Q(0)) + value
                    row = [
                        r,
                        s,
                        cell_id,
                        scalar,
                        list(mon),
                        producer.qjson(weight),
                        producer.qjson(coeff),
                        producer.qjson(value),
                    ]
                    matches.append(row)
                    first.setdefault((r, s), row)
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [
        [r, s, *producer.qjson(aggregate[(r, s)])]
        for r, s in sorted(aggregate)
    ]
    return {
        "possible_multidegrees": [[r, s] for r, s in sorted(possible)],
        "nonzero_multidegrees": [[r, s] for r, s in sorted(aggregate)],
        "coefficient_rows": rows,
        "coefficient_sha256": producer.sha(rows),
        "match_count": len(matches),
        "match_sha256": producer.sha(matches),
        "first_evidence": {
            f"{r},{s}": first[(r, s)] for r, s in sorted(first)
        },
        "_aggregate": aggregate,
    }


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
            poly = vf._shift_poly_independent(poly, channel)
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


def _independent_record(
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

    ledgers = {
        "ScSd": _ledger(witness_index, idx_gcd, left_factors, "x1", right_factors, "x1"),
        "Sc": _ledger(witness_index, idx_gc, left_factors, "x1", right_factors, "x0"),
        "Sd": _ledger(witness_index, idx_gd, left_factors, "x0", right_factors, "x1"),
        "I": _ledger(witness_index, idx_g, left_factors, "x0", right_factors, "x0"),
    }
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_multidegrees"]))
    domain = {
        degree for degree in domain if degree[0] >= 1 and degree[1] >= 1
    }
    rows = []
    nonzero = []
    for r, s in sorted(domain):
        value = (
            ledgers["ScSd"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sc"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sd"]["_aggregate"].get((r, s), Q(0))
            + ledgers["I"]["_aggregate"].get((r, s), Q(0))
        )
        row = [r, s, *producer.qjson(value)]
        rows.append(row)
        if value:
            nonzero.append(row)
    lambda_11 = next(
        (Q(num, den) for r, s, num, den in rows if (r, s) == (1, 1)),
        Q(0),
    )
    f_pair = Q(*f_record["normalized_cokernel_pairing"])
    return {
        "finite_overlap_multidegrees": [[r, s] for r, s in sorted(domain)],
        "finite_overlap_sha256": producer.sha(
            [[r, s] for r, s in sorted(domain)]
        ),
        "component_ledgers": {
            name: {
                key: value
                for key, value in ledger.items()
                if not key.startswith("_")
            }
            for name, ledger in ledgers.items()
        },
        "pairing_rows": rows,
        "pairing_sha256": producer.sha(rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_multidegree": nonzero[0][:2] if nonzero else None,
        "degree_1_1_pairing": producer.qjson(lambda_11),
        "f_degree_1_1_pairing": f_record["normalized_cokernel_pairing"],
        "degree_1_1_semantics_exactly_match_f": lambda_11 == f_pair,
        "semantic_ambiguity_kind": (
            None
            if lambda_11 == f_pair
            else "DEGREE_1_1_PAIRING_DISAGREES_WITH_T3_011_F"
        ),
        "all_genuinely_mixed_monomial_degrees_annihilated": (
            lambda_11 == f_pair and not nonzero
        ),
    }


def verify(result: dict) -> dict:
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("T3-011-G identity drift")
    producer.validate_scope()
    _assert_f_locks_independent()
    _independent_solutions.cache_clear()

    f_result = producer.f.build()
    f_replay = vf.verify(f_result)
    if f_replay.get("terminal") != producer.F_REQUIRED_TERMINAL:
        raise AssertionError("independent G requires exact negative F replay")
    if f_replay.get("tested_record_count") != producer.F_EXPECTED_RECORDS:
        raise AssertionError("independent G F replay cardinality drift")

    cls = result.get("mixed_polynomial_class", {})
    if cls.get("monomial_domain") != "x_c^r*x_d^s with integers r>=1,s>=1":
        raise AssertionError("T3-011-G monomial domain drift")
    if cls.get("unordered_pair_order") != [
        list(pair) for pair in producer.ADMITTED_PAIRS
    ]:
        raise AssertionError("T3-011-G pair order drift")
    if cls.get("finite_support_overlap_derived_without_degree_cutoff") is not True:
        raise AssertionError("T3-011-G finite-support proof-route flag missing")
    for forbidden in (
        "support_or_harmonic_enlargement_admitted",
        "rational_prefactors_admitted",
        "recurrence_search_admitted",
        "correction_layer_work_admitted",
        "candidate_linear_combinations_admitted",
    ):
        if cls.get(forbidden):
            raise AssertionError(f"T3-011-G forbidden widening: {forbidden}")

    strata, specialized, supports = vf.vd.reconstruct_context()
    banks = vf._reconstruct_banks(strata, specialized, supports)
    f_records = f_result["tested_records"]
    emitted = result.get("candidate_records", [])
    if len(emitted) != producer.F_EXPECTED_RECORDS:
        raise AssertionError("T3-011-G emitted candidate cardinality drift")

    coordinate_factors = {
        channel: _factor_map(channel, strata)
        for channel in producer.CHANNEL_COORDINATE
    }
    witness_indexes = {
        channel: _witness_index(bank["witness"])
        for channel, bank in banks.items()
    }
    poly_cache = {}
    vector_cache = {}

    global_residue = set()
    first_residue = None
    first_ambiguity = None
    cursor = 0
    for pair_index, pair in enumerate(producer.ADMITTED_PAIRS):
        left, right = pair
        left_factors = coordinate_factors[left]
        right_factors = coordinate_factors[right]
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            witness_index = witness_indexes[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                rec = emitted[cursor]
                expected_identity = {
                    "ordinal": cursor,
                    "pair_index": pair_index,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                    "pair": list(pair),
                    "endpoint": endpoint,
                    "candidate": [uid[0], list(uid[1])],
                }
                for key, value in expected_identity.items():
                    if rec.get(key) != value:
                        raise AssertionError(
                            f"T3-011-G deterministic record drift at {cursor}:{key}"
                        )
                alt = _independent_record(
                    pair,
                    endpoint,
                    uid,
                    strata,
                    bank,
                    f_records[cursor],
                    witness_index,
                    left_factors,
                    right_factors,
                    poly_cache,
                    vector_cache,
                )
                for key, value in alt.items():
                    if rec.get(key) != value:
                        raise AssertionError(
                            f"T3-011-G independent replay drift at {cursor}:{key}"
                        )
                if (
                    first_ambiguity is None
                    and alt["semantic_ambiguity_kind"] is not None
                ):
                    first_ambiguity = rec
                for r, s, _num, _den in alt["nonzero_pairings"]:
                    global_residue.add((r, s))
                    if first_residue is None:
                        first_residue = {
                            "pair": list(pair),
                            "endpoint": endpoint,
                            "candidate": rec["candidate"],
                            "multidegree": [r, s],
                        }
                cursor += 1

    residue = [[r, s] for r, s in sorted(global_residue)]
    if result.get("finite_nonzero_multidegree_residue") != residue:
        raise AssertionError("T3-011-G global finite residue drift")
    if result.get("first_nonzero_multidegree_witness") != first_residue:
        raise AssertionError("T3-011-G first residue witness drift")
    if result.get("semantic_functional_ambiguity") != first_ambiguity:
        raise AssertionError("T3-011-G semantic ambiguity drift")

    if first_ambiguity is not None:
        terminal = producer.AMBIGUITY_TERMINAL
    elif residue:
        terminal = producer.FINITE_TERMINAL
    else:
        terminal = producer.CLOSURE_TERMINAL
    if result.get("terminal") != terminal:
        raise AssertionError("T3-011-G terminal drift")
    if result.get("all_mixed_polynomial_multipliers_cokernel_invisible") != (
        terminal == producer.CLOSURE_TERMINAL
    ):
        raise AssertionError("T3-011-G closure flag drift")
    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("T3-011-G claim firewall drift")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-011-G proof/promotion firewall drift")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3-011-G T3 status drift")

    cache_info = _independent_solutions.cache_info()
    return {
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_T3_011_G_REPLAY_COMPLETE",
        "candidate_record_count": cursor,
        "finite_nonzero_multidegree_residue": residue,
        "semantic_functional_ambiguity": first_ambiguity,
        "all_mixed_polynomial_multipliers_cokernel_invisible": (
            terminal == producer.CLOSURE_TERMINAL
        ),
        "execution_ledger": {
            "coordinate_factor_maps": len(coordinate_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "multidegree_solver_cache_hits": cache_info.hits,
            "multidegree_solver_cache_misses": cache_info.misses,
        },
        "terminal": terminal,
    }


def main() -> int:
    print(
        json.dumps(
            verify(producer.build()),
            sort_keys=True,
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
