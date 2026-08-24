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

import verify_t3_010_b as vb  # noqa: E402

STAGE = "T3_010_C_BOUNDED_EXACT_SHARED_COEFFICIENT_SOLUTION_EXTRACTION_GATE"
B_HEAD = "3a6cfba4d8fc5f44d0b9f17e9521e9df43e83fc8"
B_BLOBS = {
    "t3_010_b.py": "11ce437f2a26d73d3362df3e923f6cf9c4cf91f9",
    "T3_010_B_CONTRACT.json": "d6eae2adbd34d4d3d61e985d42d6e3d01ffcefd0",
    "verify_t3_010_b.py": "89e4100e7750ccc8b86c8ddb2e28b97a8e15b7cd",
}
BLOCK_ORDER = vb.BLOCK_ORDER
a = vb.a

Unknown = tuple[str, tuple[str, ...]]
GlobalCoord = tuple[str, vb.Coord]
GlobalVector = dict[GlobalCoord, Q]


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def ukey(uid: Unknown) -> str:
    return repr(uid)


def gkey(coord: GlobalCoord) -> str:
    return repr(coord)


def unknown_json(uid: Unknown) -> list:
    return [uid[0], list(uid[1])]


def global_vector_digest(vec: GlobalVector) -> str:
    rows = []
    for (cell_id, coord) in sorted(vec, key=gkey):
        q = vec[(cell_id, coord)]
        rows.append([cell_id, vb.cjson(coord), q.numerator, q.denominator])
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


def apply_solution(ids: list[Unknown], cols: list[dict], solution: dict[Unknown, Q]) -> dict:
    out: dict = {}
    for uid, col in zip(ids, cols):
        add_scaled(out, col, solution.get(uid, Q(0)))
    return out


def parse_solution(rows: list[list]) -> dict[Unknown, Q]:
    out: dict[Unknown, Q] = {}
    for scalar, mon, num, den in rows:
        uid = (scalar, tuple(mon))
        if uid in out:
            raise AssertionError(f"duplicate C solution coefficient {uid}")
        out[uid] = Q(int(num), int(den))
    return out


def support_union(
    supports: dict[tuple[str, str], dict[str, list[tuple[str, ...]]]],
    channel: str,
) -> list[Unknown]:
    found: set[Unknown] = set()
    for block in reversed(BLOCK_ORDER):
        for scalar, mons in supports[(channel, block)].items():
            for mon in reversed(mons):
                found.add((scalar, mon))
    return sorted(found, key=ukey)


def reconstruct_channel(
    channel: str,
    strata: list[dict],
    specialized: dict[str, a.pcl.Layer],
    supports: dict[tuple[str, str], dict[str, list[tuple[str, ...]]]],
) -> tuple[dict, list[Unknown], list[GlobalVector], GlobalVector]:
    ids = support_union(supports, channel)
    pos = {uid: i for i, uid in enumerate(ids)}
    cols: list[GlobalVector] = [{} for _ in ids]
    target: GlobalVector = {}
    active = structural_zero = 0
    hist: dict[str, int] = {}

    for st in reversed(strata):
        primitive = specialized[st["id"]]
        for block in reversed(BLOCK_ORDER):
            rec, local_target, local_cols, local_ids = vb.cell(
                primitive, supports[(channel, block)], channel, block, st
            )
            cls = rec["classification"]
            hist[cls] = hist.get(cls, 0) + 1
            cell_id = f"{channel}:{block}:{st['id']}"
            if cls == "STRUCTURAL_ZERO":
                structural_zero += 1
                continue
            active += 1
            for coord, q in local_target.items():
                target[(cell_id, coord)] = q
            for uid, local_col in zip(local_ids, local_cols):
                if uid not in pos:
                    raise AssertionError(f"independent C support omission {channel}:{uid}")
                out = cols[pos[uid]]
                for coord, q in local_col.items():
                    gc = (cell_id, coord)
                    z = out.get(gc, Q(0)) + q
                    if z:
                        out[gc] = z
                    elif gc in out:
                        del out[gc]

    rank = vb.rank_reverse(cols)
    augmented_rank = vb.rank_reverse(cols + [target])
    classification = vb.classification(rank, augmented_rank, len(ids))
    record = {
        "channel": channel,
        "unknown_count": len(ids),
        "active_cell_count": active,
        "structural_zero_cell_count": structural_zero,
        "local_classification_histogram": dict(sorted(hist.items())),
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
    }
    return record, ids, cols, target


