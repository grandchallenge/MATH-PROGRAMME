from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREDECESSOR_DIR = HERE.parent / "OZ_RT_BZ_T3_010"
if str(PREDECESSOR_DIR) not in sys.path:
    sys.path.insert(0, str(PREDECESSOR_DIR))

import t3_011_e as e
import t3_011_f as f
import t3_011_g as g

semantic = g.semantic
a = g.a
p = g.p

OPERATION = "OZ-RT-BZ-T3-011-H"
STAGE = "T3_011_H_RECIPROCAL_AXIS_RATIONAL_PREFACTOR_ESCAPE_AUDIT"
ISSUE = 908
G_REVIEWED_HEAD = "4ece26a9bbe27d0a3a84c8d291e2a32210f14b63"
G_MERGE_COMMIT = "abd1ce5be6d61cf8ed3c79a9f4d7be246c76be60"
G_REQUIRED_TERMINAL = "MIXED_POLYNOMIAL_MULTIPLIER_COKERNEL_CLOSURE_CERTIFIED"
G_FROZEN_RECORD_COUNT = 1282
G_BLOBS = {
    "t3_011_g.py": "388f217c53d6100e34c488bbe2c75cdcec394d99",
    "T3_011_G_CONTRACT.json": "b0c26d8b7b5015c53cb364e2b8a35cb2245bdaa5",
    "verify_t3_011_g.py": "8cc00a1f0f1e32f84b4536ee044b5a1fb2b5c997",
}
ADMITTED_PAIRS = tuple(g.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(g.CHANNEL_COORDINATE)
ESCAPE_TERMINAL = "RECIPROCAL_AXIS_RESPONSE_ESCAPE_FOUND"
CLOSURE_TERMINAL = "RECIPROCAL_AXIS_RESPONSE_CLASS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = "RECIPROCAL_AXIS_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
BLOCKER_TERMINAL = "RECIPROCAL_AXIS_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def assert_g_locks() -> dict[str, str]:
    got = {}
    for name, want in G_BLOBS.items():
        value = a.git_blob_sha1(PREDECESSOR_DIR / name)
        if value != want:
            raise AssertionError(f"T3-011-G source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((PREDECESSOR_DIR / "T3_011_G_CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-G":
        raise AssertionError("T3-011-G contract operation drift")
    if contract.get("terminals", {}).get("closure") != G_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-G closure terminal drift")
    return got


def validate_scope(
    shifted_poles: bool = False,
    mixed_reciprocal_products: bool = False,
    positive_numerator_polynomials: bool = False,
    arbitrary_rational_functions: bool = False,
    support_or_harmonic_enlargement: bool = False,
    candidate_bank_or_scalar_namespace_widening: bool = False,
    recurrence_widening: bool = False,
    correction_recombination: bool = False,
    candidate_linear_combinations: bool = False,
) -> None:
    if shifted_poles or arbitrary_rational_functions:
        raise AssertionError("T3-011-H admits only coordinate-zero reciprocal monomials")
    if mixed_reciprocal_products or positive_numerator_polynomials:
        raise AssertionError("T3-011-H admits exactly one reciprocal axis and no numerator widening")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening:
        raise AssertionError("T3-011-H forbids support, harmonic, candidate-bank, and scalar widening")
    if recurrence_widening or correction_recombination or candidate_linear_combinations:
        raise AssertionError("T3-011-H forbids recurrence, correction, and candidate recombination")


def _invert_factor(factor, label: str):
    sig, coeff = factor
    coeff = Q(coeff)
    if not coeff:
        raise AssertionError(f"{label} coordinate specialization is zero")
    inv_sig = tuple(sorted((name, -int(exp)) for name, exp in sig if exp))
    if not inv_sig:
        raise AssertionError(f"{label} coordinate specialization is constant; reciprocal degree is not identifiable")
    return inv_sig, Q(1, 1) / coeff


def inverse_coordinate_factors(channel: str, strata: list[dict]) -> dict:
    forward = e._coordinate_factors(channel, strata)
    return {
        sid: {
            kind: _invert_factor(value, f"{channel}:{sid}:{kind}")
            for kind, value in factors.items()
        }
        for sid, factors in forward.items()
    }


def reciprocal_moment_ledger(
    witness_index: dict,
    base_index: dict,
    inverse_factors: dict,
    factor_kind: str,
) -> dict:
    aggregate: dict[int, Q] = {}
    possible: set[int] = set()
    matches = []
    first_evidence = {}
    for base_key in sorted(set(witness_index) & set(base_index), key=repr):
        cell_id, scalar, mon = base_key
        sid = g._stratum_id(cell_id)
        step_sig, step_coeff = inverse_factors[sid][factor_kind]
        for target_sig, weight in witness_index[base_key]:
            for base_sig, coeff in base_index[base_key]:
                degree = e._solve_power(base_sig, step_sig, target_sig)
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
                    qjson(weight),
                    qjson(coeff),
                    qjson(contribution),
                ]
                matches.append(row)
                first_evidence.setdefault(degree, row)
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [[degree, *qjson(aggregate[degree])] for degree in sorted(aggregate)]
    return {
        "possible_degrees": sorted(possible),
        "nonzero_degrees": sorted(aggregate),
        "coefficient_rows": rows,
        "coefficient_sha256": sha(rows),
        "match_count": len(matches),
        "match_sha256": sha(matches),
        "first_evidence": {
            str(degree): first_evidence[degree] for degree in sorted(first_evidence)
        },
        "_aggregate": aggregate,
    }


def _strip_internal(ledger: dict) -> dict:
    return {key: value for key, value in ledger.items() if not key.startswith("_")}


def _direct_mixed_pairing(witness: dict, vec_gcd: dict, vec_gc: dict, vec_gd: dict, vec_g: dict) -> Q:
    total = Q(0)
    for key, weight in witness.items():
        response = (
            Q(vec_gcd.get(key, 0))
            - Q(vec_gc.get(key, 0))
            - Q(vec_gd.get(key, 0))
            + Q(vec_g.get(key, 0))
        )
        total += Q(weight) * response
    return total


def _candidate_side_record(
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
    vec_g, idx_g = g._cached_vector_index(
        endpoint, uid, (), strata, bank, poly_cache, vector_cache
    )
    vec_gc, idx_gc = g._cached_vector_index(
        endpoint, uid, (left,), strata, bank, poly_cache, vector_cache
    )
    vec_gd, idx_gd = g._cached_vector_index(
        endpoint, uid, (right,), strata, bank, poly_cache, vector_cache
    )
    vec_gcd, idx_gcd = g._cached_vector_index(
        endpoint, uid, (left, right), strata, bank, poly_cache, vector_cache
    )

    if prefactor_channel == left:
        kinds = {"ScSd": "x1", "Sc": "x1", "Sd": "x0", "I": "x0"}
    elif prefactor_channel == right:
        kinds = {"ScSd": "x1", "Sc": "x0", "Sd": "x1", "I": "x0"}
    else:
        raise AssertionError("T3-011-H prefactor channel is outside the admitted pair")

    ledgers = {
        "ScSd": reciprocal_moment_ledger(witness_index, idx_gcd, inverse_factors, kinds["ScSd"]),
        "Sc": reciprocal_moment_ledger(witness_index, idx_gc, inverse_factors, kinds["Sc"]),
        "Sd": reciprocal_moment_ledger(witness_index, idx_gd, inverse_factors, kinds["Sd"]),
        "I": reciprocal_moment_ledger(witness_index, idx_g, inverse_factors, kinds["I"]),
    }

    domain = set()
    for ledger in ledgers.values():
        domain.update(ledger["possible_degrees"])
    domain = {degree for degree in domain if degree >= 1}

    pairing_rows = []
    nonzero = []
    for degree in sorted(domain):
        value = (
            ledgers["ScSd"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sc"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sd"]["_aggregate"].get(degree, Q(0))
            + ledgers["I"]["_aggregate"].get(degree, Q(0))
        )
        row = [degree, *qjson(value)]
        pairing_rows.append(row)
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
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "prefactor_channel": prefactor_channel,
        "prefactor_coordinate": CHANNEL_COORDINATE[prefactor_channel],
        "finite_overlap_reciprocal_degrees": sorted(domain),
        "finite_overlap_sha256": sha(sorted(domain)),
        "component_ledgers": {
            name: _strip_internal(ledger) for name, ledger in ledgers.items()
        },
        "pairing_rows": pairing_rows,
        "pairing_sha256": sha(pairing_rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_degree": nonzero[0][0] if nonzero else None,
        "degree_zero_component_pairing": qjson(degree_zero_component),
        "degree_zero_direct_pairing": qjson(degree_zero_direct),
        "degree_zero_semantics_exactly_match_direct": semantic_match,
        "semantic_ambiguity_kind": (
            None
            if semantic_match
            else "DEGREE_ZERO_COMPONENT_DECOMPOSITION_DISAGREES_WITH_DIRECT_MIXED_RESPONSE"
        ),
        "all_reciprocal_degrees_annihilated": semantic_match and not nonzero,
    }


def _blocker_result(g_locks: dict[str, str], blocker: str) -> dict:
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "RECIPROCAL_AXIS_RATIONAL_PREFACTOR_AUDIT_BLOCKED",
        "predecessor_checkpoint": {
            "reviewed_head": G_REVIEWED_HEAD,
            "merge_commit": G_MERGE_COMMIT,
            "source_blobs": g_locks,
            "required_terminal": G_REQUIRED_TERMINAL,
            "frozen_record_count": G_FROZEN_RECORD_COUNT,
        },
        "characterized_blocker": blocker,
        "tested_record_count": 0,
        "possible_record_count": 2 * G_FROZEN_RECORD_COUNT,
        "tested_records": [],
        "semantic_functional_ambiguity": None,
        "first_cokernel_breaking_direction": None,
        "all_reciprocal_axis_responses_cokernel_invisible": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": BLOCKER_TERMINAL,
    }


def build() -> dict:
    validate_scope()
    g_locks = assert_g_locks()
    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)

    try:
        inverse_factors = {
            channel: inverse_coordinate_factors(channel, strata)
            for channel in CHANNEL_COORDINATE
        }
    except AssertionError as exc:
        return _blocker_result(g_locks, str(exc))

    witness_indexes = {
        channel: g._witness_index(bank["witness"])
        for channel, bank in banks.items()
    }
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
                for side_index, prefactor_channel in enumerate(pair):
                    rec = _candidate_side_record(
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
                    rec.update(
                        {
                            "ordinal": len(records),
                            "pair_index": pair_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                            "prefactor_side_index": side_index,
                            "prefactor_side": "left" if side_index == 0 else "right",
                        }
                    )
                    records.append(rec)

                    if rec["semantic_ambiguity_kind"] is not None:
                        first_ambiguity = rec
                        stop = True
                        break
                    if rec["nonzero_pairings"]:
                        degree, num, den = rec["nonzero_pairings"][0]
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

    possible_record_count = 2 * G_FROZEN_RECORD_COUNT
    if first_ambiguity is not None:
        terminal = AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = ESCAPE_TERMINAL
    else:
        if len(records) != possible_record_count:
            raise AssertionError(
                f"T3-011-H exhaustive record drift: {len(records)} != {possible_record_count}"
            )
        terminal = CLOSURE_TERMINAL

    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "RECIPROCAL_AXIS_RATIONAL_PREFACTOR_AUDIT_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": G_REVIEWED_HEAD,
            "merge_commit": G_MERGE_COMMIT,
            "source_blobs": g_locks,
            "required_terminal": G_REQUIRED_TERMINAL,
            "frozen_record_count": G_FROZEN_RECORD_COUNT,
        },
        "reciprocal_axis_class": {
            "unordered_pair_order": [list(pair) for pair in ADMITTED_PAIRS],
            "prefactor_domain": "x_q^{-r} with q in {c,d} and integer r>=1",
            "prefactor_side_order": ["left", "right"],
            "only_pole": "x_q=0",
            "nonzero_laurent_specialization_required": True,
            "finite_support_overlap_derived_without_degree_cutoff": True,
            "shifted_poles_admitted": False,
            "mixed_reciprocal_products_admitted": False,
            "positive_numerator_polynomials_admitted": False,
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
        },
        "possible_record_count": possible_record_count,
        "tested_record_count": len(records),
        "tested_records": records,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_reciprocal_axis_responses_cokernel_invisible": terminal == CLOSURE_TERMINAL,
        "characterized_blocker": None,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }
