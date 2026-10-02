from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
I_DIR = HERE.parent / "OZ_RT_BZ_T3_011_I"
G_DIR = HERE.parent / "OZ_RT_BZ_T3_010"
if str(G_DIR) not in sys.path:
    sys.path.insert(0, str(G_DIR))


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected predecessor module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


i = _load_module(I_DIR / "producer.py", "oz_t3_011_i_producer")
h = i.h
g = i.g
f = i.f
a = i.a

OPERATION = "OZ-RT-BZ-T3-011-J"
STAGE = "T3_011_J_MIXED_SIGN_LAURENT_COKERNEL_AUDIT"
ISSUE = 914
I_REVIEWED_HEAD = "9a305d7423cc7c258230865fa1d4deca7c9138e6"
I_MERGE_COMMIT = "76e11a33fd47e8a24f9aaf1d64788ceacfecd297"
I_REQUIRED_TERMINAL = "MIXED_RECIPROCAL_RESPONSE_CLASS_COKERNEL_INVISIBLE"
I_EXPECTED_RECORDS = 1282
I_BLOBS = {
    "producer.py": "a75d54047285ea7b109ab1ed0ad83a7650e55c7b",
    "CONTRACT.json": "89fd8f4186676ccb9dcc3989d5e6495f92cb3f8e",
    "verifier.py": "be75ec0ff1c7aec79c7c87063b6af3c485ec3e48",
}
ADMITTED_PAIRS = tuple(i.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(i.CHANNEL_COORDINATE)
FROZEN_RECORD_COUNT = i.FROZEN_RECORD_COUNT
ORIENTATIONS = (
    "positive_left_negative_right",
    "negative_left_positive_right",
)
POSSIBLE_RECORD_COUNT = FROZEN_RECORD_COUNT * len(ORIENTATIONS)

ESCAPE_TERMINAL = "MIXED_SIGN_LAURENT_RESPONSE_ESCAPE_FOUND"
CLOSURE_TERMINAL = "MIXED_SIGN_LAURENT_RESPONSE_CLASS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = "MIXED_SIGN_LAURENT_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
UNBOUNDED_TERMINAL = "MIXED_SIGN_LAURENT_RESPONSE_NOT_CERTIFIED__UNBOUNDED_SIGNATURE_OVERLAP"
BLOCKER_TERMINAL = "MIXED_SIGN_LAURENT_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"


class UnboundedSignatureOverlap(RuntimeError):
    def __init__(self, evidence: dict):
        super().__init__("mixed-sign Laurent signature overlap has an unbounded degree family")
        self.evidence = evidence


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def assert_i_locks() -> dict[str, str]:
    got = {}
    for name, want in I_BLOBS.items():
        value = a.git_blob_sha1(I_DIR / name)
        if value != want:
            raise AssertionError(f"T3-011-I source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((I_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-I":
        raise AssertionError("T3-011-I contract operation drift")
    if contract.get("terminals", {}).get("closure") != I_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-I closure terminal drift")
    return got


def validate_scope(
    shifted_poles: bool = False,
    arbitrary_rational_functions: bool = False,
    support_or_harmonic_enlargement: bool = False,
    candidate_bank_or_scalar_namespace_widening: bool = False,
    recurrence_widening: bool = False,
    correction_recombination: bool = False,
    candidate_linear_combinations: bool = False,
    trivariate_spectator_multipliers: bool = False,
) -> None:
    if shifted_poles or arbitrary_rational_functions:
        raise AssertionError("T3-011-J admits only coordinate-zero Laurent monomials")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening:
        raise AssertionError("T3-011-J forbids support, harmonic, candidate-bank, and scalar widening")
    if recurrence_widening or correction_recombination or candidate_linear_combinations:
        raise AssertionError("T3-011-J forbids recurrence, correction, and candidate recombination")
    if trivariate_spectator_multipliers:
        raise AssertionError("T3-011-J is pairwise only; spectator-coordinate multipliers are excluded")


def _sig_dict(sig) -> dict:
    return {factor: int(exp) for factor, exp in sig if exp}


def _sign(sig) -> int:
    values = [int(exp) for _factor, exp in sig if exp]
    if not values:
        raise AssertionError("coordinate specialization became constant")
    if all(exp > 0 for exp in values):
        return 1
    if all(exp < 0 for exp in values):
        return -1
    raise AssertionError("coordinate specialization is not a pure-sign Laurent monomial")


def _combine_sig(base_sig, left_sig, right_sig, r: int, s: int):
    out = _sig_dict(base_sig)
    for factor, exp in left_sig:
        out[factor] = out.get(factor, 0) + r * int(exp)
        if out[factor] == 0:
            del out[factor]
    for factor, exp in right_sig:
        out[factor] = out.get(factor, 0) + s * int(exp)
        if out[factor] == 0:
            del out[factor]
    return tuple(sorted(out.items()))


def _extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    d, x1, y1 = _extended_gcd(b, a % b)
    return d, y1, x1 - (a // b) * y1


def _ceil_div(a: int, b: int) -> int:
    if b <= 0:
        raise AssertionError("positive divisor required")
    return -((-a) // b)


@lru_cache(maxsize=None)
def _solve_mixed_sign_bidegrees(base_sig, left_sig, right_sig, target_sig):
    left_sign = _sign(left_sig)
    right_sign = _sign(right_sig)
    if left_sign == right_sign:
        raise AssertionError("T3-011-J requires opposite Laurent signs")

    base = _sig_dict(base_sig)
    target = _sig_dict(target_sig)
    if left_sign > 0:
        positive = _sig_dict(left_sig)
        negative = {factor: -exp for factor, exp in _sig_dict(right_sig).items()}
        positive_is_left = True
    else:
        positive = _sig_dict(right_sig)
        negative = {factor: -exp for factor, exp in _sig_dict(left_sig).items()}
        positive_is_left = False

    factors = sorted(set(base) | set(target) | set(positive) | set(negative))
    delta = {factor: target.get(factor, 0) - base.get(factor, 0) for factor in factors}

    pivot = None
    for index, first in enumerate(factors):
        for second in factors[index + 1 :]:
            det = (
                positive.get(first, 0) * (-negative.get(second, 0))
                - positive.get(second, 0) * (-negative.get(first, 0))
            )
            if det:
                pivot = (first, second, det)
                break
        if pivot is not None:
            break

    if pivot is not None:
        first, second, det = pivot
        num_positive = (
            delta[first] * (-negative.get(second, 0))
            - delta[second] * (-negative.get(first, 0))
        )
        num_inverse = (
            positive.get(first, 0) * delta[second]
            - positive.get(second, 0) * delta[first]
        )
        if num_positive % det or num_inverse % det:
            return ("finite", ())
        positive_degree = num_positive // det
        inverse_degree = num_inverse // det
        if positive_degree < 0 or inverse_degree < 0:
            return ("finite", ())
        if any(
            positive.get(factor, 0) * positive_degree
            - negative.get(factor, 0) * inverse_degree
            != delta[factor]
            for factor in factors
        ):
            return ("finite", ())
        degree = (
            (positive_degree, inverse_degree)
            if positive_is_left
            else (inverse_degree, positive_degree)
        )
        if _combine_sig(base_sig, left_sig, right_sig, *degree) != target_sig:
            raise AssertionError("mixed-sign rank-two solution reconstruction drift")
        return ("finite", (degree,))

    reference = next((factor for factor in factors if positive.get(factor, 0) > 0), None)
    if reference is None:
        raise AssertionError("positive coordinate specialization has no Laurent exponent")
    a_ref = positive[reference]
    b_ref = negative.get(reference, 0)
    if b_ref <= 0:
        return ("finite", ())
    d_ref = delta[reference]
    if any(
        delta[factor] * a_ref != d_ref * positive.get(factor, 0)
        for factor in factors
    ):
        return ("finite", ())

    divisor = gcd(a_ref, b_ref)
    if d_ref % divisor:
        return ("finite", ())
    d, x, y = _extended_gcd(a_ref, b_ref)
    if d != divisor:
        raise AssertionError("mixed-sign gcd reconstruction drift")
    multiple = d_ref // divisor
    positive0 = x * multiple
    inverse0 = -y * multiple
    positive_step = b_ref // divisor
    inverse_step = a_ref // divisor
    t0 = max(
        _ceil_div(-positive0, positive_step),
        _ceil_div(-inverse0, inverse_step),
    )
    positive0 += positive_step * t0
    inverse0 += inverse_step * t0
    if any(
        positive.get(factor, 0) * positive0
        - negative.get(factor, 0) * inverse0
        != delta[factor]
        for factor in factors
    ):
        raise AssertionError("mixed-sign rank-one solution reconstruction drift")

    base_degree = (
        (positive0, inverse0)
        if positive_is_left
        else (inverse0, positive0)
    )
    direction = (
        (positive_step, inverse_step)
        if positive_is_left
        else (inverse_step, positive_step)
    )
    if _combine_sig(base_sig, left_sig, right_sig, *base_degree) != target_sig:
        raise AssertionError("mixed-sign unbounded base reconstruction drift")
    if _combine_sig(
        base_sig,
        left_sig,
        right_sig,
        base_degree[0] + direction[0],
        base_degree[1] + direction[1],
    ) != target_sig:
        raise AssertionError("mixed-sign unbounded direction reconstruction drift")
    return ("unbounded", (base_degree, direction))


def mixed_sign_moment_ledger(
    witness_index: dict,
    base_index: dict,
    left_factors: dict,
    left_kind: str,
    right_factors: dict,
    right_kind: str,
    context: dict,
) -> dict:
    aggregate: dict[tuple[int, int], Q] = {}
    possible: set[tuple[int, int]] = set()
    matches = []
    first_evidence = {}
    for base_key in sorted(set(witness_index) & set(base_index), key=repr):
        cell_id, scalar, mon = base_key
        sid = g._stratum_id(cell_id)
        left_sig, left_coeff = left_factors[sid][left_kind]
        right_sig, right_coeff = right_factors[sid][right_kind]
        for target_sig, weight in witness_index[base_key]:
            for base_sig, coeff in base_index[base_key]:
                status, payload = _solve_mixed_sign_bidegrees(
                    base_sig, left_sig, right_sig, target_sig
                )
                if status == "unbounded":
                    base_degree, direction = payload
                    raise UnboundedSignatureOverlap(
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
                    contribution = weight * coeff * (left_coeff ** r) * (right_coeff ** s)
                    aggregate[(r, s)] = aggregate.get((r, s), Q(0)) + contribution
                    row = [
                        r,
                        s,
                        cell_id,
                        scalar,
                        list(mon),
                        qjson(weight),
                        qjson(coeff),
                        qjson(contribution),
                    ]
                    matches.append(row)
                    first_evidence.setdefault((r, s), row)
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [[r, s, *qjson(aggregate[(r, s)])] for r, s in sorted(aggregate)]
    return {
        "possible_bidegrees": [[r, s] for r, s in sorted(possible)],
        "nonzero_bidegrees": [[r, s] for r, s in sorted(aggregate)],
        "coefficient_rows": rows,
        "coefficient_sha256": sha(rows),
        "match_count": len(matches),
        "match_sha256": sha(matches),
        "first_evidence": {
            f"{r},{s}": first_evidence[(r, s)] for r, s in sorted(first_evidence)
        },
        "_aggregate": aggregate,
    }


def _strip_internal(ledger: dict) -> dict:
    return {key: value for key, value in ledger.items() if not key.startswith("_")}


def _direct_mixed_pairing(
    witness: dict, vec_gcd: dict, vec_gc: dict, vec_gd: dict, vec_g: dict
) -> Q:
    return sum(
        (
            Q(weight)
            * (
                Q(vec_gcd.get(key, 0))
                - Q(vec_gc.get(key, 0))
                - Q(vec_gd.get(key, 0))
                + Q(vec_g.get(key, 0))
            )
            for key, weight in witness.items()
        ),
        Q(0),
    )


def _axis_rows(ledgers: dict, axis: str) -> list[list[int]]:
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    if axis == "left":
        selected = [(r, 0) for r in sorted(r for r, s in domain if r >= 1 and s == 0)]
    elif axis == "right":
        selected = [(0, s) for s in sorted(s for r, s in domain if r == 0 and s >= 1)]
    else:
        raise AssertionError(f"unknown axis: {axis}")
    rows = []
    for r, s in selected:
        value = (
            ledgers["ScSd"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sc"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sd"]["_aggregate"].get((r, s), Q(0))
            + ledgers["I"]["_aggregate"].get((r, s), Q(0))
        )
        degree = r if axis == "left" else s
        rows.append([degree, *qjson(value)])
    return rows


def _candidate_record(
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
    vec_g, idx_g = g._cached_vector_index(endpoint, uid, (), strata, bank, poly_cache, vector_cache)
    vec_gc, idx_gc = g._cached_vector_index(endpoint, uid, (left,), strata, bank, poly_cache, vector_cache)
    vec_gd, idx_gd = g._cached_vector_index(endpoint, uid, (right,), strata, bank, poly_cache, vector_cache)
    vec_gcd, idx_gcd = g._cached_vector_index(endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache)

    if orientation == "positive_left_negative_right":
        left_maps = forward_factors[left]
        right_maps = inverse_factors[right]
        monomial_domain = "x_c^r*x_d^{-s}"
        positive_axis = "left"
        reciprocal_axis = "right"
    elif orientation == "negative_left_positive_right":
        left_maps = inverse_factors[left]
        right_maps = forward_factors[right]
        monomial_domain = "x_c^{-r}*x_d^s"
        positive_axis = "right"
        reciprocal_axis = "left"
    else:
        raise AssertionError(f"unknown mixed-sign orientation: {orientation}")

    ledgers = {}
    for name, base_index, left_kind, right_kind in (
        ("ScSd", idx_gcd, "x1", "x1"),
        ("Sc", idx_gc, "x1", "x0"),
        ("Sd", idx_gd, "x0", "x1"),
        ("I", idx_g, "x0", "x0"),
    ):
        ledgers[name] = mixed_sign_moment_ledger(
            witness_index,
            base_index,
            left_maps,
            left_kind,
            right_maps,
            right_kind,
            {
                "pair": list(pair),
                "endpoint": endpoint,
                "candidate": unknown_json(uid),
                "orientation": orientation,
                "monomial_domain": monomial_domain,
                "component": name,
            },
        )

    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    mixed_domain = {(r, s) for r, s in domain if r >= 1 and s >= 1}

    pairing_rows = []
    nonzero = []
    for r, s in sorted(mixed_domain):
        value = (
            ledgers["ScSd"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sc"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sd"]["_aggregate"].get((r, s), Q(0))
            + ledgers["I"]["_aggregate"].get((r, s), Q(0))
        )
        row = [r, s, *qjson(value)]
        pairing_rows.append(row)
        if value:
            nonzero.append(row)

    direct_component = (
        ledgers["ScSd"]["_aggregate"].get((0, 0), Q(0))
        - ledgers["Sc"]["_aggregate"].get((0, 0), Q(0))
        - ledgers["Sd"]["_aggregate"].get((0, 0), Q(0))
        + ledgers["I"]["_aggregate"].get((0, 0), Q(0))
    )
    direct_pairing = _direct_mixed_pairing(
        bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g
    )
    direct_anchor = direct_component == direct_pairing

    left_axis_rows = _axis_rows(ledgers, "left")
    right_axis_rows = _axis_rows(ledgers, "right")
    positive_rows = left_axis_rows if positive_axis == "left" else right_axis_rows
    reciprocal_rows = left_axis_rows if reciprocal_axis == "left" else right_axis_rows
    positive_anchor = all(num == 0 for _degree, num, _den in positive_rows)
    reciprocal_anchor = all(num == 0 for _degree, num, _den in reciprocal_rows)

    ambiguity = None
    if not direct_anchor:
        ambiguity = "DEGREE_0_0_COMPONENT_DECOMPOSITION_DISAGREES_WITH_DIRECT_MIXED_RESPONSE"
    elif not positive_anchor:
        ambiguity = "POSITIVE_AXIS_BOUNDARY_DISAGREES_WITH_PROTECTED_POLYNOMIAL_CLOSURE"
    elif not reciprocal_anchor:
        ambiguity = "RECIPROCAL_AXIS_BOUNDARY_DISAGREES_WITH_T3_011_H"

    return {
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "coordinate_pair": [CHANNEL_COORDINATE[left], CHANNEL_COORDINATE[right]],
        "orientation": orientation,
        "monomial_domain": monomial_domain,
        "finite_overlap_mixed_sign_bidegrees": [[r, s] for r, s in sorted(mixed_domain)],
        "finite_overlap_sha256": sha([[r, s] for r, s in sorted(mixed_domain)]),
        "component_ledgers": {
            name: _strip_internal(ledger) for name, ledger in ledgers.items()
        },
        "pairing_rows": pairing_rows,
        "pairing_sha256": sha(pairing_rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_bidegree": nonzero[0][:2] if nonzero else None,
        "degree_0_0_component_pairing": qjson(direct_component),
        "degree_0_0_direct_pairing": qjson(direct_pairing),
        "degree_0_0_semantics_exactly_match_direct": direct_anchor,
        "left_axis_pairing_rows": left_axis_rows,
        "right_axis_pairing_rows": right_axis_rows,
        "positive_axis_boundary_annihilated": positive_anchor,
        "reciprocal_axis_boundary_annihilated": reciprocal_anchor,
        "semantic_ambiguity_kind": ambiguity,
        "all_mixed_sign_bidegrees_annihilated": ambiguity is None and not nonzero,
    }


def _blocked_result(i_locks: dict[str, str], blocker, terminal: str = BLOCKER_TERMINAL) -> dict:
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "MIXED_SIGN_LAURENT_COKERNEL_AUDIT_BLOCKED",
        "predecessor_checkpoint": {
            "reviewed_head": I_REVIEWED_HEAD,
            "merge_commit": I_MERGE_COMMIT,
            "source_blobs": i_locks,
            "required_terminal": I_REQUIRED_TERMINAL,
            "expected_record_count": I_EXPECTED_RECORDS,
        },
        "possible_record_count": POSSIBLE_RECORD_COUNT,
        "tested_record_count": 0,
        "tested_records": [],
        "semantic_functional_ambiguity": None,
        "first_cokernel_breaking_direction": None,
        "characterized_blocker": blocker,
        "all_mixed_sign_laurent_responses_cokernel_invisible": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }


def build() -> dict:
    validate_scope()
    _solve_mixed_sign_bidegrees.cache_clear()
    i_locks = assert_i_locks()
    predecessor = i.build()
    if predecessor.get("terminal") != I_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-J requires exact protected I closure terminal")
    if predecessor.get("possible_record_count") != I_EXPECTED_RECORDS:
        raise AssertionError("T3-011-J I possible record count drift")
    if predecessor.get("tested_record_count") != I_EXPECTED_RECORDS:
        raise AssertionError("T3-011-J I tested record count drift")
    if predecessor.get("semantic_functional_ambiguity") is not None:
        raise AssertionError("T3-011-J requires I semantic ambiguity NONE")
    if predecessor.get("first_cokernel_breaking_direction") is not None:
        raise AssertionError("T3-011-J requires I cokernel-breaking direction NONE")

    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    try:
        forward_factors = {
            channel: g.e._coordinate_factors(channel, strata)
            for channel in CHANNEL_COORDINATE
        }
        inverse_factors = {
            channel: h.inverse_coordinate_factors(channel, strata)
            for channel in CHANNEL_COORDINATE
        }
    except AssertionError as exc:
        return _blocked_result(i_locks, {"kind": "COORDINATE_FACTOR_BLOCKER", "detail": str(exc)})

    witness_indexes = {
        channel: g._witness_index(bank["witness"])
        for channel, bank in banks.items()
    }
    poly_cache = {}
    vector_cache = {}
    records = []
    first_escape = None
    first_ambiguity = None
    first_unbounded = None
    stop = False

    for pair_index, pair in enumerate(ADMITTED_PAIRS):
        for orientation_index, orientation in enumerate(ORIENTATIONS):
            for endpoint_index, endpoint in enumerate(pair):
                bank = banks[endpoint]
                witness_index = witness_indexes[endpoint]
                for candidate_index, uid in enumerate(bank["candidates"]):
                    try:
                        rec = _candidate_record(
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
                        )
                    except UnboundedSignatureOverlap as exc:
                        first_unbounded = {
                            "ordinal": len(records),
                            "pair_index": pair_index,
                            "orientation_index": orientation_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                            **exc.evidence,
                        }
                        stop = True
                        break
                    rec.update(
                        {
                            "ordinal": len(records),
                            "pair_index": pair_index,
                            "orientation_index": orientation_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                        }
                    )
                    records.append(rec)
                    if rec["semantic_ambiguity_kind"] is not None:
                        first_ambiguity = rec
                        stop = True
                        break
                    if rec["nonzero_pairings"]:
                        r, s, num, den = rec["nonzero_pairings"][0]
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

    if first_unbounded is not None:
        terminal = UNBOUNDED_TERMINAL
    elif first_ambiguity is not None:
        terminal = AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = ESCAPE_TERMINAL
    else:
        if len(records) != POSSIBLE_RECORD_COUNT:
            raise AssertionError(
                f"T3-011-J exhaustive record drift: {len(records)} != {POSSIBLE_RECORD_COUNT}"
            )
        terminal = CLOSURE_TERMINAL

    cache_info = _solve_mixed_sign_bidegrees.cache_info()
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "MIXED_SIGN_LAURENT_COKERNEL_AUDIT_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": I_REVIEWED_HEAD,
            "merge_commit": I_MERGE_COMMIT,
            "source_blobs": i_locks,
            "required_terminal": I_REQUIRED_TERMINAL,
            "possible_record_count": predecessor["possible_record_count"],
            "tested_record_count": predecessor["tested_record_count"],
            "semantic_functional_ambiguity": predecessor["semantic_functional_ambiguity"],
            "first_cokernel_breaking_direction": predecessor["first_cokernel_breaking_direction"],
        },
        "mixed_sign_laurent_class": {
            "unordered_pair_order": [list(pair) for pair in ADMITTED_PAIRS],
            "orientation_order": list(ORIENTATIONS),
            "monomial_domains": [
                "x_c^r*x_d^{-s} with integers r>=1,s>=1",
                "x_c^{-r}*x_d^s with integers r>=1,s>=1",
            ],
            "only_poles": ["x_c=0", "x_d=0"],
            "finite_support_overlap_derived_without_degree_cutoff": terminal != UNBOUNDED_TERMINAL,
            "unbounded_signature_overlap_is_explicit_blocker": True,
            "positive_axis_boundaries_require_protected_polynomial_closure": True,
            "reciprocal_axis_boundaries_require_T3_011_H_closure": True,
            "negative_negative_quadrant_is_T3_011_I_closed": True,
            "shifted_poles_admitted": False,
            "arbitrary_rational_functions_admitted": False,
            "support_or_harmonic_enlargement_admitted": False,
            "candidate_bank_or_scalar_namespace_widening_admitted": False,
            "recurrence_search_admitted": False,
            "correction_layer_work_admitted": False,
            "candidate_linear_combinations_admitted": False,
            "trivariate_spectator_multipliers_admitted": False,
        },
        "execution_ledger": {
            "forward_coordinate_factor_maps": len(forward_factors),
            "inverse_coordinate_factor_maps": len(inverse_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "mixed_sign_solver_cache_hits": cache_info.hits,
            "mixed_sign_solver_cache_misses": cache_info.misses,
        },
        "possible_record_count": POSSIBLE_RECORD_COUNT,
        "tested_record_count": len(records),
        "tested_records": records,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "characterized_blocker": first_unbounded,
        "all_mixed_sign_laurent_responses_cokernel_invisible": terminal == CLOSURE_TERMINAL,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }


def main() -> int:
    print(json.dumps(build(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
