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

import t3_010_a as a  # noqa: E402

OPERATION = "SYMMETRY_REDUCED_CHANNEL_HARMONIC_BLOCK_WITH_SHELL_STRATA_001"
STAGE = "T3_010_B_CORRECTION_FLUX_EXACT_COEFFICIENT_MATRIX_RANK_CONSISTENCY_GATE"
A_HEAD = "78186e06e3291b7b85d4d78e3a44218890f07dd9"
A_BLOBS = {
    "t3_010_a.py": "d5cdcecb4d0bbdd3e6b71f1df4340928e8ad402e",
    "T3_010_A_CONTRACT.json": "28f6617bca38a96eee3bbc9517874cd6fd07bb14",
}
BLOCK_ORDER = ("weight1", "weight2", "weight3", "weight4")


def canonical_sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def assert_a_locks() -> dict[str, str]:
    got: dict[str, str] = {}
    for name, want in A_BLOBS.items():
        sha = a.git_blob_sha1(HERE / name)
        if sha != want:
            raise AssertionError(f"T3-010-A source lock drift: {name}: {sha} != {want}")
        got[name] = sha
    contract = json.loads((HERE / "T3_010_A_CONTRACT.json").read_text())
    if contract["stage"] != a.STAGE:
        raise AssertionError("T3-010-A stage drift")
    if contract["next_gate"] != (
        "Declare bounded correction-flux unknown bases only for structurally active cells "
        "and compute exact coefficient-matrix rank/consistency before any elimination."
    ):
        raise AssertionError("T3-010-A successor gate drift")
    return got


def block_touches(mon: tuple[str, ...], block: str) -> bool:
    reps = set(a.WEIGHT_BLOCKS[block])
    return any(a.ORBIT_REP[x] in reps for x in mon)


def _const_poly(rat: a.rc.Rat) -> a.rc.Poly:
    return {(): rat} if rat else {}


def primitive_delta_atom(name: str, shift: tuple[int, int, int]) -> a.rc.Poly:
    """Exact shift increment for an oriented primitive harmonic letter.

    This is the local coefficient response generated when an exact correction
    weight is attached to one of the protected regularized flux families.  The
    protected H_{n-k}/H_{n-l} letters retain the pinv shell convention.
    """
    dn, dk, dl = shift
    if sum(int(x != 0) for x in shift) != 1:
        raise ValueError(f"unsupported compound correction shift {shift}")
    r = int(name.rsplit("_", 1)[1])

    if name.startswith("H_nmk_"):
        if dn:
            return _const_poly(a.pcl.sum_pinv([a.rc.lin_nmink(i) for i in range(1, dn + 1)], r))
        if dk:
            return _const_poly(a.rc.r_scale(a.pcl.pinv_factor(a.rc.lin_nmink(0), r), -1))
        return {}
    if name.startswith("H_nml_"):
        if dn:
            return _const_poly(a.pcl.sum_pinv([a.rc.lin_nminl(i) for i in range(1, dn + 1)], r))
        if dl:
            return _const_poly(a.rc.r_scale(a.pcl.pinv_factor(a.rc.lin_nminl(0), r), -1))
        return {}
    if name.startswith("H_nkl_"):
        if dn:
            return _const_poly(a.rc.sum_inv([a.rc.lin_nkl(i) for i in range(1, dn + 1)], r))
        if dk or dl:
            return _const_poly(a.rc.inv(a.rc.lin_nkl(1), r))
        return {}
    if name.startswith("H_nk_"):
        if dn:
            return _const_poly(a.rc.sum_inv([a.rc.lin_nk(i) for i in range(1, dn + 1)], r))
        if dk:
            return _const_poly(a.rc.inv(a.rc.lin_nk(1), r))
        return {}
    if name.startswith("H_nl_"):
        if dn:
            return _const_poly(a.rc.sum_inv([a.rc.lin_nl(i) for i in range(1, dn + 1)], r))
        if dl:
            return _const_poly(a.rc.inv(a.rc.lin_nl(1), r))
        return {}
    if name.startswith("H_kl_"):
        if dk or dl:
            return _const_poly(a.rc.inv(a.rc.lin_kl(1), r))
        return {}
    if name.startswith("H_k_"):
        if dk:
            return _const_poly(a.rc.inv(a.rc.lin_k(1), r))
        return {}
    if name.startswith("H_l_"):
        if dl:
            return _const_poly(a.rc.inv(a.rc.lin_l(1), r))
        return {}
    raise ValueError(f"unknown oriented primitive letter {name}")


