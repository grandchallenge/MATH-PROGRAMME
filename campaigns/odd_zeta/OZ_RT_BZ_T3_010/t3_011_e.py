from __future__ import annotations

import hashlib
import json
import math
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_c as semantic
import t3_011_d as d

p = d.p
c = d.c
b = d.b
a = d.a

OPERATION = "OZ-RT-BZ-T3-011-E"
STAGE = "T3_011_E_POLYNOMIAL_MULTIPLIER_COKERNEL_CLOSURE_AUDIT"
ISSUE = 505
D_REVIEWED_HEAD = "5fecbf600763b5e0e4914000a5c7729213a00393"
D_MERGE_COMMIT = "956d5a89a16ec29a369099de049f5e03c98539b0"
D_REQUIRED_TERMINAL = "SINGLE_CHANNEL_QUADRATIC_RESPONSE_CLASS_COKERNEL_INVISIBLE"
D_BLOBS = {
    "t3_011_d.py": "10e5dae57d6e506e69a5fa8547407cecd7f33c89",
    "T3_011_D_CONTRACT.json": "91be1d3ffdb644d235a1d334d992496fb6ee2a98",
    "verify_t3_011_d.py": "c3b45ef72f8ee5e1681e6d4b4128a7c4d3c883ca",
}
EXPECTED_COUNTS = dict(d.EXPECTED_COUNTS)
CHANNEL_INCREMENT = dict(d.CHANNEL_INCREMENT)
CLOSURE_TERMINAL = "POLYNOMIAL_MULTIPLIER_COKERNEL_CLOSURE_CERTIFIED"
FINITE_TERMINAL = "POLYNOMIAL_CLOSURE_REDUCES_TO_FINITE_HIGHER_DEGREE_SET"
AMBIGUITY_TERMINAL = "POLYNOMIAL_CLOSURE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
BLOCKER_TERMINAL = "POLYNOMIAL_CLOSURE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"

def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]

def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]

def assert_d_locks() -> dict[str, str]:
    got = {}
    for name, want in D_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"T3-011-D source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_011_D_CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-D":
        raise AssertionError("T3-011-D contract operation drift")
    if contract.get("terminals", {}).get("negative") != D_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-D negative terminal drift")
    if contract.get("bounded_extension_class", {}).get("expected_independent_trials") != 311:
        raise AssertionError("T3-011-D independent bank drift")
    return got

def validate_scope(
    direct_higher_degree_scan: bool = False,
    mixed_channels: bool = False,
    pair_search: bool = False,
    polynomial_sampling: bool = False,
) -> None:
    if direct_higher_degree_scan:
        raise AssertionError("T3-011-E forbids direct degree-3-or-higher response scans")
    if mixed_channels:
        raise AssertionError("T3-011-E forbids mixed-channel multipliers")
    if pair_search:
        raise AssertionError("T3-011-E forbids pair/two-lift search")
    if polynomial_sampling:
        raise AssertionError("T3-011-E forbids numerical/polynomial sampling in place of proof")

def _sig_dict(sig) -> dict:
    return {factor: int(exp) for factor, exp in sig if exp}

def _sig_add_power(sig, step_sig, degree: int):
    powers = _sig_dict(sig)
    for factor, exp in step_sig:
        powers[factor] = powers.get(factor, 0) + degree * int(exp)
        if not powers[factor]:
            del powers[factor]
    return tuple(sorted(powers.items()))

def _solve_power(base_sig, step_sig, target_sig) -> int | None:
    base = _sig_dict(base_sig)
    step = _sig_dict(step_sig)
    target = _sig_dict(target_sig)
    if not step:
        if base == target:
            raise AssertionError("coordinate specialization became constant: infinite raw support")
        return None
    candidate = None
    for factor in set(base) | set(step) | set(target):
        diff = target.get(factor, 0) - base.get(factor, 0)
        s = step.get(factor, 0)
        if not s:
            if diff:
                return None
            continue
        if diff % s:
            return None
        value = diff // s
        if value < 0:
            return None
        if candidate is None:
            candidate = value
        elif candidate != value:
            return None
    if candidate is None:
        return None
    if _sig_add_power(base_sig, step_sig, candidate) != target_sig:
        return None
    return candidate

def _single_rat_monomial(rat, label: str):
    if len(rat) != 1:
        raise AssertionError(f"{label} is not a single Laurent monomial")
    (sig, coeff), = rat.items()
    coeff = Q(coeff)
    if not coeff:
        raise AssertionError(f"{label} specialized to zero")
    return sig, coeff

def _coordinate_factors(channel: str, strata: list[dict]):
    out = {}
    for st in strata:
        x0 = a.specialize_rat(
            semantic.direct_coordinate_rat(channel), st["k_offset"], st["l_offset"]
        )
        x1 = a.specialize_rat(
            semantic.direct_shifted_coordinate_rat(channel), st["k_offset"], st["l_offset"]
        )
        out[st["id"]] = {
            "x0": _single_rat_monomial(x0, f"{channel}:{st['id']}:x0"),
            "x1": _single_rat_monomial(x1, f"{channel}:{st['id']}:x1"),
        }
    return out

