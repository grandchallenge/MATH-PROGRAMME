from __future__ import annotations

import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_f as producer
import verify_t3_011_d as vd
import verify_t3_011_e as ve

semantic = vd.semantic
a = vd.a
c = producer.c
va = vd.va
vc = vd.vc
rc = a.rc


def _assert_e_locks_independent():
    got = {}
    for name, want in producer.E_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"independent E lock drift: {name}: {value} != {want}")
        got[name] = value
    return got


def _moved_signature(sig, shift):
    dn, dk, dl = shift
    moved = {}
    for factor, exponent in reversed(sig):
        an, ak, al, constant = factor
        translated = (an, ak, al, constant + dn * an + dk * ak + dl * al)
        moved[translated] = moved.get(translated, 0) + int(exponent)
        if moved[translated] == 0:
            del moved[translated]
    return tuple(sorted(moved.items()))


def _shift_rat_independent(rat, shift):
    acc = {}
    for sig, coeff in reversed(list(rat.items())):
        key = _moved_signature(sig, shift)
        value = acc.get(key, Q(0)) + Q(coeff)
        if value:
            acc[key] = value
        elif key in acc:
            del acc[key]
    return acc


def _shift_poly_independent(poly, channel):
    shift = a.pcl.SHIFTS[channel]
    result = {}
    for mon, rat in reversed(list(poly.items())):
        coeff = _shift_rat_independent(rat, shift)
        if not coeff:
            continue
        term = {(): coeff}
        for name in reversed(mon):
            shifted_atom = rc.p_add(rc.p_atom(name), semantic.direct_delta_atom(name, shift))
            term = rc.p_mul(term, shifted_atom)
        result = rc.p_add(result, term)
    return result


def _minus(left, right):
    return rc.p_add(left, rc.p_scale(right, -1))


def _xy(left, right, left_shifted=False, right_shifted=False):
    lx = (
        semantic.direct_shifted_coordinate_rat(left)
        if left_shifted
        else semantic.direct_coordinate_rat(left)
    )
    rx = (
        semantic.direct_shifted_coordinate_rat(right)
        if right_shifted
        else semantic.direct_coordinate_rat(right)
    )
    return rc.r_mul(lx, rx)


def _independent_raw_bundle(mon, left, right):
    if producer.CHANNEL_COORDINATE[left] == producer.CHANNEL_COORDINATE[right]:
        raise AssertionError("independent mixed response admitted same-coordinate pair")

    g = semantic.direct_original_monomial(mon)
    gc = _shift_poly_independent(g, left)
    gd = _shift_poly_independent(g, right)
    gcd_rl = _shift_poly_independent(gc, right)
    gcd_lr = _shift_poly_independent(gd, left)

    # Verifier authority: two-channel product rule.
    delta_c = _minus(gc, g)
    delta_d = _minus(gd, g)
    delta_cd = rc.p_add(gcd_rl, rc.p_scale(gc, -1), rc.p_scale(gd, -1), g)
    sc_delta_d = _shift_poly_independent(delta_d, left)
    sd_delta_c = _shift_poly_independent(delta_c, right)
    product = rc.p_add(
        rc.p_scale(delta_cd, _xy(left, right)),
        rc.p_scale(
            sc_delta_d,
            rc.r_scale(semantic.direct_coordinate_rat(right), producer.CHANNEL_INCREMENT[left]),
        ),
        rc.p_scale(
            sd_delta_c,
            rc.r_scale(semantic.direct_coordinate_rat(left), producer.CHANNEL_INCREMENT[right]),
        ),
        rc.p_scale(gcd_rl, Q(producer.CHANNEL_INCREMENT[left] * producer.CHANNEL_INCREMENT[right])),
    )

    # Reconstruct the direct four-term identity independently for semantic comparison.
    direct = rc.p_add(
        rc.p_scale(gcd_rl, _xy(left, right, True, True)),
        rc.p_scale(gc, rc.r_scale(_xy(left, right, True, False), -1)),
        rc.p_scale(gd, rc.r_scale(_xy(left, right, False, True), -1)),
        rc.p_scale(g, _xy(left, right, False, False)),
    )
    direct_reverse = rc.p_add(
        rc.p_scale(gcd_lr, _xy(left, right, True, True)),
        rc.p_scale(gc, rc.r_scale(_xy(left, right, True, False), -1)),
        rc.p_scale(gd, rc.r_scale(_xy(left, right, False, True), -1)),
        rc.p_scale(g, _xy(left, right, False, False)),
    )
    return direct, product, direct_reverse


