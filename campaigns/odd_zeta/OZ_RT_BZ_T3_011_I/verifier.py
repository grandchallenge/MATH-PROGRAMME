from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
G_DIR = HERE.parent / "OZ_RT_BZ_T3_010"
if str(G_DIR) not in sys.path:
    sys.path.insert(0, str(G_DIR))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer
import verify_t3_011_g as vg

a = vg.a


def _assert_h_locks_independent() -> dict[str, str]:
    got = {}
    for name, want in producer.H_BLOBS.items():
        value = a.git_blob_sha1(producer.H_DIR / name)
        if value != want:
            raise AssertionError(
                f"independent T3-011-H source lock drift: {name}: {value} != {want}"
            )
        got[name] = value
    contract = json.loads((producer.H_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-H":
        raise AssertionError("independent T3-011-H contract operation drift")
    if contract.get("terminals", {}).get("closure") != producer.H_REQUIRED_TERMINAL:
        raise AssertionError("independent T3-011-H closure terminal drift")
    return got


def _invert_factor_independent(factor, label: str):
    sig, coeff = factor
    coeff = Q(coeff)
    if coeff == 0:
        raise AssertionError(f"{label} coordinate specialization is zero")
    inv = tuple(sorted((name, -int(exp)) for name, exp in reversed(sig) if exp))
    if not inv:
        raise AssertionError(
            f"{label} coordinate specialization is constant; reciprocal degree is not identifiable"
        )
    return inv, Q(1, 1) / coeff


def _inverse_factor_map(channel: str, strata: list[dict]) -> dict:
    forward = vg._factor_map(channel, strata)
    out = {}
    for sid in reversed(sorted(forward)):
        out[sid] = {
            kind: _invert_factor_independent(
                forward[sid][kind], f"{channel}:{sid}:{kind}"
            )
            for kind in ("x1", "x0")
        }
    return out


def _as_dict(sig) -> dict:
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
def _independent_inverse_bidegrees(base_sig, left_sig, right_sig, target_sig):
    base = _as_dict(base_sig)
    left_inv = _as_dict(left_sig)
    right_inv = _as_dict(right_sig)
    target = _as_dict(target_sig)
    if not left_inv or not right_inv:
        raise AssertionError("independent reciprocal coordinate specialization became constant")
    if any(exp > 0 for exp in left_inv.values()) or any(
        exp > 0 for exp in right_inv.values()
    ):
        raise AssertionError(
            "independent reciprocal coordinate specialization has positive Laurent step"
        )

    left = {factor: -exp for factor, exp in left_inv.items()}
    right = {factor: -exp for factor, exp in right_inv.items()}
    deficit = {
        factor: base.get(factor, 0) - target.get(factor, 0)
        for factor in set(base) | set(left) | set(right) | set(target)
    }
    if any(value < 0 for value in deficit.values()):
        return ()

    left_bounds = [
        deficit[factor] // exp for factor, exp in left.items() if exp > 0
    ]
    right_bounds = [
        deficit[factor] // exp for factor, exp in right.items() if exp > 0
    ]
    if not left_bounds or not right_bounds:
        raise AssertionError("independent finite reciprocal bidegree bound unavailable")

    out = []
    for s in range(min(right_bounds), -1, -1):
        for r in range(min(left_bounds), -1, -1):
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
    witness_index: dict,
    base_index: dict,
    left_inverse_factors: dict,
    left_kind: str,
    right_inverse_factors: dict,
    right_kind: str,
) -> dict:
    aggregate = {}
    possible = set()
    matches = []
    first = {}
    for key in sorted(set(witness_index) & set(base_index), key=repr, reverse=True):
        cell_id, scalar, mon = key
        sid = _stratum_id(cell_id)
        left_sig, left_coeff = left_inverse_factors[sid][left_kind]
        right_sig, right_coeff = right_inverse_factors[sid][right_kind]
        for target_sig, weight in reversed(witness_index[key]):
            for base_sig, coeff in reversed(base_index[key]):
                for r, s in _independent_inverse_bidegrees(
                    base_sig, left_sig, right_sig, target_sig
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
        "possible_bidegrees": [[r, s] for r, s in sorted(possible)],
        "nonzero_bidegrees": [[r, s] for r, s in sorted(aggregate)],
        "coefficient_rows": rows,
        "coefficient_sha256": producer.sha(rows),
        "match_count": len(matches),
        "match_sha256": producer.sha(matches),
        "first_evidence": {
            f"{r},{s}": first[(r, s)] for r, s in sorted(first)
        },
        "_aggregate": aggregate,
    }


def _direct_mixed_pairing(
    witness: dict, vec_gcd: dict, vec_gc: dict, vec_gd: dict, vec_g: dict
) -> Q:
    total = Q(0)
    for key, weight in reversed(list(witness.items())):
        total += Q(weight) * (
            Q(vec_gcd.get(key, 0))
            - Q(vec_gc.get(key, 0))
            - Q(vec_gd.get(key, 0))
            + Q(vec_g.get(key, 0))
        )
    return total


def _axis_rows(ledgers: dict, side: str) -> list[list[int]]:
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    if side == "left":
        degrees = sorted((r for r, s in domain if r >= 1 and s == 0), reverse=True)
        rows = []
        for r in reversed(degrees):
            value = (
                ledgers["ScSd"]["_aggregate"].get((r, 0), Q(0))
                - ledgers["Sc"]["_aggregate"].get((r, 0), Q(0))
                - ledgers["Sd"]["_aggregate"].get((r, 0), Q(0))
                + ledgers["I"]["_aggregate"].get((r, 0), Q(0))
            )
            rows.append([r, *producer.qjson(value)])
        return rows
    if side == "right":
        degrees = sorted((s for r, s in domain if r == 0 and s >= 1), reverse=True)
        rows = []
        for s in reversed(degrees):
            value = (
                ledgers["ScSd"]["_aggregate"].get((0, s), Q(0))
                - ledgers["Sc"]["_aggregate"].get((0, s), Q(0))
                - ledgers["Sd"]["_aggregate"].get((0, s), Q(0))
                + ledgers["I"]["_aggregate"].get((0, s), Q(0))
            )
            rows.append([s, *producer.qjson(value)])
        return rows
    raise AssertionError(f"independent unknown axis side: {side}")


def _candidate_key(candidate):
    return (candidate[0], tuple(candidate[1]))


def _h_record_index(h_result: dict):
    out = {}
    for rec in reversed(h_result["tested_records"]):
        key = (
            tuple(rec["pair"]),
            rec["endpoint"],
            _candidate_key(rec["candidate"]),
            rec["prefactor_channel"],
        )
        if key in out:
            raise AssertionError(f"independent duplicate H record: {key}")
        out[key] = rec
    return out


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
        poly = vg.semantic.direct_original_monomial(mon)
        for channel in shifts:
            poly = vg.vf._shift_poly_independent(poly, channel)
        poly_cache[poly_key] = poly
    vector_key = (endpoint, uid, tuple(shifts))
    cached = vector_cache.get(vector_key)
    if cached is None:
        vec = vg.semantic.direct_global_column_from_poly(
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
    witness_index,
    inverse_factors,
    h_index,
    poly_cache,
    vector_cache,
):
    left, right = pair
    vec_g, idx_g = _cached_vector_index(endpoint, uid, (), strata, bank, poly_cache, vector_cache)
    vec_gc, idx_gc = _cached_vector_index(endpoint, uid, (left,), strata, bank, poly_cache, vector_cache)
    vec_gd, idx_gd = _cached_vector_index(endpoint, uid, (right,), strata, bank, poly_cache, vector_cache)
    vec_gcd, idx_gcd = _cached_vector_index(endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache)

    left_factors = inverse_factors[left]
    right_factors = inverse_factors[right]
    ledgers = {
        "ScSd": _ledger(witness_index, idx_gcd, left_factors, "x1", right_factors, "x1"),
        "Sc": _ledger(witness_index, idx_gc, left_factors, "x1", right_factors, "x0"),
        "Sd": _ledger(witness_index, idx_gd, left_factors, "x0", right_factors, "x1"),
        "I": _ledger(witness_index, idx_g, left_factors, "x0", right_factors, "x0"),
    }

    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    mixed_domain = {(r, s) for r, s in domain if r >= 1 and s >= 1}

    rows = []
    nonzero = []
    for r, s in sorted(mixed_domain):
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

    component_zero = (
        ledgers["ScSd"]["_aggregate"].get((0, 0), Q(0))
        - ledgers["Sc"]["_aggregate"].get((0, 0), Q(0))
        - ledgers["Sd"]["_aggregate"].get((0, 0), Q(0))
        + ledgers["I"]["_aggregate"].get((0, 0), Q(0))
    )
    direct_zero = _direct_mixed_pairing(bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g)
    left_rows = _axis_rows(ledgers, "left")
    right_rows = _axis_rows(ledgers, "right")
    uid_key = (uid[0], tuple(uid[1]))
    left_h = h_index[(tuple(pair), endpoint, uid_key, left)]
    right_h = h_index[(tuple(pair), endpoint, uid_key, right)]
    left_anchor = left_rows == left_h["pairing_rows"]
    right_anchor = right_rows == right_h["pairing_rows"]
    direct_anchor = component_zero == direct_zero

    ambiguity = None
    if not direct_anchor:
        ambiguity = "DEGREE_0_0_COMPONENT_DECOMPOSITION_DISAGREES_WITH_DIRECT_MIXED_RESPONSE"
    elif not left_anchor:
        ambiguity = "LEFT_RECIPROCAL_AXIS_BOUNDARY_DISAGREES_WITH_T3_011_H"
    elif not right_anchor:
        ambiguity = "RIGHT_RECIPROCAL_AXIS_BOUNDARY_DISAGREES_WITH_T3_011_H"

    return {
        "finite_overlap_mixed_reciprocal_bidegrees": [[r, s] for r, s in sorted(mixed_domain)],
        "finite_overlap_sha256": producer.sha([[r, s] for r, s in sorted(mixed_domain)]),
        "component_ledgers": {
            name: {key: value for key, value in ledger.items() if not key.startswith("_")}
            for name, ledger in ledgers.items()
        },
        "pairing_rows": rows,
        "pairing_sha256": producer.sha(rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_bidegree": nonzero[0][:2] if nonzero else None,
        "degree_0_0_component_pairing": producer.qjson(component_zero),
        "degree_0_0_direct_pairing": producer.qjson(direct_zero),
        "degree_0_0_semantics_exactly_match_direct": direct_anchor,
        "left_axis_pairing_rows": left_rows,
        "left_H_pairing_rows": left_h["pairing_rows"],
        "left_axis_semantics_exactly_match_H": left_anchor,
        "right_axis_pairing_rows": right_rows,
        "right_H_pairing_rows": right_h["pairing_rows"],
        "right_axis_semantics_exactly_match_H": right_anchor,
        "semantic_ambiguity_kind": ambiguity,
        "all_mixed_reciprocal_bidegrees_annihilated": ambiguity is None and not nonzero,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("T3-011-I identity drift")
    producer.validate_scope()
    _assert_h_locks_independent()
    _independent_inverse_bidegrees.cache_clear()

    h_result = producer.h.build()
    if h_result.get("terminal") != producer.H_REQUIRED_TERMINAL:
        raise AssertionError("independent I requires exact protected H closure")
    if h_result.get("possible_record_count") != producer.H_EXPECTED_POSSIBLE_RECORDS:
        raise AssertionError("independent I H possible count drift")
    if h_result.get("tested_record_count") != producer.H_EXPECTED_TESTED_RECORDS:
        raise AssertionError("independent I H tested count drift")
    h_index = _h_record_index(h_result)

    strata, specialized, supports = vg.vf.vd.reconstruct_context()
    banks = vg.vf._reconstruct_banks(strata, specialized, supports)
    try:
        inverse_factors = {
            channel: _inverse_factor_map(channel, strata)
            for channel in producer.CHANNEL_COORDINATE
        }
    except AssertionError as exc:
        if result.get("terminal") != producer.BLOCKER_TERMINAL:
            raise
        if result.get("characterized_blocker") != str(exc):
            raise AssertionError("T3-011-I characterized blocker drift")
        return {
            "operation": producer.OPERATION,
            "status": "INDEPENDENT_T3_011_I_BLOCKER_REPLAY_COMPLETE",
            "characterized_blocker": str(exc),
            "terminal": producer.BLOCKER_TERMINAL,
        }

    if result.get("terminal") == producer.BLOCKER_TERMINAL:
        raise AssertionError("T3-011-I producer blocker was not reproduced independently")

    cls = result.get("mixed_reciprocal_class", {})
    if cls.get("monomial_domain") != "x_c^{-r}*x_d^{-s} with integers r>=1,s>=1":
        raise AssertionError("T3-011-I monomial domain drift")
    if cls.get("unordered_pair_order") != [list(pair) for pair in producer.ADMITTED_PAIRS]:
        raise AssertionError("T3-011-I pair order drift")
    if cls.get("only_poles") != ["x_c=0", "x_d=0"]:
        raise AssertionError("T3-011-I pole boundary drift")
    for required in (
        "nonzero_laurent_specialization_required",
        "finite_support_overlap_derived_without_degree_cutoff",
        "pure_reciprocal_axes_are_H_boundary_anchors",
        "degree_zero_is_direct_response_anchor",
    ):
        if cls.get(required) is not True:
            raise AssertionError(f"T3-011-I required boundary flag missing: {required}")
    for forbidden in (
        "shifted_poles_admitted",
        "positive_numerator_polynomials_admitted",
        "mixed_sign_laurent_monomials_admitted",
        "arbitrary_rational_functions_admitted",
        "support_or_harmonic_enlargement_admitted",
        "candidate_bank_or_scalar_namespace_widening_admitted",
        "recurrence_search_admitted",
        "correction_layer_work_admitted",
        "candidate_linear_combinations_admitted",
    ):
        if cls.get(forbidden):
            raise AssertionError(f"T3-011-I forbidden widening: {forbidden}")

    if result.get("possible_record_count") != producer.FROZEN_RECORD_COUNT:
        raise AssertionError("T3-011-I possible record count drift")
    emitted = result.get("tested_records", [])

    witness_indexes = {channel: _witness_index(bank["witness"]) for channel, bank in banks.items()}
    poly_cache = {}
    vector_cache = {}
    cursor = 0
    first_escape = None
    first_ambiguity = None
    stop = False

    for pair_index, pair in enumerate(producer.ADMITTED_PAIRS):
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            witness_index = witness_indexes[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                if cursor >= len(emitted):
                    raise AssertionError("T3-011-I producer stopped before terminal witness or exhaustion")
                rec = emitted[cursor]
                expected_identity = {
                    "ordinal": cursor,
                    "pair_index": pair_index,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                    "pair": list(pair),
                    "endpoint": endpoint,
                    "candidate": [uid[0], list(uid[1])],
                    "coordinate_pair": [producer.CHANNEL_COORDINATE[pair[0]], producer.CHANNEL_COORDINATE[pair[1]]],
                }
                for key, value in expected_identity.items():
                    if rec.get(key) != value:
                        raise AssertionError(f"T3-011-I deterministic record drift at {cursor}:{key}")

                alt = _independent_record(pair, endpoint, uid, strata, bank, witness_index, inverse_factors, h_index, poly_cache, vector_cache)
                for key, value in alt.items():
                    if rec.get(key) != value:
                        raise AssertionError(f"T3-011-I independent replay drift at {cursor}:{key}")

                cursor += 1
                if alt["semantic_ambiguity_kind"] is not None:
                    first_ambiguity = rec
                    stop = True
                    break
                if alt["nonzero_pairings"]:
                    r, s, num, den = alt["nonzero_pairings"][0]
                    first_escape = {
                        "ordinal": rec["ordinal"],
                        "pair": rec["pair"],
                        "endpoint": endpoint,
                        "candidate": rec["candidate"],
                        "reciprocal_bidegree": [r, s],
                        "normalized_cokernel_pairing": [num, den],
                    }
                    stop = True
                    break
            if stop:
                break
        if stop:
            break

    if cursor != len(emitted):
        raise AssertionError("T3-011-I emitted records extend past canonical terminal")

    if first_ambiguity is not None:
        terminal = producer.AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = producer.ESCAPE_TERMINAL
    else:
        if cursor != producer.FROZEN_RECORD_COUNT:
            raise AssertionError("T3-011-I independent exhaustive record drift")
        terminal = producer.CLOSURE_TERMINAL

    if result.get("semantic_functional_ambiguity") != first_ambiguity:
        raise AssertionError("T3-011-I semantic ambiguity drift")
    if result.get("first_cokernel_breaking_direction") != first_escape:
        raise AssertionError("T3-011-I first escape drift")
    if result.get("terminal") != terminal:
        raise AssertionError("T3-011-I terminal drift")
    if result.get("all_mixed_reciprocal_responses_cokernel_invisible") != (terminal == producer.CLOSURE_TERMINAL):
        raise AssertionError("T3-011-I closure flag drift")
    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("T3-011-I claim firewall drift")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-011-I proof/promotion firewall drift")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3-011-I T3 status drift")

    cache_info = _independent_inverse_bidegrees.cache_info()
    return {
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_T3_011_I_REPLAY_COMPLETE",
        "tested_record_count": cursor,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_mixed_reciprocal_responses_cokernel_invisible": terminal == producer.CLOSURE_TERMINAL,
        "execution_ledger": {
            "inverse_coordinate_factor_maps": len(inverse_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "bidegree_solver_cache_hits": cache_info.hits,
            "bidegree_solver_cache_misses": cache_info.misses,
        },
        "terminal": terminal,
    }


def main() -> int:
    print(json.dumps(verify(producer.build()), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
