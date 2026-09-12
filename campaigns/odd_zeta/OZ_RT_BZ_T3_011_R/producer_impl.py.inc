from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
Q_DIR = HERE.parent / "OZ_RT_BZ_T3_011_Q"
K_DIR = HERE.parent / "OZ_RT_BZ_T3_011_K"
L_DIR = HERE.parent / "OZ_RT_BZ_T3_011_L"

def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

q = _load(Q_DIR / "producer.py", "oz_t3_011_q_for_r")
p, o, n, m = q.p, q.o, q.n, q.m
k = m.k
a = q.a

OPERATION = "OZ-RT-BZ-T3-011-R"
STAGE = "T3_011_R_SPECTATOR_ONLY_LAURENT_AXIS_COKERNEL_AUDIT"
ISSUE = 944
PROTECTED_BASE = "1737fcc6ef103a1733c92c39e68cf6e7d34429d9"
Q_PROTECTED_MERGE = PROTECTED_BASE
Q_REQUIRED_TERMINAL = q.CLOSURE_TERMINAL
Q_REQUIRED_REMAINING_SEAM = q.REMAINING_SEAM

Q_BLOBS = {
    "CONTRACT.json": "54c4f093515a045fa97767e3e72556e2a3b74e73",
    "producer.py": "629faf6ca2782a5ac27a00e51fe7ef9fbb890504",
    "producer_impl.py.inc": "c9fc3c2de6b38ae2d9fb3c12f740a4439540fa31",
    "verifier.py": "db0150fe5e988693adcc11973ad26e58d9c5dcd9",
    "verifier_impl.py.inc": "3871c75c530789e16925746c4f4c9f2e8f41b5d8",
}
K_BLOBS = {
    "producer.py": "4a0d571a2157ffae385ec1979b85b5b94b5b2190",
    "CONTRACT.json": "6a75ca2ba209a1eaf0af4c5d6a04becd9fcac76a",
    "verifier.py": "9541e65858037ec616b958a426d130deaf79eae5",
}
L_BLOBS = {
    "producer.py": "b85d69d6fa9a3fc50b86ccd0716ace5c685a0951",
    "CONTRACT.json": "458c96d9e917b9ff73b0a2c2bb378de650e8cd36",
    "verifier.py": "3755441e5a94b891a525b4f559d88f8817a07d1b",
}

SIGNS = ("positive", "reciprocal")
POSITIVE_PATHS = ("K", "M_left", "M_right", "N")
RECIPROCAL_PATHS = ("L", "O_left", "O_right", "P")
EXPECTED_RECORDS_PER_SIGN = p.POSSIBLE_RECORD_COUNT

ESCAPE_TERMINAL = "SPECTATOR_ONLY_LAURENT_ESCAPE_FOUND"
CLOSURE_TERMINAL = "SPECTATOR_ONLY_LAURENT_AXIS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = "SPECTATOR_ONLY_LAURENT_NOT_CERTIFIED__SEMANTIC_PATH_AMBIGUITY"
BLOCKER_TERMINAL = "SPECTATOR_ONLY_LAURENT_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"
FULL_ALGEBRA_COROLLARY = "FROZEN_COORDINATE_ZERO_LAURENT_MONOMIAL_RESPONSE_ALGEBRA_COKERNEL_INVISIBLE"

def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

def validate_scope(
    shifted_poles: bool = False,
    arbitrary_rational_functions: bool = False,
    support_or_harmonic_enlargement: bool = False,
    candidate_bank_or_scalar_namespace_widening: bool = False,
    recurrence_widening: bool = False,
    correction_recombination: bool = False,
    candidate_linear_combinations: bool = False,
    third_finite_difference_operator: bool = False,
    source_or_representative_substitution: bool = False,
    arbitrary_degree_cutoff=None,
) -> None:
    if shifted_poles or arbitrary_rational_functions:
        raise AssertionError("R admits only the protected coordinate-zero spectator Laurent axis")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening:
        raise AssertionError("R forbids basis widening")
    if recurrence_widening or correction_recombination or candidate_linear_combinations:
        raise AssertionError("R forbids recurrence/correction/candidate recombination widening")
    if third_finite_difference_operator:
        raise AssertionError("R retains exactly Delta_c Delta_d")
    if source_or_representative_substitution:
        raise AssertionError("R preserves protected source, endpoint banks, and representatives")
    if arbitrary_degree_cutoff is not None:
        raise AssertionError("R forbids arbitrary degree cutoffs")

