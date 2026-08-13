#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_c as semantic  # noqa: E402
import t3_011_d as producer  # noqa: E402
import verify_t3_011_b as predecessor_verifier  # noqa: E402

va = predecessor_verifier.va
vc = predecessor_verifier.vc
vb = predecessor_verifier.vb
a = predecessor_verifier.a
c = producer.c
p = producer.p


def quadratic_product_rule_poly(mon: tuple[str, ...], channel: str):
    shift = a.pcl.SHIFTS[channel]
    h = producer.CHANNEL_INCREMENT[channel]
    original = semantic.direct_original_monomial(mon)
    shifted = semantic.direct_shifted_monomial(mon, shift)
    delta_g = a.rc.p_add(shifted, a.rc.p_scale(original, -1))
    x = semantic.direct_coordinate_rat(channel)
    x2 = a.rc.r_factor(semantic.coordinate_factor(channel), exponent=2)
    correction = a.rc.r_add(a.rc.r_scale(x, 2 * h), a.rc.r_const(h * h))
    return a.rc.p_add(
        a.rc.p_scale(delta_g, x2),
        a.rc.p_scale(shifted, correction),
    )


def verifier_global_column(channel, uid, strata, active):
    scalar, mon = uid
    raw = quadratic_product_rule_poly(mon, channel)
    return semantic.direct_global_column_from_poly(raw, scalar, channel, strata, active)


def _add_scaled(dst: dict, src: dict, factor: Q) -> None:
    if not factor:
        return
    for key, value in src.items():
        z = dst.get(key, Q(0)) + factor * value
        if z:
            dst[key] = z
        elif key in dst:
            del dst[key]


def _forward_echelon(cols: list[dict]):
    basis = {}
    selected = []
    pivots = []
    for idx, source in enumerate(cols):
        vec = {k: Q(q) for k, q in source.items() if q}
        while vec:
            pivot = min(vec, key=va.gkey)
            if pivot in basis:
                _add_scaled(vec, basis[pivot], -vec[pivot])
                continue
            scale = vec[pivot]
            vec = {k: q / scale for k, q in vec.items() if q}
            basis[pivot] = vec
            selected.append(idx)
            pivots.append(pivot)
            break
    return basis, selected, pivots


