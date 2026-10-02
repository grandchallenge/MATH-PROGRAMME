from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
import urllib.request
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRED_DIR = HERE.parent / "OZ_RT_BZ_T3_013_A"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"cannot load protected verifier dependency: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred13v = _load(PRED_DIR / "verifier.py", "oz_t3_013_a_verifier_for_014")
v = pred13v.v

ISSUE = 953
OPERATION = "OZ-RT-BZ-T3-014"
STAGE = "T3_014_SOURCE_DECLARED_RATIONAL_DELTA_LOCAL_JET_VIABILITY_GATE"
SOURCE_REPOSITORY = "rain-1/-odd-zeta-values-moremath"
SOURCE_COMMIT = "6cc0bf07137815ceeef0d9f340559f85352391e5"
SOURCE_DECLARATIONS = {
    "work/Z5T3_BRIDGE.md": "002c96d28123e5949c38656f26677ae5a723ee93",
    "work/Z5CF_LINALG.md": "637ecaa7f3ee941a87932de390eb7336d7fde677",
}
PREDECESSOR_BLOBS = {
    "CONTRACT.json": "846d3c399fd4d1e27cb28cbc71882d2f21f6e8e8",
    "producer.py": "8c1ae1285ca6c111366cca94dad8f7e0bd888bbb",
    "producer_impl.py.inc": "9ed7357c841ae88f0a22936a320f6f85f9202d6b",
    "verifier.py": "3d5a67013b6c43925403e476e501db91d4ca8e37",
}
PREDECESSOR_TERMINAL = "QROW_CERTIFICATE_WEIGHTED_STRICT_INTERIOR_SUBSYSTEM_INCONSISTENT"
SAMPLES = ((8, 1, 2), (9, 2, 1))


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=repr).encode("utf-8")
    ).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _file_blob(path: Path) -> str:
    return git_blob_sha1(path.read_bytes())


def _fetch_source(path: str, expected_blob: str) -> dict:
    url = f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{SOURCE_COMMIT}/{path}"
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    blob = git_blob_sha1(data)
    if blob != expected_blob:
        raise AssertionError(f"independent source declaration drift: {path}")
    return {"path": path, "git_blob_sha1": blob, "byte_count": len(data)}


