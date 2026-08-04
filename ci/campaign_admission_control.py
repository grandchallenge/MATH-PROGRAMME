"""Validate VGSE bounded active routing pending the required INTELLECT repin."""
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
DECISION_PATH = ROOT / "governance" / "vgse_bounded_admission_decision.json"
ACTIVE_PATH = ROOT / "governance" / "governed_campaign_registry.json"
ACTIVE_SCHEMA_PATH = ROOT / "schemas" / "governed_campaign_registry.schema.json"
ROUTING_PATH = ROOT / "governance" / "mathsolve_routing_audit_vgse.json"
ROUTING_SCHEMA_PATH = ROOT / "schemas" / "mathsolve_routing_audit_vgse.schema.json"
RUNTIME_PATH = ROOT / "governance" / "umbrella_runtime_contract_v5.json"
RUNTIME_SCHEMA_PATH = ROOT / "schemas" / "umbrella_runtime_contract_v5.schema.json"
ACTIVATION_PATH = ROOT / "governance" / "vgse_final_activation.json"
ACTIVATION_SCHEMA_PATH = ROOT / "schemas" / "vgse_final_activation.schema.json"

EXPECTED_ACTIVE_IDS = {
    "UC-001", "NS-CI-001", "HC-001", "BSD-001", "PC-001",
    "YM-001", "PNP-001", "RH-001", "OZ-001", "VGSE-001",
}
EXPECTED_ROUTING_IDS = {
    "UC-001", "NS-CI-001", "HC-001", "BSD-001",
    "YM-001", "PNP-001", "RH-001", "OZ-001", "VGSE-001",
}
EXPECTED_BASE_ROUTING_DIGEST = "4a27ec8aaaa60f919ba51028807b83dc522bfcff"
EXPECTED_OLD_RUNTIME_DIGEST = "33cf79f38f1273a834bb43d4cc55bfc79ba2c5e0"
EXPECTED_DECISION_DIGEST = "a419d6832757ec2631e67d7f2b5f71d16e51f359"
EXPECTED_ACTIVE_DIGEST = "4cabbd820097029d01430f9f8a0c02653321e5af"
EXPECTED_ROUTING_DIGEST = "6fb8dce8f1b4f11f8994798840e72b09ad862575"
EXPECTED_ADMISSION_DIGEST = "c724d1174c2e1caa8a74297a21a46aa9d1910962"
EXPECTED_RUNTIME_DIGEST = "2f304cbf07f934e97cdd2fbac7a6ccece2ac4a5a"
EXPECTED_ACTIVATION_DIGEST = "f9311fa0fd0060cfe28072e7a6d204898449c74e"
EXPECTED_MANIFEST_DIGEST = "3bb6b18052f5754e9ae9aa4f813d9b43dcd4e3b4"
EXPECTED_HANDOFF_DIGEST = "42cfa84978fd63c75f074b388afd8b1fcbd56091"
EXPECTED_ROUTE_DIGEST = "de56bfb0544b27b6237a68ac87044d3f0ba2e445"
EXPECTED_SOLVE_MERGE = "1ebc9ace360e453fbc3707f6b23032b1c3c561eb"
EXPECTED_CERT_MERGE = "92e3e56fda50267a241e120eb337dbbc520e900f"
EXPECTED_PROVIDER_DIGEST = "9cb5ac2d92b458f7f63e8a9811448f245a151ddd"
EXPECTED_SCREENSHOT_DIGEST = "531d8b044623569e43949f094985c083e07cf3c0c6a7b6db6e0b5c3339b57420"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(
        f"blob {len(payload)}\0".encode("ascii") + payload,
        usedforsecurity=False,
    ).hexdigest()


def schema_errors(instance: Any, schema_path: Path, label: str) -> list[str]:
    validator = Draft202012Validator(
        load_json(schema_path), format_checker=FormatChecker()
    )
    return [
        f"{label}: {error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path))
    ]


