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

import t3_011_b as predecessor_producer  # noqa: E402
import verify_t3_011_b as predecessor_verifier  # noqa: E402

p = predecessor_producer.p
c = predecessor_producer.c
b = predecessor_producer.b
a = predecessor_producer.a
va = predecessor_verifier.va

OPERATION = "OZ-RT-BZ-T3-011-C"
STAGE = "T3_011_C_DIRECT_DISCRETE_PRODUCT_RULE_RESPONSE_GENERATOR_SEMANTICS_AUDIT"
AUDIT_ID = "DIRECT_DISCRETE_PRODUCT_RULE_RESPONSE_GENERATOR_AUDIT_001"
DIRECT_AUTHORITY_ID = "EXPLICIT_PRIMITIVE_SHIFT_RAW_FINITE_DIFFERENCE_V1"
SEMANTIC_NORMAL_FORM = "COMMON_DENOMINATOR_EXPANDED_Q_N_K_L_NUMERATOR_V1"
B_REVIEWED_HEAD = "7876a44286f3c958bf03ce120117c2cd689b2379"
B_MERGE_COMMIT = "f8dc03a4e546a47b7a2b6d77a96d689f47e4d9a3"
B_REQUIRED_TERMINAL = "BOUNDED_SINGLE_CHANNEL_LINEAR_NONZERO_RESPONSE_LIFT_CLASS_EXHAUSTED"
B_BLOBS = {
    "t3_011_b.py": "c0ed8906782bde979c78f0ae2c7655ca2abca0ab",
    "T3_011_B_CONTRACT.json": "3bdba0ef8cba3d975c12053ef1f122cb412ae352",
    "verify_t3_011_b.py": "8aa180375b907686326bc802875f457b4422b610",
}
EXPECTED_COUNTS = {"n1": 67, "n2": 67, "n3": 67, "k1": 110}
CHANNEL_INCREMENT = {"n1": 1, "n2": 2, "n3": 3, "k1": 1, "l1": 1}
CHANNEL_COORDINATE = {"n1": "n", "n2": "n", "n3": "n", "k1": "k", "l1": "l"}
Unknown = p.Unknown
GlobalVector = p.GlobalVector
Poly3 = dict[tuple[int, int, int], Q]


def sha(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def unknown_json(uid: Unknown) -> list:
    return [uid[0], list(uid[1])]


def assert_b_locks() -> dict[str, str]:
    got = {}
    for name, want in B_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"T3-011-B source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_011_B_CONTRACT.json").read_text())
    if contract["stage"] != predecessor_producer.STAGE:
        raise AssertionError("T3-011-B stage drift")
    if contract["bounded_correction_class"]["expected_candidate_counts"] != EXPECTED_COUNTS:
        raise AssertionError("T3-011-B candidate count contract drift")
    if contract["bounded_correction_class"]["expected_independent_trials"] != 311:
        raise AssertionError("T3-011-B trial count contract drift")
    if contract["bounded_correction_class"]["channel_coordinate_increment"] != CHANNEL_INCREMENT:
        raise AssertionError("T3-011-B coordinate increment drift")
    if contract["negative_boundary"]["terminal"] != B_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-B terminal contract drift")
    return got


def _const_poly(rat):
    return {(): rat} if rat else {}


def direct_delta_atom(name: str, shift: tuple[int, int, int]):
    """Primitive shifted harmonic increment; no predecessor response helper is authority."""
    dn, dk, dl = shift
    if sum(int(x != 0) for x in shift) != 1:
        raise ValueError(f"unsupported compound audit shift {shift}")
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
        return _const_poly(a.rc.inv(a.rc.lin_kl(1), r)) if (dk or dl) else {}
    if name.startswith("H_k_"):
        return _const_poly(a.rc.inv(a.rc.lin_k(1), r)) if dk else {}
    if name.startswith("H_l_"):
        return _const_poly(a.rc.inv(a.rc.lin_l(1), r)) if dl else {}
    raise ValueError(f"unknown oriented primitive audit letter {name}")


def direct_original_monomial(mon: tuple[str, ...]):
    out = a.rc.p_const(1)
    for name in mon:
        out = a.rc.p_mul(out, a.rc.p_atom(name))
    return out


