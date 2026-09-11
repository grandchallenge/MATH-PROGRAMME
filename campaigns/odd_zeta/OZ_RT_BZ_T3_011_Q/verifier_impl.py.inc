from __future__ import annotations

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
        return _load(directory / "verifier.py", f"oz_t3_011_{stage.lower()}_verifier_for_q")
    finally:
        if previous is None:
            sys.modules.pop("producer", None)
        else:
            sys.modules["producer"] = previous


mv = _load_parent_verifier("M", producer.m, producer.M_DIR)
nv = _load_parent_verifier("N", producer.n, producer.N_DIR)
ov = _load_parent_verifier("O", producer.o, producer.O_DIR)
pv = _load_parent_verifier("P", producer.p, producer.P_DIR)


def _locks() -> dict:
    out = {}
    for stage, spec in producer.LOCKS.items():
        out[stage] = {}
        for name, want in spec["blobs"].items():
            got = producer.a.git_blob_sha1(spec["dir"] / name)
            if got != want:
                raise AssertionError(f"independent {stage} source lock drift: {name}")
            out[stage][name] = got
        contract = json.loads((spec["dir"] / "CONTRACT.json").read_text())
        if contract.get("operation") != spec["operation"]:
            raise AssertionError(f"independent {stage} operation drift")
        if contract.get("terminals", {}).get("closure") != spec["terminal"]:
            raise AssertionError(f"independent {stage} terminal drift")
    return out


