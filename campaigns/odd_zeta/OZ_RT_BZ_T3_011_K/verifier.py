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


def _assert_predecessor_locks_independent() -> dict:
    out = {"J": {}, "G": {}}
    for name, want in producer.J_BLOBS.items():
        value = a.git_blob_sha1(producer.J_DIR / name)
        if value != want:
            raise AssertionError(
                f"independent T3-011-J source lock drift: {name}: {value} != {want}"
            )
        out["J"][name] = value
    j_contract = json.loads((producer.J_DIR / "CONTRACT.json").read_text())
    if j_contract.get("operation") != "OZ-RT-BZ-T3-011-J":
        raise AssertionError("independent T3-011-J contract operation drift")
    if j_contract.get("terminals", {}).get("closure") != producer.J_REQUIRED_TERMINAL:
        raise AssertionError("independent T3-011-J closure terminal drift")

    for name, want in producer.G_BLOBS.items():
        value = a.git_blob_sha1(producer.G_DIR / name)
        if value != want:
            raise AssertionError(
                f"independent T3-011-G source lock drift: {name}: {value} != {want}"
            )
        out["G"][name] = value
    g_contract = json.loads((producer.G_DIR / "T3_011_G_CONTRACT.json").read_text())
    if g_contract.get("operation") != "OZ-RT-BZ-T3-011-G":
        raise AssertionError("independent T3-011-G contract operation drift")
    if g_contract.get("terminals", {}).get("closure") != producer.G_REQUIRED_TERMINAL:
        raise AssertionError("independent T3-011-G closure terminal drift")
    return out


def _as_dict(sig) -> dict:
    return {factor: int(exp) for factor, exp in sig if exp}


def _positive_step(sig, label: str) -> dict:
    out = _as_dict(sig)
    if not out:
        raise AssertionError(f"{label} coordinate specialization became constant")
    if any(exp <= 0 for exp in out.values()):
        raise AssertionError(
            f"{label} coordinate specialization is not a positive Laurent direction"
        )
    return out


def _subtract(target_sig, step_sig, degree: int):
    out = _as_dict(target_sig)
    for factor, exp in reversed(step_sig):
        out[factor] = out.get(factor, 0) - degree * int(exp)
        if out[factor] < 0:
            return None
        if out[factor] == 0:
            del out[factor]
    return tuple(sorted(out.items()))


