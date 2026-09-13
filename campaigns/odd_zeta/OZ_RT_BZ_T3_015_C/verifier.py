from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

from sympy import Rational, cancel, symbols

HERE = Path(__file__).resolve().parent
PRED_A_DIR = HERE.parent / "OZ_RT_BZ_T3_015_A"
PRED_B_DIR = HERE.parent / "OZ_RT_BZ_T3_015_B"
SCALAR_VERIFIER_PATH = HERE.parent / "OZ_RT_BZ_T3_012_B" / "verifier.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected verifier predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred_a_v = _load(PRED_A_DIR / "verifier.py", "oz_t3_015_a_verifier_for_015_c")
scalar_v = _load(SCALAR_VERIFIER_PATH, "oz_t3_012_b_verifier_for_015_c")

ISSUE = 962
OPERATION = "OZ-RT-BZ-T3-015-C"
STAGE = "T3_015_C_COMPLETENESS_BACKED_DISCRETE_RESIDUE_OBSTRUCTION"
CLASS = "SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001"
PROTECTED_BASE = "__PENDING_T3_015_B_PROTECTED_MERGE__"
PREDECESSOR_EXACT_HEAD = "188569f80946968250b9d71d87b8f32e3ee9f565"
PREDECESSOR_MODULE_SHA256 = "cdabf6d7873f3aa8e9d53b39fd7b15341dbee58ce9684911d015aee9aaae04da"
PREDECESSOR_TERMINAL = "GLOBAL_RATIONAL_DELTA_SOLVER_STRUCTURE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED"
TERMINAL = "GLOBAL_RATIONAL_DELTA_CLASS_OBSTRUCTED__COMPLETENESS_BACKED"
WITNESS = ("H_k_2", "H_nk_1", "H_nkl_1")
WITNESS_GENERATOR = 59
WITNESS_SHIFT = (0, 1, 0)
PINV_TAG = 991337
PRED_B_BLOBS = {
    "CONTRACT.json": "9dc977a81d2572d735fad2be41c5332083abd813",
    "README.md": "c18b509d05d2b390d4b25cfab12bcb6e4585984b",
    "producer.py": "8c1ae1285ca6c111366cca94dad8f7e0bd888bbb",
    "producer_impl.py.inc": "13ff6bbb508f92dfafd586fa9c187fe446129575",
    "verifier.py": "8fb54f428c240fe8a41910c2fff0bb56f540c47b",
}
SCALAR_VERIFIER_BLOB = "89d22466513957050e0d3440c801052a6531323d"

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
            raise AssertionError(f"independent T3-015-B lock drift: {name}")
        got[name] = actual
    contract = json.loads((PRED_B_DIR / "CONTRACT.json").read_text(encoding="utf-8"))
    if contract["authorized_terminal"] != PREDECESSOR_TERMINAL:
        raise AssertionError("independent T3-015-B terminal contract drift")
    if contract["predecessor"]["module_sha256"] != PREDECESSOR_MODULE_SHA256:
        raise AssertionError("independent T3-015-B module contract drift")
    scalar_blob = _file_blob(SCALAR_VERIFIER_PATH)
    if scalar_blob != SCALAR_VERIFIER_BLOB:
        raise AssertionError("independent scalar verifier authority drift")
    return {"t3_015_b": got, "scalar_verifier": scalar_blob}


def _factor_expr(factor):
    v = [int(x) for x in factor]
    if len(v) == 5:
        if v[0] != PINV_TAG:
            raise AssertionError(f"independent tagged factor drift: {v}")
        _, an, ak, al, constant = v
    elif len(v) == 4:
        an, ak, al, constant = v
    else:
        raise AssertionError(f"independent rational factor shape drift: {v}")
    return an * n + ak * k + al * l + constant


def _rat_expr(rows):
    terms = []
    for numerator, denominator, factors in rows:
        value = Rational(int(numerator), int(denominator))
        for encoded, exponent in factors:
            value *= _factor_expr(encoded) ** int(exponent)
        terms.append(value)
    return cancel(sum(terms, Rational(0)))


def _independent_witness(module: dict) -> dict:
    incoming = []
    selected = None
    for g in reversed(module["generators"]):
        if g["index"] == WITNESS_GENERATOR:
            selected = g
        local = []
        for term in reversed(g["shifted_terms"]):
            if tuple(term["monomial"]) == WITNESS:
                local.append({"generator_index": g["index"], "channel": g["channel"], "scalar": g["scalar"], "side": "shifted", "coefficient": str(_rat_expr(term["coefficient"]))})
        if tuple(g["base_term"]["monomial"]) == WITNESS:
            local.append({"generator_index": g["index"], "channel": g["channel"], "scalar": g["scalar"], "side": "base", "coefficient": str(_rat_expr(g["base_term"]["coefficient"]))})
        incoming.extend(local)
    incoming.sort(key=lambda row: (row["generator_index"], 0 if row["side"] == "base" else 1))
    targets = [
        {"scalar": row["scalar"], "coefficient": str(_rat_expr(row["coefficient"]))}
        for row in reversed(module["target_records"])
        if tuple(row["monomial"]) == WITNESS
    ]
    targets.sort(key=lambda row: (row["scalar"], row["coefficient"]))
    if selected is None or tuple(selected["support_monomial"]) != WITNESS:
        raise AssertionError("independent witness support drift")
    if tuple(selected["shift"]) != WITNESS_SHIFT or selected["channel"] != "k1" or selected["scalar"] != "SK":
        raise AssertionError("independent witness channel/scalar drift")
    expected = [
        {"generator_index": 59, "channel": "k1", "scalar": "SK", "side": "base", "coefficient": "-1"},
        {"generator_index": 59, "channel": "k1", "scalar": "SK", "side": "shifted", "coefficient": "1"},
    ]
    if incoming != expected:
        raise AssertionError(f"independent incoming incidence drift: {incoming}")
    if targets != [{"scalar": "SK", "coefficient": "1/(k + l + 1)"}]:
        raise AssertionError(f"independent witness target drift: {targets}")
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


def _independent_scalar_nonzero(producer_record: dict) -> dict:
    nodes, source = scalar_v._load_source()
    sample = tuple(producer_record["sample"])
    if sample != (8, 1, 2) or not scalar_v._qrow_check(nodes, *sample):
        raise AssertionError("independent producer-sample Q-row replay failed")
    value = scalar_v._mult(nodes, "SK", *sample)
    if not value:
        raise AssertionError("independent SK nonzero sample vanished")
    if producer_record["numerator"] != value.numerator or producer_record["denominator"] != value.denominator:
        raise AssertionError("producer/verifier SK value mismatch")
    second = (9, 2, 1)
    if not scalar_v._qrow_check(nodes, *second):
        raise AssertionError("independent second Q-row replay failed")
    second_value = scalar_v._mult(nodes, "SK", *second)
    if not second_value:
        raise AssertionError("SK vanished at independent second sample")
    return {
        "producer_sample_replayed": True,
        "second_nonzero_sample": list(second),
        "second_numerator": second_value.numerator,
        "second_denominator": second_value.denominator,
        "qrow_source": source,
        "proves_nonzero_rational_function": True,
    }


def _independent_discrete_residue(witness: dict) -> dict:
    if witness["forced_equation"] != "q_59(n,k+1,l)-q_59(n,k,l)=1/(k+l+1)":
        raise AssertionError("forced equation drift")
    target = cancel(1 / (k + l + 1))
    if cancel((k + l + 1) * target) != 1:
        raise AssertionError("independent target pole coefficient drift")
    target_orbit_coefficients = [1]
    if sum(target_orbit_coefficients) == 0:
        raise AssertionError("independent discrete residue unexpectedly vanished")
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
        "target_orbit_coefficients": target_orbit_coefficients,
        "target_orbit_sum": 1,
        "completeness_backed": True,
        "bounded_ansatz_used": False,
        "degree_cutoff": None,
        "denominator_cutoff": None,
    }


def verify(evidence: dict) -> dict:
    locks = _assert_predecessor_locks()
    reconstructed = pred_a_v.reconstruct_module()
    if reconstructed["module_sha256"] != PREDECESSOR_MODULE_SHA256:
        raise AssertionError("independent T3-015-A module digest drift")
    if evidence["predecessor_locks"]["t3_015_b"] != locks["t3_015_b"]:
        raise AssertionError("producer/verifier T3-015-B lock mismatch")
    if evidence["predecessor_module_sha256"] != reconstructed["module_sha256"]:
        raise AssertionError("producer predecessor module digest mismatch")
    witness = _independent_witness(reconstructed["module"])
    if evidence["witness"] != witness:
        raise AssertionError("producer/verifier witness mismatch")
    scalar_replay = _independent_scalar_nonzero(evidence["scalar_nonzero_witness"])
    obstruction = _independent_discrete_residue(witness)
    if evidence["discrete_residue_obstruction"] != obstruction:
        raise AssertionError("producer/verifier discrete-residue obstruction mismatch")
    if evidence["issue"] != ISSUE or evidence["operation"] != OPERATION or evidence["stage"] != STAGE:
        raise AssertionError("T3-015-C identity drift")
    if evidence["protected_base"] != PROTECTED_BASE or evidence["predecessor_exact_head"] != PREDECESSOR_EXACT_HEAD:
        raise AssertionError("T3-015-C predecessor binding drift")
    if evidence["hypothesis_class"] != CLASS or not evidence["class_nonexistence_proved"]:
        raise AssertionError("T3-015-C class conclusion drift")
    if evidence["terminal"] != TERMINAL:
        raise AssertionError("terminal drift")
    if evidence["global_certificate_constructed"] or evidence["residual_sum_zero_proved"]:
        raise AssertionError("claim firewall violated")
    if evidence["proof_effect"] != "NONE" or evidence["promotion_effect"] != "NONE" or evidence["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("claim/status drift")
    return {
        "independent_module_reconstruction_complete": True,
        "producer_module_imported_as_authority": False,
        "full_incoming_incidence_replayed": True,
        "independent_scalar_nonzero_replay": scalar_replay,
        "discrete_residue_theorem_applied": True,
        "complete_rational_nonexistence_verified": True,
        "module_sha256": reconstructed["module_sha256"],
        "terminal": TERMINAL,
    }
