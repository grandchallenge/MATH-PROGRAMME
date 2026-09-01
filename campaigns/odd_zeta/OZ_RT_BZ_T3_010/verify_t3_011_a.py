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

import verify_t3_010_c as vc  # noqa: E402

vb = vc.vb
a = vc.a

STAGE = "T3_011_A_EXACT_COKERNEL_GUIDED_SINGLE_CHANNEL_LINEAR_ZERO_RESPONSE_LIFT_VIABILITY_GATE"
CLASS_ID = "SUPPORT_LOCKED_SINGLE_CHANNEL_LINEAR_ZERO_RESPONSE_LIFT_001"
C_HEAD = "ca02bb6dad2970c169eb9b8745c871d4332447fb"
C_BLOBS = {
    "t3_010_c.py": "c6359f01c12011a22194bfe7ff960aa3e30452d3",
    "T3_010_C_CONTRACT.json": "4f547f29d8bcb734f5e76816c5838d2b095a51b9",
    "verify_t3_010_c.py": "e7defaf7fb6fa05128923ecdb1023f07882d3d36",
}
EXPECTED_ZERO_COUNTS = {"n1": 49, "n2": 49, "n3": 49, "k1": 48}
CHANNEL_COORDINATE = {"n1": "n", "n2": "n", "n3": "n", "k1": "k", "l1": "l"}
CHANNEL_INCREMENT = {"n1": 1, "n2": 2, "n3": 3, "k1": 1, "l1": 1}

Unknown = tuple[str, tuple[str, ...]]


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def gkey(coord) -> str:
    return repr(coord)


def add_scaled(dst: dict, src: dict, factor: Q) -> None:
    if not factor:
        return
    for key, value in src.items():
        z = dst.get(key, Q(0)) + factor * value
        if z:
            dst[key] = z
        elif key in dst:
            del dst[key]


def pairing(functional: dict, vector: dict) -> Q:
    return sum((q * vector.get(coord, Q(0)) for coord, q in functional.items()), Q(0))


def global_vector_digest(vec: dict) -> str:
    rows = []
    for (cell_id, coord) in sorted(vec, key=gkey):
        q = vec[(cell_id, coord)]
        rows.append([cell_id, vb.cjson(coord), q.numerator, q.denominator])
    return sha(rows)


def parse_coord_json(row):
    scalar, mon, sig_rows = row
    sig = tuple((tuple(int(x) for x in factor), int(exp)) for factor, exp in sig_rows)
    return (str(scalar), tuple(str(x) for x in mon), sig)


def parse_witness_rows(rows: list[list]) -> dict:
    out = {}
    for cell_id, coord_json, num, den in rows:
        key = (str(cell_id), parse_coord_json(coord_json))
        if key in out:
            raise AssertionError("duplicate producer cokernel witness coordinate")
        out[key] = Q(int(num), int(den))
    return out


def witness_rows(functional: dict) -> list[list]:
    rows = []
    for (cell_id, coord) in sorted(functional, key=gkey):
        q = functional[(cell_id, coord)]
        rows.append([cell_id, vb.cjson(coord), q.numerator, q.denominator])
    return rows


def reverse_echelon_basis(cols: list[dict]):
    basis = {}
    selected = []
    pivots = []
    for idx in reversed(range(len(cols))):
        v = {k: Q(q) for k, q in cols[idx].items() if q}
        while v:
            pivot = max(v, key=gkey)
            if pivot in basis:
                add_scaled(v, basis[pivot], -v[pivot])
                continue
            scale = v[pivot]
            v = {k: q / scale for k, q in v.items() if q}
            basis[pivot] = v
            selected.append(idx)
            pivots.append(pivot)
            break
    return basis, selected, pivots


def reduce_reverse(vector: dict, basis: dict) -> dict:
    v = {k: Q(q) for k, q in vector.items() if q}
    for pivot in sorted(basis, key=gkey, reverse=True):
        if pivot in v:
            add_scaled(v, basis[pivot], -v[pivot])
    return v