def direct_shifted_monomial(mon: tuple[str, ...], shift: tuple[int, int, int]):
    out = a.rc.p_const(1)
    for name in mon:
        out = a.rc.p_mul(out, a.rc.p_add(a.rc.p_atom(name), direct_delta_atom(name, shift)))
    return out


def coordinate_factor(channel: str):
    if channel in ("n1", "n2", "n3"):
        return (1, 0, 0, 0)
    if channel == "k1":
        return (0, 1, 0, 0)
    if channel == "l1":
        return (0, 0, 1, 0)
    raise ValueError(channel)


def direct_coordinate_rat(channel: str):
    return a.rc.r_factor(coordinate_factor(channel), exponent=1)


def direct_shifted_coordinate_rat(channel: str, increment_override: int | None = None):
    step = CHANNEL_INCREMENT[channel] if increment_override is None else int(increment_override)
    return a.rc.r_add(direct_coordinate_rat(channel), a.rc.r_const(step))


def direct_finite_difference_poly(mon: tuple[str, ...], channel: str, increment_override: int | None = None):
    shift = a.pcl.SHIFTS[channel]
    original = direct_original_monomial(mon)
    shifted = direct_shifted_monomial(mon, shift)
    x0 = direct_coordinate_rat(channel)
    x1 = direct_shifted_coordinate_rat(channel, increment_override)
    return a.rc.p_add(
        a.rc.p_scale(shifted, x1),
        a.rc.p_scale(original, a.rc.r_scale(x0, -1)),
    )


def direct_product_rule_poly(mon: tuple[str, ...], channel: str, increment_override: int | None = None):
    shift = a.pcl.SHIFTS[channel]
    step = CHANNEL_INCREMENT[channel] if increment_override is None else int(increment_override)
    original = direct_original_monomial(mon)
    shifted = direct_shifted_monomial(mon, shift)
    delta_g = a.rc.p_add(shifted, a.rc.p_scale(original, -1))
    return a.rc.p_add(
        a.rc.p_scale(delta_g, direct_coordinate_rat(channel)),
        a.rc.p_scale(shifted, Q(step)),
    )


def direct_specialize_poly(poly, k_offset: int | None, l_offset: int | None):
    out = {}
    for mon, rat in poly.items():
        sr = a.specialize_rat(rat, k_offset, l_offset)
        if sr:
            out[mon] = sr
    return out


def direct_block_touches(mon: tuple[str, ...], block: str) -> bool:
    reps = set(a.WEIGHT_BLOCKS[block])
    return any(a.ORBIT_REP[x] in reps for x in mon)


def direct_response_vector(poly, scalar: str, block: str):
    out = {}
    for mon, rat in poly.items():
        if not direct_block_touches(mon, block):
            continue
        for sig, coeff in rat.items():
            coord = (scalar, mon, sig)
            z = out.get(coord, Q(0)) + coeff
            if z:
                out[coord] = z
            elif coord in out:
                del out[coord]
    return out


def direct_global_column_from_poly(raw, scalar: str, channel: str, strata: list[dict], active_cell_ids: set[str]):
    out = {}
    for st in strata:
        specialized = direct_specialize_poly(raw, st["k_offset"], st["l_offset"])
        for block in c.BLOCK_ORDER:
            cell_id = f"{channel}:{block}:{st['id']}"
            if cell_id not in active_cell_ids:
                continue
            local = direct_response_vector(specialized, scalar, block)
            for coord, q in local.items():
                key = (cell_id, coord)
                z = out.get(key, Q(0)) + q
                if z:
                    out[key] = z
                elif key in out:
                    del out[key]
    return out


# Exact semantic normal form for Laurent rational coefficients.  No sampling:
# every affine factor is expanded as a linear polynomial in Q[n,k,l], all
# compared paths are lifted to one common denominator, and numerators are
# compared coefficient-for-coefficient.
def _p3_add(x: Poly3, y: Poly3) -> Poly3:
    out = dict(x)
    for m, q in y.items():
        z = out.get(m, Q(0)) + q
        if z:
            out[m] = z
        elif m in out:
            del out[m]
    return out


