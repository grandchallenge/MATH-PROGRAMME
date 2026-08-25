from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import t3_011_c as semantic
import t3_011_d as d
import t3_011_e as e

p = d.p
c = d.c
b = d.b
a = d.a
rc = a.rc

OPERATION = "OZ-RT-BZ-T3-011-F"
STAGE = "T3_011_F_MINIMAL_MIXED_CHANNEL_COKERNEL_ESCAPE_AUDIT"
ISSUE = 509
E_REVIEWED_HEAD = "18d6e84c59f5585f65d824f7d4c2a99fffa9f893"
E_MERGE_COMMIT = "cd967335c55bd9899e1e51647d294d128be33fcd"
E_REQUIRED_TERMINAL = "POLYNOMIAL_MULTIPLIER_COKERNEL_CLOSURE_CERTIFIED"
E_BLOBS = {
    "t3_011_e.py": "f7e27bb27947680c8bdda6b9b4398fceb3fc5202",
    "T3_011_E_CONTRACT.json": "d980786e6744e8f0b0fb6f71f4b99a95a1468780",
    "verify_t3_011_e.py": "ab93696f1b1fb5bb27eb11c0878cfcac2a150b3b",
}

CHANNEL_COORDINATE = dict(d.CHANNEL_COORDINATE)
CHANNEL_INCREMENT = dict(d.CHANNEL_INCREMENT)
ADMITTED_PAIRS = (
    ("n1", "k1"),
    ("n1", "l1"),
    ("n2", "k1"),
    ("n2", "l1"),
    ("n3", "k1"),
    ("n3", "l1"),
    ("k1", "l1"),
)
POSITIVE_TERMINAL = "MINIMAL_MIXED_CHANNEL_QUADRATIC_COKERNEL_BREAKING_DIRECTION_FOUND"
NEGATIVE_TERMINAL = "MIXED_CHANNEL_QUADRATIC_RESPONSE_CLASS_COKERNEL_INVISIBLE"
AMBIGUITY_TERMINAL = "MIXED_CHANNEL_SEMANTIC_FUNCTIONAL_AMBIGUITY"
E_LEDGER_FIELDS = (
    "candidate_count",
    "candidate_order_sha256",
    "active_cell_count",
    "active_cell_sha256",
    "cokernel_witness_sha256",
    "target_quotient_residual_sha256",
)


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def assert_e_locks() -> dict[str, str]:
    got = {}
    for name, want in E_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"T3-011-E source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_011_E_CONTRACT.json").read_text())
    if contract.get("operation") != "OZ-RT-BZ-T3-011-E":
        raise AssertionError("T3-011-E contract operation drift")
    if contract.get("terminals", {}).get("closure") != E_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-E closure terminal drift")
    if contract.get("candidate_bank", {}).get("expected_total_records") != 421:
        raise AssertionError("T3-011-E candidate-bank contract drift")
    return got


def validate_scope(
    pairs=ADMITTED_PAIRS,
    total_degree: int = 2,
    square_terms: bool = False,
    arbitrary_bivariate: bool = False,
    linear_combinations: bool = False,
    support_enlargement: bool = False,
) -> None:
    pairs = tuple(tuple(x) for x in pairs)
    if pairs != ADMITTED_PAIRS:
        raise AssertionError("T3-011-F admitted unordered-pair order drift")
    if total_degree != 2:
        raise AssertionError("T3-011-F admits total degree 2 only")
    if square_terms:
        raise AssertionError("T3-011-F forbids x_c^2 terms")
    if arbitrary_bivariate:
        raise AssertionError("T3-011-F forbids arbitrary bivariate polynomials")
    if linear_combinations:
        raise AssertionError("T3-011-F forbids linear combinations of mixed lifts")
    if support_enlargement:
        raise AssertionError("T3-011-F forbids support/harmonic enlargement")
    for left, right in pairs:
        if left == right:
            raise AssertionError("T3-011-F requires distinct channels")
        if CHANNEL_COORDINATE[left] == CHANNEL_COORDINATE[right]:
            raise AssertionError("T3-011-F forbids same-coordinate channel pairs closed by E")


def _translate_factor(factor, shift: tuple[int, int, int]):
    dn, dk, dl = shift
    if len(factor) == 5 and factor[0] == a.pcl.PINV_TAG:
        tag, an, ak, al, constant = factor
        return (tag, an, ak, al, constant + an * dn + ak * dk + al * dl)
    if len(factor) != 4:
        raise AssertionError(f"unexpected rational factor shape during shift: {factor}")
    an, ak, al, constant = factor
    return (an, ak, al, constant + an * dn + ak * dk + al * dl)


def _translate_sig(sig, shift: tuple[int, int, int]):
    powers = {}
    for factor, exponent in sig:
        moved = _translate_factor(factor, shift)
        powers[moved] = powers.get(moved, 0) + int(exponent)
        if not powers[moved]:
            del powers[moved]
    return tuple(sorted(powers.items()))


def translate_rat(rat, shift: tuple[int, int, int]):
    out = {}
    for sig, coeff in rat.items():
        moved = _translate_sig(sig, shift)
        value = out.get(moved, Q(0)) + Q(coeff)
        if value:
            out[moved] = value
        elif moved in out:
            del out[moved]
    return out


def shift_poly(poly, channel: str):
    shift = a.pcl.SHIFTS[channel]
    out = {}
    for mon, rat in poly.items():
        moved_rat = translate_rat(rat, shift)
        if not moved_rat:
            continue
        term = {(): moved_rat}
        for name in mon:
            term = rc.p_mul(term, b.primitive_shift_atom(name, shift))
        out = rc.p_add(out, term)
    return out


def _poly_minus(left, right):
    return rc.p_add(left, rc.p_scale(right, -1))


def _coord_product(left: str, right: str, shifted_left: bool, shifted_right: bool):
    lrat = (
        semantic.direct_shifted_coordinate_rat(left)
        if shifted_left
        else semantic.direct_coordinate_rat(left)
    )
    rrat = (
        semantic.direct_shifted_coordinate_rat(right)
        if shifted_right
        else semantic.direct_coordinate_rat(right)
    )
    return rc.r_mul(lrat, rrat)


def mixed_raw_bundle(mon: tuple[str, ...], left: str, right: str):
    if CHANNEL_COORDINATE[left] == CHANNEL_COORDINATE[right]:
        raise AssertionError("mixed response requires distinct coordinate axes")

    g = semantic.direct_original_monomial(mon)
    gc = shift_poly(g, left)
    gd = shift_poly(g, right)
    gcd_lr = shift_poly(gc, right)
    gcd_rl = shift_poly(gd, left)

    direct = rc.p_add(
        rc.p_scale(gcd_lr, _coord_product(left, right, True, True)),
        rc.p_scale(gc, rc.r_scale(_coord_product(left, right, True, False), -1)),
        rc.p_scale(gd, rc.r_scale(_coord_product(left, right, False, True), -1)),
        rc.p_scale(g, _coord_product(left, right, False, False)),
    )

    direct_reverse = rc.p_add(
        rc.p_scale(gcd_rl, _coord_product(left, right, True, True)),
        rc.p_scale(gc, rc.r_scale(_coord_product(left, right, True, False), -1)),
        rc.p_scale(gd, rc.r_scale(_coord_product(left, right, False, True), -1)),
        rc.p_scale(g, _coord_product(left, right, False, False)),
    )

    delta_c = _poly_minus(gc, g)
    delta_d = _poly_minus(gd, g)
    delta_cd = rc.p_add(gcd_lr, rc.p_scale(gc, -1), rc.p_scale(gd, -1), g)
    sc_delta_d = shift_poly(delta_d, left)
    sd_delta_c = shift_poly(delta_c, right)

    xcxd = _coord_product(left, right, False, False)
    product_rule = rc.p_add(
        rc.p_scale(delta_cd, xcxd),
        rc.p_scale(sc_delta_d, rc.r_scale(semantic.direct_coordinate_rat(right), CHANNEL_INCREMENT[left])),
        rc.p_scale(sd_delta_c, rc.r_scale(semantic.direct_coordinate_rat(left), CHANNEL_INCREMENT[right])),
        rc.p_scale(gcd_lr, Q(CHANNEL_INCREMENT[left] * CHANNEL_INCREMENT[right])),
    )
    return direct, product_rule, direct_reverse


