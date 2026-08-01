#!/usr/bin/env python3
"""Validate the OPENAI-TEN-PROOFS-WP00 candidate intake evidence boundary."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "governance" / "openai_ten_proofs_wp00_candidate_intake.json"
SCHEMA_PATH = ROOT / "schemas" / "openai_ten_proofs_candidate_intake.schema.json"
DOCUMENT_PATH = ROOT / "work_packages" / "OPENAI_TEN_PROOFS_WP00_GOVERNED_INTAKE.md"

EXPECTED_EXTERNAL_SUBJECT = {
    "repository": "openai/ten-proofs",
    "commit": "6fefffdbab0dfa726fcfde6cefae23aa7a1888f3",
    "tree": "79e6a50b1e391bdddb18b42be3e886c1d9784ed3",
    "archive_sha256": "630e10ec7f8b08ce3416fba967e6d1e4c7599677e38fd4af24fc0c68a9a5bac2",
    "root_commit": True,
}
EXPECTED_FORGE_CORE = {
    "repository": "grandchallenge/MATHFORGE",
    "pull_request": 36,
    "reviewed_head_commit": "f4283c59571a43be23d07700b4cfddafc2bcda8d",
    "merge_commit": "89f3853f697450261cb76a638b5282c3bfa96770",
    "authority_state": "protected_merge",
}
EXPECTED_FORGE_ARTIFACTS = {
    "provider_manifest": {
        "path": "provider_manifests/OPENAI-TEN-PROOFS-001.json",
        "git_blob_sha1": "c9754fd02026ee923040fac288e9285d72cb2b67",
    },
    "source_lock": {
        "path": "sources/OPENAI-TEN-PROOFS-001/source_lock.json",
        "git_blob_sha1": "1b4981178553ad300a5abead6d3c9f6bac78d0da",
    },
    "theorem_intake_matrix": {
        "path": "sources/OPENAI-TEN-PROOFS-001/theorem_intake_matrix.json",
        "git_blob_sha1": "63923c38471eb601161cbd1d3c8ba28244b86166",
    },
    "provider_coverage": {
        "path": "governance/provider_coverage.json",
        "git_blob_sha1": "5f00bd9bbd8e626fd23f8bde7f31c881cee9df38",
    },
}
EXPECTED_RESULT_FAMILIES = [
    "OTP-A-SPHERE-PACKING",
    "OTP-B1-BINARY-CODES",
    "OTP-B2-SPHERICAL-CODES",
    "OTP-C-PERMANENT",
    "OTP-D-NON-SOFIC",
    "OTP-E-CONNES-RIGIDITY",
    "OTP-F-EHRHART",
    "OTP-G-QUANTUM-PARALLEL-REPETITION",
    "OTP-H-GAPCVP",
    "OTP-I-RAMSEY",
    "OTP-J1-COMPACTNESS",
    "OTP-J2-TWO-DEGENERATE",
]
EXPECTED_GATE_STATES = {
    "source_identity": ("provider_verified", True),
    "kernel_correctness": ("not_verified", False),
    "statement_fidelity": ("not_verified", False),
    "independent_adjudication": ("not_performed", False),
}
EXPECTED_ROUTE_STATE = {
    "mathforge": "provider_manifest_merged",
    "mathsolve": "blocked_pre_route_candidate",
    "mathcert": "pre_route_candidate",
    "may_emit_solve_handoff": False,
    "may_adjudicate": False,
    "may_promote_result": False,
    "aggregate_admission_prohibited": True,
    "admission_granularity": "result_family",
}
EXPECTED_TRACKERS = {
    "mathforge": "https://github.com/grandchallenge/MATHFORGE/issues/35",
    "mathsolve": "https://github.com/grandchallenge/MATHSOLVE/issues/90",
    "mathcert": "https://github.com/grandchallenge/MATHCERT/issues/43",
}
DOCUMENT_REQUIRED_TOKENS = (
    EXPECTED_EXTERNAL_SUBJECT["commit"],
    EXPECTED_EXTERNAL_SUBJECT["tree"],
    EXPECTED_EXTERNAL_SUBJECT["archive_sha256"],
    EXPECTED_FORGE_CORE["reviewed_head_commit"],
    EXPECTED_FORGE_CORE["merge_commit"],
    "all twelve declared Comparator checks",
    "may_adjudicate: false",
    "cert_output: null",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any) -> list[str]:
    validator = Draft202012Validator(load_json(SCHEMA_PATH), format_checker=FormatChecker())
    return [
        f"OPENAI-TEN-PROOFS-WP00: {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def validation_errors(
    record: dict[str, Any] | None = None,
    document: str | None = None,
) -> list[str]:
    errors: list[str] = []
    if record is None:
        record = load_json(RECORD_PATH)
    if document is None:
        document = DOCUMENT_PATH.read_text(encoding="utf-8")

    errors.extend(schema_errors(record))
    if record.get("external_subject") != EXPECTED_EXTERNAL_SUBJECT:
        errors.append("OPENAI-TEN-PROOFS-WP00: external subject identity drift")

    forge = record.get("forge_provider_authority", {})
    for field, expected in EXPECTED_FORGE_CORE.items():
        if forge.get(field) != expected:
            errors.append(f"OPENAI-TEN-PROOFS-WP00: Forge authority drift in {field}")
    artifacts = forge.get("artifacts")
    if artifacts != EXPECTED_FORGE_ARTIFACTS:
        if not isinstance(artifacts, dict):
            errors.append("OPENAI-TEN-PROOFS-WP00: Forge artifact map missing")
        else:
            for artifact_id, expected in EXPECTED_FORGE_ARTIFACTS.items():
                if artifacts.get(artifact_id) != expected:
                    errors.append(
                        f"OPENAI-TEN-PROOFS-WP00: Forge artifact identity drift in {artifact_id}"
                    )

    if record.get("result_families") != EXPECTED_RESULT_FAMILIES:
        errors.append("OPENAI-TEN-PROOFS-WP00: result-family identity or order drift")

    gates = record.get("gate_matrix", {})
    if set(gates) != set(EXPECTED_GATE_STATES):
        errors.append("OPENAI-TEN-PROOFS-WP00: gate set drift")
    for gate_id, (state, satisfied) in EXPECTED_GATE_STATES.items():
        gate = gates.get(gate_id, {})
        if (gate.get("state"), gate.get("satisfied_for_admission")) != (state, satisfied):
            errors.append(f"OPENAI-TEN-PROOFS-WP00: gate disposition drift in {gate_id}")

    if record.get("route_state") != EXPECTED_ROUTE_STATE:
        errors.append("OPENAI-TEN-PROOFS-WP00: route prohibition or granularity drift")
    if record.get("linked_trackers") != EXPECTED_TRACKERS:
        errors.append("OPENAI-TEN-PROOFS-WP00: linked tracker identity drift")
    if record.get("active_campaign_member") is not False:
        errors.append("OPENAI-TEN-PROOFS-WP00: candidate entered active portfolio")
    if record.get("lifecycle_state") != "candidate_external_formalization":
        errors.append("OPENAI-TEN-PROOFS-WP00: candidate lifecycle drift")

    claim_boundary = record.get("claim_boundary", "")
    required_claim_phrases = (
        "does not add it to the active campaign portfolio",
        "certify any theorem",
        "assert equivalence to any paper",
    )
    if not all(phrase in claim_boundary for phrase in required_claim_phrases):
        errors.append("OPENAI-TEN-PROOFS-WP00: claim boundary weakened")

    for token in DOCUMENT_REQUIRED_TOKENS:
        if token not in document:
            errors.append(f"OPENAI-TEN-PROOFS-WP00 document: missing preserved token {token}")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        print("\n".join(errors))
        return 1
    print(
        "validated OPENAI-TEN-PROOFS-WP00 subject, Forge merge and blobs, "
        "result families, closed gates, route prohibitions, and prose pins"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