def _records(admission: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(item.get("campaign_id")): item
        for item in admission.get("candidates", [])
        if isinstance(item, dict)
    }


def validation_errors(
    admission: dict[str, Any] | None = None,
    decision: dict[str, Any] | None = None,
    runtime: dict[str, Any] | None = None,
    active: dict[str, Any] | None = None,
    routing: dict[str, Any] | None = None,
    activation: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    on_disk = all(item is None for item in (admission, decision, runtime, active, routing, activation))

    admission = load_json(ADMISSION_PATH) if admission is None else admission
    decision = load_json(DECISION_PATH) if decision is None else decision
    runtime = load_json(RUNTIME_PATH) if runtime is None else runtime
    active = load_json(ACTIVE_PATH) if active is None else active
    routing = load_json(ROUTING_PATH) if routing is None else routing
    activation = load_json(ACTIVATION_PATH) if activation is None else activation

    errors.extend(schema_errors(admission, ADMISSION_SCHEMA_PATH, "campaign admission registry"))
    errors.extend(schema_errors(active, ACTIVE_SCHEMA_PATH, "governed campaign registry"))
    errors.extend(schema_errors(routing, ROUTING_SCHEMA_PATH, "VGSE routing successor"))
    errors.extend(schema_errors(runtime, RUNTIME_SCHEMA_PATH, "runtime contract v5"))
    errors.extend(schema_errors(activation, ACTIVATION_SCHEMA_PATH, "VGSE final activation"))

    active_items = {
        str(item.get("campaign_id")): item
        for item in active.get("campaigns", [])
        if isinstance(item, dict)
    }
    if set(active_items) != EXPECTED_ACTIVE_IDS:
        errors.append("VGSE activation: active campaign portfolio drift")
    vgse_active = active_items.get("VGSE-001", {})
    if (
        vgse_active.get("lifecycle") != "active_bounded_pending_cert_evidence"
        or vgse_active.get("routing_member") is not True
        or vgse_active.get("programme_tracker_issue") != 170
    ):
        errors.append("VGSE activation: governed active-registry entry drift")

    if routing.get("base_routing_contract", {}).get("digest") != EXPECTED_BASE_ROUTING_DIGEST:
        errors.append("VGSE activation: base routing identity drift")
    successor = routing.get("successor_campaign", {})
    if successor.get("campaign_id") != "VGSE-001":
        errors.append("VGSE activation: successor routing campaign drift")
    manifest = successor.get("manifest", {})
    if (
        manifest.get("digest") != EXPECTED_MANIFEST_DIGEST
        or manifest.get("merge_commit") != EXPECTED_SOLVE_MERGE
    ):
        errors.append("VGSE activation: Solve manifest identity drift")
    cert = successor.get("cert", {})
    route = cert.get("route_registration", {})
    handoff = cert.get("handoff", {})
    if (
        cert.get("route_state") != "registered_pending_evidence"
        or cert.get("may_adjudicate") is not False
        or cert.get("cert_output") is not None
    ):
        errors.append("VGSE activation: Cert pending-route boundary drift")
    if route.get("digest") != EXPECTED_ROUTE_DIGEST or route.get("merge_commit") != EXPECTED_CERT_MERGE:
        errors.append("VGSE activation: MATHCERT route identity drift")
    if handoff.get("git_blob_sha1") != EXPECTED_HANDOFF_DIGEST or handoff.get("state") != "pending":
        errors.append("VGSE activation: pending handoff identity drift")
    combined = set(routing.get("combined_portfolio", {}).get("campaign_ids", []))
    if combined != EXPECTED_ROUTING_IDS:
        errors.append("VGSE activation: combined routing portfolio drift")
    promotion = successor.get("promotion", {})
    if promotion.get("state") != "blocked" or not promotion.get("blockers"):
        errors.append("VGSE activation: promotion boundary drift")

    records = _records(admission)
    if set(records) != {"NSOF-001", "VGSE-001"}:
        errors.append("VGSE activation: tracked admission-record portfolio drift")
    nsof = records.get("NSOF-001", {})
    if (
        nsof.get("candidate_phase") != "intake_only"
        or nsof.get("lifecycle_state") != "candidate"
        or nsof.get("active_portfolio_member") is not False
    ):
        errors.append("NSOF-001: intake-only boundary drift")
    nsof_evidence = (nsof.get("source_provenance") or {}).get("intake_evidence") or {}
    if nsof_evidence.get("sha256") != EXPECTED_SCREENSHOT_DIGEST:
        errors.append("NSOF-001: screenshot evidence identity drift")
    if any((nsof.get("admission_gates") or {}).values()):
        errors.append("NSOF-001: admission gate inflated")

    vgse = records.get("VGSE-001", {})
    if (
        vgse.get("candidate_phase") != "activated_bounded_pending_cert_evidence"
        or vgse.get("lifecycle_state") != "admitted_active"
        or vgse.get("active_portfolio_member") is not True
    ):
        errors.append("VGSE-001: active lifecycle projection drift")
    source = vgse.get("source_provenance", {})
    if (source.get("provider_manifest") or {}).get("digest") != EXPECTED_PROVIDER_DIGEST:
        errors.append("VGSE-001: provider manifest identity drift")
    solve = vgse.get("solve_candidate", {})
    if (
        solve.get("state") != "active_manifest_and_pending_handoff_admitted"
        or solve.get("merge_commit") != EXPECTED_SOLVE_MERGE
        or (solve.get("active_manifest") or {}).get("digest") != EXPECTED_MANIFEST_DIGEST
        or (solve.get("cert_handoff") or {}).get("digest") != EXPECTED_HANDOFF_DIGEST
    ):
        errors.append("VGSE-001: active Solve evidence drift")
    cert_record = vgse.get("certification_candidate", {})
    if (
        cert_record.get("state") != "registered_pending_evidence"
        or cert_record.get("may_adjudicate") is not False
        or cert_record.get("cert_output") is not None
        or (cert_record.get("route_registry_entry") or {}).get("digest") != EXPECTED_ROUTE_DIGEST
    ):
        errors.append("VGSE-001: registered pending Cert record drift")
    gates = vgse.get("admission_gates", {})
    true_gates = {
        "forge_provider_manifest_admitted",
        "source_revision_concordance_complete",
        "solve_candidate_package_reviewed",
        "cert_route_registered",
        "programme_active_registry_updated",
        "programme_routing_registry_updated",
        "runtime_contract_updated_for_active_admission",
    }
    for name, value in gates.items():
        expected = name in true_gates
        if value is not expected:
            errors.append(f"VGSE-001: admission gate inflated or rolled back: {name}")
    if gates.get("intellect_repin_complete_if_required") is not False:
        errors.append("VGSE-001: INTELLECT repin may not close before protected consumer merge")

    active_ref = admission.get("active_campaign_registry", {})
    if (
        active_ref.get("digest") != EXPECTED_ACTIVE_DIGEST
        or active_ref.get("active_routing_member_count") != 9
    ):
        errors.append("VGSE activation: admission registry active reference drift")

    if runtime.get("supersedes", {}).get("git_blob_sha1") != EXPECTED_OLD_RUNTIME_DIGEST:
        errors.append("VGSE activation: runtime predecessor identity drift")
    refs = [
        (runtime.get("programme_routing_contract", {}), EXPECTED_ROUTING_DIGEST, "runtime routing"),
        (runtime.get("programme_campaign_contract", {}), EXPECTED_ACTIVE_DIGEST, "runtime campaign"),
        (runtime.get("candidate_admission_contract", {}), EXPECTED_ADMISSION_DIGEST, "runtime admission"),
        (runtime.get("certification_contract", {}), EXPECTED_ROUTE_DIGEST, "runtime Cert"),
    ]
    for ref, expected, label in refs:
        if ref.get("digest") != expected:
            errors.append(f"VGSE activation: {label} identity drift")
    if runtime.get("active_portfolio", {}).get("pending_cert_evidence") != ["VGSE-001"]:
        errors.append("VGSE activation: runtime pending-Cert projection drift")
    candidate_portfolio = runtime.get("candidate_portfolio", {})
    if (
        candidate_portfolio.get("pre_admission") != ["NSOF-001"]
        or candidate_portfolio.get("admitted_active") != ["VGSE-001"]
    ):
        errors.append("VGSE activation: runtime candidate lifecycle projection drift")
    consumer = runtime.get("consumer_sync", {})
    if (
        consumer.get("intellect_repin_required") is not True
        or consumer.get("intellect_repin_complete") is not False
    ):
        errors.append("VGSE activation: INTELLECT consumer gate drift")
    claims = runtime.get("claim_boundaries", {})
    prohibited_runtime_true = {
        "mathematical_target_proved",
        "novelty_claim_authorized",
        "priority_claim_authorized",
        "mathcert_adjudication_authorized",
        "certificate_output_authorized",
        "mechanical_or_manufacturing_claim_authorized",
        "product_or_commercial_claim_authorized",
        "release_trust_issues_reopened",
    }
    if any(claims.get(name) is not False for name in prohibited_runtime_true):
        errors.append("VGSE activation: runtime claim inflation")

    if decision.get("decision") != "ADMIT_BOUNDED_PENDING_CROSS_REPOSITORY_ACTIVATION":
        errors.append("VGSE activation: historical bounded decision drift")
    if activation.get("disposition") != "ACTIVATE_BOUNDED_PENDING_INTELLECT_REPIN":
        errors.append("VGSE activation: activation disposition drift")
    programme_effect = activation.get("programme_effect", {})
    for key, expected in {
        "active_registry": EXPECTED_ACTIVE_DIGEST,
        "routing_overlay": EXPECTED_ROUTING_DIGEST,
        "admission_registry": EXPECTED_ADMISSION_DIGEST,
        "runtime_contract": EXPECTED_RUNTIME_DIGEST,
    }.items():
        if (programme_effect.get(key) or {}).get("digest") != expected:
            errors.append(f"VGSE activation: activation {key} identity drift")
    obligation = activation.get("consumer_obligation", {})
    if (
        obligation.get("repin_required") is not True
        or obligation.get("repin_complete") is not False
        or obligation.get("programme_issue_may_close") is not False
        or obligation.get("required_runtime_digest") != EXPECTED_RUNTIME_DIGEST
    ):
        errors.append("VGSE activation: consumer obligation drift")
    if any((activation.get("claim_boundary") or {}).values()):
        errors.append("VGSE activation: activation claim boundary inflation")

    if on_disk:
        for path, expected, label in [
            (ACTIVE_PATH, EXPECTED_ACTIVE_DIGEST, "active registry"),
            (ROUTING_PATH, EXPECTED_ROUTING_DIGEST, "routing successor"),
            (ADMISSION_PATH, EXPECTED_ADMISSION_DIGEST, "admission registry"),
            (RUNTIME_PATH, EXPECTED_RUNTIME_DIGEST, "runtime contract"),
            (ACTIVATION_PATH, EXPECTED_ACTIVATION_DIGEST, "activation record"),
            (DECISION_PATH, EXPECTED_DECISION_DIGEST, "historical decision"),
        ]:
            if git_blob_sha1(path) != expected:
                errors.append(f"VGSE activation: on-disk {label} blob drift")

    return errors


def main() -> int:
    errors = validation_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(
        "validated VGSE bounded active routing, pending non-adjudicating Cert route, "
        "preserved NSOF intake boundary, and required INTELLECT repin"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
