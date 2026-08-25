from __future__ import annotations

import math
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_e as producer
import verify_t3_011_d as vd

semantic = vd.semantic
d = vd.producer
a = vd.a
c = d.c
p = d.p
vc = vd.vc

def _sig_dict(sig):
    return {factor: int(exp) for factor, exp in sig if exp}

def _solve_power_reverse(base_sig, step_sig, target_sig):
    base = _sig_dict(base_sig)
    step = _sig_dict(step_sig)
    target = _sig_dict(target_sig)
    if not step:
        if base == target:
            raise AssertionError("independent coordinate specialization became constant")
        return None
    degree = None
    for factor in sorted(set(base) | set(step) | set(target), key=repr, reverse=True):
        delta = target.get(factor, 0) - base.get(factor, 0)
        stride = step.get(factor, 0)
        if stride == 0:
            if delta:
                return None
            continue
        q, r = divmod(delta, stride)
        if r or q < 0:
            return None
        if degree is None:
            degree = q
        elif degree != q:
            return None
    if degree is None:
        return None
    powers = dict(base)
    for factor, exp in step.items():
        powers[factor] = powers.get(factor, 0) + degree * exp
        if not powers[factor]:
            del powers[factor]
    if tuple(sorted(powers.items())) != target_sig:
        return None
    return degree

def _single_rat_monomial(rat, label):
    items = list(rat.items())
    if len(items) != 1:
        raise AssertionError(f"{label} is not a single independent Laurent monomial")
    sig, coeff = items[0]
    coeff = Q(coeff)
    if not coeff:
        raise AssertionError(f"{label} vanished")
    return sig, coeff

def _factor_map(channel, strata):
    out = {}
    for st in reversed(strata):
        x = a.specialize_rat(
            semantic.direct_coordinate_rat(channel), st["k_offset"], st["l_offset"]
        )
        xp = a.specialize_rat(
            semantic.direct_shifted_coordinate_rat(channel), st["k_offset"], st["l_offset"]
        )
        out[st["id"]] = {
            "x0": _single_rat_monomial(x, f"{channel}:{st['id']}:x0"),
            "x1": _single_rat_monomial(xp, f"{channel}:{st['id']}:x1"),
        }
    return out

def _group_vector(vec):
    out = {}
    for (cell_id, coord), coeff in vec.items():
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(coeff)))
    return out

def _group_witness(witness):
    out = {}
    for (cell_id, coord), weight in witness.items():
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(weight)))
    return out

def _moment(witness, base_vec, factor_map, kind):
    widx = _group_witness(witness)
    bidx = _group_vector(base_vec)
    aggregate = {}
    possible = set()
    evidence = {}
    for key in sorted(set(widx) & set(bidx), key=repr, reverse=True):
        cell_id, scalar, mon = key
        stratum = cell_id.split(":", 2)[2]
        step_sig, step_coeff = factor_map[stratum][kind]
        for target_sig, weight in reversed(widx[key]):
            for base_sig, coeff in reversed(bidx[key]):
                degree = _solve_power_reverse(base_sig, step_sig, target_sig)
                if degree is None:
                    continue
                possible.add(degree)
                value = weight * coeff * (step_coeff ** degree)
                aggregate[degree] = aggregate.get(degree, Q(0)) + value
                evidence.setdefault(degree, [
                    degree, cell_id, scalar, list(mon),
                    [[list(f), e] for f, e in base_sig],
                    [[list(f), e] for f, e in step_sig],
                    [[list(f), e] for f, e in target_sig],
                ])
    aggregate = {j: q for j, q in aggregate.items() if q}
    rows = [[j, q.numerator, q.denominator] for j, q in sorted(aggregate.items())]
    return {
        "possible_degrees": sorted(possible),
        "nonzero_degrees": sorted(aggregate),
        "coefficient_rows": rows,
        "aggregate": aggregate,
        "evidence": evidence,
    }

