"""Fail-closed validation for OZ-SOURCE-REVISION-DELTA-002."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parent
RECORD_PATH = PACKAGE / "OZ_SOURCE_REVISION_DELTA_002.json"
SCHEMA_PATH = PACKAGE / "OZ_SOURCE_REVISION_DELTA_002.schema.json"
T3_PATH = ROOT / "campaigns/odd_zeta/OZ_RT_BZ_T3_001/OZ_RT_BZ_T3_001.json"

EXPECTED_CLASSES = {
    "PROVED_SOURCE_CLAIM_PENDING_INDEPENDENT_REPLAY",
    "VERIFIED_FINITE_OR_COMPUTER_ASSISTED",
    "CONJECTURAL",
    "EXCLUDED_OR_REFUTED_IN_RECORDED_SCOPE",
    "SUPERSEDED_OR_CORRECTED",
    "DOCUMENTARY_ONLY",
}
EXPECTED_BOUNDARY_FALSE = {
    "t3_proved",
    "t3_refuted",
    "depth_certified",
    "t1_top_certified",
    "sharp12_accepted",
    "novelty_assessed",
    "priority_assessed",
    "new_irrationality_conclusion",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors(record: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors.extend(
        f"schema{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path))
    )

    if set(record.get("claim_classes", [])) != EXPECTED_CLASSES:
        errors.append("claim_classes must equal the closed classification vocabulary")

    authority = record.get("authority", {})
    if authority.get("protected_source_pin") == authority.get("candidate_source_head"):
        errors.append("candidate source head must differ from the protected source pin")
    if authority.get("ahead_by") != 7:
        errors.append("the locked source delta must contain exactly seven commits")

    claims = record.get("claim_register", [])
    ids = [claim.get("id") for claim in claims]
    if len(ids) != len(set(ids)):
        errors.append("claim register IDs must be unique")
    unknown = {
        claim.get("classification")
        for claim in claims
        if claim.get("classification") not in EXPECTED_CLASSES
    }
    if unknown:
        errors.append(f"claim register contains unknown classifications: {sorted(unknown)}")
    if not any(claim.get("classification") == "CONJECTURAL" for claim in claims):
        errors.append("claim register must preserve at least one conjectural claim")
    if not any(
        claim.get("classification") == "EXCLUDED_OR_REFUTED_IN_RECORDED_SCOPE"
        for claim in claims
    ):
        errors.append("claim register must preserve bounded negative evidence")

    t3 = load_json(T3_PATH)
    concordance = record.get("t1_top_t3_concordance", {})
    if concordance.get("t3_status") != t3.get("disposition", {}).get("status"):
        errors.append("T1-top/T3 concordance must preserve the protected T3 disposition")
    if concordance.get("relation") != (
        "DISTINCT_REPRESENTATIVES_WITH_SHARED_TOP_ROW_TARGET_NO_ACCEPTED_EQUIVALENCE"
    ):
        errors.append("T1-top and T3 may not be silently identified")
    not_accepted = set(concordance.get("not_accepted", []))
    required_rejections = {
        "T3 is syntactically identical to T1-top.",
        "T3 alone proves T1-top for w5_I.",
        "T1-top for w5_I proves T3 without an independently checked homogeneous representative identity.",
    }
    if not required_rejections <= not_accepted:
        errors.append("T1-top/T3 inference firewall is incomplete")

    depth = record.get("depth_impact", {})
    expected_depth = {
        "variables": 448,
        "fitting_rank": 313,
        "joint_rank": 324,
        "augmented_joint_rank": 324,
        "solution_dimension": 124,
        "depth_conditions": 42,
        "additional_independent_depth_conditions": 11,
    }
    for key, expected in expected_depth.items():
        if depth.get(key) != expected:
            errors.append(f"depth_impact.{key} must equal {expected}")
    if depth.get("variables", 0) - depth.get("joint_rank", 0) != depth.get(
        "solution_dimension"
    ):
        errors.append("DEPTH dimension arithmetic is inconsistent")
    if depth.get("programme_state") != "UNPROVED_INPUT":
        errors.append("DEPTH must remain an unproved Programme input")
    if depth.get("promotion_allowed") is not False:
        errors.append("DEPTH promotion must remain prohibited")

    boundaries = record.get("boundaries", {})
    for key in EXPECTED_BOUNDARY_FALSE:
        if boundaries.get(key) is not False:
            errors.append(f"boundaries.{key} must remain false")
    if boundaries.get("existing_programme_source_pin_unchanged") is not True:
        errors.append("the protected Programme source pin must remain unchanged")
    if boundaries.get("mathcert_state") != "pending":
        errors.append("MATHCERT must remain pending")

    routes = {route.get("id"): route for route in record.get("route_recommendations", [])}
    if routes.get("OZ-ROUTE-R002", {}).get("state") != (
        "AUTHORIZED_AS_ISSUE_222_PENDING_DEPENDENCY"
    ):
        errors.append("DEPTH route must remain dependency-gated by issue #221")
    if routes.get("OZ-ROUTE-R004", {}).get("state") != (
        "PROHIBITED_UNTIL_DEPTH_AND_T1_TOP_ACCEPTED"
    ):
        errors.append("Sharp-12 Cert routing must remain prohibited")

    execution_state = record.get("execution_state")
    archive_state = authority.get("archive_digest_state")
    archive_sha = authority.get("archive_sha256")
    if execution_state == "PREPARED_PENDING_EXACT_REPLAY":
        if archive_state != "PENDING_EXACT_WORKFLOW_REPLAY" or archive_sha is not None:
            errors.append("prepared state must retain a null, pending archive digest")
        lean = record.get("lean_replay", {})
        if lean.get("aggregate_build") != "PENDING":
            errors.append("prepared state must not claim a completed Lean build")
        if lean.get("formal_promotion_allowed") is not False:
            errors.append("formal promotion must remain prohibited before replay")
    elif execution_state == "CLOSED":
        if archive_state != "EXACT_REPLAY_BOUND" or not isinstance(archive_sha, str):
            errors.append("closed state requires an exact archive digest")
        if record.get("required_closure_updates"):
            errors.append("closed state may not retain unresolved closure updates")

    return errors


def main() -> int:
    record = load_json(RECORD_PATH)
    errors = validation_errors(record)
    if errors:
        for error in errors:
            print(error)
        print(f"OZ source revision delta validation failed with {len(errors)} error(s)")
        return 1
    print(
        "OZ source revision delta package is fail-closed: source admission is pending, "
        "T1-top and T3 remain distinct, DEPTH remains unproved, and no claim is promoted"
    )
    return 0
