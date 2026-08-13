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

import t3_011_b as predecessor  # noqa: E402

p = predecessor.p
c = predecessor.c
b = predecessor.b
a = predecessor.a

OPERATION = "OZ-RT-BZ-T3-011-D"
STAGE = "T3_011_D_MINIMAL_COKERNEL_BREAKING_POLYNOMIAL_DEGREE_EXTENSION"
CLASS_ID = "SUPPORT_LOCKED_SINGLE_CHANNEL_QUADRATIC_NONZERO_RESPONSE_LIFT_001"
ISSUE = 498
DEGREE = 2
C_REVIEWED_HEAD = "a24b1f4aa17e2b42e2288d3e6a19d0c636f42060"
C_MERGE_COMMIT = "6ee10e932c696cc327e6470748c10790dc8ca7d3"
C_REQUIRED_TERMINAL = "T3_011_B_LIFTED_RESPONSE_GENERATOR_SEMANTICS_CERTIFIED"
C_BLOBS = {
    "t3_011_c.py": "772e1e3d9c5624952ded42743137b8e64e9e1da7",
    "T3_011_C_CONTRACT.json": "ffc84ae0b9089e31bf558b5f68196b53d85f80df",
    "verify_t3_011_c.py": "9dd80cc7d6bfd706b350ba13c3ca8e3715c89cb6",
}
EXPECTED_COUNTS = {"n1": 67, "n2": 67, "n3": 67, "k1": 110}
CHANNEL_INCREMENT = {"n1": 1, "n2": 2, "n3": 3, "k1": 1, "l1": 1}
CHANNEL_COORDINATE = {"n1": "n", "n2": "n", "n3": "n", "k1": "k", "l1": "l"}
POSITIVE_TERMINAL = "MINIMAL_SINGLE_CHANNEL_QUADRATIC_COKERNEL_BREAKING_DIRECTION_FOUND"
NEGATIVE_TERMINAL = "SINGLE_CHANNEL_QUADRATIC_RESPONSE_CLASS_COKERNEL_INVISIBLE"

Unknown = p.Unknown
GlobalVector = p.GlobalVector


def sha(obj: object) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def qjson(x: Q) -> list[int]:
    return [x.numerator, x.denominator]


def unknown_json(uid: Unknown) -> list:
    return [uid[0], list(uid[1])]


def assert_c_locks() -> dict[str, str]:
    got = {}
    for name, want in C_BLOBS.items():
        value = a.git_blob_sha1(HERE / name)
        if value != want:
            raise AssertionError(f"T3-011-C source lock drift: {name}: {value} != {want}")
        got[name] = value
    contract = json.loads((HERE / "T3_011_C_CONTRACT.json").read_text())
    if contract.get("stage") != "T3_011_C_DIRECT_DISCRETE_PRODUCT_RULE_RESPONSE_GENERATOR_SEMANTICS_AUDIT":
        raise AssertionError("T3-011-C contract stage drift")
    if contract.get("terminals", {}).get("certified") != C_REQUIRED_TERMINAL:
        raise AssertionError("T3-011-C certified terminal drift")
    if contract.get("candidate_bank", {}).get("expected_independent_trials") != 311:
        raise AssertionError("T3-011-C candidate bank drift")
    return got


def validate_operation_parameters(
    degree: int = DEGREE,
    increments: dict[str, int] | None = None,
    pairs_admitted: bool = False,
    mixed_channels_admitted: bool = False,
) -> None:
    if degree != 2:
        raise AssertionError("T3-011-D admits polynomial degree 2 only")
    if increments is not None and increments != CHANNEL_INCREMENT:
        raise AssertionError("T3-011-D coordinate increment drift")
    if pairs_admitted:
        raise AssertionError("T3-011-D pair/two-lift search is forbidden")
    if mixed_channels_admitted:
        raise AssertionError("T3-011-D mixed-channel multipliers are forbidden")


