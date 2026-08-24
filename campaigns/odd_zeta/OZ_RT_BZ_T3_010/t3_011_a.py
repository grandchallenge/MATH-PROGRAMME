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

import t3_010_c as c  # noqa: E402

b = c.b
a = b.a

OPERATION = "OZ-RT-BZ-T3-011-A"
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
GlobalCoord = c.GlobalCoord
GlobalVector = c.GlobalVector


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid: Unknown) -> list:
    return [uid[0], list(uid[1])]


def assert_c_locks() -> dict[str, str]:
    got: dict[str, str] = {}
    for name, want in C_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"T3-010-C source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_010_C_CONTRACT.json").read_text())
    if contract["stage"] != c.STAGE:
        raise AssertionError("T3-010-C stage drift")
    if contract["bounded_correction_class"]["id"] != (
        "SUPPORT_LOCKED_ORIENTED_ONE_BODY_DEGREE0_WEIGHT_CORRECTION_001"
    ):
        raise AssertionError("T3-010-C bounded class drift")
    if contract["bounded_correction_class"]["coefficient_degree"] != 0:
        raise AssertionError("T3-010-C degree drift")
    return got


def add_scaled(dst: dict, src: dict, factor: Q) -> None:
    if not factor:
        return
    for key, value in src.items():
        z = dst.get(key, Q(0)) + factor * value
        if z:
            dst[key] = z
        elif key in dst:
            del dst[key]


def pairing(functional: dict[GlobalCoord, Q], vector: GlobalVector) -> Q:
    return sum((q * vector.get(coord, Q(0)) for coord, q in functional.items()), Q(0))


def echelon_basis(cols: list[GlobalVector]) -> tuple[dict[GlobalCoord, GlobalVector], list[int], list[GlobalCoord]]:
    """Deterministic exact column echelon basis with smallest-coordinate pivots."""
    basis: dict[GlobalCoord, GlobalVector] = {}
    selected: list[int] = []
    pivots: list[GlobalCoord] = []
    for idx, source in enumerate(cols):
        v: GlobalVector = {k: Q(q) for k, q in source.items() if q}
        while v:
            pivot = min(v, key=c.gkey)
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


def reduce_vector(vector: GlobalVector, basis: dict[GlobalCoord, GlobalVector]) -> GlobalVector:
    v: GlobalVector = {k: Q(q) for k, q in vector.items() if q}
    for pivot in sorted(basis, key=c.gkey):
        if pivot in v:
            add_scaled(v, basis[pivot], -v[pivot])
    return v


