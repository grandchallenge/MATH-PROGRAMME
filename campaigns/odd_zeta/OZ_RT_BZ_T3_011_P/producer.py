from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
O_DIR = HERE.parent / "OZ_RT_BZ_T3_011_O"
G_DIR = HERE.parent / "OZ_RT_BZ_T3_010"
if str(G_DIR) not in sys.path:
    sys.path.insert(0, str(G_DIR))


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


o = _load(O_DIR / "producer.py", "oz_t3_011_o_for_p")
n = o.n
i = n.i
h = o.h
g, f, a = o.g, o.f, o.a

OPERATION = "OZ-RT-BZ-T3-011-P"
STAGE = "T3_011_P_ALL_RECIPROCAL_TRIVARIATE_LAURENT_COKERNEL_AUDIT"
ISSUE = 934
O_REVIEWED_HEAD = "da9e2204edc452f39328ba88de54d73455ba9f32"
O_MERGE_COMMIT = "0065b997317d59a9c20f3fbff8792b37527b4a65"
O_REQUIRED_TERMINAL = "ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_RESPONSE_CLASS_COKERNEL_INVISIBLE"
O_EXPECTED_RECORDS = 2564
O_BLOBS = {
    "producer.py": "39ff905f2837d434fff20be5eea9abef6fa852a6",
    "CONTRACT.json": "9bb7dce32472ebbb6a09f036ea7932f85151dd77",
    "verifier.py": "325cdfec0538c25a0cc709ab5d150b98632b288c",
}
N_REQUIRED_TERMINAL = n.CLOSURE_TERMINAL
I_REQUIRED_TERMINAL = i.CLOSURE_TERMINAL
ADMITTED_PAIRS = tuple(n.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(n.CHANNEL_COORDINATE)
CANONICAL_SPECTATOR_CHANNEL = dict(n.CANONICAL_SPECTATOR_CHANNEL)
ORIENTATIONS = ("negative_left_negative_right_negative_spectator",)
FROZEN_RECORD_COUNT = n.FROZEN_RECORD_COUNT
POSSIBLE_RECORD_COUNT = FROZEN_RECORD_COUNT
COMPONENTS = tuple(n.COMPONENTS)
ESCAPE_TERMINAL = "ALL_RECIPROCAL_TRIVARIATE_RESPONSE_ESCAPE_FOUND"
CLOSURE_TERMINAL = "ALL_RECIPROCAL_TRIVARIATE_RESPONSE_CLASS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = "ALL_RECIPROCAL_TRIVARIATE_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
BLOCKER_TERMINAL = "ALL_RECIPROCAL_TRIVARIATE_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"


class UnboundedSupportOverlap(RuntimeError):
    def __init__(self, evidence: dict):
        super().__init__("all-reciprocal trivariate support overlap is unbounded")
        self.evidence = evidence


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def validate_scope(
    reciprocal_active_axes: int = 2,
    reciprocal_spectator: bool = True,
    all_reciprocal_trivariate: bool = True,
    shifted_spectator: bool = False,
    shifted_poles: bool = False,
    arbitrary_rational_functions: bool = False,
    support_or_harmonic_enlargement: bool = False,
    candidate_bank_or_scalar_namespace_widening: bool = False,
    recurrence_widening: bool = False,
    correction_recombination: bool = False,
    candidate_linear_combinations: bool = False,
    third_finite_difference_operator: bool = False,
    arbitrary_degree_cutoff=None,
):
    if reciprocal_active_axes != 2:
        raise AssertionError("P admits exactly two reciprocal active axes")
    if reciprocal_spectator is not True or all_reciprocal_trivariate is not True:
        raise AssertionError("P admits exactly the all-reciprocal trivariate octant")
    if shifted_spectator or shifted_poles:
        raise AssertionError("P retains the unshifted spectator and coordinate-zero poles only")
    if arbitrary_rational_functions:
        raise AssertionError("arbitrary rational functions forbidden")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening:
        raise AssertionError("basis widening forbidden")
    if recurrence_widening or correction_recombination or candidate_linear_combinations:
        raise AssertionError("recombination widening forbidden")
    if third_finite_difference_operator:
        raise AssertionError("exactly two finite differences retained")
    if arbitrary_degree_cutoff is not None:
        raise AssertionError("arbitrary degree cutoffs forbidden")


def assert_locks():
    got = {}
    for name, want in O_BLOBS.items():
        value = a.git_blob_sha1(O_DIR / name)
        if value != want:
            raise AssertionError(f"O source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((O_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-O":
        raise AssertionError("O contract operation drift")
    if contract.get("terminals", {}).get("closure") != O_REQUIRED_TERMINAL:
        raise AssertionError("O closure terminal drift")
    if n.CLOSURE_TERMINAL != N_REQUIRED_TERMINAL or i.CLOSURE_TERMINAL != I_REQUIRED_TERMINAL:
        raise AssertionError("boundary predecessor terminal drift")
    return {"O": got}


def solve_signed_tridegrees(base_sig, left_sig, right_sig, spectator_sig, target_sig, lower=(1, 1, 1)):
    return n.solve_signed_tridegrees(
        base_sig, left_sig, right_sig, spectator_sig, target_sig, tuple(lower)
    )


def _solution_matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, degree):
    return n._solution_matches(base_sig, left_sig, right_sig, spectator_sig, target_sig, degree)


def _ray_matches(left_sig, right_sig, spectator_sig, ray):
    return n._ray_matches(left_sig, right_sig, spectator_sig, ray)


def _spectator(pair):
    remaining = {"n", "k", "l"} - {
        CHANNEL_COORDINATE[pair[0]], CHANNEL_COORDINATE[pair[1]]
    }
    if len(remaining) != 1:
        raise AssertionError("pair does not determine unique spectator")
    axis = next(iter(remaining))
    return axis, CANONICAL_SPECTATOR_CHANNEL[axis]


def _component_indexes(endpoint, uid, pair, strata, bank, poly_cache, vector_cache):
    return n._component_indexes(endpoint, uid, pair, strata, bank, poly_cache, vector_cache)


def _pairing_rows(ledgers, degrees):
    return n._pairing_rows(ledgers, degrees)


def _strip_internal(ledger):
    return {key: value for key, value in ledger.items() if not key.startswith("_")}


def _signed_ledger(
    witness_index,
    base_index,
    left_maps,
    left_kind,
    right_maps,
    right_kind,
    spectator_maps,
    lower,
    context,
):
    try:
        return n.signed_moment_ledger(
            witness_index,
            base_index,
            left_maps,
            left_kind,
            right_maps,
            right_kind,
            spectator_maps,
            lower,
            context,
        )
    except n.UnboundedSupportOverlap as exc:
        raise UnboundedSupportOverlap(exc.evidence) from exc


def _make_ledgers(
    pair,
    endpoint,
    uid,
    strata,
    bank,
    witness_index,
    inverse_factors,
    poly_cache,
    vector_cache,
    lower,
    purpose,
):
    left, right = pair
    axis, sch = _spectator(pair)
    indexes = _component_indexes(endpoint, uid, pair, strata, bank, poly_cache, vector_cache)
    ledgers = {}
    for name, left_kind, right_kind, _marker in COMPONENTS:
        ledgers[name] = _signed_ledger(
            witness_index,
            indexes[name],
            inverse_factors[left],
            left_kind,
            inverse_factors[right],
            right_kind,
            inverse_factors[sch],
            lower,
            {
                "pair": list(pair),
                "endpoint": endpoint,
                "candidate": unknown_json(uid),
                "orientation": ORIENTATIONS[0],
                "reciprocal_active_axes": ["left", "right"],
                "reciprocal_spectator": True,
                "spectator_axis": axis,
                "component": name,
                "purpose": purpose,
            },
        )
    return ledgers, axis, sch


def _selected_rows(ledgers, selector):
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
    selected = {degree for degree in domain if selector(*degree)}
    return _pairing_rows(ledgers, selected)


def _i_t_zero_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    inverse_factors, poly_cache, vector_cache,
):
    return n._i_boundary_rows(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse_factors, poly_cache, vector_cache
    )


