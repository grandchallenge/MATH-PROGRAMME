from __future__ import annotations

import itertools
import json
import math
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

m, k, j, i, h = producer.m, producer.k, producer.j, producer.i, producer.h
g, f, a = producer.g, producer.f, producer.a


def _locks():
    got = {}
    for name, want in producer.M_BLOBS.items():
        value = a.git_blob_sha1(producer.M_DIR / name)
        if value != want:
            raise AssertionError(f"independent M source lock drift: {name}")
        got[name] = value
    contract = json.loads((producer.M_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-M":
        raise AssertionError("independent M contract operation drift")
    if contract.get("terminals", {}).get("closure") != producer.M_REQUIRED_TERMINAL:
        raise AssertionError("independent M terminal drift")
    return {"M": got}


def _dict(sig):
    return {factor: int(exp) for factor, exp in sig if exp}


def _atom(sig, label):
    data = _dict(sig)
    if len(data) != 1:
        raise AssertionError(f"independent {label} is not one Laurent atom")
    factor, coeff = next(iter(data.items()))
    if coeff == 0:
        raise AssertionError(f"independent {label} exponent is zero")
    return factor, coeff


def _ceil(a0, b0):
    if b0 <= 0:
        raise AssertionError("independent positive divisor required")
    return -((-a0) // b0)


def _bezout(a0, b0):
    if b0 == 0:
        return abs(a0), 1 if a0 >= 0 else -1, 0
    d0, x0, y0 = _bezout(b0, a0 % b0)
    return d0, y0, x0 - (a0 // b0) * y0


def _difference_seed(a0, b0, d0):
    """Solve a*x-b*y=d with a,b>0 and x,y>=0."""
    gg, u0, v0 = _bezout(a0, b0)
    if d0 % gg:
        return None
    mult = d0 // gg
    x0, y0 = u0 * mult, -v0 * mult
    dx, dy = b0 // gg, a0 // gg
    shift = max(_ceil(-x0, dx), _ceil(-y0, dy))
    x1, y1 = x0 + shift * dx, y0 + shift * dy
    if x1 < 0 or y1 < 0 or a0 * x1 - b0 * y1 != d0:
        raise AssertionError("independent difference reconstruction drift")
    return x1, y1


def _positive_sum_solutions(coeffs, rhs):
    if rhs < 0:
        return []
    if len(coeffs) == 1:
        a0 = coeffs[0]
        return [(rhs // a0,)] if rhs % a0 == 0 else []
    if len(coeffs) == 2:
        a0, a1 = coeffs
        return [
            (x0, (rhs - a0 * x0) // a1)
            for x0 in range(rhs // a0 + 1)
            if (rhs - a0 * x0) % a1 == 0
        ]
    if len(coeffs) == 3:
        a0, a1, a2 = coeffs
        rows = []
        for x0 in range(rhs // a0 + 1):
            rem1 = rhs - a0 * x0
            for y0 in range(rem1 // a1 + 1):
                rem2 = rem1 - a1 * y0
                if rem2 % a2 == 0:
                    rows.append((x0, y0, rem2 // a2))
        return rows
    raise AssertionError("independent same-sign group arity drift")


def _mixed_seed_ray(coeffs, rhs):
    """Solve one mixed-sign factor equation and bind one primitive recession ray."""
    pos = [i for i, coeff in enumerate(coeffs) if coeff > 0]
    neg = [i for i, coeff in enumerate(coeffs) if coeff < 0]
    if not pos or not neg:
        raise AssertionError("independent mixed solver received one sign")

    if len(coeffs) == 2:
        ip, im = pos[0], neg[0]
        pair = _difference_seed(coeffs[ip], -coeffs[im], rhs)
        if pair is None:
            return None
        seed = [0, 0]
        seed[ip], seed[im] = pair
        gg = math.gcd(coeffs[ip], -coeffs[im])
        ray = [0, 0]
        ray[ip] = (-coeffs[im]) // gg
        ray[im] = coeffs[ip] // gg
        return tuple(seed), tuple(ray)

    if len(coeffs) != 3:
        raise AssertionError("independent mixed group arity drift")

    normalized, target = list(coeffs), rhs
    if len(pos) == 1:
        normalized = [-coeff for coeff in normalized]
        target = -target
    positive = [i for i, coeff in enumerate(normalized) if coeff > 0]
    negative = [i for i, coeff in enumerate(normalized) if coeff < 0]
    if len(positive) != 2 or len(negative) != 1:
        raise AssertionError("independent trivariate sign normalization drift")

    ix, iy = positive
    iz = negative[0]
    ax, by, cz = normalized[ix], normalized[iy], -normalized[iz]
    hh = math.gcd(ax, cz)
    gg = math.gcd(by, hh)
    if target % gg:
        return None

    period = hh // gg
    seed = None
    for y0 in range(period):
        remainder = target - by * y0
        if remainder % hh:
            continue
        pair = _difference_seed(ax, cz, remainder)
        if pair is not None:
            seed = [0, 0, 0]
            seed[ix], seed[iy], seed[iz] = pair[0], y0, pair[1]
            break
    if seed is None:
        raise AssertionError("independent trivariate congruence seed reconstruction failed")

    rg = math.gcd(ax, cz)
    ray = [0, 0, 0]
    ray[ix] = cz // rg
    ray[iz] = ax // rg
    return tuple(seed), tuple(ray)


def _matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, degree):
    out = _dict(base_sig)
    for sig, power in zip((left_sig, right_sig, spectator_sig), degree):
        for factor, exp in sig:
            out[factor] = out.get(factor, 0) + int(exp) * int(power)
            if out[factor] == 0:
                del out[factor]
    return tuple(sorted(out.items())) == tuple(target_sig)


def _ray_zero(left_sig, right_sig, spectator_sig, ray):
    out = {}
    for sig, power in zip((left_sig, right_sig, spectator_sig), ray):
        for factor, exp in sig:
            out[factor] = out.get(factor, 0) + int(exp) * int(power)
    return any(ray) and all(value == 0 for value in out.values())


@lru_cache(maxsize=None)
def independent_solve(base_sig, left_sig, right_sig, spectator_sig, target_sig, lower=(1, 1, 1)):
    """Independent exact solver for target-base=rL+sR+tE with lower bounds."""
    atoms = [
        _atom(left_sig, "left"),
        _atom(right_sig, "right"),
        _atom(spectator_sig, "spectator"),
    ]
    base, target = _dict(base_sig), _dict(target_sig)
    factors = set(base) | set(target) | {factor for factor, _ in atoms}
    rhs = {factor: target.get(factor, 0) - base.get(factor, 0) for factor in factors}
    for index, (factor, coeff) in enumerate(atoms):
        rhs[factor] -= int(lower[index]) * coeff

    groups = {}
    for index, (factor, coeff) in enumerate(atoms):
        groups.setdefault(factor, []).append((index, coeff))
    if any(rhs[factor] != 0 for factor in factors if factor not in groups):
        return "finite", (), None, None

    parts = []
    recession = None
    for factor in sorted(groups, key=repr):
        members = groups[factor]
        indexes = [index for index, _ in members]
        coeffs = [coeff for _, coeff in members]
        target_value = rhs.get(factor, 0)
        signs = {1 if coeff > 0 else -1 for coeff in coeffs}
        if len(signs) == 1:
            sign = 1 if coeffs[0] > 0 else -1
            sols = _positive_sum_solutions([abs(coeff) for coeff in coeffs], sign * target_value)
            if not sols:
                return "finite", (), None, None
            parts.append((indexes, sols))
        else:
            solved = _mixed_seed_ray(coeffs, target_value)
            if solved is None:
                return "finite", (), None, None
            local_seed, local_ray = solved
            parts.append((indexes, [local_seed]))
            ray = [0, 0, 0]
            for index, value in zip(indexes, local_ray):
                ray[index] = value
            if recession is None:
                recession = tuple(ray)

    def combine(choice):
        shifted = [0, 0, 0]
        for (indexes, _solutions), values in zip(parts, choice):
            for index, value in zip(indexes, values):
                shifted[index] = value
        return tuple(shifted[index] + int(lower[index]) for index in range(3))

    seed = combine(tuple(solutions[0] for _indexes, solutions in parts))
    if recession is not None:
        if not _matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, seed):
            raise AssertionError("independent unbounded seed mismatch")
        if not _ray_zero(left_sig, right_sig, spectator_sig, recession):
            raise AssertionError("independent recession direction mismatch")
        return "unbounded", (), seed, recession

    rows = []
    for choice in itertools.product(*(solutions for _indexes, solutions in parts)):
        degree = combine(choice)
        if not _matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, degree):
            raise AssertionError("independent finite solution mismatch")
        rows.append(degree)
    return "finite", tuple(sorted(set(rows))), None, None


def _spectator(pair):
    remaining = {"n", "k", "l"} - {
        producer.CHANNEL_COORDINATE[pair[0]],
        producer.CHANNEL_COORDINATE[pair[1]],
    }
    if len(remaining) != 1:
        raise AssertionError("independent spectator ambiguity")
    axis = next(iter(remaining))
    return axis, producer.CANONICAL_SPECTATOR_CHANNEL[axis]


def _maps(pair, orientation, forward, inverse):
    left, right = pair
    if orientation == "negative_left_negative_right":
        return inverse[left], inverse[right], "both"
    raise AssertionError("independent orientation drift")


def _indexes(endpoint, uid, pair, strata, bank, pcache, vcache):
    left, right = pair
    return {
        "I": vg._cached_vector_index(endpoint, uid, (), strata, bank, pcache, vcache)[1],
        "Sc": vg._cached_vector_index(endpoint, uid, (left,), strata, bank, pcache, vcache)[1],
        "Sd": vg._cached_vector_index(endpoint, uid, (right,), strata, bank, pcache, vcache)[1],
        "ScSd": vg._cached_vector_index(endpoint, uid, (left, right), strata, bank, pcache, vcache)[1],
    }


def _ledger(witness_index, base_index, left_maps, left_kind, right_maps, right_kind, spectator_maps, lower, evidence):
    aggregate = {}
    possible = set()
    support_pairs = 0
    for key in sorted(set(witness_index) & set(base_index), key=repr):
        cell_id, scalar, monomial = key
        sid = vg._stratum_id(cell_id)
        left_sig, left_coeff = left_maps[sid][left_kind]
        right_sig, right_coeff = right_maps[sid][right_kind]
        spectator_sig, spectator_coeff = spectator_maps[sid]["x0"]
        for target_sig, weight in witness_index[key]:
            for base_sig, coeff in base_index[key]:
                support_pairs += 1
                status, rows, seed, ray = independent_solve(
                    base_sig,
                    left_sig,
                    right_sig,
                    spectator_sig,
                    target_sig,
                    tuple(lower),
                )
                if status == "unbounded":
                    raise producer.UnboundedSupportOverlap({
                        **evidence,
                        "cell_id": cell_id,
                        "stratum_id": sid,
                        "scalar": scalar,
                        "monomial": list(monomial),
                        "base_signature": [list(item) for item in base_sig],
                        "target_signature": [list(item) for item in target_sig],
                        "left_step_signature": [list(item) for item in left_sig],
                        "right_step_signature": [list(item) for item in right_sig],
                        "spectator_step_signature": [list(item) for item in spectator_sig],
                        "feasible_seed_tridegree": list(seed),
                        "primitive_integer_ray": list(ray),
                        "support_feasible_recession": True,
                    })
                for r, s, t in rows:
                    possible.add((r, s, t))
                    value = (
                        weight
                        * coeff
                        * (left_coeff ** r)
                        * (right_coeff ** s)
                        * (spectator_coeff ** t)
                    )
                    aggregate[(r, s, t)] = aggregate.get((r, s, t), Q(0)) + value
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    return possible, aggregate, support_pairs


def _rows(ledgers, domain):
    out = []
    for degree in sorted(domain):
        value = (
            ledgers["ScSd"][1].get(degree, Q(0))
            - ledgers["Sc"][1].get(degree, Q(0))
            - ledgers["Sd"][1].get(degree, Q(0))
            + ledgers["I"][1].get(degree, Q(0))
        )
        out.append([*degree, *producer.qjson(value)])
    return out


def _build_ledgers(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache, lower, purpose):
    axis, spectator_channel = _spectator(pair)
    left_maps, right_maps, reciprocal_axis = _maps(pair, orientation, forward, inverse)
    indexes = _indexes(endpoint, uid, pair, strata, bank, pcache, vcache)
    ledgers = {}
    for name, left_kind, right_kind, _marker in producer.COMPONENTS:
        ledgers[name] = _ledger(
            witness_index,
            indexes[name],
            left_maps,
            left_kind,
            right_maps,
            right_kind,
            forward[spectator_channel],
            lower,
            {
                "pair": list(pair),
                "endpoint": endpoint,
                "candidate": producer.unknown_json(uid),
                "orientation": orientation,
                "reciprocal_active_axis": reciprocal_axis,
                "spectator_axis": axis,
                "component": name,
                "purpose": purpose,
            },
        )
    return ledgers, axis, spectator_channel, reciprocal_axis, indexes


def _protected_i_rows(pair, endpoint, uid, strata, bank, witness_index, inverse, pcache, vcache):
    left, right = pair
    indexes = _indexes(endpoint, uid, pair, strata, bank, pcache, vcache)
    ledgers = {
        "ScSd": i.inverse_bivariate_moment_ledger(witness_index, indexes["ScSd"], inverse[left], "x1", inverse[right], "x1"),
        "Sc": i.inverse_bivariate_moment_ledger(witness_index, indexes["Sc"], inverse[left], "x1", inverse[right], "x0"),
        "Sd": i.inverse_bivariate_moment_ledger(witness_index, indexes["Sd"], inverse[left], "x0", inverse[right], "x1"),
        "I": i.inverse_bivariate_moment_ledger(witness_index, indexes["I"], inverse[left], "x0", inverse[right], "x0"),
    }
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    out = []
    for degree in sorted((r, s) for r, s in domain if r >= 1 and s >= 1):
        value = (
            ledgers["ScSd"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sc"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sd"]["_aggregate"].get(degree, Q(0))
            + ledgers["I"]["_aggregate"].get(degree, Q(0))
        )
        out.append([*degree, *producer.qjson(value)])
    return out


def _protected_m_rows(pair, endpoint, uid, zero_side, strata, bank, witness_index, forward, inverse, pcache, vcache):
    if zero_side == "left":
        orientation, lower = "positive_left_negative_right", (0, 1, 1)
        selector = lambda r, s, t: r == 0 and s >= 1 and t >= 1
    else:
        orientation, lower = "negative_left_positive_right", (1, 0, 1)
        selector = lambda r, s, t: s == 0 and r >= 1 and t >= 1
    ledgers, *_ = m._make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward, inverse, pcache, vcache, lower, f"independent_{zero_side}_M_boundary"
    )
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
    return m._pairing_rows(ledgers, {(r, s, t) for r, s, t in domain if selector(r, s, t)})


def _record_summary(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache):
    primary, axis, spectator_channel, _reciprocal_axis, _indexes0 = _build_ledgers(
        pair,
        endpoint,
        uid,
        orientation,
        strata,
        bank,
        witness_index,
        forward,
        inverse,
        pcache,
        vcache,
        (1, 1, 1),
        "admitted_N_class",
    )
    domain = set()
    support_pairs = 0
    for possible, _aggregate, count in primary.values():
        domain.update(possible)
        support_pairs += count
    domain = {degree for degree in domain if min(degree) >= 1}
    pairing_rows = _rows(primary, domain)

    i_boundary, *_rest_i = _build_ledgers(
        pair,
        endpoint,
        uid,
        orientation,
        strata,
        bank,
        witness_index,
        forward,
        inverse,
        pcache,
        vcache,
        (1, 1, 0),
        "t_zero_I_boundary",
    )
    i_domain = set().union(*(value[0] for value in i_boundary.values()))
    i_selected = {(r, s, 0) for r, s, t in i_domain if r >= 1 and s >= 1 and t == 0}
    i_here = [[r, s, num, den] for r, s, _t, num, den in _rows(i_boundary, i_selected)]
    i_protected = _protected_i_rows(
        pair,
        endpoint,
        uid,
        strata,
        bank,
        witness_index,
        inverse,
        pcache,
        vcache,
    )

    zero_matches = []
    for zero_side, lower in (("left", (0, 1, 1)), ("right", (1, 0, 1))):
        boundary, *_ = _build_ledgers(
            pair, endpoint, uid, orientation, strata, bank, witness_index,
            forward, inverse, pcache, vcache, lower,
            f"{zero_side}_reciprocal_degree_zero_N_boundary",
        )
        bdomain = set().union(*(value[0] for value in boundary.values()))
        if zero_side == "left":
            selected = {(r, s, t) for r, s, t in bdomain if r == 0 and s >= 1 and t >= 1}
        else:
            selected = {(r, s, t) for r, s, t in bdomain if s == 0 and r >= 1 and t >= 1}
        here = _rows(boundary, selected)
        protected = _protected_m_rows(
            pair, endpoint, uid, zero_side, strata, bank, witness_index,
            forward, inverse, pcache, vcache,
        )
        zero_matches.append(here == protected and not any(row[-2] != 0 for row in protected))

    return {
        "finite_overlap_sha256": producer.sha([[r, s, t] for r, s, t in sorted(domain)]),
        "pairing_sha256": producer.sha(pairing_rows),
        "nonzero_pairings": [row for row in pairing_rows if row[-2] != 0],
        "i_match": i_here == i_protected and not any(row[-2] != 0 for row in i_protected),
        "m_match": all(zero_matches),
        "support_pairs": support_pairs,
        "spectator_axis": axis,
        "spectator_channel": spectator_channel,
    }


def verify(result=None):
    producer.validate_scope()
    independent_solve.cache_clear()
    locks = _locks()
    if result is None:
        result = producer.build()
    if result.get("issue") != producer.ISSUE or result.get("operation") != producer.OPERATION:
        raise AssertionError("producer identity mismatch")
    if result.get("predecessor_checkpoint", {}).get("merge_commit") != producer.M_MERGE_COMMIT:
        raise AssertionError("producer predecessor merge mismatch")

    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    forward = {channel: g.e._coordinate_factors(channel, strata) for channel in producer.CHANNEL_COORDINATE}
    inverse = {channel: h.inverse_coordinate_factors(channel, strata) for channel in producer.CHANNEL_COORDINATE}
    witness_indexes = {channel: vg._witness_index(bank["witness"]) for channel, bank in banks.items()}
    pcache, vcache = {}, {}

    independent_terminal = producer.CLOSURE_TERMINAL
    blocker = None
    first_escape = None
    first_ambiguity = None
    tested = 0
    support_pairs = 0
    ordinal = 0
    stop = False
    producer_records = result.get("tested_records", [])

    for pair_index, pair in enumerate(producer.ADMITTED_PAIRS):
        for orientation_index, orientation in enumerate(producer.ORIENTATIONS):
            for endpoint_index, endpoint in enumerate(pair):
                bank = banks[endpoint]
                witness_index = witness_indexes[endpoint]
                for candidate_index, uid in enumerate(bank["candidates"]):
                    try:
                        summary = _record_summary(
                            pair,
                            endpoint,
                            uid,
                            orientation,
                            strata,
                            bank,
                            witness_index,
                            forward,
                            inverse,
                            pcache,
                            vcache,
                        )
                    except producer.UnboundedSupportOverlap as exc:
                        blocker = {
                            "kind": "UNBOUNDED_DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_CANCELLATION_RAY",
                            "pair_index": pair_index,
                            "orientation_index": orientation_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                            **exc.evidence,
                        }
                        independent_terminal = producer.BLOCKER_TERMINAL
                        stop = True
                        break

                    tested += 1
                    support_pairs += summary["support_pairs"]
                    if ordinal >= len(producer_records):
                        raise AssertionError("producer stopped before independently finite record")
                    record = producer_records[ordinal]
                    expected_identity = {
                        "pair_index": pair_index,
                        "orientation_index": orientation_index,
                        "endpoint_index": endpoint_index,
                        "candidate_index": candidate_index,
                    }
                    if any(record.get(key) != value for key, value in expected_identity.items()):
                        raise AssertionError("producer record order drift")
                    if record.get("finite_overlap_sha256") != summary["finite_overlap_sha256"]:
                        raise AssertionError("independent finite overlap digest mismatch")
                    if record.get("pairing_sha256") != summary["pairing_sha256"]:
                        raise AssertionError("independent cokernel pairing digest mismatch")

                    if not summary["i_match"]:
                        first_ambiguity = record
                        independent_terminal = producer.AMBIGUITY_TERMINAL
                        stop = True
                        break
                    if not record.get("t_zero_semantics_exactly_match_I"):
                        raise AssertionError("producer I boundary claim disagrees with independent replay")
                    if not summary["m_match"]:
                        first_ambiguity = record
                        independent_terminal = producer.AMBIGUITY_TERMINAL
                        stop = True
                        break
                    if not record.get("reciprocal_degree_zero_semantics_exactly_match_M"):
                        raise AssertionError("producer M boundary claim disagrees with independent replay")

                    if summary["nonzero_pairings"]:
                        row = summary["nonzero_pairings"][0]
                        first_escape = {
                            "ordinal": ordinal,
                            "pair": list(pair),
                            "endpoint": endpoint,
                            "candidate": producer.unknown_json(uid),
                            "orientation": orientation,
                            "spectator_axis": summary["spectator_axis"],
                            "tridegree": row[:3],
                            "normalized_cokernel_pairing": row[-2:],
                        }
                        independent_terminal = producer.ESCAPE_TERMINAL
                        stop = True
                        break
                    ordinal += 1
                if stop:
                    break
            if stop:
                break
        if stop:
            break

    if not stop and tested != producer.POSSIBLE_RECORD_COUNT:
        raise AssertionError(f"independent exhaustive record drift: {tested}")
    if result.get("terminal") != independent_terminal:
        raise AssertionError(
            f"producer/verifier terminal mismatch: {result.get('terminal')} != {independent_terminal}"
        )
    if result.get("tested_record_count") != tested:
        raise AssertionError("producer/verifier tested record count mismatch")
    if result.get("domain_analysis", {}).get("support_signature_pairs_inspected") != support_pairs:
        raise AssertionError("producer/verifier support-pair count mismatch")

    if independent_terminal == producer.BLOCKER_TERMINAL:
        if result.get("characterized_blocker") != blocker:
            raise AssertionError("producer/verifier characterized blocker mismatch")
    elif independent_terminal == producer.ESCAPE_TERMINAL:
        if result.get("first_cokernel_breaking_direction") != first_escape:
            raise AssertionError("producer/verifier escape evidence mismatch")
    elif independent_terminal == producer.AMBIGUITY_TERMINAL:
        if result.get("semantic_functional_ambiguity") != first_ambiguity:
            raise AssertionError("producer/verifier semantic ambiguity mismatch")
    elif independent_terminal == producer.CLOSURE_TERMINAL:
        if (
            result.get("characterized_blocker") is not None
            or result.get("semantic_functional_ambiguity") is not None
            or result.get("first_cokernel_breaking_direction") is not None
        ):
            raise AssertionError("closure carries forbidden escape/ambiguity/blocker")
        if not result.get("all_double_reciprocal_active_trivariate_responses_cokernel_invisible"):
            raise AssertionError("closure flag false")

    return {
        "schema_version": "1.0.0",
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_REPLAY_COMPLETE",
        "producer_result_sha256": producer.sha(result),
        "source_locks": locks,
        "possible_record_count": producer.POSSIBLE_RECORD_COUNT,
        "tested_record_count": tested,
        "support_signature_pairs_inspected": support_pairs,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "characterized_blocker": blocker,
        "all_double_reciprocal_active_trivariate_responses_cokernel_invisible": independent_terminal == producer.CLOSURE_TERMINAL,
        "finite_solver_uses_signature_derived_bounds_only": True,
        "arbitrary_degree_cutoff_used": False,
        "terminal": independent_terminal,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
