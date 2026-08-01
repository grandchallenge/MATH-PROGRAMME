"""Validate reviewed and intake-only candidates without altering active admission."""
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
EXPECTED_CANDIDATE_IDS = {"NSOF-001", "VGSE-001"}
EXPECTED_CANDIDATE_DIGEST = "934eccd89fdbc3350fb4e9d89a0a9759bdb7fc61"
EXPECTED_ACTIVE_DIGEST = "b1f1e4682d0f3ff0108d020e466fa2ecb0809b57"
EXPECTED_CERT_DIGEST = "5b3e8d48b9f6c5b03ed3dc439bf9e43876e017b1"
EXPECTED_SCREENSHOT_DIGEST = "531d8b044623569e43949f094985c083e07cf3c0c6a7b6db6e0b5c3339b57420"
EXPECTED_VGSE_SOURCE_DIGEST = "e513789426ae6247438920bfc80cfba6bd9c32dc6799a4f7873d806a865f95de"
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
    validator = Draft202012Validator(load_json(schema_path), format_checker=FormatChecker())
    return [
        f"{label}: {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def _candidate_map(admission: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("campaign_id")): item
        for item in admission.get("candidates", [])
        if isinstance(item, dict)
    }


def _gate_errors(candidate_id: str, candidate: dict[str, Any], reviewed: bool) -> list[str]:
    errors: list[str] = []
    gates = candidate.get("admission_gates", {})
    if set(gates) != EXPECTED_GATES:
        errors.append(f"{candidate_id}: admission gate set drift")
        return errors
    expected_true = {"solve_candidate_package_reviewed"} if reviewed else set()
    for field in EXPECTED_GATES:
        if gates.get(field) is not (field in expected_true):
            errors.append(f"{candidate_id}: admission gate inflated or rolled back: {field}")
    return errors


