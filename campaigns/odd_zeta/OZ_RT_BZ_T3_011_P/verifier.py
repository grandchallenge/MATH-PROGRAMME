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

n, i, h = producer.n, producer.i, producer.h
g, f, a = producer.g, producer.f, producer.a


def _locks():
    got = {}
    for name, want in producer.O_BLOBS.items():
        value = a.git_blob_sha1(producer.O_DIR / name)
        if value != want:
            raise AssertionError(f"independent O source lock drift: {name}")
        got[name] = value
    contract = json.loads((producer.O_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-O":
        raise AssertionError("independent O contract operation drift")
    if contract.get("terminals", {}).get("closure") != producer.O_REQUIRED_TERMINAL:
        raise AssertionError("independent O terminal drift")
    return {"O": got}


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


def _ceil(a0: int, b0: int) -> int:
    if b0 <= 0:
        raise AssertionError("independent positive divisor required")
    return -((-a0) // b0)


def _bezout(a0: int, b0: int):
    if b0 == 0:
        return abs(a0), 1 if a0 >= 0 else -1, 0
    d0, x0, y0 = _bezout(b0, a0 % b0)
    return d0, y0, x0 - (a0 // b0) * y0


def _difference_seed(a0: int, b0: int, d0: int):
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
    pos = [index for index, coeff in enumerate(coeffs) if coeff > 0]
    neg = [index for index, coeff in enumerate(coeffs) if coeff < 0]
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
    positive = [index for index, coeff in enumerate(normalized) if coeff > 0]
    negative = [index for index, coeff in enumerate(normalized) if coeff < 0]
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
def independent_solve(
    base_sig, left_sig, right_sig, spectator_sig, target_sig, lower=(1, 1, 1)
):
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
            solutions = _positive_sum_solutions(
                [abs(coeff) for coeff in coeffs], sign * target_value
            )
            if not solutions:
                return "finite", (), None, None
            parts.append((indexes, solutions))
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
        producer.CHANNEL_COORDINATE[pair[0]], producer.CHANNEL_COORDINATE[pair[1]]
    }
    if len(remaining) != 1:
        raise AssertionError("independent spectator ambiguity")
    axis = next(iter(remaining))
    return axis, producer.CANONICAL_SPECTATOR_CHANNEL[axis]


def _indexes(endpoint, uid, pair, strata, bank, pcache, vcache):
    left, right = pair
    return {
        "I": vg._cached_vector_index(endpoint, uid, (), strata, bank, pcache, vcache)[1],
        "Sc": vg._cached_vector_index(endpoint, uid, (left,), strata, bank, pcache, vcache)[1],
        "Sd": vg._cached_vector_index(endpoint, uid, (right,), strata, bank, pcache, vcache)[1],
        "ScSd": vg._cached_vector_index(endpoint, uid, (left, right), strata, bank, pcache, vcache)[1],
    }


def _ledger(
    witness_index, base_index, left_maps, left_kind, right_maps, right_kind,
    spectator_maps, lower, evidence,
):
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
                    base_sig, left_sig, right_sig, spectator_sig, target_sig, tuple(lower)
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
                        weight * coeff * (left_coeff ** r) * (right_coeff ** s)
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


def _build_ledgers(
    pair, endpoint, uid, strata, bank, witness_index,
    inverse, pcache, vcache, lower, purpose,
):
    left, right = pair
    axis, spectator_channel = _spectator(pair)
    indexes = _indexes(endpoint, uid, pair, strata, bank, pcache, vcache)
    ledgers = {}
    for name, left_kind, right_kind, _marker in producer.COMPONENTS:
        ledgers[name] = _ledger(
            witness_index,
            indexes[name],
            inverse[left],
            left_kind,
            inverse[right],
            right_kind,
            inverse[spectator_channel],
            lower,
            {
                "pair": list(pair),
                "endpoint": endpoint,
                "candidate": producer.unknown_json(uid),
                "orientation": producer.ORIENTATIONS[0],
                "reciprocal_active_axes": ["left", "right"],
                "reciprocal_spectator": True,
                "spectator_axis": axis,
                "component": name,
                "purpose": purpose,
            },
        )
    return ledgers, axis, spectator_channel


def _selected(ledgers, selector):
    domain = set().union(*(part[0] for part in ledgers.values()))
    return _rows(ledgers, {degree for degree in domain if selector(*degree)})


def _protected_i_rows(
    pair, endpoint, uid, strata, bank, witness_index, inverse, pcache, vcache,
):
    left, right = pair
    indexes = _indexes(endpoint, uid, pair, strata, bank, pcache, vcache)
    ledgers = {
        "ScSd": i.inverse_bivariate_moment_ledger(
            witness_index, indexes["ScSd"], inverse[left], "x1", inverse[right], "x1"
        ),
        "Sc": i.inverse_bivariate_moment_ledger(
            witness_index, indexes["Sc"], inverse[left], "x1", inverse[right], "x0"
        ),
        "Sd": i.inverse_bivariate_moment_ledger(
            witness_index, indexes["Sd"], inverse[left], "x0", inverse[right], "x1"
        ),
        "I": i.inverse_bivariate_moment_ledger(
            witness_index, indexes["I"], inverse[left], "x0", inverse[right], "x0"
        ),
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


def _record_summary(
    pair, endpoint, uid, strata, bank, witness_index, inverse, pcache, vcache,
):
    primary, axis, spectator_channel = _build_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse, pcache, vcache, (1, 1, 1), "independent_admitted_P_class"
    )
    domain = set().union(*(part[0] for part in primary.values()))
    support_pairs = sum(part[2] for part in primary.values())
    domain = {degree for degree in domain if min(degree) >= 1}
    pairing_rows = _rows(primary, domain)

    t_zero, *_ = _build_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse, pcache, vcache, (1, 1, 0),
        "independent_spectator_reciprocal_degree_zero_I_boundary",
    )
    t_zero_here3 = _selected(t_zero, lambda r, s, t: r >= 1 and s >= 1 and t == 0)
    t_zero_here = [[r, s, num, den] for r, s, _t, num, den in t_zero_here3]
    t_zero_protected = _protected_i_rows(
        pair, endpoint, uid, strata, bank, witness_index, inverse, pcache, vcache
    )
    i_match = (
        t_zero_here == t_zero_protected
        and not any(row[-2] != 0 for row in t_zero_protected)
    )

    left_zero, *_ = _build_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse, pcache, vcache, (0, 1, 1),
        "independent_left_reciprocal_degree_zero_direct_response_anchor",
    )
    left_rows = _selected(left_zero, lambda r, s, t: r == 0 and s >= 1 and t >= 1)
    right_zero, *_ = _build_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse, pcache, vcache, (1, 0, 1),
        "independent_right_reciprocal_degree_zero_direct_response_anchor",
    )
    right_rows = _selected(right_zero, lambda r, s, t: s == 0 and r >= 1 and t >= 1)

    return {
        "finite_overlap_sha256": producer.sha([list(degree) for degree in sorted(domain)]),
        "pairing_sha256": producer.sha(pairing_rows),
        "nonzero_pairings": [row for row in pairing_rows if row[-2] != 0],
        "i_match": i_match,
        "left_anchor_sha256": producer.sha(left_rows),
        "right_anchor_sha256": producer.sha(right_rows),
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
    if result.get("predecessor_checkpoint", {}).get("merge_commit") != producer.O_MERGE_COMMIT:
        raise AssertionError("producer predecessor merge mismatch")

    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    inverse = {
        channel: h.inverse_coordinate_factors(channel, strata)
        for channel in producer.CHANNEL_COORDINATE
    }
    witness_indexes = {
        channel: vg._witness_index(bank["witness"])
        for channel, bank in banks.items()
    }
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
        for orientation_index, _orientation in enumerate(producer.ORIENTATIONS):
            for endpoint_index, endpoint in enumerate(pair):
                bank = banks[endpoint]
                witness_index = witness_indexes[endpoint]
                for candidate_index, uid in enumerate(bank["candidates"]):
                    try:
                        summary = _record_summary(
                            pair, endpoint, uid, strata, bank, witness_index,
                            inverse, pcache, vcache
                        )
                    except producer.UnboundedSupportOverlap as exc:
                        blocker = {
                            "kind": "UNBOUNDED_ALL_RECIPROCAL_TRIVARIATE_CANCELLATION_RAY",
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
                    identity = {
                        "pair_index": pair_index,
                        "orientation_index": orientation_index,
                        "endpoint_index": endpoint_index,
                        "candidate_index": candidate_index,
                    }
                    if any(record.get(key) != value for key, value in identity.items()):
                        raise AssertionError("producer record order drift")
                    if record.get("finite_overlap_sha256") != summary["finite_overlap_sha256"]:
                        raise AssertionError("independent finite overlap digest mismatch")
                    if record.get("pairing_sha256") != summary["pairing_sha256"]:
                        raise AssertionError("independent pairing digest mismatch")
                    if record.get("spectator_reciprocal_degree_zero_semantics_exactly_match_I") != summary["i_match"]:
                        raise AssertionError("independent I boundary mismatch")
                    if producer.sha(record.get("left_reciprocal_degree_zero_direct_response_rows", [])) != summary["left_anchor_sha256"]:
                        raise AssertionError("independent left direct-response anchor mismatch")
                    if producer.sha(record.get("right_reciprocal_degree_zero_direct_response_rows", [])) != summary["right_anchor_sha256"]:
                        raise AssertionError("independent right direct-response anchor mismatch")

                    if not summary["i_match"]:
                        first_ambiguity = record
                        independent_terminal = producer.AMBIGUITY_TERMINAL
                        stop = True
                    elif summary["nonzero_pairings"]:
                        r, s, t, num, den = summary["nonzero_pairings"][0]
                        first_escape = {
                            "ordinal": ordinal,
                            "pair": list(pair),
                            "endpoint": endpoint,
                            "candidate": producer.unknown_json(uid),
                            "orientation": producer.ORIENTATIONS[0],
                            "spectator_axis": summary["spectator_axis"],
                            "tridegree": [r, s, t],
                            "normalized_cokernel_pairing": [num, den],
                        }
                        independent_terminal = producer.ESCAPE_TERMINAL
                        stop = True
                    ordinal += 1
                    if stop:
                        break
                if stop:
                    break
            if stop:
                break
        if stop:
            break

    if independent_terminal == producer.CLOSURE_TERMINAL and tested != producer.POSSIBLE_RECORD_COUNT:
        raise AssertionError(
            f"independent P exhaustive record drift: {tested} != {producer.POSSIBLE_RECORD_COUNT}"
        )
    if result.get("terminal") != independent_terminal:
        raise AssertionError(
            f"independent terminal mismatch: {result.get('terminal')} != {independent_terminal}"
        )
    if result.get("possible_record_count") != producer.POSSIBLE_RECORD_COUNT:
        raise AssertionError("producer possible record count drift")
    if result.get("tested_record_count") != tested:
        raise AssertionError("producer tested record count drift")
    if result.get("domain_analysis", {}).get("support_signature_pairs_inspected") != support_pairs:
        raise AssertionError("producer/verifier support-pair count mismatch")

    if independent_terminal == producer.BLOCKER_TERMINAL:
        if result.get("characterized_blocker") != blocker:
            raise AssertionError("independent blocker mismatch")
    elif independent_terminal == producer.ESCAPE_TERMINAL:
        if result.get("first_cokernel_breaking_direction") != first_escape:
            raise AssertionError("independent escape mismatch")
    elif independent_terminal == producer.AMBIGUITY_TERMINAL:
        if result.get("semantic_functional_ambiguity") != first_ambiguity:
            raise AssertionError("independent semantic ambiguity mismatch")
    else:
        if any(result.get(key) is not None for key in (
            "characterized_blocker", "semantic_functional_ambiguity", "first_cokernel_breaking_direction"
        )):
            raise AssertionError("closure retained blocker, ambiguity, or escape")
        if not result.get("all_all_reciprocal_trivariate_responses_cokernel_invisible"):
            raise AssertionError("closure flag false")

    return {
        "schema_version": "1.0.0",
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_ALL_RECIPROCAL_TRIVARIATE_REPLAY_COMPLETE",
        "producer_result_sha256": producer.sha(result),
        "source_locks": locks,
        "possible_record_count": producer.POSSIBLE_RECORD_COUNT,
        "tested_record_count": tested,
        "support_signature_pairs_inspected": support_pairs,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "characterized_blocker": blocker,
        "all_all_reciprocal_trivariate_responses_cokernel_invisible": independent_terminal == producer.CLOSURE_TERMINAL,
        "finite_solver_uses_signature_derived_bounds_only": True,
        "arbitrary_degree_cutoff_used": False,
        "terminal": independent_terminal,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
