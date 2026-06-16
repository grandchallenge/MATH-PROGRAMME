#!/usr/bin/env python3
"""Validate MATHFORGE ResearchMath intake fixture RM-DIO-004."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path("fixtures/researchmath/RM-DIO-004")
REQUIRED_SOURCE_FIELDS = {
    "dataset",
    "paper_id",
    "question_link",
    "original_question",
    "self_contained_problem",
    "taxonomy_level_1",
    "taxonomy_level_2",
    "taxonomy_level_3",
    "open_status",
    "status_evidence",
    "status_evidence_urls",
}
FORBIDDEN_STATUSES = {"SOLVED", "CERTIFIED", "CHECKED", "CHECKED_GLOBAL_STATUS", "COMPLETE_INTEGER_CLASSIFICATION"}


class ResearchMathFixtureError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ResearchMathFixtureError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResearchMathFixtureError(f"{path}: cannot load JSON: {exc}") from exc
    require(isinstance(value, dict), f"{path}: top-level value must be an object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_polynomial_terms(terms: Any) -> None:
    require(isinstance(terms, list) and len(terms) == 4, "canonical polynomial must have four terms")
    expected = [
        {"coefficient": [1, 1], "exponents": [2, 0]},
        {"coefficient": [-1, 1], "exponents": [1, 0]},
        {"coefficient": [-1, 1], "exponents": [0, 5]},
        {"coefficient": [1, 1], "exponents": [0, 1]},
    ]
    require(terms == expected, "canonical polynomial must encode x^2 - x - y^5 + y in descending lex order")


def check_source_row(source: dict[str, Any]) -> None:
    require(REQUIRED_SOURCE_FIELDS <= set(source), "source row is missing required ResearchMath fields")
    dataset = source.get("dataset")
    require(isinstance(dataset, dict), "source dataset metadata must be an object")
    require(dataset.get("name") == "amphora/ResearchMath-14k", "wrong source dataset")
    require(dataset.get("split") == "test", "wrong source split")
    require(dataset.get("dataset_license") == "MIT", "source license must be preserved")
    require(dataset.get("row_source") == "huggingface_dataset_viewer_sample", "row source must be preserved")
    require(source.get("paper_id") == "07-workshop-problems", "unexpected paper_id")
    require(nonempty(source.get("question_link")), "question_link is required")
    require(source.get("open_status") == "unknown", "imported open_status must remain unknown")
    require("x^2 - x = y^5 - y" in source.get("original_question", ""), "original question changed")
    require(isinstance(source.get("status_evidence_urls"), list) and source["status_evidence_urls"], "evidence URLs required")


def check_problem_card(card: dict[str, Any], source_hash: str) -> None:
    require(card.get("fixture_id") == "RM-DIO-004", "problem card fixture_id mismatch")
    require(card.get("artifact_kind") == "researchmath_problem_card", "wrong artifact_kind")
    require(card.get("schema_version") == "1.0.0", "unsupported problem-card schema")
    require(card.get("source_row_sha256") == source_hash, "problem card source hash mismatch")
    status = card.get("status_audit")
    require(isinstance(status, dict), "status_audit must be an object")
    require(status.get("imported_open_status") == "unknown", "imported status must remain unknown")
    require(status.get("mathforge_audited_status") == "STATUS_UNVERIFIED_UNKNOWN", "audited status must be unverified unknown")
    require(status.get("promotion_allowed") is False, "ResearchMath intake must not allow status promotion")
    require(isinstance(status.get("promotion_blockers"), list) and len(status["promotion_blockers"]) >= 2, "promotion blockers required")

    extraction = card.get("algebraic_extraction")
    require(isinstance(extraction, dict), "algebraic_extraction must be an object")
    require(extraction.get("coefficient_domain") == {"kind": "integer_ring", "symbol": "ZZ"}, "coefficient domain must be ZZ")
    require(extraction.get("model_class") == "integer_points_on_affine_plane_curve", "model class changed")
    require(extraction.get("variables") == ["x", "y"], "variable order must be [x, y]")
    equations = extraction.get("equations")
    require(isinstance(equations, list) and len(equations) == 1, "exactly one extracted equation required")
    check_polynomial_terms(equations[0].get("canonical_polynomial"))
    excluded = extraction.get("excluded_relaxations")
    require(isinstance(excluded, list) and len(excluded) >= 3, "excluded relaxations are required")

    route = card.get("route_classification")
    require(isinstance(route, dict), "route_classification must be an object")
    require(route.get("primary_route") == "DIOPHANTINE_ALGEBRAIC_INTAKE", "wrong primary route")
    require(route.get("application_lane") == "APP-DIO-01", "wrong application lane")
    require(route.get("route_status") == "MATHFORGE_TRIAGE_READY", "wrong route status")
    require(nonempty(route.get("first_executable_step")), "first executable step required")
    require("not a completeness proof" in route["first_executable_step"], "first step must preserve finite-screen boundary")

    boundary = card.get("semantic_boundary")
    require(isinstance(boundary, dict), "semantic boundary required")
    require(nonempty(boundary.get("excluded_inference")), "excluded inference required")
    require("does not solve" in boundary["excluded_inference"], "fixture must explicitly reject solving the problem")
    require("MATHCERT has no theorem" in boundary.get("handoff_boundary", ""), "MATHCERT boundary must be explicit")


def check_handoff(handoff: dict[str, Any], source_hash: str, card_hash: str) -> None:
    require(handoff.get("fixture_id") == "RM-DIO-004", "handoff fixture_id mismatch")
    require(handoff.get("artifact_kind") == "mathsolve_handoff", "wrong handoff artifact kind")
    require(handoff.get("source_row_sha256") == source_hash, "handoff source hash mismatch")
    require(handoff.get("problem_card_sha256") == card_hash, "handoff problem-card hash mismatch")
    require(handoff.get("from_pillar") == "MATHFORGE" and handoff.get("to_pillar") == "MATHSOLVE", "wrong pillar handoff")
    require(handoff.get("handoff_status") == "READY_FOR_MATHSOLVE_TRIAGE", "handoff status must remain triage-ready")
    seed = handoff.get("work_package_seed")
    require(isinstance(seed, dict), "work_package_seed required")
    for field in ("title", "motivating_object", "obstruction", "theorem_spine_seed", "proof_debt_register", "first_executable_step"):
        require(field in seed, f"work package seed missing {field}")
    require(isinstance(seed["proof_debt_register"], list) and len(seed["proof_debt_register"]) >= 3, "proof debt register too weak")
    first = seed["first_executable_step"]
    require(isinstance(first, dict), "first executable step must be an object")
    require(first.get("kind") == "finite_exact_sanity_screen", "wrong first executable step kind")
    require(first.get("not_a_proof_of") == "complete integer solution set", "finite screen boundary missing")
    boundary = handoff.get("semantic_boundary")
    require(isinstance(boundary, dict), "handoff semantic boundary required")
    require("mark the ResearchMath problem solved" in boundary.get("mathsolve_not_allowed_to_do", ""), "handoff must forbid solving/status overclaim")


def check_claim_ledger(ledger: dict[str, Any], source_hash: str, card_hash: str, handoff_hash: str) -> None:
    require(ledger.get("fixture_id") == "RM-DIO-004", "ledger fixture_id mismatch")
    claims = ledger.get("claims")
    require(isinstance(claims, list) and len(claims) == 3, "claim ledger must contain exactly three claims")
    by_id = {claim.get("claim_id"): claim for claim in claims if isinstance(claim, dict)}
    require(set(by_id) == {"RM-DIO-004-C001", "RM-DIO-004-C002", "RM-DIO-004-C003"}, "claim IDs changed")
    for claim in claims:
        require(claim.get("status") not in FORBIDDEN_STATUSES, f"{claim.get('claim_id')}: forbidden status")
    require(by_id["RM-DIO-004-C001"].get("artifact_hashes", {}).get("source_row.json") == source_hash, "source-row hash mismatch")
    require(by_id["RM-DIO-004-C002"].get("artifact_hashes", {}).get("problem_card.json") == card_hash, "problem-card hash mismatch")
    require(by_id["RM-DIO-004-C003"].get("artifact_hashes", {}).get("mathsolve_handoff.json") == handoff_hash, "handoff hash mismatch")
    require(by_id["RM-DIO-004-C003"].get("status") == "PROVISIONAL", "handoff claim must remain provisional")
    forbidden = ledger.get("forbidden_promotions")
    require(isinstance(forbidden, list) and "SOLVED" in forbidden and "CERTIFIED" in forbidden, "forbidden promotions required")


def check_fixture(root: Path = ROOT) -> None:
    source_path = root / "source_row.json"
    card_path = root / "problem_card.json"
    handoff_path = root / "mathsolve_handoff.json"
    ledger_path = root / "claim_ledger.json"

    source = load_json(source_path)
    card = load_json(card_path)
    handoff = load_json(handoff_path)
    ledger = load_json(ledger_path)

    source_hash = sha256(source_path)
    card_hash = sha256(card_path)
    handoff_hash = sha256(handoff_path)

    check_source_row(source)
    check_problem_card(card, source_hash)
    check_handoff(handoff, source_hash, card_hash)
    check_claim_ledger(ledger, source_hash, card_hash, handoff_hash)


def main(argv: list[str]) -> int:
    root = Path(argv[1]) if len(argv) == 2 else ROOT
    try:
        check_fixture(root)
    except ResearchMathFixtureError as exc:
        print(f"researchmath fixture rejected: {exc}", file=sys.stderr)
        return 1
    print(f"researchmath fixture checked: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
