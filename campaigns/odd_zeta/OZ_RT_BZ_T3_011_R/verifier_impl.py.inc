from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import producer

def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected verifier: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def _load_parent_verifier(stage: str, parent, directory: Path):
    previous = sys.modules.get("producer")
    sys.modules["producer"] = parent
    try:
        return _load(
            directory / "verifier.py",
            f"oz_t3_011_{stage.lower()}_verifier_for_r",
        )
    finally:
        if previous is None:
            sys.modules.pop("producer", None)
        else:
            sys.modules["producer"] = previous

kv = _load_parent_verifier("K", producer.k, producer.K_DIR)
mv = _load_parent_verifier("M", producer.m, producer.q.M_DIR)
nv = _load_parent_verifier("N", producer.n, producer.q.N_DIR)
ov = _load_parent_verifier("O", producer.o, producer.q.O_DIR)
pv = _load_parent_verifier("P", producer.p, producer.q.P_DIR)

def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

def _independent_locks() -> dict:
    return producer.assert_locks()

def _vrows(module, ledgers, selector):
    domain = set().union(*(part[0] for part in ledgers.values()))
    selected = {degree for degree in domain if selector(*degree)}
    return module._rows(ledgers, selected)

def _k_positive_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    forward, pcache, vcache,
):
    left, right = pair
    _axis, sch = kv._spectator(pair)
    idx = {}
    for name, shifts in (
        ("I", ()),
        ("Sc", (left,)),
        ("Sd", (right,)),
        ("ScSd", (left, right)),
    ):
        idx[name] = kv._cached_vector_index(
            endpoint, uid, shifts, strata, bank, pcache, vcache
        )[1]
    ledgers = {
        "ScSd": kv._ledger(
            witness_index, idx["ScSd"], forward[left], "x1",
            forward[right], "x1", forward[sch]
        ),
        "Sc": kv._ledger(
            witness_index, idx["Sc"], forward[left], "x1",
            forward[right], "x0", forward[sch]
        ),
        "Sd": kv._ledger(
            witness_index, idx["Sd"], forward[left], "x0",
            forward[right], "x1", forward[sch]
        ),
        "I": kv._ledger(
            witness_index, idx["I"], forward[left], "x0",
            forward[right], "x0", forward[sch]
        ),
    }
    domain = {
        degree
        for ledger in ledgers.values()
        for degree in map(tuple, ledger["possible_tridegrees"])
        if degree[0] == 0 and degree[1] == 0 and degree[2] >= 1
    }
    return kv._pairing_rows(ledgers, domain)