def solve_square_reverse(matrix: list[list[Q]], rhs: list[Q]) -> list[Q]:
    n = len(matrix)
    if len(rhs) != n or any(len(row) != n for row in matrix):
        raise ValueError("reverse square solve shape drift")
    aug = [[Q(x) for x in row] + [Q(rhs[i])] for i, row in enumerate(matrix)]
    for step in range(n):
        col = n - 1 - step
        row = n - 1 - step
        pivot = next((r for r in range(row, -1, -1) if aug[r][col]), None)
        if pivot is None:
            raise AssertionError("singular reverse canonical pivot matrix")
        if pivot != row:
            aug[row], aug[pivot] = aug[pivot], aug[row]
        scale = aug[row][col]
        aug[row] = [x / scale for x in aug[row]]
        for r in range(n):
            if r == row or not aug[r][col]:
                continue
            factor = aug[r][col]
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[row])]
    sol = [Q(0) for _ in range(n)]
    for row in range(n):
        pivot_col = next((j for j, x in enumerate(aug[row][:-1]) if x), None)
        if pivot_col is None:
            raise AssertionError("reverse solve lost pivot")
        sol[pivot_col] = aug[row][-1]
    return sol


def independent_cokernel_witness(cols: list[dict], target: dict) -> dict:
    basis, selected, pivots = reverse_echelon_basis(cols)
    r = len(selected)
    if r != vb.rank_reverse(cols):
        raise AssertionError("independent base rank/echelon drift")
    if not r:
        qcoord = max(target, key=gkey)
        return {qcoord: Q(1) / target[qcoord]}

    matrix = [[cols[j].get(p, Q(0)) for j in selected] for p in pivots]
    alpha = solve_square_reverse(matrix, [target.get(p, Q(0)) for p in pivots])
    residual = {k: Q(q) for k, q in target.items() if q}
    for coeff, j in zip(alpha, selected):
        add_scaled(residual, cols[j], -coeff)
    if not residual:
        raise AssertionError("independent C target unexpectedly in base span")
    qcoord = max(residual, key=gkey)
    transpose = [[matrix[row][col] for row in range(r)] for col in range(r)]
    qrow = [cols[j].get(qcoord, Q(0)) for j in selected]
    gamma = solve_square_reverse(transpose, [-x for x in qrow])
    functional = {qcoord: Q(1)}
    for p, coeff in zip(pivots, gamma):
        if coeff:
            functional[p] = functional.get(p, Q(0)) + coeff
            if not functional[p]:
                del functional[p]
    for col in cols:
        if pairing(functional, col):
            raise AssertionError("independent cokernel witness misses base column")
    value = pairing(functional, target)
    if not value:
        raise AssertionError("independent cokernel witness misses target")
    return {k: q / value for k, q in functional.items() if q}


def monomial_poly(mon: tuple[str, ...]) -> a.rc.Poly:
    out = a.rc.p_const(1)
    for name in mon:
        out = a.rc.p_mul(out, a.rc.p_atom(name))
    return out


def shifted_monomial_poly(mon: tuple[str, ...], shift: tuple[int, int, int]) -> a.rc.Poly:
    out = a.rc.p_const(1)
    for name in mon:
        out = a.rc.p_mul(
            out, a.rc.p_add(a.rc.p_atom(name), vb.delta_atom(name, shift))
        )
    return out


def coordinate_factors(channel: str):
    if channel in ("n1", "n2", "n3"):
        step = CHANNEL_INCREMENT[channel]
        return (1, 0, 0, 0), (1, 0, 0, step)
    if channel == "k1":
        return (0, 1, 0, 0), (0, 1, 0, 1)
    if channel == "l1":
        return (0, 0, 1, 0), (0, 0, 1, 1)
    raise ValueError(channel)


def lifted_delta(mon: tuple[str, ...], channel: str) -> a.rc.Poly:
    shift = a.pcl.SHIFTS[channel]
    f0, f1 = coordinate_factors(channel)
    shifted = shifted_monomial_poly(mon, shift)
    original = monomial_poly(mon)
    return a.rc.p_add(
        a.rc.p_scale(shifted, a.rc.r_factor(f1, exponent=1)),
        a.rc.p_scale(original, a.rc.r_factor(f0, exponent=1, scale=-1)),
    )


