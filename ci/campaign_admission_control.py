"""Validate post-merge candidate execution without altering active admission."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ADMISSION_PATH = ROOT / "governance" / "campaign_admission_registry.json"
ADMISSION_SCHEMA_PATH = ROOT / "schemas" / "campaign_admission_registry.schema.json"
RUNTIME_PATH = ROOT / "governance" / "umbrella_runtime_contract_v4.json"
RUNTIME_SCHEMA_PATH = ROOT / "schemas" / "umbrella_runtime_contract_v4.schema.json"
ACTIVE_PATH = ROOT / "governance" / "governed_campaign_registry.json"
ROUTING_PATH = ROOT / "governance" / "mathsolve_routing_audit.json"

EXPECTED_ACTIVE_IDS = {
    "UC-001", "NS-CI-001", "HC-001", "BSD-001", "PC-001",
    "YM-001", "PNP-001", "RH-001", "OZ-001",
}
EXPECTED_ROUTING_IDS = EXPECTED_ACTIVE_IDS - {"PC-001"}
EXPECTED_CANDIDATE_IDS = {"VGSE-001"}
EXPECTED_CANDIDATE_DIGEST = "a6bffaa197aa3921e3eb9d4f8a02b5dc2bbded24"
EXPECTED_ACTIVE_DIGEST = "b1f1e4682d0f3ff0108d020e466fa2ecb0809b57"
EXPECTED_CERT_DIGEST = "5b3e8d48b9f6c5b03ed3dc439bf9e43876e017b1"
EXPECTED_SOURCE_DIGEST = "e513789426ae6247438920bfc80cfba6bd9c32dc6799a4f7873d806a865f95de"
EXPECTED_SOLVE_HEAD = "0d66a75412543e534b81c21a51a6ad88c035b55b"
EXPECTED_SOLVE_MERGE = "709c7d3f388b8df75c87a247f80424e560c31e72"
EXPECTED_WORKFLOW_RUNS = {
    "solve_checks": 30641057206,
    "gcl_conformance": 30641058060,
    "candidate_replay": 30641057393,
}
EXPECTED_GATES = {
    "forge_provider_manifest_admitted",
    "source_revision_concordance_complete",
    "solve_candidate_package_reviewed",
    "cert_route_registered",
    "programme_active_registry_updated",
    "programme_routing_registry_updated",
    "runtime_contract_updated_for_active_admission",
    "intellect_repin_complete_if_required",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode() + payload).hexdigest()


def schema_errors(instance: Any, schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"{label}: {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def validation_errors(
    admission: dict[str, Any] | None = None,
    runtime: dict[str, Any] | None = None,
    active: dict[str, Any] | None = None,
    routing: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    if admission is None:
        admission = load_json(ADMISSION_PATH)
        errors.extend(schema_errors(admission, ADMISSION_SCHEMA_PATH, "campaign admission registry"))
    if runtime is None:
        runtime = load_json(RUNTIME_PATH)
        errors.extend(schema_errors(runtime, RUNTIME_SCHEMA_PATH, "runtime contract v4"))
    if active is None:
        active = load_json(ACTIVE_PATH)
    if routing is None:
        routing = load_json(ROUTING_PATH)

    candidates = {
        str(item.get("campaign_id")): item
        for item in admission.get("candidates", [])
        if isinstance(item, dict)
    }
    active_ids = {
        str(item.get("campaign_id"))
        for item in active.get("campaigns", [])
        if isinstance(item, dict)
    }
    routing_ids = {
        str(item.get("campaign_id"))
        for item in routing.get("campaigns", [])
        if isinstance(item, dict)
    }

    if active_ids != EXPECTED_ACTIVE_IDS:
        errors.append("candidate admission: active campaign portfolio drift")
    if routing_ids != EXPECTED_ROUTING_IDS:
        errors.append("candidate admission: active routing portfolio drift")
    if set(candidates) != EXPECTED_CANDIDATE_IDS:
        errors.append("candidate admission: candidate portfolio drift")
    if set(candidates) & active_ids:
        errors.append("candidate admission: candidate leaked into active campaign registry")
    if set(candidates) & routing_ids:
        errors.append("candidate admission: candidate leaked into active routing registry")

    authority = admission.get("authority", {})
    if authority.get("state_authority") != "protected_branch_repository_records":
        errors.append("candidate admission: protected repository authority required")
    if authority.get("candidate_issue_mutation_can_admit_campaign") is not False:
        errors.append("candidate admission: issue mutation may not admit a campaign")
    if authority.get("candidate_work_can_modify_active_portfolio") is not False:
        errors.append("candidate admission: candidate work may not modify active portfolio")

    if admission.get("lifecycle_states") != ["candidate", "admitted_active", "rejected", "withdrawn"]:
        errors.append("candidate admission: lifecycle state vocabulary drift")

    vgse = candidates.get("VGSE-001", {})
    if vgse.get("lifecycle_state") != "candidate" or vgse.get("active_portfolio_member") is not False:
        errors.append("VGSE-001: must remain a non-active candidate")
    if vgse.get("programme_tracker_issue") != 170:
        errors.append("VGSE-001: Programme tracker identity drift")
    if vgse.get("governance_issue") != 175 or vgse.get("governance_history") != [172]:
        errors.append("VGSE-001: Programme governance history drift")

    source = vgse.get("source_provenance", {})
    if source.get("state") != "unverified_candidate":
        errors.append("VGSE-001: source provenance inflated beyond unverified candidate")
    if source.get("forge_issue") != 32 or source.get("provider_manifest") is not None:
        errors.append("VGSE-001: Forge provider state drift")
    if source.get("candidate_source", {}).get("candidate_sha256") != EXPECTED_SOURCE_DIGEST:
        errors.append("VGSE-001: candidate source digest drift")

    solve = vgse.get("solve_candidate", {})
    if solve.get("issue") != 84 or solve.get("pull_request") != 85:
        errors.append("VGSE-001: Solve mirror identity drift")
    if solve.get("base_commit") != "916f3434abcce29098ba7508a3b457a461461193":
        errors.append("VGSE-001: Solve protected-base identity drift")
    if solve.get("reviewed_head") != EXPECTED_SOLVE_HEAD:
        errors.append("VGSE-001: reviewed candidate head drift")
    if solve.get("merge_commit") != EXPECTED_SOLVE_MERGE:
        errors.append("VGSE-001: merged candidate commit drift")
    if solve.get("merged_at") != "2026-07-31T15:04:53Z":
        errors.append("VGSE-001: candidate merge timestamp drift")
    if solve.get("workflow_runs") != EXPECTED_WORKFLOW_RUNS:
        errors.append("VGSE-001: candidate workflow evidence drift")
    if solve.get("state") != "merged_candidate_work_package":
        errors.append("VGSE-001: candidate work package must be recorded as merged")
    if solve.get("may_merge_candidate_work_package") is not False:
        errors.append("VGSE-001: completed candidate merge may not remain authorized as future work")
    for field in (
        "may_create_campaign_manifest", "may_create_cert_handoff",
        "may_create_adjudication", "may_create_promotion_record",
    ):
        if solve.get(field) is not False:
            errors.append(f"VGSE-001: prohibited candidate authority in {field}")
    if solve.get("required_admission_record_path") != "work_packages/VGSE_WP00/candidate_admission.json":
        errors.append("VGSE-001: candidate admission record path drift")

    cert = vgse.get("certification_candidate", {})
    if cert != {
        "issue": 41,
        "state": "pre_route_candidate",
        "route_registry_entry": None,
        "may_adjudicate": False,
    }:
        errors.append("VGSE-001: Cert pre-route boundary drift")

    gates = vgse.get("admission_gates", {})
    if set(gates) != EXPECTED_GATES:
        errors.append("VGSE-001: admission gate set drift")
    if gates.get("solve_candidate_package_reviewed") is not True:
        errors.append("VGSE-001: reviewed candidate package gate must remain true")
    for field in EXPECTED_GATES - {"solve_candidate_package_reviewed"}:
        if gates.get(field) is not False:
            errors.append(f"VGSE-001: admission gate inflated before evidence: {field}")

    if git_blob_sha1(ADMISSION_PATH) != EXPECTED_CANDIDATE_DIGEST:
        errors.append("candidate admission: on-disk registry blob drift")
    active_ref = admission.get("active_campaign_registry", {})
    if active_ref.get("digest") != EXPECTED_ACTIVE_DIGEST or git_blob_sha1(ACTIVE_PATH) != EXPECTED_ACTIVE_DIGEST:
        errors.append("candidate admission: active registry identity drift")

    candidate_ref = runtime.get("candidate_admission_contract", {})
    if candidate_ref.get("path") != "governance/campaign_admission_registry.json":
        errors.append("runtime v4: candidate admission path drift")
    if candidate_ref.get("digest") != EXPECTED_CANDIDATE_DIGEST:
        errors.append("runtime v4: candidate admission digest drift")
    if candidate_ref.get("candidate_ids") != ["VGSE-001"] or candidate_ref.get("candidate_count") != 1:
        errors.append("runtime v4: candidate portfolio identity drift")
    if runtime.get("candidate_portfolio") != {
        "pre_admission": ["VGSE-001"],
        "reviewed_candidate_work_packages": ["VGSE-001"],
        "active_portfolio_effect": "none",
    }:
        errors.append("runtime v4: reviewed candidate execution state drift")
    runtime_authority = runtime.get("authority_model", {})
    if runtime_authority.get("candidate_registry_is_separate_from_active_registry") is not True:
        errors.append("runtime v4: candidate and active registries must remain separate")
    if runtime_authority.get("candidate_work_can_self_admit") is not False:
        errors.append("runtime v4: candidate work may not self-admit")
    if runtime.get("certification_contract", {}).get("digest") != EXPECTED_CERT_DIGEST:
        errors.append("runtime v4: Cert contract identity drift")
    boundaries = runtime.get("claim_boundaries", {})
    if boundaries.get("candidate_campaign_admitted") is not False:
        errors.append("runtime v4: candidate campaign admission inflation")
    if boundaries.get("mathematical_target_proved") is not False:
        errors.append("runtime v4: mathematical proof inflation")
    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("validated reviewed and merged candidate work, unchanged active portfolio, unverified source provenance, and pre-route Cert state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
