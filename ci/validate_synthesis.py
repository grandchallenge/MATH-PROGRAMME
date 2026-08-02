#!/usr/bin/env python3
"""Validate the bounded GCL synthesis pilot and generated projections."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from render_synthesis import render_report, render_review_packet

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "synthesis" / "pilot_registry.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "gcl_synthesis_registry.schema.json"
DEFAULT_REPORT = ROOT / "docs" / "governance" / "GCL_SYNTHESIS_REPORT.md"
DEFAULT_REVIEW = ROOT / "docs" / "governance" / "GCL_SYNTHESIS_REVIEW_PACKET.md"

EXPECTED_SOURCES = {
    "SRC-TRUTH-SPINE": ("governance/gcl_truth_spine_registry.json", "c4b30773be2f3151b3e975131ab6510245a3810b"),
    "SRC-NEGATIVE-KNOWLEDGE": ("negative_knowledge/pilot_registry.json", "9e205e485dfc02e04049503d67082cb7f9340c24"),
    "SRC-PORTFOLIO": ("portfolio/pilot_registry.json", "9dd22242790ceb8a75632926bcd08838360b5a2f"),
    "SRC-CANDIDATE-ADMISSION": ("governance/campaign_admission_registry.json", "934eccd89fdbc3350fb4e9d89a0a9759bdb7fc61"),
}
EXPECTED_TRANSFERS = {
    "TR-TRUTH-SPINE-IDENTITY-001": "accepted_bounded",
    "TR-NEGATIVE-REOPEN-001": "accepted_bounded",
    "TR-PORTFOLIO-DEPENDENCY-001": "accepted_bounded",
    "TR-NS-GEOMETRY-ANALOGY-001": "rejected_analogy",
}
EXPECTED_CONTRADICTIONS = {
    "CD-AETHER-GITHUB-AUTHORITY-001": "preserve_boundary",
    "CD-VGSE-STAGE-SEPARATION-001": "preserve_boundary",
    "CD-PORTFOLIO-SYNTHESIS-DUP-001": "distinct_responsibilities",
    "CD-TRUTH-SPINE-SYNTHESIS-DUP-001": "reuse_existing_control",
}
EXPECTED_OFFICES = {"Axiomatist", "Cartographer", "Verifier", "Adversary", "Formalist", "Amanuensis", "Referee", "Human Steward"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(
    registry_path: Path = DEFAULT_REGISTRY,
    schema_path: Path = DEFAULT_SCHEMA,
    report_path: Path = DEFAULT_REPORT,
    review_path: Path = DEFAULT_REVIEW,
) -> list[str]:
    errors: list[str] = []
    try:
        registry = load_json(registry_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"registry load failed: {exc}"]
    try:
        schema = load_json(schema_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"schema load failed: {exc}"]

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(registry), key=lambda item: list(item.path)):
        location = "/".join(str(part) for part in error.path) or "<root>"
        errors.append(f"schema {location}: {error.message}")
    if errors:
        return errors

    if set(registry["activation"]["required_conditions"]) != {"external_exact_head_review", "human_steward_release", "protected_merge"}:
        errors.append("activation conditions must be the exact external review, Human release, and protected merge set")

    sources = {item["source_ref"]: item for item in registry["source_artifacts"]}
    if set(sources) != set(EXPECTED_SOURCES):
        errors.append("source artifacts must be the exact four protected pilot sources")
    for source_ref, (path, blob) in EXPECTED_SOURCES.items():
        source = sources.get(source_ref)
        if source and (source["path"], source["git_blob_sha1"]) != (path, blob):
            errors.append(f"{source_ref}: protected path or blob identity mismatch")
        if source and source["authority_class"] != "protected_normative_record":
            errors.append(f"{source_ref}: mutable or generated source cannot satisfy transfer evidence")

    transfers = registry["transfer_records"]
    transfer_ids = [item["transfer_id"] for item in transfers]
    if len(transfer_ids) != len(set(transfer_ids)):
        errors.append("transfer_id values must be unique")
    if {item["transfer_id"]: item["analysis_disposition"] for item in transfers} != EXPECTED_TRANSFERS:
        errors.append("transfer pilot membership or dispositions drifted")

    normalized_targets: set[tuple[str, str]] = set()
    for item in transfers:
        transfer_id = item["transfer_id"]
        if item["source_ref"] not in sources:
            errors.append(f"{transfer_id}: unknown source_ref")
        if item["source_ref"] not in item["evidence_links"]:
            errors.append(f"{transfer_id}: evidence_links must include source_ref")
        if not item["source_assumptions"] or not item["target_assumptions"]:
            errors.append(f"{transfer_id}: source and target assumptions are required")
        if not item["non_transferable_component"].strip():
            errors.append(f"{transfer_id}: non-transferability is required")
        if not item["falsifying_test"].strip():
            errors.append(f"{transfer_id}: falsifying test is required")
        if item["governance"]["automated"] or not item["governance"]["advisory_only"]:
            errors.append(f"{transfer_id}: automated or authoritative disposition is prohibited")
        if any(item["claim_boundaries"].values()):
            errors.append(f"{transfer_id}: claim-boundary widening is prohibited")

        target_key = (item["target"]["programme_id"], " ".join(item["target"]["obligation"].lower().split()))
        if target_key in normalized_targets:
            errors.append(f"{transfer_id}: duplicate relabeling of an existing target obligation")
        normalized_targets.add(target_key)

        if item["analysis_disposition"] == "accepted_bounded":
            if not item["bounded_executable_consequence"]:
                errors.append(f"{transfer_id}: accepted transfer requires a bounded executable consequence")
            if item["rejection_reason"] is not None:
                errors.append(f"{transfer_id}: accepted transfer cannot carry a rejection reason")
        else:
            if item["bounded_executable_consequence"] is not None:
                errors.append(f"{transfer_id}: rejected analogy cannot retain executable authority")
            if not item["rejection_reason"]:
                errors.append(f"{transfer_id}: rejected analogy requires a rejection reason")

    if sum(item["analysis_disposition"] == "accepted_bounded" for item in transfers) != 3:
        errors.append("pilot must contain exactly three accepted bounded transfers")
    if sum(item["analysis_disposition"] == "rejected_analogy" for item in transfers) != 1:
        errors.append("pilot must contain exactly one rejected analogy")

    contradictions = registry["contradiction_records"]
    contradiction_map = {item["record_id"]: item["disposition"] for item in contradictions}
    if contradiction_map != EXPECTED_CONTRADICTIONS:
        errors.append("contradiction and duplication pilot membership or dispositions drifted")
    if len(contradiction_map) != len(contradictions):
        errors.append("contradiction record IDs must be unique")
    for item in contradictions:
        for source_ref in item["source_refs"]:
            if source_ref not in sources:
                errors.append(f"{item['record_id']}: unknown source_ref")
        if not item["must_not_do"].strip():
            errors.append(f"{item['record_id']}: contradiction or duplication collapse must be prohibited")
        if item["kind"] == "contradiction" and item["disposition"] != "preserve_boundary":
            errors.append(f"{item['record_id']}: contradiction must remain preserved")
        if item["kind"] == "duplication" and item["disposition"] not in {"distinct_responsibilities", "reuse_existing_control"}:
            errors.append(f"{item['record_id']}: duplication must separate responsibilities or reuse control")
        if any(item["claim_boundaries"].values()):
            errors.append(f"{item['record_id']}: claim-boundary widening is prohibited")

    offices = [item["office"] for item in registry["review_packet"]]
    if set(offices) != EXPECTED_OFFICES or len(offices) != len(EXPECTED_OFFICES):
        errors.append("review packet must contain the exact eight offices once each")
    for item in registry["review_packet"]:
        if item["status"] != "pending_external_review" or item["may_self_authenticate"]:
            errors.append(f"{item['office']}: review packet cannot self-authenticate")

    if any(registry["claim_boundaries"].values()):
        errors.append("registry claim-boundary widening is prohibited")

    try:
        actual_report = report_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"generated report load failed: {exc}")
    else:
        if actual_report != render_report(registry):
            errors.append("generated synthesis report does not match protected records")

    try:
        actual_review = review_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"generated review packet load failed: {exc}")
    else:
        if actual_review != render_review_packet(registry):
            errors.append("generated synthesis review packet does not match protected records")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"synthesis validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("synthesis pilot registry is valid: 4 transfers, 4 contradiction/duplication records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
