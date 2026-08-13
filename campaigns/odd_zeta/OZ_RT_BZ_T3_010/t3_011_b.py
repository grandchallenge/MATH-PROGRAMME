#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_a as p  # noqa: E402

c = p.c
b = p.b
a = p.a

OPERATION = "OZ-RT-BZ-T3-011-B"
STAGE = "T3_011_B_EXACT_COKERNEL_ACTIVE_SINGLE_CHANNEL_LINEAR_NONZERO_RESPONSE_LIFT_VIABILITY_GATE"
CLASS_ID = "SUPPORT_LOCKED_SINGLE_CHANNEL_LINEAR_NONZERO_RESPONSE_LIFT_001"
A_REVIEWED_HEAD = "c7bdd6c76f7abd76ea39430dc6758418ea557a19"
A_MERGE_COMMIT = "862f7680e1bf09f66f475c1f371f3c4a377f4cad"
A_BLOBS = {
    "t3_011_a.py": "af3fc961e768b08c059ee40b2058b735df20a1fc",
    "T3_011_A_CONTRACT.json": "395ba53261d5480d5e6912948624e092d5d0048b",
    "verify_t3_011_a.py": "84d765ddce83e8a5af9b5b8f2362423e7eeed90c",
}
EXPECTED_NONZERO_COUNTS = {"n1": 67, "n2": 67, "n3": 67, "k1": 110}

Unknown = p.Unknown
GlobalVector = p.GlobalVector


def assert_a_locks() -> dict[str, str]:
    got: dict[str, str] = {}
    for name, want in A_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"T3-011-A source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_011_A_CONTRACT.json").read_text())
    if contract["stage"] != p.STAGE:
        raise AssertionError("T3-011-A stage drift")
    if contract["bounded_correction_class"]["id"] != p.CLASS_ID:
        raise AssertionError("T3-011-A bounded class drift")
    if contract["negative_boundary"]["terminal"] != (
        "BOUNDED_SINGLE_CHANNEL_LINEAR_ZERO_RESPONSE_LIFT_CLASS_EXHAUSTED"
    ):
        raise AssertionError("T3-011-A terminal contract drift")
    return got


def build_channel(
    channel: str,
    primitive_full: a.pcl.Layer,
    strata: list[dict],
    specialized: dict[str, a.pcl.Layer],
    supports: dict[tuple[str, str], dict[str, list[tuple[str, ...]]]],
) -> tuple[dict, dict]:
    base, ids, cols, target = c.build_channel_system(
        channel, primitive_full, strata, specialized, supports
    )
    if base["classification"] != "EXACTLY_INCONSISTENT":
        raise AssertionError(f"T3-011-B requires inconsistent C base: {channel}")

    nonzero_items = [(i, uid) for i, (uid, col) in enumerate(zip(ids, cols)) if col]
    if len(nonzero_items) != EXPECTED_NONZERO_COUNTS[channel]:
        raise AssertionError(f"nonzero-response candidate count drift in {channel}")
    if len(nonzero_items) != base["coefficient_rank"]:
        raise AssertionError(f"nonzero-response bank/rank drift in {channel}")

    basis, _, _ = p.echelon_basis(cols)
    if len(basis) != base["coefficient_rank"]:
        raise AssertionError(f"base echelon rank drift in {channel}")
    target_residual = p.reduce_vector(target, basis)
    if not target_residual:
        raise AssertionError(f"inconsistent target residual vanished in {channel}")
    witness, witness_projection_residual = p.cokernel_witness(cols, target)
    if not witness_projection_residual:
        raise AssertionError("witness projection residual unexpectedly empty")

    active_ids = {x["id"] for x in base["active_cells"]}
    trials = []
    survivors = []
    survivor_payloads: dict[str, tuple[Unknown, GlobalVector, dict[Unknown, Q]]] = {}

    for _, uid in nonzero_items:
        lift_col = p.lifted_global_column(channel, uid, strata, active_ids)
        rec = p.candidate_record(
            channel,
            uid,
            lift_col,
            witness,
            basis,
            target_residual,
            base["coefficient_rank"],
            len(ids),
        )
        if rec["rank_consistent"]:
            ext_uid = p.lift_unknown(uid, channel)
            ext_ids = ids + [ext_uid]
            ext_cols = cols + [lift_col]
            solution = c.exact_particular_solution(ext_ids, ext_cols, target)
            if solution is None:
                raise AssertionError(f"rank-consistent lift solver failure in {channel}:{uid}")
            if c.apply_solution(ext_ids, ext_cols, solution) != target:
                raise AssertionError(f"lift exact substitution failure in {channel}:{uid}")
            rec["exact_solution_exists"] = True
            rec["exact_substitution_checks"] = base["active_cell_count"]
            rec["canonical_solution_sha256"] = p.solution_digest(ext_ids, solution)
            key = c.ukey(uid)
            survivors.append(uid)
            survivor_payloads[key] = (ext_uid, lift_col, solution)
        trials.append(rec)

    selected = survivors[0] if survivors else None
    selected_solution_rows = []
    selected_solution_sha = None
    selected_lift_response_sha = None
    selected_solution = None
    selected_lift_col = None
    selected_ext_uid = None
    if selected is not None:
        selected_ext_uid, selected_lift_col, selected_solution = survivor_payloads[c.ukey(selected)]
        ext_ids = ids + [selected_ext_uid]
        selected_solution_sha = p.solution_digest(ext_ids, selected_solution)
        selected_lift_response_sha = c.global_vector_digest(selected_lift_col)
        for uid in ext_ids:
            q = selected_solution.get(uid, Q(0))
            selected_solution_rows.append([uid[0], list(uid[1]), q.numerator, q.denominator])

    nonzero_pairing_count = sum(x["obstruction_pairing_nonzero"] for x in trials)
    zero_pairing_count = len(trials) - nonzero_pairing_count
    if selected is not None:
        disposition = "CANONICAL_SINGLE_LIFT_SURVIVOR"
    elif nonzero_pairing_count:
        disposition = "COKERNEL_ACTIVE_SINGLE_LIFTS_EXACTLY_INCONSISTENT"
    else:
        disposition = "ALL_NONZERO_RESPONSE_SINGLE_LIFTS_COKERNEL_INVISIBLE"

    record = {
        "channel": channel,
        "base_unknown_count": len(ids),
        "base_coefficient_rank": base["coefficient_rank"],
        "base_augmented_rank": base["augmented_rank"],
        "base_nullity": base["nullity"],
        "base_zero_global_columns": base["zero_global_columns"],
        "active_cell_count": base["active_cell_count"],
        "candidate_count": len(nonzero_items),
        "candidate_bank": "complete-global-response-nonzero C unknowns only",
        "cokernel_witness_support_count": len(witness),
        "cokernel_witness_sha256": p.sha(p.witness_rows(witness)),
        "cokernel_witness_rows": p.witness_rows(witness),
        "cokernel_target_pairing": p.qjson(p.pairing(witness, target)),
        "target_quotient_residual_sha256": c.global_vector_digest(target_residual),
        "zero_obstruction_pairing_candidate_count": zero_pairing_count,
        "nonzero_obstruction_pairing_candidate_count": nonzero_pairing_count,
        "rank_tested_candidate_count": nonzero_pairing_count,
        "rank_consistent_candidate_count": len(survivors),
        "trials": trials,
        "canonical_selected_candidate": p.unknown_json(selected) if selected else None,
        "selected_lift_response_sha256": selected_lift_response_sha,
        "selected_solution_sha256": selected_solution_sha,
        "selected_solution_coefficients": selected_solution_rows,
        "selected_exact_substitution_checks": base["active_cell_count"] if selected else 0,
        "canonical_channel_disposition": disposition,
    }
    internal = {
        "ids": ids,
        "cols": cols,
        "target": target,
        "selected": selected,
        "selected_ext_uid": selected_ext_uid,
        "selected_lift_col": selected_lift_col,
        "selected_solution": selected_solution,
    }
    return record, internal


def build() -> dict:
    a_locks = assert_a_locks()
    p.assert_c_locks()
    c.assert_b_locks()
    b.assert_a_locks()
    a.assert_source_locks()
    a.validate_architecture()

    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 coefficient-layer digest drift in T3-011-B")
    primitive_full = a.primitive_oriented_layer(layer)
    strata = a.shell_strata()
    specialized = {
        st["id"]: a.primitive_oriented_layer(
            a.specialize_layer(layer, st["k_offset"], st["l_offset"])
        )
        for st in strata
    }
    supports = {
        (channel, block): b.candidate_support(primitive_full, channel, block)
        for channel in a.CHANNEL_SCALARS
        for block in c.BLOCK_ORDER
    }

    channels = []
    internals = {}
    for channel in a.INDEPENDENT_CHANNELS:
        rec, internal = build_channel(channel, primitive_full, strata, specialized, supports)
        channels.append(rec)
        internals[channel] = internal

    if sum(x["candidate_count"] for x in channels) != 311:
        raise AssertionError("T3-011-B independent candidate bank drift")

    lbase, lids, lcols, ltarget = c.build_channel_system(
        "l1", primitive_full, strata, specialized, supports
    )
    kint = internals["k1"]
    mirror_record = {
        "base_classification": lbase["classification"],
        "base_unknown_count": lbase["unknown_count"],
        "base_coefficient_rank": lbase["coefficient_rank"],
        "base_augmented_rank": lbase["augmented_rank"],
        "canonical_mirrored_candidate": None,
        "lift_coefficient_rank": None,
        "lift_augmented_rank": None,
        "lift_classification": "NOT_TESTED_NO_CANONICAL_K1_SURVIVOR",
        "mirrored_k1_solution_exactly_satisfies_l1": False,
    }

    if kint["selected"] is not None:
        luid = c.mirror_unknown_k_to_l(kint["selected"])
        lactive = {x["id"] for x in lbase["active_cells"]}
        llift = p.lifted_global_column("l1", luid, strata, lactive)
        lrank, _ = b.rank_sparse(lcols + [llift])
        laug, _ = b.rank_sparse(lcols + [llift, ltarget])
        lcls = b.classify(lrank, laug, len(lids) + 1)
        mirror_record.update({
            "canonical_mirrored_candidate": p.unknown_json(luid),
            "lift_coefficient_rank": lrank,
            "lift_augmented_rank": laug,
            "lift_classification": lcls,
        })

        if kint["selected_solution"] is not None:
            ksol = kint["selected_solution"]
            lsol: dict[Unknown, Q] = {}
            for uid in kint["ids"]:
                lsol[c.mirror_unknown_k_to_l(uid)] = ksol.get(uid, Q(0))
            lext_uid = p.lift_unknown(luid, "l1")
            lsol[lext_uid] = ksol.get(kint["selected_ext_uid"], Q(0))
            if set(lsol) != set(lids) | {lext_uid}:
                raise AssertionError("mirrored selected solution support drift")
            if c.apply_solution(lids + [lext_uid], lcols + [llift], lsol) == ltarget:
                mirror_record["mirrored_k1_solution_exactly_satisfies_l1"] = True

    all_selected = all(x["canonical_selected_candidate"] is not None for x in channels)
    mirror_ok = mirror_record["mirrored_k1_solution_exactly_satisfies_l1"]
    all_viable = all_selected and mirror_ok
    terminal = (
        "T3_011_B_COMPLETE__SINGLE_LINEAR_NONZERO_RESPONSE_LIFT_CLASS_VIABLE__EXACT_RECOMBINATION_PENDING"
        if all_viable
        else "BOUNDED_SINGLE_CHANNEL_LINEAR_NONZERO_RESPONSE_LIFT_CLASS_EXHAUSTED"
    )

    return {
        "schema_version": "1.0.0",
        "issue": 486,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "EXACT_COKERNEL_ACTIVE_SINGLE_CHANNEL_LINEAR_NONZERO_RESPONSE_LIFT_GATE_COMPLETE",
        "t3_011_a_checkpoint": {
            "reviewed_head": A_REVIEWED_HEAD,
            "merge_commit": A_MERGE_COMMIT,
            "source_blobs": a_locks,
            "required_terminal": "BOUNDED_SINGLE_CHANNEL_LINEAR_ZERO_RESPONSE_LIFT_CLASS_EXHAUSTED",
        },
        "bounded_correction_class": {
            "id": CLASS_ID,
            "base_class": "SUPPORT_LOCKED_ORIENTED_ONE_BODY_DEGREE0_WEIGHT_CORRECTION_001",
            "candidate_bank": "complete-global-response-nonzero C unknowns only",
            "independent_trial_count": 311,
            "one_lift_per_trial": True,
            "pairs_admitted": False,
            "mix_with_zero_response_bank": False,
            "new_harmonic_monomials": False,
            "full_degree1_envelope": False,
            "rational_prefactor_search": False,
            "adaptive_basis_growth": False,
            "generic_198_raw_jet_reopened": False,
            "recurrence_search": False,
        },
        "channel_systems": channels,
        "independent_candidate_count": sum(x["candidate_count"] for x in channels),
        "independent_nonzero_obstruction_pairing_candidate_count": sum(
            x["nonzero_obstruction_pairing_candidate_count"] for x in channels
        ),
        "independent_rank_consistent_candidate_count": sum(
            x["rank_consistent_candidate_count"] for x in channels
        ),
        "independent_channel_with_survivor_count": sum(
            x["canonical_selected_candidate"] is not None for x in channels
        ),
        "all_independent_channels_have_canonical_single_lift": all_selected,
        "mirrored_l1_system": mirror_record,
        "all_channels_and_mirror_viable": all_viable,
        "full_correction_layer_recombined": False,
        "finite_boundary_assembly_completed": False,
        "final_n_holonomic_search_run": False,
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