def _binomial_value(A, h, degree):
    return sum(
        (q * Q(math.comb(degree, j)) * (Q(h) ** (degree - j))
         for j, q in A.items() if j <= degree),
        Q(0),
    )

def _first_mismatch(A, C, h):
    if not A and not C:
        return None
    ma = max(A, default=-1)
    mc = max(C, default=-1)
    bound = max(ma, mc) + max(1, ma + 2)
    for degree in range(bound + 1):
        left = C.get(degree, Q(0))
        right = _binomial_value(A, h, degree)
        if left != right:
            return degree, left, right
    if A:
        raise AssertionError("independent nonzero binomial transform unexpectedly finite")
    return None

def _assert_d_locks_independent():
    got = {}
    for name, want in producer.D_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"independent D lock drift: {name}: {value} != {want}")
        got[name] = value
    return got

def _record(channel, uid, strata, active, witness, factors):
    scalar, mon = uid
    shift = a.pcl.SHIFTS[channel]
    shifted = semantic.direct_global_column_from_poly(
        semantic.direct_shifted_monomial(mon, shift), scalar, channel, strata, active
    )
    original = semantic.direct_global_column_from_poly(
        semantic.direct_original_monomial(mon), scalar, channel, strata, active
    )
    A = _moment(witness, shifted, factors, "x0")
    B = _moment(witness, original, factors, "x0")
    C = _moment(witness, shifted, factors, "x1")
    h = producer.CHANNEL_INCREMENT[channel]
    mismatch = _first_mismatch(A["aggregate"], C["aggregate"], h)

    values = []
    for degree in (0, 1, 2):
        value = _binomial_value(A["aggregate"], h, degree) - B["aggregate"].get(degree, Q(0))
        if value:
            raise AssertionError(f"independent certified degree drift {channel}:{uid}: d={degree}")
        values.append([degree, value.numerator, value.denominator])
    if mismatch is not None and mismatch[0] <= 2:
        raise AssertionError(f"independent semantic mismatch inside certified prefix: {channel}:{uid}")

    return {
        "A": A,
        "B": B,
        "C": C,
        "values": values,
        "mismatch": mismatch,
        "higher": sorted(j for j, q in B["aggregate"].items() if j > 2 and q),
    }