def _candidate_record(
    pair, endpoint, uid, strata, bank, witness_index,
    inverse_factors, poly_cache, vector_cache,
):
    primary, axis, sch = _make_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse_factors, poly_cache, vector_cache,
        (1, 1, 1), "admitted_P_all_reciprocal_class"
    )
    domain = set()
    support_pairs = 0
    for ledger in primary.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
        support_pairs += ledger["support_signature_pairs_inspected"]
    domain = {degree for degree in domain if min(degree) >= 1}
    pairing_rows = _pairing_rows(primary, domain)
    nonzero = [row for row in pairing_rows if row[-2] != 0]

    t_zero_ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse_factors, poly_cache, vector_cache,
        (1, 1, 0), "spectator_reciprocal_degree_zero_I_boundary"
    )
    t_zero_rows3 = _selected_rows(
        t_zero_ledgers, lambda r, s, t: r >= 1 and s >= 1 and t == 0
    )
    t_zero_here = [[r, s, num, den] for r, s, _t, num, den in t_zero_rows3]
    t_zero_protected = _i_t_zero_rows(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse_factors, poly_cache, vector_cache,
    )
    i_match = (
        t_zero_here == t_zero_protected
        and not any(row[-2] != 0 for row in t_zero_protected)
    )

    left_zero_ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse_factors, poly_cache, vector_cache,
        (0, 1, 1), "left_reciprocal_degree_zero_direct_response_anchor"
    )
    left_zero_rows = _selected_rows(
        left_zero_ledgers, lambda r, s, t: r == 0 and s >= 1 and t >= 1
    )
    right_zero_ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse_factors, poly_cache, vector_cache,
        (1, 0, 1), "right_reciprocal_degree_zero_direct_response_anchor"
    )
    right_zero_rows = _selected_rows(
        right_zero_ledgers, lambda r, s, t: s == 0 and r >= 1 and t >= 1
    )

    ambiguity = None
    if not i_match:
        ambiguity = "SPECTATOR_RECIPROCAL_DEGREE_ZERO_BOUNDARY_DISAGREES_WITH_PROTECTED_T3_011_I"

    return {
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "coordinate_pair": [CHANNEL_COORDINATE[pair[0]], CHANNEL_COORDINATE[pair[1]]],
        "orientation": ORIENTATIONS[0],
        "reciprocal_active_axes": ["left", "right"],
        "spectator_axis": axis,
        "spectator_channel_representative": sch,
        "finite_overlap_tridegrees": [list(degree) for degree in sorted(domain)],
        "finite_overlap_sha256": sha([list(degree) for degree in sorted(domain)]),
        "component_ledgers": {name: _strip_internal(ledger) for name, ledger in primary.items()},
        "pairing_rows": pairing_rows,
        "pairing_sha256": sha(pairing_rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_tridegree": nonzero[0][:3] if nonzero else None,
        "spectator_reciprocal_degree_zero_boundary_rows": t_zero_here,
        "protected_I_boundary_rows": t_zero_protected,
        "spectator_reciprocal_degree_zero_semantics_exactly_match_I": i_match,
        "left_reciprocal_degree_zero_direct_response_rows": left_zero_rows,
        "right_reciprocal_degree_zero_direct_response_rows": right_zero_rows,
        "active_reciprocal_degree_zero_anchor_kind": "DIRECT_RESPONSE_ONLY_NO_PREDECESSOR_CLASS_PROMOTION",
        "support_signature_pairs_inspected": support_pairs,
        "semantic_ambiguity_kind": ambiguity,
        "all_all_reciprocal_trivariate_degrees_annihilated": ambiguity is None and not nonzero,
    }


def _base_result(locks, support_records, support_pairs):
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "predecessor_checkpoint": {
            "reviewed_head": O_REVIEWED_HEAD,
            "merge_commit": O_MERGE_COMMIT,
            "source_blobs": locks,
            "required_terminal": O_REQUIRED_TERMINAL,
            "possible_record_count": O_EXPECTED_RECORDS,
            "tested_record_count": O_EXPECTED_RECORDS,
            "semantic_functional_ambiguity": None,
            "first_cokernel_breaking_direction": None,
            "characterized_blocker": None,
        },
        "boundary_checkpoints": {
            "N": N_REQUIRED_TERMINAL,
            "I": I_REQUIRED_TERMINAL,
        },
        "all_reciprocal_trivariate_class": {
            "monomial_domain": "x_c^-r*x_d^-s*x_e^-t",
            "degrees": "r,s,t>=1",
            "unordered_pair_order": [list(pair) for pair in ADMITTED_PAIRS],
            "orientation_order": list(ORIENTATIONS),
            "spectator_is_unshifted": True,
            "reciprocal_active_axes": 2,
            "reciprocal_spectator_admitted": True,
            "all_reciprocal_trivariate_octant_admitted": True,
            "complete_overlap_derived_from_exact_signatures": True,
            "support_feasible_seed_required_for_recession": True,
            "arbitrary_degree_cutoff_used": False,
            "spectator_reciprocal_degree_zero_boundary_matches_protected_I": True,
            "active_reciprocal_degree_zero_faces_are_direct_response_anchors_only": True,
            "third_finite_difference_operator_admitted": False,
        },
        "domain_analysis": {
            "candidate_records_inspected_for_support": support_records,
            "support_signature_pairs_inspected": support_pairs,
            "finite_solver_uses_signature_derived_bounds_only": True,
            "arbitrary_degree_cutoff_used": False,
        },
    }


