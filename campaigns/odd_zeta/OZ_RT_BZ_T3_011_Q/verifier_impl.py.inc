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
            f"oz_t3_011_{stage.lower()}_verifier_for_q",
        )
    finally:
        if previous is None:
            sys.modules.pop("producer", None)
        else:
            sys.modules["producer"] = previous


mv = _load_parent_verifier("M", producer.m, producer.M_DIR)
nv = _load_parent_verifier("N", producer.n, producer.N_DIR)
ov = _load_parent_verifier("O", producer.o, producer.O_DIR)
pv = _load_parent_verifier("P", producer.p, producer.P_DIR)


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


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


def _vrows(module, ledgers, selector):
    domain = set().union(*(part[0] for part in ledgers.values()))
    selected = {degree for degree in domain if selector(*degree)}
    return module._rows(ledgers, selected)


def _independent_face_rows(
    family, side, pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    lower = (0, 1, 1) if side == "left" else (1, 0, 1)
    selector = (
        (lambda r, s, t: r == 0 and s >= 1 and t >= 1)
        if side == "left"
        else (lambda r, s, t: s == 0 and r >= 1 and t >= 1)
    )

    if family == "++":
        orientation = (
            "negative_left_positive_right"
            if side == "left"
            else "positive_left_negative_right"
        )
        ledgers, *_ = mv._build_ledgers(
            pair, endpoint, uid, orientation, strata, bank, witness_index,
            forward, inverse, pcache, vcache, lower,
            f"independent_Q_{family}_{side}_active_zero_face",
        )
        return _vrows(mv, ledgers, selector)

    if family == "-+":
        ledgers, *_ = nv._build_ledgers(
            pair, endpoint, uid, "negative_left_negative_right",
            strata, bank, witness_index, forward, inverse, pcache, vcache,
            lower, f"independent_Q_{family}_{side}_active_zero_face",
        )
        return _vrows(nv, ledgers, selector)

    if family == "+-":
        orientation = (
            "negative_left_positive_right"
            if side == "left"
            else "positive_left_negative_right"
        )
        ledgers, *_ = ov._build_ledgers(
            pair, endpoint, uid, orientation, strata, bank, witness_index,
            forward, inverse, pcache, vcache, lower,
            f"independent_Q_{family}_{side}_active_zero_face",
        )
        return _vrows(ov, ledgers, selector)

    if family == "--":
        ledgers, *_ = pv._build_ledgers(
            pair, endpoint, uid, strata, bank, witness_index,
            inverse, pcache, vcache, lower,
            f"independent_Q_{family}_{side}_active_zero_face",
        )
        return _vrows(pv, ledgers, selector)

    raise AssertionError(f"unknown independent Q face family: {family}")


def _new_family():
    return {
        "record_count": 0,
        "row_count": 0,
        "record_sha256": None,
        "first_nonzero": None,
    }


def _independent_partition(strata, banks, forward, inverse, witness_indexes):
    families = {family: _new_family() for family in producer.FAMILY_ORDER}
    first_nonzero = None
    blocker = None

    for family in producer.FAMILY_ORDER:
        digest_records = []
        pcache, vcache = {}, {}
        try:
            for pair_index, pair in enumerate(producer.p.ADMITTED_PAIRS):
                for endpoint_index, endpoint in enumerate(pair):
                    bank = banks[endpoint]
                    witness_index = witness_indexes[endpoint]
                    for candidate_index, uid in enumerate(bank["candidates"]):
                        for side in producer.SIDE_ORDER:
                            rows = _independent_face_rows(
                                family, side, pair, endpoint, uid, strata, bank,
                                witness_index, forward, inverse, pcache, vcache,
                            )
                            record = {
                                "pair_index": pair_index,
                                "endpoint_index": endpoint_index,
                                "candidate_index": candidate_index,
                                "pair": list(pair),
                                "endpoint": endpoint,
                                "candidate": producer.p.unknown_json(uid),
                                "side": side,
                                "rows": rows,
                            }
                            digest_records.append(record)
                            families[family]["record_count"] += 1
                            families[family]["row_count"] += len(rows)
                            for row_index, row in enumerate(rows):
                                if int(row[-2]) != 0:
                                    witness = {
                                        "family": family,
                                        "pair_index": pair_index,
                                        "endpoint_index": endpoint_index,
                                        "candidate_index": candidate_index,
                                        "pair": list(pair),
                                        "endpoint": endpoint,
                                        "candidate": producer.p.unknown_json(uid),
                                        "side": side,
                                        "row_index": row_index,
                                        "row": row,
                                    }
                                    families[family]["first_nonzero"] = witness
                                    first_nonzero = witness
                                    break
                            if first_nonzero is not None:
                                break
                        if first_nonzero is not None:
                            break
                    if first_nonzero is not None:
                        break
                if first_nonzero is not None:
                    break
        except (
            producer.m.UnboundedSupportOverlap,
            producer.n.UnboundedSupportOverlap,
            producer.o.UnboundedSupportOverlap,
            producer.p.UnboundedSupportOverlap,
        ) as exc:
            blocker = {
                "kind": "UNBOUNDED_ACTIVE_ZERO_FACE_DOMAIN",
                "family": family,
                **getattr(exc, "evidence", {}),
            }
        families[family]["record_sha256"] = sha(digest_records)
        if first_nonzero is not None or blocker is not None:
            break

    complete = first_nonzero is None and blocker is None
    if complete:
        for family in producer.FAMILY_ORDER:
            if families[family]["record_count"] != producer.EXPECTED_FACE_RECORDS_PER_FAMILY:
                raise AssertionError(
                    f"independent Q {family} coverage drift: "
                    f"{families[family]['record_count']} != "
                    f"{producer.EXPECTED_FACE_RECORDS_PER_FAMILY}"
                )

    return {
        "families": families,
        "expected_face_records_per_family": producer.EXPECTED_FACE_RECORDS_PER_FAMILY,
        "first_nonzero": first_nonzero,
        "characterized_blocker": blocker,
        "all_one_active_zero_sign_families_annihilated": complete,
        "coverage_complete": complete,
    }


def verify(result: dict) -> dict:
    _locks()
    producer.validate_scope()

    mv.independent_solve.cache_clear()
    nv.independent_solve.cache_clear()
    ov.independent_solve.cache_clear()
    pv.independent_solve.cache_clear()

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

    partition = _independent_partition(
        strata, banks, forward, inverse, witness_indexes
    )
    if partition["characterized_blocker"] is not None:
        terminal = producer.BLOCKER_TERMINAL
    elif partition["first_nonzero"] is not None:
        terminal = producer.ESCAPE_TERMINAL
    else:
        terminal = producer.CLOSURE_TERMINAL

    if result.get("operation") != producer.OPERATION or result.get("issue") != producer.ISSUE:
        raise AssertionError("Q identity drift")
    if result.get("protected_base") != producer.PROTECTED_BASE:
        raise AssertionError("Q protected-base drift")
    if result.get("active_zero_face_partition") != partition:
        raise AssertionError("Q producer face partition disagrees with independent replay")
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
        raise AssertionError("Q must not nominate a seam after escape/blocker")

    if result.get("residual_sum_zero_proved") is not False:
        raise AssertionError("residual-sum claim inflation")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("proof/promotion claim inflation")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status inflation")

    return {
        "terminal": terminal,
        "first_nonzero": partition["first_nonzero"],
        "characterized_blocker": partition["characterized_blocker"],
        "all_one_active_zero_sign_families_annihilated":
            partition["all_one_active_zero_sign_families_annihilated"],
        "coverage_complete": partition["coverage_complete"],
        "remaining_lower_dimensional_seam": (
            producer.REMAINING_SEAM
            if terminal == producer.CLOSURE_TERMINAL
            else None
        ),
        "independent_face_families": partition["families"],
    }


if __name__ == "__main__":
    payload = producer.build()
    print(json.dumps(verify(payload), sort_keys=True, separators=(",", ":")))
