from __future__ import annotations

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
        raise AssertionError(f"cannot load protected predecessor: {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


pred13 = _load(PRED_DIR / "producer.py", "oz_t3_013_a_for_014")

ISSUE = 953
OPERATION = "OZ-RT-BZ-T3-014"
STAGE = "T3_014_SOURCE_DECLARED_RATIONAL_DELTA_LOCAL_JET_VIABILITY_GATE"
CLASS = "SOURCE_DECLARED_RATIONAL_DELTA_COEFFICIENT_CLASS_001"
PROTECTED_BASE = "ced68d9f56d8757554ef1b06360808d1a13b9982"
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
ESCAPE_TERMINAL = "RATIONAL_DELTA_LOCAL_JET_PREDECESSOR_OBSTRUCTION_ESCAPED__GLOBAL_RATIONAL_CERTIFICATE_REQUIRED"
NEGATIVE_TERMINAL = "RATIONAL_DELTA_CLASS_REFUTED_AT_INHERITED_NECESSARY_SUBSYSTEM"
SAMPLES = tuple(pred13.SAMPLES)


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=repr).encode("utf-8")
    ).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def _fetch_source(path: str, expected_blob: str) -> dict:
    url = f"https://raw.githubusercontent.com/{SOURCE_REPOSITORY}/{SOURCE_COMMIT}/{path}"
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    blob = git_blob_sha1(data)
    if blob != expected_blob:
        raise AssertionError(f"source declaration drift: {path}: {blob} != {expected_blob}")
    return {"path": path, "git_blob_sha1": blob, "byte_count": len(data)}


def assert_predecessor_locks() -> dict[str, str]:
    got: dict[str, str] = {}
    for name, want in PREDECESSOR_BLOBS.items():
        value = pred13.pred.c.b.a.git_blob_sha1(PRED_DIR / name)
        if value != want:
            raise AssertionError(f"T3-013-A lock drift: {name}: {value} != {want}")
        got[name] = value
    pred13.assert_predecessor_locks()
    return got


def _point_shift(point: tuple[int, int, int], shift: tuple[int, int, int]) -> tuple[int, int, int]:
    return tuple(a + b for a, b in zip(point, shift))


@lru_cache(maxsize=None)
def _shifted_monomial_poly(mon: tuple[str, ...], shift: tuple[int, int, int]):
    shifted = pred13.pred.c.b.a.rc.p_const(1)
    for name in mon:
        shifted = pred13.pred.c.b.a.rc.p_mul(
            shifted, pred13.pred.c.b.primitive_shift_atom(name, shift)
        )
    return shifted


def _assemble_target(nodes, primitive_full) -> tuple[dict, list[dict[str, Q]]]:
    target: dict = {}
    sample_multipliers: list[dict[str, Q]] = []
    scalars = ("TN1", "TN2", "TN3", "SK", "AK", "LKK", "LLK")
    for sample_index, (n, k, l) in enumerate(SAMPLES):
        multipliers = {
            scalar: pred13.pred.scalar_multiplier(nodes, scalar, n, k, l)
            for scalar in scalars
        }
        sample_multipliers.append(multipliers)
        for mon, by_scalar in primitive_full.items():
            total = Q(0)
            for scalar, rat in by_scalar.items():
                if scalar in multipliers:
                    total += multipliers[scalar] * pred13.pred._eval_rat(rat, n, k, l)
            if total:
                target[(sample_index, mon)] = total
    return target, sample_multipliers