def build():
    validate_scope()
    n.solve_signed_tridegrees.cache_clear()
    locks = assert_locks()
    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    try:
        inverse_factors = {
            channel: h.inverse_coordinate_factors(channel, strata)
            for channel in CHANNEL_COORDINATE
        }
    except AssertionError as exc:
        base = _base_result(locks, 0, 0)
        return {
            **base,
            "status": "ALL_RECIPROCAL_TRIVARIATE_LAURENT_COKERNEL_AUDIT_BLOCKED",
            "characterized_blocker": {"kind": "COORDINATE_FACTOR_BLOCKER", "detail": str(exc)},
            "possible_record_count": POSSIBLE_RECORD_COUNT,
            "tested_record_count": 0,
            "tested_records": [],
            "semantic_functional_ambiguity": None,
            "first_cokernel_breaking_direction": None,
            "all_all_reciprocal_trivariate_responses_cokernel_invisible": False,
            "residual_sum_zero_proved": False,
            "proof_effect": "NONE",
            "promotion_effect": "NONE",
            "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
            "terminal": BLOCKER_TERMINAL,
        }

    witness_indexes = {
        channel: g._witness_index(bank["witness"])
        for channel, bank in banks.items()
    }
    poly_cache, vector_cache = {}, {}
    records = []
    first_escape = None
    first_ambiguity = None
    first_blocker = None
    support_pairs = 0
    stop = False

    for pair_index, pair in enumerate(ADMITTED_PAIRS):
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            witness_index = witness_indexes[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                try:
                    record = _candidate_record(
                        pair, endpoint, uid, strata, bank, witness_index,
                        inverse_factors, poly_cache, vector_cache
                    )
                except UnboundedSupportOverlap as exc:
                    first_blocker = {
                        "kind": "UNBOUNDED_ALL_RECIPROCAL_TRIVARIATE_CANCELLATION_RAY",
                        "pair_index": pair_index,
                        "orientation_index": 0,
                        "endpoint_index": endpoint_index,
                        "candidate_index": candidate_index,
                        **exc.evidence,
                    }
                    stop = True
                    break
                record.update({
                    "ordinal": len(records),
                    "pair_index": pair_index,
                    "orientation_index": 0,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                })
                records.append(record)
                support_pairs += record["support_signature_pairs_inspected"]
                if record["semantic_ambiguity_kind"] is not None:
                    first_ambiguity = record
                    stop = True
                    break
                if record["nonzero_pairings"]:
                    r, s, t, num, den = record["nonzero_pairings"][0]
                    first_escape = {
                        "ordinal": record["ordinal"],
                        "pair": record["pair"],
                        "endpoint": endpoint,
                        "candidate": record["candidate"],
                        "orientation": ORIENTATIONS[0],
                        "spectator_axis": record["spectator_axis"],
                        "tridegree": [r, s, t],
                        "normalized_cokernel_pairing": [num, den],
                    }
                    stop = True
                    break
            if stop:
                break
        if stop:
            break

    base = _base_result(
        locks,
        len(records) + (1 if first_blocker is not None else 0),
        support_pairs,
    )
    if first_blocker is not None:
        terminal = BLOCKER_TERMINAL
    elif first_ambiguity is not None:
        terminal = AMBIGUITY_TERMINAL
    elif first_escape is not None:
        terminal = ESCAPE_TERMINAL
    else:
        if len(records) != POSSIBLE_RECORD_COUNT:
            raise AssertionError(
                f"P exhaustive record drift: {len(records)} != {POSSIBLE_RECORD_COUNT}"
            )
        terminal = CLOSURE_TERMINAL

    cache = n.solve_signed_tridegrees.cache_info()
    return {
        **base,
        "status": (
            "ALL_RECIPROCAL_TRIVARIATE_LAURENT_COKERNEL_AUDIT_COMPLETE"
            if first_blocker is None
            else "ALL_RECIPROCAL_TRIVARIATE_LAURENT_COKERNEL_AUDIT_BLOCKED"
        ),
        "execution_ledger": {
            "inverse_coordinate_factor_maps": len(inverse_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "signed_solver_cache_hits": cache.hits,
            "signed_solver_cache_misses": cache.misses,
        },
        "characterized_blocker": first_blocker,
        "possible_record_count": POSSIBLE_RECORD_COUNT,
        "tested_record_count": len(records),
        "tested_records": records,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_all_reciprocal_trivariate_responses_cokernel_invisible": terminal == CLOSURE_TERMINAL,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }
