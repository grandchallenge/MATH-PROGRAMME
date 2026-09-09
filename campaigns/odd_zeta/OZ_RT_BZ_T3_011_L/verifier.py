from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as Q
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
    return out


def _d(sig):
    return {factor: int(exp) for factor, exp in sig if exp}


def _single(sig, label):
    out = _d(sig)
    if not out or any(exp <= 0 for exp in out.values()):
        raise AssertionError(f"independent {label} coordinate factor is not positive")
    if len(out) != 1:
        raise AssertionError(
            f"independent {label} coordinate factor is not a single affine Laurent atom"
        )
    return next(iter(out.items()))


def _primitive_ray(ls, rs, es):
    lf, le = _single(ls, "left")
    rf, re = _single(rs, "right")
    ef, ee = _single(es, "spectator")
    candidates = []
    if ef == lf:
        g0 = math.gcd(le, ee)
        candidates.append([ee // g0, 0, le // g0])
    if ef == rf:
        g0 = math.gcd(re, ee)
        candidates.append([0, ee // g0, re // g0])
    if not candidates:
        return None
    return min(candidates)


def _spectator(pair):
    rem = sorted(
        {"n", "k", "l"}
        - {
            producer.CHANNEL_COORDINATE[pair[0]],
            producer.CHANNEL_COORDINATE[pair[1]],
        }
    )
    if len(rem) != 1:
        raise AssertionError("independent spectator ambiguity")
    return rem[0], producer.CANONICAL_SPECTATOR_CHANNEL[rem[0]]


def _positive_solution_exists(base_sig, target_sig, ls, rs, es):
    lf, le = _single(ls, "left")
    rf, re = _single(rs, "right")
    ef, ee = _single(es, "spectator")
    base, target = _d(base_sig), _d(target_sig)
    factors = set(base) | set(target) | {lf, rf, ef}
    diff = {z: target.get(z, 0) - base.get(z, 0) for z in factors}
    if any(diff[z] for z in factors - {lf, rf, ef}):
        return False

    if ef == lf and ef != rf:
        other = diff.get(rf, 0)
        if other % re or other // re < 1:
            return False
        return diff.get(lf, 0) % math.gcd(le, ee) == 0

    if ef == rf and ef != lf:
        other = diff.get(lf, 0)
        if other % le or other // le < 1:
            return False
        return diff.get(rf, 0) % math.gcd(re, ee) == 0

    if ef == lf == rf:
        return diff.get(ef, 0) % math.gcd(math.gcd(le, re), ee) == 0

    return False


def _validate_seed(blocker, factors):
    pair = tuple(blocker["pair"])
    sid = blocker["stratum"]
    _, sch = _spectator(pair)
    ls, _ = factors[pair[0]][sid][blocker["left_factor_kind"]]
    rs, _ = factors[pair[1]][sid][blocker["right_factor_kind"]]
    es, _ = factors[sch][sid]["x0"]
    base = _d(tuple(tuple(x) for x in blocker["base_signature"]))
    target = _d(tuple(tuple(x) for x in blocker["target_signature"]))
    L, R, E = _d(ls), _d(rs), _d(es)
    r, s, t = blocker["feasible_seed_tridegree"]
    if min(r, s, t) < 1:
        raise AssertionError("producer feasible seed is not positive")
    for z in set(base) | set(target) | set(L) | set(R) | set(E):
        lhs = target.get(z, 0) - base.get(z, 0)
        rhs = r * L.get(z, 0) + s * R.get(z, 0) - t * E.get(z, 0)
        if lhs != rhs:
            raise AssertionError("producer feasible seed does not satisfy support equation")


def _scan(strata, banks, factors):
    witness_indexes = {
        channel: vg._witness_index(bank["witness"]) for channel, bank in banks.items()
    }
    poly_cache = {}
    vector_cache = {}
    records_inspected = 0
    ray_support_pairs = 0

    for pair_index, pair in enumerate(producer.ADMITTED_PAIRS):
        left, right = pair
        axis, sch = _spectator(pair)
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            witness_index = witness_indexes[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                component_indexes = {
                    "I": vg._cached_vector_index(
                        endpoint, uid, (), strata, bank, poly_cache, vector_cache
                    )[1],
                    "Sc": vg._cached_vector_index(
                        endpoint, uid, (left,), strata, bank, poly_cache, vector_cache
                    )[1],
                    "Sd": vg._cached_vector_index(
                        endpoint, uid, (right,), strata, bank, poly_cache, vector_cache
                    )[1],
                    "ScSd": vg._cached_vector_index(
                        endpoint,
                        uid,
                        (left, right),
                        strata,
                        bank,
                        poly_cache,
                        vector_cache,
                    )[1],
                }
                records_inspected += 1
                for component_index, (component, lk, rk, _marker) in enumerate(
                    producer.COMPONENTS
                ):
                    base_index = component_indexes[component]
                    for base_key in sorted(
                        set(witness_index) & set(base_index), key=repr
                    ):
                        cell_id, scalar, mon = base_key
                        sid = cell_id.split(":", 2)[2]
                        ls, _ = factors[left][sid][lk]
                        rs, _ = factors[right][sid][rk]
                        es, ec = factors[sch][sid]["x0"]
                        ray = _primitive_ray(ls, rs, es)
                        if ray is None:
                            continue
                        for target_sig, _weight in sorted(
                            witness_index[base_key], key=repr
                        ):
                            for base_sig, _coeff in sorted(
                                base_index[base_key], key=repr
                            ):
                                ray_support_pairs += 1
                                if not _positive_solution_exists(
                                    base_sig, target_sig, ls, rs, es
                                ):
                                    continue
                                kind = (
                                    "RECIPROCAL_SPECTATOR_SPECIALIZES_TO_ZERO_ON_ADMITTED_SUPPORT"
                                    if Q(ec) == 0
                                    else "UNBOUNDED_RECIPROCAL_SPECTATOR_CANCELLATION_RAY"
                                )
                                return {
                                    "kind": kind,
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
                                    "left_factor_kind": lk,
                                    "right_factor_kind": rk,
                                    "reciprocal_spectator_factor_kind": "x0",
                                    "primitive_integer_ray": ray,
                                    "support_key": [cell_id, scalar, list(mon)],
                                    "base_signature": list(base_sig),
                                    "target_signature": list(target_sig),
                                }, records_inspected, ray_support_pairs
    return None, records_inspected, ray_support_pairs


def _compare_blocker_identity(emitted, independent):
    keys = (
        "kind",
        "pair_index",
        "endpoint_index",
        "candidate_index",
        "pair",
        "endpoint",
        "candidate",
        "component_index",
        "component",
        "stratum",
        "spectator_axis",
        "spectator_channel_representative",
        "left_factor_kind",
        "right_factor_kind",
        "reciprocal_spectator_factor_kind",
        "primitive_integer_ray",
        "support_key",
        "base_signature",
        "target_signature",
    )
    for key in keys:
        if emitted.get(key) != independent.get(key):
            raise AssertionError(f"L independent blocker drift: {key}")


def verify(result):
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("L identity drift")
    producer.validate_scope()
    locks = _locks()
    if result.get("predecessor_checkpoint", {}).get("source_blobs") != locks:
        raise AssertionError("L lock ledger drift")

    strata, specialized, supports = vg.vf.vd.reconstruct_context()
    banks = vg.vf._reconstruct_banks(strata, specialized, supports)
    factors = {
        ch: vg._factor_map(ch, strata) for ch in producer.CHANNEL_COORDINATE
    }
    blocker, records_inspected, ray_support_pairs = _scan(strata, banks, factors)
    emitted = result.get("characterized_blocker")
    if blocker is None:
        if emitted.get("kind") != "FINITE_RECIPROCAL_SPECTATOR_DOMAIN_NOT_ESTABLISHED":
            raise AssertionError("L producer blocker not reproduced independently")
    else:
        _compare_blocker_identity(emitted, blocker)
        _validate_seed(emitted, factors)
        dr, ds, dt = emitted["primitive_integer_ray"]
        if min(dr, ds, dt) < 0 or dt <= 0 or dr + ds == 0:
            raise AssertionError("invalid independent recession ray")

    domain = result.get("domain_analysis", {})
    if domain.get("candidate_records_inspected_for_support") != records_inspected:
        raise AssertionError("L support-record inspection count drift")
    if domain.get("ray_bearing_support_signature_pairs_inspected") != ray_support_pairs:
        raise AssertionError("L support-signature inspection count drift")
    if domain.get("feasible_support_seed_required") is not True:
        raise AssertionError("L feasibility gate missing")
    if domain.get("arbitrary_degree_cutoff_used") is not False:
        raise AssertionError("L degree-cutoff firewall drift")

    if result.get("terminal") != producer.BLOCKER_TERMINAL:
        raise AssertionError("L must stop at characterized blocker")
    if result.get("tested_record_count") != 0 or result.get("tested_records") != []:
        raise AssertionError("L must not truncate or pairing-scan an unbounded class")
    if (
        result.get("residual_sum_zero_proved") is not False
        or result.get("proof_effect") != "NONE"
        or result.get("promotion_effect") != "NONE"
        or result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER"
    ):
        raise AssertionError("L claim firewall drift")

    return {
        "operation": producer.OPERATION,
        "status": "INDEPENDENT_T3_011_L_SUPPORT_FEASIBILITY_REPLAY_COMPLETE",
        "characterized_blocker": emitted,
        "candidate_records_inspected_for_support": records_inspected,
        "ray_bearing_support_signature_pairs_inspected": ray_support_pairs,
        "tested_record_count": 0,
        "terminal": producer.BLOCKER_TERMINAL,
    }
