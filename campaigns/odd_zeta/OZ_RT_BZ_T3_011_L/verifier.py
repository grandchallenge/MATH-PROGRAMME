from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
G_DIR = HERE.parent / "OZ_RT_BZ_T3_010"
sys.path.insert(0, str(G_DIR))
sys.path.insert(0, str(HERE))

import producer
import verify_t3_011_g as vg

a = vg.a


def _locks():
    out = {"K": {}, "G": {}}
    for name, want in producer.K_BLOBS.items():
        got = a.git_blob_sha1(producer.K_DIR / name)
        if got != want:
            raise AssertionError(f"independent K source lock drift: {name}")
        out["K"][name] = got
    kc = json.loads((producer.K_DIR / "CONTRACT.json").read_text())
    if kc.get("terminals", {}).get("closure") != producer.K_REQUIRED_TERMINAL:
        raise AssertionError("independent K contract drift")
    for name, want in producer.G_BLOBS.items():
        got = a.git_blob_sha1(producer.G_DIR / name)
        if got != want:
            raise AssertionError(f"independent G source lock drift: {name}")
        out["G"][name] = got
    gc = json.loads((producer.G_DIR / "T3_011_G_CONTRACT.json").read_text())
    if gc.get("terminals", {}).get("closure") != producer.G_REQUIRED_TERMINAL:
        raise AssertionError("independent G contract drift")
    return out


def _d(sig):
    return {factor: int(exp) for factor, exp in sig if exp}


def _single(sig, label):
    data = _d(sig)
    if not data or any(exp <= 0 for exp in data.values()):
        raise AssertionError(f"independent {label} coordinate factor is not positive")
    if len(data) != 1:
        raise AssertionError(f"independent {label} factor is not one affine Laurent atom")
    return next(iter(data.items()))


def _spectator(pair):
    rem = sorted(
        {"n", "k", "l"}
        - {producer.CHANNEL_COORDINATE[pair[0]], producer.CHANNEL_COORDINATE[pair[1]]}
    )
    if len(rem) != 1:
        raise AssertionError("independent spectator ambiguity")
    return rem[0], producer.CANONICAL_SPECTATOR_CHANNEL[rem[0]]