def rational_value_jet_gate(primitive_full, supports: dict) -> dict:
    nodes, qrow_source = pred13.load_current_qrow_ast()
    for point in SAMPLES:
        n, k, l = point
        if not (0 <= k < n and 0 <= l <= n and k + 1 <= n):
            raise AssertionError(f"functional witness not strictly interior: {point}")
        if not pred13.pred.qrow_point_check(nodes, n, k, l):
            raise AssertionError(f"current-source Q-row point replay failed: {point}")

    predecessor_gate = pred13.weighted_source_functional_gate(primitive_full, supports)
    if predecessor_gate["terminal"] != PREDECESSOR_TERMINAL or predecessor_gate["consistent"]:
        raise AssertionError("T3-013-A negative predecessor did not replay exactly")
    if (
        predecessor_gate["embedded_predecessor_coefficient_rank"],
        predecessor_gate["embedded_predecessor_augmented_rank"],
    ) != (84, 85):
        raise AssertionError("embedded T3-012-B constant obstruction drift")

    base_ids = pred13._base_ids(primitive_full, supports)
    target, sample_multipliers = _assemble_target(nodes, primitive_full)
    target_digest = sha(
        sorted((repr(key), value.numerator, value.denominator) for key, value in target.items())
    )
    if target_digest != predecessor_gate["target_sha256"]:
        raise AssertionError("protected target drift between T3-013-A and T3-014")

    unknown_ids: list[tuple[int, tuple[int, int, int]]] = []
    unknown_index: dict[tuple[int, tuple[int, int, int]], int] = {}
    orbit_by_channel: dict[str, set[tuple[int, int, int]]] = {}
    for base_index, (channel, _scalar, _mon) in enumerate(base_ids):
        shift = pred13.pred.c.b.a.pcl.SHIFTS[channel]
        points = set(SAMPLES)
        points.update(_point_shift(point, shift) for point in SAMPLES)
        orbit_by_channel.setdefault(channel, set()).update(points)
        for point in sorted(points):
            key = (base_index, point)
            unknown_index[key] = len(unknown_ids)
            unknown_ids.append(key)

    columns: list[dict] = [{} for _ in unknown_ids]
    for sample_index, (n, k, l) in enumerate(SAMPLES):
        base_point = (n, k, l)
        multipliers = sample_multipliers[sample_index]
        for base_index, (channel, scalar, support_mon) in enumerate(base_ids):
            mult = multipliers[scalar]
            if not mult:
                continue
            shift = pred13.pred.c.b.a.pcl.SHIFTS[channel]
            shifted_point = _point_shift(base_point, shift)

            base_col = columns[unknown_index[(base_index, base_point)]]
            base_key = (sample_index, support_mon)
            base_col[base_key] = base_col.get(base_key, Q(0)) - mult
            if not base_col[base_key]:
                del base_col[base_key]

            shifted_col = columns[unknown_index[(base_index, shifted_point)]]
            for shifted_mon, rat in _shifted_monomial_poly(support_mon, shift).items():
                value = mult * pred13.pred._eval_rat(rat, n, k, l)
                if not value:
                    continue
                key = (sample_index, shifted_mon)
                shifted_col[key] = shifted_col.get(key, Q(0)) + value
                if not shifted_col[key]:
                    del shifted_col[key]

    rank = pred13.pred.exact_rank(columns)
    rank_reverse = pred13.pred.exact_rank(columns, reverse=True)
    augmented = pred13.pred.exact_rank(columns + [target])
    augmented_reverse = pred13.pred.exact_rank(columns + [target], reverse=True)
    if rank != rank_reverse or augmented != augmented_reverse:
        raise AssertionError("rational-value-jet exact rank ordering drift")

    consistent = rank == augmented
    orbit_record = {
        channel: [list(point) for point in sorted(points)]
        for channel, points in sorted(orbit_by_channel.items())
    }
    return {
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
        "predecessor_t3_013_a_terminal": predecessor_gate["terminal"],
        "predecessor_t3_013_a_coefficient_rank": predecessor_gate["coefficient_rank"],
        "predecessor_t3_013_a_augmented_rank": predecessor_gate["augmented_rank"],
        "embedded_t3_012_b_coefficient_rank": predecessor_gate["embedded_predecessor_coefficient_rank"],
        "embedded_t3_012_b_augmented_rank": predecessor_gate["embedded_predecessor_augmented_rank"],
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": consistent,
        "nullity": len(columns) - rank,
        "unknown_identity_sha256": sha(
            [[base_index, list(point)] for base_index, point in unknown_ids]
        ),
        "target_sha256": target_digest,
        "terminal": ESCAPE_TERMINAL if consistent else NEGATIVE_TERMINAL,
        "interpretation": (
            "Exact inherited necessary-subsystem gate for the source-declared rational Delta coefficient class. "
            "Consistency proves only escape from the inherited obstruction; it does not construct global rational "
            "coefficients, a global Delta certificate, or the T3 identity."
        ),
    }


def build() -> dict:
    predecessor_locks = assert_predecessor_locks()
    declaration_locks = {
        path: _fetch_source(path, blob)
        for path, blob in SOURCE_DECLARATIONS.items()
    }
    _systems, primitive_full, supports = pred13.pred.reconstruct_c_systems()
    gate = rational_value_jet_gate(primitive_full, supports)
    return {
        "schema_version": "1.1.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "hypothesis_class": CLASS,
        "protected_base": PROTECTED_BASE,
        "source_declaration_locks": declaration_locks,
        "predecessor": {
            "operation": "OZ-RT-BZ-T3-013-A",
            "required_terminal": PREDECESSOR_TERMINAL,
            "source_locks": predecessor_locks,
        },
        "non_reducibility": {
            "t3_011_r": "coefficient functions range over Q(n,k,l), beyond the frozen coordinate-zero Laurent monomial response algebra",
            "t3_012_b": "coefficient law changes from constants to Q(n,k,l) with target/support/harmonics/scalars fixed",
            "t3_013_a": "strictly widens fixed span_Q{1,rho,sigma} to the source-declared rational function field Q(n,k,l)",
            "source_motivated": True,
            "cutoff_escalation": False,
        },
        "gate": gate,
        "terminal": gate["terminal"],
        "global_certificate_constructed": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }
