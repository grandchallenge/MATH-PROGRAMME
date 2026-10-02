from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
N_DIR = HERE.parent / "OZ_RT_BZ_T3_011_N"
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


n = _load(N_DIR / "producer.py", "oz_t3_011_n_for_o")
m = n.m
l = m.l
h = n.h
g, f, a = n.g, n.f, n.a

OPERATION = "OZ-RT-BZ-T3-011-O"
STAGE = "T3_011_O_ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_COKERNEL_AUDIT"
ISSUE = 931
N_REVIEWED_HEAD = "a71335bdf4651d0ac0f693ff22802dd96ff098de"
N_MERGE_COMMIT = "70a688252f6ec440dff7380ea778401d3252c9fa"
N_REQUIRED_TERMINAL = "DOUBLE_RECIPROCAL_ACTIVE_TRIVARIATE_RESPONSE_CLASS_COKERNEL_INVISIBLE"
N_EXPECTED_RECORDS = 1282
N_BLOBS = {
    "producer.py": "0a89560dc074687c75091c2891685a0619bee745",
    "CONTRACT.json": "d5e6051512fb02b05e61f12312566bd8fd9f28b9",
    "verifier.py": "b197908d0297e283fc8e7f603978dfd358736989",
}
M_REQUIRED_TERMINAL = m.CLOSURE_TERMINAL
L_REQUIRED_TERMINAL = l.CLOSURE_TERMINAL
ADMITTED_PAIRS = tuple(n.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(n.CHANNEL_COORDINATE)
CANONICAL_SPECTATOR_CHANNEL = dict(n.CANONICAL_SPECTATOR_CHANNEL)
ORIENTATIONS = (
    "negative_left_positive_right",
    "positive_left_negative_right",
)
FROZEN_RECORD_COUNT = n.FROZEN_RECORD_COUNT
POSSIBLE_RECORD_COUNT = FROZEN_RECORD_COUNT * len(ORIENTATIONS)
COMPONENTS = tuple(n.COMPONENTS)
ESCAPE_TERMINAL = "ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_RESPONSE_ESCAPE_FOUND"
CLOSURE_TERMINAL = "ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_RESPONSE_CLASS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = "ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
BLOCKER_TERMINAL = "ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"


class UnboundedSupportOverlap(RuntimeError):
    def __init__(self, evidence: dict):
        super().__init__("active-plus-spectator double-reciprocal trivariate support overlap is unbounded")
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
    reciprocal_active_axes: int = 1,
    reciprocal_spectator: bool = True,
    all_reciprocal_trivariate: bool = False,
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
    if reciprocal_active_axes != 1:
        raise AssertionError("O admits exactly one reciprocal active axis")
    if reciprocal_spectator is not True:
        raise AssertionError("O requires exactly one reciprocal unshifted spectator")
    if all_reciprocal_trivariate:
        raise AssertionError("O does not admit the all-reciprocal trivariate octant")
    if shifted_spectator or shifted_poles:
        raise AssertionError("O retains the unshifted spectator and coordinate-zero poles only")
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
    for name, want in N_BLOBS.items():
        value = a.git_blob_sha1(N_DIR / name)
        if value != want:
            raise AssertionError(f"N source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((N_DIR / "CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-N":
        raise AssertionError("N contract operation drift")
    if contract.get("terminals", {}).get("closure") != N_REQUIRED_TERMINAL:
        raise AssertionError("N closure terminal drift")
    if m.CLOSURE_TERMINAL != M_REQUIRED_TERMINAL or l.CLOSURE_TERMINAL != L_REQUIRED_TERMINAL:
        raise AssertionError("boundary predecessor terminal drift")
    return {"N": got}


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


def _orientation_maps(pair, orientation, forward_factors, inverse_factors):
    left, right = pair
    if orientation == "negative_left_positive_right":
        return inverse_factors[left], forward_factors[right], "left"
    if orientation == "positive_left_negative_right":
        return forward_factors[left], inverse_factors[right], "right"
    raise AssertionError(f"unknown O orientation: {orientation}")


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
    orientation,
    strata,
    bank,
    witness_index,
    forward_factors,
    inverse_factors,
    poly_cache,
    vector_cache,
    lower,
    purpose,
    active_mode="O",
):
    left, right = pair
    axis, sch = _spectator(pair)
    if active_mode == "O":
        left_maps, right_maps, reciprocal_axis = _orientation_maps(
            pair, orientation, forward_factors, inverse_factors
        )
    elif active_mode == "L":
        left_maps, right_maps, reciprocal_axis = forward_factors[left], forward_factors[right], "none"
    else:
        raise AssertionError(f"unknown active mode: {active_mode}")
    spectator_maps = inverse_factors[sch]
    indexes = _component_indexes(endpoint, uid, pair, strata, bank, poly_cache, vector_cache)
    ledgers = {}
    for name, left_kind, right_kind, _marker in COMPONENTS:
        ledgers[name] = _signed_ledger(
            witness_index,
            indexes[name],
            left_maps,
            left_kind,
            right_maps,
            right_kind,
            spectator_maps,
            lower,
            {
                "pair": list(pair),
                "endpoint": endpoint,
                "candidate": unknown_json(uid),
                "orientation": orientation,
                "reciprocal_active_axis": reciprocal_axis,
                "spectator_axis": axis,
                "component": name,
                "purpose": purpose,
            },
        )
    return ledgers, axis, sch, reciprocal_axis


def _selected_rows(ledgers, selector):
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
    selected = {degree for degree in domain if selector(*degree)}
    return _pairing_rows(ledgers, selected)


def _m_t_zero_rows(
    pair, endpoint, uid, orientation, strata, bank, witness_index,
    forward_factors, inverse_factors, poly_cache, vector_cache,
):
    ledgers, *_ = m._make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        (1, 1, 0), "protected_M_t_zero_boundary_for_O"
    )
    return m._pairing_rows(
        ledgers,
        {
            degree
            for ledger in ledgers.values()
            for degree in map(tuple, ledger["possible_tridegrees"])
            if degree[0] >= 1 and degree[1] >= 1 and degree[2] == 0
        },
    )