def mirror_unknown_k_to_l(uid: Unknown) -> Unknown:
    scalar, mon = uid
    if scalar not in a.MIRROR_SCALAR:
        raise AssertionError(f"unexpected k1 scalar in C verifier mirror: {scalar}")
    return (
        a.MIRROR_SCALAR[scalar],
        tuple(sorted(vb.mletter(x) for x in mon)),
    )


def verify(result: dict) -> dict:
    if result.get("stage") != STAGE:
        raise AssertionError("T3-010-C stage drift")
    if result.get("t3_010_b_checkpoint", {}).get("validated_head") != B_HEAD:
        raise AssertionError("T3-010-B checkpoint drift in C")
    for name, want in B_BLOBS.items():
        if a.git_blob_sha1(HERE / name) != want:
            raise AssertionError(f"T3-010-B blob drift in C verifier: {name}")
    contract = json.loads((HERE / "T3_010_C_CONTRACT.json").read_text())
    if contract["stage"] != STAGE:
        raise AssertionError("T3-010-C contract stage drift")
    if contract["shared_coefficient_system"]["field"] != "Q":
        raise AssertionError("T3-010-C exact field drift")
    if contract["bounded_correction_class"]["coefficient_degree"] != 0:
        raise AssertionError("T3-010-C bounded degree drift")

    a.assert_source_locks()
    a.validate_architecture()
    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("predecessor digest drift in C verifier")
    primitive_full = a.primitive_oriented_layer(layer)
    strata = a.shell_strata()
    specialized = {
        st["id"]: a.primitive_oriented_layer(
            a.specialize_layer(layer, st["k_offset"], st["l_offset"])
        )
        for st in strata
    }
    supports = {
        (channel, block): vb.support(primitive_full, channel, block)
        for channel in a.CHANNEL_SCALARS
        for block in BLOCK_ORDER
    }

    expected = {x["channel"]: x for x in result.get("channel_systems", [])}
    if set(expected) != set(a.INDEPENDENT_CHANNELS):
        raise AssertionError("C independent-channel result cardinality drift")

    consistent_count = inconsistent_count = extracted_count = 0
    substitution_checks = 0

    for channel in a.INDEPENDENT_CHANNELS:
        got, ids, cols, target = reconstruct_channel(channel, strata, specialized, supports)
        rec = expected[channel]
        for key in (
            "unknown_count", "active_cell_count", "structural_zero_cell_count",
            "local_classification_histogram", "coefficient_rank", "augmented_rank",
            "nullity", "classification", "global_target_coordinate_count",
            "global_matrix_coordinate_count", "zero_global_columns",
            "unknown_support_sha256", "global_coefficient_matrix_sha256",
            "global_target_sha256",
        ):
            if rec.get(key) != got[key]:
                raise AssertionError(f"independent C reconstruction drift {channel}:{key}")

        consistent = got["classification"].startswith("CONSISTENT_")
        if consistent:
            consistent_count += 1
        elif got["classification"] == "EXACTLY_INCONSISTENT":
            inconsistent_count += 1
        else:
            raise AssertionError(f"unexpected C global classification {got['classification']}")

        extracted = bool(rec.get("exact_solution_extracted"))
        if extracted != consistent:
            raise AssertionError(f"C solution extraction/classification drift {channel}")
        rows = rec.get("solution_coefficients", [])
        if extracted:
            solution = parse_solution(rows)
            if set(solution) != set(ids):
                raise AssertionError(f"C solution support drift {channel}")
            if sha(rows) != rec.get("canonical_solution_sha256"):
                raise AssertionError(f"C solution digest drift {channel}")
            if apply_solution(ids, cols, solution) != target:
                raise AssertionError(f"C exact solution substitution drift {channel}")
            if rec.get("exact_substitution_checks") != got["active_cell_count"]:
                raise AssertionError(f"C substitution-check count drift {channel}")
            extracted_count += 1
            substitution_checks += got["active_cell_count"]
        else:
            if rows or rec.get("canonical_solution_sha256") is not None:
                raise AssertionError(f"C inconsistent system carries solution {channel}")
            if rec.get("exact_substitution_checks") != 0:
                raise AssertionError(f"C inconsistent system carries substitution checks {channel}")

    lgot, lids, lcols, ltarget = reconstruct_channel("l1", strata, specialized, supports)
    mirror = result.get("mirrored_l1_system", {})
    for key in (
        "classification", "coefficient_rank", "augmented_rank", "unknown_count",
        "active_cell_count", "global_coefficient_matrix_sha256", "global_target_sha256",
    ):
        if mirror.get(key) != lgot[key]:
            raise AssertionError(f"independent C l1 reconstruction drift:{key}")

    krec = expected["k1"]
    if (
        lgot["classification"], lgot["coefficient_rank"], lgot["augmented_rank"],
        lgot["active_cell_count"]
    ) != (
        krec["classification"], krec["coefficient_rank"], krec["augmented_rank"],
        krec["active_cell_count"]
    ):
        raise AssertionError("C independent k1/l1 global rank mirror drift")

    mirror_solution_ok = False
    if krec["exact_solution_extracted"]:
        ksol = parse_solution(krec["solution_coefficients"])
        lsol = {mirror_unknown_k_to_l(uid): q for uid, q in ksol.items()}
        if set(lsol) != set(lids):
            raise AssertionError("C independent l1 mirrored solution support drift")
        if apply_solution(lids, lcols, lsol) != ltarget:
            raise AssertionError("C independent l1 mirrored solution substitution drift")
        mirror_solution_ok = True
    if mirror.get("mirrored_k1_solution_exactly_satisfies_l1") != mirror_solution_ok:
        raise AssertionError("C mirrored l1 solution witness drift")

    all_consistent = consistent_count == len(a.INDEPENDENT_CHANNELS)
    if result.get("globally_consistent_independent_channel_count") != consistent_count:
        raise AssertionError("C global consistent-channel aggregate drift")
    if result.get("globally_inconsistent_independent_channel_count") != inconsistent_count:
        raise AssertionError("C global inconsistent-channel aggregate drift")
    if result.get("exact_solution_extracted_channel_count") != extracted_count:
        raise AssertionError("C extraction aggregate drift")
    if result.get("all_independent_channels_globally_consistent") != all_consistent:
        raise AssertionError("C all-channel compatibility aggregate drift")

    expected_terminal = (
        "T3_010_C_COMPLETE__FULL_CORRECTION_LAYER_RECOMBINATION_PENDING"
        if all_consistent
        else "BOUNDED_SUPPORT_LOCKED_DEGREE0_CORRECTION_CLASS_GLOBALLY_INCOMPATIBLE"
    )
    if result.get("terminal") != expected_terminal:
        raise AssertionError("C terminal drift")

    for key in (
        "local_consistency_promoted_to_certificate",
        "full_correction_layer_recombined",
        "full_symbolic_flux_identity_substituted",
        "finite_boundary_assembly_completed",
        "final_n_holonomic_search_run",
        "finite_sampling_used_as_sum_proof",
        "residual_sum_zero_proved",
    ):
        if result.get(key):
            raise AssertionError(f"C claim-boundary inflation:{key}")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("C proof/promotion inflation")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("C T3 status inflation")

    return {
        "schema_version": "1.0.0",
        "stage": STAGE,
        "status": "INDEPENDENT_T3_010_C_GLOBAL_EXACT_SOLUTION_REPLAY_COMPLETE",
        "independent_channel_count": len(a.INDEPENDENT_CHANNELS),
        "globally_consistent_independent_channel_count": consistent_count,
        "globally_inconsistent_independent_channel_count": inconsistent_count,
        "exact_solution_extracted_channel_count": extracted_count,
        "exact_substitution_check_count": substitution_checks,
        "mirrored_l1_solution_check": mirror_solution_ok,
        "rank_path": "independent exact-Q reverse sparse elimination over cell-namespaced global coordinates",
        "producer_matrix_imported_as_authority": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    import t3_010_c as producer
    print(json.dumps(verify(producer.build()), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