def verify(result: dict) -> dict:
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("T3-011-E identity drift")
    _assert_d_locks_independent()

    proof_route = result.get("proof_route", {})
    if proof_route.get("direct_higher_degree_response_scan_used"):
        raise AssertionError("T3-011-E illegally ran a higher-degree response scan")
    if proof_route.get("polynomial_sampling_used"):
        raise AssertionError("T3-011-E illegally used sampling")
    if proof_route.get("semantic_normal_form") != semantic.SEMANTIC_NORMAL_FORM:
        raise AssertionError("T3-011-E semantic normal form drift")

    strata, specialized, supports = vd.reconstruct_context()
    expected_records = result.get("candidate_records", [])
    index = 0
    first_ambiguity = None
    higher = set()
    k1_candidates = None

    for channel in list(a.INDEPENDENT_CHANNELS) + ["l1"]:
        base, ids, cols, target = vc.reconstruct_channel(channel, strata, specialized, supports)
        if base["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"independent E base drift: {channel}")
        candidates = [uid for uid, col in zip(ids, cols) if col]
        if channel in producer.EXPECTED_COUNTS and len(candidates) != producer.EXPECTED_COUNTS[channel]:
            raise AssertionError(f"independent E bank drift: {channel}")
        if channel == "k1":
            k1_candidates = list(candidates)
        if channel == "l1":
            if k1_candidates is None:
                raise AssertionError("independent l1 mirror source missing")
            candidates = [vc.mirror_unknown_k_to_l(uid) for uid in k1_candidates]
        witness = vd.frozen_canonical_witness(cols, target)
        active = vd.independent_active_namespace(channel, strata, specialized, supports)
        factors = _factor_map(channel, strata)

        for uid in candidates:
            if index >= len(expected_records):
                raise AssertionError("producer candidate record truncation")
            got = _record(channel, uid, strata, active, witness, factors)
            rec = expected_records[index]
            if rec.get("channel") != channel or rec.get("candidate") != [uid[0], list(uid[1])]:
                raise AssertionError(f"producer candidate order drift at {index}")
            for key, label in (
                ("shifted_x_moments", "A"),
                ("original_x_moments", "B"),
                ("shifted_opaque_moments", "C"),
            ):
                prod = rec[key]
                alt = got[label]
                if prod.get("possible_degrees") != alt["possible_degrees"]:
                    raise AssertionError(f"{channel}:{uid}:{label} possible-degree drift")
                if prod.get("nonzero_degrees") != alt["nonzero_degrees"]:
                    raise AssertionError(f"{channel}:{uid}:{label} nonzero-degree drift")
                if prod.get("coefficient_rows") != alt["coefficient_rows"]:
                    raise AssertionError(f"{channel}:{uid}:{label} coefficient drift")
            if rec.get("certified_semantic_lambda_0_2") != got["values"]:
                raise AssertionError(f"{channel}:{uid}: certified prefix drift")

            mismatch = got["mismatch"]
            invariant = mismatch is None
            if rec.get("semantic_functional_relation_invariant") != invariant:
                raise AssertionError(f"{channel}:{uid}: semantic-invariance flag drift")
            if mismatch is not None:
                expected = {
                    "degree": mismatch[0],
                    "direct_shifted_pairing": [mismatch[1].numerator, mismatch[1].denominator],
                    "binomial_expanded_shifted_pairing": [mismatch[2].numerator, mismatch[2].denominator],
                }
                if rec.get("first_semantic_relation_mismatch") != expected:
                    raise AssertionError(f"{channel}:{uid}: semantic mismatch witness drift")
                if first_ambiguity is None:
                    first_ambiguity = {"channel": channel, "candidate": rec["candidate"], **expected}
            else:
                if rec.get("finite_higher_degree_residue") != got["higher"]:
                    raise AssertionError(f"{channel}:{uid}: higher-degree residue drift")
                higher.update(got["higher"])
            index += 1

    if index != 421 or index != len(expected_records):
        raise AssertionError(f"T3-011-E complete candidate replay drift: {index}")

    if first_ambiguity is not None:
        terminal = producer.AMBIGUITY_TERMINAL
    elif higher:
        terminal = producer.FINITE_TERMINAL
    else:
        terminal = producer.CLOSURE_TERMINAL

    if result.get("terminal") != terminal:
        raise AssertionError("T3-011-E terminal drift")
    if result.get("semantic_functional_ambiguity") != first_ambiguity:
        raise AssertionError("T3-011-E first ambiguity drift")
    if result.get("higher_degree_set") != sorted(higher):
        raise AssertionError("T3-011-E higher-degree set drift")
    if result.get("first_unresolved_degree") != (min(higher) if higher else None):
        raise AssertionError("T3-011-E first unresolved degree drift")
    if result.get("all_single_channel_polynomial_multipliers_cokernel_invisible") != (
        terminal == producer.CLOSURE_TERMINAL
    ):
        raise AssertionError("T3-011-E closure flag drift")

    if result.get("residual_sum_zero_proved"):
        raise AssertionError("T3-011-E claim firewall inflation")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-011-E proof/promotion inflation")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3-011-E T3 status inflation")

    return {
        "stage": producer.STAGE,
        "status": "INDEPENDENT_T3_011_E_REPLAY_COMPLETE",
        "candidate_record_count": index,
        "terminal": terminal,
        "semantic_functional_ambiguity": first_ambiguity,
        "higher_degree_set": sorted(higher),
        "all_single_channel_polynomial_multipliers_cokernel_invisible":
            terminal == producer.CLOSURE_TERMINAL,
        "direct_higher_degree_response_scan_used": False,
        "polynomial_sampling_used": False,
        "semantic_normal_form": semantic.SEMANTIC_NORMAL_FORM,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
