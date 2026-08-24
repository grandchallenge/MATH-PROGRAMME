#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_010_b as b  # noqa: E402

OPERATION = "SYMMETRY_REDUCED_CHANNEL_HARMONIC_BLOCK_WITH_SHELL_STRATA_001"
STAGE = "T3_010_C_BOUNDED_EXACT_SHARED_COEFFICIENT_SOLUTION_EXTRACTION_GATE"
B_HEAD = "3a6cfba4d8fc5f44d0b9f17e9521e9df43e83fc8"
B_BLOBS = {
    "t3_010_b.py": "11ce437f2a26d73d3362df3e923f6cf9c4cf91f9",
    "T3_010_B_CONTRACT.json": "d6eae2adbd34d4d3d61e985d42d6e3d01ffcefd0",
    "verify_t3_010_b.py": "89e4100e7750ccc8b86c8ddb2e28b97a8e15b7cd",
}
BLOCK_ORDER = b.BLOCK_ORDER

Unknown = tuple[str, tuple[str, ...]]
GlobalCoord = tuple[str, b.Coord]
GlobalVector = dict[GlobalCoord, Q]


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def assert_b_locks() -> dict[str, str]:
    got: dict[str, str] = {}
    for name, want in B_BLOBS.items():
        value = b.a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"T3-010-B source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_010_B_CONTRACT.json").read_text())
    if contract["stage"] != b.STAGE:
        raise AssertionError("T3-010-B contract stage drift")
    if contract["coefficient_envelope"]["degree"] != 0:
        raise AssertionError("T3-010-B coefficient envelope drift")
    if contract["positive_classification_boundary"]["solution_extraction"]:
        raise AssertionError("T3-010-B extraction boundary drift")
    return got


def ukey(uid: Unknown) -> str:
    return repr(uid)


def gkey(coord: GlobalCoord) -> str:
    return repr(coord)


def unknown_json(uid: Unknown) -> list:
    scalar, mon = uid
    return [scalar, list(mon)]


def global_vector_digest(vec: GlobalVector) -> str:
    rows = []
    for (cell_id, coord) in sorted(vec, key=gkey):
        q = vec[(cell_id, coord)]
        rows.append([cell_id, b._coord_json(coord), q.numerator, q.denominator])
    return sha(rows)


def global_column_digest(ids: list[Unknown], cols: list[GlobalVector]) -> str:
    return sha([
        [unknown_json(uid), global_vector_digest(col)]
        for uid, col in zip(ids, cols)
    ])


def add_scaled(dst: dict, src: dict, factor: Q) -> None:
    if not factor:
        return
    for key, value in src.items():
        z = dst.get(key, Q(0)) + factor * value
        if z:
            dst[key] = z
        elif key in dst:
            del dst[key]


def apply_solution(
    ids: list[Unknown],
    cols: list[dict],
    solution: dict[Unknown, Q],
) -> dict:
    out: dict = {}
    for uid, col in zip(ids, cols):
        add_scaled(out, col, solution.get(uid, Q(0)))
    return out


def exact_particular_solution(
    ids: list[Unknown],
    cols: list[GlobalVector],
    target: GlobalVector,
) -> dict[Unknown, Q] | None:
    """Solve A x = target exactly over Q, setting nonpivot/free columns to zero.

    The elimination is deterministic in declared unknown order and smallest
    global-coordinate pivot order. Basis representations are retained so the
    target reduction yields an exact coefficient vector.
    """
    basis: dict[GlobalCoord, tuple[GlobalVector, dict[Unknown, Q]]] = {}
    for uid, source in zip(ids, cols):
        vec: GlobalVector = {k: Q(v) for k, v in source.items() if v}
        rep: dict[Unknown, Q] = {uid: Q(1)}
        while vec:
            pivot = min(vec, key=gkey)
            if pivot in basis:
                base_vec, base_rep = basis[pivot]
                factor = vec[pivot]
                add_scaled(vec, base_vec, -factor)
                add_scaled(rep, base_rep, -factor)
                continue
            scale = vec[pivot]
            vec = {k: v / scale for k, v in vec.items() if v}
            rep = {k: v / scale for k, v in rep.items() if v}
            basis[pivot] = (vec, rep)
            break

    rem: GlobalVector = {k: Q(v) for k, v in target.items() if v}
    sol: dict[Unknown, Q] = {}
    while rem:
        pivot = min(rem, key=gkey)
        if pivot not in basis:
            return None
        base_vec, base_rep = basis[pivot]
        factor = rem[pivot]
        add_scaled(rem, base_vec, -factor)
        add_scaled(sol, base_rep, factor)
    return {uid: sol.get(uid, Q(0)) for uid in ids}


def solution_rows(ids: list[Unknown], solution: dict[Unknown, Q]) -> list[list]:
    rows = []
    for uid in ids:
        q = solution.get(uid, Q(0))
        rows.append([uid[0], list(uid[1]), q.numerator, q.denominator])
    return rows


def parse_solution_rows(rows: list[list]) -> dict[Unknown, Q]:
    out: dict[Unknown, Q] = {}
    for scalar, mon, num, den in rows:
        out[(scalar, tuple(mon))] = Q(int(num), int(den))
    return out