def lifted_global_column(channel: str, uid: Unknown, strata: list[dict], active: set[str]) -> dict:
    scalar, mon = uid
    raw = lifted_delta(mon, channel)
    out = {}
    for st in reversed(strata):
        sp = vb.sp(raw, st["k_offset"], st["l_offset"])
        for block in reversed(vc.BLOCK_ORDER):
            cell_id = f"{channel}:{block}:{st['id']}"
            if cell_id not in active:
                continue
            local = vb.response(sp, scalar, block)
            for coord, q in local.items():
                key = (cell_id, coord)
                z = out.get(key, Q(0)) + q
                if z:
                    out[key] = z
                elif key in out:
                    del out[key]
    return out


def proportional(a_vec: dict, b_vec: dict) -> bool:
    if not a_vec and not b_vec:
        return True
    if not a_vec or not b_vec:
        return False
    keys = sorted(set(a_vec).union(b_vec), key=gkey, reverse=True)
    pivot = next((k for k in keys if b_vec.get(k, Q(0))), None)
    if pivot is None:
        return False
    q = a_vec.get(pivot, Q(0)) / b_vec[pivot]
    return all(a_vec.get(k, Q(0)) == q * b_vec.get(k, Q(0)) for k in keys)


def exact_classification(base_rank: int, base_unknowns: int, basis: dict, target_residual: dict, lift: dict):
    lr = reduce_reverse(lift, basis)
    rank = base_rank + (1 if lr else 0)
    consistent = bool(lr) and proportional(target_residual, lr)
    if consistent:
        aug = rank
        cls = "CONSISTENT_UNIQUE" if rank == base_unknowns + 1 else "CONSISTENT_AFFINE"
    else:
        aug = base_rank + (1 if not lr else 2)
        cls = "EXACTLY_INCONSISTENT"
    return rank, aug, cls


def parse_solution_rows(rows: list[list]) -> dict[Unknown, Q]:
    out = {}
    for scalar, mon, num, den in rows:
        uid = (str(scalar), tuple(str(x) for x in mon))
        if uid in out:
            raise AssertionError("duplicate selected solution coefficient")
        out[uid] = Q(int(num), int(den))
    return out


def apply_solution(ids: list[Unknown], cols: list[dict], solution: dict[Unknown, Q]) -> dict:
    out = {}
    for uid, col in zip(ids, cols):
        add_scaled(out, col, solution.get(uid, Q(0)))
    return out


