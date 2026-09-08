from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_h as producer
import verify_t3_011_g as vg

semantic = vg.semantic
a = vg.a
p = vg.p


def _assert_g_locks_independent() -> dict[str, str]:
    got = {}
    for name, want in producer.G_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"independent G source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_011_G_CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-G":
        raise AssertionError("independent G contract operation drift")
    if contract.get("terminals", {}).get("closure") != producer.G_REQUIRED_TERMINAL:
        raise AssertionError("independent G closure terminal drift")
    return got


def _invert_factor(factor, label: str):
    sig, coeff = factor
    coeff = Q(coeff)
    if coeff == 0:
        raise AssertionError(f"{label} coordinate specialization is zero")
    inv = tuple(sorted((name, -int(exp)) for name, exp in reversed(sig) if exp))
    if not inv:
        raise AssertionError(f"{label} coordinate specialization is constant; reciprocal degree is not identifiable")
    return inv, Q(1, 1) / coeff


def _inverse_factor_map(channel: str, strata: list[dict]) -> dict:
    forward = vg._factor_map(channel, strata)
    out = {}
    for sid in reversed(sorted(forward)):
        out[sid] = {
            kind: _invert_factor(forward[sid][kind], f"{channel}:{sid}:{kind}")
            for kind in ("x0", "x1")
        }
    return out


def _as_dict(sig) -> dict:
    return {factor: int(exp) for factor, exp in sig if exp}


def _compose(base_sig, step_sig, degree: int):
    out = _as_dict(base_sig)
    for factor, exp in reversed(step_sig):
        out[factor] = out.get(factor, 0) + degree * int(exp)
        if out[factor] == 0:
            del out[factor]
    return tuple(sorted(out.items()))


def _solve_inverse_power(base_sig, step_sig, target_sig) -> int | None:
    base = _as_dict(base_sig)
    step = _as_dict(step_sig)
    target = _as_dict(target_sig)
    if not step:
        if base == target:
            raise AssertionError("independent reciprocal coordinate specialization became constant")
        return None
    candidate = None
    for factor in set(base) | set(step) | set(target):
        diff = target.get(factor, 0) - base.get(factor, 0)
        increment = step.get(factor, 0)
        if increment == 0:
            if diff != 0:
                return None
            continue
        if diff % increment:
            return None
        value = diff // increment
        if value < 0:
            return None
        if candidate is None:
            candidate = value
        elif candidate != value:
            return None
    if candidate is None:
        return None
    if _compose(base_sig, step_sig, candidate) != target_sig:
        return None
    return candidate


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


def _ledger(witness_index: dict, base_index: dict, inverse_factors: dict, factor_kind: str) -> dict:
    aggregate = {}
    possible = set()
    matches = []
    first = {}
    for key in sorted(set(witness_index) & set(base_index), key=repr, reverse=True):
        cell_id, scalar, mon = key
        sid = _stratum_id(cell_id)
        step_sig, step_coeff = inverse_factors[sid][factor_kind]
        for target_sig, weight in reversed(witness_index[key]):
            for base_sig, coeff in reversed(base_index[key]):
                degree = _solve_inverse_power(base_sig, step_sig, target_sig)
                if degree is None:
                    continue
                possible.add(degree)
                value = weight * coeff * (step_coeff ** degree)
                aggregate[degree] = aggregate.get(degree, Q(0)) + value
                row = [
                    degree,
                    cell_id,
                    scalar,
                    list(mon),
                    producer.qjson(weight),
                    producer.qjson(coeff),
                    producer.qjson(value),
                ]
                matches.append(row)
                first.setdefault(degree, row)
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [[degree, *producer.qjson(aggregate[degree])] for degree in sorted(aggregate)]
    return {
        "possible_degrees": sorted(possible),
        "nonzero_degrees": sorted(aggregate),
        "coefficient_rows": rows,
        "coefficient_sha256": producer.sha(rows),
        "match_count": len(matches),
        "match_sha256": producer.sha(matches),
        "first_evidence": {str(degree): first[degree] for degree in sorted(first)},
        "_aggregate": aggregate,
    }


def _direct_mixed_pairing(witness: dict, vec_gcd: dict, vec_gc: dict, vec_gd: dict, vec_g: dict) -> Q:
    total = Q(0)
    for key, weight in reversed(list(witness.items())):
        response = (
            Q(vec_gcd.get(key, 0))
            - Q(vec_gc.get(key, 0))
            - Q(vec_gd.get(key, 0))
            + Q(vec_g.get(key, 0))
        )
        total += Q(weight) * response
    return total