@lru_cache(maxsize=None)
def _independent_tridegrees(base_sig, left_sig, right_sig, spectator_sig, target_sig):
    base = _as_dict(base_sig)
    target = _as_dict(target_sig)
    left = _positive_step(left_sig, "independent left")
    right = _positive_step(right_sig, "independent right")
    spectator = _positive_step(spectator_sig, "independent spectator")
    factors = set(base) | set(target) | set(left) | set(right) | set(spectator)
    diff = {factor: target.get(factor, 0) - base.get(factor, 0) for factor in factors}
    if any(value < 0 for value in diff.values()):
        return ()
    bounds = [diff[factor] // exp for factor, exp in spectator.items() if exp > 0]
    if not bounds:
        raise AssertionError("independent finite spectator-degree bound unavailable")

    rows = []
    for t in range(min(bounds), -1, -1):
        reduced = _subtract(target_sig, spectator_sig, t)
        if reduced is None:
            continue
        for r, s in vg._independent_solutions(
            base_sig, left_sig, right_sig, reduced
        ):
            rows.append((r, s, t))
    return tuple(sorted(rows))


def _ledger(
    witness_index,
    base_index,
    left_factors,
    left_kind,
    right_factors,
    right_kind,
    spectator_factors,
):
    aggregate = {}
    possible = set()
    matches = []
    for key in sorted(set(witness_index) & set(base_index), key=repr, reverse=True):
        cell_id, scalar, mon = key
        sid = cell_id.split(":", 2)[2]
        left_sig, left_coeff = left_factors[sid][left_kind]
        right_sig, right_coeff = right_factors[sid][right_kind]
        spectator_sig, spectator_coeff = spectator_factors[sid]["x0"]
        for target_sig, weight in reversed(witness_index[key]):
            for base_sig, coeff in reversed(base_index[key]):
                for r, s, t in _independent_tridegrees(
                    base_sig, left_sig, right_sig, spectator_sig, target_sig
                ):
                    possible.add((r, s, t))
                    value = (
                        weight
                        * coeff
                        * (left_coeff ** r)
                        * (right_coeff ** s)
                        * (spectator_coeff ** t)
                    )
                    aggregate[(r, s, t)] = aggregate.get((r, s, t), Q(0)) + value
                    matches.append(
                        [
                            r,
                            s,
                            t,
                            cell_id,
                            scalar,
                            list(mon),
                            producer.qjson(weight),
                            producer.qjson(coeff),
                            producer.qjson(value),
                        ]
                    )
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [
        [r, s, t, *producer.qjson(aggregate[(r, s, t)])]
        for r, s, t in sorted(aggregate)
    ]
    return {
        "possible_tridegrees": [[r, s, t] for r, s, t in sorted(possible)],
        "nonzero_tridegrees": [[r, s, t] for r, s, t in sorted(aggregate)],
        "coefficient_rows": rows,
        "coefficient_sha256": producer.sha(rows),
        "match_count": len(matches),
        "match_sha256": producer.sha(sorted(matches, key=repr)),
        "_aggregate": aggregate,
    }


def _cached_vector_index(
    endpoint, uid, shifts, strata, bank, poly_cache, vector_cache
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
        cached = (vec, vg._base_index(vec))
        vector_cache[vector_key] = cached
    return cached


def _witness_index(witness):
    return vg._witness_index(witness)


def _pairing_rows(ledgers, degrees):
    rows = []
    for degree in sorted(degrees):
        value = (
            ledgers["ScSd"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sc"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sd"]["_aggregate"].get(degree, Q(0))
            + ledgers["I"]["_aggregate"].get(degree, Q(0))
        )
        rows.append([*degree, *producer.qjson(value)])
    return rows


def _bivariate_rows(
    witness_index,
    idx_gcd,
    idx_gc,
    idx_gd,
    idx_g,
    left_factors,
    right_factors,
):
    ledgers = {
        "ScSd": vg._ledger(
            witness_index, idx_gcd, left_factors, "x1", right_factors, "x1"
        ),
        "Sc": vg._ledger(
            witness_index, idx_gc, left_factors, "x1", right_factors, "x0"
        ),
        "Sd": vg._ledger(
            witness_index, idx_gd, left_factors, "x0", right_factors, "x1"
        ),
        "I": vg._ledger(
            witness_index, idx_g, left_factors, "x0", right_factors, "x0"
        ),
    }
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_multidegrees"]))
    domain = {(r, s) for r, s in domain if r >= 1 and s >= 1}
    rows = []
    for r, s in sorted(domain):
        value = (
            ledgers["ScSd"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sc"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sd"]["_aggregate"].get((r, s), Q(0))
            + ledgers["I"]["_aggregate"].get((r, s), Q(0))
        )
        rows.append([r, s, *producer.qjson(value)])
    return rows


def _direct_pairing(witness, vec_gcd, vec_gc, vec_gd, vec_g):
    total = Q(0)
    for key, weight in reversed(list(witness.items())):
        total += Q(weight) * (
            Q(vec_gcd.get(key, 0))
            - Q(vec_gc.get(key, 0))
            - Q(vec_gd.get(key, 0))
            + Q(vec_g.get(key, 0))
        )
    return total


def _spectator(pair):
    left_axis = producer.CHANNEL_COORDINATE[pair[0]]
    right_axis = producer.CHANNEL_COORDINATE[pair[1]]
    remaining = {"n", "k", "l"} - {left_axis, right_axis}
    if len(remaining) != 1:
        raise AssertionError(f"independent pair does not determine spectator: {pair}")
    axis = sorted(remaining)[0]
    return axis, producer.CANONICAL_SPECTATOR_CHANNEL[axis]


def _independent_record(
    pair,
    endpoint,
    uid,
    strata,
    bank,
    witness_index,
    coordinate_factors,
    poly_cache,
    vector_cache,
):
    left, right = pair
    spectator_axis, spectator_channel = _spectator(pair)
    left_factors = coordinate_factors[left]
    right_factors = coordinate_factors[right]
    spectator_factors = coordinate_factors[spectator_channel]

    vec_g, idx_g = _cached_vector_index(
        endpoint, uid, (), strata, bank, poly_cache, vector_cache
    )
    vec_gc, idx_gc = _cached_vector_index(
        endpoint, uid, (left,), strata, bank, poly_cache, vector_cache
    )
    vec_gd, idx_gd = _cached_vector_index(
        endpoint, uid, (right,), strata, bank, poly_cache, vector_cache
    )
    vec_gcd, idx_gcd = _cached_vector_index(
        endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache
    )

    ledgers = {
        "ScSd": _ledger(
            witness_index, idx_gcd, left_factors, "x1", right_factors, "x1", spectator_factors
        ),
        "Sc": _ledger(
            witness_index, idx_gc, left_factors, "x1", right_factors, "x0", spectator_factors
        ),
        "Sd": _ledger(
            witness_index, idx_gd, left_factors, "x0", right_factors, "x1", spectator_factors
        ),
        "I": _ledger(
            witness_index, idx_g, left_factors, "x0", right_factors, "x0", spectator_factors
        ),
    }
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
    t0 = {(r, s, 0) for r, s, t in domain if t == 0 and r >= 1 and s >= 1}
    mixed = {(r, s, t) for r, s, t in domain if r >= 1 and s >= 1 and t >= 1}

    t0_rows_raw = _pairing_rows(ledgers, t0)
    t0_rows = [[r, s, num, den] for r, s, _t, num, den in t0_rows_raw]
    g_rows = _bivariate_rows(
        witness_index, idx_gcd, idx_gc, idx_gd, idx_g, left_factors, right_factors
    )
    boundary_match = t0_rows == g_rows
    rows = _pairing_rows(ledgers, mixed)
    nonzero = [row for row in rows if row[-2] != 0]

    component_zero = (
        ledgers["ScSd"]["_aggregate"].get((0, 0, 0), Q(0))
        - ledgers["Sc"]["_aggregate"].get((0, 0, 0), Q(0))
        - ledgers["Sd"]["_aggregate"].get((0, 0, 0), Q(0))
        + ledgers["I"]["_aggregate"].get((0, 0, 0), Q(0))
    )
    direct_zero = _direct_pairing(bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g)
    direct_match = component_zero == direct_zero

    ambiguity = None
    if not direct_match:
        ambiguity = "DEGREE_0_0_0_COMPONENT_DECOMPOSITION_DISAGREES_WITH_DIRECT_MIXED_RESPONSE"
    elif not boundary_match:
        ambiguity = "T_ZERO_BOUNDARY_DISAGREES_WITH_T3_011_G_FACTOR_SEMANTICS"
    elif any(row[-2] != 0 for row in g_rows):
        ambiguity = "PROTECTED_T3_011_G_BOUNDARY_RECONSTRUCTION_IS_NONZERO"

    return {
        "coordinate_pair": [
            producer.CHANNEL_COORDINATE[left],
            producer.CHANNEL_COORDINATE[right],
        ],
        "spectator_axis": spectator_axis,
        "spectator_channel_representative": spectator_channel,
        "finite_overlap_tridegrees": [[r, s, t] for r, s, t in sorted(mixed)],
        "finite_overlap_sha256": producer.sha(
            [[r, s, t] for r, s, t in sorted(mixed)]
        ),
        "component_ledgers": {
            name: {
                key: value for key, value in ledger.items() if not key.startswith("_")
            }
            for name, ledger in ledgers.items()
        },
        "pairing_rows": rows,
        "pairing_sha256": producer.sha(rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_tridegree": nonzero[0][:3] if nonzero else None,
        "t_zero_boundary_rows": t0_rows,
        "protected_G_boundary_rows": g_rows,
        "t_zero_semantics_exactly_match_G": boundary_match
        and not any(row[-2] != 0 for row in g_rows),
        "degree_0_0_0_component_pairing": producer.qjson(component_zero),
        "degree_0_0_0_direct_pairing": producer.qjson(direct_zero),
        "degree_0_0_0_semantics_exactly_match_direct": direct_match,
        "semantic_ambiguity_kind": ambiguity,
        "all_trivariate_spectator_degrees_annihilated": ambiguity is None and not nonzero,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("T3-011-K identity drift")
    producer.validate_scope()
    locks = _assert_predecessor_locks_independent()
    if result.get("predecessor_checkpoint", {}).get("source_blobs") != locks:
        raise AssertionError("T3-011-K predecessor source lock ledger drift")

    _independent_tridegrees.cache_clear()
    vg._independent_solutions.cache_clear()

    strata, specialized, supports = vg.vf.vd.reconstruct_context()
    banks = vg.vf._reconstruct_banks(strata, specialized, supports)
    try:
        coordinate_factors = {
            channel: vg._factor_map(channel, strata)
            for channel in producer.CHANNEL_COORDINATE
        }
        for channel, factor_map in coordinate_factors.items():
            for sid, kinds in factor_map.items():
                for kind, (sig, _coeff) in kinds.items():
                    _positive_step(sig, f"independent {channel}:{sid}:{kind}")
    except AssertionError as exc:
        if result.get("terminal") != producer.BLOCKER_TERMINAL:
            raise
        if result.get("characterized_blocker") != str(exc):
            raise AssertionError("T3-011-K characterized blocker drift")
        return {
            "operation": producer.OPERATION,
            "status": "INDEPENDENT_T3_011_K_BLOCKER_REPLAY_COMPLETE",
            "characterized_blocker": str(exc),
            "terminal": producer.BLOCKER_TERMINAL,
        }

    if result.get("terminal") == producer.BLOCKER_TERMINAL:
        raise AssertionError("T3-011-K producer blocker was not reproduced independently")

    cls = result.get("trivariate_spectator_class", {})
    if cls.get("monomial_domain") != (
        "x_c^r*x_d^s*x_e^t with integers r>=1,s>=1,t>=1"
    ):
        raise AssertionError("T3-011-K monomial domain drift")
    if cls.get("unordered_pair_order") != [
        list(pair) for pair in producer.ADMITTED_PAIRS
    ]:
        raise AssertionError("T3-011-K pair order drift")
    for required in (
        "spectator_is_unshifted",
        "finite_support_overlap_derived_without_degree_cutoff",
        "t_zero_boundary_matches_protected_G",
    ):
        if cls.get(required) is not True:
            raise AssertionError(f"T3-011-K required boundary flag missing: {required}")
    for forbidden in (
        "reciprocal_spectator_admitted",
        "shifted_spectator_admitted",
        "shifted_poles_admitted",
        "arbitrary_rational_functions_admitted",
        "support_or_harmonic_enlargement_admitted",
        "candidate_bank_or_scalar_namespace_widening_admitted",
        "recurrence_search_admitted",
        "correction_layer_work_admitted",
        "candidate_linear_combinations_admitted",
        "third_finite_difference_operator_admitted",
    ):
        if cls.get(forbidden):
            raise AssertionError(f"T3-011-K forbidden widening: {forbidden}")

    if result.get("possible_record_count") != producer.FROZEN_RECORD_COUNT:
        raise AssertionError("T3-011-K possible record count drift")

    emitted = result.get("tested_records", [])
    witness_indexes = {
        channel: _witness_index(bank["witness"]) for channel, bank in banks.items()
    }
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
                    raise AssertionError(
                        "T3-011-K producer stopped before terminal witness or exhaustion"
                    )
                rec = emitted[cursor]
                identity = {
                    "ordinal": cursor,
                    "pair_index": pair_index,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                    "pair": list(pair),
                    "endpoint": endpoint,
                    "candidate": [uid[0], list(uid[1])],
                }
                for key, value in identity.items():
                    if rec.get(key) != value:
                        raise AssertionError(
                            f"T3-011-K deterministic record drift at {cursor}:{key}"
                        )
                alt = _independent_record(
                    pair,
                    endpoint,
                    uid,
                    strata,
                    bank,
                    witness_index,
                    coordinate_factors,
                    poly_cache,
                    vector_cache,
                )
                for key, value in alt.items():
                    if rec.get(key) != value:
                        raise AssertionError(
                            f"T3-011-K independent replay drift at {cursor}:{key}"
                        )
                cursor += 1
                if alt["semantic_ambiguity_kind"] is not None:
                    first_ambiguity = rec
                    stop = True
                    break
                if alt["nonzero_pairings"]:
                    r, s, t, num, den = alt["nonzero_pairings"][0]
                    first_escape = {
                        "ordinal": rec["ordinal"],
                        "pair": rec["pair"],
                        "endpoint": endpoint,
                        "candidate": rec["candidate"],
                        "spectator_axis": rec["spectator_axis"],
                        "tridegree": [r, s, t],
                        "normalized_cokernel_pairing": [num, den],
                    }
                    stop = True
                    break
            if stop:
                break
        if stop:
            break

    if cursor != len(emitted):
        raise AssertionError("T3-011-K emitted records extend past canonical terminal")

    if first_ambiguity is not None:
        terminal = producer.AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = producer.ESCAPE_TERMINAL
    else:
        if cursor != producer.FROZEN_RECORD_COUNT:
            raise AssertionError("T3-011-K independent exhaustive record drift")
        terminal = producer.CLOSURE_TERMINAL

    if result.get("semantic_functional_ambiguity") != first_ambiguity:
        raise AssertionError("T3-011-K semantic ambiguity drift")
    if result.get("first_cokernel_breaking_direction") != first_escape:
        raise AssertionError("T3-011-K first escape drift")
    if result.get("terminal") != terminal:
        raise AssertionError("T3-011-K terminal drift")
    if result.get("all_trivariate_spectator_responses_cokernel_invisible") != (
        terminal == producer.CLOSURE_TERMINAL
    ):
        raise AssertionError("T3-011-K closure flag drift")
    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("T3-011-K claim firewall drift")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-011-K proof/promotion firewall drift")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3-011-K T3 status drift")

    tri_cache = _independent_tridegrees.cache_info()
    bi_cache = vg._independent_solutions.cache_info()
    return {
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_T3_011_K_REPLAY_COMPLETE",
        "tested_record_count": cursor,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_trivariate_spectator_responses_cokernel_invisible": (
            terminal == producer.CLOSURE_TERMINAL
        ),
        "execution_ledger": {
            "coordinate_factor_maps": len(coordinate_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "tridegree_solver_cache_hits": tri_cache.hits,
            "tridegree_solver_cache_misses": tri_cache.misses,
            "bivariate_boundary_solver_cache_hits": bi_cache.hits,
            "bivariate_boundary_solver_cache_misses": bi_cache.misses,
        },
        "terminal": terminal,
    }
