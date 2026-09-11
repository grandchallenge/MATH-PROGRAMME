from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
P_DIR = HERE.parent / "OZ_RT_BZ_T3_011_P"
O_DIR = HERE.parent / "OZ_RT_BZ_T3_011_O"
N_DIR = HERE.parent / "OZ_RT_BZ_T3_011_N"
M_DIR = HERE.parent / "OZ_RT_BZ_T3_011_M"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


p = _load(P_DIR / "producer.py", "oz_t3_011_p_for_q")
o = p.o
n = o.n
m = n.m
a = p.a

OPERATION = "OZ-RT-BZ-T3-011-Q"
STAGE = "T3_011_Q_ACTIVE_ZERO_TRIVARIATE_LAURENT_FACE_AUDIT"
ISSUE = 939
PROTECTED_BASE = "954f6382d4d5499bf3653a34627ac46605980cd3"

LOCKS = {
    "M": {
        "dir": M_DIR,
        "operation": "OZ-RT-BZ-T3-011-M",
        "terminal": m.CLOSURE_TERMINAL,
        "blobs": {
            "producer.py": "19ec58bd410359f3721236bbabc612d0f649636b",
            "CONTRACT.json": "e3aaea4f714c3e243fd8a782baf59e05111380a6",
            "verifier.py": "8621c594d510b54928a798259fadcf67f7fb6b82",
        },
    },
    "N": {
        "dir": N_DIR,
        "operation": "OZ-RT-BZ-T3-011-N",
        "terminal": n.CLOSURE_TERMINAL,
        "blobs": {
            "producer.py": "0a89560dc074687c75091c2891685a0619bee745",
            "CONTRACT.json": "d5e6051512fb02b05e61f12312566bd8fd9f28b9",
            "verifier.py": "b197908d0297e283fc8e7f603978dfd358736989",
        },
    },
    "O": {
        "dir": O_DIR,
        "operation": "OZ-RT-BZ-T3-011-O",
        "terminal": o.CLOSURE_TERMINAL,
        "blobs": {
            "producer.py": "39ff905f2837d434fff20be5eea9abef6fa852a6",
            "CONTRACT.json": "9bb7dce32472ebbb6a09f036ea7932f85151dd77",
            "verifier.py": "325cdfec0538c25a0cc709ab5d150b98632b288c",
        },
    },
    "P": {
        "dir": P_DIR,
        "operation": "OZ-RT-BZ-T3-011-P",
        "terminal": p.CLOSURE_TERMINAL,
        "blobs": {
            "producer.py": "9853c445ba856a0dff4afd4e7c0a7a9f5c56a7a5",
            "CONTRACT.json": "a8b36f356e296c53443975b0e68c6841b2483a76",
            "verifier.py": "99cf73227224a86bac353d9a972c7404ed4b224f",
        },
    },
}

ESCAPE_TERMINAL = "ACTIVE_ZERO_LAURENT_FACE_ESCAPE_FOUND"
CLOSURE_TERMINAL = "ACTIVE_ZERO_LAURENT_FACES_COKERNEL_INVISIBLE"
BLOCKER_TERMINAL = "ACTIVE_ZERO_LAURENT_FACES_NOT_CERTIFIED__CHARACTERIZED_BLOCKER"
FULL_ALGEBRA_COROLLARY = "FROZEN_COORDINATE_ZERO_LAURENT_MONOMIAL_RESPONSE_ALGEBRA_COKERNEL_INVISIBLE"
REMAINING_SEAM = "BOTH_ACTIVE_EXPONENTS_ZERO_WITH_NONZERO_SPECTATOR_EXPONENT"
FAMILY_ORDER = ("++", "-+", "+-", "--")
SIDE_ORDER = ("left", "right")
EXPECTED_FACE_RECORDS_PER_FAMILY = 2 * p.POSSIBLE_RECORD_COUNT


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
        raise AssertionError("Q admits only the protected coordinate-zero Laurent faces")
    if support_or_harmonic_enlargement or candidate_bank_or_scalar_namespace_widening:
        raise AssertionError("Q forbids basis widening")
    if recurrence_widening or correction_recombination or candidate_linear_combinations:
        raise AssertionError("Q forbids recurrence/correction/candidate recombination widening")
    if third_finite_difference_operator:
        raise AssertionError("Q retains exactly Delta_c Delta_d")
    if source_or_representative_substitution:
        raise AssertionError("Q preserves the protected source and representative")
    if arbitrary_degree_cutoff is not None:
        raise AssertionError("Q forbids arbitrary degree cutoffs")


def assert_locks() -> dict:
    out = {}
    for stage, spec in LOCKS.items():
        out[stage] = {}
        for name, want in spec["blobs"].items():
            got = a.git_blob_sha1(spec["dir"] / name)
            if got != want:
                raise AssertionError(f"{stage} source lock drift: {name}: {got} != {want}")
            out[stage][name] = got
        contract = json.loads((spec["dir"] / "CONTRACT.json").read_text())
        if contract.get("operation") != spec["operation"]:
            raise AssertionError(f"{stage} operation drift")
        if contract.get("terminals", {}).get("closure") != spec["terminal"]:
            raise AssertionError(f"{stage} closure terminal drift")
    return out


def _domain_rows(module, ledgers, selector):
    domain = {
        degree
        for ledger in ledgers.values()
        for degree in map(tuple, ledger["possible_tridegrees"])
        if selector(*degree)
    }
    return module._pairing_rows(ledgers, domain)