def quadratic_delta_monomial(
    mon: tuple[str, ...],
    channel: str,
    degree: int = DEGREE,
    increment_override: int | None = None,
):
    validate_operation_parameters(degree=degree)
    if increment_override is not None and increment_override != CHANNEL_INCREMENT[channel]:
        raise AssertionError("quadratic response increment drift")
    shift = a.pcl.SHIFTS[channel]
    f0, f1 = p.channel_coordinate_factors(channel)
    shifted = p.shifted_monomial_poly(mon, shift)
    original = p.monomial_poly(mon)
    return a.rc.p_add(
        a.rc.p_scale(shifted, a.rc.r_factor(f1, exponent=2)),
        a.rc.p_scale(original, a.rc.r_factor(f0, exponent=2, scale=-1)),
    )


def quadratic_global_column(
    channel: str,
    uid: Unknown,
    strata: list[dict],
    active_cell_ids: set[str],
    degree: int = DEGREE,
) -> GlobalVector:
    scalar, mon = uid
    raw = quadratic_delta_monomial(mon, channel, degree=degree)
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


def build_context():
    predecessor.assert_a_locks()
    p.assert_c_locks()
    c.assert_b_locks()
    b.assert_a_locks()
    a.assert_source_locks()
    a.validate_architecture()

    layer, prior = a.pcl.build_layer()
    if prior["final_layer"]["sha256"] != a.PREDECESSOR_LAYER_SHA256:
        raise AssertionError("T3-009 coefficient-layer digest drift in T3-011-D")
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
    return primitive_full, strata, specialized, supports


def channel_bank(channel, primitive_full, strata, specialized, supports):
    base, ids, cols, target = c.build_channel_system(
        channel, primitive_full, strata, specialized, supports
    )
    if base["classification"] != "EXACTLY_INCONSISTENT":
        raise AssertionError(f"T3-011-D requires inconsistent base: {channel}")
    candidates = [uid for uid, col in zip(ids, cols) if col]
    if channel in EXPECTED_COUNTS and len(candidates) != EXPECTED_COUNTS[channel]:
        raise AssertionError(f"T3-011-D candidate bank drift: {channel}")
    active = {row["id"] for row in base["active_cells"]}
    witness, residual = p.cokernel_witness(cols, target)
    if p.pairing(witness, target) != 1:
        raise AssertionError(f"T3-011-D witness normalization drift: {channel}")
    for col in cols:
        if p.pairing(witness, col):
            raise AssertionError(f"T3-011-D witness no longer annihilates base: {channel}")
    return base, ids, cols, target, candidates, active, witness, residual


def scan_channel(channel, candidates, strata, active, witness, start_ordinal):
    rows = []
    found = None
    for local_index, uid in enumerate(candidates):
        lift = quadratic_global_column(channel, uid, strata, active)
        pairing = p.pairing(witness, lift)
        row = {
            "ordinal": start_ordinal + local_index,
            "channel": channel,
            "candidate": unknown_json(uid),
            "coordinate": CHANNEL_COORDINATE[channel],
            "coordinate_increment": CHANNEL_INCREMENT[channel],
            "polynomial_degree": DEGREE,
            "quadratic_response_sha256": c.global_vector_digest(lift),
            "obstruction_pairing": qjson(pairing),
            "obstruction_pairing_nonzero": bool(pairing),
        }
        rows.append(row)
        if pairing:
            found = row
            break
    return rows, found


def build() -> dict:
    validate_operation_parameters(increments=CHANNEL_INCREMENT)
    c_locks = assert_c_locks()
    primitive_full, strata, specialized, supports = build_context()

    independent_rows = []
    channel_ledgers = []
    first = None
    ordinal = 0
    k1_candidates = None

    for channel in a.INDEPENDENT_CHANNELS:
        base, _ids, _cols, _target, candidates, active, witness, residual = channel_bank(
            channel, primitive_full, strata, specialized, supports
        )
        if channel == "k1":
            k1_candidates = list(candidates)
        rows, found = scan_channel(channel, candidates, strata, active, witness, ordinal)
        independent_rows.extend(rows)
        channel_ledgers.append({
            "channel": channel,
            "frozen_candidate_count": len(candidates),
            "candidate_order_sha256": sha([unknown_json(uid) for uid in candidates]),
            "active_cell_count": len(active),
            "active_cell_sha256": sha(sorted(active)),
            "cokernel_witness_sha256": p.sha(p.witness_rows(witness)),
            "target_quotient_residual_sha256": c.global_vector_digest(residual),
            "tested_prefix_count": len(rows),
            "first_nonzero_pairing": found,
        })
        ordinal += len(candidates)
        if found is not None:
            first = found
            break

    if sum(EXPECTED_COUNTS.values()) != 311:
        raise AssertionError("internal frozen candidate cardinality drift")
    if k1_candidates is None and first is None:
        raise AssertionError("k1 candidate bank was not reconstructed")

    mirror_rows = []
    mirror_ledger = {
        "source_channel": "k1",
        "tested": False,
        "candidate_count": 0,
        "candidate_order_sha256": None,
        "active_cell_count": 0,
        "active_cell_sha256": None,
        "cokernel_witness_sha256": None,
        "first_nonzero_pairing": None,
    }

    if first is None:
        if k1_candidates is None or len(k1_candidates) != EXPECTED_COUNTS["k1"]:
            raise AssertionError("mirror source bank drift")
        _lbase, _lids, _lcols, _ltarget, _lcandidates, lactive, lwitness, lresidual = channel_bank(
            "l1", primitive_full, strata, specialized, supports
        )
        mirrored = [c.mirror_unknown_k_to_l(uid) for uid in k1_candidates]
        mirror_ledger.update({
            "tested": True,
            "candidate_count": len(mirrored),
            "candidate_order_sha256": sha([unknown_json(uid) for uid in mirrored]),
            "active_cell_count": len(lactive),
            "active_cell_sha256": sha(sorted(lactive)),
            "cokernel_witness_sha256": p.sha(p.witness_rows(lwitness)),
            "target_quotient_residual_sha256": c.global_vector_digest(lresidual),
        })
        rows, found = scan_channel("l1", mirrored, strata, lactive, lwitness, 311)
        for source, row in zip(k1_candidates, rows):
            row["source_k1_candidate"] = unknown_json(source)
        mirror_rows.extend(rows)
        mirror_ledger["first_nonzero_pairing"] = found
        if found is not None:
            first = found

    if first is None and len(independent_rows) != 311:
        raise AssertionError("negative terminal requires full independent quadratic sweep")
    if first is None and len(mirror_rows) != 110:
        raise AssertionError("negative terminal requires full mirror-derived l1 sweep")

    terminal = POSITIVE_TERMINAL if first is not None else NEGATIVE_TERMINAL

    return {
        "schema_version": "1.0.0",
        "issue": ISSUE,
        "operation": OPERATION,
        "stage": STAGE,
        "status": "MINIMAL_POLYNOMIAL_DEGREE_EXTENSION_COMPLETE",
        "predecessor_checkpoint": {
            "reviewed_head": C_REVIEWED_HEAD,
            "merge_commit": C_MERGE_COMMIT,
            "source_blobs": c_locks,
            "required_terminal": C_REQUIRED_TERMINAL,
        },
        "bounded_extension_class": {
            "id": CLASS_ID,
            "only_changed_dimension": "coordinate_multiplier_polynomial_degree",
            "predecessor_degree": 1,
            "admitted_degree": 2,
            "coordinate_multiplier": "x_c^2",
            "direct_finite_difference": "(x_c+h_c)^2 S_c(G)-x_c^2 G",
            "product_rule": "x_c^2 Delta_c(G)+(2 h_c x_c+h_c^2)S_c(G)",
            "channel_coordinate_increment": CHANNEL_INCREMENT,
            "independent_candidate_count": 311,
            "mirror_derived_l1_count": 110,
            "stop_at_first_nonzero_pairing": True,
            "pairs_admitted": False,
            "mixed_channel_monomials_admitted": False,
            "arbitrary_polynomial_envelope_admitted": False,
            "degree_gt_2_admitted": False,
            "support_enlargement_admitted": False,
            "harmonic_enlargement_admitted": False,
            "rational_prefactors_admitted": False,
            "adaptive_basis_growth_admitted": False,
            "raw_jet_reopened": False,
            "recurrence_search": False,
        },
        "channel_ledgers": channel_ledgers,
        "tested_independent_prefix_count": len(independent_rows),
        "tested_independent_prefix": independent_rows,
        "mirror_l1": {
            **mirror_ledger,
            "tested_prefix_count": len(mirror_rows),
            "tested_prefix": mirror_rows,
        },
        "first_cokernel_breaking_direction": first,
        "polynomial_degree_alone_breaks_cokernel_obstruction": first is not None,
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
