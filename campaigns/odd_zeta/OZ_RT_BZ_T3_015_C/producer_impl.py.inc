from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from sympy import Rational, cancel, symbols

HERE = Path(__file__).resolve().parent
PRED_B_DIR = HERE.parent / "OZ_RT_BZ_T3_015_B"
SCALAR_AUTHORITY_PATH = HERE.parent / "OZ_RT_BZ_T3_012_B" / "producer.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred_b = _load(PRED_B_DIR / "producer.py", "oz_t3_015_b_for_015_c")
scalar_authority = _load(SCALAR_AUTHORITY_PATH, "oz_t3_012_b_scalar_for_015_c")

ISSUE = 962
OPERATION = "OZ-RT-BZ-T3-015-C"
STAGE = "T3_015_C_COMPLETENESS_BACKED_DISCRETE_RESIDUE_OBSTRUCTION"
CLASS = "SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001"
PROTECTED_BASE = "__PENDING_T3_015_B_PROTECTED_MERGE__"
PREDECESSOR_EXACT_HEAD = "188569f80946968250b9d71d87b8f32e3ee9f565"
PREDECESSOR_TERMINAL = "GLOBAL_RATIONAL_DELTA_SOLVER_STRUCTURE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED"
PREDECESSOR_MODULE_SHA256 = "cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da"
TERMINAL = "GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED"
WITNESS = ("H_k_2", "H_nk_1", "H_nkl_1")
WITNESS_GENERATOR = 59
WITNESS_CHANNEL = "k1"
WITNESS_SCALAR = "SK"
WITNESS_SHIFT = (0, 1, 0)
PINV_TAG = 991337
PRED_B_BLOBS = {
    "CONTRACT.json": "9dc977a81d2572d735fad2be41c5332083abd813",
    "README.md": "c18b509d05d2b390d4b25cfab12bcb6e4585984b",
    "producer.py": "8c1ae1285ca6c111366cca94dad8f7e0bd888bbb",
    "producer_impl.py.inc": "13ff6bbb508f92dfafd586fa9c187fe446129575",
    "verifier.py": "8fb54f428c240fe8a41910c2fff0bb56f540c47b",
}
SCALAR_AUTHORITY_BLOB = "5682d61997499eccefddc15c6967dc907c091af4"
NONZERO_SAMPLE = (8, 1, 2)

n, k, l = symbols("n k l")


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _file_blob(path: Path) -> str:
    return _git_blob_sha1(path.read_bytes())


def _assert_predecessor_locks() -> dict:
    got = {}
    for name, expected in PRED_B_BLOBS.items():
        actual = _file_blob(PRED_B_DIR / name)
        if actual != expected:
            raise AssertionError(f"T3-015-B lock drift: {name}: {actual} != {expected}")
        got[name] = actual
    contract = json.loads((PRED_B_DIR / "CONTRACT.json").read_text(encoding="utf-8"))
    if contract["authorized_terminal"] != PREDECESSOR_TERMINAL:
        raise AssertionError("T3-015-B terminal contract drift")
    if contract["predecessor"]["module_sha256"] != PREDECESSOR_MODULE_SHA256:
        raise AssertionError("T3-015-B module contract drift")
    scalar_blob = _file_blob(SCALAR_AUTHORITY_PATH)
    if scalar_blob != SCALAR_AUTHORITY_BLOB:
        raise AssertionError("protected scalar authority drift")
    return {"t3_015_b": got, "scalar_authority": scalar_blob}


def _factor_expr(factor):
    v = tuple(map(int, factor))
    if len(v) == 5 and v[0] == PINV_TAG:
        _, an, ak, al, constant = v
        return an * n + ak * k + al * l + constant
    if len(v) == 4:
        an, ak, al, constant = v
        return an * n + ak * k + al * l + constant
    raise AssertionError(f"unexpected rational factor encoding: {v}")


def _rat_expr(rows):
    out = 0
    for numerator, denominator, factors in rows:
        term = Rational(int(numerator), int(denominator))
        for factor, exponent in factors:
            term *= _factor_expr(factor) ** int(exponent)
        out += term
    return cancel(out)


