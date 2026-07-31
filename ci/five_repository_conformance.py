"""Policy checks for the final five-repository conformance matrix."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "governance" / "five_repository_conformance_matrix.json"
SCHEMA_PATH = ROOT / "schemas" / "five_repository_conformance_matrix.schema.json"
ROUTING_PATH = ROOT / "governance" / "mathsolve_routing_audit.json"
AUDIT_PATH = ROOT / "governance" / "umbrella_current_state_conformance.json"

EXPECTED_HEADS = {
    "math_programme": "6c0b3e55eeca9be1ef5a538b0fb659f3bf1045a2",
    "mathforge": "0faee396ffa56c568ee0ae6a348bdb43ca80ac4d",
    "mathsolve": "916f3434abcce29098ba7508a3b457a461461193",
    "mathcert": "0258e4f0bca0d90fac05b62aeef108f16dccffdd",
    "intellect": "7ce82ee5ad5614459ee4bffa57d22dc39adacbc1",
}
EXPECTED_BLOBS = {
    "routing": "4a27ec8aaaa60f919ba51028807b83dc522bfcff",
    "successor_audit": "a2a1c3d590f535972c87f57d9b86155a246a61ba",
    "cert_registry": "5b3e8d48b9f6c5b03ed3dc439bf9e43876e017b1",
    "intellect_provider": "7f16e1739f7c1818c0a8d3d78f0afc92144ab14d",
    "intellect_fixture": "690a71ad1fe9f3467ef0999c1fbc5da77d7fcff2",
}
EXPECTED_STATES = {
    "qualified": {"NS-CI-001", "RH-001"},
    "ready": {"UC-001", "HC-001"},
    "pending": {"BSD-001", "PNP-001", "YM-001", "OZ-001"},
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validation_errors(matrix: dict[str, Any] | None = None) -> list[str]:
    errors: list[str] = []
    if matrix is None:
        matrix = load_json(MATRIX_PATH)
        schema = load_json(SCHEMA_PATH)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors.extend(
            f"governance/five_repository_conformance_matrix.json: {error.json_path}: {error.message}"
            for error in sorted(validator.iter_errors(matrix), key=lambda item: list(item.path))
        )

    if matrix.get("identity_mismatch_count") != 0:
        errors.append("five-repository matrix: identity mismatch count must be zero")
    if matrix.get("merge_clean_at_verification") is not True:
        errors.append("five-repository matrix: repositories were not merge-clean")

    repositories = matrix.get("repositories", {})
    for name, expected in EXPECTED_HEADS.items():
        actual = repositories.get(name, {}).get("state_commit")
        if actual != expected:
            errors.append(f"five-repository matrix: {name} head drift; expected {expected}")

    programme = repositories.get("math_programme", {})
    if programme.get("routing", {}).get("digest") != EXPECTED_BLOBS["routing"]:
        errors.append("five-repository matrix: Programme routing blob drift")
    if programme.get("successor_audit", {}).get("digest") != EXPECTED_BLOBS["successor_audit"]:
        errors.append("five-repository matrix: Programme successor-audit blob drift")
    cert = repositories.get("mathcert", {})
    if cert.get("route_registry", {}).get("digest") != EXPECTED_BLOBS["cert_registry"]:
        errors.append("five-repository matrix: Cert registry blob drift")
    intellect = repositories.get("intellect", {})
    if intellect.get("current_provider", {}).get("digest") != EXPECTED_BLOBS["intellect_provider"]:
        errors.append("five-repository matrix: INTELLECT current-provider blob drift")
    if intellect.get("qualification_fixture", {}).get("digest") != EXPECTED_BLOBS["intellect_fixture"]:
        errors.append("five-repository matrix: INTELLECT qualification-fixture blob drift")

    routing = load_json(ROUTING_PATH)
    actual_states = {"qualified": set(), "ready": set(), "pending": set()}
    for entry in routing.get("campaigns", []):
        state = entry.get("cert", {}).get("route_state")
        if state in actual_states:
            actual_states[state].add(entry.get("campaign_id"))
        if state == "qualified":
            if entry.get("cert", {}).get("qualification_scope") != "qualified_interface_only":
                errors.append(f"five-repository matrix: {entry.get('campaign_id')} scope inflation")
            if entry.get("promotion", {}).get("state") != "blocked":
                errors.append(f"five-repository matrix: {entry.get('campaign_id')} promotion inflation")
    if actual_states != EXPECTED_STATES:
        errors.append("five-repository matrix: portfolio state mismatch")

    portfolio = matrix.get("portfolio", {})
    if set(portfolio.get("qualified_interface_only", [])) != EXPECTED_STATES["qualified"]:
        errors.append("five-repository matrix: qualified portfolio mismatch")
    if set(portfolio.get("ready_intake", [])) != EXPECTED_STATES["ready"]:
        errors.append("five-repository matrix: ready portfolio mismatch")
    if set(portfolio.get("pending", [])) != EXPECTED_STATES["pending"]:
        errors.append("five-repository matrix: pending portfolio mismatch")

    audit = load_json(AUDIT_PATH)
    if audit.get("claim_boundaries", {}).get("operational_release_complete_preserved") is not True:
        errors.append("five-repository matrix: operational release closure was not preserved")
    boundaries = matrix.get("claim_boundaries", {})
    for field in ("mathematical_target_proved", "novelty_claim_authorized", "priority_claim_authorized", "release_trust_issues_reopened"):
        if boundaries.get(field) is not False:
            errors.append(f"five-repository matrix: prohibited boundary inflation in {field}")
    if boundaries.get("operational_release_complete_preserved") is not True:
        errors.append("five-repository matrix: operational release closure must remain true")

    if set(matrix.get("preserved_blockers", {})) != set(EXPECTED_STATES["qualified"] | EXPECTED_STATES["ready"] | EXPECTED_STATES["pending"]):
        errors.append("five-repository matrix: blocker coverage does not equal active routing portfolio")
    if matrix.get("tracker_reconciliation", {}).get("mathsolve_retrospective_closed_completed") != [66, 67, 68, 69]:
        errors.append("five-repository matrix: retrospective Solve closure set drift")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validated five exact repository heads, zero identity mismatches, tracker reconciliation, and preserved mathematical blockers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