def _independent_record(
    pair,
    endpoint,
    uid,
    prefactor_channel,
    strata,
    bank,
    witness_index,
    inverse_factors,
    poly_cache,
    vector_cache,
):
    left, right = pair
    vec_g, idx_g = vg._cached_vector_index(
        endpoint, uid, (), strata, bank, poly_cache, vector_cache
    )
    vec_gc, idx_gc = vg._cached_vector_index(
        endpoint, uid, (left,), strata, bank, poly_cache, vector_cache
    )
    vec_gd, idx_gd = vg._cached_vector_index(
        endpoint, uid, (right,), strata, bank, poly_cache, vector_cache
    )
    vec_gcd, idx_gcd = vg._cached_vector_index(
        endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache
    )

    if prefactor_channel == left:
        kinds = {"ScSd": "x1", "Sc": "x1", "Sd": "x0", "I": "x0"}
    elif prefactor_channel == right:
        kinds = {"ScSd": "x1", "Sc": "x0", "Sd": "x1", "I": "x0"}
    else:
        raise AssertionError("independent H prefactor channel is outside the admitted pair")

    ledgers = {
        "ScSd": _ledger(witness_index, idx_gcd, inverse_factors, kinds["ScSd"]),
        "Sc": _ledger(witness_index, idx_gc, inverse_factors, kinds["Sc"]),
        "Sd": _ledger(witness_index, idx_gd, inverse_factors, kinds["Sd"]),
        "I": _ledger(witness_index, idx_g, inverse_factors, kinds["I"]),
    }

    domain = set()
    for ledger in ledgers.values():
        domain.update(ledger["possible_degrees"])
    domain = {degree for degree in domain if degree >= 1}

    rows = []
    nonzero = []
    for degree in sorted(domain):
        value = (
            ledgers["ScSd"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sc"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sd"]["_aggregate"].get(degree, Q(0))
            + ledgers["I"]["_aggregate"].get(degree, Q(0))
        )
        row = [degree, *producer.qjson(value)]
        rows.append(row)
        if value:
            nonzero.append(row)

    degree_zero_component = (
        ledgers["ScSd"]["_aggregate"].get(0, Q(0))
        - ledgers["Sc"]["_aggregate"].get(0, Q(0))
        - ledgers["Sd"]["_aggregate"].get(0, Q(0))
        + ledgers["I"]["_aggregate"].get(0, Q(0))
    )
    degree_zero_direct = _direct_mixed_pairing(
        bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g
    )
    semantic_match = degree_zero_component == degree_zero_direct

    return {
        "finite_overlap_reciprocal_degrees": sorted(domain),
        "finite_overlap_sha256": producer.sha(sorted(domain)),
        "component_ledgers": {
            name: {key: value for key, value in ledger.items() if not key.startswith("_")}
            for name, ledger in ledgers.items()
        },
        "pairing_rows": rows,
        "pairing_sha256": producer.sha(rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_degree": nonzero[0][0] if nonzero else None,
        "degree_zero_component_pairing": producer.qjson(degree_zero_component),
        "degree_zero_direct_pairing": producer.qjson(degree_zero_direct),
        "degree_zero_semantics_exactly_match_direct": semantic_match,
        "semantic_ambiguity_kind": (
            None
            if semantic_match
            else "DEGREE_ZERO_COMPONENT_DECOMPOSITION_DISAGREES_WITH_DIRECT_MIXED_RESPONSE"
        ),
        "all_reciprocal_degrees_annihilated": semantic_match and not nonzero,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("T3-011-H identity drift")
    producer.validate_scope()
    _assert_g_locks_independent()

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
            raise AssertionError("T3-011-H characterized blocker drift")
        return {
            "operation": producer.OPERATION,
            "status": "INDEPENDENT_T3_011_H_BLOCKER_REPLAY_COMPLETE",
            "characterized_blocker": str(exc),
            "terminal": producer.BLOCKER_TERMINAL,
        }

    if result.get("terminal") == producer.BLOCKER_TERMINAL:
        raise AssertionError("T3-011-H producer reported a blocker not reproduced independently")

    cls = result.get("reciprocal_axis_class", {})
    if cls.get("prefactor_domain") != "x_q^{-r} with q in {c,d} and integer r>=1":
        raise AssertionError("T3-011-H prefactor domain drift")
    if cls.get("unordered_pair_order") != [list(pair) for pair in producer.ADMITTED_PAIRS]:
        raise AssertionError("T3-011-H pair order drift")
    if cls.get("prefactor_side_order") != ["left", "right"]:
        raise AssertionError("T3-011-H side order drift")
    if cls.get("only_pole") != "x_q=0":
        raise AssertionError("T3-011-H pole boundary drift")
    if cls.get("nonzero_laurent_specialization_required") is not True:
        raise AssertionError("T3-011-H pole-safety requirement missing")
    if cls.get("finite_support_overlap_derived_without_degree_cutoff") is not True:
        raise AssertionError("T3-011-H finite-overlap proof-route flag missing")
    for forbidden in (
        "shifted_poles_admitted",
        "mixed_reciprocal_products_admitted",
        "positive_numerator_polynomials_admitted",
        "arbitrary_rational_functions_admitted",
        "support_or_harmonic_enlargement_admitted",
        "candidate_bank_or_scalar_namespace_widening_admitted",
        "recurrence_search_admitted",
        "correction_layer_work_admitted",
        "candidate_linear_combinations_admitted",
    ):
        if cls.get(forbidden):
            raise AssertionError(f"T3-011-H forbidden widening: {forbidden}")

    emitted = result.get("tested_records", [])
    possible_record_count = 2 * producer.G_FROZEN_RECORD_COUNT
    if result.get("possible_record_count") != possible_record_count:
        raise AssertionError("T3-011-H possible record count drift")

    witness_indexes = {
        channel: _witness_index(bank["witness"])
        for channel, bank in banks.items()
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
                for side_index, prefactor_channel in enumerate(pair):
                    if cursor >= len(emitted):
                        raise AssertionError("T3-011-H producer stopped before a terminal witness or exhaustion")
                    rec = emitted[cursor]
                    expected_identity = {
                        "ordinal": cursor,
                        "pair_index": pair_index,
                        "endpoint_index": endpoint_index,
                        "candidate_index": candidate_index,
                        "prefactor_side_index": side_index,
                        "prefactor_side": "left" if side_index == 0 else "right",
                        "pair": list(pair),
                        "endpoint": endpoint,
                        "candidate": [uid[0], list(uid[1])],
                        "prefactor_channel": prefactor_channel,
                        "prefactor_coordinate": producer.CHANNEL_COORDINATE[prefactor_channel],
                    }
                    for key, value in expected_identity.items():
                        if rec.get(key) != value:
                            raise AssertionError(
                                f"T3-011-H deterministic record drift at {cursor}:{key}"
                            )

                    alt = _independent_record(
                        pair,
                        endpoint,
                        uid,
                        prefactor_channel,
                        strata,
                        bank,
                        witness_index,
                        inverse_factors[prefactor_channel],
                        poly_cache,
                        vector_cache,
                    )
                    for key, value in alt.items():
                        if rec.get(key) != value:
                            raise AssertionError(
                                f"T3-011-H independent replay drift at {cursor}:{key}"
                            )

                    cursor += 1
                    if alt["semantic_ambiguity_kind"] is not None:
                        first_ambiguity = rec
                        stop = True
                        break
                    if alt["nonzero_pairings"]:
                        degree, num, den = alt["nonzero_pairings"][0]
                        first_escape = {
                            "ordinal": rec["ordinal"],
                            "pair": rec["pair"],
                            "endpoint": endpoint,
                            "candidate": rec["candidate"],
                            "prefactor_side": rec["prefactor_side"],
                            "prefactor_channel": prefactor_channel,
                            "reciprocal_degree": degree,
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
        raise AssertionError("T3-011-H producer emitted records beyond the canonical terminal")

    if first_ambiguity is not None:
        terminal = producer.AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = producer.ESCAPE_TERMINAL
    else:
        if cursor != possible_record_count:
            raise AssertionError("T3-011-H negative terminal lacks exhaustive reciprocal-axis coverage")
        terminal = producer.CLOSURE_TERMINAL

    if result.get("tested_record_count") != cursor:
        raise AssertionError("T3-011-H tested record count drift")
    if result.get("semantic_functional_ambiguity") != first_ambiguity:
        raise AssertionError("T3-011-H semantic ambiguity drift")
    if result.get("first_cokernel_breaking_direction") != first_escape:
        raise AssertionError("T3-011-H first escape drift")
    if result.get("terminal") != terminal:
        raise AssertionError("T3-011-H terminal drift")
    if result.get("all_reciprocal_axis_responses_cokernel_invisible") != (
        terminal == producer.CLOSURE_TERMINAL
    ):
        raise AssertionError("T3-011-H closure flag drift")
    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("T3-011-H residual claim firewall drift")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-011-H proof/promotion firewall drift")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3-011-H T3 status drift")

    return {
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_T3_011_H_REPLAY_COMPLETE",
        "possible_record_count": possible_record_count,
        "tested_record_count": cursor,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_reciprocal_axis_responses_cokernel_invisible": (
            terminal == producer.CLOSURE_TERMINAL
        ),
        "execution_ledger": {
            "inverse_coordinate_factor_maps": len(inverse_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
        },
        "terminal": terminal,
    }