def _witness_from_module(module: dict) -> dict:
    incoming = []
    witness_generator = None
    for g in module["generators"]:
        if g["index"] == WITNESS_GENERATOR:
            witness_generator = g
        if tuple(g["base_term"]["monomial"]) == WITNESS:
            incoming.append({"generator_index": g["index"], "channel": g["channel"], "scalar": g["scalar"], "side": "base", "coefficient": str(_rat_expr(g["base_term"]["coefficient"]))})
        for term in g["shifted_terms"]:
            if tuple(term["monomial"]) == WITNESS:
                incoming.append({"generator_index": g["index"], "channel": g["channel"], "scalar": g["scalar"], "side": "shifted", "coefficient": str(_rat_expr(term["coefficient"]))})
    targets = [
        {"scalar": row["scalar"], "coefficient": str(_rat_expr(row["coefficient"]))}
        for row in module["target_records"]
        if tuple(row["monomial"]) == WITNESS
    ]
    expected_incoming = [
        {"generator_index": 59, "channel": "k1", "scalar": "SK", "side": "base", "coefficient": "-1"},
        {"generator_index": 59, "channel": "k1", "scalar": "SK", "side": "shifted", "coefficient": "1"},
    ]
    if incoming != expected_incoming:
        raise AssertionError(f"witness incoming incidence drift: {incoming}")
    if targets != [{"scalar": "SK", "coefficient": "1/(k + l + 1)"}]:
        raise AssertionError(f"witness target drift: {targets}")
    if witness_generator is None or tuple(witness_generator["support_monomial"]) != WITNESS:
        raise AssertionError("witness generator support drift")
    if tuple(witness_generator["shift"]) != WITNESS_SHIFT:
        raise AssertionError("witness generator shift drift")
    return {
        "monomial": list(WITNESS),
        "generator_index": 59,
        "channel": "k1",
        "scalar": "SK",
        "shift": [0, 1, 0],
        "full_incoming_incidence_checked": True,
        "incoming": incoming,
        "targets": targets,
        "forced_equation": "q_59(n,k+1,l)-q_59(n,k,l)=1/(k+l+1)",
    }


def _nonzero_scalar_witness() -> dict:
    nodes, source = scalar_authority.load_qrow_ast()
    if not scalar_authority.qrow_point_check(nodes, *NONZERO_SAMPLE):
        raise AssertionError("Q-row replay failed at SK nonzero sample")
    value = scalar_authority.scalar_multiplier(nodes, "SK", *NONZERO_SAMPLE)
    if not value:
        raise AssertionError("SK unexpectedly vanishes at exact nonzero witness")
    return {
        "scalar": "SK",
        "sample": list(NONZERO_SAMPLE),
        "numerator": value.numerator,
        "denominator": value.denominator,
        "qrow_source": source,
        "proves_nonzero_rational_function": True,
    }


def _discrete_residue_obstruction() -> dict:
    target = cancel(1 / (k + l + 1))
    if cancel((k + l + 1) * target) != 1:
        raise AssertionError("unexpected witness discrete residue")
    return {
        "base_field": "Q(n,l)",
        "rational_function_field": "Q(n,l)(k)",
        "shift": "tau(k)=k+1",
        "pole_orbit_representative": "k+l+1",
        "pole_order": 1,
        "target_discrete_residue": {"numerator": 1, "denominator": 1},
        "forward_difference_orbit_residue": {"numerator": 0, "denominator": 1},
        "partial_fraction_orbit_law": "for finite orbit coefficients c_j, Delta coefficient is c_{j-1}-c_j and the orbit sum telescopes to 0",
        "target_orbit_support": [0],
        "target_orbit_coefficients": [1],
        "target_orbit_sum": 1,
        "completeness_backed": True,
        "bounded_ansatz_used": False,
        "degree_cutoff": None,
        "denominator_cutoff": None,
    }


def build() -> dict:
    locks = _assert_predecessor_locks()
    predecessor, module = pred_b.build_with_module()
    if predecessor["terminal"] != PREDECESSOR_TERMINAL:
        raise AssertionError("T3-015-B predecessor terminal drift")
    if predecessor["predecessor_module_sha256"] != PREDECESSOR_MODULE_SHA256:
        raise AssertionError("T3-015-B predecessor module digest drift")
    if predecessor["structure"]["max_monomial_degree"] != 3 or not predecessor["structure"]["strict_degree_lowering"]:
        raise AssertionError("T3-015-B triangular structure drift")
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "protected_base": PROTECTED_BASE,
        "predecessor_exact_head": PREDECESSOR_EXACT_HEAD,
        "hypothesis_class": CLASS,
        "predecessor_locks": locks,
        "predecessor_module_sha256": PREDECESSOR_MODULE_SHA256,
        "witness": _witness_from_module(module),
        "scalar_nonzero_witness": _nonzero_scalar_witness(),
        "discrete_residue_obstruction": _discrete_residue_obstruction(),
        "class_nonexistence_proved": True,
        "terminal": TERMINAL,
        "global_certificate_constructed": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def compact_result(evidence: dict) -> dict:
    return {
        "module_sha256": evidence["predecessor_module_sha256"],
        "witness": evidence["witness"]["monomial"],
        "generator_index": evidence["witness"]["generator_index"],
        "forced_equation": evidence["witness"]["forced_equation"],
        "target_discrete_residue": evidence["discrete_residue_obstruction"]["target_discrete_residue"],
        "completeness_backed": evidence["discrete_residue_obstruction"]["completeness_backed"],
        "class_nonexistence_proved": evidence["class_nonexistence_proved"],
        "terminal": evidence["terminal"],
    }


if __name__ == "__main__":
    print("T3_015_C_RESULT " + json.dumps(compact_result(build()), sort_keys=True, separators=(",", ":")))