def primitive_shift_atom(name: str, shift: tuple[int, int, int]) -> a.rc.Poly:
    return a.rc.p_add(a.rc.p_atom(name), primitive_delta_atom(name, shift))


def primitive_delta_monomial(mon: tuple[str, ...], shift: tuple[int, int, int]) -> a.rc.Poly:
    shifted = a.rc.p_const(1)
    original = a.rc.p_const(1)
    for name in mon:
        shifted = a.rc.p_mul(shifted, primitive_shift_atom(name, shift))
        original = a.rc.p_mul(original, a.rc.p_atom(name))
    return a.rc.p_add(shifted, a.rc.p_scale(original, -1))


def specialize_poly(poly: a.rc.Poly, k_offset: int | None, l_offset: int | None) -> a.rc.Poly:
    out: a.rc.Poly = {}
    for mon, rat in poly.items():
        sr = a.specialize_rat(rat, k_offset, l_offset)
        if sr:
            out[mon] = sr
    return out


def block_project_poly(poly: a.rc.Poly, block: str) -> a.rc.Poly:
    return {mon: rat for mon, rat in poly.items() if block_touches(mon, block)}


Coord = tuple[str, tuple[str, ...], a.rc.Sig]
Vector = dict[Coord, Q]


def coord_sort_key(coord: Coord) -> str:
    return repr(coord)


def forcing_vector(layer: a.pcl.Layer, channel: str, block: str) -> Vector:
    out: Vector = {}
    allowed = set(a.CHANNEL_SCALARS[channel])
    for mon, by_scalar in layer.items():
        if not block_touches(mon, block):
            continue
        for scalar, rat in by_scalar.items():
            if scalar not in allowed:
                continue
            for sig, coeff in rat.items():
                coord = (scalar, mon, sig)
                out[coord] = out.get(coord, Q(0)) + coeff
                if out[coord] == 0:
                    del out[coord]
    return out


def response_vector(poly: a.rc.Poly, scalar: str, block: str) -> Vector:
    out: Vector = {}
    for mon, rat in block_project_poly(poly, block).items():
        for sig, coeff in rat.items():
            coord = (scalar, mon, sig)
            out[coord] = out.get(coord, Q(0)) + coeff
            if out[coord] == 0:
                del out[coord]
    return out


def _factor_json(factor: tuple[int, ...]) -> list[int]:
    return [int(x) for x in factor]


def _coord_json(coord: Coord):
    scalar, mon, sig = coord
    return [scalar, list(mon), [[_factor_json(f), int(e)] for f, e in sig]]


def vector_digest(vec: Vector) -> str:
    rows = []
    for coord in sorted(vec, key=coord_sort_key):
        c = vec[coord]
        rows.append([_coord_json(coord), c.numerator, c.denominator])
    return canonical_sha(rows)


def column_bundle_digest(column_ids: list[tuple[str, tuple[str, ...]]], columns: list[Vector]) -> str:
    rows = []
    for (scalar, mon), vec in zip(column_ids, columns):
        rows.append([scalar, list(mon), vector_digest(vec)])
    return canonical_sha(rows)


def rank_sparse(vectors: list[Vector], reverse: bool = False) -> tuple[int, list[Coord]]:
    """Exact Q-rank by deterministic sparse Gaussian elimination on columns."""
    basis: dict[Coord, Vector] = {}
    pivots: list[Coord] = []
    for source in vectors:
        v = {k: Q(c) for k, c in source.items() if c}
        while v:
            pivot = (max if reverse else min)(v, key=coord_sort_key)
            if pivot in basis:
                factor = v[pivot]
                b = basis[pivot]
                for coord, coeff in b.items():
                    z = v.get(coord, Q(0)) - factor * coeff
                    if z:
                        v[coord] = z
                    elif coord in v:
                        del v[coord]
                continue
            p = v[pivot]
            v = {coord: coeff / p for coord, coeff in v.items() if coeff}
            basis[pivot] = v
            pivots.append(pivot)
            break
    return len(basis), pivots


def classify(rank: int, augmented_rank: int, unknowns: int) -> str:
    if augmented_rank > rank:
        return "EXACTLY_INCONSISTENT"
    if rank == unknowns:
        return "CONSISTENT_UNIQUE"
    return "CONSISTENT_AFFINE"


