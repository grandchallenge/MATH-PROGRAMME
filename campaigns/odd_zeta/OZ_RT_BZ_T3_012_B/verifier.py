from __future__ import annotations

import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
T3_010 = HERE.parent / "OZ_RT_BZ_T3_010"
if str(T3_010) not in sys.path:
    sys.path.insert(0, str(T3_010))

import t3_010_c as c  # noqa: E402

MODES = (
    "erase_partition_only",
    "erase_scalar_labels",
    "retain_shell_erase_rational_labels",
    "erase_rational_coefficient_labels",
)


def add(dst: dict, key: object, value: Q) -> None:
    z = dst.get(key, Q(0)) + value
    if z:
        dst[key] = z
    elif key in dst:
        del dst[key]


def projected_key(mode: str, stratum: str, coord) -> tuple:
    scalar, mon, sig = coord
    if mode == "erase_partition_only":
        return scalar, mon, sig
    if mode == "erase_scalar_labels":
        return mon, sig
    if mode == "retain_shell_erase_rational_labels":
        return stratum, mon
    if mode == "erase_rational_coefficient_labels":
        return (mon,)
    raise ValueError(mode)


def rank_reverse(vectors: list[dict]) -> int:
    basis: dict[object, dict] = {}
    for source in reversed(vectors):
        v = {k: Q(x) for k, x in source.items() if x}
        while v:
            pivot = max(v, key=repr)
            if pivot in basis:
                factor = v[pivot]
                for key, coeff in basis[pivot].items():
                    add(v, key, -factor * coeff)
                continue
            scale = v[pivot]
            basis[pivot] = {k: x / scale for k, x in v.items() if x}
            break
    return len(basis)


def reconstruct_projection(mode: str) -> dict:
    c.assert_b_locks()
    c.b.assert_a_locks()
    c.b.a.assert_source_locks()
    c.b.a.validate_architecture()
    layer, predecessor = c.b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != c.b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 layer drift in T3-012-B verifier")
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

    target: dict = {}
    columns: list[dict] = []
    channel_offsets: dict[str, int] = {}
    channel_ids: dict[str, list] = {}
    for channel in c.b.a.INDEPENDENT_CHANNELS:
        ids = c.union_support_ids(supports, channel)
        channel_offsets[channel] = len(columns)
        channel_ids[channel] = ids
        columns.extend({} for _ in ids)

    for st in reversed(strata):
        primitive = specialized[st["id"]]
        for channel in reversed(c.b.a.INDEPENDENT_CHANNELS):
            ids = channel_ids[channel]
            pos = {uid: channel_offsets[channel] + i for i, uid in enumerate(ids)}
            for block in reversed(c.BLOCK_ORDER):
                rec, local_target, local_cols, local_ids = c.b.analyze_cell(
                    primitive, supports[(channel, block)], channel, block, st
                )
                if rec["classification"] == "STRUCTURAL_ZERO":
                    continue
                for coord, value in local_target.items():
                    add(target, projected_key(mode, st["id"], coord), value)
                for uid, local_col in zip(local_ids, local_cols):
                    out = columns[pos[uid]]
                    for coord, value in local_col.items():
                        add(out, projected_key(mode, st["id"], coord), value)

    rank = rank_reverse(columns)
    augmented = rank_reverse(columns + [target])
    return {
        "mode": mode,
        "unknown_count": len(columns),
        "nonzero_column_count": sum(bool(x) for x in columns),
        "target_coordinate_count": len(target),
        "coefficient_rank": rank,
        "augmented_rank": augmented,
        "consistent": rank == augmented,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != 927 or result.get("stage") != "T3_012_B_COUPLED_RECOMBINATION_VIABILITY_PROBE":
        raise AssertionError("T3-012-B result identity drift")
    if result.get("actual_source_locked_recombination_map_reconstructed"):
        raise AssertionError("projection probe inflated to exact functional map")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-012-B projection probe promoted")
    expected = {row["mode"]: row for row in result["probes"]}
    replay = []
    for mode in MODES:
        got = reconstruct_projection(mode)
        row = expected[mode]
        for field in (
            "unknown_count", "nonzero_column_count", "target_coordinate_count",
            "coefficient_rank", "augmented_rank", "consistent",
        ):
            if got[field] != row[field]:
                raise AssertionError(f"T3-012-B independent replay drift {mode}:{field}")
        replay.append(got)
    return {
        "terminal": result["terminal"],
        "independent_projection_replay_complete": True,
        "producer_projected_matrices_imported_as_authority": False,
        "probes": replay,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
    }