def _channel_banks(primitive_full, strata, specialized, supports):
    banks = {}
    k1_candidates = None
    for channel in list(a.INDEPENDENT_CHANNELS) + ["l1"]:
        base, ids, cols, target, candidates, active, witness, residual = d.channel_bank(
            channel, primitive_full, strata, specialized, supports
        )
        if channel == "k1":
            k1_candidates = list(candidates)
        if channel == "l1":
            if k1_candidates is None:
                raise AssertionError("T3-011-F l1 mirror source missing")
            candidates = [c.mirror_unknown_k_to_l(uid) for uid in k1_candidates]
            if len(candidates) != 110:
                raise AssertionError("T3-011-F l1 mirror cardinality drift")
        banks[channel] = {
            "base": base,
            "ids": ids,
            "cols": cols,
            "target": target,
            "candidates": list(candidates),
            "active": set(active),
            "witness": witness,
            "residual": residual,
        }
    return banks


def _bank_ledger(bank) -> dict:
    candidates = bank["candidates"]
    return {
        "candidate_count": len(candidates),
        "candidate_order_sha256": sha([unknown_json(uid) for uid in candidates]),
        "active_cell_count": len(bank["active"]),
        "active_cell_sha256": sha(sorted(bank["active"])),
        "cokernel_witness_sha256": p.sha(p.witness_rows(bank["witness"])),
        "target_quotient_residual_sha256": c.global_vector_digest(bank["residual"]),
    }


def assert_predecessor_channel_ledgers(predecessor: dict, bank_ledgers: dict[str, dict]) -> str:
    rows = predecessor.get("channel_ledgers")
    if not isinstance(rows, list):
        raise AssertionError("T3-011-F E channel ledger missing")
    expected = {row.get("channel"): row for row in rows}
    if None in expected or set(expected) != set(bank_ledgers):
        raise AssertionError("T3-011-F E channel set drift")
    canonical = []
    for row in rows:
        channel = row["channel"]
        actual = bank_ledgers[channel]
        for field in E_LEDGER_FIELDS:
            if actual.get(field) != row.get(field):
                raise AssertionError(
                    f"T3-011-F frozen E ledger drift: {channel}:{field}: "
                    f"{actual.get(field)} != {row.get(field)}"
                )
        canonical.append({"channel": channel, **{field: actual[field] for field in E_LEDGER_FIELDS}})
    return sha(canonical)


def _candidate_record(pair, endpoint, uid, strata, bank):
    left, right = pair
    scalar, mon = uid
    direct_raw, product_raw, reverse_raw = mixed_raw_bundle(mon, left, right)
    direct_vec = semantic.direct_global_column_from_poly(
        direct_raw, scalar, endpoint, strata, bank["active"]
    )
    product_vec = semantic.direct_global_column_from_poly(
        product_raw, scalar, endpoint, strata, bank["active"]
    )
    reverse_vec = semantic.direct_global_column_from_poly(
        reverse_raw, scalar, endpoint, strata, bank["active"]
    )
    sem = semantic.semantic_bundle([direct_vec, product_vec, reverse_vec])
    product_equal = sem["equals_direct"][1]
    commute_equal = sem["equals_direct"][2]
    direct_pairing = p.pairing(bank["witness"], direct_vec)
    product_pairing = p.pairing(bank["witness"], product_vec)
    reverse_pairing = p.pairing(bank["witness"], reverse_vec)
    pairing_invariant = direct_pairing == product_pairing == reverse_pairing

    ambiguity_kind = None
    ambiguity_coordinates = []
    if not commute_equal:
        ambiguity_kind = "COMPOUND_SHIFT_ORDER_MISMATCH"
        ambiguity_coordinates = sem["mismatch_base_coordinates"][2]
    elif not product_equal:
        ambiguity_kind = "DIRECT_FOUR_TERM_VS_TWO_CHANNEL_PRODUCT_RULE"
        ambiguity_coordinates = sem["mismatch_base_coordinates"][1]
    elif not pairing_invariant:
        ambiguity_kind = "WITNESS_PAIRING_REPRESENTATION_DEPENDENCE"

    return {
        "pair": [left, right],
        "endpoint": endpoint,
        "candidate": unknown_json(uid),
        "coordinate_pair": [CHANNEL_COORDINATE[left], CHANNEL_COORDINATE[right]],
        "increment_pair": [CHANNEL_INCREMENT[left], CHANNEL_INCREMENT[right]],
        "total_degree": 2,
        "semantic_normal_form": semantic.SEMANTIC_NORMAL_FORM,
        "semantic_base_coordinate_count": sem["base_coordinate_count"],
        "direct_semantic_sha256": sem["semantic_sha256"][0],
        "product_rule_semantic_sha256": sem["semantic_sha256"][1],
        "reverse_shift_semantic_sha256": sem["semantic_sha256"][2],
        "direct_equals_product_rule": product_equal,
        "compound_shift_orders_commute_semantically": commute_equal,
        "semantic_ambiguity_kind": ambiguity_kind,
        "semantic_ambiguity_coordinate_count": len(ambiguity_coordinates),
        "first_semantic_ambiguity_coordinates": ambiguity_coordinates[:8],
        "mixed_response_representation_sha256": c.global_vector_digest(direct_vec),
        "mixed_response_nonzero": bool(direct_vec),
        "direct_normalized_cokernel_pairing": qjson(direct_pairing),
        "product_rule_normalized_cokernel_pairing": qjson(product_pairing),
        "reverse_shift_normalized_cokernel_pairing": qjson(reverse_pairing),
        "pairing_representation_invariant": pairing_invariant,
        "normalized_cokernel_pairing": qjson(direct_pairing),
        "normalized_cokernel_pairing_nonzero": bool(direct_pairing),
    }