def candidate_support(primitive_full: a.pcl.Layer, channel: str, block: str) -> dict[str, list[tuple[str, ...]]]:
    out: dict[str, list[tuple[str, ...]]] = {}
    for scalar in a.CHANNEL_SCALARS[channel]:
        mons = [
            mon for mon, by_scalar in primitive_full.items()
            if scalar in by_scalar and block_touches(mon, block)
        ]
        out[scalar] = sorted(set(mons))
    return out


def analyze_cell(
    primitive_specialized: a.pcl.Layer,
    supports: dict[str, list[tuple[str, ...]]],
    channel: str,
    block: str,
    stratum: dict,
) -> tuple[dict, Vector, list[Vector], list[tuple[str, tuple[str, ...]]]]:
    target = forcing_vector(primitive_specialized, channel, block)
    cell_id = f"{channel}:{block}:{stratum['id']}"
    if not target:
        return ({
            "id": cell_id,
            "channel": channel,
            "block": block,
            "stratum": stratum["id"],
            "status": "SKIPPED_STRUCTURAL_ZERO",
            "unknowns": 0,
            "coefficient_rank": 0,
            "augmented_rank": 0,
            "nullity": 0,
            "classification": "STRUCTURAL_ZERO",
            "target_coordinate_count": 0,
            "matrix_coordinate_count": 0,
            "zero_response_columns": 0,
            "candidate_support_sha256": canonical_sha([]),
            "coefficient_matrix_sha256": canonical_sha([]),
            "target_sha256": vector_digest({}),
            "rank_pivot_sha256": canonical_sha([]),
            "solution_extraction_admitted": False,
        }, target, [], [])

    shift = a.pcl.SHIFTS[channel]
    columns: list[Vector] = []
    column_ids: list[tuple[str, tuple[str, ...]]] = []
    support_rows = []
    for scalar in a.CHANNEL_SCALARS[channel]:
        for mon in supports[scalar]:
            delta = primitive_delta_monomial(mon, shift)
            delta = specialize_poly(delta, stratum["k_offset"], stratum["l_offset"])
            vec = response_vector(delta, scalar, block)
            columns.append(vec)
            column_ids.append((scalar, mon))
            support_rows.append([scalar, list(mon)])

    rank, pivots = rank_sparse(columns)
    augmented_rank, _ = rank_sparse(columns + [target])
    unknowns = len(columns)
    cls = classify(rank, augmented_rank, unknowns)
    coords = set(target)
    for col in columns:
        coords.update(col)
    record = {
        "id": cell_id,
        "channel": channel,
        "block": block,
        "stratum": stratum["id"],
        "status": "EXACT_CORRECTION_MATRIX_CLASSIFIED",
        "unknowns": unknowns,
        "coefficient_rank": rank,
        "augmented_rank": augmented_rank,
        "nullity": unknowns - rank,
        "classification": cls,
        "target_coordinate_count": len(target),
        "matrix_coordinate_count": len(coords),
        "zero_response_columns": sum(not x for x in columns),
        "candidate_support_sha256": canonical_sha(support_rows),
        "coefficient_matrix_sha256": column_bundle_digest(column_ids, columns),
        "target_sha256": vector_digest(target),
        "rank_pivot_sha256": canonical_sha([_coord_json(x) for x in pivots]),
        "rank_field": "Q",
        "solution_extraction_admitted": False,
    }
    return record, target, columns, column_ids


def mirror_letter(name: str) -> str:
    swaps = (
        ("H_nmk_", "H_nml_"), ("H_nml_", "H_nmk_"),
        ("H_nk_", "H_nl_"), ("H_nl_", "H_nk_"),
        ("H_k_", "H_l_"), ("H_l_", "H_k_"),
    )
    for left, right in swaps:
        if name.startswith(left):
            return right + name[len(left):]
    return name


def mirror_sig(sig: a.rc.Sig) -> a.rc.Sig:
    powers: dict[tuple[int, ...], int] = {}
    for factor, exponent in sig:
        if len(factor) == 5 and factor[0] == a.pcl.PINV_TAG:
            tag, aa, b, c, d = factor
            mf = (tag, aa, c, b, d)
        else:
            aa, b, c, d = factor
            mf = (aa, c, b, d)
        powers[mf] = powers.get(mf, 0) + exponent
        if powers[mf] == 0:
            del powers[mf]
    return tuple(sorted(powers.items()))


