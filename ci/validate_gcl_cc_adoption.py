#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ADOPTION = ROOT / "governance" / "GCL-CC-00-ADOPTION.json"
SCHEMA = ROOT / "schemas" / "gcl_cc_programme_adoption.schema.json"


class CoreClarityAdoptionError(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise CoreClarityAdoptionError(f"expected object: {path}")
    return value


def validate(root: Path = ROOT) -> None:
    adoption = load(root / "governance" / "GCL-CC-00-ADOPTION.json")
    schema = load(root / "schemas" / "gcl_cc_programme_adoption.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        adoption,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    if adoption["applicability"] != {
        "scope": "all_governed_GCL_campaigns_in_MATH_PROGRAMME",
        "canonical_campaign_record_required": True,
        "human_view_derived_or_validated": True,
        "operational_presentational_drift_blocking": True,
        "fresh_session_resume_from_protected_state": True,
    }:
        raise CoreClarityAdoptionError("GCL-CC-00 applicability contract drift")

    if adoption["lifecycle_contracts"]["external_agent"] != [
        "PREPARED", "LEASED", "LAUNCHED", "RETURNED", "CAPTURED",
        "ADJUDICATING", "ACCEPTED", "REJECTED", "SUPERSEDED", "CLOSED",
    ]:
        raise CoreClarityAdoptionError("external-agent lifecycle contract drift")
    if adoption["lifecycle_contracts"]["leased_not_launched_substate"] != "LEASED_NOT_LAUNCHED":
        raise CoreClarityAdoptionError("LEASED_NOT_LAUNCHED substate missing")
    if adoption["lifecycle_contracts"]["competition"] != [
        "CANDIDATE", "LOCALLY_VERIFIED", "CERT_PENDING", "CERTIFIED",
        "SUBMISSION_READY", "SUBMITTED", "ACCEPTED", "REJECTED",
    ]:
        raise CoreClarityAdoptionError("competition lifecycle contract drift")
    if adoption["lifecycle_contracts"]["explicit_not_submitted_required"] is not True:
        raise CoreClarityAdoptionError("explicit NOT_SUBMITTED requirement weakened")

    if not all(adoption["completion_contract"].values()):
        raise CoreClarityAdoptionError("completion contract may not omit a Core Clarity condition")

    remediation = adoption["remediation_contract"]
    if remediation["permitted_modes"] != ["REPAIR_IN_PLACE", "EXPLICIT_SUPERSESSION_WITH_MIGRATION"]:
        raise CoreClarityAdoptionError("remediation modes drift")
    if remediation["unresolved_remediation_layering_permitted"] is not False:
        raise CoreClarityAdoptionError("unresolved remediation layering may not be enabled")
    if remediation["migration_and_retirement_required_for_parallel_replacement"] is not True:
        raise CoreClarityAdoptionError("parallel replacement must require migration and retirement")

    enforcement = adoption["enforcement"]
    if enforcement != {
        "initial_campaign": "OPENMATH-2026",
        "canonical_state": "governance/openmath_2026_campaign_state.json",
        "human_view": "docs/campaigns/OPENMATH_2026_STATUS.md",
        "local_validator": "ci/validate_openmath_2026_core_clarity.py",
        "live_verification": "required_before_campaign_transition",
        "on_drift": "BLOCK_DISCRETIONARY_SUBSTANTIVE_ADVANCEMENT",
    }:
        raise CoreClarityAdoptionError("GCL-CC-00 enforcement profile drift")

    if any(bool(value) for value in adoption["claim_boundaries"].values()):
        raise CoreClarityAdoptionError("GCL-CC-00 adoption widens prohibited authority")


if __name__ == "__main__":
    validate()
    print("GCL-CC-00 Programme adoption: valid")