def validation_errors(
    admission: dict[str, Any] | None = None,
    runtime: dict[str, Any] | None = None,
    active: dict[str, Any] | None = None,
    routing: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    on_disk_admission = admission is None
    on_disk_runtime = runtime is None
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

    candidates = _candidate_map(admission)
    active_ids = {
        str(item.get("campaign_id")) for item in active.get("campaigns", [])
        if isinstance(item, dict)
    }
    routing_ids = {
        str(item.get("campaign_id")) for item in routing.get("campaigns", [])
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
    if vgse.get("candidate_phase") != "reviewed_candidate_work_package":
        errors.append("VGSE-001: reviewed candidate phase drift")
    if vgse.get("lifecycle_state") != "candidate" or vgse.get("active_portfolio_member") is not False:
        errors.append("VGSE-001: must remain a non-active candidate")
    if (vgse.get("programme_tracker_issue"), vgse.get("governance_issue"), vgse.get("governance_history")) != (170, 175, [172]):
        errors.append("VGSE-001: Programme governance identity drift")
    vgse_source = vgse.get("source_provenance", {})
    if vgse_source.get("state") != "unverified_candidate" or vgse_source.get("provider_manifest") is not None:
        errors.append("VGSE-001: source provenance inflated")
    if vgse_source.get("forge_issue") != 32 or vgse_source.get("intake_evidence") is not None:
        errors.append("VGSE-001: source evidence shape drift")
    if (vgse_source.get("candidate_source") or {}).get("candidate_sha256") != EXPECTED_VGSE_SOURCE_DIGEST:
        errors.append("VGSE-001: candidate source digest drift")
    vgse_solve = vgse.get("solve_candidate", {})
    if (vgse_solve.get("issue"), vgse_solve.get("pull_request"), vgse_solve.get("state")) != (84, 85, "merged_candidate_work_package"):
        errors.append("VGSE-001: merged Solve candidate identity drift")
    for field in ("may_merge_candidate_work_package", "may_create_campaign_manifest", "may_create_cert_handoff", "may_create_adjudication", "may_create_promotion_record"):
        if vgse_solve.get(field) is not False:
            errors.append(f"VGSE-001: prohibited candidate authority in {field}")
    if vgse.get("certification_candidate") != {"issue": 41, "state": "pre_route_candidate", "route_registry_entry": None, "may_adjudicate": False}:
        errors.append("VGSE-001: Cert pre-route boundary drift")
    errors.extend(_gate_errors("VGSE-001", vgse, reviewed=True))

    nsof = candidates.get("NSOF-001", {})
    if nsof.get("candidate_phase") != "intake_only":
        errors.append("NSOF-001: must remain intake-only")
    if nsof.get("lifecycle_state") != "candidate" or nsof.get("active_portfolio_member") is not False:
        errors.append("NSOF-001: must remain a non-active candidate")
    if (nsof.get("programme_tracker_issue"), nsof.get("governance_issue"), nsof.get("governance_history")) != (195, 196, []):
        errors.append("NSOF-001: Programme governance identity drift")
    source = nsof.get("source_provenance", {})
    if source.get("state") != "unverified_candidate" or source.get("provider_manifest") is not None:
        errors.append("NSOF-001: source provenance inflated beyond screenshot intake")
    if source.get("forge_issue") != 34 or source.get("candidate_source") is not None:
        errors.append("NSOF-001: manuscript source identity fabricated before acquisition")
    evidence = source.get("intake_evidence") or {}
    expected_evidence = {
        "artifact_type": "screenshot", "media_type": "image/png",
        "sha256": EXPECTED_SCREENSHOT_DIGEST, "byte_length": 408154,
        "pixel_width": 820, "pixel_height": 513,
        "visible_title": "NONSOFIC GROUPS EXIST", "visible_attribution": "OPENAI",
        "received_date": "2026-08-01", "manuscript_bytes_acquired": False,
        "manuscript_digest": None, "official_release_found": False,
        "arxiv_record_found": False,
    }
    if evidence != expected_evidence:
        errors.append("NSOF-001: screenshot evidence identity or source boundary drift")
    solve = nsof.get("solve_candidate", {})
    if (solve.get("issue"), solve.get("state")) != (89, "gated_preparation"):
        errors.append("NSOF-001: gated Solve preparation identity drift")
    for field in ("pull_request", "base_commit", "reviewed_head", "merge_commit", "merged_at", "workflow_runs", "required_admission_record_path"):
        if solve.get(field) is not None:
            errors.append(f"NSOF-001: fabricated Solve execution evidence in {field}")
    for field in ("may_merge_candidate_work_package", "may_create_campaign_manifest", "may_create_cert_handoff", "may_create_adjudication", "may_create_promotion_record"):
        if solve.get(field) is not False:
            errors.append(f"NSOF-001: prohibited intake authority in {field}")
    if nsof.get("certification_candidate") != {"issue": 42, "state": "pre_route_candidate", "route_registry_entry": None, "may_adjudicate": False}:
        errors.append("NSOF-001: Cert pre-route boundary drift")
    errors.extend(_gate_errors("NSOF-001", nsof, reviewed=False))

    if on_disk_admission and git_blob_sha1(ADMISSION_PATH) != EXPECTED_CANDIDATE_DIGEST:
        errors.append("candidate admission: on-disk registry blob drift")
    active_ref = admission.get("active_campaign_registry", {})
    if active_ref.get("digest") != EXPECTED_ACTIVE_DIGEST or git_blob_sha1(ACTIVE_PATH) != EXPECTED_ACTIVE_DIGEST:
        errors.append("candidate admission: active registry identity drift")

    candidate_ref = runtime.get("candidate_admission_contract", {})
    if candidate_ref.get("path") != "governance/campaign_admission_registry.json" or candidate_ref.get("digest") != EXPECTED_CANDIDATE_DIGEST:
        errors.append("runtime v4: candidate admission identity drift")
    if candidate_ref.get("candidate_ids") != ["NSOF-001", "VGSE-001"] or candidate_ref.get("candidate_count") != 2:
        errors.append("runtime v4: candidate portfolio identity drift")
    expected_portfolio = {
        "pre_admission": ["NSOF-001", "VGSE-001"],
        "intake_only": ["NSOF-001"],
        "reviewed_candidate_work_packages": ["VGSE-001"],
        "active_portfolio_effect": "none",
    }
    if runtime.get("candidate_portfolio") != expected_portfolio:
        errors.append("runtime v4: candidate phase projection drift")
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
    print("validated reviewed VGSE candidate, screenshot-only NSOF intake, unchanged active portfolio, and pre-route Cert boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