def mirror_coord_l_to_k(coord: Coord) -> Coord:
    scalar, mon, sig = coord
    inverse_scalar = {v: k for k, v in a.MIRROR_SCALAR.items()}
    if scalar not in inverse_scalar:
        raise AssertionError(f"unexpected l1 scalar in B mirror: {scalar}")
    return (
        inverse_scalar[scalar],
        tuple(sorted(mirror_letter(x) for x in mon)),
        mirror_sig(sig),
    )


def mirror_vector_l_to_k(vec: Vector) -> Vector:
    out: Vector = {}
    for coord, coeff in vec.items():
        mc = mirror_coord_l_to_k(coord)
        out[mc] = out.get(mc, Q(0)) + coeff
        if out[mc] == 0:
            del out[mc]
    return out


def mirror_column_id_l_to_k(item: tuple[str, tuple[str, ...]]) -> tuple[str, tuple[str, ...]]:
    scalar, mon = item
    inverse_scalar = {v: k for k, v in a.MIRROR_SCALAR.items()}
    return inverse_scalar[scalar], tuple(sorted(mirror_letter(x) for x in mon))


def verify_l1_matrix_mirror(
    k_target: Vector,
    k_columns: list[Vector],
    k_ids: list[tuple[str, tuple[str, ...]]],
    l_target: Vector,
    l_columns: list[Vector],
    l_ids: list[tuple[str, tuple[str, ...]]],
) -> dict:
    mt = mirror_vector_l_to_k(l_target)
    if mt != k_target:
        raise AssertionError("T3-010-B exact target mirror drift")
    normalized_l = {
        mirror_column_id_l_to_k(cid): mirror_vector_l_to_k(vec)
        for cid, vec in zip(l_ids, l_columns)
    }
    kmap = {cid: vec for cid, vec in zip(k_ids, k_columns)}
    if normalized_l != kmap:
        raise AssertionError("T3-010-B exact correction-matrix mirror drift")
    return {
        "target_sha256": vector_digest(k_target),
        "coefficient_matrix_sha256": column_bundle_digest(k_ids, k_columns),
        "exact_equal_after_k_l_mirror": True,
    }


