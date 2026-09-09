from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
T3_010 = HERE.parent / "OZ_RT_BZ_T3_010"
if str(T3_010) not in sys.path:
    sys.path.insert(0, str(T3_010))

import t3_010_c as c  # noqa: E402

ISSUE = 927
STAGE = "T3_012_B_COUPLED_RECOMBINATION_VIABILITY_PROBE"
PROTECTED_BASE = "68826ff58629b59a09a97bbfcff9f560ac518d18"
C_BLOBS = {
    "t3_010_c.py": "c6359f01c12011a22194bfe7ff960aa3e30452d3",
    "T3_010_C_CONTRACT.json": "4f547f29d8bcb734f5e76816c5838d2b095a51b9",
}
EXPECTED_C_RANKS = {
    "n1": (116, 67, 68),
    "n2": (116, 67, 68),
    "n3": (116, 67, 68),
    "k1": (158, 110, 111),
}


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), default=repr).encode("utf-8")
    ).hexdigest()


def assert_source_locks() -> dict[str, str]:
    got: dict[str, str] = {}
    for name, want in C_BLOBS.items():
        value = c.b.a.git_blob_sha1(T3_010 / name)
        if value != want:
            raise AssertionError(f"T3-010-C source lock drift: {name}: {value} != {want}")
        got[name] = value
    c.assert_b_locks()
    c.b.assert_a_locks()
    c.b.a.assert_source_locks()
    c.b.a.validate_architecture()
    return got


def add_scaled(dst: dict, src: dict, factor: Q = Q(1)) -> None:
    if not factor:
        return
    for key, value in src.items():
        z = dst.get(key, Q(0)) + factor * value
        if z:
            dst[key] = z
        elif key in dst:
            del dst[key]


def exact_rank(vectors: list[dict], reverse: bool = False) -> int:
    basis: dict[object, dict] = {}
    keyfn = repr
    for source in vectors:
        v = {k: Q(x) for k, x in source.items() if x}
        while v:
            pivot = (max if reverse else min)(v, key=keyfn)
            if pivot in basis:
                factor = v[pivot]
                add_scaled(v, basis[pivot], -factor)
                continue
            scale = v[pivot]
            v = {k: x / scale for k, x in v.items() if x}
            basis[pivot] = v
            break
    return len(basis)


def _split_cell(cell_id: str) -> tuple[str, str, str]:
    parts = cell_id.split(":", 2)
    if len(parts) != 3:
        raise AssertionError(f"unexpected T3-010-C cell id {cell_id!r}")
    return parts[0], parts[1], parts[2]


def project_vector(vec: dict, mode: str) -> dict:
    out: dict = {}
    for (cell_id, coord), value in vec.items():
        channel, block, stratum = _split_cell(cell_id)
        scalar, mon, sig = coord
        if mode == "erase_partition_only":
            key = (scalar, mon, sig)
        elif mode == "erase_scalar_labels":
            key = (mon, sig)
        elif mode == "erase_rational_coefficient_labels":
            key = (mon,)
        elif mode == "retain_shell_erase_rational_labels":
            key = (stratum, mon)
        else:
            raise ValueError(mode)
        out[key] = out.get(key, Q(0)) + value
        if out[key] == 0:
            del out[key]
    return out


def reconstruct_c_systems():
    layer, predecessor = c.b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != c.b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 coefficient-layer digest drift in T3-012-B")
    primitive_full = c.b.a.primitive_oriented_layer(layer)
    strata = c.b.a.shell_strata()
    specialized = {
        st["id"]: c.b.a.primitive_oriented_layer(
            c.b.a.specialize_layer(layer, st["k_offset"], st["l_offset"])
        )
        for st in strata
    }
    supports = {
        (channel, block): c.b.candidate_support(primitive_full, channel, block)
        for channel in c.b.a.CHANNEL_SCALARS
        for block in c.BLOCK_ORDER
    }
    systems = {}
    for channel in c.b.a.INDEPENDENT_CHANNELS:
        rec, ids, cols, target = c.build_channel_system(
            channel, primitive_full, strata, specialized, supports
        )
        expected = EXPECTED_C_RANKS[channel]
        got = (rec["unknown_count"], rec["coefficient_rank"], rec["augmented_rank"])
        if got != expected or rec["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"protected T3-010-C rank drift in {channel}: {got} != {expected}")
        systems[channel] = (rec, ids, cols, target)
    return systems


def analyze_projection(systems: dict, mode: str) -> dict:
    columns: list[dict] = []
    column_ids: list[tuple] = []
    target: dict = {}
    for channel in c.b.a.INDEPENDENT_CHANNELS:
        _rec, ids, cols, local_target = systems[channel]
        add_scaled(target, project_vector(local_target, mode))
        for uid, col in zip(ids, cols):
            columns.append(project_vector(col, mode))
            column_ids.append((channel, uid[0], uid[1]))
    rank = exact_rank(columns)
    reverse_rank = exact_rank(columns, reverse=True)
    augmented = exact_rank(columns + [target])
    reverse_augmented = exact_rank(columns + [target], reverse=True)
    if rank != reverse_rank or augmented != reverse_augmented:
        raise AssertionError(f"projection rank ordering drift in {mode}")
    return {
        "mode": mode,
        "unknown_count": len(columns),
        "nonzero_column_count": sum(bool(x) for x in columns),
        "target_coordinate_count": len(target),
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": rank == augmented,
        "nullity": len(columns) - rank,
        "column_identity_sha256": sha([[ch, scalar, list(mon)] for ch, scalar, mon in column_ids]),
        "target_sha256": sha(sorted((repr(k), v.numerator, v.denominator) for k, v in target.items())),
    }


def build() -> dict:
    locks = assert_source_locks()
    systems = reconstruct_c_systems()
    modes = [
        "erase_partition_only",
        "erase_scalar_labels",
        "retain_shell_erase_rational_labels",
        "erase_rational_coefficient_labels",
    ]
    probes = [analyze_projection(systems, mode) for mode in modes]
    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "stage": STAGE,
        "protected_base": PROTECTED_BASE,
        "source_locks": locks,
        "protected_c_channel_ranks": {
            channel: {
                "unknown_count": EXPECTED_C_RANKS[channel][0],
                "coefficient_rank": EXPECTED_C_RANKS[channel][1],
                "augmented_rank": EXPECTED_C_RANKS[channel][2],
            }
            for channel in c.b.a.INDEPENDENT_CHANNELS
        },
        "probe_semantics": {
            "status": "DISCOVERY_ONLY",
            "purpose": "Measure how far the protected C inconsistency survives increasingly permissive linear projections before paying the cost of exact regularized scalar-functional reconstruction.",
            "not_a_functional_recombination_certificate": True,
            "finite_sampling_used": False,
            "exact_Q_linear_algebra": True,
        },
        "probes": probes,
        "actual_source_locked_recombination_map_reconstructed": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": "COUPLED_RECOMBINATION_PROJECTION_VIABILITY_PROBE_COMPLETE__EXACT_FUNCTIONAL_MAP_PENDING",
    }