def _primitive_ray(ls, rs, es):
    lf, le = _single(ls, "left")
    rf, re = _single(rs, "right")
    ef, ee = _single(es, "spectator")
    rays = []
    if ef == lf:
        d0 = math.gcd(le, ee)
        rays.append([ee // d0, 0, le // d0])
    if ef == rf:
        d0 = math.gcd(re, ee)
        rays.append([0, ee // d0, re // d0])
    return min(rays) if rays else None


def _egcd(a0, b0):
    if b0 == 0:
        return abs(a0), 1 if a0 >= 0 else -1, 0
    g0, x1, y1 = _egcd(b0, a0 % b0)
    return g0, y1, x1 - (a0 // b0) * y1


def _ceil_div(a0, b0):
    return -((-a0) // b0)


def _positive_difference_solution(a0, b0, d0):
    g0, xg, yg = _egcd(a0, b0)
    if d0 % g0:
        return None
    scale = d0 // g0
    x0, y0 = xg * scale, -yg * scale
    dx, dy = b0 // g0, a0 // g0
    shift = max(_ceil_div(1 - x0, dx), _ceil_div(1 - y0, dy))
    x, y = x0 + shift * dx, y0 + shift * dy
    return (x, y) if x >= 1 and y >= 1 and a0 * x - b0 * y == d0 else None


def _seed(base_sig, target_sig, ls, rs, es):
    lf, le = _single(ls, "left")
    rf, re = _single(rs, "right")
    ef, ee = _single(es, "spectator")
    base, target = _d(base_sig), _d(target_sig)
    factors = set(base) | set(target) | {lf, rf, ef}
    diff = {z: target.get(z, 0) - base.get(z, 0) for z in factors}
    if any(diff[z] for z in factors - {lf, rf, ef}):
        return None
    if ef == lf and ef != rf:
        if diff.get(rf, 0) % re:
            return None
        s = diff.get(rf, 0) // re
        if s < 1:
            return None
        pair = _positive_difference_solution(le, ee, diff.get(lf, 0))
        return [pair[0], s, pair[1]] if pair else None
    if ef == rf and ef != lf:
        if diff.get(lf, 0) % le:
            return None
        r = diff.get(lf, 0) // le
        if r < 1:
            return None
        pair = _positive_difference_solution(re, ee, diff.get(rf, 0))
        return [r, pair[0], pair[1]] if pair else None
    if ef == lf == rf:
        target_value = diff.get(ef, 0)
        common = math.gcd(math.gcd(le, re), ee)
        if target_value % common:
            return None
        # Search one complete residue period for s; positivity in r,t is then supplied by the recession direction.
        h = math.gcd(le, ee)
        period = h // math.gcd(re, h)
        for s in range(1, period + 1):
            pair = _positive_difference_solution(le, ee, target_value - re * s)
            if pair:
                return [pair[0], s, pair[1]]
        return None
    return None


@lru_cache(maxsize=None)
def _finite(base_sig, left_sig, right_sig, spectator_sig, target_sig):
    lf, le = _single(left_sig, "left")
    rf, re = _single(right_sig, "right")
    ef, ee = _single(spectator_sig, "spectator")
    base, target = _d(base_sig), _d(target_sig)
    factors = set(base) | set(target) | {lf, rf, ef}
    diff = {z: target.get(z, 0) - base.get(z, 0) for z in factors}
    if any(diff[z] for z in factors - {lf, rf, ef}):
        return ()
    if ef == lf or ef == rf:
        if _seed(base_sig, target_sig, left_sig, right_sig, spectator_sig):
            raise AssertionError("independent unbounded support escaped preflight")
        return ()
    if lf != rf:
        vals = (diff.get(lf, 0), diff.get(rf, 0), -diff.get(ef, 0))
        steps = (le, re, ee)
        if any(v % step for v, step in zip(vals, steps)):
            return ()
        degree = tuple(v // step for v, step in zip(vals, steps))
        return (degree,) if min(degree) >= 1 else ()
    spectator_amount = -diff.get(ef, 0)
    if spectator_amount % ee:
        return ()
    t = spectator_amount // ee
    if t < 1:
        return ()
    active = diff.get(lf, 0)
    rows = []
    r = 1
    while le * r + re <= active:
        rem = active - le * r
        if rem % re == 0 and rem // re >= 1:
            rows.append((r, rem // re, t))
        r += 1
    return tuple(rows)


def _blocker_scan(strata, banks, factors):
    witness_indexes = {name: vg._witness_index(bank["witness"]) for name, bank in banks.items()}
    poly_cache = {}
    vector_cache = {}
    records = 0
    support_pairs = 0
    for pair_index, pair in enumerate(producer.ADMITTED_PAIRS):
        left, right = pair
        axis, sch = _spectator(pair)
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            witness_index = witness_indexes[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                indexes = {
                    "I": vg._cached_vector_index(endpoint, uid, (), strata, bank, poly_cache, vector_cache)[1],
                    "Sc": vg._cached_vector_index(endpoint, uid, (left,), strata, bank, poly_cache, vector_cache)[1],
                    "Sd": vg._cached_vector_index(endpoint, uid, (right,), strata, bank, poly_cache, vector_cache)[1],
                    "ScSd": vg._cached_vector_index(endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache)[1],
                }
                records += 1
                for component_index, (component, lk, rk, _marker) in enumerate(producer.COMPONENTS):
                    base_index = indexes[component]
                    for key in sorted(set(witness_index) & set(base_index), key=repr):
                        cell_id, scalar, mon = key
                        sid = cell_id.split(":", 2)[2]
                        ls, _ = factors[left][sid][lk]
                        rs, _ = factors[right][sid][rk]
                        es, ec = factors[sch][sid]["x0"]
                        ray = _primitive_ray(ls, rs, es)
                        for target_sig, _weight in sorted(witness_index[key], key=repr):
                            for base_sig, _coeff in sorted(base_index[key], key=repr):
                                support_pairs += 1
                                seed = _seed(base_sig, target_sig, ls, rs, es) if ray else None
                                finite = () if seed else _finite(base_sig, ls, rs, es, target_sig)
                                if not seed and not finite:
                                    continue
                                common = {
                                    "pair_index": pair_index,
                                    "endpoint_index": endpoint_index,
                                    "candidate_index": candidate_index,
                                    "pair": list(pair),
                                    "endpoint": endpoint,
                                    "candidate": [uid[0], list(uid[1])],
                                    "component_index": component_index,
                                    "component": component,
                                    "stratum": sid,
                                    "spectator_axis": axis,
                                    "spectator_channel_representative": sch,
                                    "support_key": [cell_id, scalar, list(mon)],
                                    "base_signature": list(base_sig),
                                    "target_signature": list(target_sig),
                                }
                                if Q(ec) == 0:
                                    return {"kind": "RECIPROCAL_SPECTATOR_SPECIALIZES_TO_ZERO_ON_ADMITTED_SUPPORT", **common}, records, support_pairs
                                if seed:
                                    return {
                                        "kind": "UNBOUNDED_RECIPROCAL_SPECTATOR_CANCELLATION_RAY",
                                        **common,
                                        "left_factor_kind": lk,
                                        "right_factor_kind": rk,
                                        "reciprocal_spectator_factor_kind": "x0",
                                        "primitive_integer_ray": ray,
                                        "feasible_seed_tridegree": seed,
                                        "homogeneous_relation": "dr*L + ds*R - dt*E = 0",
                                        "affine_relation": "target-base = r*L + s*R - t*E",
                                    }, records, support_pairs
    return None, records, support_pairs


def _ledger(witness_index, base_index, left_factors, lk, right_factors, rk, spectator_factors):
    aggregate = {}
    possible = set()
    matches = []
    for key in sorted(set(witness_index) & set(base_index), key=repr, reverse=True):
        cell_id, scalar, mon = key
        sid = cell_id.split(":", 2)[2]
        ls, lc = left_factors[sid][lk]
        rs, rc = right_factors[sid][rk]
        es, ec = spectator_factors[sid]["x0"]
        for target_sig, weight in reversed(witness_index[key]):
            for base_sig, coeff in reversed(base_index[key]):
                for r, s, t in _finite(base_sig, ls, rs, es, target_sig):
                    if Q(ec) == 0:
                        raise AssertionError("independent zero reciprocal spectator escaped preflight")
                    value = weight * coeff * (lc ** r) * (rc ** s) * (ec ** (-t))
                    possible.add((r, s, t))
                    aggregate[(r, s, t)] = aggregate.get((r, s, t), Q(0)) + value
                    matches.append([r, s, t, cell_id, scalar, list(mon), producer.qjson(weight), producer.qjson(coeff), producer.qjson(value)])
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [[r, s, t, *producer.qjson(aggregate[(r, s, t)])] for r, s, t in sorted(aggregate)]
    return {
        "possible_tridegrees": [[r, s, t] for r, s, t in sorted(possible)],
        "nonzero_tridegrees": [[r, s, t] for r, s, t in sorted(aggregate)],
        "coefficient_rows": rows,
        "coefficient_sha256": producer.sha(rows),
        "match_count": len(matches),
        "match_sha256": producer.sha(sorted(matches, key=repr)),
        "_aggregate": aggregate,
    }


def _boundary_rows(witness_index, idx_gcd, idx_gc, idx_gd, idx_g, left_factors, right_factors):
    ledgers = {
        "ScSd": vg._ledger(witness_index, idx_gcd, left_factors, "x1", right_factors, "x1"),
        "Sc": vg._ledger(witness_index, idx_gc, left_factors, "x1", right_factors, "x0"),
        "Sd": vg._ledger(witness_index, idx_gd, left_factors, "x0", right_factors, "x1"),
        "I": vg._ledger(witness_index, idx_g, left_factors, "x0", right_factors, "x0"),
    }
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_multidegrees"]))
    rows = []
    for r, s in sorted((r, s) for r, s in domain if r >= 1 and s >= 1):
        value = ledgers["ScSd"]["_aggregate"].get((r, s), Q(0)) - ledgers["Sc"]["_aggregate"].get((r, s), Q(0)) - ledgers["Sd"]["_aggregate"].get((r, s), Q(0)) + ledgers["I"]["_aggregate"].get((r, s), Q(0))
        rows.append([r, s, *producer.qjson(value)])
    return rows


def _record(pair, endpoint, uid, strata, bank, witness_index, factors, poly_cache, vector_cache):
    left, right = pair
    axis, sch = _spectator(pair)
    left_factors, right_factors, spectator_factors = factors[left], factors[right], factors[sch]
    _, idx_g = vg._cached_vector_index(endpoint, uid, (), strata, bank, poly_cache, vector_cache)
    _, idx_gc = vg._cached_vector_index(endpoint, uid, (left,), strata, bank, poly_cache, vector_cache)
    _, idx_gd = vg._cached_vector_index(endpoint, uid, (right,), strata, bank, poly_cache, vector_cache)
    _, idx_gcd = vg._cached_vector_index(endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache)
    ledgers = {
        "ScSd": _ledger(witness_index, idx_gcd, left_factors, "x1", right_factors, "x1", spectator_factors),
        "Sc": _ledger(witness_index, idx_gc, left_factors, "x1", right_factors, "x0", spectator_factors),
        "Sd": _ledger(witness_index, idx_gd, left_factors, "x0", right_factors, "x1", spectator_factors),
        "I": _ledger(witness_index, idx_g, left_factors, "x0", right_factors, "x0", spectator_factors),
    }
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
    domain = {(r, s, t) for r, s, t in domain if min(r, s, t) >= 1}
    rows = []
    for degree in sorted(domain):
        value = ledgers["ScSd"]["_aggregate"].get(degree, Q(0)) - ledgers["Sc"]["_aggregate"].get(degree, Q(0)) - ledgers["Sd"]["_aggregate"].get(degree, Q(0)) + ledgers["I"]["_aggregate"].get(degree, Q(0))
        rows.append([*degree, *producer.qjson(value)])
    nonzero = [row for row in rows if row[-2] != 0]
    boundary = _boundary_rows(witness_index, idx_gcd, idx_gc, idx_gd, idx_g, left_factors, right_factors)
    boundary_ok = not any(row[-2] != 0 for row in boundary)
    return {
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": [uid[0], list(uid[1])],
        "coordinate_pair": [producer.CHANNEL_COORDINATE[left], producer.CHANNEL_COORDINATE[right]],
        "spectator_axis": axis,
        "spectator_channel_representative": sch,
        "finite_overlap_tridegrees": [[r, s, t] for r, s, t in sorted(domain)],
        "finite_overlap_sha256": producer.sha([[r, s, t] for r, s, t in sorted(domain)]),
        "component_ledgers": {name: {key: value for key, value in ledger.items() if not key.startswith("_")} for name, ledger in ledgers.items()},
        "pairing_rows": rows,
        "pairing_sha256": producer.sha(rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_tridegree": nonzero[0][:3] if nonzero else None,
        "protected_G_boundary_rows": boundary,
        "t_zero_semantics_exactly_match_G": boundary_ok,
        "semantic_ambiguity_kind": None if boundary_ok else "PROTECTED_T3_011_G_BOUNDARY_RECONSTRUCTION_IS_NONZERO",
        "all_reciprocal_spectator_degrees_annihilated": boundary_ok and not nonzero,
    }


def _compare_record(emitted, independent):
    for key, value in independent.items():
        if emitted.get(key) != value:
            raise AssertionError(f"L independent record drift: {key}")


def verify(result):
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("L identity drift")
    producer.validate_scope()
    _finite.cache_clear()
    locks = _locks()
    if result.get("predecessor_checkpoint", {}).get("source_blobs") != locks:
        raise AssertionError("L lock ledger drift")
    cls = result.get("reciprocal_spectator_class", {})
    for required in ("spectator_is_unshifted", "reciprocal_spectator_admitted", "complete_overlap_derived_from_exact_signatures", "t_zero_boundary_matches_protected_G"):
        if cls.get(required) is not True:
            raise AssertionError(f"L required class flag missing: {required}")
    if cls.get("arbitrary_degree_cutoff_used") is not False or cls.get("third_finite_difference_operator_admitted") is not False:
        raise AssertionError("L scope firewall drift")

    strata, specialized, supports = vg.vf.vd.reconstruct_context()
    banks = vg.vf._reconstruct_banks(strata, specialized, supports)
    factors = {ch: vg._factor_map(ch, strata) for ch in producer.CHANNEL_COORDINATE}
    blocker, records_inspected, support_pairs = _blocker_scan(strata, banks, factors)
    domain_info = result.get("domain_analysis", {})
    if domain_info.get("candidate_records_inspected_for_support") != records_inspected:
        raise AssertionError("L support record count drift")
    if domain_info.get("support_signature_pairs_inspected") != support_pairs:
        raise AssertionError("L support signature count drift")
    if domain_info.get("finite_solver_uses_signature_derived_bounds_only") is not True or domain_info.get("arbitrary_degree_cutoff_used") is not False:
        raise AssertionError("L exact finite-domain contract drift")

    if blocker is not None:
        if result.get("characterized_blocker") != blocker:
            raise AssertionError("L characterized blocker drift")
        if result.get("terminal") != producer.BLOCKER_TERMINAL or result.get("tested_record_count") != 0:
            raise AssertionError("L blocker terminal drift")
        terminal = producer.BLOCKER_TERMINAL
        first_escape = None
        first_ambiguity = None
        cursor = 0
    else:
        if result.get("characterized_blocker") is not None:
            raise AssertionError("L producer emitted unreproduced blocker")
        emitted = result.get("tested_records", [])
        witness_indexes = {name: vg._witness_index(bank["witness"]) for name, bank in banks.items()}
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
                        raise AssertionError("L producer stopped before canonical terminal")
                    rec = emitted[cursor]
                    identity = {"ordinal": cursor, "pair_index": pair_index, "endpoint_index": endpoint_index, "candidate_index": candidate_index, "pair": list(pair), "endpoint": endpoint, "candidate": [uid[0], list(uid[1])]}
                    for key, value in identity.items():
                        if rec.get(key) != value:
                            raise AssertionError(f"L deterministic identity drift: {key}")
                    alt = _record(pair, endpoint, uid, strata, bank, witness_index, factors, poly_cache, vector_cache)
                    _compare_record(rec, alt)
                    cursor += 1
                    if alt["semantic_ambiguity_kind"] is not None:
                        first_ambiguity = rec
                        stop = True
                        break
                    if alt["nonzero_pairings"]:
                        r, s, t, num, den = alt["nonzero_pairings"][0]
                        first_escape = {"ordinal": rec["ordinal"], "pair": rec["pair"], "endpoint": endpoint, "candidate": rec["candidate"], "spectator_axis": rec["spectator_axis"], "tridegree": [r, s, t], "normalized_cokernel_pairing": [num, den]}
                        stop = True
                        break
                if stop:
                    break
            if stop:
                break
        if cursor != len(emitted):
            raise AssertionError("L emitted records extend past canonical terminal")
        if first_ambiguity is not None:
            terminal = producer.AMBIGUITY_TERMINAL
        elif first_escape is not None:
            terminal = producer.ESCAPE_TERMINAL
        else:
            if cursor != producer.FROZEN_RECORD_COUNT:
                raise AssertionError("L exhaustive record count drift")
            terminal = producer.CLOSURE_TERMINAL
        if result.get("semantic_functional_ambiguity") != first_ambiguity:
            raise AssertionError("L semantic ambiguity drift")
        if result.get("first_cokernel_breaking_direction") != first_escape:
            raise AssertionError("L first escape drift")
        if result.get("terminal") != terminal:
            raise AssertionError("L terminal drift")
        if result.get("all_reciprocal_spectator_responses_cokernel_invisible") != (terminal == producer.CLOSURE_TERMINAL):
            raise AssertionError("L closure flag drift")

    if result.get("residual_sum_zero_proved") is not False or result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE" or result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("L claim firewall drift")
    return {
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_T3_011_L_REPLAY_COMPLETE",
        "tested_record_count": cursor,
        "characterized_blocker": blocker,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_reciprocal_spectator_responses_cokernel_invisible": terminal == producer.CLOSURE_TERMINAL,
        "terminal": terminal,
    }