def _point_shift(point: tuple[int, int, int], shift: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(a + b for a, b in zip(point, shift))


@lru_cache(maxsize=None)
def _shifted_poly(mon: tuple[str, ...], shift: tuple[int, int, int]):
    shifted = v.c.b.a.rc.p_const(1)
    for name in mon:
        shifted = v.c.b.a.rc.p_mul(shifted, v.c.b.primitive_shift_atom(name, shift))
    return shifted


def reconstruct() -> dict:
    for name, expected in PREDECESSOR_BLOBS.items():
        got = _file_blob(PRED_DIR / name)
        if got != expected:
            raise AssertionError(f"independent T3-013-A lock drift: {name}")
    predecessor_contract = json.loads((PRED_DIR / "CONTRACT.json").read_text())
    if predecessor_contract["authorized_terminals"]["negative"] != PREDECESSOR_TERMINAL:
        raise AssertionError("T3-013-A authorized negative terminal drift")

    declaration_locks = {
        path: _fetch_source(path, blob)
        for path, blob in SOURCE_DECLARATIONS.items()
    }

    v.c.assert_b_locks()
    v.c.b.assert_a_locks()
    v.c.b.a.assert_source_locks()
    v.c.b.a.validate_architecture()
    layer, predecessor = v.c.b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != v.c.b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 layer drift in T3-014 verifier")
    primitive = v.c.b.a.primitive_oriented_layer(layer)
    supports = {
        (channel, block): v.c.b.candidate_support(primitive, channel, block)
        for channel in v.c.b.a.CHANNEL_SCALARS
        for block in v.c.BLOCK_ORDER
    }

    nodes, qrow_source = pred13v._load_source()
    for n, k, l in SAMPLES:
        if not (0 <= k < n and 0 <= l <= n and k + 1 <= n):
            raise AssertionError("T3-014 witness left strict interior")
        if not v._qrow_check(nodes, n, k, l):
            raise AssertionError("independent current-source Q-row replay failed")

    predecessor_gate = pred13v.reconstruct()
    if predecessor_gate["consistent"]:
        raise AssertionError("independent T3-013-A negative predecessor did not replay")
    if (
        predecessor_gate["embedded_predecessor_coefficient_rank"],
        predecessor_gate["embedded_predecessor_augmented_rank"],
    ) != (84, 85):
        raise AssertionError("independent embedded T3-012-B obstruction drift")

    base_ids: list[tuple[str, str, tuple[str, ...]]] = []
    for channel in v.c.b.a.INDEPENDENT_CHANNELS:
        for scalar, mon in v.c.union_support_ids(supports, channel):
            base_ids.append((channel, scalar, mon))
    if len(base_ids) != 506:
        raise AssertionError("independent protected support cardinality drift")

    scalars = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
    target: dict = {}
    sample_multipliers: list[dict[str, Q]] = []
    for sample_index, (n, k, l) in enumerate(SAMPLES):
        multipliers = {scalar: v._mult(nodes, scalar, n, k, l) for scalar in scalars}
        sample_multipliers.append(multipliers)
        for mon, by_scalar in primitive.items():
            total = Q(0)
            for scalar, rat in by_scalar.items():
                if scalar in multipliers:
                    total += multipliers[scalar] * v.c.b.a.pcl.rat_eval_polefree(rat, n, k, l)
            if total:
                target[(sample_index, mon)] = total

    target_digest = sha(
        sorted((repr(key), value.numerator, value.denominator) for key, value in target.items())
    )

    unknown_ids: list[tuple[int, tuple[int, int, int]]] = []
    unknown_index: dict[tuple[int, tuple[int, int, int]], int] = {}
    orbit_by_channel: dict[str, set[tuple[int, int, int]]] = {}
    for base_index, (channel, _scalar, _mon) in enumerate(base_ids):
        shift = v.c.b.a.pcl.SHIFTS[channel]
        points = set(SAMPLES)
        points.update(_point_shift(point, shift) for point in SAMPLES)
        orbit_by_channel.setdefault(channel, set()).update(points)
        for point in sorted(points):
            key = (base_index, point)
            unknown_index[key] = len(unknown_ids)
            unknown_ids.append(key)

    columns: list[dict] = [{} for _ in unknown_ids]
    for sample_index in reversed(range(len(SAMPLES))):
        n, k, l = SAMPLES[sample_index]
        base_point = (n, k, l)
        multipliers = sample_multipliers[sample_index]
        for base_index in reversed(range(len(base_ids))):
            channel, scalar, support_mon = base_ids[base_index]
            mult = multipliers[scalar]
            if not mult:
                continue
            shift = v.c.b.a.pcl.SHIFTS[channel]
            shifted_point = _point_shift(base_point, shift)

            shifted_col = columns[unknown_index[(base_index, shifted_point)]]
            items = list(_shifted_poly(support_mon, shift).items())
            for shifted_mon, rat in reversed(items):
                value = mult * v.c.b.a.pcl.rat_eval_polefree(rat, n, k, l)
                if not value:
                    continue
                key = (sample_index, shifted_mon)
                shifted_col[key] = shifted_col.get(key, Q(0)) + value
                if not shifted_col[key]:
                    del shifted_col[key]

            base_col = columns[unknown_index[(base_index, base_point)]]
            base_key = (sample_index, support_mon)
            base_col[base_key] = base_col.get(base_key, Q(0)) - mult
            if not base_col[base_key]:
                del base_col[base_key]

    rank = v.rank_reverse(columns)
    augmented = v.rank_reverse(columns + [target])
    orbit_record = {
        channel: [list(point) for point in sorted(points)]
        for channel, points in sorted(orbit_by_channel.items())
    }
    return {
        "source_declaration_locks": declaration_locks,
        "source_qrow": qrow_source,
        "samples": [list(point) for point in SAMPLES],
        "sample_set_inherited_exactly_from_t3_012_b": True,
        "strict_interior_only": True,
        "coefficient_field": "Q(n,k,l)",
        "coefficient_shift_semantics": "Delta(q_i*M)=q_i(shifted_point)*M_shift-q_i(base_point)*M",
        "finite_value_assignment_realizable_by_polynomial_interpolation": True,
        "finite_value_jet_is_exact_restriction_not_relaxation": True,
        "rational_degree_cutoff": None,
        "denominator_cutoff": None,
        "protected_base_unknown_count": len(base_ids),
        "value_jet_unknown_count": len(columns),
        "nonzero_value_jet_column_count": sum(bool(column) for column in columns),
        "target_coordinate_count": len(target),
        "orbit_points_by_channel": orbit_record,
        "predecessor_t3_013_a_coefficient_rank": predecessor_gate["coefficient_rank"],
        "predecessor_t3_013_a_augmented_rank": predecessor_gate["augmented_rank"],
        "embedded_t3_012_b_coefficient_rank": predecessor_gate["embedded_predecessor_coefficient_rank"],
        "embedded_t3_012_b_augmented_rank": predecessor_gate["embedded_predecessor_augmented_rank"],
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": rank == augmented,
        "nullity": len(columns) - rank,
        "unknown_identity_sha256": sha(
            [[base_index, list(point)] for base_index, point in unknown_ids]
        ),
        "target_sha256": target_digest,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != ISSUE or result.get("operation") != OPERATION or result.get("stage") != STAGE:
        raise AssertionError("T3-014 result identity drift")
    if result.get("global_certificate_constructed") or result.get("residual_sum_zero_proved"):
        raise AssertionError("T3-014 local gate inflated to proof")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-014 local gate promoted claims")

    expected = result["gate"]
    got = reconstruct()
    for field in (
        "source_qrow", "samples", "sample_set_inherited_exactly_from_t3_012_b",
        "strict_interior_only", "coefficient_field", "coefficient_shift_semantics",
        "finite_value_assignment_realizable_by_polynomial_interpolation",
        "finite_value_jet_is_exact_restriction_not_relaxation", "rational_degree_cutoff",
        "denominator_cutoff", "protected_base_unknown_count", "value_jet_unknown_count",
        "nonzero_value_jet_column_count", "target_coordinate_count", "orbit_points_by_channel",
        "predecessor_t3_013_a_coefficient_rank", "predecessor_t3_013_a_augmented_rank",
        "embedded_t3_012_b_coefficient_rank", "embedded_t3_012_b_augmented_rank",
        "coefficient_rank", "augmented_rank", "consistent", "nullity",
        "unknown_identity_sha256", "target_sha256",
    ):
        if got[field] != expected[field]:
            raise AssertionError(f"T3-014 independent replay drift: {field}")
    if got["source_declaration_locks"] != result["source_declaration_locks"]:
        raise AssertionError("T3-014 independent source declaration lock mismatch")

    expected_terminal = (
        "RATIONAL_DELTA_LOCAL_JET_PREDECESSOR_OBSTRUCTION_ESCAPED__GLOBAL_RATIONAL_CERTIFICATE_REQUIRED"
        if got["consistent"]
        else "RATIONAL_DELTA_CLASS_REFUTED_AT_INHERITED_NECESSARY_SUBSYSTEM"
    )
    if result.get("terminal") != expected_terminal:
        raise AssertionError("T3-014 terminal does not match independently reconstructed gate")
    return {
        "terminal": expected_terminal,
        "independent_rational_value_jet_replay_complete": True,
        "producer_value_jet_matrix_imported_as_authority": False,
        "producer_rank_result_imported_as_authority": False,
        "gate": got,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
    }