def _candidate_record(
    pair, endpoint, uid, orientation, strata, bank, witness_index,
    forward_factors, inverse_factors, poly_cache, vector_cache,
):
    primary, axis, sch, reciprocal_axis = _make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        (1, 1, 1), "admitted_O_class", "O"
    )
    domain = set()
    support_pairs = 0
    for ledger in primary.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
        support_pairs += ledger["support_signature_pairs_inspected"]
    domain = {degree for degree in domain if min(degree) >= 1}
    pairing_rows = _pairing_rows(primary, domain)
    nonzero = [row for row in pairing_rows if row[-2] != 0]

    t_zero_here_ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        (1, 1, 0), "spectator_reciprocal_degree_zero_M_boundary", "O"
    )
    t_zero_here = _selected_rows(
        t_zero_here_ledgers, lambda r, s, t: r >= 1 and s >= 1 and t == 0
    )
    t_zero_protected = _m_t_zero_rows(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
    )
    m_match = t_zero_here == t_zero_protected

    reciprocal_zero_side = "left" if reciprocal_axis == "left" else "right"
    if reciprocal_zero_side == "left":
        reciprocal_lower = (0, 1, 1)
        reciprocal_selector = lambda r, s, t: r == 0 and s >= 1 and t >= 1
        positive_lower = (1, 0, 1)
        positive_selector = lambda r, s, t: r >= 1 and s == 0 and t >= 1
    else:
        reciprocal_lower = (1, 0, 1)
        reciprocal_selector = lambda r, s, t: s == 0 and r >= 1 and t >= 1
        positive_lower = (0, 1, 1)
        positive_selector = lambda r, s, t: r == 0 and s >= 1 and t >= 1

    reciprocal_zero_here_ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        reciprocal_lower, "reciprocal_active_degree_zero_L_boundary", "O"
    )
    reciprocal_zero_here = _selected_rows(reciprocal_zero_here_ledgers, reciprocal_selector)
    reciprocal_zero_l_ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        reciprocal_lower, "protected_L_semantic_extension_for_O", "L"
    )
    reciprocal_zero_l = _selected_rows(reciprocal_zero_l_ledgers, reciprocal_selector)
    l_match = reciprocal_zero_here == reciprocal_zero_l

    positive_zero_ledgers, *_ = _make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward_factors, inverse_factors, poly_cache, vector_cache,
        positive_lower, "positive_active_degree_zero_direct_response_anchor", "O"
    )
    positive_zero_rows = _selected_rows(positive_zero_ledgers, positive_selector)

    ambiguity = None
    if not m_match:
        ambiguity = "SPECTATOR_RECIPROCAL_DEGREE_ZERO_BOUNDARY_DISAGREES_WITH_PROTECTED_T3_011_M"
    elif not l_match:
        ambiguity = "RECIPROCAL_ACTIVE_DEGREE_ZERO_BOUNDARY_DISAGREES_WITH_PROTECTED_T3_011_L_SEMANTICS"

    return {
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "coordinate_pair": [CHANNEL_COORDINATE[pair[0]], CHANNEL_COORDINATE[pair[1]]],
        "orientation": orientation,
        "reciprocal_active_axis": reciprocal_axis,
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
        "protected_M_boundary_rows": t_zero_protected,
        "spectator_reciprocal_degree_zero_semantics_exactly_match_M": m_match,
        "reciprocal_active_degree_zero_boundary_rows": reciprocal_zero_here,
        "protected_L_semantic_boundary_rows": reciprocal_zero_l,
        "reciprocal_active_degree_zero_semantics_exactly_match_L": l_match,
        "positive_active_degree_zero_direct_response_rows": positive_zero_rows,
        "positive_active_degree_zero_anchor_kind": "DIRECT_RESPONSE_ONLY_NOT_T3_011_I",
        "support_signature_pairs_inspected": support_pairs,
        "semantic_ambiguity_kind": ambiguity,
        "all_active_spectator_double_reciprocal_trivariate_degrees_annihilated": ambiguity is None and not nonzero,
    }