def _m_positive_rows(
    orientation, pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    ledgers, *_ = mv._build_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward, inverse, pcache, vcache, (0, 0, 1),
        f"independent_R_positive_{orientation}",
    )
    return _vrows(mv, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _n_positive_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    ledgers, *_ = nv._build_ledgers(
        pair, endpoint, uid, producer.n.ORIENTATIONS[0],
        strata, bank, witness_index, forward, inverse, pcache, vcache,
        (0, 0, 1), "independent_R_positive_N",
    )
    return _vrows(nv, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _l_reciprocal_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    ledgers, *_ = ov._build_ledgers(
        pair, endpoint, uid, producer.o.ORIENTATIONS[0],
        strata, bank, witness_index, forward, inverse, pcache, vcache,
        (0, 0, 1), "independent_R_reciprocal_L", "L",
    )
    return _vrows(ov, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _o_reciprocal_rows(
    orientation, pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    ledgers, *_ = ov._build_ledgers(
        pair, endpoint, uid, orientation, strata, bank, witness_index,
        forward, inverse, pcache, vcache, (0, 0, 1),
        f"independent_R_reciprocal_{orientation}", "O",
    )
    return _vrows(ov, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

def _p_reciprocal_rows(
    pair, endpoint, uid, strata, bank, witness_index,
    inverse, pcache, vcache,
):
    ledgers, *_ = pv._build_ledgers(
        pair, endpoint, uid, strata, bank, witness_index,
        inverse, pcache, vcache, (0, 0, 1), "independent_R_reciprocal_P",
    )
    return _vrows(pv, ledgers, lambda r, s, t: r == 0 and s == 0 and t >= 1)

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
                producer.m.ORIENTATIONS[0], pair, endpoint, uid, strata, bank,
                witness_index, forward, inverse, pcache, vcache,
            ),
            "M_right": _m_positive_rows(
                producer.m.ORIENTATIONS[1], pair, endpoint, uid, strata, bank,
                witness_index, forward, inverse, pcache, vcache,
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
                producer.o.ORIENTATIONS[0], pair, endpoint, uid, strata, bank,
                witness_index, forward, inverse, pcache, vcache,
            ),
            "O_right": _o_reciprocal_rows(
                producer.o.ORIENTATIONS[1], pair, endpoint, uid, strata, bank,
                witness_index, forward, inverse, pcache, vcache,
            ),
            "P": _p_reciprocal_rows(
                pair, endpoint, uid, strata, bank, witness_index,
                inverse, pcache, vcache,
            ),
        }
    raise AssertionError(f"unknown sign: {sign}")

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

    for sign in producer.SIGNS:
        records = []
        row_count = 0
        path_names = (
            producer.POSITIVE_PATHS
            if sign == "positive"
            else producer.RECIPROCAL_PATHS
        )
        try:
            for pair_index, pair in enumerate(producer.p.ADMITTED_PAIRS):
                for endpoint_index, endpoint in enumerate(pair):
                    bank = banks[endpoint]
                    witness_index = witness_indexes[endpoint]
                    for candidate_index, uid in enumerate(bank["candidates"]):
                        paths = _record_paths(
                            sign, pair, endpoint, uid, strata, bank, witness_index,
                            forward, inverse,
                        )
                        if tuple(paths) != path_names:
                            raise AssertionError(f"independent R {sign} path-order drift")
                        disagreement = _first_path_disagreement(paths)
                        canonical_rows = next(iter(paths.values()))
                        record = {
                            "pair_index": pair_index,
                            "endpoint_index": endpoint_index,
                            "candidate_index": candidate_index,
                            "pair": list(pair),
                            "endpoint": endpoint,
                            "candidate": producer.p.unknown_json(uid),
                            "spectator_axis": producer.p._spectator(pair)[0],
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
                                "candidate": producer.p.unknown_json(uid),
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
                                    "candidate": producer.p.unknown_json(uid),
                                    "spectator_axis": producer.p._spectator(pair)[0],
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
        except Exception as exc:
            if exc.__class__.__name__ != "UnboundedSupportOverlap":
                raise
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
        and set(signs) == set(producer.SIGNS)
    )
    if complete:
        for sign in producer.SIGNS:
            if signs[sign]["record_count"] != producer.EXPECTED_RECORDS_PER_SIGN:
                raise AssertionError(
                    f"independent R {sign} coverage drift: "
                    f"{signs[sign]['record_count']} != {producer.EXPECTED_RECORDS_PER_SIGN}"
                )

    return {
        "signs": signs,
        "expected_records_per_sign": producer.EXPECTED_RECORDS_PER_SIGN,
        "first_nonzero": first_nonzero,
        "semantic_path_ambiguity": semantic_ambiguity,
        "characterized_blocker": blocker,
        "coverage_complete": complete,
        "all_parent_paths_agree": complete,
        "all_spectator_only_responses_annihilated": complete,
    }

def verify(result: dict) -> dict:
    _independent_locks()
    producer.validate_scope()

    mv.independent_solve.cache_clear()
    nv.independent_solve.cache_clear()
    ov.independent_solve.cache_clear()
    pv.independent_solve.cache_clear()
    kv._independent_tridegrees.cache_clear()

    primitive_full, strata, specialized, supports = ov.f.d.build_context()
    banks = ov.f._channel_banks(primitive_full, strata, specialized, supports)
    forward = {
        channel: ov.g.e._coordinate_factors(channel, strata)
        for channel in producer.o.CHANNEL_COORDINATE
    }
    inverse = {
        channel: ov.h.inverse_coordinate_factors(channel, strata)
        for channel in producer.o.CHANNEL_COORDINATE
    }
    witness_indexes = {
        channel: ov.vg._witness_index(bank["witness"])
        for channel, bank in banks.items()
    }

    audit = _collect(strata, banks, forward, inverse, witness_indexes)
    if audit["characterized_blocker"] is not None:
        terminal = producer.BLOCKER_TERMINAL
    elif audit["semantic_path_ambiguity"] is not None:
        terminal = producer.AMBIGUITY_TERMINAL
    elif audit["first_nonzero"] is not None:
        terminal = producer.ESCAPE_TERMINAL
    else:
        terminal = producer.CLOSURE_TERMINAL

    if result.get("operation") != producer.OPERATION or result.get("issue") != producer.ISSUE:
        raise AssertionError("R identity drift")
    if result.get("protected_base") != producer.PROTECTED_BASE:
        raise AssertionError("R protected-base drift")
    pred = result.get("predecessor", {})
    if pred.get("operation") != "OZ-RT-BZ-T3-011-Q":
        raise AssertionError("R predecessor operation drift")
    if pred.get("protected_merge") != producer.Q_PROTECTED_MERGE:
        raise AssertionError("R Q merge binding drift")
    if pred.get("required_terminal") != producer.Q_REQUIRED_TERMINAL:
        raise AssertionError("R Q terminal binding drift")
    if pred.get("required_remaining_seam") != producer.Q_REQUIRED_REMAINING_SEAM:
        raise AssertionError("R Q seam binding drift")

    if result.get("spectator_only_axis_audit") != audit:
        raise AssertionError("R producer audit disagrees with independent replay")
    if result.get("terminal") != terminal:
        raise AssertionError("R terminal disagrees with independent replay")

    closed = terminal == producer.CLOSURE_TERMINAL
    expected_corollary = producer.FULL_ALGEBRA_COROLLARY if closed else None
    if result.get("full_coordinate_zero_laurent_algebra_corollary") != expected_corollary:
        raise AssertionError("R full-algebra structural corollary drift")
    if result.get("full_coordinate_zero_laurent_algebra_closed") is not closed:
        raise AssertionError("R full-algebra closure flag drift")

    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("residual-sum claim inflation")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("proof/promotion claim inflation")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status inflation")

    return {
        "terminal": terminal,
        "first_nonzero": audit["first_nonzero"],
        "semantic_path_ambiguity": audit["semantic_path_ambiguity"],
        "characterized_blocker": audit["characterized_blocker"],
        "coverage_complete": audit["coverage_complete"],
        "all_parent_paths_agree": audit["all_parent_paths_agree"],
        "all_spectator_only_responses_annihilated":
            audit["all_spectator_only_responses_annihilated"],
        "full_coordinate_zero_laurent_algebra_corollary": expected_corollary,
        "independent_signs": audit["signs"],
    }

if __name__ == "__main__":
    payload = producer.build()
    print(json.dumps(verify(payload), sort_keys=True, separators=(",", ":")))
