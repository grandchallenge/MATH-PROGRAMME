from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping

import yaml

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "governance/gcl_tcs_profile_authority_map.json"
POLICY_PATH = ROOT / "docs/council/submissions/GCL-TCS-00/GCL-TCS-00.policy.yaml"
ROLE_PATH = ROOT / "council_submissions/GCL-TCS-00/parts/05-review-roles-controls-change.md"
COUNCIL_PATH = ROOT / "docs/MATH_PROGRAMME_AGENT_COUNCIL.md"

EXPECTED_STANDARD = {"id": "GCL-TCS-00", "version": "0.1.0", "status": "candidate"}
EXPECTED_GATES = {f"G{i}" for i in range(10)}
MODE_BY_MATRIX = {"M": "required", "C": "conditional", "I": "inherited"}


class ProfileAuthorityMapError(RuntimeError):
    pass


def _read_json(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ProfileAuthorityMapError(f"{path}: expected mapping")
    return raw


def _read_policy(root: Path) -> dict[str, Any]:
    raw = yaml.safe_load((root / POLICY_PATH.relative_to(ROOT)).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ProfileAuthorityMapError("GCL-TCS policy must be a mapping")
    return raw


def _agent_council_roles(root: Path) -> set[str]:
    text = (root / COUNCIL_PATH.relative_to(ROOT)).read_text(encoding="utf-8")
    roles = set(re.findall(r"^\| The ([A-Za-z][A-Za-z ]+) \|", text, flags=re.MULTILINE))
    if not roles:
        raise ProfileAuthorityMapError("active Agent Council role table not found")
    return roles


def _require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_profile_authority_map(mapping: Any, *, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    if not isinstance(mapping, Mapping):
        return ["map: malformed_non_mapping"]

    policy = _read_policy(root)
    standard = policy.get("standard")
    profiles = policy.get("profiles")
    gate_matrix = policy.get("gate_matrix")
    mandatory_metadata = policy.get("mandatory_metadata", {}).get("core", [])

    _require(isinstance(standard, Mapping), "policy: standard_missing", errors)
    _require(isinstance(profiles, Mapping), "policy: profiles_missing", errors)
    _require(isinstance(gate_matrix, Mapping), "policy: gate_matrix_missing", errors)
    if errors:
        return sorted(set(errors))

    for key, value in EXPECTED_STANDARD.items():
        _require(standard.get(key) == value, f"policy: standard_{key}_drift", errors)
        _require(mapping.get("standard", {}).get(key) == value, f"map: standard_{key}_drift", errors)

    _require("owner" in mandatory_metadata, "policy: mandatory_artifact_owner_missing", errors)
    _require(mapping.get("mapping_status") == "APPROVED_MAPPING_OF_EXISTING_AUTHORITY", "map: mapping_status_invalid", errors)
    _require(mapping.get("record_type") == "DERIVATIVE_PROFILE_OWNER_REVIEW_ROLE_MAP", "map: record_type_invalid", errors)

    semantics = mapping.get("authority_semantics")
    if not isinstance(semantics, Mapping):
        errors.append("map: authority_semantics_missing")
        semantics = {}
    for key in (
        "mapping_is_authority_registry",
        "mapping_confers_authority_by_role_name",
        "mapping_replaces_artifact_owner",
        "mapping_activates_promotion_gate",
    ):
        _require(semantics.get(key) is False, f"authority_semantics: {key}_must_be_false", errors)
    _require(semantics.get("profile_lifecycle_owner_role") == "Steward", "authority_semantics: lifecycle_owner_must_be_Steward", errors)
    _require(semantics.get("artifact_owner_binding") == "mandatory_metadata.owner", "authority_semantics: artifact_owner_binding_invalid", errors)
    _require(semantics.get("artifact_owner_fixed_by_profile") is False, "authority_semantics: artifact_owner_must_not_be_fixed", errors)

    boundary = mapping.get("boundary")
    if not isinstance(boundary, Mapping):
        errors.append("map: boundary_missing")
        boundary = {}
    for key in (
        "standard_version_changed",
        "normative_source_changed",
        "constitutional_authority_created",
        "new_role_registry_created",
        "artifact_ownership_preassigned",
        "promotion_requested",
        "referee_disposition_created",
    ):
        _require(boundary.get(key) is False, f"boundary: {key}_must_be_false", errors)

    role_text = (root / ROLE_PATH.relative_to(ROOT)).read_text(encoding="utf-8")
    _require(
        "Roles identify review functions. They do not confer authority without a review record." in role_text,
        "role_source: non_conferral_clause_missing",
        errors,
    )
    _require(
        "| Steward | Standards selection, impact class, and lifecycle governance |" in role_text,
        "role_source: Steward_lifecycle_function_missing",
        errors,
    )

    allowed_roles = _agent_council_roles(root)
    mapped_profiles = mapping.get("profiles")
    if not isinstance(mapped_profiles, Mapping):
        return sorted(set(errors + ["map: profiles_missing"]))

    _require(set(mapped_profiles) == set(profiles), "map: profile_set_mismatch", errors)

    for profile_id, policy_profile in profiles.items():
        item = mapped_profiles.get(profile_id)
        if not isinstance(item, Mapping):
            errors.append(f"{profile_id}: mapping_missing")
            continue
        _require(item.get("name") == policy_profile.get("name"), f"{profile_id}: name_drift", errors)
        _require(item.get("version") == policy_profile.get("version"), f"{profile_id}: version_drift", errors)
        _require(item.get("profile_lifecycle_owner_role") == "Steward", f"{profile_id}: lifecycle_owner_must_be_Steward", errors)
        _require(item.get("artifact_owner_binding") == "mandatory_metadata.owner", f"{profile_id}: artifact_owner_binding_invalid", errors)

        gates = item.get("gates")
        if not isinstance(gates, Mapping):
            errors.append(f"{profile_id}: gates_missing")
            continue
        _require(set(gates) == EXPECTED_GATES, f"{profile_id}: gate_set_mismatch", errors)

        for gate in sorted(EXPECTED_GATES):
            gate_item = gates.get(gate)
            if not isinstance(gate_item, Mapping):
                errors.append(f"{profile_id}/{gate}: mapping_missing")
                continue
            matrix_value = gate_matrix.get(gate, {}).get(profile_id)
            expected_mode = MODE_BY_MATRIX.get(matrix_value)
            _require(expected_mode is not None, f"{profile_id}/{gate}: policy_matrix_value_invalid", errors)
            _require(gate_item.get("mode") == expected_mode, f"{profile_id}/{gate}: mode_mismatch", errors)

            review_roles = gate_item.get("review_roles")
            _require(isinstance(review_roles, list) and bool(review_roles), f"{profile_id}/{gate}: review_roles_missing", errors)
            if isinstance(review_roles, list):
                for role in review_roles:
                    _require(isinstance(role, str) and role in allowed_roles, f"{profile_id}/{gate}: unknown_review_role:{role}", errors)

            conditional_roles = gate_item.get("conditional_domain_roles", [])
            _require(isinstance(conditional_roles, list), f"{profile_id}/{gate}: conditional_domain_roles_invalid", errors)
            if isinstance(conditional_roles, list):
                for role in conditional_roles:
                    _require(isinstance(role, str) and role in allowed_roles, f"{profile_id}/{gate}: unknown_conditional_role:{role}", errors)

        _require(gates.get("G0", {}).get("review_roles") == ["Amanuensis"], f"{profile_id}/G0: registry_function_must_resolve_to_Amanuensis", errors)
        _require(gates.get("G1", {}).get("artifact_owner_required") is True, f"{profile_id}/G1: artifact_owner_must_remain_required", errors)
        _require("Steward" in gates.get("G1", {}).get("review_roles", []), f"{profile_id}/G1: Steward_missing", errors)
        _require(set(gates.get("G2", {}).get("review_roles", [])) == {"Amanuensis", "Cartographer"}, f"{profile_id}/G2: documentary_roles_mismatch", errors)
        _require(gates.get("G3", {}).get("review_roles") == ["Grammarian"], f"{profile_id}/G3: Grammarian_missing", errors)
        _require("Verifier" in gates.get("G4", {}).get("review_roles", []), f"{profile_id}/G4: Verifier_missing", errors)
        _require("Adversary" in gates.get("G6", {}).get("review_roles", []), f"{profile_id}/G6: Adversary_missing", errors)
        _require(gates.get("G8", {}).get("review_roles") == ["Referee"], f"{profile_id}/G8: Referee_mapping_invalid", errors)
        _require(gates.get("G8", {}).get("promotion_only") is True, f"{profile_id}/G8: promotion_only_required", errors)
        _require(set(gates.get("G9", {}).get("review_roles", [])) == {"Steward", "Amanuensis"}, f"{profile_id}/G9: release_roles_mismatch", errors)

    return sorted(set(errors))


def validate_file(*, root: Path = ROOT) -> list[str]:
    mapping = _read_json(root / MAP_PATH.relative_to(ROOT))
    return validate_profile_authority_map(mapping, root=root)