def _base_result(locks, support_records, support_pairs):
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "predecessor_checkpoint": {
            "reviewed_head": N_REVIEWED_HEAD,
            "merge_commit": N_MERGE_COMMIT,
            "source_blobs": locks,
            "required_terminal": N_REQUIRED_TERMINAL,
            "possible_record_count": N_EXPECTED_RECORDS,
            "tested_record_count": N_EXPECTED_RECORDS,
            "semantic_functional_ambiguity": None,
            "first_cokernel_breaking_direction": None,
            "characterized_blocker": None,
        },
        "boundary_checkpoints": {
            "M": M_REQUIRED_TERMINAL,
            "L": L_REQUIRED_TERMINAL,
        },
        "active_spectator_double_reciprocal_trivariate_class": {
            "monomial_domains": [
                "x_c^-r*x_d^s*x_e^-t",
                "x_c^r*x_d^-s*x_e^-t",
            ],
            "degrees": "r,s,t>=1",
            "unordered_pair_order": [list(pair) for pair in ADMITTED_PAIRS],
            "orientation_order": list(ORIENTATIONS),
            "spectator_is_unshifted": True,
            "reciprocal_active_axis_count": 1,
            "reciprocal_spectator_admitted": True,
            "all_reciprocal_trivariate_octant_admitted": False,
            "complete_overlap_derived_from_exact_signatures": True,
            "support_feasible_seed_required_for_recession": True,
            "arbitrary_degree_cutoff_used": False,
            "spectator_reciprocal_degree_zero_boundary_matches_protected_M": True,
            "reciprocal_active_degree_zero_boundary_matches_protected_L": True,
            "positive_active_degree_zero_is_direct_response_anchor_only": True,
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
        forward_factors = {
            channel: g.e._coordinate_factors(channel, strata)
            for channel in CHANNEL_COORDINATE
        }
        inverse_factors = {
            channel: h.inverse_coordinate_factors(channel, strata)
            for channel in CHANNEL_COORDINATE
        }
    except AssertionError as exc:
        base = _base_result(locks, 0, 0)
        return {
            **base,
            "status": "ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_COKERNEL_AUDIT_BLOCKED",
            "characterized_blocker": {"kind": "COORDINATE_FACTOR_BLOCKER", "detail": str(exc)},
            "possible_record_count": POSSIBLE_RECORD_COUNT,
            "tested_record_count": 0,
            "tested_records": [],
            "semantic_functional_ambiguity": None,
            "first_cokernel_breaking_direction": None,
            "all_active_spectator_double_reciprocal_trivariate_responses_cokernel_invisible": False,
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
        for orientation_index, orientation in enumerate(ORIENTATIONS):
            for endpoint_index, endpoint in enumerate(pair):
                bank = banks[endpoint]
                witness_index = witness_indexes[endpoint]
                for candidate_index, uid in enumerate(bank["candidates"]):
                    try:
                        record = _candidate_record(
                            pair, endpoint, uid, orientation, strata, bank, witness_index,
                            forward_factors, inverse_factors, poly_cache, vector_cache
                        )
                    except UnboundedSupportOverlap as exc:
                        first_blocker = {
                            "kind": "UNBOUNDED_ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_CANCELLATION_RAY",
                            "pair_index": pair_index,
                            "orientation_index": orientation_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                            **exc.evidence,
                        }
                        stop = True
                        break
                    record.update({
                        "ordinal": len(records),
                        "pair_index": pair_index,
                        "orientation_index": orientation_index,
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
                            "orientation": orientation,
                            "reciprocal_active_axis": record["reciprocal_active_axis"],
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
                f"O exhaustive record drift: {len(records)} != {POSSIBLE_RECORD_COUNT}"
            )
        terminal = CLOSURE_TERMINAL

    cache = n.solve_signed_tridegrees.cache_info()
    return {
        **base,
        "status": (
            "ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_COKERNEL_AUDIT_COMPLETE"
            if first_blocker is None
            else "ACTIVE_SPECTATOR_DOUBLE_RECIPROCAL_TRIVARIATE_COKERNEL_AUDIT_BLOCKED"
        ),
        "execution_ledger": {
            "coordinate_factor_maps": len(forward_factors),
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
        "all_active_spectator_double_reciprocal_trivariate_responses_cokernel_invisible": terminal == CLOSURE_TERMINAL,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }
