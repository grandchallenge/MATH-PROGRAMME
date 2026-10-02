from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
J_DIR = HERE.parent / "OZ_RT_BZ_T3_011_J"
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


j = _load_module(J_DIR / "producer.py", "oz_t3_011_j_producer")
g = j.g
f = j.f
a = j.a

OPERATION = "OZ-RT-BZ-T3-011-K"
STAGE = "T3_011_K_TRIVARIATE_SPECTATOR_POLYNOMIAL_COKERNEL_AUDIT"
ISSUE = 916

J_REVIEWED_HEAD = "7c59a5e6a7a27f2ca5fccf60da166b66845f5fc7"
J_MERGE_COMMIT = "7450da94160f413f9191d56c0ee6a5d1d484c8f4"
J_REQUIRED_TERMINAL = "MIXED_SIGN_LAURENT_RESPONSE_CLASS_COKERNEL_INVISIBLE"
J_EXPECTED_RECORDS = 2564
J_BLOBS = {
    "producer.py": "4f967527a5ad0dafe40f76b4714e6ba05e38bf17",
    "CONTRACT.json": "eae0a0bc9c86ce1ba51409d2c73985f8f7f8368f",
    "verifier.py": "40fa61185005dd1a5f9a83888fdc3e1d730efacc",
}
G_REQUIRED_TERMINAL = "MIXED_POLYNOMIAL_MULTIPLIER_COKERNEL_CLOSURE_CERTIFIED"
G_EXPECTED_RECORDS = 1282
G_BLOBS = {
    "t3_011_g.py": "388f217c53d6100e34c488bbe2c75cdcec394d99",
    "T3_011_G_CONTRACT.json": "b0c26d8b7b5015c53cb364e2b8a35cb2245bdaa5",
    "verify_t3_011_g.py": "8cc00a1f0f1e32f84b4536ee044b5a1fb2b5c997",
}

ADMITTED_PAIRS = tuple(g.ADMITTED_PAIRS)
CHANNEL_COORDINATE = dict(g.CHANNEL_COORDINATE)
FROZEN_RECORD_COUNT = G_EXPECTED_RECORDS
CANONICAL_SPECTATOR_CHANNEL = {"n": "n1", "k": "k1", "l": "l1"}

ESCAPE_TERMINAL = "TRIVARIATE_SPECTATOR_POLYNOMIAL_RESPONSE_ESCAPE_FOUND"
CLOSURE_TERMINAL = "TRIVARIATE_SPECTATOR_POLYNOMIAL_RESPONSE_CLASS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = (
    "TRIVARIATE_SPECTATOR_POLYNOMIAL_RESPONSE_NOT_CERTIFIED__SEMANTIC_FUNCTIONAL_AMBIGUITY"
)
BLOCKER_TERMINAL = (
    "TRIVARIATE_SPECTATOR_POLYNOMIAL_RESPONSE_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"
)


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def assert_predecessor_locks() -> dict:
    j_locks = {}
    for name, want in J_BLOBS.items():
        value = a.git_blob_sha1(J_DIR / name)
        if value != want:
            raise AssertionError(f"T3-011-J source lock drift: {name}: {value} != {want}")
        j_locks[name] = value
    j_contract = json.loads((J_DIR / "CONTRACT.json").read_text())
    if j_contract.get("operation") != "OZ-RT-BZ-T3-011-J":
        raise AssertionError("T3-011-J contract operation drift")
    if j_contract.get("terminals", {}).get("closure") != J_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-J closure terminal drift")

    g_locks = {}
    for name, want in G_BLOBS.items():
        value = a.git_blob_sha1(G_DIR / name)
        if value != want:
            raise AssertionError(f"T3-011-G source lock drift: {name}: {value} != {want}")
        g_locks[name] = value
    g_contract = json.loads((G_DIR / "T3_011_G_CONTRACT.json").read_text())
    if g_contract.get("operation") != "OZ-RT-BZ-T3-011-G":
        raise AssertionError("T3-011-G contract operation drift")
    if g_contract.get("terminals", {}).get("closure") != G_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-G closure terminal drift")
    return {"J": j_locks, "G": g_locks}