def _solve_square_forward(matrix: list[list[Q]], rhs: list[Q]) -> list[Q]:
    n = len(matrix)
    if len(rhs) != n or any(len(row) != n for row in matrix):
        raise ValueError("forward square solve shape drift")
    aug = [[Q(x) for x in row] + [Q(rhs[i])] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col]), None)
        if pivot is None:
            raise AssertionError("singular forward canonical pivot matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for row in range(n):
            if row == col or not aug[row][col]:
                continue
            factor = aug[row][col]
            aug[row] = [x - factor * y for x, y in zip(aug[row], aug[col])]
    return [aug[i][-1] for i in range(n)]


def frozen_canonical_witness(cols: list[dict], target: dict) -> dict:
    """Independently reproduce the predecessor's smallest-coordinate normalized witness."""
    basis, selected, pivots = _forward_echelon(cols)
    rank = vb.rank_reverse(cols)
    if len(selected) != rank:
        raise AssertionError("forward frozen witness rank drift")
    if not selected:
        qcoord = min(target, key=va.gkey)
        return {qcoord: Q(1) / target[qcoord]}

    matrix = [[cols[j].get(pivot, Q(0)) for j in selected] for pivot in pivots]
    alpha = _solve_square_forward(matrix, [target.get(pivot, Q(0)) for pivot in pivots])
    residual = {k: Q(q) for k, q in target.items() if q}
    for coeff, j in zip(alpha, selected):
        _add_scaled(residual, cols[j], -coeff)
    for pivot in pivots:
        if residual.get(pivot, Q(0)):
            raise AssertionError("frozen witness target projection pivot drift")
    if not residual:
        raise AssertionError("frozen witness target unexpectedly entered base span")
    qcoord = min(residual, key=va.gkey)

    transpose = [[matrix[row][col] for row in range(len(selected))] for col in range(len(selected))]
    qrow = [cols[j].get(qcoord, Q(0)) for j in selected]
    gamma = _solve_square_forward(transpose, [-x for x in qrow])
    witness = {qcoord: Q(1)}
    for pivot, coeff in zip(pivots, gamma):
        if coeff:
            witness[pivot] = witness.get(pivot, Q(0)) + coeff
            if not witness[pivot]:
                del witness[pivot]
    for col in cols:
        if va.pairing(witness, col):
            raise AssertionError("frozen canonical witness fails base annihilation")
    value = va.pairing(witness, target)
    if not value:
        raise AssertionError("frozen canonical witness misses target")
    witness = {k: q / value for k, q in witness.items() if q}
    if va.pairing(witness, target) != 1:
        raise AssertionError("frozen canonical witness normalization drift")
    return witness


def reconstruct_context():
    a.assert_source_locks()
    a.validate_architecture()
    layer, prior = a.pcl.build_layer()
    if prior["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 predecessor drift in T3-011-D verifier")
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
    return strata, specialized, supports


def _verified_pairing(witness: dict, prod: dict, alt: dict, channel: str, uid) -> Q:
    sem = semantic.semantic_bundle([prod, alt])
    if not sem["equals_direct"][1]:
        raise AssertionError(f"quadratic finite-difference/product-rule mismatch: {channel}:{uid}")
    prod_pairing = va.pairing(witness, prod)
    alt_pairing = va.pairing(witness, alt)
    if alt_pairing != prod_pairing:
        raise AssertionError(
            f"quadratic cokernel pairing is representation-dependent: {channel}:{uid}: "
            f"direct={prod_pairing} product_rule={alt_pairing}"
        )
    return prod_pairing


def verify(result: dict) -> dict:
    if result.get("stage") != producer.STAGE:
        raise AssertionError("T3-011-D stage drift")
    if result.get("issue") != 498:
        raise AssertionError("T3-011-D issue drift")
    producer.validate_operation_parameters(increments=producer.CHANNEL_INCREMENT)
    producer.assert_c_locks()

    cls = result.get("bounded_extension_class", {})
    if cls.get("only_changed_dimension") != "coordinate_multiplier_polynomial_degree":
        raise AssertionError("T3-011-D widening dimension drift")
    if cls.get("predecessor_degree") != 1 or cls.get("admitted_degree") != 2:
        raise AssertionError("T3-011-D polynomial degree drift")
    for forbidden in (
        "pairs_admitted",
        "mixed_channel_monomials_admitted",
        "arbitrary_polynomial_envelope_admitted",
        "degree_gt_2_admitted",
        "support_enlargement_admitted",
        "harmonic_enlargement_admitted",
        "rational_prefactors_admitted",
        "adaptive_basis_growth_admitted",
        "raw_jet_reopened",
        "recurrence_search",
    ):
        if cls.get(forbidden):
            raise AssertionError(f"T3-011-D forbidden enlargement: {forbidden}")

    strata, specialized, supports = reconstruct_context()
    rows = result.get("tested_independent_prefix", [])
    row_index = 0
    first = None
    k1_candidates = None

    for channel in a.INDEPENDENT_CHANNELS:
        base, ids, cols, target = vc.reconstruct_channel(channel, strata, specialized, supports)
        if base["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"independent C base drift: {channel}")
        candidates = [uid for uid, col in zip(ids, cols) if col]
        if len(candidates) != producer.EXPECTED_COUNTS[channel]:
            raise AssertionError(f"independent candidate bank drift: {channel}")
        if channel == "k1":
            k1_candidates = list(candidates)
        witness = frozen_canonical_witness(cols, target)
        if va.pairing(witness, target) != 1:
            raise AssertionError(f"independent frozen witness normalization drift: {channel}")
        active = {rec["id"] for rec in base["active_cells"]}

        for uid in candidates:
            if row_index >= len(rows):
                break
            row = rows[row_index]
            if row["channel"] != channel or row["candidate"] != [uid[0], list(uid[1])]:
                break
            prod = producer.quadratic_global_column(channel, uid, strata, active)
            alt = verifier_global_column(channel, uid, strata, active)
            pairing = _verified_pairing(witness, prod, alt, channel, uid)
            if row["quadratic_response_sha256"] != c.global_vector_digest(prod):
                raise AssertionError(f"quadratic response digest drift: {channel}:{uid}")
            if row["obstruction_pairing"] != producer.qjson(pairing):
                raise AssertionError(f"quadratic obstruction pairing drift: {channel}:{uid}")
            if row["obstruction_pairing_nonzero"] != bool(pairing):
                raise AssertionError(f"quadratic pairing flag drift: {channel}:{uid}")
            row_index += 1
            if pairing:
                first = row
                break
        if first is not None:
            break

    if row_index != len(rows):
        raise AssertionError("tested independent prefix is not the canonical frozen prefix")

    mirror = result.get("mirror_l1", {})
    mirror_rows = mirror.get("tested_prefix", [])
    mirror_index = 0
    if first is None:
        if k1_candidates is None:
            raise AssertionError("k1 source bank absent")
        base, ids, cols, target = vc.reconstruct_channel("l1", strata, specialized, supports)
        witness = frozen_canonical_witness(cols, target)
        active = {rec["id"] for rec in base["active_cells"]}
        mirrored = [vc.mirror_unknown_k_to_l(uid) for uid in k1_candidates]
        for source, uid in zip(k1_candidates, mirrored):
            if mirror_index >= len(mirror_rows):
                break
            row = mirror_rows[mirror_index]
            if row["candidate"] != [uid[0], list(uid[1])]:
                raise AssertionError("l1 mirror candidate order drift")
            if row.get("source_k1_candidate") != [source[0], list(source[1])]:
                raise AssertionError("l1 mirror source marker drift")
            prod = producer.quadratic_global_column("l1", uid, strata, active)
            alt = verifier_global_column("l1", uid, strata, active)
            pairing = _verified_pairing(witness, prod, alt, "l1", uid)
            if row["obstruction_pairing"] != producer.qjson(pairing):
                raise AssertionError(f"l1 quadratic pairing drift: {uid}")
            mirror_index += 1
            if pairing:
                first = row
                break
        if mirror_index != len(mirror_rows):
            raise AssertionError("l1 tested prefix drift")

    expected_terminal = producer.POSITIVE_TERMINAL if first is not None else producer.NEGATIVE_TERMINAL
    if result.get("terminal") != expected_terminal:
        raise AssertionError("T3-011-D terminal drift")
    if result.get("first_cokernel_breaking_direction") != first:
        raise AssertionError("T3-011-D first direction drift")
    if result.get("polynomial_degree_alone_breaks_cokernel_obstruction") != (first is not None):
        raise AssertionError("T3-011-D answer flag drift")
    if first is None:
        if len(rows) != 311 or len(mirror_rows) != 110:
            raise AssertionError("negative terminal lacks complete quadratic exhaustion")
    else:
        if not (rows and rows[-1] == first) and not (mirror_rows and mirror_rows[-1] == first):
            raise AssertionError("first-nonzero stop rule violated")

    if result.get("residual_sum_zero_proved"):
        raise AssertionError("claim firewall inflation")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("proof/promotion firewall drift")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3 status inflation")

    return {
        "stage": producer.STAGE,
        "status": "INDEPENDENT_T3_011_D_REPLAY_COMPLETE",
        "terminal": expected_terminal,
        "tested_independent_prefix_count": len(rows),
        "tested_mirror_prefix_count": len(mirror_rows),
        "first_cokernel_breaking_direction": first,
        "polynomial_degree_alone_breaks_cokernel_obstruction": first is not None,
        "semantic_normal_form": semantic.SEMANTIC_NORMAL_FORM,
        "pairing_representation_invariance_checked": True,
        "finite_sampling_used": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    print(json.dumps(verify(producer.build()), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