def union_support_ids(
    supports: dict[tuple[str, str], dict[str, list[tuple[str, ...]]]],
    channel: str,
) -> list[Unknown]:
    found: set[Unknown] = set()
    for block in BLOCK_ORDER:
        for scalar, mons in supports[(channel, block)].items():
            for mon in mons:
                found.add((scalar, mon))
    return sorted(found, key=ukey)


def build_channel_system(
    channel: str,
    primitive_full: b.a.pcl.Layer,
    strata: list[dict],
    specialized: dict[str, b.a.pcl.Layer],
    supports: dict[tuple[str, str], dict[str, list[tuple[str, ...]]]],
) -> tuple[dict, list[Unknown], list[GlobalVector], GlobalVector]:
    ids = union_support_ids(supports, channel)
    pos = {uid: i for i, uid in enumerate(ids)}
    cols: list[GlobalVector] = [{} for _ in ids]
    target: GlobalVector = {}
    active_records: list[dict] = []
    structural_zero = 0
    local_hist: dict[str, int] = {}

    for st in strata:
        primitive = specialized[st["id"]]
        for block in BLOCK_ORDER:
            rec, local_target, local_cols, local_ids = b.analyze_cell(
                primitive, supports[(channel, block)], channel, block, st
            )
            cls = rec["classification"]
            local_hist[cls] = local_hist.get(cls, 0) + 1
            if cls == "STRUCTURAL_ZERO":
                structural_zero += 1
                continue
            active_records.append({
                "id": rec["id"],
                "block": block,
                "stratum": st["id"],
                "local_classification": cls,
                "local_rank": rec["coefficient_rank"],
                "local_augmented_rank": rec["augmented_rank"],
            })
            for coord, q in local_target.items():
                target[(rec["id"], coord)] = q
            for uid, local_col in zip(local_ids, local_cols):
                if uid not in pos:
                    raise AssertionError(f"global support omission {channel}:{uid}")
                out = cols[pos[uid]]
                for coord, q in local_col.items():
                    gc = (rec["id"], coord)
                    z = out.get(gc, Q(0)) + q
                    if z:
                        out[gc] = z
                    elif gc in out:
                        del out[gc]

    rank, _ = b.rank_sparse(cols)
    augmented_rank, _ = b.rank_sparse(cols + [target])
    classification = b.classify(rank, augmented_rank, len(ids))
    solution = exact_particular_solution(ids, cols, target)
    consistent = classification.startswith("CONSISTENT_")
    if consistent != (solution is not None):
        raise AssertionError(f"rank/solver consistency drift in {channel}")

    substitution_checks = 0
    rows: list[list] = []
    solution_digest = None
    if solution is not None:
        got = apply_solution(ids, cols, solution)
        if got != target:
            raise AssertionError(f"global exact substitution drift in {channel}")
        substitution_checks = len(active_records)
        rows = solution_rows(ids, solution)
        solution_digest = sha(rows)

    record = {
        "channel": channel,
        "unknown_count": len(ids),
        "active_cell_count": len(active_records),
        "structural_zero_cell_count": structural_zero,
        "local_classification_histogram": dict(sorted(local_hist.items())),
        "coefficient_rank": rank,
        "augmented_rank": augmented_rank,
        "nullity": len(ids) - rank,
        "classification": classification,
        "global_target_coordinate_count": len(target),
        "global_matrix_coordinate_count": len(set(target).union(*(set(x) for x in cols))),
        "zero_global_columns": sum(not col for col in cols),
        "unknown_support_sha256": sha([unknown_json(x) for x in ids]),
        "global_coefficient_matrix_sha256": global_column_digest(ids, cols),
        "global_target_sha256": global_vector_digest(target),
        "exact_solution_extracted": solution is not None,
        "exact_substitution_checks": substitution_checks,
        "canonical_solution_sha256": solution_digest,
        "solution_coefficients": rows,
        "active_cells": active_records,
    }
    return record, ids, cols, target


def mirror_unknown_k_to_l(uid: Unknown) -> Unknown:
    scalar, mon = uid
    if scalar not in b.a.MIRROR_SCALAR:
        raise AssertionError(f"unexpected k1 scalar in C mirror: {scalar}")
    return (
        b.a.MIRROR_SCALAR[scalar],
        tuple(sorted(b.mirror_letter(x) for x in mon)),
    )