def _reconstruct_banks(strata, specialized, supports):
    banks = {}
    k1_candidates = None
    for channel in list(a.INDEPENDENT_CHANNELS) + ["l1"]:
        base, ids, cols, target = vc.reconstruct_channel(channel, strata, specialized, supports)
        if base["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"independent F base drift: {channel}")
        candidates = [uid for uid, col in zip(ids, cols) if col]
        if channel in producer.d.EXPECTED_COUNTS:
            if len(candidates) != producer.d.EXPECTED_COUNTS[channel]:
                raise AssertionError(f"independent F candidate-bank drift: {channel}")
        if channel == "k1":
            k1_candidates = list(candidates)
        if channel == "l1":
            if k1_candidates is None:
                raise AssertionError("independent F l1 mirror source missing")
            candidates = [vc.mirror_unknown_k_to_l(uid) for uid in k1_candidates]
            if len(candidates) != 110:
                raise AssertionError("independent F l1 mirror cardinality drift")
        witness = vd.frozen_canonical_witness(cols, target)
        if va.pairing(witness, target) != 1:
            raise AssertionError(f"independent F witness normalization drift: {channel}")
        active = vd.independent_active_namespace(channel, strata, specialized, supports)
        banks[channel] = {
            "candidates": candidates,
            "active": active,
            "witness": witness,
        }
    return banks


def _independent_record(pair, endpoint, uid, strata, bank):
    left, right = pair
    scalar, mon = uid
    direct_raw, product_raw, reverse_raw = _independent_raw_bundle(mon, left, right)
    direct = semantic.direct_global_column_from_poly(direct_raw, scalar, endpoint, strata, bank["active"])
    product = semantic.direct_global_column_from_poly(product_raw, scalar, endpoint, strata, bank["active"])
    reverse = semantic.direct_global_column_from_poly(reverse_raw, scalar, endpoint, strata, bank["active"])

    sem = semantic.semantic_bundle([direct, product, reverse])
    product_equal = sem["equals_direct"][1]
    commute_equal = sem["equals_direct"][2]
    qd = va.pairing(bank["witness"], direct)
    qp = va.pairing(bank["witness"], product)
    qr = va.pairing(bank["witness"], reverse)
    pairing_invariant = qd == qp == qr

    ambiguity = None
    if not commute_equal:
        ambiguity = "COMPOUND_SHIFT_ORDER_MISMATCH"
    elif not product_equal:
        ambiguity = "DIRECT_FOUR_TERM_VS_TWO_CHANNEL_PRODUCT_RULE"
    elif not pairing_invariant:
        ambiguity = "WITNESS_PAIRING_REPRESENTATION_DEPENDENCE"

    return {
        "direct_equals_product_rule": product_equal,
        "compound_shift_orders_commute_semantically": commute_equal,
        "pairing_representation_invariant": pairing_invariant,
        "semantic_ambiguity_kind": ambiguity,
        "mixed_response_nonzero": bool(direct),
        "direct_pairing": qd,
        "product_pairing": qp,
        "reverse_pairing": qr,
    }


def verify(result: dict) -> dict:
    if result.get("issue") != producer.ISSUE or result.get("stage") != producer.STAGE:
        raise AssertionError("T3-011-F identity drift")
    producer.validate_scope()
    _assert_e_locks_independent()

    e_result = producer.e.build()
    e_replay = ve.verify(e_result)
    if e_replay.get("terminal") != producer.E_REQUIRED_TERMINAL:
        raise AssertionError("independent F requires exact E closure replay")
    if e_replay.get("candidate_record_count") != 421:
        raise AssertionError("independent F E replay cardinality drift")
    if e_replay.get("semantic_functional_ambiguity") is not None:
        raise AssertionError("independent F requires E ambiguity NONE")
    if e_replay.get("higher_degree_set") != []:
        raise AssertionError("independent F requires E higher-degree residue []")

    mixed = result.get("mixed_class", {})
    if mixed.get("total_degree") != 2 or mixed.get("multiplier") != "x_c*x_d":
        raise AssertionError("T3-011-F mixed-class degree/multiplier drift")
    if mixed.get("unordered_pair_order") != [list(x) for x in producer.ADMITTED_PAIRS]:
        raise AssertionError("T3-011-F pair-order drift")
    for forbidden in (
        "square_terms_admitted",
        "degree_gt_2_admitted",
        "arbitrary_bivariate_polynomials_admitted",
        "linear_combinations_admitted",
        "support_or_harmonic_enlargement_admitted",
        "rational_prefactors_admitted",
        "recurrence_search_admitted",
        "correction_layer_work_admitted",
    ):
        if mixed.get(forbidden):
            raise AssertionError(f"T3-011-F forbidden widening: {forbidden}")

    strata, specialized, supports = vd.reconstruct_context()
    banks = _reconstruct_banks(strata, specialized, supports)
    expected_records = result.get("tested_records", [])
    cursor = 0
    first_breaking = None
    first_ambiguity = None
    stop = False

    for pair_index, pair in enumerate(producer.ADMITTED_PAIRS):
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            for candidate_index, uid in enumerate(bank["candidates"]):
                if cursor >= len(expected_records):
                    raise AssertionError("producer mixed scan truncated before its declared terminal")
                rec = expected_records[cursor]
                expected_identity = {
                    "ordinal": cursor,
                    "pair_index": pair_index,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                    "pair": list(pair),
                    "endpoint": endpoint,
                    "candidate": [uid[0], list(uid[1])],
                }
                for key, value in expected_identity.items():
                    if rec.get(key) != value:
                        raise AssertionError(f"T3-011-F deterministic scan drift at {cursor}: {key}")

                alt = _independent_record(pair, endpoint, uid, strata, bank)
                if rec.get("direct_equals_product_rule") != alt["direct_equals_product_rule"]:
                    raise AssertionError(f"F product-rule semantic flag drift at {cursor}")
                if rec.get("compound_shift_orders_commute_semantically") != alt[
                    "compound_shift_orders_commute_semantically"
                ]:
                    raise AssertionError(f"F commuting-shift semantic flag drift at {cursor}")
                if rec.get("pairing_representation_invariant") != alt["pairing_representation_invariant"]:
                    raise AssertionError(f"F pairing-invariance flag drift at {cursor}")
                if rec.get("semantic_ambiguity_kind") != alt["semantic_ambiguity_kind"]:
                    raise AssertionError(f"F ambiguity-kind drift at {cursor}")
                if rec.get("mixed_response_nonzero") != alt["mixed_response_nonzero"]:
                    raise AssertionError(f"F response nonzero flag drift at {cursor}")

                qd = alt["direct_pairing"]
                if rec.get("normalized_cokernel_pairing") != [qd.numerator, qd.denominator]:
                    raise AssertionError(f"F normalized cokernel pairing drift at {cursor}")
                if rec.get("direct_normalized_cokernel_pairing") != [qd.numerator, qd.denominator]:
                    raise AssertionError(f"F direct pairing drift at {cursor}")
                qp = alt["product_pairing"]
                if rec.get("product_rule_normalized_cokernel_pairing") != [qp.numerator, qp.denominator]:
                    raise AssertionError(f"F product pairing drift at {cursor}")
                qr = alt["reverse_pairing"]
                if rec.get("reverse_shift_normalized_cokernel_pairing") != [qr.numerator, qr.denominator]:
                    raise AssertionError(f"F reverse pairing drift at {cursor}")
                if rec.get("normalized_cokernel_pairing_nonzero") != bool(qd):
                    raise AssertionError(f"F cokernel nonzero flag drift at {cursor}")

                cursor += 1
                if alt["semantic_ambiguity_kind"] is not None:
                    first_ambiguity = rec
                    stop = True
                    break
                if qd:
                    first_breaking = rec
                    stop = True
                    break
            if stop:
                break
        if stop:
            break

    if cursor != len(expected_records):
        raise AssertionError("producer emitted records after the canonical first terminal event")

    if first_ambiguity is not None:
        terminal = producer.AMBIGUITY_TERMINAL
    elif first_breaking is not None:
        terminal = producer.POSITIVE_TERMINAL
    else:
        terminal = producer.NEGATIVE_TERMINAL

    full_count = sum(
        len(banks[left]["candidates"]) + len(banks[right]["candidates"])
        for left, right in producer.ADMITTED_PAIRS
    )
    if terminal == producer.NEGATIVE_TERMINAL and cursor != full_count:
        raise AssertionError("independent negative terminal lacks full mixed-class exhaustion")
    if result.get("expected_full_record_count") != full_count:
        raise AssertionError("T3-011-F expected full record-count drift")
    if result.get("tested_record_count") != cursor:
        raise AssertionError("T3-011-F tested record-count drift")
    if result.get("terminal") != terminal:
        raise AssertionError("T3-011-F terminal drift")
    if result.get("first_cokernel_breaking_direction") != first_breaking:
        raise AssertionError("T3-011-F first breaking direction drift")
    if result.get("first_semantic_functional_ambiguity") != first_ambiguity:
        raise AssertionError("T3-011-F first ambiguity drift")

    if result.get("residual_sum_zero_proved"):
        raise AssertionError("T3-011-F claim firewall inflation")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE":
        raise AssertionError("T3-011-F proof/promotion firewall drift")
    if result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3-011-F T3 status inflation")

    return {
        "stage": producer.STAGE,
        "status": "INDEPENDENT_T3_011_F_REPLAY_COMPLETE",
        "terminal": terminal,
        "tested_record_count": cursor,
        "expected_full_record_count": full_count,
        "first_cokernel_breaking_direction": first_breaking,
        "first_semantic_functional_ambiguity": first_ambiguity,
        "semantic_normal_form": semantic.SEMANTIC_NORMAL_FORM,
        "finite_sampling_used": False,
        "residual_sum_zero_proved": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    print(json.dumps(verify(producer.build()), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