def _first(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return a if json.dumps(a, sort_keys=True) <= json.dumps(b, sort_keys=True) else b


def _scan(records, field, family, source, side=None):
    count = 0
    first = None
    for index, record in enumerate(records):
        rows = record.get(field, [])
        count += len(rows)
        for row_index, row in enumerate(rows):
            if int(row[-2]) != 0:
                witness = {
                    "family": family,
                    "source_stage": source,
                    "record_index": index,
                    "row_index": row_index,
                    "pair": record.get("pair"),
                    "endpoint": record.get("endpoint"),
                    "candidate": record.get("candidate"),
                    "orientation": record.get("orientation"),
                    "side": side,
                    "row": row,
                }
                first = _first(first, witness)
    return {"record_count": len(records), "row_count": count, "first_nonzero": first}


def _independent_summary(mr, nr, orr, pr):
    m_records = mr["tested_records"]
    n_records = nr["tested_records"]
    o_records = orr["tested_records"]
    p_records = pr["tested_records"]

    if not all(x.get("reciprocal_degree_zero_semantics_exactly_match_K") is True for x in m_records):
        raise AssertionError("independent M/K face partition drift")
    if not all(x.get("reciprocal_degree_zero_semantics_exactly_match_M") is True for x in n_records):
        raise AssertionError("independent N/M face partition drift")
    if not all(x.get("reciprocal_active_degree_zero_semantics_exactly_match_L") is True for x in o_records):
        raise AssertionError("independent O/L face partition drift")
    if not all(x.get("positive_active_degree_zero_anchor_kind") == "DIRECT_RESPONSE_ONLY_NOT_T3_011_I" for x in o_records):
        raise AssertionError("independent O anchor-kind drift")
    if not all(x.get("active_reciprocal_degree_zero_anchor_kind") == "DIRECT_RESPONSE_ONLY_NO_PREDECESSOR_CLASS_PROMOTION" for x in p_records):
        raise AssertionError("independent P anchor-kind drift")

    pp = _scan(m_records, "protected_K_boundary_rows", "++", "M")
    mp_l = _scan(n_records, "protected_M_left_boundary_rows", "-+", "N", "left")
    mp_r = _scan(n_records, "protected_M_right_boundary_rows", "-+", "N", "right")
    pm = _scan(o_records, "reciprocal_active_degree_zero_boundary_rows", "+-", "O")
    mm_o = _scan(o_records, "positive_active_degree_zero_direct_response_rows", "--", "O")
    mm_pl = _scan(p_records, "left_reciprocal_degree_zero_direct_response_rows", "--", "P", "left")
    mm_pr = _scan(p_records, "right_reciprocal_degree_zero_direct_response_rows", "--", "P", "right")

    mp_first = _first(mp_l["first_nonzero"], mp_r["first_nonzero"])
    mm_first = _first(_first(mm_o["first_nonzero"], mm_pl["first_nonzero"]), mm_pr["first_nonzero"])
    overall = None
    for item in (pp["first_nonzero"], mp_first, pm["first_nonzero"], mm_first):
        overall = _first(overall, item)

    return {
        "families": {
            "++": pp,
            "-+": {"left": mp_l, "right": mp_r, "first_nonzero": mp_first},
            "+-": pm,
            "--": {
                "O_positive_zero": mm_o,
                "P_left_zero": mm_pl,
                "P_right_zero": mm_pr,
                "first_nonzero": mm_first,
            },
        },
        "first_nonzero": overall,
        "all_one_active_zero_sign_families_annihilated": overall is None,
    }


def verify(result: dict) -> dict:
    _locks()
    producer.validate_scope()

    mr = producer.m.build()
    nr = producer.n.build()
    orr = producer.o.build()
    pr = producer.p.build()

    raw = {"M": mr, "N": nr, "O": orr, "P": pr}
    expected_terminals = {
        "M": producer.m.CLOSURE_TERMINAL,
        "N": producer.n.CLOSURE_TERMINAL,
        "O": producer.o.CLOSURE_TERMINAL,
        "P": producer.p.CLOSURE_TERMINAL,
    }
    parent_replays = {
        "M": mv.verify(mr),
        "N": nv.verify(nr),
        "O": ov.verify(orr),
        "P": pv.verify(pr),
    }
    for stage, expected in expected_terminals.items():
        if raw[stage].get("terminal") != expected:
            raise AssertionError(f"protected {stage} producer did not reproduce closure")
        if raw[stage].get("tested_record_count") != raw[stage].get("possible_record_count"):
            raise AssertionError(f"protected {stage} producer replay incomplete")
        replay = parent_replays[stage]
        if replay.get("terminal") != expected:
            raise AssertionError(f"independent {stage} verifier did not reproduce closure")

    summary = _independent_summary(mr, nr, orr, pr)
    terminal = producer.ESCAPE_TERMINAL if summary["first_nonzero"] is not None else producer.CLOSURE_TERMINAL

    if result.get("operation") != producer.OPERATION or result.get("issue") != producer.ISSUE:
        raise AssertionError("Q identity drift")
    if result.get("protected_base") != producer.PROTECTED_BASE:
        raise AssertionError("Q protected-base drift")
    if result.get("active_zero_face_partition") != summary:
        raise AssertionError("Q producer face summary disagrees with independent replay")
    if result.get("terminal") != terminal:
        raise AssertionError("Q terminal disagrees with independent replay")
    if result.get("full_coordinate_zero_laurent_algebra_corollary") is not None:
        raise AssertionError("Q overclaims full Laurent algebra closure")
    if result.get("full_coordinate_zero_laurent_algebra_closed") is not False:
        raise AssertionError("Q must leave the spectator-only seam open")
    if terminal == producer.CLOSURE_TERMINAL:
        if result.get("remaining_lower_dimensional_seam") != producer.REMAINING_SEAM:
            raise AssertionError("Q remaining seam drift")
    elif result.get("remaining_lower_dimensional_seam") is not None:
        raise AssertionError("Q must not nominate a seam after an escape")

    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("residual-sum claim inflation")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("proof/promotion claim inflation")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status inflation")

    return {
        "terminal": terminal,
        "first_nonzero": summary["first_nonzero"],
        "all_one_active_zero_sign_families_annihilated": summary["all_one_active_zero_sign_families_annihilated"],
        "remaining_lower_dimensional_seam": producer.REMAINING_SEAM if terminal == producer.CLOSURE_TERMINAL else None,
        "parent_terminals": expected_terminals,
    }


if __name__ == "__main__":
    payload = producer.build()
    print(json.dumps(verify(payload), sort_keys=True, separators=(",", ":")))
