from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from math import gcd
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


def _assert_i_locks_independent() -> dict[str, str]:
    got = {}
    for name, want in producer.I_BLOBS.items():
        value = a.git_blob_sha1(producer.I_DIR / name)
        if value != want:
            raise AssertionError(
                f"independent T3-011-I source lock drift: {name}: {value} != {want}"
            )
        got[name] = value
    contract = json.loads((producer.I_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-I":
        raise AssertionError("independent T3-011-I contract operation drift")
    if contract.get("terminals", {}).get("closure") != producer.I_REQUIRED_TERMINAL:
        raise AssertionError("independent T3-011-I closure terminal drift")
    return got


def _invert_factor_independent(factor, label: str):
    sig, coeff = factor
    coeff = Q(coeff)
    if coeff == 0:
        raise AssertionError(f"{label} coordinate specialization is zero")
    inv = tuple(sorted((name, -int(exp)) for name, exp in reversed(sig) if exp))
    if not inv:
        raise AssertionError(
            f"{label} coordinate specialization is constant; Laurent degree is not identifiable"
        )
    return inv, Q(1, 1) / coeff


def _forward_factor_map(channel: str, strata: list[dict]) -> dict:
    return vg._factor_map(channel, strata)


def _inverse_factor_map(channel: str, strata: list[dict]) -> dict:
    forward = _forward_factor_map(channel, strata)
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


def _signature_sign(sig) -> int:
    vals = [int(exp) for _factor, exp in sig if exp]
    if not vals:
        raise AssertionError("independent coordinate specialization became constant")
    if min(vals) > 0:
        return 1
    if max(vals) < 0:
        return -1
    raise AssertionError("independent coordinate specialization has mixed Laurent sign")


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


def _ceil_div(a: int, b: int) -> int:
    if b <= 0:
        raise AssertionError("independent positive divisor required")
    return -((-a) // b)


@lru_cache(maxsize=None)
def _independent_mixed_sign_solutions(base_sig, left_sig, right_sig, target_sig):
    left_sign = _signature_sign(left_sig)
    right_sign = _signature_sign(right_sig)
    if left_sign == right_sign:
        raise AssertionError("independent J requires opposite Laurent signs")

    base = _as_dict(base_sig)
    target = _as_dict(target_sig)
    if left_sign > 0:
        pos = _as_dict(left_sig)
        neg = {name: -exp for name, exp in _as_dict(right_sig).items()}
        positive_is_left = True
    else:
        pos = _as_dict(right_sig)
        neg = {name: -exp for name, exp in _as_dict(left_sig).items()}
        positive_is_left = False

    factors = sorted(set(base) | set(target) | set(pos) | set(neg))
    delta = {name: target.get(name, 0) - base.get(name, 0) for name in factors}

    pivot = None
    for ix, u in enumerate(factors):
        for v in factors[ix + 1 :]:
            det = pos.get(v, 0) * neg.get(u, 0) - pos.get(u, 0) * neg.get(v, 0)
            if det:
                pivot = (u, v, det)
                break
        if pivot:
            break
    if pivot:
        u, v, det = pivot
        r_num = delta[v] * neg.get(u, 0) - delta[u] * neg.get(v, 0)
        s_num = pos.get(u, 0) * delta[v] - pos.get(v, 0) * delta[u]
        if r_num % det or s_num % det:
            return ("finite", ())
        rp = r_num // det
        sp = s_num // det
        if rp < 0 or sp < 0:
            return ("finite", ())
        if any(
            pos.get(name, 0) * rp - neg.get(name, 0) * sp != delta[name]
            for name in factors
        ):
            return ("finite", ())
        degree = (rp, sp) if positive_is_left else (sp, rp)
        if _compose(base_sig, left_sig, right_sig, *degree) != target_sig:
            raise AssertionError("independent rank-two reconstruction drift")
        return ("finite", (degree,))

    reference = next((name for name in factors if pos.get(name, 0) > 0), None)
    if reference is None:
        raise AssertionError("independent positive Laurent direction vanished")
    ar = pos[reference]
    br = neg.get(reference, 0)
    if br <= 0:
        return ("finite", ())
    dr = delta[reference]
    for name in factors:
        if delta[name] * ar != dr * pos.get(name, 0):
            return ("finite", ())

    divisor = gcd(ar, br)
    if dr % divisor:
        return ("finite", ())

    period_r = br // divisor
    period_s = ar // divisor
    residue = None
    for trial in range(period_r):
        numerator = ar * trial - dr
        if numerator % br == 0:
            residue = trial
            break
    if residue is None:
        raise AssertionError("independent rank-one residue search drift")
    s0 = (ar * residue - dr) // br
    t0 = max(0, _ceil_div(-s0, period_s))
    rp = residue + period_r * t0
    sp = s0 + period_s * t0
    if any(
        pos.get(name, 0) * rp - neg.get(name, 0) * sp != delta[name]
        for name in factors
    ):
        raise AssertionError("independent rank-one base reconstruction drift")

    base_degree = (rp, sp) if positive_is_left else (sp, rp)
    direction = (period_r, period_s) if positive_is_left else (period_s, period_r)
    if _compose(base_sig, left_sig, right_sig, *base_degree) != target_sig:
        raise AssertionError("independent unbounded base signature drift")
    next_degree = (base_degree[0] + direction[0], base_degree[1] + direction[1])
    if _compose(base_sig, left_sig, right_sig, *next_degree) != target_sig:
        raise AssertionError("independent unbounded direction signature drift")
    return ("unbounded", (base_degree, direction))


def _base_index(vec: dict) -> dict:
    out = {}
    for (cell_id, coord), coeff in reversed(list(vec.items())):
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(coeff)))
    return out


def _witness_index(witness: dict) -> dict:
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
    left_factors: dict,
    left_kind: str,
    right_factors: dict,
    right_kind: str,
    context: dict,
) -> dict:
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
                status, payload = _independent_mixed_sign_solutions(
                    base_sig, left_sig, right_sig, target_sig
                )
                if status == "unbounded":
                    base_degree, direction = payload
                    raise producer.UnboundedSignatureOverlap(
                        {
                            **context,
                            "cell_id": cell_id,
                            "stratum_id": sid,
                            "scalar": scalar,
                            "monomial": list(mon),
                            "base_signature": [list(item) for item in base_sig],
                            "target_signature": [list(item) for item in target_sig],
                            "left_step_signature": [list(item) for item in left_sig],
                            "right_step_signature": [list(item) for item in right_sig],
                            "first_nonnegative_bidegree": list(base_degree),
                            "unbounded_bidegree_direction": list(direction),
                            "mixed_admissible_family_exists": True,
                        }
                    )
                for r, s in payload:
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
        cached = (vec, _base_index(vec))
        vector_cache[vector_key] = cached
    return cached


