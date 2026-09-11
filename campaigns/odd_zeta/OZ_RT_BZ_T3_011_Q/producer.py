from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
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


def _require_parent(result: dict, stage: str, terminal: str) -> None:
    if result.get("terminal") != terminal:
        raise AssertionError(f"protected {stage} did not replay its closure terminal")
    if result.get("tested_record_count") != result.get("possible_record_count"):
        raise AssertionError(f"protected {stage} replay is incomplete")
    if result.get("semantic_functional_ambiguity") is not None:
        raise AssertionError(f"protected {stage} replay has semantic ambiguity")
    if result.get("characterized_blocker") is not None:
        raise AssertionError(f"protected {stage} replay has characterized blocker")
    if result.get("first_cokernel_breaking_direction") is not None:
        raise AssertionError(f"protected {stage} replay has a non-boundary escape")


def _scan_rows(records: list[dict], field: str, family: str, source: str, side: str | None = None):
    row_count = 0
    first = None
    for index, record in enumerate(records):
        rows = record.get(field, [])
        row_count += len(rows)
        for row_index, row in enumerate(rows):
            if row[-2] != 0:
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
                if first is None or json.dumps(witness, sort_keys=True) < json.dumps(first, sort_keys=True):
                    first = witness
    return {"record_count": len(records), "row_count": row_count, "first_nonzero": first}


def _combine_first(*items):
    present = [x for x in items if x is not None]
    return min(present, key=lambda x: json.dumps(x, sort_keys=True)) if present else None


def _summarize(mr: dict, nr: dict, orr: dict, pr: dict) -> dict:
    m_records = mr["tested_records"]
    n_records = nr["tested_records"]
    o_records = orr["tested_records"]
    p_records = pr["tested_records"]

    if not all(r.get("reciprocal_degree_zero_semantics_exactly_match_K") for r in m_records):
        raise AssertionError("M/K active-zero boundary semantics drift")
    if not all(r.get("reciprocal_degree_zero_semantics_exactly_match_M") for r in n_records):
        raise AssertionError("N/M active-zero boundary semantics drift")
    if not all(r.get("reciprocal_active_degree_zero_semantics_exactly_match_L") for r in o_records):
        raise AssertionError("O/L active-zero boundary semantics drift")
    if not all(r.get("positive_active_degree_zero_anchor_kind") == "DIRECT_RESPONSE_ONLY_NOT_T3_011_I" for r in o_records):
        raise AssertionError("O direct-response anchor kind drift")
    if not all(r.get("active_reciprocal_degree_zero_anchor_kind") == "DIRECT_RESPONSE_ONLY_NO_PREDECESSOR_CLASS_PROMOTION" for r in p_records):
        raise AssertionError("P direct-response anchor kind drift")

    plus_plus = _scan_rows(m_records, "protected_K_boundary_rows", "++", "M")
    minus_plus_left = _scan_rows(n_records, "protected_M_left_boundary_rows", "-+", "N", "left")
    minus_plus_right = _scan_rows(n_records, "protected_M_right_boundary_rows", "-+", "N", "right")
    plus_minus = _scan_rows(o_records, "reciprocal_active_degree_zero_boundary_rows", "+-", "O")
    minus_minus_o = _scan_rows(o_records, "positive_active_degree_zero_direct_response_rows", "--", "O")
    minus_minus_p_left = _scan_rows(p_records, "left_reciprocal_degree_zero_direct_response_rows", "--", "P", "left")
    minus_minus_p_right = _scan_rows(p_records, "right_reciprocal_degree_zero_direct_response_rows", "--", "P", "right")

    first = _combine_first(
        plus_plus["first_nonzero"],
        minus_plus_left["first_nonzero"], minus_plus_right["first_nonzero"],
        plus_minus["first_nonzero"],
        minus_minus_o["first_nonzero"],
        minus_minus_p_left["first_nonzero"], minus_minus_p_right["first_nonzero"],
    )
    return {
        "families": {
            "++": plus_plus,
            "-+": {
                "left": minus_plus_left,
                "right": minus_plus_right,
                "first_nonzero": _combine_first(minus_plus_left["first_nonzero"], minus_plus_right["first_nonzero"]),
            },
            "+-": plus_minus,
            "--": {
                "O_positive_zero": minus_minus_o,
                "P_left_zero": minus_minus_p_left,
                "P_right_zero": minus_minus_p_right,
                "first_nonzero": _combine_first(minus_minus_o["first_nonzero"], minus_minus_p_left["first_nonzero"], minus_minus_p_right["first_nonzero"]),
            },
        },
        "first_nonzero": first,
        "all_one_active_zero_sign_families_annihilated": first is None,
    }


def build() -> dict:
    validate_scope()
    locks = assert_locks()
    mr, nr, orr, pr = m.build(), n.build(), o.build(), p.build()
    _require_parent(mr, "M", m.CLOSURE_TERMINAL)
    _require_parent(nr, "N", n.CLOSURE_TERMINAL)
    _require_parent(orr, "O", o.CLOSURE_TERMINAL)
    _require_parent(pr, "P", p.CLOSURE_TERMINAL)

    summary = _summarize(mr, nr, orr, pr)
    terminal = ESCAPE_TERMINAL if summary["first_nonzero"] is not None else CLOSURE_TERMINAL
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "protected_base": PROTECTED_BASE,
        "source_locks": locks,
        "predecessor_terminals": {
            "M": mr["terminal"], "N": nr["terminal"], "O": orr["terminal"], "P": pr["terminal"],
        },
        "active_zero_face_partition": summary,
        "terminal": terminal,
        "full_coordinate_zero_laurent_algebra_corollary": None,
        "full_coordinate_zero_laurent_algebra_closed": False,
        "remaining_lower_dimensional_seam": REMAINING_SEAM if terminal == CLOSURE_TERMINAL else None,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True, separators=(",", ":")))
