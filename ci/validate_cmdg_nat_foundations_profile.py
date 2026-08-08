#!/usr/bin/env python3
"""Fail-closed validation for CMDG-NAT-CONCORDANCE-FOUNDATIONS-PROFILE-001."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "cmdg_nat_concordance_foundations_profile.schema.json"
PROFILE = ROOT / "governance" / "cmdg_nat_concordance_foundations_profile_001.json"
TOOLCHAIN = ROOT / "fixtures" / "formal" / "LOG-GCD-001" / "lean-toolchain"
LAKE_MANIFEST = ROOT / "fixtures" / "formal" / "LOG-GCD-001" / "lake-manifest.json"

EXPECTED_ZF_SINGLE_AXIOMS = {
    "EXTENSIONALITY",
    "PAIRING",
    "UNION",
    "POWER_SET",
    "INFINITY",
    "FOUNDATION",
}
EXPECTED_ZF_SCHEMAS = {"SEPARATION_SCHEMA", "REPLACEMENT_SCHEMA"}
EXPECTED_ZFC_ITEMS = EXPECTED_ZF_SINGLE_AXIOMS | EXPECTED_ZF_SCHEMAS | {"CHOICE"}
EXPECTED_NONCLAIMS = {
    "consistency",
    "standard_model",
    "foundational_equivalence",
    "definitional_identity",
    "foundational_concordance",
    "graph_certified",
    "global_dependency_completeness",
}
EXPECTED_ENV_EVIDENCE = {
    "fixtures/formal/LOG-GCD-001/lean-toolchain@fd85b262bf1c734663aa8292b0101f672168788f",
    "fixtures/formal/LOG-GCD-001/lake-manifest.json@99d43177d509c4ceb340c8b2e6330e9c75233169",
}


class FoundationProfileError(RuntimeError):
    def __init__(self, code: str, message: str):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message


def reject(code: str, message: str) -> None:
    raise FoundationProfileError(code, message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        reject("JSON_LOAD_FAILED", f"{path}: {exc}")
    if not isinstance(value, dict):
        reject("JSON_ROOT_MALFORMED", f"{path} root must be an object")
    return value


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def validate_schema(profile: dict[str, Any], schema: dict[str, Any] | None = None) -> None:
    schema = schema or load_json(SCHEMA)
    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:
        reject("SCHEMA_INVALID", str(exc))
    errors = sorted(Draft202012Validator(schema).iter_errors(profile), key=lambda e: list(e.path))
    if errors:
        error = errors[0]
        path = ".".join(str(part) for part in error.path) or "<root>"
        reject("SCHEMA_VIOLATION", f"{path}: {error.message}")


def _assert_nonclaims(profile: dict[str, Any]) -> None:
    for section_name in (
        "syntactic_zfc_profile",
        "semantic_set_realization_profile",
        "categorical_nno_profile",
        "dtt_nat_profile",
    ):
        flags = profile[section_name]["nonclaims"]
        if set(flags) != EXPECTED_NONCLAIMS:
            reject("NONCLAIM_SET_DRIFT", section_name)
        if any(flags.values()):
            reject("PROHIBITED_FOUNDATIONAL_OVERCLAIM", section_name)


def _validate_zfc(profile: dict[str, Any]) -> None:
    zfc = profile["syntactic_zfc_profile"]
    inventory = zfc["zf_axiom_inventory"]
    if len({entry["axiom_id"] for entry in inventory}) != len(inventory):
        reject("DUPLICATE_ZF_AXIOM", "ZF inventory contains duplicate identifiers")
    singles = {entry["axiom_id"] for entry in inventory if entry["kind"] == "SINGLE_AXIOM"}
    schemas = {entry["axiom_id"] for entry in inventory if entry["kind"] == "AXIOM_SCHEMA"}
    if singles != EXPECTED_ZF_SINGLE_AXIOMS:
        reject("INCOMPLETE_ZF_AXIOM_INVENTORY", f"single axioms: {sorted(singles)}")
    if schemas != EXPECTED_ZF_SCHEMAS:
        reject("SCHEMA_AXIOM_MISCLASSIFIED", f"axiom schemas: {sorted(schemas)}")
    for entry in inventory:
        if entry["kind"] == "AXIOM_SCHEMA" and not entry.get("schema_parameterization"):
            reject("SCHEMA_PARAMETERIZATION_MISSING", entry["axiom_id"])
        if entry["kind"] == "SINGLE_AXIOM" and "schema_parameterization" in entry:
            reject("SINGLE_AXIOM_SCHEMA_CONFUSION", entry["axiom_id"])
    if zfc["derived_theorems"] != [
        {"theorem_id": "EMPTY_SET", "status": "DERIVED_NOT_PRIMITIVE_AXIOM"}
    ]:
        reject("ZF_PRESENTATION_DRIFT", "EMPTY_SET must remain derived in this exact presentation")
    if not zfc["logic"]["classicality_explicit"]:
        reject("HIDDEN_CLASSICALITY", "object-theory classicality must be explicit")
    if not zfc["substrate_separation"]["conflation_prohibited"]:
        reject("SUBSTRATE_OBJECT_THEORY_CONFLATION", "Lean substrate and ZFC object theory must remain distinct")


def _validate_environment(profile: dict[str, Any]) -> None:
    env = profile["proof_environment"]
    if set(env["evidence_refs"]) != EXPECTED_ENV_EVIDENCE:
        reject("PROOF_ENVIRONMENT_EVIDENCE_DRIFT", "retained local pins changed")
    try:
        toolchain_text = TOOLCHAIN.read_text(encoding="utf-8").strip()
        manifest = json.loads(LAKE_MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        reject("PROOF_ENVIRONMENT_UNAVAILABLE", str(exc))
    if toolchain_text != env["lean_toolchain"]:
        reject("LEAN_TOOLCHAIN_PIN_DRIFT", f"{toolchain_text!r} != {env['lean_toolchain']!r}")
    toolchain_ref = f"fixtures/formal/LOG-GCD-001/lean-toolchain@{git_blob_sha1(TOOLCHAIN)}"
    manifest_ref = f"fixtures/formal/LOG-GCD-001/lake-manifest.json@{git_blob_sha1(LAKE_MANIFEST)}"
    if {toolchain_ref, manifest_ref} != EXPECTED_ENV_EVIDENCE:
        reject("LOCAL_PIN_BLOB_DRIFT", "retained Lean environment blobs changed")
    mathlib_packages = [
        package
        for package in manifest.get("packages", [])
        if isinstance(package, dict) and package.get("name") == "mathlib"
    ]
    if len(mathlib_packages) != 1:
        reject("MATHLIB_PIN_MALFORMED", "expected exactly one mathlib package")
    mathlib = mathlib_packages[0]
    if mathlib.get("url") != "https://github.com/leanprover-community/mathlib4":
        reject("MATHLIB_REPOSITORY_DRIFT", str(mathlib.get("url")))
    if mathlib.get("rev") != env["mathlib"]["commit"]:
        reject("MATHLIB_COMMIT_DRIFT", f"{mathlib.get('rev')} != {env['mathlib']['commit']}")


def _validate_set_realization(profile: dict[str, Any]) -> None:
    realization = profile["semantic_set_realization_profile"]
    carrier_source = realization["carrier"]["source"]
    env = profile["proof_environment"]
    if carrier_source["repository"] != env["mathlib"]["repository"]:
        reject("SET_CARRIER_REPOSITORY_DRIFT", carrier_source["repository"])
    if carrier_source["commit"] != env["mathlib"]["commit"]:
        reject("SET_CARRIER_COMMIT_DRIFT", carrier_source["commit"])
    obligations = realization["object_theory_obligation_status"]
    ids = {item["object_theory_item"] for item in obligations}
    if ids != EXPECTED_ZFC_ITEMS:
        reject("SET_REALIZATION_OBLIGATION_INVENTORY_DRIFT", f"{sorted(ids)}")
    for item in obligations:
        if item["object_theory_item"] == "CHOICE":
            if item["programme_formula_crosswalk"] != "DIRECT_DECLARATION_IDENTIFIED":
                reject("CHOICE_DECLARATION_NOT_IDENTIFIED", str(item))
        elif item["programme_formula_crosswalk"] != "NOT_YET_ADMITTED":
            reject(
                "UNREVIEWED_SET_THEORY_CROSSWALK_PROMOTION",
                item["object_theory_item"],
            )
    if realization["programme_realizes_as_status"] != "NOT_ADMITTED":
        reject("UNADMITTED_REALIZES_AS_PROMOTION", realization["programme_realizes_as_status"])


def _validate_nno(profile: dict[str, Any]) -> None:
    nno = profile["categorical_nno_profile"]
    if nno["binding_status"] != "NO_CONCRETE_IMPLEMENTATION_BOUND":
        reject("UNREVIEWED_NNO_IMPLEMENTATION_BINDING", nno["binding_status"])
    if nno["ambient_category"]["binary_coproducts_required"]:
        reject("UNNECESSARY_NNO_COPRODUCT_ASSUMPTION", "direct recursor profile does not require binary coproducts")
    expected_equations = ["zero ≫ h = x0", "succ ≫ h = h ≫ s"]
    if nno["universal_property"]["equations"] != expected_equations:
        reject("MALFORMED_NNO_UNIVERSAL_PROPERTY", str(nno["universal_property"]["equations"]))
    uniqueness = nno["uniqueness_status"]
    if uniqueness["definitional_identity"]:
        reject("NNO_DEFINITIONAL_IDENTITY_OVERCLAIM", "NNO uniqueness is only up to unique isomorphism")
    if nno["initial_algebra_reformulation"]["used_as_defining_requirement"]:
        reject("NNO_PROFILE_SCOPE_DRIFT", "1+(-) initial-algebra reformulation is not the defining requirement")


def _validate_dtt(profile: dict[str, Any]) -> None:
    dtt = profile["dtt_nat_profile"]
    if dtt["source"]["commit"] != profile["proof_environment"]["lean_commit"]:
        reject("DTT_NAT_COMMIT_DRIFT", dtt["source"]["commit"])
    if dtt["declaration"] != "Nat" or dtt["constructors"] != ["Nat.zero", "Nat.succ"]:
        reject("DTT_NAT_IDENTITY_DRIFT", "Nat identity or constructors changed")
    if dtt["eliminator"]["declaration"] != "Nat.rec":
        reject("DTT_NAT_ELIMINATOR_DRIFT", dtt["eliminator"]["declaration"])


def _validate_relation_policy(profile: dict[str, Any]) -> None:
    policy = profile["cross_foundational_relation_policy"]
    if policy["current_promoted_edges"]:
        reject("UNADMITTED_FOUNDATIONAL_EDGE", "this operation may not promote a foundational edge")
    if policy["foundational_concordance_status"] != "NOT_ESTABLISHED":
        reject("PREMATURE_FOUNDATIONAL_CONCORDANCE", policy["foundational_concordance_status"])
    required = {
        "EXPLICIT_SOURCE_IDENTITY",
        "EXPLICIT_TARGET_IDENTITY",
        "EXPLICIT_DIRECTION",
        "EXACT_PROFILE_VERSION_BINDINGS",
        "EVIDENCE_REFERENCES",
        "INDEPENDENT_REVIEW",
        "LIMITATIONS_AND_NONCLAIMS",
        "NO_AUTOMATIC_DEFINITIONAL_IDENTITY",
    }
    if not required.issubset(set(policy["evidence_requirements"])):
        reject("FOUNDATIONAL_RELATION_EVIDENCE_INCOMPLETE", "future relation evidence contract is incomplete")


def _validate_claim_boundary(profile: dict[str, Any]) -> None:
    boundary = profile["claim_boundary"]
    if boundary["profile_prerequisite_satisfied_by_artifact_alone"]:
        reject("PROTECTED_ADMISSION_BYPASS", "artifact alone cannot discharge C03")
    prohibited = {
        "realizes_as_conferred",
        "nat_concordance_conferred",
        "foundational_equivalence_conferred",
        "graph_certified_conferred",
        "global_dependency_completeness_claim",
        "consistency_claim",
        "standard_model_claim",
    }
    if any(boundary[key] for key in prohibited):
        reject("PROHIBITED_AUTHORITY_PROMOTION", "profile operation attempted a stronger claim")
    if not boundary["c04_c05_c06_unchanged"]:
        reject("UNRELATED_CORRECTION_GATE_DRIFT", "C04-C06 must remain unaffected")


def validate_profile(
    profile: dict[str, Any],
    *,
    schema: dict[str, Any] | None = None,
    validate_local_environment: bool = True,
) -> None:
    validate_schema(profile, schema)
    _assert_nonclaims(profile)
    _validate_zfc(profile)
    if validate_local_environment:
        _validate_environment(profile)
    _validate_set_realization(profile)
    _validate_nno(profile)
    _validate_dtt(profile)
    _validate_relation_policy(profile)
    _validate_claim_boundary(profile)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", type=Path, default=PROFILE)
    parser.add_argument("--schema", type=Path, default=SCHEMA)
    args = parser.parse_args()
    profile = load_json(args.profile)
    schema = load_json(args.schema)
    validate_profile(profile, schema=schema)
    print(
        "CMDG foundations profile valid; C03 profile-definition prerequisite remains "
        "conditional on independent exact-head review and protected admission."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