def verify(result: dict) -> dict:
    if result.get("stage") != STAGE:
        raise AssertionError("T3-011-A stage drift")
    if result.get("t3_010_c_checkpoint", {}).get("validated_head") != C_HEAD:
        raise AssertionError("T3-010-C checkpoint drift in T3-011-A")
    for name, want in C_BLOBS.items():
        if a.git_blob_sha1(HERE / name) != want:
            raise AssertionError(f"T3-010-C blob drift in T3-011-A verifier: {name}")
    contract = json.loads((HERE / "T3_011_A_CONTRACT.json").read_text())
    if contract["stage"] != STAGE:
        raise AssertionError("T3-011-A contract stage drift")
    if contract["bounded_correction_class"]["id"] != CLASS_ID:
        raise AssertionError("T3-011-A class drift")
    if contract["bounded_correction_class"]["expected_independent_trials"] != 195:
        raise AssertionError("T3-011-A bounded trial count drift")
    for forbidden in (
        "pairs_admitted", "arbitrary_linear_combinations_admitted",
        "new_harmonic_monomials", "full_degree1_envelope",
        "rational_prefactor_search", "adaptive_basis_growth",
        "generic_198_raw_jet_reopened",
    ):
        if contract["bounded_correction_class"][forbidden]:
            raise AssertionError(f"T3-011-A forbidden enlargement: {forbidden}")

    a.assert_source_locks()
    a.validate_architecture()
    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 predecessor drift in T3-011-A verifier")
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
        raise AssertionError("T3-011-A channel cardinality drift")

    selected_count = 0
    trial_count = 0
    independent_witness_support = {}
    reconstructed = {}

    for channel in a.INDEPENDENT_CHANNELS:
        base, ids, cols, target = vc.reconstruct_channel(
            channel, strata, specialized, supports
        )
        if base["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"independent C base no longer inconsistent: {channel}")
        zero_uids = [uid for uid, col in zip(ids, cols) if not col]
        if len(zero_uids) != EXPECTED_ZERO_COUNTS[channel]:
            raise AssertionError(f"independent zero-response bank drift: {channel}")
        rec = expected_records[channel]
        if rec["candidate_count"] != len(zero_uids):
            raise AssertionError(f"producer candidate count drift: {channel}")
        if rec["base_coefficient_rank"] != base["coefficient_rank"]:
            raise AssertionError(f"producer base rank drift: {channel}")
        if rec["base_augmented_rank"] != base["augmented_rank"]:
            raise AssertionError(f"producer base augmented-rank drift: {channel}")

        producer_witness = parse_witness_rows(rec["cokernel_witness_rows"])
        if sha(witness_rows(producer_witness)) != rec["cokernel_witness_sha256"]:
            raise AssertionError(f"producer witness digest drift: {channel}")
        for col in cols:
            if pairing(producer_witness, col):
                raise AssertionError(f"producer witness fails C annihilation: {channel}")
        if pairing(producer_witness, target) != 1:
            raise AssertionError(f"producer witness target normalization drift: {channel}")

        iw = independent_cokernel_witness(cols, target)
        independent_witness_support[channel] = len(iw)
        if pairing(iw, target) != 1:
            raise AssertionError(f"independent witness normalization drift: {channel}")

        basis, _, _ = reverse_echelon_basis(cols)
        target_residual = reduce_reverse(target, basis)
        active = {f"{channel}:{block}:{st['id']}" for st in strata for block in vc.BLOCK_ORDER}
        trials = rec.get("trials", [])
        if len(trials) != len(zero_uids):
            raise AssertionError(f"trial ledger cardinality drift: {channel}")

        exact_survivors = []
        selected_lift = None
        selected_uid = None
        for uid, trial in zip(zero_uids, trials):
            if trial["candidate"] != [uid[0], list(uid[1])]:
                raise AssertionError(f"candidate order drift: {channel}")
            lift = lifted_global_column(channel, uid, strata, active)
            if trial["lift_response_sha256"] != global_vector_digest(lift):
                raise AssertionError(f"lift response digest drift: {channel}:{uid}")
            producer_pair = pairing(producer_witness, lift)
            if trial["obstruction_pairing"] != qjson(producer_pair):
                raise AssertionError(f"candidate obstruction pairing drift: {channel}:{uid}")
            rank, aug, cls = exact_classification(
                base["coefficient_rank"], len(ids), basis, target_residual, lift
            )
            if producer_pair == 0:
                if trial["classification"] != "REJECTED_BY_COKERNEL_WITNESS":
                    raise AssertionError(f"zero-pairing pruning drift: {channel}:{uid}")
                if cls != "EXACTLY_INCONSISTENT":
                    raise AssertionError(f"cokernel-pruned candidate was actually viable: {channel}:{uid}")
            else:
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

        selected = exact_survivors[0] if exact_survivors else None
        if rec["canonical_selected_candidate"] != (
            [selected[0], list(selected[1])] if selected else None
        ):
            raise AssertionError(f"canonical selected candidate drift: {channel}")
        if selected is not None:
            selected_count += 1
            selected_uid = selected
            selected_lift = lifted_global_column(channel, selected, strata, active)
            solution = parse_solution_rows(rec["selected_solution_coefficients"])
            ext_uid = (selected[0], (f"__CHANNEL_LINEAR_{CHANNEL_COORDINATE[channel]}__",) + selected[1])
            ext_ids = ids + [ext_uid]
            if set(solution) != set(ext_ids):
                raise AssertionError(f"selected solution support drift: {channel}")
            if apply_solution(ext_ids, cols + [selected_lift], solution) != target:
                raise AssertionError(f"selected exact substitution drift: {channel}")
            rows = []
            for uid2 in ext_ids:
                q = solution[uid2]
                rows.append([uid2[0], list(uid2[1]), q.numerator, q.denominator])
            if sha(rows) != rec["selected_solution_sha256"]:
                raise AssertionError(f"selected solution digest drift: {channel}")
            if rec["selected_exact_substitution_checks"] != base["active_cell_count"]:
                raise AssertionError(f"selected substitution count drift: {channel}")
        else:
            if rec["selected_solution_coefficients"]:
                raise AssertionError(f"solution rows present without selected candidate: {channel}")
        reconstructed[channel] = {
            "ids": ids, "cols": cols, "target": target,
            "selected_uid": selected_uid, "selected_lift": selected_lift,
            "selected_solution_rows": rec["selected_solution_coefficients"],
        }

    if trial_count != 195 or result.get("independent_candidate_count") != 195:
        raise AssertionError("T3-011-A aggregate trial count drift")
    if result.get("independent_channel_with_survivor_count") != selected_count:
        raise AssertionError("T3-011-A selected-channel count drift")

    lbase, lids, lcols, ltarget = vc.reconstruct_channel(
        "l1", strata, specialized, supports
    )
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
        llift = lifted_global_column("l1", luid, strata, lactive)
        lbasis, _, _ = reverse_echelon_basis(lcols)
        ltres = reduce_reverse(ltarget, lbasis)
        lr, la, lcls = exact_classification(
            lbase["coefficient_rank"], len(lids), lbasis, ltres, llift
        )
        if (mirror.get("lift_coefficient_rank"), mirror.get("lift_augmented_rank"), mirror.get("lift_classification")) != (
            lr, la, lcls
        ):
            raise AssertionError("l1 independent lift rank drift")

        ksolution = parse_solution_rows(kdata["selected_solution_rows"])
        lsolution = {}
        klift_marker = f"__CHANNEL_LINEAR_{CHANNEL_COORDINATE['k1']}__"
        for uid, q in ksolution.items():
            scalar, mon = uid
            if mon and mon[0] == klift_marker:
                original = (scalar, mon[1:])
                mirrored_original = vc.mirror_unknown_k_to_l(original)
                lsolution[(mirrored_original[0], ("__CHANNEL_LINEAR_l__",) + mirrored_original[1])] = q
            else:
                lsolution[vc.mirror_unknown_k_to_l(uid)] = q
        lext = (luid[0], ("__CHANNEL_LINEAR_l__",) + luid[1])
        if set(lsolution) != set(lids) | {lext}:
            raise AssertionError("l1 mirrored solution support drift")
        mirror_ok = apply_solution(lids + [lext], lcols + [llift], lsolution) == ltarget
        if mirror.get("mirrored_k1_solution_exactly_satisfies_l1") != mirror_ok:
            raise AssertionError("l1 mirrored solution substitution drift")

    all_selected = selected_count == 4
    all_viable = all_selected and mirror_ok
    if result.get("all_independent_channels_have_canonical_single_lift") != all_selected:
        raise AssertionError("all-selected aggregate drift")
    if result.get("all_channels_and_mirror_viable") != all_viable:
        raise AssertionError("all-viable aggregate drift")
    expected_terminal = (
        "T3_011_A_COMPLETE__SINGLE_LINEAR_LIFT_CLASS_VIABLE__EXACT_RECOMBINATION_PENDING"
        if all_viable
        else "BOUNDED_SINGLE_CHANNEL_LINEAR_ZERO_RESPONSE_LIFT_CLASS_EXHAUSTED"
    )
    if result.get("terminal") != expected_terminal:
        raise AssertionError("T3-011-A terminal drift")

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
            raise AssertionError(f"T3-011-A claim-boundary inflation: {key}")

    return {
        "status": "INDEPENDENT_T3_011_A_COKERNEL_SINGLE_LIFT_REPLAY_COMPLETE",
        "independent_trial_count": trial_count,
        "independent_channel_with_survivor_count": selected_count,
        "all_channels_and_mirror_viable": all_viable,
        "independent_witness_support_count": independent_witness_support,
        "producer_matrix_imported_as_authority": False,
        "terminal": expected_terminal,
    }


def main() -> int:
    import t3_011_a as producer
    result = producer.build()
    print(json.dumps(verify(result), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
