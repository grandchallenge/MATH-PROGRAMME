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

l, k, j, h = producer.l, producer.k, producer.j, producer.h
g, f, a = producer.g, producer.f, producer.a


def _locks():
    got = {}
    for name, want in producer.L_BLOBS.items():
        value = a.git_blob_sha1(producer.L_DIR / name)
        if value != want:
            raise AssertionError(f"independent L source lock drift: {name}")
        got[name] = value
    contract = json.loads((producer.L_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-L":
        raise AssertionError("independent L contract operation drift")
    if contract.get("terminals", {}).get("closure") != producer.L_REQUIRED_TERMINAL:
        raise AssertionError("independent L terminal drift")
    return {"L": got}


def _dict(sig):
    return {factor: int(exp) for factor, exp in sig if exp}


def _atom(sig, label):
    d = _dict(sig)
    if len(d) != 1:
        raise AssertionError(f"independent {label} is not one Laurent atom")
    factor, coeff = next(iter(d.items()))
    if coeff == 0:
        raise AssertionError(f"independent {label} exponent is zero")
    return factor, coeff


def _ceil(a, b):
    return -((-a) // b)


def _bezout(a, b):
    if b == 0:
        return abs(a), 1 if a >= 0 else -1, 0
    d, x, y = _bezout(b, a % b)
    return d, y, x - (a // b) * y


def _difference_seed(a, b, d):
    gg, u, v = _bezout(a, b)
    if d % gg:
        return None
    mult = d // gg
    x0, y0 = u * mult, -v * mult
    dx, dy = b // gg, a // gg
    n = max(_ceil(-x0, dx), _ceil(-y0, dy))
    x, y = x0 + n * dx, y0 + n * dy
    return (x, y) if x >= 0 and y >= 0 and a * x - b * y == d else None


def _positive_sum_solutions(coeffs, d):
    if d < 0:
        return []
    if len(coeffs) == 1:
        a0 = coeffs[0]
        return [(d // a0,)] if d % a0 == 0 else []
    if len(coeffs) == 2:
        a0, a1 = coeffs
        return [(x, (d - a0 * x) // a1) for x in range(d // a0 + 1) if (d - a0 * x) % a1 == 0]
    if len(coeffs) == 3:
        a0, a1, a2 = coeffs
        rows = []
        for x in range(d // a0 + 1):
            d1 = d - a0 * x
            for y in range(d1 // a1 + 1):
                d2 = d1 - a1 * y
                if d2 % a2 == 0:
                    rows.append((x, y, d2 // a2))
        return rows
    raise AssertionError("independent group arity drift")


def _mixed_seed_ray(coeffs, rhs):
    pos = [i for i, c in enumerate(coeffs) if c > 0]
    neg = [i for i, c in enumerate(coeffs) if c < 0]
    if len(coeffs) == 2:
        p, n = pos[0], neg[0]
        seed_pair = _difference_seed(coeffs[p], -coeffs[n], rhs)
        if seed_pair is None:
            return None
        seed = [0, 0]
        seed[p], seed[n] = seed_pair
        gg = math.gcd(coeffs[p], -coeffs[n])
        ray = [0, 0]
        ray[p], ray[n] = (-coeffs[n]) // gg, coeffs[p] // gg
        return tuple(seed), tuple(ray)
    if len(coeffs) != 3:
        raise AssertionError("independent mixed arity drift")
    cc, dd = list(coeffs), rhs
    if len(pos) == 1:
        cc, dd = [-c for c in cc], -dd
    pp = [i for i, c in enumerate(cc) if c > 0]
    nn = [i for i, c in enumerate(cc) if c < 0]
    if len(pp) != 2 or len(nn) != 1:
        raise AssertionError("independent three-variable sign normalization drift")
    p0, p1, n0 = pp[0], pp[1], nn[0]
    aa, bb, ccneg = cc[p0], cc[p1], -cc[n0]
    hh = math.gcd(aa, ccneg)
    gg = math.gcd(bb, hh)
    if dd % gg:
        return None
    period = hh // gg
    seed = None
    for y in range(period):
        remainder = dd - bb * y
        if remainder % hh:
            continue
        pair = _difference_seed(aa, ccneg, remainder)
        if pair is not None:
            seed = [0, 0, 0]
            seed[p0], seed[p1], seed[n0] = pair[0], y, pair[1]
            break
    if seed is None:
        raise AssertionError("independent congruence seed reconstruction failed")
    ray = [0, 0, 0]
    rg = math.gcd(aa, ccneg)
    ray[p0], ray[n0] = ccneg // rg, aa // rg
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
    total = {}
    for sig, power in zip((left_sig, right_sig, spectator_sig), ray):
        for factor, exp in sig:
            total[factor] = total.get(factor, 0) + int(exp) * int(power)
    return any(ray) and all(v == 0 for v in total.values())


@lru_cache(maxsize=None)
def independent_solve(base_sig, left_sig, right_sig, spectator_sig, target_sig, lower=(1, 1, 1)):
    atoms = [_atom(left_sig, "left"), _atom(right_sig, "right"), _atom(spectator_sig, "spectator")]
    base, target = _dict(base_sig), _dict(target_sig)
    factors = set(base) | set(target) | {p for p, _ in atoms}
    delta = {p: target.get(p, 0) - base.get(p, 0) for p in factors}
    for idx, (p, c) in enumerate(atoms):
        delta[p] -= int(lower[idx]) * c
    groups = {}
    for idx, (p, c) in enumerate(atoms):
        groups.setdefault(p, []).append((idx, c))
    if any(delta[p] != 0 for p in factors if p not in groups):
        return "finite", (), None, None

    parts = []
    global_ray = None
    for p in sorted(groups, key=repr):
        members = groups[p]
        ids = [idx for idx, _ in members]
        coeffs = [c for _, c in members]
        rhs = delta.get(p, 0)
        signs = {c > 0 for c in coeffs}
        if len(signs) == 1:
            sign = 1 if coeffs[0] > 0 else -1
            sols = _positive_sum_solutions([abs(c) for c in coeffs], sign * rhs)
            if not sols:
                return "finite", (), None, None
            parts.append((ids, sols))
        else:
            pair = _mixed_seed_ray(coeffs, rhs)
            if pair is None:
                return "finite", (), None, None
            seed_local, ray_local = pair
            parts.append((ids, [seed_local]))
            ray = [0, 0, 0]
            for idx, value in zip(ids, ray_local):
                ray[idx] = value
            if global_ray is None:
                global_ray = tuple(ray)

    def combine(values):
        y = [0, 0, 0]
        for (ids, _), local in zip(parts, values):
            for idx, value in zip(ids, local):
                y[idx] = value
        return tuple(y[i] + int(lower[i]) for i in range(3))

    seed = combine(tuple(sols[0] for _ids, sols in parts))
    if global_ray is not None:
        if not _matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, seed):
            raise AssertionError("independent unbounded seed mismatch")
        if not _ray_zero(left_sig, right_sig, spectator_sig, global_ray):
            raise AssertionError("independent recession direction mismatch")
        return "unbounded", (), seed, global_ray
    rows = []
    for choice in itertools.product(*(sols for _ids, sols in parts)):
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


def _maps(pair, orientation, forward, inverse):
    left, right = pair
    if orientation == "negative_left_positive_right":
        return inverse[left], forward[right]
    if orientation == "positive_left_negative_right":
        return forward[left], inverse[right]
    raise AssertionError("independent orientation drift")


def _indexes(endpoint, uid, pair, strata, bank, pcache, vcache):
    left, right = pair
    return {
        "I": vg._cached_vector_index(endpoint, uid, (), strata, bank, pcache, vcache)[1],
        "Sc": vg._cached_vector_index(endpoint, uid, (left,), strata, bank, pcache, vcache)[1],
        "Sd": vg._cached_vector_index(endpoint, uid, (right,), strata, bank, pcache, vcache)[1],
        "ScSd": vg._cached_vector_index(endpoint, uid, (left, right), strata, bank, pcache, vcache)[1],
    }


def _ledger(witness_index, base_index, lm, lk, rm, rk, sm, lower, evidence):
    agg, possible = {}, set()
    support_pairs = 0
    for key in sorted(set(witness_index) & set(base_index), key=repr, reverse=True):
        cell_id, scalar, mon = key
        sid = vg._stratum_id(cell_id)
        ls, lc = lm[sid][lk]
        rs, rc = rm[sid][rk]
        es, ec = sm[sid]["x0"]
        for target_sig, weight in reversed(witness_index[key]):
            for base_sig, coeff in reversed(base_index[key]):
                support_pairs += 1
                status, rows, seed, ray = independent_solve(base_sig, ls, rs, es, target_sig, tuple(lower))
                if status == "unbounded":
                    raise producer.UnboundedSupportOverlap({
                        **evidence,
                        "cell_id": cell_id,
                        "stratum_id": sid,
                        "scalar": scalar,
                        "monomial": list(mon),
                        "base_signature": [list(x) for x in base_sig],
                        "target_signature": [list(x) for x in target_sig],
                        "left_step_signature": [list(x) for x in ls],
                        "right_step_signature": [list(x) for x in rs],
                        "spectator_step_signature": [list(x) for x in es],
                        "feasible_seed_tridegree": list(seed),
                        "primitive_integer_ray": list(ray),
                        "support_feasible_recession": True,
                    })
                for r, s, t in rows:
                    possible.add((r, s, t))
                    value = weight * coeff * (lc ** r) * (rc ** s) * (ec ** t)
                    agg[(r, s, t)] = agg.get((r, s, t), Q(0)) + value
    agg = {degree: value for degree, value in agg.items() if value}
    return possible, agg, support_pairs


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
    left, right = pair
    axis, sch = _spectator(pair)
    lm, rm = _maps(pair, orientation, forward, inverse)
    indexes = _indexes(endpoint, uid, pair, strata, bank, pcache, vcache)
    ledgers = {}
    for name, lk, rk, _ in producer.COMPONENTS:
        ledgers[name] = _ledger(
            witness_index, indexes[name], lm, lk, rm, rk, forward[sch], lower,
            {"pair": list(pair), "endpoint": endpoint, "candidate": producer.unknown_json(uid), "orientation": orientation, "spectator_axis": axis, "component": name, "purpose": purpose},
        )
    return ledgers, axis, sch, indexes


def _protected_j_rows(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache):
    rec = j._candidate_record(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache)
    if rec["semantic_ambiguity_kind"] is not None or rec["nonzero_pairings"]:
        raise AssertionError("independent protected J boundary drift")
    return rec["pairing_rows"]


def _protected_k_rows(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, pcache, vcache):
    left, right = pair
    _axis, sch = _spectator(pair)
    idx = _indexes(endpoint, uid, pair, strata, bank, pcache, vcache)
    ledgers = {
        "ScSd": k.trivariate_moment_ledger(witness_index, idx["ScSd"], forward[left], "x1", forward[right], "x1", forward[sch]),
        "Sc": k.trivariate_moment_ledger(witness_index, idx["Sc"], forward[left], "x1", forward[right], "x0", forward[sch]),
        "Sd": k.trivariate_moment_ledger(witness_index, idx["Sd"], forward[left], "x0", forward[right], "x1", forward[sch]),
        "I": k.trivariate_moment_ledger(witness_index, idx["I"], forward[left], "x0", forward[right], "x0", forward[sch]),
    }
    domain = set()
    for led in ledgers.values():
        domain.update(map(tuple, led["possible_tridegrees"]))
    if orientation == "negative_left_positive_right":
        selected = {(0, s, t) for r, s, t in domain if r == 0 and s >= 1 and t >= 1}
    else:
        selected = {(r, 0, t) for r, s, t in domain if s == 0 and r >= 1 and t >= 1}
    return k._pairing_rows(ledgers, selected)


def _record_summary(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache):
    primary, axis, sch, _idx = _build_ledgers(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache, (1,1,1), "admitted_M_class")
    domain = set()
    support_pairs = 0
    for possible, _agg, count in primary.values():
        domain.update(possible)
        support_pairs += count
    domain = {d for d in domain if min(d) >= 1}
    pairing = _rows(primary, domain)

    jb, *_ = _build_ledgers(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache, (1,1,0), "t_zero_J_boundary")
    jd = set().union(*(v[0] for v in jb.values()))
    js = {(r,s,0) for r,s,t in jd if r>=1 and s>=1 and t==0}
    j_here = [[r,s,num,den] for r,s,_t,num,den in _rows(jb, js)]
    j_protected = _protected_j_rows(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache)

    lower = (0,1,1) if orientation == "negative_left_positive_right" else (1,0,1)
    kb, *_ = _build_ledgers(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache, lower, "reciprocal_degree_zero_K_boundary")
    kd = set().union(*(v[0] for v in kb.values()))
    if orientation == "negative_left_positive_right":
        ks = {(0,s,t) for r,s,t in kd if r==0 and s>=1 and t>=1}
    else:
        ks = {(r,0,t) for r,s,t in kd if s==0 and r>=1 and t>=1}
    k_here = _rows(kb, ks)
    k_protected = _protected_k_rows(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, pcache, vcache)

    return {
        "finite_overlap_sha256": producer.sha([[r,s,t] for r,s,t in sorted(domain)]),
        "pairing_sha256": producer.sha(pairing),
        "nonzero_pairings": [row for row in pairing if row[-2] != 0],
        "j_match": j_here == j_protected,
        "k_match": k_here == k_protected and not any(row[-2] != 0 for row in k_protected),
        "support_pairs": support_pairs,
        "spectator_axis": axis,
        "spectator_channel": sch,
    }


def verify(result=None):
    producer.validate_scope()
    independent_solve.cache_clear()
    locks = _locks()
    if result is None:
        result = producer.build()
    if result.get("issue") != producer.ISSUE or result.get("operation") != producer.OPERATION:
        raise AssertionError("producer identity mismatch")
    if result.get("predecessor_checkpoint", {}).get("merge_commit") != producer.L_MERGE_COMMIT:
        raise AssertionError("producer predecessor merge mismatch")

    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    forward = {ch: g.e._coordinate_factors(ch, strata) for ch in producer.CHANNEL_COORDINATE}
    inverse = {ch: h.inverse_coordinate_factors(ch, strata) for ch in producer.CHANNEL_COORDINATE}
    witness_indexes = {ch: vg._witness_index(bank["witness"]) for ch, bank in banks.items()}
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
                        summary = _record_summary(pair, endpoint, uid, orientation, strata, bank, witness_index, forward, inverse, pcache, vcache)
                    except producer.UnboundedSupportOverlap as exc:
                        blocker = {
                            "kind": "UNBOUNDED_SINGLE_RECIPROCAL_ACTIVE_TRIVARIATE_CANCELLATION_RAY",
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
                    rec = producer_records[ordinal]
                    if rec.get("pair_index") != pair_index or rec.get("orientation_index") != orientation_index or rec.get("endpoint_index") != endpoint_index or rec.get("candidate_index") != candidate_index:
                        raise AssertionError("producer record order drift")
                    if rec.get("finite_overlap_sha256") != summary["finite_overlap_sha256"]:
                        raise AssertionError("independent finite overlap digest mismatch")
                    if rec.get("pairing_sha256") != summary["pairing_sha256"]:
                        raise AssertionError("independent cokernel pairing digest mismatch")
                    if not summary["j_match"] or not rec.get("t_zero_semantics_exactly_match_J"):
                        first_ambiguity = {"ordinal": ordinal, "kind": "T_ZERO_BOUNDARY_DISAGREES_WITH_PROTECTED_T3_011_J"}
                        independent_terminal = producer.AMBIGUITY_TERMINAL
                        stop = True
                        break
                    if not summary["k_match"] or not rec.get("reciprocal_degree_zero_semantics_exactly_match_K"):
                        first_ambiguity = {"ordinal": ordinal, "kind": "RECIPROCAL_DEGREE_ZERO_BOUNDARY_DISAGREES_WITH_PROTECTED_T3_011_K"}
                        independent_terminal = producer.AMBIGUITY_TERMINAL
                        stop = True
                        break
                    if summary["nonzero_pairings"]:
                        row = summary["nonzero_pairings"][0]
                        first_escape = {"ordinal": ordinal, "tridegree": row[:3], "normalized_cokernel_pairing": row[-2:]}
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
        raise AssertionError(f"producer/verifier terminal mismatch: {result.get('terminal')} != {independent_terminal}")
    if result.get("tested_record_count") != tested:
        raise AssertionError("producer/verifier tested record count mismatch")
    if independent_terminal == producer.BLOCKER_TERMINAL and result.get("characterized_blocker") != blocker:
        raise AssertionError("producer/verifier characterized blocker mismatch")
    if independent_terminal == producer.CLOSURE_TERMINAL:
        if result.get("characterized_blocker") is not None or result.get("semantic_functional_ambiguity") is not None or result.get("first_cokernel_breaking_direction") is not None:
            raise AssertionError("closure carries forbidden escape/ambiguity/blocker")
        if not result.get("all_single_reciprocal_active_trivariate_responses_cokernel_invisible"):
            raise AssertionError("closure flag false")

    return {
        "schema_version": "1.0.0",
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_SINGLE_RECIPROCAL_ACTIVE_TRIVARIATE_REPLAY_COMPLETE",
        "producer_result_sha256": producer.sha(result),
        "source_locks": locks,
        "possible_record_count": producer.POSSIBLE_RECORD_COUNT,
        "tested_record_count": tested,
        "support_signature_pairs_inspected": support_pairs,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "characterized_blocker": blocker,
        "all_single_reciprocal_active_trivariate_responses_cokernel_invisible": independent_terminal == producer.CLOSURE_TERMINAL,
        "finite_solver_uses_signature_derived_bounds_only": True,
        "arbitrary_degree_cutoff_used": False,
        "terminal": independent_terminal,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