def _producer_face_rows(
    family, side, pair, endpoint, uid, strata, bank, witness_index,
    forward, inverse, pcache, vcache,
):
    if family == "++":
        orientation = (
            "negative_left_positive_right"
            if side == "left"
            else "positive_left_negative_right"
        )
        return m._k_zero_boundary_rows(
            pair, endpoint, uid, orientation, strata, bank, witness_index,
            forward, pcache, vcache,
        )

    if family == "-+":
        return n._n_zero_boundary_rows(
            pair, endpoint, uid, side, strata, bank, witness_index,
            forward, inverse, pcache, vcache,
        )

    if family == "+-":
        orientation = (
            "negative_left_positive_right"
            if side == "left"
            else "positive_left_negative_right"
        )
        lower = (0, 1, 1) if side == "left" else (1, 0, 1)
        selector = (
            (lambda r, s, t: r == 0 and s >= 1 and t >= 1)
            if side == "left"
            else (lambda r, s, t: s == 0 and r >= 1 and t >= 1)
        )
        ledgers, *_ = o._make_ledgers(
            pair, endpoint, uid, orientation, strata, bank, witness_index,
            forward, inverse, pcache, vcache, lower,
            f"Q_{family}_{side}_active_zero_face", "O",
        )
        return o._selected_rows(ledgers, selector)

    if family == "--":
        lower = (0, 1, 1) if side == "left" else (1, 0, 1)
        selector = (
            (lambda r, s, t: r == 0 and s >= 1 and t >= 1)
            if side == "left"
            else (lambda r, s, t: s == 0 and r >= 1 and t >= 1)
        )
        ledgers, *_ = p._make_ledgers(
            pair, endpoint, uid, strata, bank, witness_index,
            inverse, pcache, vcache, lower,
            f"Q_{family}_{side}_active_zero_face",
        )
        return p._selected_rows(ledgers, selector)

    raise AssertionError(f"unknown Q face family: {family}")


def _new_family():
    return {
        "record_count": 0,
        "row_count": 0,
        "record_sha256": None,
        "first_nonzero": None,
    }


def _collect_face_partition(strata, banks, forward, inverse, witness_indexes):
    families = {family: _new_family() for family in FAMILY_ORDER}
    first_nonzero = None
    blocker = None

    for family in FAMILY_ORDER:
        digest_records = []
        pcache, vcache = {}, {}
        try:
            for pair_index, pair in enumerate(p.ADMITTED_PAIRS):
                for endpoint_index, endpoint in enumerate(pair):
                    bank = banks[endpoint]
                    witness_index = witness_indexes[endpoint]
                    for candidate_index, uid in enumerate(bank["candidates"]):
                        for side in SIDE_ORDER:
                            rows = _producer_face_rows(
                                family, side, pair, endpoint, uid, strata, bank,
                                witness_index, forward, inverse, pcache, vcache,
                            )
                            record = {
                                "pair_index": pair_index,
                                "endpoint_index": endpoint_index,
                                "candidate_index": candidate_index,
                                "pair": list(pair),
                                "endpoint": endpoint,
                                "candidate": p.unknown_json(uid),
                                "side": side,
                                "rows": rows,
                            }
                            digest_records.append(record)
                            families[family]["record_count"] += 1
                            families[family]["row_count"] += len(rows)
                            for row_index, row in enumerate(rows):
                                if row[-2] != 0:
                                    witness = {
                                        "family": family,
                                        "pair_index": pair_index,
                                        "endpoint_index": endpoint_index,
                                        "candidate_index": candidate_index,
                                        "pair": list(pair),
                                        "endpoint": endpoint,
                                        "candidate": p.unknown_json(uid),
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
            m.UnboundedSupportOverlap,
            n.UnboundedSupportOverlap,
            o.UnboundedSupportOverlap,
            p.UnboundedSupportOverlap,
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
        for family in FAMILY_ORDER:
            if families[family]["record_count"] != EXPECTED_FACE_RECORDS_PER_FAMILY:
                raise AssertionError(
                    f"Q {family} face coverage drift: "
                    f"{families[family]['record_count']} != {EXPECTED_FACE_RECORDS_PER_FAMILY}"
                )

    return {
        "families": families,
        "expected_face_records_per_family": EXPECTED_FACE_RECORDS_PER_FAMILY,
        "first_nonzero": first_nonzero,
        "characterized_blocker": blocker,
        "all_one_active_zero_sign_families_annihilated": complete,
        "coverage_complete": complete,
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

    partition = _collect_face_partition(
        strata, banks, forward, inverse, witness_indexes
    )
    if partition["characterized_blocker"] is not None:
        terminal = BLOCKER_TERMINAL
    elif partition["first_nonzero"] is not None:
        terminal = ESCAPE_TERMINAL
    else:
        terminal = CLOSURE_TERMINAL

    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "protected_base": PROTECTED_BASE,
        "source_locks": locks,
        "predecessor_terminals": {
            stage: spec["terminal"] for stage, spec in LOCKS.items()
        },
        "active_zero_face_partition": partition,
        "terminal": terminal,
        "full_coordinate_zero_laurent_algebra_corollary": None,
        "full_coordinate_zero_laurent_algebra_closed": False,
        "remaining_lower_dimensional_seam": (
            REMAINING_SEAM if terminal == CLOSURE_TERMINAL else None
        ),
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, separators=(",", ":")))