def _base_index(vec: dict):
    out = {}
    for (cell_id, coord), coeff in vec.items():
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(coeff)))
    return out

def _witness_index(witness: dict):
    out = {}
    for (cell_id, coord), weight in witness.items():
        scalar, mon, sig = coord
        out.setdefault((cell_id, scalar, mon), []).append((sig, Q(weight)))
    return out

def _stratum_id(cell_id: str) -> str:
    return cell_id.split(":", 2)[2]

def moment_ledger(witness: dict, base_vec: dict, factor_by_stratum: dict, factor_kind: str):
    widx = _witness_index(witness)
    bidx = _base_index(base_vec)
    aggregate: dict[int, Q] = {}
    possible: set[int] = set()
    first_evidence: dict[int, list] = {}
    detailed = []
    for base_key in sorted(set(widx) & set(bidx), key=repr):
        cell_id, scalar, mon = base_key
        step_sig, step_coeff = factor_by_stratum[_stratum_id(cell_id)][factor_kind]
        for target_sig, weight in widx[base_key]:
            for base_sig, coeff in bidx[base_key]:
                degree = _solve_power(base_sig, step_sig, target_sig)
                if degree is None:
                    continue
                possible.add(degree)
                contribution = weight * coeff * (step_coeff ** degree)
                aggregate[degree] = aggregate.get(degree, Q(0)) + contribution
                row = [
                    degree,
                    cell_id,
                    scalar,
                    list(mon),
                    [[list(f), e] for f, e in base_sig],
                    [[list(f), e] for f, e in step_sig],
                    [[list(f), e] for f, e in target_sig],
                    qjson(weight),
                    qjson(coeff),
                    qjson(contribution),
                ]
                detailed.append(row)
                first_evidence.setdefault(degree, row)
    aggregate = {j: q for j, q in aggregate.items() if q}
    rows = [[j, *qjson(aggregate[j])] for j in sorted(aggregate)]
    return {
        "possible_degrees": sorted(possible),
        "nonzero_degrees": sorted(aggregate),
        "coefficient_rows": rows,
        "coefficient_sha256": sha(rows),
        "match_count": len(detailed),
        "match_sha256": sha(detailed),
        "first_evidence": {str(j): first_evidence[j] for j in sorted(first_evidence)},
        "_aggregate": aggregate,
    }

def _sequence_value(moment: dict[int, Q], h: int, degree: int) -> Q:
    total = Q(0)
    for j, coeff in moment.items():
        if j <= degree:
            total += coeff * Q(math.comb(degree, j)) * (Q(h) ** (degree - j))
    return total

def _first_semantic_mismatch(A: dict[int, Q], C: dict[int, Q], h: int) -> tuple[int, Q, Q] | None:
    if not A and not C:
        return None
    max_a = max(A, default=-1)
    max_c = max(C, default=-1)
    bound = max(max_a, max_c) + max(1, max_a + 2)
    for degree in range(bound + 1):
        semantic_value = _sequence_value(A, h, degree)
        direct_value = C.get(degree, Q(0))
        if semantic_value != direct_value:
            return degree, direct_value, semantic_value
    if A:
        raise AssertionError("nonzero binomial moment sequence matched a finite-support sequence beyond proof bound")
    return None

def _strip_internal(ledger: dict) -> dict:
    return {k: v for k, v in ledger.items() if not k.startswith("_")}

def _candidate_record(channel, uid, strata, active, witness, coordinate_factors):
    scalar, mon = uid
    shift = a.pcl.SHIFTS[channel]
    shifted_raw = semantic.direct_shifted_monomial(mon, shift)
    original_raw = semantic.direct_original_monomial(mon)
    shifted = semantic.direct_global_column_from_poly(shifted_raw, scalar, channel, strata, active)
    original = semantic.direct_global_column_from_poly(original_raw, scalar, channel, strata, active)

    A = moment_ledger(witness, shifted, coordinate_factors, "x0")
    B = moment_ledger(witness, original, coordinate_factors, "x0")
    C = moment_ledger(witness, shifted, coordinate_factors, "x1")
    h = CHANNEL_INCREMENT[channel]

    mismatch = _first_semantic_mismatch(A["_aggregate"], C["_aggregate"], h)
    semantic_lambda_0_2 = []
    for degree in (0, 1, 2):
        value = _sequence_value(A["_aggregate"], h, degree) - B["_aggregate"].get(degree, Q(0))
        semantic_lambda_0_2.append([degree, *qjson(value)])
        if value:
            raise AssertionError(
                f"certified degree-0/1/2 annihilation drift: {channel}:{uid}: d={degree}: {value}"
            )

    if mismatch is not None and mismatch[0] <= 2:
        raise AssertionError(
            f"predecessor semantic invariance drift at certified degree {mismatch[0]}: {channel}:{uid}"
        )

    higher = sorted(j for j, q in B["_aggregate"].items() if j > 2 and q)
    return {
        "channel": channel,
        "candidate": unknown_json(uid),
        "shifted_x_moments": _strip_internal(A),
        "original_x_moments": _strip_internal(B),
        "shifted_opaque_moments": _strip_internal(C),
        "certified_semantic_lambda_0_2": semantic_lambda_0_2,
        "semantic_functional_relation_invariant": mismatch is None,
        "first_semantic_relation_mismatch": (
            None if mismatch is None else {
                "degree": mismatch[0],
                "direct_shifted_pairing": qjson(mismatch[1]),
                "binomial_expanded_shifted_pairing": qjson(mismatch[2]),
            }
        ),
        "finite_higher_degree_residue": higher if mismatch is None else [],
        "all_polynomial_degrees_annihilated": mismatch is None and not higher,
    }

