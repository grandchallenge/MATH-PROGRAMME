from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
H_DIR = HERE.parent / "OZ_RT_BZ_T3_011_H"
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


h = _load_module(H_DIR / "producer.py", "oz_t3_011_h_producer")
g = h.g
f = h.f
a = h.a

OPERATION = "OZ-RT-BZ-T3-011-I"
STAGE = "T3_011_I_MIXED_RECIPROCAL_LAURENT_COKERNEL_AUDIT"
ISSUE = 910
H_REVIEWED_HEAD = "154fda97329fa125965c5c78daa60c8939a6bbdb"
H_MERGE_COMMIT = "f8e1a3dfe005fd46c0999bb4d553be23bdc24231"
H_REQUIRED_TERMINAL = "RECIPROCAL_AXIS_RESPONSE_CLASS_COKERNEL_INVISIBLE"
H_EXPECTED_POSSIBLE_RECORDS = 2564
H_EXPECTED_TESTED_RECORDS = 2564
H_BLOBS = {
    "producer.py": "29ee99a0db47e1e8af0113527c0f939cda01b4eb",
    "CONTRACT.json": "4ad745b29e0cced1fe5cba76abfecf5daedf5975",
    "verifier.py": "192d802efe147cb64732912366d09f69cee52830",
}
ADMITTED_PAIRS = tuple(h.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(h.CHANNEL_COORDINATE)
FROZEN_RECORD_COUNT = h.G_FROZEN_RECORD_COUNT

ESCAPE_TERMINAL = "MIXED_RECIPROCAL_RESPONSE_ESCAPE_FOUND"
CLOSURE_TERMINAL = "MIXED_RECIPROCAL_RESPONSE_CLASS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = "MIXED_RECIPROCAL_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
BLOCKER_TERMINAL = "MIXED_RECIPROCAL_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def _candidate_key(candidate) -> tuple:
    return (candidate[0], tuple(candidate[1]))


def assert_h_locks() -> dict[str, str]:
    got = {}
    for name, want in H_BLOBS.items():
        value = a.git_blob_sha1(H_DIR / name)
        if value != want:
            raise AssertionError(f"T3-011-H source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((H_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-H":
        raise AssertionError("T3-011-H contract operation drift")
    if contract.get("terminals", {}).get("closure") != H_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-H closure terminal drift")
    return got


def validate_scope(
    shifted_poles: bool = False,
    positive_numerator_polynomials: bool = False,
    mixed_sign_laurent_monomials: bool = False,
    arbitrary_rational_functions: bool = False,
    support_or_harmonic_enlargement: bool = False,
    candidate_bank_or_scalar_namespace_widening: bool = False,
    recurrence_widening: bool = False,
    correction_recombination: bool = False,
    candidate_linear_combinations: bool = False,
) -> None:
    if shifted_poles or arbitrary_rational_functions:
        raise AssertionError("T3-011-I admits only the two protected coordinate-zero poles")
    if positive_numerator_polynomials or mixed_sign_laurent_monomials:
        raise AssertionError("T3-011-I admits exactly x_c^{-r} x_d^{-s}, r,s>=1")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening:
        raise AssertionError("T3-011-I forbids support, harmonic, candidate-bank, and scalar widening")
    if recurrence_widening or correction_recombination or candidate_linear_combinations:
        raise AssertionError("T3-011-I forbids recurrence, correction, and candidate recombination")


def _sig_dict(sig) -> dict:
    return {factor: int(exp) for factor, exp in sig if exp}


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


@lru_cache(maxsize=None)
def _solve_inverse_bidegrees(base_sig, left_sig, right_sig, target_sig):
    base = _sig_dict(base_sig)
    left_inv = _sig_dict(left_sig)
    right_inv = _sig_dict(right_sig)
    target = _sig_dict(target_sig)
    if not left_inv or not right_inv:
        raise AssertionError("reciprocal coordinate specialization became constant")
    if any(exp > 0 for exp in left_inv.values()) or any(exp > 0 for exp in right_inv.values()):
        raise AssertionError("reciprocal coordinate specialization has a positive Laurent step")

    left = {factor: -exp for factor, exp in left_inv.items()}
    right = {factor: -exp for factor, exp in right_inv.items()}
    deficit = {
        factor: base.get(factor, 0) - target.get(factor, 0)
        for factor in set(base) | set(left) | set(right) | set(target)
    }
    if any(value < 0 for value in deficit.values()):
        return ()

    def upper(step: dict) -> int:
        bounds = [deficit[factor] // exp for factor, exp in step.items() if exp > 0]
        if not bounds:
            raise AssertionError("reciprocal coordinate specialization has no negative Laurent exponent")
        return min(bounds)

    rmax = upper(left)
    smax = upper(right)
    out = []
    for r in range(rmax + 1):
        for s in range(smax + 1):
            if _combine_sig(base_sig, left_sig, right_sig, r, s) == target_sig:
                out.append((r, s))
    return tuple(out)


def inverse_bivariate_moment_ledger(
    witness_index: dict,
    base_index: dict,
    left_inverse_factors: dict,
    left_kind: str,
    right_inverse_factors: dict,
    right_kind: str,
) -> dict:
    aggregate: dict[tuple[int, int], Q] = {}
    possible: set[tuple[int, int]] = set()
    matches = []
    first_evidence = {}
    for base_key in sorted(set(witness_index) & set(base_index), key=repr):
        cell_id, scalar, mon = base_key
        sid = g._stratum_id(cell_id)
        left_sig, left_coeff = left_inverse_factors[sid][left_kind]
        right_sig, right_coeff = right_inverse_factors[sid][right_kind]
        for target_sig, weight in witness_index[base_key]:
            for base_sig, coeff in base_index[base_key]:
                for r, s in _solve_inverse_bidegrees(
                    base_sig, left_sig, right_sig, target_sig
                ):
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
    total = Q(0)
    for key, weight in witness.items():
        total += Q(weight) * (
            Q(vec_gcd.get(key, 0))
            - Q(vec_gc.get(key, 0))
            - Q(vec_gd.get(key, 0))
            + Q(vec_g.get(key, 0))
        )
    return total


def _axis_rows(ledgers: dict, side: str) -> list[list[int]]:
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_bidegrees"]))
    if side == "left":
        degrees = sorted(r for r, s in domain if r >= 1 and s == 0)
        return [
            [
                r,
                *qjson(
                    ledgers["ScSd"]["_aggregate"].get((r, 0), Q(0))
                    - ledgers["Sc"]["_aggregate"].get((r, 0), Q(0))
                    - ledgers["Sd"]["_aggregate"].get((r, 0), Q(0))
                    + ledgers["I"]["_aggregate"].get((r, 0), Q(0))
                ),
            ]
            for r in degrees
        ]
    if side == "right":
        degrees = sorted(s for r, s in domain if r == 0 and s >= 1)
        return [
            [
                s,
                *qjson(
                    ledgers["ScSd"]["_aggregate"].get((0, s), Q(0))
                    - ledgers["Sc"]["_aggregate"].get((0, s), Q(0))
                    - ledgers["Sd"]["_aggregate"].get((0, s), Q(0))
                    + ledgers["I"]["_aggregate"].get((0, s), Q(0))
                ),
            ]
            for s in degrees
        ]
    raise AssertionError(f"unknown axis side: {side}")


def _h_record_index(h_result: dict) -> dict:
    out = {}
    for rec in h_result["tested_records"]:
        key = (
            tuple(rec["pair"]),
            rec["endpoint"],
            _candidate_key(rec["candidate"]),
            rec["prefactor_channel"],
        )
        if key in out:
            raise AssertionError(f"duplicate T3-011-H predecessor record: {key}")
        out[key] = rec
    return out


def _candidate_record(
    pair,
    endpoint,
    uid,
    strata,
    bank,
    witness_index,
    inverse_factors,
    h_index,
    poly_cache,
    vector_cache,
):
    left, right = pair
    vec_g, idx_g = g._cached_vector_index(endpoint, uid, (), strata, bank, poly_cache, vector_cache)
    vec_gc, idx_gc = g._cached_vector_index(endpoint, uid, (left,), strata, bank, poly_cache, vector_cache)
    vec_gd, idx_gd = g._cached_vector_index(endpoint, uid, (right,), strata, bank, poly_cache, vector_cache)
    vec_gcd, idx_gcd = g._cached_vector_index(endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache)

    left_factors = inverse_factors[left]
    right_factors = inverse_factors[right]
    ledgers = {
        "ScSd": inverse_bivariate_moment_ledger(witness_index, idx_gcd, left_factors, "x1", right_factors, "x1"),
        "Sc": inverse_bivariate_moment_ledger(witness_index, idx_gc, left_factors, "x1", right_factors, "x0"),
        "Sd": inverse_bivariate_moment_ledger(witness_index, idx_gd, left_factors, "x0", right_factors, "x1"),
        "I": inverse_bivariate_moment_ledger(witness_index, idx_g, left_factors, "x0", right_factors, "x0"),
    }

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
    direct_pairing = _direct_mixed_pairing(bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g)

    left_axis_rows = _axis_rows(ledgers, "left")
    right_axis_rows = _axis_rows(ledgers, "right")
    uid_key = _candidate_key(unknown_json(uid))
    left_h = h_index[(tuple(pair), endpoint, uid_key, left)]
    right_h = h_index[(tuple(pair), endpoint, uid_key, right)]
    left_anchor = left_axis_rows == left_h["pairing_rows"]
    right_anchor = right_axis_rows == right_h["pairing_rows"]
    direct_anchor = direct_component == direct_pairing

    ambiguity = None
    if not direct_anchor:
        ambiguity = "DEGREE_0_0_COMPONENT_DECOMPOSITION_DISAGREES_WITH_DIRECT_MIXED_RESPONSE"
    elif not left_anchor:
        ambiguity = "LEFT_RECIPROCAL_AXIS_BOUNDARY_DISAGREES_WITH_T3_011_H"
    elif not right_anchor:
        ambiguity = "RIGHT_RECIPROCAL_AXIS_BOUNDARY_DISAGREES_WITH_T3_011_H"

    return {
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "coordinate_pair": [CHANNEL_COORDINATE[left], CHANNEL_COORDINATE[right]],
        "finite_overlap_mixed_reciprocal_bidegrees": [[r, s] for r, s in sorted(mixed_domain)],
        "finite_overlap_sha256": sha([[r, s] for r, s in sorted(mixed_domain)]),
        "component_ledgers": {name: _strip_internal(ledger) for name, ledger in ledgers.items()},
        "pairing_rows": pairing_rows,
        "pairing_sha256": sha(pairing_rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_bidegree": nonzero[0][:2] if nonzero else None,
        "degree_0_0_component_pairing": qjson(direct_component),
        "degree_0_0_direct_pairing": qjson(direct_pairing),
        "degree_0_0_semantics_exactly_match_direct": direct_anchor,
        "left_axis_pairing_rows": left_axis_rows,
        "left_H_pairing_rows": left_h["pairing_rows"],
        "left_axis_semantics_exactly_match_H": left_anchor,
        "right_axis_pairing_rows": right_axis_rows,
        "right_H_pairing_rows": right_h["pairing_rows"],
        "right_axis_semantics_exactly_match_H": right_anchor,
        "semantic_ambiguity_kind": ambiguity,
        "all_mixed_reciprocal_bidegrees_annihilated": ambiguity is None and not nonzero,
    }


def _blocker_result(h_locks: dict[str, str], blocker: str) -> dict:
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "MIXED_RECIPROCAL_LAURENT_COKERNEL_AUDIT_BLOCKED",
        "predecessor_checkpoint": {
            "reviewed_head": H_REVIEWED_HEAD,
            "merge_commit": H_MERGE_COMMIT,
            "source_blobs": h_locks,
            "required_terminal": H_REQUIRED_TERMINAL,
            "possible_record_count": H_EXPECTED_POSSIBLE_RECORDS,
            "tested_record_count": H_EXPECTED_TESTED_RECORDS,
        },
        "characterized_blocker": blocker,
        "possible_record_count": FROZEN_RECORD_COUNT,
        "tested_record_count": 0,
        "tested_records": [],
        "semantic_functional_ambiguity": None,
        "first_cokernel_breaking_direction": None,
        "all_mixed_reciprocal_responses_cokernel_invisible": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": BLOCKER_TERMINAL,
    }


def build() -> dict:
    validate_scope()
    _solve_inverse_bidegrees.cache_clear()
    h_locks = assert_h_locks()
    h_result = h.build()
    if h_result.get("terminal") != H_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-I requires exact protected H closure terminal")
    if h_result.get("possible_record_count") != H_EXPECTED_POSSIBLE_RECORDS:
        raise AssertionError("T3-011-I H possible record count drift")
    if h_result.get("tested_record_count") != H_EXPECTED_TESTED_RECORDS:
        raise AssertionError("T3-011-I H tested record count drift")
    if h_result.get("semantic_functional_ambiguity") is not None:
        raise AssertionError("T3-011-I requires H semantic ambiguity NONE")
    if h_result.get("first_cokernel_breaking_direction") is not None:
        raise AssertionError("T3-011-I requires H cokernel-breaking direction NONE")

    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    try:
        inverse_factors = {channel: h.inverse_coordinate_factors(channel, strata) for channel in CHANNEL_COORDINATE}
    except AssertionError as exc:
        return _blocker_result(h_locks, str(exc))

    h_index = _h_record_index(h_result)
    witness_indexes = {channel: g._witness_index(bank["witness"]) for channel, bank in banks.items()}
    poly_cache = {}
    vector_cache = {}

    records = []
    first_escape = None
    first_ambiguity = None
    stop = False

    for pair_index, pair in enumerate(ADMITTED_PAIRS):
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            witness_index = witness_indexes[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                rec = _candidate_record(pair, endpoint, uid, strata, bank, witness_index, inverse_factors, h_index, poly_cache, vector_cache)
                rec.update({
                    "ordinal": len(records),
                    "pair_index": pair_index,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                })
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
                        "reciprocal_bidegree": [r, s],
                        "normalized_cokernel_pairing": [num, den],
                    }
                    stop = True
                    break
            if stop:
                break
        if stop:
            break

    if first_ambiguity is not None:
        terminal = AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = ESCAPE_TERMINAL
    else:
        if len(records) != FROZEN_RECORD_COUNT:
            raise AssertionError(f"T3-011-I exhaustive record drift: {len(records)} != {FROZEN_RECORD_COUNT}")
        terminal = CLOSURE_TERMINAL

    cache_info = _solve_inverse_bidegrees.cache_info()
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "MIXED_RECIPROCAL_LAURENT_COKERNEL_AUDIT_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": H_REVIEWED_HEAD,
            "merge_commit": H_MERGE_COMMIT,
            "source_blobs": h_locks,
            "required_terminal": H_REQUIRED_TERMINAL,
            "possible_record_count": h_result["possible_record_count"],
            "tested_record_count": h_result["tested_record_count"],
            "semantic_functional_ambiguity": h_result["semantic_functional_ambiguity"],
            "first_cokernel_breaking_direction": h_result["first_cokernel_breaking_direction"],
        },
        "mixed_reciprocal_class": {
            "unordered_pair_order": [list(pair) for pair in ADMITTED_PAIRS],
            "monomial_domain": "x_c^{-r}*x_d^{-s} with integers r>=1,s>=1",
            "only_poles": ["x_c=0", "x_d=0"],
            "nonzero_laurent_specialization_required": True,
            "finite_support_overlap_derived_without_degree_cutoff": True,
            "pure_reciprocal_axes_are_H_boundary_anchors": True,
            "degree_zero_is_direct_response_anchor": True,
            "shifted_poles_admitted": False,
            "positive_numerator_polynomials_admitted": False,
            "mixed_sign_laurent_monomials_admitted": False,
            "arbitrary_rational_functions_admitted": False,
            "support_or_harmonic_enlargement_admitted": False,
            "candidate_bank_or_scalar_namespace_widening_admitted": False,
            "recurrence_search_admitted": False,
            "correction_layer_work_admitted": False,
            "candidate_linear_combinations_admitted": False,
        },
        "execution_ledger": {
            "inverse_coordinate_factor_maps": len(inverse_factors),
            "pole_safety_strata_checked": sum(len(value) for value in inverse_factors.values()),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "bidegree_solver_cache_hits": cache_info.hits,
            "bidegree_solver_cache_misses": cache_info.misses,
        },
        "possible_record_count": FROZEN_RECORD_COUNT,
        "tested_record_count": len(records),
        "tested_records": records,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_mixed_reciprocal_responses_cokernel_invisible": terminal == CLOSURE_TERMINAL,
        "characterized_blocker": None,
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