def build() -> dict:
    b_locks = assert_b_locks()
    b.assert_a_locks()
    b.a.assert_source_locks()
    b.a.validate_architecture()
    layer, predecessor = b.a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != b.a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 coefficient-layer digest drift in C")

    primitive_full = b.a.primitive_oriented_layer(layer)
    strata = b.a.shell_strata()
    specialized = {
        st["id"]: b.a.primitive_oriented_layer(
            b.a.specialize_layer(layer, st["k_offset"], st["l_offset"])
        )
        for st in strata
    }
    supports = {
        (channel, block): b.candidate_support(primitive_full, channel, block)
        for channel in b.a.CHANNEL_SCALARS
        for block in BLOCK_ORDER
    }

    systems: list[dict] = []
    internals: dict[str, tuple[list[Unknown], list[GlobalVector], GlobalVector]] = {}
    for channel in b.a.INDEPENDENT_CHANNELS:
        rec, ids, cols, target = build_channel_system(
            channel, primitive_full, strata, specialized, supports
        )
        systems.append(rec)
        internals[channel] = (ids, cols, target)

    # l1 remains derived from k1, but C also reconstructs the complete l1 global
    # system and requires mirrored k1 coefficients to satisfy it exactly.
    lrec, lids, lcols, ltarget = build_channel_system(
        "l1", primitive_full, strata, specialized, supports
    )
    krec = next(x for x in systems if x["channel"] == "k1")
    if (
        lrec["coefficient_rank"],
        lrec["augmented_rank"],
        lrec["classification"],
        lrec["active_cell_count"],
    ) != (
        krec["coefficient_rank"],
        krec["augmented_rank"],
        krec["classification"],
        krec["active_cell_count"],
    ):
        raise AssertionError("T3-010-C k1/l1 global rank mirror drift")

    mirror_solution_check = False
    if krec["exact_solution_extracted"]:
        ksol = parse_solution_rows(krec["solution_coefficients"])
        lsol = {mirror_unknown_k_to_l(uid): q for uid, q in ksol.items()}
        if set(lsol) != set(lids):
            raise AssertionError("T3-010-C mirrored l1 unknown support drift")
        if apply_solution(lids, lcols, lsol) != ltarget:
            raise AssertionError("T3-010-C mirrored l1 exact substitution drift")
        mirror_solution_check = True
    elif lrec["exact_solution_extracted"]:
        raise AssertionError("T3-010-C l1/k1 consistency mirror drift")

    all_consistent = all(x["classification"].startswith("CONSISTENT_") for x in systems)
    extracted_channels = sum(x["exact_solution_extracted"] for x in systems)
    terminal = (
        "T3_010_C_COMPLETE__FULL_CORRECTION_LAYER_RECOMBINATION_PENDING"
        if all_consistent
        else "BOUNDED_SUPPORT_LOCKED_DEGREE0_CORRECTION_CLASS_GLOBALLY_INCOMPATIBLE"
    )

    return {
        "schema_version": "1.0.0",
        "issue": 403,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "EXACT_SHARED_COEFFICIENT_COMPATIBILITY_AND_EXTRACTION_GATE_COMPLETE",
        "t3_010_b_checkpoint": {
            "validated_head": B_HEAD,
            "source_blobs": b_locks,
            "required_status": "EXACT_CORRECTION_FLUX_COEFFICIENT_MATRIX_RANK_CONSISTENCY_GATE_COMPLETE",
        },
        "correction_class": {
            "id": "SUPPORT_LOCKED_ORIENTED_ONE_BODY_DEGREE0_WEIGHT_CORRECTION_001",
            "coefficient_field": "Q",
            "coefficient_degree": 0,
            "shared_unknown": "one exact rational coefficient per scalar-family x support-locked oriented primitive correction weight, shared across every shell stratum and every overlapping harmonic-block projection in its channel",
            "adaptive_basis_growth": False,
            "new_harmonic_monomials_admitted": False,
            "generic_198_raw_jet_reopened": False,
        },
        "global_system_semantics": {
            "independent_channels": list(b.a.INDEPENDENT_CHANNELS),
            "mirror_derived_channel": "l1",
            "row_key": "active local cell id x exact B coefficient coordinate",
            "reason": "cell identity is retained when stacking equations, so no cancellation across shell/block projections can manufacture compatibility",
            "exact_field": "Q",
            "free_variable_policy": "deterministic particular solution with nonpivot/free columns set to zero",
        },
        "channel_systems": systems,
        "globally_consistent_independent_channel_count": sum(
            x["classification"].startswith("CONSISTENT_") for x in systems
        ),
        "globally_inconsistent_independent_channel_count": sum(
            x["classification"] == "EXACTLY_INCONSISTENT" for x in systems
        ),
        "exact_solution_extracted_channel_count": extracted_channels,
        "all_independent_channels_globally_consistent": all_consistent,
        "mirrored_l1_system": {
            "classification": lrec["classification"],
            "coefficient_rank": lrec["coefficient_rank"],
            "augmented_rank": lrec["augmented_rank"],
            "unknown_count": lrec["unknown_count"],
            "active_cell_count": lrec["active_cell_count"],
            "global_coefficient_matrix_sha256": lrec["global_coefficient_matrix_sha256"],
            "global_target_sha256": lrec["global_target_sha256"],
            "mirrored_k1_solution_exactly_satisfies_l1": mirror_solution_check,
        },
        "local_consistency_promoted_to_certificate": False,
        "full_correction_layer_recombined": False,
        "full_symbolic_flux_identity_substituted": False,
        "finite_boundary_assembly_completed": False,
        "final_n_holonomic_search_run": False,
        "finite_sampling_used_as_sum_proof": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
        "terminal": terminal,
    }


def main() -> int:
    print(json.dumps(build(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