def _p3_mul(x: Poly3, y: Poly3) -> Poly3:
    out: Poly3 = {}
    for (an, ak, al), qx in x.items():
        for (bn, bk, bl), qy in y.items():
            m = (an + bn, ak + bk, al + bl)
            z = out.get(m, Q(0)) + qx * qy
            if z:
                out[m] = z
            elif m in out:
                del out[m]
    return out


def _p3_scale(x: Poly3, q: Q) -> Poly3:
    return {m: q * v for m, v in x.items() if q * v}


def _linear_poly(factor) -> Poly3:
    an, ak, al, d = factor
    out: Poly3 = {}
    for mon, coeff in (((1, 0, 0), an), ((0, 1, 0), ak), ((0, 0, 1), al), ((0, 0, 0), d)):
        if coeff:
            out[mon] = Q(coeff)
    return out


def _p3_pow_linear(factor, exponent: int) -> Poly3:
    if exponent < 0:
        raise AssertionError("negative exponent entered polynomial numerator")
    out: Poly3 = {(0, 0, 0): Q(1)}
    base = _linear_poly(factor)
    for _ in range(exponent):
        out = _p3_mul(out, base)
    return out


def _joint_denominator(rats: list[dict]) -> dict:
    den = {}
    for rat in rats:
        for sig in rat:
            for factor, exponent in sig:
                if exponent < 0:
                    den[factor] = max(den.get(factor, 0), -exponent)
    return den


def _rat_common_numerator(rat: dict, den: dict) -> Poly3:
    out: Poly3 = {}
    for sig, coeff in rat.items():
        exp = dict(sig)
        term: Poly3 = {(0, 0, 0): Q(coeff)}
        for factor in sorted(set(den) | set(exp)):
            power = exp.get(factor, 0) + den.get(factor, 0)
            if power < 0:
                raise AssertionError(f"common denominator underflow at {factor}: {power}")
            if power:
                term = _p3_mul(term, _p3_pow_linear(factor, power))
        out = _p3_add(out, term)
    return out


def _poly3_rows(poly: Poly3) -> list[list[int]]:
    return [[an, ak, al, q.numerator, q.denominator] for (an, ak, al), q in sorted(poly.items())]


def _den_rows(den: dict) -> list[list]:
    return [[list(f), e] for f, e in sorted(den.items()) if e]


def _vector_rat_map(vec: GlobalVector) -> dict:
    out = {}
    for (cell_id, coord), q in vec.items():
        scalar, mon, sig = coord
        base = (cell_id, scalar, mon)
        rat = out.setdefault(base, {})
        z = rat.get(sig, Q(0)) + q
        if z:
            rat[sig] = z
        elif sig in rat:
            del rat[sig]
    return out


def semantic_bundle(vectors: list[GlobalVector]) -> dict:
    maps = [_vector_rat_map(v) for v in vectors]
    bases = sorted(set().union(*(set(m) for m in maps)), key=repr)
    rows = [[] for _ in vectors]
    mismatches = [[] for _ in vectors]
    for base in bases:
        rats = [m.get(base, {}) for m in maps]
        den = _joint_denominator(rats)
        nums = [_rat_common_numerator(rat, den) for rat in rats]
        cell_id, scalar, mon = base
        drows = _den_rows(den)
        for i, num in enumerate(nums):
            rows[i].append([cell_id, scalar, list(mon), drows, _poly3_rows(num)])
            if i and num != nums[0]:
                mismatches[i].append(repr(base))
    return {
        "normal_form": SEMANTIC_NORMAL_FORM,
        "semantic_sha256": [sha(r) for r in rows],
        "equals_direct": [not x for x in mismatches],
        "mismatch_base_coordinates": mismatches,
        "base_coordinate_count": len(bases),
    }


def representation_digest(vec: GlobalVector) -> str:
    return c.global_vector_digest(vec)