def validate_scope(
    reciprocal_spectator: bool = False,
    shifted_spectator: bool = False,
    shifted_poles: bool = False,
    arbitrary_rational_functions: bool = False,
    support_or_harmonic_enlargement: bool = False,
    candidate_bank_or_scalar_namespace_widening: bool = False,
    recurrence_widening: bool = False,
    correction_recombination: bool = False,
    candidate_linear_combinations: bool = False,
    third_finite_difference_operator: bool = False,
) -> None:
    if reciprocal_spectator or shifted_spectator:
        raise AssertionError("T3-011-K admits only an unshifted positive spectator")
    if shifted_poles or arbitrary_rational_functions:
        raise AssertionError("T3-011-K does not widen pole geometry or rational syntax")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening:
        raise AssertionError("T3-011-K forbids support, harmonic, candidate-bank, and scalar widening")
    if recurrence_widening or correction_recombination or candidate_linear_combinations:
        raise AssertionError("T3-011-K forbids recurrence, correction, and candidate recombination")
    if third_finite_difference_operator:
        raise AssertionError("T3-011-K retains exactly Delta_c Delta_d")


def _sig_dict(sig) -> dict:
    return {factor: int(exp) for factor, exp in sig if exp}


def _positive_step(sig, label: str) -> dict:
    step = _sig_dict(sig)
    if not step:
        raise AssertionError(f"{label} coordinate specialization became constant")
    if any(exp <= 0 for exp in step.values()):
        raise AssertionError(f"{label} coordinate specialization is not a positive Laurent direction")
    return step


def _subtract_signature(target_sig, step_sig, degree: int):
    out = _sig_dict(target_sig)
    for factor, exp in step_sig:
        out[factor] = out.get(factor, 0) - degree * int(exp)
        if out[factor] < 0:
            return None
        if out[factor] == 0:
            del out[factor]
    return tuple(sorted(out.items()))


@lru_cache(maxsize=None)
def _solve_tridegrees(base_sig, left_sig, right_sig, spectator_sig, target_sig):
    base = _sig_dict(base_sig)
    target = _sig_dict(target_sig)
    left = _positive_step(left_sig, "left")
    right = _positive_step(right_sig, "right")
    spectator = _positive_step(spectator_sig, "spectator")
    factors = set(base) | set(target) | set(left) | set(right) | set(spectator)
    diff = {factor: target.get(factor, 0) - base.get(factor, 0) for factor in factors}
    if any(value < 0 for value in diff.values()):
        return ()

    tbounds = [
        diff[factor] // exp for factor, exp in spectator.items() if exp > 0
    ]
    if not tbounds:
        raise AssertionError("finite spectator-degree bound unavailable")
    out = []
    for t in range(min(tbounds) + 1):
        reduced_target = _subtract_signature(target_sig, spectator_sig, t)
        if reduced_target is None:
            continue
        for r, s in g._solve_multidegrees(
            base_sig, left_sig, right_sig, reduced_target
        ):
            out.append((r, s, t))
    return tuple(sorted(out))


def trivariate_moment_ledger(
    witness_index: dict,
    base_index: dict,
    left_factors: dict,
    left_kind: str,
    right_factors: dict,
    right_kind: str,
    spectator_factors: dict,
) -> dict:
    aggregate: dict[tuple[int, int, int], Q] = {}
    possible: set[tuple[int, int, int]] = set()
    matches = []
    for base_key in sorted(set(witness_index) & set(base_index), key=repr):
        cell_id, scalar, mon = base_key
        sid = g._stratum_id(cell_id)
        left_sig, left_coeff = left_factors[sid][left_kind]
        right_sig, right_coeff = right_factors[sid][right_kind]
        spectator_sig, spectator_coeff = spectator_factors[sid]["x0"]
        for target_sig, weight in witness_index[base_key]:
            for base_sig, coeff in base_index[base_key]:
                for r, s, t in _solve_tridegrees(
                    base_sig, left_sig, right_sig, spectator_sig, target_sig
                ):
                    possible.add((r, s, t))
                    contribution = (
                        weight
                        * coeff
                        * (left_coeff ** r)
                        * (right_coeff ** s)
                        * (spectator_coeff ** t)
                    )
                    aggregate[(r, s, t)] = aggregate.get((r, s, t), Q(0)) + contribution
                    matches.append(
                        [
                            r,
                            s,
                            t,
                            cell_id,
                            scalar,
                            list(mon),
                            qjson(weight),
                            qjson(coeff),
                            qjson(contribution),
                        ]
                    )
    aggregate = {degree: value for degree, value in aggregate.items() if value}
    rows = [
        [r, s, t, *qjson(aggregate[(r, s, t)])]
        for r, s, t in sorted(aggregate)
    ]
    return {
        "possible_tridegrees": [[r, s, t] for r, s, t in sorted(possible)],
        "nonzero_tridegrees": [[r, s, t] for r, s, t in sorted(aggregate)],
        "coefficient_rows": rows,
        "coefficient_sha256": sha(rows),
        "match_count": len(matches),
        "match_sha256": sha(sorted(matches, key=repr)),
        "_aggregate": aggregate,
    }