def assert_locks() -> dict:
    out = {"Q": {}, "K": {}, "L": {}}
    for name, want in Q_BLOBS.items():
        got = a.git_blob_sha1(Q_DIR / name)
        if got != want:
            raise AssertionError(f"Q source lock drift: {name}: {got} != {want}")
        out["Q"][name] = got
    for stage, directory, blobs in (("K", K_DIR, K_BLOBS), ("L", L_DIR, L_BLOBS)):
        for name, want in blobs.items():
            got = a.git_blob_sha1(directory / name)
            if got != want:
                raise AssertionError(f"{stage} source lock drift: {name}: {got} != {want}")
            out[stage][name] = got

    qc = json.loads((Q_DIR / "CONTRACT.json").read_text())
    if qc.get("operation") != "OZ-RT-BZ-T3-011-Q":
        raise AssertionError("Q contract operation drift")
    if qc.get("terminals", {}).get("closure") != Q_REQUIRED_TERMINAL:
        raise AssertionError("Q closure terminal drift")
    kc = json.loads((K_DIR / "CONTRACT.json").read_text())
    if kc.get("operation") != "OZ-RT-BZ-T3-011-K":
        raise AssertionError("K contract operation drift")
    lc = json.loads((L_DIR / "CONTRACT.json").read_text())
    if lc.get("operation") != "OZ-RT-BZ-T3-011-L":
        raise AssertionError("L contract operation drift")
    return out

def _domain_rows(module, ledgers, selector):
    domain = {
        degree
        for ledger in ledgers.values()
        for degree in map(tuple, ledger["possible_tridegrees"])
        if selector(*degree)
    }
    return module._pairing_rows(ledgers, domain)

def _component_indexes(endpoint, uid, pair, strata, bank, pcache, vcache):
    return m._component_indexes(endpoint, uid, pair, strata, bank, pcache, vcache)

