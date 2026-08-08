#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

PKG = Path(__file__).resolve().parent
RECORD = PKG / "OZ_RT_SHARP12_DEPTH_001.json"
SCHEMA = PKG / "OZ_RT_SHARP12_DEPTH_001.schema.json"

EXPECTED_ARTIFACT_IDS = {
    "DEPTH-PRODUCER-001",
    "DEPTH-VARIABLE-ORDER-001",
    "DEPTH-FITTING-ROW-ORDER-001",
    "DEPTH-RAW-ROW-ORDER-001",
    "DEPTH-NORMALIZATION-001",
    "DEPTH-FITTING-MATRIX-001",
    "DEPTH-DEPTH-MATRIX-001",
    "DEPTH-JOINT-MATRIX-001",
    "DEPTH-AUGMENTED-MATRIX-001",
}
EXPECTED_REOPEN_IDS = {f"REOPEN-{i:02d}" for i in range(1, 8)}


def load_record() -> dict:
    return json.loads(RECORD.read_text(encoding="utf-8"))


def errors(record: dict | None = None) -> list[str]:
    record = load_record() if record is None else record
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    out = [
        f"schema{err.json_path}: {err.message}"
        for err in Draft202012Validator(schema).iter_errors(record)
    ]

    target = record.get("target_lock", {})
    if target.get("upstream_commit") != "790685b7ee4f642a8a88a1bd120636d1b8b39ea8":
        out.append("upstream commit drift")
    if target.get("upstream_tree") != "646ee73dd9066e059b043fad64fb20959f111cbf":
        out.append("upstream tree drift")
    sharp = target.get("sharp12_source", {})
    if sharp.get("blob") != "6a347e2a483ec781afac98016635ce1d73b3c38e":
        out.append("Sharp-12 source blob drift")

    audit = record.get("audit_scope", {})
    if audit.get("result") != "CANONICAL_DEPTH_PRODUCER_AND_ORDER_ARTIFACTS_NOT_RECOVERABLE_FROM_EXACT_TREE":
        out.append("absence result drift")
    if audit.get("tree_listing_examined") is not True:
        out.append("exact-tree audit must remain explicit")
    if len(audit.get("admitted_replays_examined", [])) != 5:
        out.append("all five admitted source-revision replays must remain enumerated")

    observations = record.get("source_observations", {})
    expected_numeric = {
        "variables": 448,
        "fitting_equations_n": 600,
        "raw_depth_condition_rows": 68,
        "independent_depth_conditions": 42,
        "fitting_rank": 313,
        "joint_rank": 324,
        "augmented_joint_rank": 324,
        "source_reported_solution_dimension": 124,
        "additional_independent_depth_conditions_beyond_fitting": 11,
    }
    for key, value in expected_numeric.items():
        if observations.get(key) != value:
            out.append(f"source-observation drift: {key}")
    if observations.get("auxiliary_primes") != [33554393, 33554467]:
        out.append("auxiliary-prime drift")
    if observations.get("rational_certificate_independently_replayable") is not False:
        out.append("rational certificate falsely promoted")

    artifact_ids = {row.get("id") for row in record.get("unrecoverable_producer_order_artifacts", [])}
    if artifact_ids != EXPECTED_ARTIFACT_IDS:
        out.append("unrecoverable producer/order artifact ledger incomplete")

    downstream = {row.get("id"): row for row in record.get("downstream_certificate_blockers", [])}
    if set(downstream) != {
        "DEPTH-RATIONAL-CONSISTENCY-001",
        "DEPTH-RATIONAL-RANK-001",
        "DEPTH-MODULAR-PIVOTS-001",
    }:
        out.append("downstream certificate blocker ledger incomplete")
    if downstream.get("DEPTH-MODULAR-PIVOTS-001", {}).get("state") != "NOT_RECOVERABLE_AS_EXACT_TRANSCRIPTS":
        out.append("modular pivot transcript absence drift")

    reopen_ids = {row.get("id") for row in record.get("reopening_requirements", [])}
    if reopen_ids != EXPECTED_REOPEN_IDS:
        out.append("reopening requirements incomplete")

    nonclaims = record.get("nonclaims", {})
    if any(value is not False for value in nonclaims.values()):
        out.append("nonclaim boundary opened")
    for required in (
        "depth_certified",
        "t1_top_proved",
        "sharp12_proved",
        "t3_proved",
        "t3_refuted",
        "quarantined_lean_repaired",
        "prime_2_covered",
        "prime_3_covered",
        "mathcert_adjudicated",
        "new_irrationality_claim",
        "sharp12_gate_open",
    ):
        if nonclaims.get(required) is not False:
            out.append(f"required nonclaim drift: {required}")

    disposition = record.get("disposition", {})
    if record.get("terminal_disposition") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        out.append("terminal disposition drift")
    if disposition.get("status") != "OPEN_WITH_CHARACTERIZED_BLOCKER":
        out.append("disposition status drift")
    if disposition.get("proof_effect") != "NONE" or disposition.get("promotion_effect") != "NONE":
        out.append("blocker package may not promote a mathematical claim")
    if disposition.get("reopen_only_on_requirements_satisfied") is not True:
        out.append("reopening gate weakened")
    return out


def main() -> int:
    found = errors()
    if found:
        for item in found:
            print(item, file=sys.stderr)
        print(f"OZ Sharp-12 DEPTH blocker validation failed with {len(found)} error(s)", file=sys.stderr)
        return 1
    print(
        "OZ Sharp-12 DEPTH exact-tree absence audit is valid: canonical producer/order artifacts "
        "remain unrecoverable, all nonclaims remain closed, and disposition is "
        "OPEN_WITH_CHARACTERIZED_BLOCKER"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