def _strip_internal(ledger: dict) -> dict:
    return {key: value for key, value in ledger.items() if not key.startswith("_")}


def _pairing_rows(ledgers: dict, degrees) -> list[list[int]]:
    rows = []
    for degree in sorted(degrees):
        value = (
            ledgers["ScSd"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sc"]["_aggregate"].get(degree, Q(0))
            - ledgers["Sd"]["_aggregate"].get(degree, Q(0))
            + ledgers["I"]["_aggregate"].get(degree, Q(0))
        )
        rows.append([*degree, *qjson(value)])
    return rows


def _bivariate_rows(
    witness_index,
    idx_gcd,
    idx_gc,
    idx_gd,
    idx_g,
    left_factors,
    right_factors,
):
    ledgers = {
        "ScSd": g.bivariate_moment_ledger(
            witness_index, idx_gcd, left_factors, "x1", right_factors, "x1"
        ),
        "Sc": g.bivariate_moment_ledger(
            witness_index, idx_gc, left_factors, "x1", right_factors, "x0"
        ),
        "Sd": g.bivariate_moment_ledger(
            witness_index, idx_gd, left_factors, "x0", right_factors, "x1"
        ),
        "I": g.bivariate_moment_ledger(
            witness_index, idx_g, left_factors, "x0", right_factors, "x0"
        ),
    }
    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_multidegrees"]))
    domain = {(r, s) for r, s in domain if r >= 1 and s >= 1}
    rows = []
    for r, s in sorted(domain):
        value = (
            ledgers["ScSd"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sc"]["_aggregate"].get((r, s), Q(0))
            - ledgers["Sd"]["_aggregate"].get((r, s), Q(0))
            + ledgers["I"]["_aggregate"].get((r, s), Q(0))
        )
        rows.append([r, s, *qjson(value)])
    return rows


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


def _spectator(pair) -> tuple[str, str]:
    left_axis = CHANNEL_COORDINATE[pair[0]]
    right_axis = CHANNEL_COORDINATE[pair[1]]
    remaining = {"n", "k", "l"} - {left_axis, right_axis}
    if len(remaining) != 1:
        raise AssertionError(f"T3-011-K pair does not determine a unique spectator: {pair}")
    axis = next(iter(remaining))
    return axis, CANONICAL_SPECTATOR_CHANNEL[axis]


def _candidate_record(
    pair,
    endpoint,
    uid,
    strata,
    bank,
    witness_index,
    coordinate_factors,
    poly_cache,
    vector_cache,
):
    left, right = pair
    spectator_axis, spectator_channel = _spectator(pair)
    left_factors = coordinate_factors[left]
    right_factors = coordinate_factors[right]
    spectator_factors = coordinate_factors[spectator_channel]

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

    ledgers = {
        "ScSd": trivariate_moment_ledger(
            witness_index, idx_gcd, left_factors, "x1", right_factors, "x1", spectator_factors
        ),
        "Sc": trivariate_moment_ledger(
            witness_index, idx_gc, left_factors, "x1", right_factors, "x0", spectator_factors
        ),
        "Sd": trivariate_moment_ledger(
            witness_index, idx_gd, left_factors, "x0", right_factors, "x1", spectator_factors
        ),
        "I": trivariate_moment_ledger(
            witness_index, idx_g, left_factors, "x0", right_factors, "x0", spectator_factors
        ),
    }

    domain = set()
    for ledger in ledgers.values():
        domain.update(map(tuple, ledger["possible_tridegrees"]))
    t0_domain = {(r, s, 0) for r, s, t in domain if t == 0 and r >= 1 and s >= 1}
    mixed_domain = {
        (r, s, t) for r, s, t in domain if r >= 1 and s >= 1 and t >= 1
    }
    t0_rows = _pairing_rows(ledgers, t0_domain)
    normalized_t0_rows = [[r, s, num, den] for r, s, _t, num, den in t0_rows]
    g_rows = _bivariate_rows(
        witness_index, idx_gcd, idx_gc, idx_gd, idx_g, left_factors, right_factors
    )
    boundary_match = normalized_t0_rows == g_rows

    pairing_rows = _pairing_rows(ledgers, mixed_domain)
    nonzero = [row for row in pairing_rows if row[-2] != 0]

    component_zero = (
        ledgers["ScSd"]["_aggregate"].get((0, 0, 0), Q(0))
        - ledgers["Sc"]["_aggregate"].get((0, 0, 0), Q(0))
        - ledgers["Sd"]["_aggregate"].get((0, 0, 0), Q(0))
        + ledgers["I"]["_aggregate"].get((0, 0, 0), Q(0))
    )
    direct_zero = _direct_mixed_pairing(bank["witness"], vec_gcd, vec_gc, vec_gd, vec_g)
    direct_match = component_zero == direct_zero

    ambiguity = None
    if not direct_match:
        ambiguity = "DEGREE_0_0_0_COMPONENT_DECOMPOSITION_DISAGREES_WITH_DIRECT_MIXED_RESPONSE"
    elif not boundary_match:
        ambiguity = "T_ZERO_BOUNDARY_DISAGREES_WITH_T3_011_G_FACTOR_SEMANTICS"
    elif any(row[-2] != 0 for row in g_rows):
        ambiguity = "PROTECTED_T3_011_G_BOUNDARY_RECONSTRUCTION_IS_NONZERO"

    return {
        "pair": list(pair),
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "coordinate_pair": [CHANNEL_COORDINATE[left], CHANNEL_COORDINATE[right]],
        "spectator_axis": spectator_axis,
        "spectator_channel_representative": spectator_channel,
        "finite_overlap_tridegrees": [[r, s, t] for r, s, t in sorted(mixed_domain)],
        "finite_overlap_sha256": sha([[r, s, t] for r, s, t in sorted(mixed_domain)]),
        "component_ledgers": {
            name: _strip_internal(ledger) for name, ledger in ledgers.items()
        },
        "pairing_rows": pairing_rows,
        "pairing_sha256": sha(pairing_rows),
        "nonzero_pairings": nonzero,
        "first_nonzero_tridegree": nonzero[0][:3] if nonzero else None,
        "t_zero_boundary_rows": normalized_t0_rows,
        "protected_G_boundary_rows": g_rows,
        "t_zero_semantics_exactly_match_G": boundary_match and not any(
            row[-2] != 0 for row in g_rows
        ),
        "degree_0_0_0_component_pairing": qjson(component_zero),
        "degree_0_0_0_direct_pairing": qjson(direct_zero),
        "degree_0_0_0_semantics_exactly_match_direct": direct_match,
        "semantic_ambiguity_kind": ambiguity,
        "all_trivariate_spectator_degrees_annihilated": ambiguity is None and not nonzero,
    }


def _blocker_result(locks: dict, blocker: str) -> dict:
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "TRIVARIATE_SPECTATOR_POLYNOMIAL_COKERNEL_AUDIT_BLOCKED",
        "predecessor_checkpoint": {
            "reviewed_head": J_REVIEWED_HEAD,
            "merge_commit": J_MERGE_COMMIT,
            "source_blobs": locks,
            "required_terminal": J_REQUIRED_TERMINAL,
        },
        "characterized_blocker": blocker,
        "possible_record_count": FROZEN_RECORD_COUNT,
        "tested_record_count": 0,
        "tested_records": [],
        "semantic_functional_ambiguity": None,
        "first_cokernel_breaking_direction": None,
        "all_trivariate_spectator_responses_cokernel_invisible": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": BLOCKER_TERMINAL,
    }


def build() -> dict:
    validate_scope()
    _solve_tridegrees.cache_clear()
    g._solve_multidegrees.cache_clear()
    locks = assert_predecessor_locks()

    j_result = j.build()
    if j_result.get("terminal") != J_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-K requires exact protected J closure terminal")
    if j_result.get("possible_record_count") != J_EXPECTED_RECORDS:
        raise AssertionError("T3-011-K J possible record count drift")
    if j_result.get("tested_record_count") != J_EXPECTED_RECORDS:
        raise AssertionError("T3-011-K J tested record count drift")
    if j_result.get("semantic_functional_ambiguity") is not None:
        raise AssertionError("T3-011-K requires J semantic ambiguity NONE")
    if j_result.get("first_cokernel_breaking_direction") is not None:
        raise AssertionError("T3-011-K requires J cokernel-breaking direction NONE")

    primitive_full, strata, specialized, supports = f.d.build_context()
    banks = f._channel_banks(primitive_full, strata, specialized, supports)
    try:
        coordinate_factors = {
            channel: g.e._coordinate_factors(channel, strata)
            for channel in CHANNEL_COORDINATE
        }
        for channel, factor_map in coordinate_factors.items():
            for sid, kinds in factor_map.items():
                for kind, (sig, _coeff) in kinds.items():
                    _positive_step(sig, f"{channel}:{sid}:{kind}")
    except AssertionError as exc:
        return _blocker_result(locks, str(exc))

    witness_indexes = {
        channel: g._witness_index(bank["witness"]) for channel, bank in banks.items()
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
                rec = _candidate_record(
                    pair,
                    endpoint,
                    uid,
                    strata,
                    bank,
                    witness_index,
                    coordinate_factors,
                    poly_cache,
                    vector_cache,
                )
                rec.update(
                    {
                        "ordinal": len(records),
                        "pair_index": pair_index,
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
                    r, s, t, num, den = rec["nonzero_pairings"][0]
                    first_escape = {
                        "ordinal": rec["ordinal"],
                        "pair": rec["pair"],
                        "endpoint": endpoint,
                        "candidate": rec["candidate"],
                        "spectator_axis": rec["spectator_axis"],
                        "tridegree": [r, s, t],
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
            raise AssertionError(
                f"T3-011-K exhaustive record drift: {len(records)} != {FROZEN_RECORD_COUNT}"
            )
        terminal = CLOSURE_TERMINAL

    tri_cache = _solve_tridegrees.cache_info()
    bi_cache = g._solve_multidegrees.cache_info()
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "TRIVARIATE_SPECTATOR_POLYNOMIAL_COKERNEL_AUDIT_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": J_REVIEWED_HEAD,
            "merge_commit": J_MERGE_COMMIT,
            "source_blobs": locks,
            "required_terminal": J_REQUIRED_TERMINAL,
            "possible_record_count": j_result["possible_record_count"],
            "tested_record_count": j_result["tested_record_count"],
            "semantic_functional_ambiguity": j_result["semantic_functional_ambiguity"],
            "first_cokernel_breaking_direction": j_result["first_cokernel_breaking_direction"],
        },
        "trivariate_spectator_class": {
            "unordered_pair_order": [list(pair) for pair in ADMITTED_PAIRS],
            "monomial_domain": "x_c^r*x_d^s*x_e^t with integers r>=1,s>=1,t>=1",
            "spectator_axis_rule": "unique remaining axis in {n,k,l}",
            "canonical_unshifted_spectator_channels": CANONICAL_SPECTATOR_CHANNEL,
            "spectator_is_unshifted": True,
            "finite_support_overlap_derived_without_degree_cutoff": True,
            "t_zero_boundary_matches_protected_G": True,
            "reciprocal_spectator_admitted": False,
            "shifted_spectator_admitted": False,
            "shifted_poles_admitted": False,
            "arbitrary_rational_functions_admitted": False,
            "support_or_harmonic_enlargement_admitted": False,
            "candidate_bank_or_scalar_namespace_widening_admitted": False,
            "recurrence_search_admitted": False,
            "correction_layer_work_admitted": False,
            "candidate_linear_combinations_admitted": False,
            "third_finite_difference_operator_admitted": False,
        },
        "execution_ledger": {
            "coordinate_factor_maps": len(coordinate_factors),
            "witness_indexes": len(witness_indexes),
            "cached_shifted_polynomials": len(poly_cache),
            "cached_semantic_vectors": len(vector_cache),
            "tridegree_solver_cache_hits": tri_cache.hits,
            "tridegree_solver_cache_misses": tri_cache.misses,
            "bivariate_boundary_solver_cache_hits": bi_cache.hits,
            "bivariate_boundary_solver_cache_misses": bi_cache.misses,
        },
        "possible_record_count": FROZEN_RECORD_COUNT,
        "tested_record_count": len(records),
        "tested_records": records,
        "semantic_functional_ambiguity": first_ambiguity,
        "first_cokernel_breaking_direction": first_escape,
        "all_trivariate_spectator_responses_cokernel_invisible": terminal == CLOSURE_TERMINAL,
        "characterized_blocker": None,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }
