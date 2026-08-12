#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import verify_t3_011_a as va  # noqa: E402

vc = va.vc
vb = va.vb
a = va.a

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
CHANNEL_COORDINATE = {"n1": "n", "n2": "n", "n3": "n", "k1": "k", "l1": "l"}

Unknown = va.Unknown


def verify(result: dict) -> dict:
    if result.get("stage") != STAGE:
        raise AssertionError("T3-011-B stage drift")
    checkpoint = result.get("t3_011_a_checkpoint", {})
    if checkpoint.get("reviewed_head") != A_REVIEWED_HEAD:
        raise AssertionError("T3-011-A reviewed-head drift in T3-011-B")
    if checkpoint.get("merge_commit") != A_MERGE_COMMIT:
        raise AssertionError("T3-011-A merge checkpoint drift in T3-011-B")
    for name, want in A_BLOBS.items():
        if a.git_blob_sha1(HERE / name) != want:
            raise AssertionError(f"T3-011-A blob drift in T3-011-B verifier: {name}")

    contract = json.loads((HERE / "T3_011_B_CONTRACT.json").read_text())
    if contract["stage"] != STAGE:
        raise AssertionError("T3-011-B contract stage drift")
    if contract["bounded_correction_class"]["id"] != CLASS_ID:
        raise AssertionError("T3-011-B class drift")
    if contract["bounded_correction_class"]["expected_independent_trials"] != 311:
        raise AssertionError("T3-011-B bounded trial count drift")
    for forbidden in (
        "pairs_admitted",
        "arbitrary_linear_combinations_admitted",
        "mix_with_zero_response_bank",
        "new_harmonic_monomials",
        "full_degree1_envelope",
        "rational_prefactor_search",
        "adaptive_basis_growth",
        "generic_198_raw_jet_reopened",
        "recurrence_search",
    ):
        if contract["bounded_correction_class"][forbidden]:
            raise AssertionError(f"T3-011-B forbidden enlargement: {forbidden}")

    a.assert_source_locks()
    a.validate_architecture()
    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 predecessor drift in T3-011-B verifier")
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
        for block in vc.BLOCK_ORDER
    }

    expected_records = {x["channel"]: x for x in result.get("channel_systems", [])}
    if set(expected_records) != set(a.INDEPENDENT_CHANNELS):
        raise AssertionError("T3-011-B channel cardinality drift")

    selected_count = 0
    trial_count = 0
    nonzero_pairing_total = 0
    rank_consistent_total = 0
    independent_witness_support = {}
    reconstructed = {}
    channel_dispositions = {}

    for channel in a.INDEPENDENT_CHANNELS:
        base, ids, cols, target = vc.reconstruct_channel(channel, strata, specialized, supports)
        if base["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"independent C base no longer inconsistent: {channel}")
        nonzero_uids = [uid for uid, col in zip(ids, cols) if col]
        if len(nonzero_uids) != EXPECTED_NONZERO_COUNTS[channel]:
            raise AssertionError(f"independent nonzero-response bank drift: {channel}")
        if len(nonzero_uids) != base["coefficient_rank"]:
            raise AssertionError(f"nonzero bank/rank drift: {channel}")

        rec = expected_records[channel]
        if rec["candidate_count"] != len(nonzero_uids):
            raise AssertionError(f"producer candidate count drift: {channel}")
        if rec["base_coefficient_rank"] != base["coefficient_rank"]:
            raise AssertionError(f"producer base rank drift: {channel}")
        if rec["base_augmented_rank"] != base["augmented_rank"]:
            raise AssertionError(f"producer base augmented-rank drift: {channel}")

        producer_witness = va.parse_witness_rows(rec["cokernel_witness_rows"])
        if va.sha(va.witness_rows(producer_witness)) != rec["cokernel_witness_sha256"]:
            raise AssertionError(f"producer witness digest drift: {channel}")
        for col in cols:
            if va.pairing(producer_witness, col):
                raise AssertionError(f"producer witness fails C annihilation: {channel}")
        if va.pairing(producer_witness, target) != 1:
            raise AssertionError(f"producer witness target normalization drift: {channel}")

        iw = va.independent_cokernel_witness(cols, target)
        independent_witness_support[channel] = len(iw)
        if va.pairing(iw, target) != 1:
            raise AssertionError(f"independent witness normalization drift: {channel}")

        basis, _, _ = va.reverse_echelon_basis(cols)
        target_residual = va.reduce_reverse(target, basis)
        active = {f"{channel}:{block}:{st['id']}" for st in strata for block in vc.BLOCK_ORDER}
        trials = rec.get("trials", [])
        if len(trials) != len(nonzero_uids):
            raise AssertionError(f"trial ledger cardinality drift: {channel}")

        exact_survivors = []
        selected_lift = None
        selected_uid = None
        channel_nonzero_pairing = 0
        for uid, trial in zip(nonzero_uids, trials):
            if trial["candidate"] != [uid[0], list(uid[1])]:
                raise AssertionError(f"candidate order drift: {channel}")
            lift = va.lifted_global_column(channel, uid, strata, active)
            if trial["lift_response_sha256"] != va.global_vector_digest(lift):
                raise AssertionError(f"lift response digest drift: {channel}:{uid}")
            producer_pair = va.pairing(producer_witness, lift)
            if trial["obstruction_pairing"] != va.qjson(producer_pair):
                raise AssertionError(f"candidate obstruction pairing drift: {channel}:{uid}")
            rank, aug, cls = va.exact_classification(
                base["coefficient_rank"], len(ids), basis, target_residual, lift
            )
            if producer_pair == 0:
                if trial["classification"] != "REJECTED_BY_COKERNEL_WITNESS":
                    raise AssertionError(f"zero-pairing pruning drift: {channel}:{uid}")
                if trial["exact_rank_test_run"]:
                    raise AssertionError(f"zero-pairing candidate incorrectly rank-tested: {channel}:{uid}")
                if cls != "EXACTLY_INCONSISTENT":
                    raise AssertionError(f"cokernel-pruned candidate was actually viable: {channel}:{uid}")
            else:
                channel_nonzero_pairing += 1
                if not trial["exact_rank_test_run"]:
                    raise AssertionError(f"nonzero-pairing rank test omitted: {channel}:{uid}")
                if (trial["coefficient_rank"], trial["augmented_rank"], trial["classification"]) != (
                    rank, aug, cls
                ):
                    raise AssertionError(f"independent lift rank drift: {channel}:{uid}")
            if cls.startswith("CONSISTENT_"):
                exact_survivors.append(uid)
                if not trial["exact_solution_exists"]:
                    raise AssertionError(f"rank-consistent candidate lacks exact solution flag: {channel}:{uid}")
            trial_count += 1

        if rec["nonzero_obstruction_pairing_candidate_count"] != channel_nonzero_pairing:
            raise AssertionError(f"nonzero-pairing count drift: {channel}")
        if rec["zero_obstruction_pairing_candidate_count"] != len(nonzero_uids) - channel_nonzero_pairing:
            raise AssertionError(f"zero-pairing count drift: {channel}")
        if rec["rank_tested_candidate_count"] != channel_nonzero_pairing:
            raise AssertionError(f"rank-tested count drift: {channel}")
        if rec["rank_consistent_candidate_count"] != len(exact_survivors):
            raise AssertionError(f"rank-consistent count drift: {channel}")
        nonzero_pairing_total += channel_nonzero_pairing
        rank_consistent_total += len(exact_survivors)

        selected = exact_survivors[0] if exact_survivors else None
        if rec["canonical_selected_candidate"] != ([selected[0], list(selected[1])] if selected else None):
            raise AssertionError(f"canonical selected candidate drift: {channel}")

        if selected is not None:
            expected_disposition = "CANONICAL_SINGLE_LIFT_SURVIVOR"
            selected_count += 1
            selected_uid = selected
            selected_lift = va.lifted_global_column(channel, selected, strata, active)
            solution = va.parse_solution_rows(rec["selected_solution_coefficients"])
            ext_uid = (selected[0], (f"__CHANNEL_LINEAR_{CHANNEL_COORDINATE[channel]}__",) + selected[1])
            ext_ids = ids + [ext_uid]
            if set(solution) != set(ext_ids):
                raise AssertionError(f"selected solution support drift: {channel}")
            if va.apply_solution(ext_ids, cols + [selected_lift], solution) != target:
                raise AssertionError(f"selected exact substitution drift: {channel}")
            rows = []
            for uid2 in ext_ids:
                q = solution[uid2]
                rows.append([uid2[0], list(uid2[1]), q.numerator, q.denominator])
            if va.sha(rows) != rec["selected_solution_sha256"]:
                raise AssertionError(f"selected solution digest drift: {channel}")
            if rec["selected_exact_substitution_checks"] != base["active_cell_count"]:
                raise AssertionError(f"selected substitution count drift: {channel}")
        elif channel_nonzero_pairing:
            expected_disposition = "COKERNEL_ACTIVE_SINGLE_LIFTS_EXACTLY_INCONSISTENT"
            if rec["selected_solution_coefficients"]:
                raise AssertionError(f"solution rows present without selected candidate: {channel}")
        else:
            expected_disposition = "ALL_NONZERO_RESPONSE_SINGLE_LIFTS_COKERNEL_INVISIBLE"
            if rec["selected_solution_coefficients"]:
                raise AssertionError(f"solution rows present without selected candidate: {channel}")

        if rec["canonical_channel_disposition"] != expected_disposition:
            raise AssertionError(f"canonical channel disposition drift: {channel}")
        channel_dispositions[channel] = expected_disposition
        reconstructed[channel] = {
            "ids": ids,
            "cols": cols,
            "target": target,
            "selected_uid": selected_uid,
            "selected_lift": selected_lift,
            "selected_solution_rows": rec["selected_solution_coefficients"],
        }

    if trial_count != 311 or result.get("independent_candidate_count") != 311:
        raise AssertionError("T3-011-B aggregate trial count drift")
    if result.get("independent_nonzero_obstruction_pairing_candidate_count") != nonzero_pairing_total:
        raise AssertionError("T3-011-B aggregate nonzero-pairing drift")
    if result.get("independent_rank_consistent_candidate_count") != rank_consistent_total:
        raise AssertionError("T3-011-B aggregate rank-consistent drift")
    if result.get("independent_channel_with_survivor_count") != selected_count:
        raise AssertionError("T3-011-B selected-channel count drift")

    lbase, lids, lcols, ltarget = vc.reconstruct_channel("l1", strata, specialized, supports)
    mirror = result.get("mirrored_l1_system", {})
    kdata = reconstructed["k1"]
    mirror_ok = False
    if kdata["selected_uid"] is None:
        if mirror.get("canonical_mirrored_candidate") is not None:
            raise AssertionError("l1 mirror candidate present without k1 survivor")
        if mirror.get("lift_classification") != "NOT_TESTED_NO_CANONICAL_K1_SURVIVOR":
            raise AssertionError("l1 no-candidate terminal drift")
    else:
        luid = vc.mirror_unknown_k_to_l(kdata["selected_uid"])
        if mirror.get("canonical_mirrored_candidate") != [luid[0], list(luid[1])]:
            raise AssertionError("l1 mirrored candidate drift")
        lactive = {f"l1:{block}:{st['id']}" for st in strata for block in vc.BLOCK_ORDER}
        llift = va.lifted_global_column("l1", luid, strata, lactive)
        lbasis, _, _ = va.reverse_echelon_basis(lcols)
        ltres = va.reduce_reverse(ltarget, lbasis)
        lr, la, lcls = va.exact_classification(lbase["coefficient_rank"], len(lids), lbasis, ltres, llift)
        if (mirror.get("lift_coefficient_rank"), mirror.get("lift_augmented_rank"), mirror.get("lift_classification")) != (lr, la, lcls):
            raise AssertionError("l1 independent lift rank drift")

        ksolution = va.parse_solution_rows(kdata["selected_solution_rows"])
        lsolution = {}
        marker = f"__CHANNEL_LINEAR_{CHANNEL_COORDINATE['k1']}__"
        for uid, q in ksolution.items():
            scalar, mon = uid
            if mon and mon[0] == marker:
                original = (scalar, mon[1:])
                mirrored_original = vc.mirror_unknown_k_to_l(original)
                lsolution[(mirrored_original[0], ("__CHANNEL_LINEAR_l__",) + mirrored_original[1])] = q
            else:
                lsolution[vc.mirror_unknown_k_to_l(uid)] = q
        lext = (luid[0], ("__CHANNEL_LINEAR_l__",) + luid[1])
        if set(lsolution) != set(lids) | {lext}:
            raise AssertionError("l1 mirrored solution support drift")
        mirror_ok = va.apply_solution(lids + [lext], lcols + [llift], lsolution) == ltarget
        if mirror.get("mirrored_k1_solution_exactly_satisfies_l1") != mirror_ok:
            raise AssertionError("l1 mirrored solution substitution drift")

    all_selected = selected_count == 4
    all_viable = all_selected and mirror_ok
    if result.get("all_independent_channels_have_canonical_single_lift") != all_selected:
        raise AssertionError("all-selected aggregate drift")
    if result.get("all_channels_and_mirror_viable") != all_viable:
        raise AssertionError("all-viable aggregate drift")
    expected_terminal = (
        "T3_011_B_COMPLETE__SINGLE_LINEAR_NONZERO_RESPONSE_LIFT_CLASS_VIABLE__EXACT_RECOMBINATION_PENDING"
        if all_viable
        else "BOUNDED_SINGLE_CHANNEL_LINEAR_NONZERO_RESPONSE_LIFT_CLASS_EXHAUSTED"
    )
    if result.get("terminal") != expected_terminal:
        raise AssertionError("T3-011-B terminal drift")

    for key, want in (
        ("full_correction_layer_recombined", False),
        ("finite_boundary_assembly_completed", False),
        ("final_n_holonomic_search_run", False),
        ("residual_sum_zero_proved", False),
        ("proof_effect", "NONE"),
        ("promotion_effect", "NONE"),
        ("t3_status", "OPEN_WITH_CHARACTERIZED_BLOCKER"),
    ):
        if result.get(key) != want:
            raise AssertionError(f"T3-011-B claim-boundary inflation: {key}")

    return {
        "status": "INDEPENDENT_T3_011_B_COKERNEL_NONZERO_RESPONSE_SINGLE_LIFT_REPLAY_COMPLETE",
        "independent_trial_count": trial_count,
        "independent_nonzero_obstruction_pairing_candidate_count": nonzero_pairing_total,
        "independent_rank_consistent_candidate_count": rank_consistent_total,
        "independent_channel_with_survivor_count": selected_count,
        "all_channels_and_mirror_viable": all_viable,
        "independent_witness_support_count": independent_witness_support,
        "canonical_channel_dispositions": channel_dispositions,
        "producer_matrix_imported_as_authority": False,
        "terminal": expected_terminal,
    }


def main() -> int:
    import t3_011_b as producer
    result = producer.build()
    print(json.dumps(verify(result), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