def solve_square(matrix: list[list[Q]], rhs: list[Q]) -> list[Q]:
    n = len(matrix)
    if len(rhs) != n or any(len(row) != n for row in matrix):
        raise ValueError("square solve shape drift")
    aug = [[Q(x) for x in row] + [Q(rhs[i])] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col]), None)
        if pivot is None:
            raise AssertionError("singular canonical pivot matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r == col or not aug[r][col]:
                continue
            factor = aug[r][col]
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    return [aug[i][-1] for i in range(n)]


def cokernel_witness(cols: list[GlobalVector], target: GlobalVector) -> tuple[dict[GlobalCoord, Q], GlobalVector]:
    basis, selected, pivots = echelon_basis(cols)
    if len(selected) != b.rank_sparse(cols)[0]:
        raise AssertionError("base rank/echelon drift")
    r = len(selected)
    if not r:
        coord = min(target, key=c.gkey)
        witness = {coord: Q(1, 1) / target[coord]}
        return witness, dict(target)

    matrix = [[cols[j].get(p, Q(0)) for j in selected] for p in pivots]
    alpha = solve_square(matrix, [target.get(p, Q(0)) for p in pivots])
    residual: GlobalVector = {k: Q(q) for k, q in target.items() if q}
    for coeff, j in zip(alpha, selected):
        add_scaled(residual, cols[j], -coeff)
    for p in pivots:
        if residual.get(p, Q(0)):
            raise AssertionError("target projection did not vanish on pivot rows")
    if not residual:
        raise AssertionError("C target unexpectedly entered degree-zero span")
    qcoord = min(residual, key=c.gkey)

    transpose = [[matrix[row][col] for row in range(r)] for col in range(r)]
    qrow = [cols[j].get(qcoord, Q(0)) for j in selected]
    gamma = solve_square(transpose, [-x for x in qrow])
    witness: dict[GlobalCoord, Q] = {qcoord: Q(1)}
    for p, coeff in zip(pivots, gamma):
        if coeff:
            witness[p] = witness.get(p, Q(0)) + coeff
            if not witness[p]:
                del witness[p]

    for col in cols:
        if pairing(witness, col):
            raise AssertionError("cokernel witness does not annihilate C matrix")
    value = pairing(witness, target)
    if not value:
        raise AssertionError("cokernel witness misses inconsistent target")
    witness = {k: q / value for k, q in witness.items() if q}
    if pairing(witness, target) != 1:
        raise AssertionError("cokernel witness normalization drift")
    return witness, residual


def witness_rows(witness: dict[GlobalCoord, Q]) -> list[list]:
    rows = []
    for (cell_id, coord) in sorted(witness, key=c.gkey):
        q = witness[(cell_id, coord)]
        rows.append([cell_id, b._coord_json(coord), q.numerator, q.denominator])
    return rows


def channel_coordinate_factors(channel: str):
    if channel in ("n1", "n2", "n3"):
        step = CHANNEL_INCREMENT[channel]
        return (1, 0, 0, 0), (1, 0, 0, step)
    if channel == "k1":
        return (0, 1, 0, 0), (0, 1, 0, 1)
    if channel == "l1":
        return (0, 0, 1, 0), (0, 0, 1, 1)
    raise ValueError(channel)


def monomial_poly(mon: tuple[str, ...]) -> a.rc.Poly:
    out = a.rc.p_const(1)
    for name in mon:
        out = a.rc.p_mul(out, a.rc.p_atom(name))
    return out


def shifted_monomial_poly(mon: tuple[str, ...], shift: tuple[int, int, int]) -> a.rc.Poly:
    out = a.rc.p_const(1)
    for name in mon:
        out = a.rc.p_mul(out, b.primitive_shift_atom(name, shift))
    return out


def lifted_delta_monomial(mon: tuple[str, ...], channel: str) -> a.rc.Poly:
    shift = a.pcl.SHIFTS[channel]
    f0, f1 = channel_coordinate_factors(channel)
    shifted = shifted_monomial_poly(mon, shift)
    original = monomial_poly(mon)
    return a.rc.p_add(
        a.rc.p_scale(shifted, a.rc.r_factor(f1, exponent=1)),
        a.rc.p_scale(original, a.rc.r_factor(f0, exponent=1, scale=-1)),
    )


def lifted_global_column(
    channel: str,
    uid: Unknown,
    strata: list[dict],
    active_cell_ids: set[str],
) -> GlobalVector:
    scalar, mon = uid
    raw = lifted_delta_monomial(mon, channel)
    out: GlobalVector = {}
    for st in strata:
        specialized = b.specialize_poly(raw, st["k_offset"], st["l_offset"])
        for block in c.BLOCK_ORDER:
            cell_id = f"{channel}:{block}:{st['id']}"
            if cell_id not in active_cell_ids:
                continue
            local = b.response_vector(specialized, scalar, block)
            for coord, q in local.items():
                key = (cell_id, coord)
                z = out.get(key, Q(0)) + q
                if z:
                    out[key] = z
                elif key in out:
                    del out[key]
    return out


def proportional(a_vec: GlobalVector, b_vec: GlobalVector) -> Q | None:
    """Return q with a_vec = q*b_vec, else None. Empty vectors handled exactly."""
    if not a_vec and not b_vec:
        return Q(1)
    if not a_vec or not b_vec:
        return None
    keys = sorted(set(a_vec).union(b_vec), key=c.gkey)
    pivot = next((k for k in keys if b_vec.get(k, Q(0))), None)
    if pivot is None:
        return None
    q = a_vec.get(pivot, Q(0)) / b_vec[pivot]
    for key in keys:
        if a_vec.get(key, Q(0)) != q * b_vec.get(key, Q(0)):
            return None
    return q


def lift_unknown(uid: Unknown, channel: str) -> Unknown:
    return (uid[0], (f"__CHANNEL_LINEAR_{CHANNEL_COORDINATE[channel]}__",) + uid[1])


def solution_digest(ids: list[Unknown], solution: dict[Unknown, Q]) -> str:
    rows = []
    for uid in ids:
        q = solution.get(uid, Q(0))
        rows.append([uid[0], list(uid[1]), q.numerator, q.denominator])
    return sha(rows)


def candidate_record(
    channel: str,
    uid: Unknown,
    lift_col: GlobalVector,
    witness: dict[GlobalCoord, Q],
    basis: dict[GlobalCoord, GlobalVector],
    target_residual: GlobalVector,
    base_rank: int,
    base_unknown_count: int,
) -> dict:
    obstruction = pairing(witness, lift_col)
    lift_residual = reduce_vector(lift_col, basis)
    quotient_ratio = proportional(target_residual, lift_residual)
    rank = base_rank + (1 if lift_residual else 0)
    if quotient_ratio is not None and lift_residual:
        augmented_rank = rank
        classification = "CONSISTENT_AFFINE" if rank < base_unknown_count + 1 else "CONSISTENT_UNIQUE"
    else:
        quotient_rank = 1 if not lift_residual else 2
        augmented_rank = base_rank + quotient_rank
        classification = "EXACTLY_INCONSISTENT"

    if obstruction == 0 and classification != "EXACTLY_INCONSISTENT":
        raise AssertionError("zero cokernel pairing cannot remove witnessed inconsistency")

    return {
        "candidate": unknown_json(uid),
        "lift_coordinate": CHANNEL_COORDINATE[channel],
        "lift_increment": CHANNEL_INCREMENT[channel],
        "obstruction_pairing": qjson(obstruction),
        "obstruction_pairing_nonzero": obstruction != 0,
        "lift_response_coordinate_count": len(lift_col),
        "lift_response_sha256": c.global_vector_digest(lift_col),
        "lift_quotient_residual_coordinate_count": len(lift_residual),
        "lift_quotient_residual_sha256": c.global_vector_digest(lift_residual),
        "exact_rank_test_run": obstruction != 0,
        "coefficient_rank": rank if obstruction != 0 else None,
        "augmented_rank": augmented_rank if obstruction != 0 else None,
        "classification": classification if obstruction != 0 else "REJECTED_BY_COKERNEL_WITNESS",
        "rank_consistent": obstruction != 0 and classification.startswith("CONSISTENT_"),
        "exact_solution_exists": False,
        "exact_substitution_checks": 0,
        "canonical_solution_sha256": None,
    }


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
        raise AssertionError(f"T3-011-A requires inconsistent C base: {channel}")
    zero_items = [(i, uid) for i, (uid, col) in enumerate(zip(ids, cols)) if not col]
    if len(zero_items) != EXPECTED_ZERO_COUNTS[channel]:
        raise AssertionError(f"zero-response candidate count drift in {channel}")

    basis, _, _ = echelon_basis(cols)
    if len(basis) != base["coefficient_rank"]:
        raise AssertionError(f"base echelon rank drift in {channel}")
    target_residual = reduce_vector(target, basis)
    if not target_residual:
        raise AssertionError(f"inconsistent target residual vanished in {channel}")
    witness, witness_projection_residual = cokernel_witness(cols, target)
    if not witness_projection_residual:
        raise AssertionError("witness projection residual unexpectedly empty")

    active_ids = {x["id"] for x in base["active_cells"]}
    trials = []
    survivors = []
    survivor_payloads: dict[str, tuple[Unknown, GlobalVector, dict[Unknown, Q]]] = {}
    for _, uid in zero_items:
        lift_col = lifted_global_column(channel, uid, strata, active_ids)
        rec = candidate_record(
            channel, uid, lift_col, witness, basis, target_residual,
            base["coefficient_rank"], len(ids)
        )
        if rec["rank_consistent"]:
            ext_uid = lift_unknown(uid, channel)
            ext_ids = ids + [ext_uid]
            ext_cols = cols + [lift_col]
            solution = c.exact_particular_solution(ext_ids, ext_cols, target)
            if solution is None:
                raise AssertionError(f"rank-consistent lift solver failure in {channel}:{uid}")
            if c.apply_solution(ext_ids, ext_cols, solution) != target:
                raise AssertionError(f"lift exact substitution failure in {channel}:{uid}")
            rec["exact_solution_exists"] = True
            rec["exact_substitution_checks"] = base["active_cell_count"]
            rec["canonical_solution_sha256"] = solution_digest(ext_ids, solution)
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
        selected_solution_sha = solution_digest(ext_ids, selected_solution)
        selected_lift_response_sha = c.global_vector_digest(selected_lift_col)
        for uid in ext_ids:
            q = selected_solution.get(uid, Q(0))
            selected_solution_rows.append(
                [uid[0], list(uid[1]), q.numerator, q.denominator]
            )

    record = {
        "channel": channel,
        "base_unknown_count": len(ids),
        "base_coefficient_rank": base["coefficient_rank"],
        "base_augmented_rank": base["augmented_rank"],
        "base_nullity": base["nullity"],
        "base_zero_global_columns": base["zero_global_columns"],
        "active_cell_count": base["active_cell_count"],
        "candidate_count": len(zero_items),
        "cokernel_witness_support_count": len(witness),
        "cokernel_witness_sha256": sha(witness_rows(witness)),
        "cokernel_witness_rows": witness_rows(witness),
        "cokernel_target_pairing": qjson(pairing(witness, target)),
        "target_quotient_residual_sha256": c.global_vector_digest(target_residual),
        "nonzero_obstruction_pairing_candidate_count": sum(
            x["obstruction_pairing_nonzero"] for x in trials
        ),
        "rank_consistent_candidate_count": len(survivors),
        "trials": trials,
        "canonical_selected_candidate": unknown_json(selected) if selected else None,
        "selected_lift_response_sha256": selected_lift_response_sha,
        "selected_solution_sha256": selected_solution_sha,
        "selected_solution_coefficients": selected_solution_rows,
        "selected_exact_substitution_checks": (
            base["active_cell_count"] if selected is not None else 0
        ),
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
    c_locks = assert_c_locks()
    c.assert_b_locks()
    b.assert_a_locks()
    a.assert_source_locks()
    a.validate_architecture()

    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 coefficient-layer digest drift in T3-011-A")
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
        rec, internal = build_channel(
            channel, primitive_full, strata, specialized, supports
        )
        channels.append(rec)
        internals[channel] = internal

    if sum(x["candidate_count"] for x in channels) != 195:
        raise AssertionError("T3-011-A independent candidate bank drift")

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
        llift = lifted_global_column("l1", luid, strata, lactive)
        lrank, _ = b.rank_sparse(lcols + [llift])
        laug, _ = b.rank_sparse(lcols + [llift, ltarget])
        lcls = b.classify(lrank, laug, len(lids) + 1)
        mirror_record.update({
            "canonical_mirrored_candidate": unknown_json(luid),
            "lift_coefficient_rank": lrank,
            "lift_augmented_rank": laug,
            "lift_classification": lcls,
        })

        if kint["selected_solution"] is not None:
            ksol = kint["selected_solution"]
            lsol: dict[Unknown, Q] = {}
            for uid in kint["ids"]:
                lsol[c.mirror_unknown_k_to_l(uid)] = ksol.get(uid, Q(0))
            lext_uid = lift_unknown(luid, "l1")
            lsol[lext_uid] = ksol.get(kint["selected_ext_uid"], Q(0))
            if set(lsol) != set(lids) | {lext_uid}:
                raise AssertionError("mirrored selected solution support drift")
            if c.apply_solution(lids + [lext_uid], lcols + [llift], lsol) == ltarget:
                mirror_record["mirrored_k1_solution_exactly_satisfies_l1"] = True

    all_selected = all(x["canonical_selected_candidate"] is not None for x in channels)
    mirror_ok = mirror_record["mirrored_k1_solution_exactly_satisfies_l1"]
    all_viable = all_selected and mirror_ok
    terminal = (
        "T3_011_A_COMPLETE__SINGLE_LINEAR_LIFT_CLASS_VIABLE__EXACT_RECOMBINATION_PENDING"
        if all_viable
        else "BOUNDED_SINGLE_CHANNEL_LINEAR_ZERO_RESPONSE_LIFT_CLASS_EXHAUSTED"
    )

    return {
        "schema_version": "1.0.0",
        "issue": 444,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "EXACT_COKERNEL_GUIDED_SINGLE_CHANNEL_LINEAR_ZERO_RESPONSE_LIFT_GATE_COMPLETE",
        "t3_010_c_checkpoint": {
            "validated_head": C_HEAD,
            "source_blobs": c_locks,
            "required_terminal": "BOUNDED_SUPPORT_LOCKED_DEGREE0_CORRECTION_CLASS_GLOBALLY_INCOMPATIBLE",
        },
        "bounded_correction_class": {
            "id": CLASS_ID,
            "base_class": "SUPPORT_LOCKED_ORIENTED_ONE_BODY_DEGREE0_WEIGHT_CORRECTION_001",
            "candidate_bank": "complete-global-response-zero C unknowns only",
            "independent_trial_count": 195,
            "one_lift_per_trial": True,
            "new_harmonic_monomials": False,
            "full_degree1_envelope": False,
            "rational_prefactor_search": False,
            "adaptive_basis_growth": False,
            "generic_198_raw_jet_reopened": False,
        },
        "channel_systems": channels,
        "independent_candidate_count": sum(x["candidate_count"] for x in channels),
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