def _k_positive_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    forward, pcache, vcache,
):
    left, right = pair
    _axis, sch = k._spectator(pair)
    indexes = _component_indexes(endpoint, uid, pair, strata, bank, pcache, vcache)
    ledgers = {
        "ScSd": k.trivariate_moment_ledger(
            witness_index, indexes["ScSd"], forward[left], "x1",
            forward[right], "x1", forward[sch]
        ),
        "Sc": k.trivariate_moment_ledger(
            witness_index, indexes["Sc"], forward[left], "x1",
            forward[right], "x0", forward[sch]
        ),
        "Sd": k.trivariate_moment_ledger(
            witness_index, indexes["Sd"], forward[left], "x0",
            forward[right], "x1", forward[sch]
        ),
        "I": k.trivariate_moment_ledger(
            witness_index, indexes["I"], forward[left], "x0",
            forward[right], "x0", forward[sch]
        ),
    }
    return _domain_rows(k, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _m_positive_rows(
    orientation, pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    ledgers, *_ = m._make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward, inverse, pcache, vcache, (0, 0, 1),
        f"R_positive_spectator_{orientation}",
    )
    return _domain_rows(m, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _n_positive_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    ledgers, *_ = n._make_ledgers(
        pair, endpoint, uid, n.ORIENTATIONS[0], strata, bank, witness_index,
        forward, inverse, pcache, vcache, (0, 0, 1),
        "R_positive_spectator_N",
    )
    return _domain_rows(n, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _l_reciprocal_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    left, right = pair
    _axis, sch = p._spectator(pair)
    indexes = _component_indexes(endpoint, uid, pair, strata, bank, pcache, vcache)
    ledgers = {}
    for name, lk, rk, _marker in m.COMPONENTS:
        ledgers[name] = n.signed_moment_ledger(
            witness_index,
            indexes[name],
            forward[left],
            lk,
            forward[right],
            rk,
            inverse[sch],
            (0, 0, 1),
            {
                "pair": list(pair),
                "endpoint": endpoint,
                "candidate": p.unknown_json(uid),
                "orientation": "positive_left_positive_right_negative_spectator",
                "spectator_axis": p._spectator(pair)[0],
                "component": name,
                "purpose": "R_reciprocal_spectator_L",
            },
        )
    return _domain_rows(n, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _o_reciprocal_rows(
    orientation, pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    ledgers, *_ = o._make_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward, inverse, pcache, vcache, (0, 0, 1),
        f"R_reciprocal_spectator_{orientation}", "O",
    )
    return _domain_rows(o, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _p_reciprocal_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    inverse, pcache, vcache,
):
    ledgers, *_ = p._make_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse, pcache, vcache, (0, 0, 1), "R_reciprocal_spectator_P"
    )
    return _domain_rows(p, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _record_paths(
    sign, pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse,
):
    pcache, vcache = {}, {}
    if sign == "positive":
        return {
            "K": _k_positive_rows(
                pair, endpoint, uid, strata, bank, witness_index,
                forward, pcache, vcache,
            ),
            "M_left": _m_positive_rows(
                m.ORIENTATIONS[0], pair, endpoint, uid, strata, bank, witness_index,
                forward, inverse, pcache, vcache,
            ),
            "M_right": _m_positive_rows(
                m.ORIENTATIONS[1], pair, endpoint, uid, strata, bank, witness_index,
                forward, inverse, pcache, vcache,
            ),
            "N": _n_positive_rows(
                pair, endpoint, uid, strata, bank, witness_index,
                forward, inverse, pcache, vcache,
            ),
        }
    if sign == "reciprocal":
        return {
            "L": _l_reciprocal_rows(
                pair, endpoint, uid, strata, bank, witness_index,
                forward, inverse, pcache, vcache,
            ),
            "O_left": _o_reciprocal_rows(
                o.ORIENTATIONS[0], pair, endpoint, uid, strata, bank, witness_index,
                forward, inverse, pcache, vcache,
            ),
            "O_right": _o_reciprocal_rows(
                o.ORIENTATIONS[1], pair, endpoint, uid, strata, bank, witness_index,
                forward, inverse, pcache, vcache,
            ),
            "P": _p_reciprocal_rows(
                pair, endpoint, uid, strata, bank, witness_index,
                inverse, pcache, vcache,
            ),
        }
    raise AssertionError(f"unknown spectator sign: {sign}")

def _first_path_disagreement(paths: dict):
    items = list(paths.items())
    base_name, base_rows = items[0]
    for name, rows in items[1:]:
        if rows != base_rows:
            return {
                "reference_path": base_name,
                "disagreeing_path": name,
                "reference_rows_sha256": sha(base_rows),
                "disagreeing_rows_sha256": sha(rows),
                "reference_rows": base_rows,
                "disagreeing_rows": rows,
            }
    return None

def _collect(strata, banks, forward, inverse, witness_indexes):
    signs = {}
    first_nonzero = None
    semantic_ambiguity = None
    blocker = None

    for sign in SIGNS:
        records = []
        row_count = 0
        path_names = POSITIVE_PATHS if sign == "positive" else RECIPROCAL_PATHS
        try:
            for pair_index, pair in enumerate(p.ADMITTED_PAIRS):
                for endpoint_index, endpoint in enumerate(pair):
                    bank = banks[endpoint]
                    witness_index = witness_indexes[endpoint]
                    for candidate_index, uid in enumerate(bank["candidates"]):
                        paths = _record_paths(
                            sign, pair, endpoint, uid, strata, bank, witness_index,
                            forward, inverse,
                        )
                        if tuple(paths) != path_names:
                            raise AssertionError(f"R {sign} path-order drift")
                        disagreement = _first_path_disagreement(paths)
                        canonical_rows = next(iter(paths.values()))
                        record = {
                            "pair_index": pair_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                            "pair": list(pair),
                            "endpoint": endpoint,
                            "candidate": p.unknown_json(uid),
                            "spectator_axis": p._spectator(pair)[0],
                            "path_rows_sha256": {
                                name: sha(rows) for name, rows in paths.items()
                            },
                            "canonical_rows": canonical_rows,
                            "path_agreement": disagreement is None,
                        }
                        records.append(record)
                        row_count += len(canonical_rows)
                        if disagreement is not None:
                            semantic_ambiguity = {
                                "kind": "SPECTATOR_ONLY_PARENT_PATH_DISAGREEMENT",
                                "sign": sign,
                                "pair_index": pair_index,
                                "endpoint_index": endpoint_index,
                                "candidate_index": candidate_index,
                                "pair": list(pair),
                                "endpoint": endpoint,
                                "candidate": p.unknown_json(uid),
                                **disagreement,
                            }
                            break
                        for row_index, row in enumerate(canonical_rows):
                            if int(row[-2]) != 0:
                                first_nonzero = {
                                    "sign": sign,
                                    "pair_index": pair_index,
                                    "endpoint_index": endpoint_index,
                                    "candidate_index": candidate_index,
                                    "pair": list(pair),
                                    "endpoint": endpoint,
                                    "candidate": p.unknown_json(uid),
                                    "spectator_axis": p._spectator(pair)[0],
                                    "row_index": row_index,
                                    "row": row,
                                }
                                break
                        if first_nonzero is not None or semantic_ambiguity is not None:
                            break
                    if first_nonzero is not None or semantic_ambiguity is not None:
                        break
                if first_nonzero is not None or semantic_ambiguity is not None:
                    break
        except (
            m.UnboundedSupportOverlap,
            n.UnboundedSupportOverlap,
            o.UnboundedSupportOverlap,
            p.UnboundedSupportOverlap,
        ) as exc:
            blocker = {
                "kind": "UNBOUNDED_SPECTATOR_ONLY_LAURENT_DOMAIN",
                "sign": sign,
                **getattr(exc, "evidence", {}),
            }

        signs[sign] = {
            "path_order": list(path_names),
            "record_count": len(records),
            "row_count": row_count,
            "record_sha256": sha(records),
            "all_paths_agree": semantic_ambiguity is None,
            "records": records,
        }
        if first_nonzero is not None or semantic_ambiguity is not None or blocker is not None:
            break

    complete = (
        first_nonzero is None
        and semantic_ambiguity is None
        and blocker is None
        and set(signs) == set(SIGNS)
    )
    if complete:
        for sign in SIGNS:
            if signs[sign]["record_count"] != EXPECTED_RECORDS_PER_SIGN:
                raise AssertionError(
                    f"R {sign} coverage drift: {signs[sign]['record_count']} "
                    f"!= {EXPECTED_RECORDS_PER_SIGN}"
                )

    return {
        "signs": signs,
        "expected_records_per_sign": EXPECTED_RECORDS_PER_SIGN,
        "first_nonzero": first_nonzero,
        "semantic_path_ambiguity": semantic_ambiguity,
        "characterized_blocker": blocker,
        "coverage_complete": complete,
        "all_parent_paths_agree": complete,
        "all_spectator_only_responses_annihilated": complete,
    }

def build() -> dict:
    validate_scope()
    locks = assert_locks()

    m.solve_signed_tridegrees.cache_clear()
    n.solve_signed_tridegrees.cache_clear()

    primitive_full, strata, specialized, supports = o.f.d.build_context()
    banks = o.f._channel_banks(primitive_full, strata, specialized, supports)
    forward = {
        channel: o.g.e._coordinate_factors(channel, strata)
        for channel in o.CHANNEL_COORDINATE
    }
    inverse = {
        channel: o.h.inverse_coordinate_factors(channel, strata)
        for channel in o.CHANNEL_COORDINATE
    }
    witness_indexes = {
        channel: o.g._witness_index(bank["witness"])
        for channel, bank in banks.items()
    }

    audit = _collect(strata, banks, forward, inverse, witness_indexes)
    if audit["characterized_blocker"] is not None:
        terminal = BLOCKER_TERMINAL
    elif audit["semantic_path_ambiguity"] is not None:
        terminal = AMBIGUITY_TERMINAL
    elif audit["first_nonzero"] is not None:
        terminal = ESCAPE_TERMINAL
    else:
        terminal = CLOSURE_TERMINAL

    full_closed = terminal == CLOSURE_TERMINAL
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "protected_base": PROTECTED_BASE,
        "predecessor": {
            "operation": "OZ-RT-BZ-T3-011-Q",
            "protected_merge": Q_PROTECTED_MERGE,
            "required_terminal": Q_REQUIRED_TERMINAL,
            "required_remaining_seam": Q_REQUIRED_REMAINING_SEAM,
            "source_locks": locks,
        },
        "spectator_only_axis_audit": audit,
        "terminal": terminal,
        "full_coordinate_zero_laurent_algebra_corollary": (
            FULL_ALGEBRA_COROLLARY if full_closed else None
        ),
        "full_coordinate_zero_laurent_algebra_closed": full_closed,
        "partition_basis": {
            "all_active_and_spectator_exponents_nonzero": "protected T3-011 K/L/M/N/O/P",
            "exactly_one_active_exponent_zero_with_nonzero_spectator": "protected T3-011-Q",
            "both_active_exponents_zero_with_nonzero_spectator": OPERATION,
            "zero_spectator_pairwise_and_single_axis_boundaries": "protected T3-011 E/G/H/I/J boundary semantics",
        },
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }

if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, separators=(",", ":")))