def candidate_record(channel: str, uid: Unknown, strata: list[dict], active_cell_ids: set[str]):
    scalar, mon = uid
    raw_fd = direct_finite_difference_poly(mon, channel)
    raw_product = direct_product_rule_poly(mon, channel)
    direct_fd = direct_global_column_from_poly(raw_fd, scalar, channel, strata, active_cell_ids)
    direct_product = direct_global_column_from_poly(raw_product, scalar, channel, strata, active_cell_ids)
    producer = p.lifted_global_column(channel, uid, strata, active_cell_ids)
    verifier = va.lifted_global_column(channel, uid, strata, active_cell_ids)
    sem = semantic_bundle([direct_fd, direct_product, producer, verifier])
    fd_eq_product = sem["equals_direct"][1]
    fd_eq_producer = sem["equals_direct"][2]
    fd_eq_verifier = sem["equals_direct"][3]
    all_equal = fd_eq_product and fd_eq_producer and fd_eq_verifier
    mismatch_kind = None
    mismatch = []
    if not fd_eq_product:
        mismatch_kind = "DIRECT_FINITE_DIFFERENCE_VS_PRODUCT_RULE"
        mismatch = sem["mismatch_base_coordinates"][1]
    elif not fd_eq_producer:
        mismatch_kind = "DIRECT_VS_T3_011_B_PRODUCER"
        mismatch = sem["mismatch_base_coordinates"][2]
    elif not fd_eq_verifier:
        mismatch_kind = "DIRECT_VS_T3_011_B_VERIFIER"
        mismatch = sem["mismatch_base_coordinates"][3]
    labels = [
        "direct_finite_difference",
        "direct_product_rule",
        "t3_011_b_producer",
        "t3_011_b_verifier",
    ]
    vectors = [direct_fd, direct_product, producer, verifier]
    digests = {f"{label}_sha256": sem["semantic_sha256"][i] for i, label in enumerate(labels)}
    repr_digests = {f"{label}_representation_sha256": representation_digest(vectors[i]) for i, label in enumerate(labels)}
    return {
        "candidate": unknown_json(uid),
        "channel": channel,
        "coordinate": CHANNEL_COORDINATE[channel],
        "coordinate_increment": CHANNEL_INCREMENT[channel],
        "semantic_normal_form": SEMANTIC_NORMAL_FORM,
        "semantic_base_coordinate_count": sem["base_coordinate_count"],
        **digests,
        **repr_digests,
        "direct_finite_difference_equals_product_rule": fd_eq_product,
        "direct_equals_t3_011_b_producer": fd_eq_producer,
        "direct_equals_t3_011_b_verifier": fd_eq_verifier,
        "all_three_existing_paths_plus_product_rule_concordant": all_equal,
        "mismatch_kind": mismatch_kind,
        "mismatch_coordinate_count": len(mismatch),
        "first_mismatch_coordinates": mismatch[:8],
    }