def build() -> dict:
    a_locks = assert_a_locks()
    a.assert_source_locks()
    a.validate_architecture()
    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 coefficient-layer digest drift in B")

    primitive_full = a.primitive_oriented_layer(layer)
    strata = a.shell_strata()
    specialized = {
        st["id"]: a.primitive_oriented_layer(
            a.specialize_layer(layer, st["k_offset"], st["l_offset"])
        )
        for st in strata
    }
    supports = {
        (channel, block): candidate_support(primitive_full, channel, block)
        for channel in a.CHANNEL_SCALARS
        for block in BLOCK_ORDER
    }

    cells: list[dict] = []
    mirror_cells: list[dict] = []
    mirror_checks = 0
    probe_active = 0

    for st in strata:
        primitive = specialized[st["id"]]
        for channel in a.INDEPENDENT_CHANNELS:
            for block in BLOCK_ORDER:
                probe = a.support_probe(primitive, channel, block, st["id"])
                record, target, columns, ids = analyze_cell(
                    primitive, supports[(channel, block)], channel, block, st
                )
                active = record["classification"] != "STRUCTURAL_ZERO"
                if active != (probe["status"] == "STRUCTURALLY_ACTIVE_FORCING_SUPPORT"):
                    raise AssertionError(f"A/B structural activity drift: {record['id']}")
                if active:
                    probe_active += 1
                cells.append(record)

                if channel == "k1":
                    mirror_st = next(x for x in strata if x["id"] == st["mirror"])
                    lprimitive = specialized[mirror_st["id"]]
                    lrecord, ltarget, lcolumns, lids = analyze_cell(
                        lprimitive, supports[("l1", block)], "l1", block, mirror_st
                    )
                    if active != (lrecord["classification"] != "STRUCTURAL_ZERO"):
                        raise AssertionError("k1/l1 structural activity mirror drift in B")
                    witness = verify_l1_matrix_mirror(
                        target, columns, ids, ltarget, lcolumns, lids
                    )
                    if active:
                        if (
                            record["coefficient_rank"] != lrecord["coefficient_rank"]
                            or record["augmented_rank"] != lrecord["augmented_rank"]
                            or record["classification"] != lrecord["classification"]
                        ):
                            raise AssertionError("k1/l1 exact rank classification mirror drift")
                    mirror_cells.append({
                        "id": f"l1:{block}:{mirror_st['id']}",
                        "derived_from": record["id"],
                        "block": block,
                        "stratum": mirror_st["id"],
                        "classification": lrecord["classification"],
                        "coefficient_rank": lrecord["coefficient_rank"],
                        "augmented_rank": lrecord["augmented_rank"],
                        "exact_matrix_mirror": witness["exact_equal_after_k_l_mirror"],
                    })
                    mirror_checks += 1

    if len(cells) != 400 or len(mirror_cells) != 100 or mirror_checks != 100:
        raise AssertionError("T3-010-B cell cardinality drift")

    active = [x for x in cells if x["classification"] != "STRUCTURAL_ZERO"]
    if len(active) != probe_active:
        raise AssertionError("T3-010-B active-cell count drift")
    class_hist: dict[str, int] = {}
    for cell in cells:
        key = cell["classification"]
        class_hist[key] = class_hist.get(key, 0) + 1
    viable = [x for x in active if x["classification"].startswith("CONSISTENT_")]
    inconsistent = [x for x in active if x["classification"] == "EXACTLY_INCONSISTENT"]

    terminal = (
        "T3_010_B_COMPLETE__BOUNDED_EXACT_SOLUTION_EXTRACTION_PENDING"
        if viable
        else "BOUNDED_SUPPORT_LOCKED_DEGREE0_CORRECTION_CLASS_EXHAUSTED"
    )
    return {
        "schema_version": "1.0.0",
        "issue": 403,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "EXACT_CORRECTION_FLUX_COEFFICIENT_MATRIX_RANK_CONSISTENCY_GATE_COMPLETE",
        "t3_010_a_checkpoint": {
            "validated_head": A_HEAD,
            "source_blobs": a_locks,
            "terminal": "T3_010_A_COMPLETE__CORRECTION_FLUX_MATRIX_RANK_GATE_PENDING",
        },
        "mathematical_predecessor": {
            "protected_merge": a.PREDECESSOR_MERGE,
            "tree": a.PREDECESSOR_TREE,
            "coefficient_layer_sha256": a.PREDECESSOR_LAYER_SHA256,
        },
        "correction_class": {
            "id": "SUPPORT_LOCKED_ORIENTED_ONE_BODY_DEGREE0_WEIGHT_CORRECTION_001",
            "coefficient_field": "Q",
            "candidate_weights": "For each scalar family, use exactly the oriented primitive one-body monomials already present in that scalar's protected T3-009 coefficient support and touching the selected harmonic block.",
            "coefficient_degree": 0,
            "new_harmonic_monomials_admitted": False,
            "generic_198_raw_jet_reopened": False,
            "local_response": "For a candidate correction weight G attached to a protected regularized flux family, use the exact shifted-scalar product-rule coefficient Delta_channel(G)=G(shift)-G. Construct this before shell specialization and then apply the exact protected pinv stratum restriction.",
            "block_projection": "Each 5+4+2+2 block is a local necessary projection: retain coefficient coordinates whose oriented primitive monomial touches that block. Cross-block leakage and shared-coefficient compatibility are deferred to bounded exact solution extraction and full recombination.",
            "interpretation": "Exact inconsistency rules out this declared local correction class for that cell. Exact consistency is viability only; it is not a correction certificate until shared coefficients are extracted and the complete flux identity is symbolically substituted and recombined.",
        },
        "rank_criterion": {
            "matrix": "A_c x = b_c over exact Q coefficient coordinates (scalar, oriented primitive monomial, affine-Laurent signature)",
            "coefficient_rank": "rank_Q(A_c)",
            "augmented_rank": "rank_Q([A_c|b_c])",
            "inconsistent": "augmented_rank > coefficient_rank",
            "consistent_unique": "augmented_rank = coefficient_rank = unknowns",
            "consistent_affine": "augmented_rank = coefficient_rank < unknowns",
            "floating_point_used": False,
            "modular_rank_used": False,
            "sampled_rank_used": False,
        },
        "independent_cell_count": 400,
        "mirrored_l1_cell_count": 100,
        "active_cell_count": len(active),
        "structural_zero_cell_count": len(cells) - len(active),
        "viable_cell_count": len(viable),
        "inconsistent_cell_count": len(inconsistent),
        "classification_histogram": dict(sorted(class_hist.items())),
        "matrix_cells": cells,
        "mirrored_l1_cells": mirror_cells,
        "exact_k1_l1_matrix_mirror_checks": mirror_checks,
        "solution_coefficients_extracted": False,
        "full_correction_layer_recombined": False,
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