def build() -> dict:
    validate_scope()
    d_locks = assert_d_locks()
    primitive_full, strata, specialized, supports = d.build_context()

    records = []
    channels = []
    first_ambiguity = None
    higher_degrees: set[int] = set()
    higher_evidence = {}
    k1_candidates = None

    scan_channels = list(a.INDEPENDENT_CHANNELS) + ["l1"]
    for channel in scan_channels:
        base, ids, cols, target, candidates, active, witness, residual = d.channel_bank(
            channel, primitive_full, strata, specialized, supports
        )
        if channel == "k1":
            k1_candidates = list(candidates)
        if channel == "l1":
            if k1_candidates is None:
                raise AssertionError("k1 mirror source missing before l1")
            candidates = [c.mirror_unknown_k_to_l(uid) for uid in k1_candidates]
            if len(candidates) != 110:
                raise AssertionError("l1 mirror cardinality drift")
        factors = _coordinate_factors(channel, strata)
        start = len(records)
        for uid in candidates:
            rec = _candidate_record(channel, uid, strata, active, witness, factors)
            records.append(rec)
            if first_ambiguity is None and not rec["semantic_functional_relation_invariant"]:
                first_ambiguity = {
                    "channel": channel,
                    "candidate": rec["candidate"],
                    **rec["first_semantic_relation_mismatch"],
                }
            if rec["semantic_functional_relation_invariant"]:
                for degree in rec["finite_higher_degree_residue"]:
                    higher_degrees.add(degree)
                    higher_evidence.setdefault(str(degree), {
                        "channel": channel,
                        "candidate": rec["candidate"],
                        "original_moment_evidence":
                            rec["original_x_moments"]["first_evidence"].get(str(degree)),
                    })
        channels.append({
            "channel": channel,
            "candidate_count": len(candidates),
            "candidate_order_sha256": sha([unknown_json(uid) for uid in candidates]),
            "active_cell_count": len(active),
            "active_cell_sha256": sha(sorted(active)),
            "cokernel_witness_sha256": p.sha(p.witness_rows(witness)),
            "target_quotient_residual_sha256": c.global_vector_digest(residual),
            "record_start": start,
            "record_count": len(candidates),
        })

    if len(records) != 421:
        raise AssertionError(f"T3-011-E candidate total drift: {len(records)}")

    if first_ambiguity is not None:
        terminal = AMBIGUITY_TERMINAL
    elif higher_degrees:
        terminal = FINITE_TERMINAL
    else:
        terminal = CLOSURE_TERMINAL

    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "POLYNOMIAL_MULTIPLIER_COKERNEL_CLOSURE_AUDIT_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": D_REVIEWED_HEAD,
            "merge_commit": D_MERGE_COMMIT,
            "source_blobs": d_locks,
            "required_terminal": D_REQUIRED_TERMINAL,
        },
        "proof_route": {
            "direct_higher_degree_response_scan_used": False,
            "polynomial_sampling_used": False,
            "moment_basis": [
                "<w,x^j S(G)>",
                "<w,x^j G>",
                "<w,(x+h)^j S(G)>",
            ],
            "semantic_identity":
                "<w,(x+h)^dS-x^dG>=sum_j binom(d,j)h^(d-j)<w,x^jS>-<w,x^dG>",
            "finite_support_reason":
                "frozen witness support makes each raw moment ledger finite; all-d comparison is then exact by the binomial transform",
            "semantic_normal_form": semantic.SEMANTIC_NORMAL_FORM,
        },
        "channel_ledgers": channels,
        "candidate_record_count": len(records),
        "candidate_records": records,
        "semantic_functional_ambiguity": first_ambiguity,
        "higher_degree_set": sorted(higher_degrees),
        "first_unresolved_degree": min(higher_degrees) if higher_degrees else None,
        "higher_degree_evidence": higher_evidence,
        "all_single_channel_polynomial_multipliers_cokernel_invisible":
            terminal == CLOSURE_TERMINAL,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }
