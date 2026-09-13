from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRED_DIR = HERE.parent / "OZ_RT_BZ_T3_014"
SCALAR_AUTHORITY_PATH = HERE.parent / "OZ_RT_BZ_T3_012_B" / "producer.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected verifier predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred14v = _load(PRED_DIR / "verifier.py", "oz_t3_014_verifier_for_015a")
v = pred14v.v

ISSUE = 956
OPERATION = "OZ-RT-BZ-T3-015-A"
CLASS = "SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001"
PROTECTED_BASE = "9c570e92b9bb0f80183b495715751340e35f0150"
PREDECESSOR_TERMINAL = (
    "RATIONAL_DELTA_LOCAL_JET_PREDECESSOR_OBSTRUCTION_ESCAPED__GLOBAL_RATIONAL_CERTIFICATE_REQUIRED"
)
TERMINAL = "GLOBAL_RATIONAL_DELTA_DIFFERENCE_MODULE_EXTRACTED__COMPLETE_RATIONAL_SOLVER_REQUIRED"

SOURCE_REPOSITORY = "rain-1/-odd-zeta-values-moremath"
SOURCE_COMMIT = "6cc0bf07137815ceeef0d9f340559f85352391e5"
SOURCE_DECLARATIONS = {
    "work/Z5T3_BRIDGE.md": "002c96d28123e5949c38656f26677ae5a723ee93",
    "work/Z5CF_LINALG.md": "637ecaa7f3ee941a87932de390eb7336d7fde677",
}
QROW_BLOB = "61f12f412726887f506e1d423b7ee183a22116e5"
SCALAR_AUTHORITY_BLOB = "5682d61997499eccefddc15c6967dc907c091af4"
PREDECESSOR_BLOBS = {
    "CONTRACT.json": "ebb244851395b7d72f9932cc9d1d8190faf305f1",
    "README.md": "7612cc5c993e80e0197b1fc7b61a4c809f217922",
    "producer.py": "8c1ae1285ca6c111366cca94dad8f7e0bd888bbb",
    "producer_impl.py.inc": "b7746d8f6bb03333a384b695e51f3a98ab328d0c",
    "verifier.py": "ef88efd1277d69175deb6b20ed73e8fa069746ba",
}
SCALARS = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
EXPECTED_CHANNEL_COUNTS = {"n1": 116, "n2": 116, "n3": 116, "k1": 158}
SCALAR_DEFINITIONS = {
    "TN1": "recurrence_coeff(1,n)*T(n+1,k,l)/T(n,k,l)",
    "TN2": "recurrence_coeff(2,n)*T(n+2,k,l)/T(n,k,l)",
    "TN3": "recurrence_coeff(3,n)*T(n+3,k,l)/T(n,k,l)",
    "SK": "2*(-k_shift_ratio(n,k,l)*rho_sym(n,k+1,l))",
    "AK": "2*(-k_shift_ratio(n,k,l)*(dkl_rho_sym-dk_rho_sym*Ll-dl_rho_sym*Lk))(n,k+1,l)",
    "LKK": "2*k_shift_ratio(n,k,l)*dk_rho_sym(n,k+1,l)",
    "LLK": "2*k_shift_ratio(n,k,l)*dl_rho_sym(n,k+1,l)",
}


def _sha(obj: object) -> str:
    raw = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _file_blob(path: Path) -> str:
    return _git_blob_sha1(path.read_bytes())


def _fetch_source(path: str, expected_blob: str) -> dict:
    url = f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{SOURCE_COMMIT}/{path}"
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    got = _git_blob_sha1(data)
    if got != expected_blob:
        raise AssertionError(f"independent source lock drift: {path}")
    return {"path": path, "git_blob_sha1": got, "byte_count": len(data)}


def _assert_locks() -> dict:
    predecessor = {}
    for name, expected in PREDECESSOR_BLOBS.items():
        got = _file_blob(PRED_DIR / name)
        if got != expected:
            raise AssertionError(f"independent T3-014 lock drift: {name}")
        predecessor[name] = got
    contract = json.loads((PRED_DIR / "CONTRACT.json").read_text(encoding="utf-8"))
    if contract["hypothesis_class"]["id"] != CLASS:
        raise AssertionError("independent T3-014 class drift")
    if contract["authorized_terminals"]["escape"] != PREDECESSOR_TERMINAL:
        raise AssertionError("independent T3-014 terminal drift")

    scalar_authority = _file_blob(SCALAR_AUTHORITY_PATH)
    if scalar_authority != SCALAR_AUTHORITY_BLOB:
        raise AssertionError("independent protected scalar-definition authority drift")

    declarations = {
        path: _fetch_source(path, blob)
        for path, blob in SOURCE_DECLARATIONS.items()
    }
    nodes, qrow = pred14v.pred13v._load_source()
    if qrow["git_blob_sha1"] != QROW_BLOB:
        raise AssertionError("independent Q-row source object drift")
    if len(nodes) != 2:
        raise AssertionError("independent Q-row source arity drift")
    return {
        "predecessor": predecessor,
        "declarations": declarations,
        "qrow": qrow,
        "scalar_authority": {
            "path": "campaigns/odd_zeta/OZ_RT_BZ_T3_012_B/producer.py",
            "git_blob_sha1": scalar_authority,
        },
    }


def _serialize_poly(poly, rc):
    return [
        {"monomial": list(mon), "coefficient": rc.rat_json(rat)}
        for mon, rat in sorted(poly.items(), key=lambda item: repr(item[0]))
    ]


def _independent_shifted_poly(mon, shift):
    rc = v.c.b.a.rc
    out = rc.p_const(1)
    for atom in reversed(mon):
        out = rc.p_mul(out, v.c.b.primitive_shift_atom(atom, shift))
    return out


def reconstruct_module() -> dict:
    locks = _assert_locks()
    v.c.assert_b_locks()
    v.c.b.assert_a_locks()
    v.c.b.a.assert_source_locks()
    v.c.b.a.validate_architecture()

    layer, predecessor = v.c.b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != v.c.b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 layer drift in T3-015-A verifier")
    primitive = v.c.b.a.primitive_oriented_layer(layer)
    supports = {
        (channel, block): v.c.b.candidate_support(primitive, channel, block)
        for channel in v.c.b.a.CHANNEL_SCALARS
        for block in v.c.BLOCK_ORDER
    }

    ids = []
    for channel in reversed(v.c.b.a.INDEPENDENT_CHANNELS):
        rows = list(v.c.union_support_ids(supports, channel))
        for scalar, mon in reversed(rows):
            ids.append((channel, scalar, mon))
    ids = sorted(ids, key=repr)
    if len(ids) != 506:
        raise AssertionError("independent protected generator count drift")
    channel_counts = {}
    for channel, _scalar, _mon in ids:
        channel_counts[channel] = channel_counts.get(channel, 0) + 1
    if channel_counts != EXPECTED_CHANNEL_COUNTS:
        raise AssertionError(f"independent protected channel counts drift: {channel_counts}")

    rc = v.c.b.a.rc
    shifts = v.c.b.a.pcl.SHIFTS
    minus_one = rc.rat_json(rc.r_const(-1))
    generators = []
    coordinate_monomials = set()
    for index, (channel, scalar, mon) in enumerate(ids):
        shift = tuple(shifts[channel])
        shifted = _independent_shifted_poly(mon, shift)
        coordinate_monomials.add(tuple(mon))
        coordinate_monomials.update(shifted)
        generators.append(
            {
                "index": index,
                "channel": channel,
                "scalar": scalar,
                "support_monomial": list(mon),
                "shift": list(shift),
                "base_term": {
                    "monomial": list(mon),
                    "coefficient": minus_one,
                },
                "shifted_terms": _serialize_poly(shifted, rc),
            }
        )

    target = []
    for mon, by_scalar in sorted(primitive.items(), key=lambda item: repr(item[0])):
        for scalar in reversed(SCALARS):
            rat = by_scalar.get(scalar)
            if rat:
                target.append(
                    {
                        "scalar": scalar,
                        "monomial": list(mon),
                        "coefficient": rc.rat_json(rat),
                    }
                )
    target = sorted(
        target,
        key=lambda row: (repr(tuple(row["monomial"])), SCALARS.index(row["scalar"])),
    )
    coordinate_monomials.update(tuple(row["monomial"]) for row in target)

    module = {
        "schema_version": "1.0.0",
        "coefficient_field": "Q(n,k,l)",
        "hypothesis_class": CLASS,
        "operator_semantics": "mu_s(n,k,l)*(q_i(shift)*M_shift-q_i(n,k,l)*M)",
        "finite_sample_grid_used": False,
        "rational_degree_cutoff": None,
        "denominator_cutoff": None,
        "global_shift_module_only": True,
        "generator_count": len(generators),
        "channel_counts": channel_counts,
        "scalar_namespace": list(SCALARS),
        "scalar_definitions": SCALAR_DEFINITIONS,
        "coordinate_monomial_count": len(coordinate_monomials),
        "coordinate_monomials": [
            list(mon) for mon in sorted(coordinate_monomials, key=repr)
        ],
        "target_record_count": len(target),
        "target_records": target,
        "generators": generators,
    }
    return {"locks": locks, "module": module, "module_sha256": _sha(module)}


def verify(evidence: dict) -> dict:
    reconstructed = reconstruct_module()
    if evidence["source_locks"] != reconstructed["locks"]:
        raise AssertionError("source/predecessor lock replay mismatch")
    if evidence["module"] != reconstructed["module"]:
        raise AssertionError("independent global rational Delta module mismatch")
    if evidence["module_sha256"] != reconstructed["module_sha256"]:
        raise AssertionError("independent global module digest mismatch")
    if evidence["terminal"] != TERMINAL:
        raise AssertionError("T3-015-A terminal drift")
    if evidence["protected_base"] != PROTECTED_BASE:
        raise AssertionError("T3-015-A protected-base drift")
    if evidence["global_certificate_constructed"] or evidence["residual_sum_zero_proved"]:
        raise AssertionError("claim firewall violated")
    if evidence["proof_effect"] != "NONE" or evidence["promotion_effect"] != "NONE":
        raise AssertionError("claim effect drift")
    if evidence["t3_status"] != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status drift")
    return {
        "independent_global_module_replay_complete": True,
        "producer_module_imported_as_authority": False,
        "module_sha256": reconstructed["module_sha256"],
        "generator_count": reconstructed["module"]["generator_count"],
        "channel_counts": reconstructed["module"]["channel_counts"],
        "coordinate_monomial_count": reconstructed["module"]["coordinate_monomial_count"],
        "target_record_count": reconstructed["module"]["target_record_count"],
        "terminal": TERMINAL,
    }
