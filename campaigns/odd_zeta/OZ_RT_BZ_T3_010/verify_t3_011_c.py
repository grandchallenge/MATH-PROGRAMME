#!/usr/bin/env python3
from __future__ import annotations

import ast
import hashlib
import json
import subprocess
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
a = predecessor_producer.a
va = predecessor_verifier.va
vc = predecessor_verifier.vc
vb = predecessor_verifier.vb

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
Poly3 = dict[tuple[int, int, int], Q]


def sha(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def unknown_json(uid) -> list:
    return [uid[0], list(uid[1])]


def representation_digest(vec: dict) -> str:
    return vc.global_vector_digest(vec)


def assert_direct_authority_independence(source_text: str | None = None) -> dict:
    path = HERE / "t3_011_c.py"
    text = path.read_text() if source_text is None else source_text
    tree = ast.parse(text, filename=str(path))
    direct_functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("direct_")
    }
    if not direct_functions:
        raise AssertionError("T3-011-C direct authority functions absent")
    banned = {
        "b.primitive_shift_atom", "b.specialize_poly", "b.response_vector",
        "p.lifted_delta_monomial", "p.lifted_global_column",
        "va.lifted_delta", "va.lifted_global_column",
        "vb.delta_atom", "vb.sp", "vb.response",
    }

    def dotted(node):
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
        return ".".join(reversed(parts))

    seen = set()
    for fn in direct_functions.values():
        for node in ast.walk(fn):
            if isinstance(node, ast.Call):
                name = dotted(node.func)
                if name:
                    seen.add(name)
    overlap = sorted(seen & banned)
    if overlap:
        raise AssertionError(f"direct audit path reuses forbidden response authority: {overlap}")
    return {
        "direct_function_count": len(direct_functions),
        "forbidden_helper_overlap": overlap,
        "source_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def verifier_original_monomial(mon):
    out = a.rc.p_const(1)
    for name in mon:
        out = a.rc.p_mul(out, a.rc.p_atom(name))
    return out


def verifier_shifted_monomial(mon, shift):
    out = a.rc.p_const(1)
    for name in mon:
        out = a.rc.p_mul(out, a.rc.p_add(a.rc.p_atom(name), vb.delta_atom(name, shift)))
    return out


def coordinate_factor(channel):
    if channel in ("n1", "n2", "n3"):
        return (1, 0, 0, 0)
    if channel == "k1":
        return (0, 1, 0, 0)
    if channel == "l1":
        return (0, 0, 1, 0)
    raise ValueError(channel)


def verifier_coordinate_rat(channel):
    return a.rc.r_factor(coordinate_factor(channel), exponent=1)


def verifier_shifted_coordinate_rat(channel):
    return a.rc.r_add(verifier_coordinate_rat(channel), a.rc.r_const(CHANNEL_INCREMENT[channel]))


def verifier_fd_poly(mon, channel):
    shift = a.pcl.SHIFTS[channel]
    original = verifier_original_monomial(mon)
    shifted = verifier_shifted_monomial(mon, shift)
    x0 = verifier_coordinate_rat(channel)
    x1 = verifier_shifted_coordinate_rat(channel)
    return a.rc.p_add(
        a.rc.p_scale(shifted, x1),
        a.rc.p_scale(original, a.rc.r_scale(x0, -1)),
    )


def verifier_product_rule_poly(mon, channel):
    shift = a.pcl.SHIFTS[channel]
    original = verifier_original_monomial(mon)
    shifted = verifier_shifted_monomial(mon, shift)
    delta = a.rc.p_add(shifted, a.rc.p_scale(original, -1))
    return a.rc.p_add(
        a.rc.p_scale(delta, verifier_coordinate_rat(channel)),
        a.rc.p_scale(shifted, Q(CHANNEL_INCREMENT[channel])),
    )


def verifier_global_column(raw, scalar, channel, strata, active):
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


def independent_active_namespace(channel, strata, specialized, supports):
    active = set()
    for st in reversed(strata):
        primitive = specialized[st["id"]]
        for block in reversed(vc.BLOCK_ORDER):
            rec, _target, _cols, _ids = vb.cell(
                primitive, supports[(channel, block)], channel, block, st
            )
            if rec["classification"] != "STRUCTURAL_ZERO":
                active.add(f"{channel}:{block}:{st['id']}")
    return active


# Independent implementation of the exact rational-function normal form used
# for comparison.  It does not import the C producer or sample numeric points.
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


def _linear_poly(factor) -> Poly3:
    an, ak, al, d = factor
    out: Poly3 = {}
    for mon, coeff in (((1, 0, 0), an), ((0, 1, 0), ak), ((0, 0, 1), al), ((0, 0, 0), d)):
        if coeff:
            out[mon] = Q(coeff)
    return out


def _p3_pow_linear(factor, exponent: int) -> Poly3:
    if exponent < 0:
        raise AssertionError("negative exponent entered verifier polynomial numerator")
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
                raise AssertionError(f"verifier common denominator underflow at {factor}: {power}")
            if power:
                term = _p3_mul(term, _p3_pow_linear(factor, power))
        out = _p3_add(out, term)
    return out


def _poly3_rows(poly: Poly3) -> list[list[int]]:
    return [[an, ak, al, q.numerator, q.denominator] for (an, ak, al), q in sorted(poly.items())]


def _den_rows(den: dict) -> list[list]:
    return [[list(f), e] for f, e in sorted(den.items()) if e]


def _vector_rat_map(vec: dict) -> dict:
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


def semantic_bundle(vectors: list[dict]) -> dict:
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


def verify_candidate(row, channel, uid, strata, active):
    if row.get("candidate") != unknown_json(uid):
        raise AssertionError(f"T3-011-C candidate order drift: {channel}")
    if row.get("coordinate_increment") != CHANNEL_INCREMENT[channel]:
        raise AssertionError(f"T3-011-C per-candidate increment drift: {channel}:{uid}")
    if row.get("semantic_normal_form") != SEMANTIC_NORMAL_FORM:
        raise AssertionError(f"T3-011-C semantic normal form drift: {channel}:{uid}")
    scalar, mon = uid
    fd = verifier_global_column(verifier_fd_poly(mon, channel), scalar, channel, strata, active)
    product = verifier_global_column(verifier_product_rule_poly(mon, channel), scalar, channel, strata, active)
    producer = p.lifted_global_column(channel, uid, strata, active)
    old_verifier = va.lifted_global_column(channel, uid, strata, active)
    vectors = [fd, product, producer, old_verifier]
    sem = semantic_bundle(vectors)
    labels = ["direct_finite_difference", "direct_product_rule", "t3_011_b_producer", "t3_011_b_verifier"]
    for i, label in enumerate(labels):
        if row.get(f"{label}_sha256") != sem["semantic_sha256"][i]:
            raise AssertionError(f"T3-011-C semantic response digest drift: {channel}:{uid}:{label}")
        if row.get(f"{label}_representation_sha256") != representation_digest(vectors[i]):
            raise AssertionError(f"T3-011-C representation digest drift: {channel}:{uid}:{label}")
    if row.get("semantic_base_coordinate_count") != sem["base_coordinate_count"]:
        raise AssertionError(f"T3-011-C semantic coordinate count drift: {channel}:{uid}")
    flags = {
        "direct_finite_difference_equals_product_rule": sem["equals_direct"][1],
        "direct_equals_t3_011_b_producer": sem["equals_direct"][2],
        "direct_equals_t3_011_b_verifier": sem["equals_direct"][3],
    }
    for key, want in flags.items():
        if row.get(key) != want:
            raise AssertionError(f"T3-011-C concordance flag drift: {channel}:{uid}:{key}")
    all_equal = all(flags.values())
    if row.get("all_three_existing_paths_plus_product_rule_concordant") != all_equal:
        raise AssertionError(f"T3-011-C aggregate concordance drift: {channel}:{uid}")
    return all_equal


def verify(result: dict) -> dict:
    if result.get("stage") != STAGE or result.get("audit_class") != AUDIT_ID:
        raise AssertionError("T3-011-C identity drift")
    checkpoint = result.get("predecessor_checkpoint", {})
    if checkpoint.get("reviewed_head") != B_REVIEWED_HEAD:
        raise AssertionError("T3-011-B reviewed-head drift")
    if checkpoint.get("merge_commit") != B_MERGE_COMMIT:
        raise AssertionError("T3-011-B merge checkpoint drift")
    if checkpoint.get("required_terminal") != B_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-B terminal checkpoint drift")
    for name, want in B_BLOBS.items():
        if a.git_blob_sha1(HERE / name) != want:
            raise AssertionError(f"T3-011-B source blob drift in C verifier: {name}")
        if checkpoint.get("source_blobs", {}).get(name) != want:
            raise AssertionError(f"T3-011-C reported source blob drift: {name}")

    contract = json.loads((HERE / "T3_011_C_CONTRACT.json").read_text())
    if contract["stage"] != STAGE or contract["audit_class"]["id"] != AUDIT_ID:
        raise AssertionError("T3-011-C contract identity drift")
    if contract["predecessor"]["reviewed_head"] != B_REVIEWED_HEAD or contract["predecessor"]["merge_commit"] != B_MERGE_COMMIT:
        raise AssertionError("T3-011-C contract predecessor drift")
    if contract["candidate_bank"]["expected_candidate_counts"] != EXPECTED_COUNTS:
        raise AssertionError("T3-011-C contract candidate counts drift")
    if contract["candidate_bank"]["expected_independent_trials"] != 311 or contract["candidate_bank"]["expected_mirror_l1_checks"] != 110:
        raise AssertionError("T3-011-C contract audit cardinality drift")
    if contract["direct_response"]["channel_coordinate_increment"] != CHANNEL_INCREMENT:
        raise AssertionError("T3-011-C contract coordinate increments drift")
    if contract["direct_response"]["direct_authority_id"] != DIRECT_AUTHORITY_ID:
        raise AssertionError("T3-011-C direct authority identity drift")
    if contract["direct_response"].get("semantic_normal_form") != SEMANTIC_NORMAL_FORM:
        raise AssertionError("T3-011-C contract semantic normal form drift")

    direct_meta = result.get("direct_reconstruction", {})
    if direct_meta.get("authority_id") != DIRECT_AUTHORITY_ID:
        raise AssertionError("T3-011-C result direct authority drift")
    if direct_meta.get("channel_coordinate_increment") != CHANNEL_INCREMENT:
        raise AssertionError("T3-011-C result increment drift")
    if direct_meta.get("semantic_normal_form") != SEMANTIC_NORMAL_FORM or direct_meta.get("finite_sampling_used") is not False:
        raise AssertionError("T3-011-C result exact semantic normal form drift")
    if direct_meta.get("uses_t3_011_b_generator_as_direct_authority") or direct_meta.get("uses_t3_011_b_verifier_generator_as_direct_authority"):
        raise AssertionError("T3-011-C predecessor response generator imported as direct authority")

    for key in (
        "new_candidates_authorized", "pairs_or_two_lifts_authorized",
        "arbitrary_linear_combination_search_authorized", "generic_degree1_envelope_authorized",
        "support_or_harmonic_enlargement_authorized", "rational_prefactors_authorized",
        "adaptive_basis_growth_authorized", "raw_jet_reopening_authorized",
        "recurrence_search_authorized", "correction_layer_recombination_authorized",
        "theorem_promotion_authorized", "residual_sum_zero_proved",
    ):
        if result.get(key) is not False:
            raise AssertionError(f"T3-011-C claim firewall drift: {key}")
    if result.get("proof_effect") != "NONE" or result.get("promotion_effect") != "NONE" or result.get("t3_status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        raise AssertionError("T3-011-C claim status inflation")

    source_independence = assert_direct_authority_independence()
    predecessor_producer.assert_a_locks()
    p.assert_c_locks()
    c.assert_b_locks()
    a.assert_source_locks()
    a.validate_architecture()
    layer, predecessor = a.pcl.build_layer()
    if predecessor["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 layer drift in C verifier")
    primitive_full = a.primitive_oriented_layer(layer)
    strata = a.shell_strata()
    if direct_meta.get("strata_semantics_sha256") != sha([[st["id"], st["k_offset"], st["l_offset"]] for st in strata]):
        raise AssertionError("T3-011-C shell/strata semantics drift")
    specialized = {
        st["id"]: a.primitive_oriented_layer(a.specialize_layer(layer, st["k_offset"], st["l_offset"]))
        for st in strata
    }
    supports = {
        (channel, block): vb.support(primitive_full, channel, block)
        for channel in a.CHANNEL_SCALARS
        for block in vc.BLOCK_ORDER
    }

    records = {rec["channel"]: rec for rec in result.get("channel_audits", [])}
    if set(records) != set(a.INDEPENDENT_CHANNELS):
        raise AssertionError("T3-011-C channel audit cardinality drift")
    total = 0
    mismatches = 0
    k1_candidates = None
    for channel in a.INDEPENDENT_CHANNELS:
        base, ids, cols, _target = vc.reconstruct_channel(channel, strata, specialized, supports)
        if base["classification"] != "EXACTLY_INCONSISTENT":
            raise AssertionError(f"T3-011-C reverse C base drift: {channel}")
        candidates = [uid for uid, col in zip(ids, cols) if col]
        if len(candidates) != EXPECTED_COUNTS[channel]:
            raise AssertionError(f"T3-011-C reverse candidate count drift: {channel}")
        active = independent_active_namespace(channel, strata, specialized, supports)
        rec = records[channel]
        if rec.get("candidate_count") != len(candidates):
            raise AssertionError(f"T3-011-C reported candidate count drift: {channel}")
        if rec.get("candidate_order_sha256") != sha([unknown_json(uid) for uid in candidates]):
            raise AssertionError(f"T3-011-C candidate order digest drift: {channel}")
        if rec.get("active_cell_count") != len(active) or rec.get("active_cell_sha256") != sha(sorted(active)):
            raise AssertionError(f"T3-011-C active-cell namespace drift: {channel}")
        rows = rec.get("candidates", [])
        if len(rows) != len(candidates):
            raise AssertionError(f"T3-011-C candidate ledger count drift: {channel}")
        local_mismatch = sum(not verify_candidate(row, channel, uid, strata, active) for row, uid in zip(rows, candidates))
        if rec.get("mismatch_count") != local_mismatch or rec.get("all_candidates_concordant") != (local_mismatch == 0):
            raise AssertionError(f"T3-011-C channel mismatch ledger drift: {channel}")
        total += len(candidates)
        mismatches += local_mismatch
        if channel == "k1":
            k1_candidates = candidates

    if total != 311 or result.get("independent_candidate_count") != 311 or result.get("independent_mismatch_count") != mismatches:
        raise AssertionError("T3-011-C aggregate independent ledger drift")
    if k1_candidates is None:
        raise AssertionError("T3-011-C k1 candidate bank absent")

    mirror = result.get("mirror_l1_audit", {})
    if mirror.get("candidate_count") != 110 or mirror.get("source_k1_order_sha256") != sha([unknown_json(uid) for uid in k1_candidates]):
        raise AssertionError("T3-011-C l1 mirror source drift")
    mirror_rows = mirror.get("candidates", [])
    if len(mirror_rows) != 110:
        raise AssertionError("T3-011-C l1 mirror ledger cardinality drift")
    lactive = independent_active_namespace("l1", strata, specialized, supports)
    if mirror.get("active_cell_count") != len(lactive) or mirror.get("active_cell_sha256") != sha(sorted(lactive)):
        raise AssertionError("T3-011-C l1 active-cell namespace drift")
    mirror_mismatch = 0
    for row, kuid in zip(mirror_rows, k1_candidates):
        if row.get("source_k1_candidate") != unknown_json(kuid):
            raise AssertionError("T3-011-C l1 mirror source marker drift")
        luid = vc.mirror_unknown_k_to_l(kuid)
        if not verify_candidate(row, "l1", luid, strata, lactive):
            mirror_mismatch += 1
    if mirror.get("mismatch_count") != mirror_mismatch or mirror.get("all_candidates_concordant") != (mirror_mismatch == 0):
        raise AssertionError("T3-011-C l1 mismatch ledger drift")

    all_concordant = mismatches == 0 and mirror_mismatch == 0
    if result.get("all_frozen_responses_concordant") != all_concordant:
        raise AssertionError("T3-011-C aggregate concordance terminal drift")
    expected_terminal = (
        "T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_CERTIFIED"
        if all_concordant
        else "T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_MISMATCH"
    )
    if result.get("terminal") != expected_terminal:
        raise AssertionError("T3-011-C terminal drift")
    return {
        "status": "INDEPENDENT_T3_011_C_RESPONSE_GENERATOR_SEMANTICS_AUDIT_REPLAY_COMPLETE",
        "independent_candidate_count": total,
        "mirror_l1_check_count": len(mirror_rows),
        "mismatch_count": mismatches + mirror_mismatch,
        "semantic_normal_form": SEMANTIC_NORMAL_FORM,
        "finite_sampling_used": False,
        "terminal": expected_terminal,
        "direct_authority_source_independence": source_independence,
        "audit_producer_imported_as_authority": False,
        "t3_011_b_producer_generator_compared_not_trusted": True,
        "t3_011_b_verifier_generator_compared_not_trusted": True,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    proc = subprocess.run([sys.executable, str(HERE / "t3_011_c.py")], check=True, capture_output=True, text=True)
    result = json.loads(proc.stdout)
    print(json.dumps(verify(result), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
