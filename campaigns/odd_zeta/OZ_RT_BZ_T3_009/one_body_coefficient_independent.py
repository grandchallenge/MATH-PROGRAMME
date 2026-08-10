#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import one_body_coefficient_verify as iv

HERE = Path(__file__).resolve().parent
RESULT = HERE / "ONE_BODY_COEFFICIENT_LAYER.json"


def canonical_rows(layer):
    rows = []
    for mon in sorted(layer):
        terms = []
        for scalar in iv.SCALARS:
            coeff = layer[mon].get(scalar)
            if coeff:
                terms.append([scalar, iv.rc.rat_json(coeff)])
        rows.append([list(mon), terms])
    return rows


def digest_rows(rows) -> str:
    raw = json.dumps(rows, separators=(",", ":"), sort_keys=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def verify() -> dict:
    retained = json.loads(RESULT.read_text(encoding="utf-8"))
    if retained["execution_boundary"] != "FULL_POLE_FREE_ONE_BODY_RESIDUAL_COEFFICIENT_LAYER_001":
        raise AssertionError("execution boundary drift")
    if retained["proof_effect"] != "NONE" or retained["promotion_effect"] != "NONE" or retained["residual_sum_zero_proved"]:
        raise AssertionError("claim inflation")

    lock_map = {
        "RESIDUAL_CANONICAL_RESULT.json": retained["source_locks"]["residual_canonical_result_blob"],
        "ONE_BODY_STRUCTURE_RESULT.json": retained["source_locks"]["one_body_structure_result_blob"],
        "NESTED_DERIVATIVE_CERTIFICATE_ROUTE.json": retained["source_locks"]["nested_derivative_certificate_route_blob"],
        "QROW_SYMMETRIC_GAUGE.json": retained["source_locks"]["qrow_symmetric_gauge_blob"],
    }
    if lock_map != iv.SOURCE_BLOBS:
        raise AssertionError("source-lock declaration drift")
    for name, expected in iv.SOURCE_BLOBS.items():
        got = iv.git_blob_sha1(HERE / name)
        if got != expected:
            raise AssertionError(f"source blob drift {name}: {got}")

    layer, skeleton = iv.independent_expected_layer()
    rows = canonical_rows(layer)
    atoms = sorted({a for mon in layer for a in mon})
    digest = digest_rows(rows)

    final = retained["final_layer"]
    if final["monomials"] != len(layer):
        raise AssertionError("monomial count drift")
    if final["atoms"] != len(atoms) or final["atom_names"] != atoms:
        raise AssertionError("atom universe drift")
    if final["max_atomic_arity"] != max((len(mon) for mon in layer), default=0):
        raise AssertionError("atomic arity drift")
    if final["scalar_basis_size"] != len(iv.SCALARS):
        raise AssertionError("scalar basis size drift")
    if final["sha256"] != digest:
        raise AssertionError("independent coefficient-layer digest mismatch")
    if retained["nested_skeleton_exact_digests"] != skeleton:
        raise AssertionError("nested-skeleton digest drift")

    abel_checks = iv.verify_abel_sign_and_shift()
    return {
        "status": "INDEPENDENT_FULL_POLE_FREE_ONE_BODY_COEFFICIENT_REPLAY_COMPLETE",
        "monomials": len(layer),
        "atoms": len(atoms),
        "scalar_basis_size": len(iv.SCALARS),
        "sha256": digest,
        "nested_skeleton_channels_verified": len(skeleton),
        "abel_exact_checks": abel_checks,
        "full_rows_reconstructed_independently": True,
        "finite_sampling_used_as_sum_proof": False,
        "proof_effect": "NONE",
        "promotion_effect": "NONE",
        "t3_status": "OPEN_WITH_CHARACTERIZED_BLOCKER",
    }


def main() -> int:
    print(json.dumps(verify(), sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
