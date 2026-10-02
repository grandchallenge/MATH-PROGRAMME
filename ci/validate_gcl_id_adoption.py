#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ADOPTION = ROOT / "governance" / "GCL-ID-00-ADOPTION.json"
ADOPTION_SCHEMA = ROOT / "schemas" / "gcl_id_programme_adoption.schema.json"
PREFLIGHT_SCHEMA = ROOT / "schemas" / "identifiability_preflight.schema.json"
PREFLIGHT_DIR = ROOT / "governance" / "identifiability_preflights"
REVIEW_SCHEMA = ROOT / "schemas" / "gcl_id_observational_review.schema.json"
REVIEW = ROOT / "governance" / "GCL-ID-00-OBSERVATIONAL-REVIEW.json"


class GCLIDAdoptionError(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GCLIDAdoptionError(f"expected object: {path}")
    return value


def validate_with_schema(instance: dict[str, Any], schema_path: Path) -> None:
    schema = load(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        instance,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )


def validate_adoption_object(adoption: dict[str, Any]) -> None:
    validate_with_schema(adoption, ADOPTION_SCHEMA)

    if adoption["levels"]["default"] != "ID-PREFLIGHT-LITE":
        raise GCLIDAdoptionError("default level must remain ID-PREFLIGHT-LITE")
    if adoption["anti_bureaucracy"]["injectivity_proof_required_before_experimentation"]:
        raise GCLIDAdoptionError("adoption may not require an injectivity proof before experimentation")
    if not adoption["anti_bureaucracy"]["unresolved_is_valid"]:
        raise GCLIDAdoptionError("UNRESOLVED must remain a valid preflight state")
    if adoption["anti_bureaucracy"]["retrospective_rewrite_required"]:
        raise GCLIDAdoptionError("adoption may not require retrospective rewrite")
    if adoption["historical_motivation"]["counts_toward_prospective_review"]:
        raise GCLIDAdoptionError("VGSE-WP06 may motivate but may not count toward the prospective review")
    if any(bool(value) for value in adoption["claim_boundaries"].values()):
        raise GCLIDAdoptionError("GCL-ID-00 adoption may not widen claim or authority boundaries")

    review = adoption["observational_review"]
    if (review["minimum_completed_packages"], review["target_completed_packages"], review["maximum_completed_packages_before_review_required"]) != (8, 10, 12):
        raise GCLIDAdoptionError("observational review window must remain 8 / 10 / 12")


def semantic_preflight_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    classification = record["recoverable_object"]["classification"]
    equivalence_status = record["observational_equivalence"]["status"]
    full_permitted = record["solver_gate"]["full_representative_recovery_claim_permitted"]
    extra = record["symmetry_breaking"]["extra_information_or_normalization_for_stronger_recovery"]

    if classification in {
        "QUOTIENT_IDENTIFIABLE_ONLY",
        "LOCAL_OR_PARTIAL_IDENTIFIABILITY",
        "STRUCTURAL_NON_IDENTIFIABILITY",
        "UNRESOLVED",
    } and full_permitted:
        errors.append("full representative recovery cannot be permitted by a partial, quotient, structural-obstruction, or unresolved classification")

    if classification == "FULL_IDENTIFIABILITY":
        if equivalence_status != "INJECTIVITY_ESTABLISHED":
            errors.append("FULL_IDENTIFIABILITY requires an established injectivity disposition, not merely absence of a known symmetry")
        if not record["evidence_refs"]:
            errors.append("FULL_IDENTIFIABILITY requires evidence references")

    if classification == "IDENTIFIABLE_WITH_DECLARED_NORMALIZATION" and not extra:
        errors.append("declared-normalization identifiability requires the added normalization or information to be named")

    if equivalence_status == "NONTRIVIAL_EQUIVALENCE_FOUND" and classification == "FULL_IDENTIFIABILITY":
        errors.append("a nontrivial observational equivalence contradicts unqualified FULL_IDENTIFIABILITY")

    if record["level"] == "ID-CERTIFIED" and record["status"] == "COMPLETE":
        if not any("MATHCERT" in ref.upper() for ref in record["evidence_refs"]):
            errors.append("completed ID-CERTIFIED records require a durable MATHCERT evidence reference")

    if any(bool(value) for value in record["claim_boundaries"].values()):
        errors.append("preflight records cannot manufacture claim authority")

    return errors


def validate_preflight_object(record: dict[str, Any]) -> None:
    validate_with_schema(record, PREFLIGHT_SCHEMA)
    errors = semantic_preflight_errors(record)
    if errors:
        raise GCLIDAdoptionError("; ".join(errors))


def discover_preflights(root: Path = ROOT) -> list[dict[str, Any]]:
    directory = root / "governance" / "identifiability_preflights"
    if not directory.is_dir():
        return []
    rows: list[dict[str, Any]] = []
    identifiers: set[str] = set()
    for path in sorted(directory.glob("*.json")):
        record = load(path)
        validate_preflight_object(record)
        if record["identifier"] in identifiers:
            raise GCLIDAdoptionError(f"duplicate identifiability preflight identifier: {record['identifier']}")
        identifiers.add(record["identifier"])
        rows.append(record)
    return rows


def validate_review_requirement(records: list[dict[str, Any]], review: dict[str, Any] | None) -> None:
    completed = sum(record["status"] == "COMPLETE" for record in records)

    if review is not None:
        validate_with_schema(review, REVIEW_SCHEMA)
        reviewed_count = review["completed_package_count"]
        if reviewed_count > completed:
            raise GCLIDAdoptionError("observational review cannot claim more completed packages than exist")
        for key, value in review["metrics"].items():
            if value > reviewed_count:
                raise GCLIDAdoptionError(f"observational review metric exceeds reviewed package count: {key}")
        if any(bool(value) for value in review["claim_boundaries"].values()):
            raise GCLIDAdoptionError("observational review cannot widen claim authority")

    if completed >= 12 and review is None:
        raise GCLIDAdoptionError("GCL-ID-00 observational review is required no later than 12 completed in-scope packages")


def validate(root: Path = ROOT) -> None:
    adoption_path = root / "governance" / "GCL-ID-00-ADOPTION.json"
    adoption = load(adoption_path)
    validate_adoption_object(adoption)

    for schema_path in (
        root / "schemas" / "identifiability_preflight.schema.json",
        root / "schemas" / "gcl_id_observational_review.schema.json",
    ):
        jsonschema.Draft202012Validator.check_schema(load(schema_path))

    records = discover_preflights(root)
    review_path = root / "governance" / "GCL-ID-00-OBSERVATIONAL-REVIEW.json"
    review = load(review_path) if review_path.is_file() else None
    validate_review_requirement(records, review)


if __name__ == "__main__":
    validate()
    print("GCL-ID-00 Programme adoption: valid")