def build() -> dict:
    b_locks = assert_b_locks()
    predecessor_producer.assert_a_locks()
    p.assert_c_locks()
    c.assert_b_locks()
    b.assert_a_locks()
    a.assert_source_locks()
    a.validate_architecture()
    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 coefficient layer drift in T3-011-C")
    primitive_full = a.primitive_oriented_layer(layer)
    strata = a.shell_strata()
    specialized = {
        st["id"]: a.primitive_oriented_layer(a.specialize_layer(layer, st["k_offset"], st["l_offset"]))
        for st in strata
    }
    supports = {
        (channel, block): b.candidate_support(primitive_full, channel, block)
        for channel in a.CHANNEL_SCALARS
        for block in c.BLOCK_ORDER
    }
    channels = []
    total = 0
    total_mismatch = 0
    k1_candidates = None
    for channel in a.INDEPENDENT_CHANNELS:
        base, ids, cols, _target = c.build_channel_system(channel, primitive_full, strata, specialized, supports)
        if base["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"T3-011-C predecessor C base drift: {channel}")
        candidates = [uid for uid, col in zip(ids, cols) if col]
        if len(candidates) != EXPECTED_COUNTS[channel]:
            raise AssertionError(f"T3-011-C candidate bank drift: {channel}")
        active = {rec["id"] for rec in base["active_cells"]}
        rows = [candidate_record(channel, uid, strata, active) for uid in candidates]
        mismatch_count = sum(not row["all_three_existing_paths_plus_product_rule_concordant"] for row in rows)
        channels.append({
            "channel": channel,
            "candidate_count": len(candidates),
            "candidate_order_sha256": sha([unknown_json(uid) for uid in candidates]),
            "active_cell_count": len(active),
            "active_cell_sha256": sha(sorted(active)),
            "mismatch_count": mismatch_count,
            "all_candidates_concordant": mismatch_count == 0,
            "candidates": rows,
        })
        total += len(candidates)
        total_mismatch += mismatch_count
        if channel == "k1":
            k1_candidates = candidates
    if total != 311 or k1_candidates is None:
        raise AssertionError("T3-011-C independent candidate cardinality drift")

    lbase, _lids, _lcols, _ltarget = c.build_channel_system("l1", primitive_full, strata, specialized, supports)
    lactive = {rec["id"] for rec in lbase["active_cells"]}
    mirror_rows = []
    for kuid in k1_candidates:
        luid = c.mirror_unknown_k_to_l(kuid)
        rec = candidate_record("l1", luid, strata, lactive)
        rec["source_k1_candidate"] = unknown_json(kuid)
        mirror_rows.append(rec)
    mirror_mismatch = sum(not row["all_three_existing_paths_plus_product_rule_concordant"] for row in mirror_rows)
    if len(mirror_rows) != 110:
        raise AssertionError("T3-011-C l1 mirror audit cardinality drift")

    all_concordant = total_mismatch == 0 and mirror_mismatch == 0
    terminal = (
        "T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_CERTIFIED"
        if all_concordant
        else "T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_MISMATCH"
    )
    return {
        "schema_version": "1.0.0",
        "issue": 494,
        "operation": OPERATION,
        "stage": STAGE,
        "audit_class": AUDIT_ID,
        "status": "DIRECT_DISCRETE_PRODUCT_RULE_RESPONSE_GENERATOR_AUDIT_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": B_REVIEWED_HEAD,
            "merge_commit": B_MERGE_COMMIT,
            "source_blobs": b_locks,
            "required_terminal": B_REQUIRED_TERMINAL,
        },
        "direct_reconstruction": {
            "authority_id": DIRECT_AUTHORITY_ID,
            "raw_definition": "(x_c + Delta_c x_c) S_c(G) - x_c G",
            "coordinate_shift_normalization": "x_c + step is represented additively in the direct path",
            "semantic_normal_form": SEMANTIC_NORMAL_FORM,
            "semantic_normal_form_definition": "group coefficient signatures by cell/scalar/harmonic monomial; lift all compared Laurent rational functions to one exact common denominator; expand each affine factor into Q[n,k,l]; compare expanded numerator polynomials coefficient-for-coefficient",
            "finite_sampling_used": False,
            "product_rule": "x_c(S_c(G)-G)+(Delta_c x_c)S_c(G)",
            "channel_coordinate_increment": CHANNEL_INCREMENT,
            "uses_t3_011_b_generator_as_direct_authority": False,
            "uses_t3_011_b_verifier_generator_as_direct_authority": False,
            "strata_semantics_sha256": sha([[st["id"], st["k_offset"], st["l_offset"]] for st in strata]),
        },
        "channel_audits": channels,
        "independent_candidate_count": total,
        "independent_mismatch_count": total_mismatch,
        "mirror_l1_audit": {
            "source_channel": "k1",
            "candidate_count": len(mirror_rows),
            "source_k1_order_sha256": sha([unknown_json(uid) for uid in k1_candidates]),
            "active_cell_count": len(lactive),
            "active_cell_sha256": sha(sorted(lactive)),
            "mismatch_count": mirror_mismatch,
            "all_candidates_concordant": mirror_mismatch == 0,
            "candidates": mirror_rows,
        },
        "all_frozen_responses_concordant": all_concordant,
        "new_candidates_authorized": False,
        "pairs_or_two_lifts_authorized": False,
        "arbitrary_linear_combination_search_authorized": False,
        "generic_degree1_envelope_authorized": False,
        "support_or_harmonic_enlargement_authorized": False,
        "rational_prefactors_authorized": False,
        "adaptive_basis_growth_authorized": False,
        "raw_jet_reopening_authorized": False,
        "recurrence_search_authorized": False,
        "correction_layer_recombination_authorized": False,
        "theorem_promotion_authorized": False,
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