def build() -> dict:
    validate_scope()
    e_locks = assert_e_locks()
    predecessor = e.build()
    if predecessor.get("terminal") != E_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-F requires certified E closure terminal")
    if predecessor.get("candidate_record_count") != 421:
        raise AssertionError("T3-011-F E candidate-record drift")
    if predecessor.get("semantic_functional_ambiguity") is not None:
        raise AssertionError("T3-011-F requires E semantic ambiguity NONE")
    if predecessor.get("higher_degree_set") != []:
        raise AssertionError("T3-011-F requires E higher-degree residue []")

    primitive_full, strata, specialized, supports = d.build_context()
    banks = _channel_banks(primitive_full, strata, specialized, supports)
    bank_ledgers = {channel: _bank_ledger(bank) for channel, bank in banks.items()}
    predecessor_channel_ledger_sha256 = assert_predecessor_channel_ledgers(predecessor, bank_ledgers)

    records = []
    pair_ledgers = []
    first_breaking = None
    first_ambiguity = None

    stop = False
    ordinal = 0
    for pair_index, pair in enumerate(ADMITTED_PAIRS):
        pair_start = len(records)
        endpoint_ledgers = []
        for endpoint_index, endpoint in enumerate(pair):
            bank = banks[endpoint]
            endpoint_start = len(records)
            for candidate_index, uid in enumerate(bank["candidates"]):
                rec = _candidate_record(pair, endpoint, uid, strata, bank)
                rec.update({
                    "ordinal": ordinal,
                    "pair_index": pair_index,
                    "endpoint_index": endpoint_index,
                    "candidate_index": candidate_index,
                })
                records.append(rec)
                ordinal += 1
                if rec["semantic_ambiguity_kind"] is not None:
                    first_ambiguity = rec
                    stop = True
                    break
                if rec["normalized_cokernel_pairing_nonzero"]:
                    first_breaking = rec
                    stop = True
                    break
            endpoint_ledgers.append({
                "endpoint": endpoint,
                "frozen_candidate_count": len(bank["candidates"]),
                "tested_prefix_count": len(records) - endpoint_start,
                "candidate_order_sha256": bank_ledgers[endpoint]["candidate_order_sha256"],
                "witness_sha256": bank_ledgers[endpoint]["cokernel_witness_sha256"],
            })
            if stop:
                break
        pair_ledgers.append({
            "pair": list(pair),
            "pair_index": pair_index,
            "endpoint_ledgers": endpoint_ledgers,
            "tested_prefix_count": len(records) - pair_start,
        })
        if stop:
            break

    if first_ambiguity is not None:
        terminal = AMBIGUITY_TERMINAL
    elif first_breaking is not None:
        terminal = POSITIVE_TERMINAL
    else:
        terminal = NEGATIVE_TERMINAL

    expected_full = sum(
        len(banks[left]["candidates"]) + len(banks[right]["candidates"])
        for left, right in ADMITTED_PAIRS
    )
    if terminal == NEGATIVE_TERMINAL and len(records) != expected_full:
        raise AssertionError("negative terminal requires exhaustive admitted mixed-class scan")

    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "MINIMAL_MIXED_CHANNEL_COKERNEL_ESCAPE_AUDIT_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": E_REVIEWED_HEAD,
            "merge_commit": E_MERGE_COMMIT,
            "source_blobs": e_locks,
            "required_terminal": E_REQUIRED_TERMINAL,
            "candidate_record_count": predecessor["candidate_record_count"],
            "semantic_functional_ambiguity": predecessor["semantic_functional_ambiguity"],
            "higher_degree_set": predecessor["higher_degree_set"],
            "channel_ledgers_exactly_matched": True,
            "channel_ledgers_sha256": predecessor_channel_ledger_sha256,
        },
        "mixed_class": {
            "total_degree": 2,
            "multiplier": "x_c*x_d",
            "unordered_pair_order": [list(pair) for pair in ADMITTED_PAIRS],
            "same_coordinate_pairs_excluded_as_E_reducible": True,
            "endpoint_anchored_candidate_banks": True,
            "direct_four_term_identity": "(x_c+h_c)(x_d+h_d)S_cS_d(G)-(x_c+h_c)x_dS_c(G)-x_c(x_d+h_d)S_d(G)+x_cx_dG",
            "two_channel_product_rule": "x_cx_d Delta_cDelta_d(G)+h_c x_d S_c(Delta_dG)+h_d x_c S_d(Delta_cG)+h_ch_d S_cS_d(G)",
            "semantic_normal_form": semantic.SEMANTIC_NORMAL_FORM,
            "square_terms_admitted": False,
            "degree_gt_2_admitted": False,
            "arbitrary_bivariate_polynomials_admitted": False,
            "linear_combinations_admitted": False,
            "support_or_harmonic_enlargement_admitted": False,
            "rational_prefactors_admitted": False,
            "recurrence_search_admitted": False,
            "correction_layer_work_admitted": False,
        },
        "bank_ledgers": bank_ledgers,
        "pair_ledgers": pair_ledgers,
        "expected_full_record_count": expected_full,
        "tested_record_count": len(records),
        "tested_records": records,
        "first_cokernel_breaking_direction": first_breaking,
        "first_semantic_functional_ambiguity": first_ambiguity,
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