def _direct_pairing(witness, vec_gcd, vec_gc, vec_gd, vec_g) -> Q:
    total = Q(0)
    for key, weight in reversed(list(witness.items())):
        total += Q(weight) * (
            Q(vec_gcd.get(key, 0))
            - Q(vec_gc.get(key, 0))
            - Q(vec_gd.get(key, 0))
            + Q(vec_g.get(key, 0))
        )
    return total


def _axis_rows(ledgers: dict, axis: str) -> list[list[int]]:
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    if axis == "left":
        degrees = [
            (r, 0) for r in sorted(r for r, s in domain if r >= 1 and s == 0)
        ]
    elif axis == "right":
        degrees = [
            (0, s) for s in sorted(s for r, s in domain if r == 0 and s >= 1)
        ]
    else:
        raise AssertionError(f"independent unknown axis {axis}")
    rows = []
    for r, s in degrees:
        value = (
            ledgers["ScSd"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sc"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sd"]["_aggregate"].get((r, s), Q(0))
            + ledgers["I"]["_aggregate"].get((r, s), Q(0))
        )
        rows.append([r if axis == "left" else s, *producer.qjson(value)])
    return rows


def _independent_record(
    pair,
    endpoint,
    uid,
    orientation,
    strata,
    bank,
    witness_index,
    forward_factors,
    inverse_factors,
    poly_cache,
    vector_cache,
):
    left, right = pair
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

    if orientation == "positive_left_negative_right":
        left_maps, right_maps = forward_factors[left], inverse_factors[right]
        monomial_domain = "x_c^r*x_d^{-s}"
        positive_axis, reciprocal_axis = "left", "right"
    elif orientation == "negative_left_positive_right":
        left_maps, right_maps = inverse_factors[left], forward_factors[right]
        monomial_domain = "x_c^{-r}*x_d^s"
        positive_axis, reciprocal_axis = "right", "left"
    else:
        raise AssertionError("independent mixed-sign orientation drift")

    ledgers = {}
    for name, base_index, left_kind, right_kind in (
        ("ScSd", idx_gcd, "x1", "x1"),
        ("Sc", idx_gc, "x1", "x0"),
        ("Sd", idx_gd, "x0", "x1"),
        ("I", idx_g, "x0", "x0"),
    ):
        ledgers[name] = _ledger(
            witness_index,
            base_index,
            left_maps,
            left_kind,
            right_maps,
            right_kind,
            {
                "pair": list(pair),
                "endpoint": endpoint,
                "candidate": [uid[0], list(uid[1])],
                "orientation": orientation,
                "monomial_domain": monomial_domain,
                "component": name,
            },
        )

    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    mixed = {(r, s) for r, s in domain if r >= 1 and s >= 1}
    rows, nonzero = [], []
    for r, s in sorted(mixed):
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
    direct_zero = _direct_pairing(
        bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g
    )
    direct_anchor = component_zero == direct_zero
    left_rows = _axis_rows(ledgers, "left")
    right_rows = _axis_rows(ledgers, "right")
    pos_rows = left_rows if positive_axis == "left" else right_rows
    inv_rows = left_rows if reciprocal_axis == "left" else right_rows
    pos_anchor = all(num == 0 for _deg, num, _den in pos_rows)
    inv_anchor = all(num == 0 for _deg, num, _den in inv_rows)

    ambiguity = None
    if not direct_anchor:
        ambiguity = "DEGREE_0_0_COMPONENT_DECOMPOSITION_DISAGREES_WITH_DIRECT_MIXED_RESPONSE"
    elif not pos_anchor:
        ambiguity = "POSITIVE_AXIS_BOUNDARY_DISAGREES_WITH_PROTECTED_POLYNOMIAL_CLOSURE"
    elif not inv_anchor:
        ambiguity = "RECIPROCAL_AXIS_BOUNDARY_DISAGREES_WITH_T3_011_H"

    return {
        "finite_overlap_mixed_sign_bidegrees": [[r, s] for r, s in sorted(mixed)],
        "finite_overlap_sha256": producer.sha(
            [[r, s] for r, s in sorted(mixed)]
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
        "first_nonzero_bidegree": nonzero[0][:2] if nonzero else None,
        "degree_0_0_component_pairing": producer.qjson(component_zero),
        "degree_0_0_direct_pairing": producer.qjson(direct_zero),
        "degree_0_0_semantics_exactly_match_direct": direct_anchor,
        "left_axis_pairing_rows": left_rows,
        "right_axis_pairing_rows": right_rows,
        "positive_axis_boundary_annihilated": pos_anchor,
        "reciprocal_axis_boundary_annihilated": inv_anchor,
        "semantic_ambiguity_kind": ambiguity,
        "all_mixed_sign_bidegrees_annihilated": ambiguity is None and not nonzero,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("T3-011-J identity drift")
    producer.validate_scope()
    _assert_i_locks_independent()
    _independent_mixed_sign_solutions.cache_clear()

    pred = producer.i.build()
    if pred.get("terminal") != producer.I_REQUIRED_TERMINAL:
        raise AssertionError("independent J requires exact protected I closure")
    if pred.get("possible_record_count") != producer.I_EXPECTED_RECORDS:
        raise AssertionError("independent J I possible count drift")
    if pred.get("tested_record_count") != producer.I_EXPECTED_RECORDS:
        raise AssertionError("independent J I tested count drift")

    strata, specialized, supports = vg.vf.vd.reconstruct_context()
    banks = vg.vf._reconstruct_banks(strata, specialized, supports)
    try:
        forward = {
            channel: _forward_factor_map(channel, strata)
            for channel in producer.CHANNEL_COORDINATE
        }
        inverse = {
            channel: _inverse_factor_map(channel, strata)
            for channel in producer.CHANNEL_COORDINATE
        }
    except AssertionError as exc:
        if result.get("terminal") != producer.BLOCKER_TERMINAL:
            raise
        expected = {"kind": "COORDINATE_FACTOR_BLOCKER", "detail": str(exc)}
        if result.get("characterized_blocker") != expected:
            raise AssertionError("T3-011-J coordinate-factor blocker drift")
        return {
            "operation": producer.OPERATION,
            "status": "INDEPENDENT_T3_011_J_BLOCKER_REPLAY_COMPLETE",
            "characterized_blocker": expected,
            "terminal": producer.BLOCKER_TERMINAL,
        }

    if result.get("terminal") == producer.BLOCKER_TERMINAL:
        raise AssertionError(
            "T3-011-J producer blocker was not independently reproduced"
        )

    cls = result.get("mixed_sign_laurent_class", {})
    if cls.get("orientation_order") != list(producer.ORIENTATIONS):
        raise AssertionError("T3-011-J orientation order drift")
    if cls.get("unordered_pair_order") != [
        list(pair) for pair in producer.ADMITTED_PAIRS
    ]:
        raise AssertionError("T3-011-J pair order drift")
    if cls.get("only_poles") != ["x_c=0", "x_d=0"]:
        raise AssertionError("T3-011-J pole boundary drift")
    for flag in (
        "unbounded_signature_overlap_is_explicit_blocker",
        "positive_axis_boundaries_require_protected_polynomial_closure",
        "reciprocal_axis_boundaries_require_T3_011_H_closure",
        "negative_negative_quadrant_is_T3_011_I_closed",
    ):
        if cls.get(flag) is not True:
            raise AssertionError(f"T3-011-J required boundary flag missing: {flag}")
    for flag in (
        "shifted_poles_admitted",
        "arbitrary_rational_functions_admitted",
        "support_or_harmonic_enlargement_admitted",
        "candidate_bank_or_scalar_namespace_widening_admitted",
        "recurrence_search_admitted",
        "correction_layer_work_admitted",
        "candidate_linear_combinations_admitted",
        "trivariate_spectator_multipliers_admitted",
    ):
        if cls.get(flag):
            raise AssertionError(f"T3-011-J forbidden widening: {flag}")

    if result.get("possible_record_count") != producer.POSSIBLE_RECORD_COUNT:
        raise AssertionError("T3-011-J possible record count drift")

    emitted = result.get("tested_records", [])
    witness_indexes = {
        channel: _witness_index(bank["witness"])
        for channel, bank in banks.items()
    }
    poly_cache, vector_cache = {}, {}
    cursor = 0
    first_escape = None
    first_ambiguity = None
    first_unbounded = None
    stop = False

    for pair_index, pair in enumerate(producer.ADMITTED_PAIRS):
        for orientation_index, orientation in enumerate(producer.ORIENTATIONS):
            for endpoint_index, endpoint in enumerate(pair):
                bank = banks[endpoint]
                witness_index = witness_indexes[endpoint]
                for candidate_index, uid in enumerate(bank["candidates"]):
                    try:
                        alt = _independent_record(
                            pair,
                            endpoint,
                            uid,
                            orientation,
                            strata,
                            bank,
                            witness_index,
                            forward,
                            inverse,
                            poly_cache,
                            vector_cache,
                        )
                    except producer.UnboundedSignatureOverlap as exc:
                        first_unbounded = {
                            "ordinal": cursor,
                            "pair_index": pair_index,
                            "orientation_index": orientation_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                            **exc.evidence,
                        }
                        stop = True
                        break

                    if cursor >= len(emitted):
                        raise AssertionError(
                            "T3-011-J producer stopped before terminal witness or exhaustion"
                        )
                    rec = emitted[cursor]
                    expected_identity = {
                        "ordinal": cursor,
                        "pair_index": pair_index,
                        "orientation_index": orientation_index,
                        "endpoint_index": endpoint_index,
                        "candidate_index": candidate_index,
                        "pair": list(pair),
                        "endpoint": endpoint,
                        "candidate": [uid[0], list(uid[1])],
                        "coordinate_pair": [
                            producer.CHANNEL_COORDINATE[pair[0]],
                            producer.CHANNEL_COORDINATE[pair[1]],
                        ],
                        "orientation": orientation,
                    }
                    for key, value in expected_identity.items():
                        if rec.get(key) != value:
                            raise AssertionError(
                                f"T3-011-J deterministic record drift at {cursor}:{key}"
                            )
                    for key, value in alt.items():
                        if rec.get(key) != value:
                            raise AssertionError(
                                f"T3-011-J independent replay drift at {cursor}:{key}"
                            )
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
                            "orientation": orientation,
                            "mixed_sign_bidegree": [r, s],
                            "normalized_cokernel_pairing": [num, den],
                        }
                        stop = True
                        break
                if stop:
                    break
            if stop:
                break
        if stop:
            break

    if cursor != len(emitted):
        raise AssertionError("T3-011-J emitted records extend past canonical terminal")

    if first_unbounded is not None:
        terminal = producer.UNBOUNDED_TERMINAL
    elif first_ambiguity is not None:
        terminal = producer.AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = producer.ESCAPE_TERMINAL
    else:
        if cursor != producer.POSSIBLE_RECORD_COUNT:
            raise AssertionError("T3-011-J independent exhaustive record drift")
        terminal = producer.CLOSURE_TERMINAL

    if result.get("semantic_functional_ambiguity") != first_ambiguity:
        raise AssertionError("T3-011-J semantic ambiguity drift")
    if result.get("first_cokernel_breaking_direction") != first_escape:
        raise AssertionError("T3-011-J first escape drift")
    if result.get("characterized_blocker") != first_unbounded:
        raise AssertionError("T3-011-J characterized blocker drift")
    if result.get("terminal") != terminal:
        raise AssertionError("T3-011-J terminal drift")
    if result.get("all_mixed_sign_laurent_responses_cokernel_invisible") != (
        terminal == producer.CLOSURE_TERMINAL
    ):
        raise AssertionError("T3-011-J closure flag drift")
    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("T3-011-J claim firewall drift")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-011-J proof/promotion firewall drift")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3-011-J T3 status drift")

    cache_info = _independent_mixed_sign_solutions.cache_info()
    return {
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_T3_011_J_REPLAY_COMPLETE",
        "tested_record_count": cursor,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "characterized_blocker": first_unbounded,
        "all_mixed_sign_laurent_responses_cokernel_invisible": (
            terminal == producer.CLOSURE_TERMINAL
        ),
        "execution_ledger": {
            "forward_coordinate_factor_maps": len(forward),
            "inverse_coordinate_factor_maps": len(inverse),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "mixed_sign_solver_cache_hits": cache_info.hits,
            "mixed_sign_solver_cache_misses": cache_info.misses,
        },
        "terminal": terminal,
    }


def main() -> int:
    print(
        json.dumps(
            verify(producer.build()), sort_keys=True, separators=(",", ":")
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
