#!/usr/bin/env python3
"""Apply and verify the governed INTELLECT live-profile reconciliation."""
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from release_trust_admin import (
    GitHubClient,
    ReleaseTrustError,
    branch_ruleset,
    canonical_sha256,
    normalize_ruleset,
    ruleset_errors,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "governance" / "intellect_profile_admin_contract.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "intellect_profile_admin_contract.schema.json"
REQUIRED_INSTALLATION_REPOSITORIES = {
    "grandchallenge/MATH-PROGRAMME",
    "grandchallenge/INTELLECT",
}
FALSE_BOUNDARIES = {
    "profile_conformance_authorized",
    "organization_wide_conformance",
    "mathematical_claim_authorized",
    "certification_claim_authorized",
    "novelty_claim_authorized",
    "priority_claim_authorized",
    "deployment_claim_authorized",
    "manufacturing_claim_authorized",
    "product_claim_authorized",
    "commercial_claim_authorized",
}


class IntellectProfileAdminError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_contract(contract: dict[str, Any], schema: dict[str, Any]) -> None:
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(contract),
        key=lambda error: list(error.path),
    )
    if errors:
        raise IntellectProfileAdminError(
            "; ".join(f"{error.json_path}: {error.message}" for error in errors)
        )
    names = [row["property_name"] for row in contract["property_schema_extensions"]]
    if names != ["constitutional_profile", "authority_scope"]:
        raise IntellectProfileAdminError("property-schema extension identity drift")
    for field in FALSE_BOUNDARIES:
        if contract["claim_boundaries"].get(field) is not False:
            raise IntellectProfileAdminError(f"claim-boundary inflation: {field}")


def normalize_installation_scope(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise IntellectProfileAdminError("installation scope response must be an object")
    rows = payload.get("repositories")
    if not isinstance(rows, list):
        raise IntellectProfileAdminError("installation scope repositories must be a list")
    repositories: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            raise IntellectProfileAdminError("malformed installation repository row")
        full_name = row.get("full_name")
        repository_id = row.get("id")
        if not isinstance(full_name, str) or not isinstance(repository_id, int):
            raise IntellectProfileAdminError("installation repository identity is malformed")
        repositories.append({"id": repository_id, "full_name": full_name})
    names = {row["full_name"] for row in repositories}
    if names != REQUIRED_INSTALLATION_REPOSITORIES:
        raise IntellectProfileAdminError(
            "Release Trust App installation scope must be exactly MATH-PROGRAMME and INTELLECT"
        )
    if len(repositories) != len(names):
        raise IntellectProfileAdminError("duplicate installation repository identity")
    total_count = payload.get("total_count")
    if total_count != len(repositories):
        raise IntellectProfileAdminError("installation repository count drift")
    return {
        "authentication": "github_app_installation",
        "repository_count": total_count,
        "repositories": sorted(repositories, key=lambda row: row["full_name"]),
    }


def property_update_payload(current: dict[str, Any], required_value: str) -> dict[str, Any]:
    if current.get("value_type") != "single_select":
        raise IntellectProfileAdminError("property must remain single_select")
    allowed = current.get("allowed_values")
    if not isinstance(allowed, list) or not all(isinstance(value, str) for value in allowed):
        raise IntellectProfileAdminError("property allowed_values are malformed")
    merged = list(allowed)
    if required_value not in merged:
        merged.append(required_value)
    if len(merged) != len(set(merged)):
        raise IntellectProfileAdminError("property allowed_values contain duplicates")
    return {
        "value_type": "single_select",
        "required": bool(current.get("required", False)),
        "default_value": current.get("default_value"),
        "description": current.get("description"),
        "allowed_values": merged,
        "values_editable_by": current.get("values_editable_by"),
        "require_explicit_values": bool(current.get("require_explicit_values", False)),
    }


def verify_property_schema_change(
    before: dict[str, Any], after: dict[str, Any], required_value: str
) -> None:
    immutable_fields = (
        "property_name",
        "value_type",
        "required",
        "default_value",
        "description",
        "values_editable_by",
        "require_explicit_values",
        "source_type",
    )
    for field in immutable_fields:
        if before.get(field) != after.get(field):
            raise IntellectProfileAdminError(
                f"property schema changed outside allowed_values: {field}"
            )
    before_allowed = before.get("allowed_values")
    after_allowed = after.get("allowed_values")
    if not isinstance(before_allowed, list) or not isinstance(after_allowed, list):
        raise IntellectProfileAdminError("property allowed_values readback is malformed")
    expected = list(before_allowed)
    if required_value not in expected:
        expected.append(required_value)
    if after_allowed != expected:
        raise IntellectProfileAdminError(
            "property allowed_values changed outside authorized extension"
        )


def normalize_property_values(rows: Any) -> dict[str, Any]:
    if not isinstance(rows, list):
        raise IntellectProfileAdminError("property-value response must be a list")
    result: dict[str, Any] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("property_name"), str):
            raise IntellectProfileAdminError("malformed property-value row")
        name = row["property_name"]
        if name in result:
            raise IntellectProfileAdminError(f"duplicate property-value row: {name}")
        result[name] = row.get("value")
    return result


def writable_ruleset(detail: dict[str, Any], target_name: str) -> dict[str, Any]:
    for field in ("target", "enforcement", "conditions", "rules"):
        if field not in detail:
            raise IntellectProfileAdminError(f"ruleset detail lacks {field}")
    return {
        "name": target_name,
        "target": detail["target"],
        "enforcement": detail["enforcement"],
        "bypass_actors": detail.get("bypass_actors") or [],
        "conditions": detail["conditions"],
        "rules": detail["rules"],
    }


def normalize_intellect_ruleset(detail: dict[str, Any]) -> dict[str, Any]:
    normalized = normalize_ruleset(detail)
    pull_request = next(
        (row for row in detail.get("rules", []) if row.get("type") == "pull_request"),
        {},
    )
    parameters = pull_request.get("parameters", {})
    normalized["allowed_merge_methods"] = sorted(
        str(value) for value in parameters.get("allowed_merge_methods") or []
    )
    return normalized


def validate_ruleset(normalized: dict[str, Any], contract: dict[str, Any]) -> None:
    expected = contract["ruleset"]
    if normalized.get("name") not in expected["allowed_pre_names"]:
        raise IntellectProfileAdminError("unexpected INTELLECT ruleset name")
    policy = {
        "strict_status_checks": expected["strict_status_checks"],
        "enforce_admins": expected["zero_bypass"],
        "required_approving_reviews": expected["required_approving_reviews"],
        "dismiss_stale_reviews": expected["dismiss_stale_reviews"],
        "require_last_push_approval": expected["require_last_push_approval"],
        "require_code_owner_reviews": expected["require_code_owner_reviews"],
        "required_conversation_resolution": expected["required_conversation_resolution"],
        "allow_force_pushes": expected["allow_force_pushes"],
        "allow_deletions": expected["allow_deletions"],
        "required_linear_history": expected["required_linear_history"],
    }
    current_errors = ruleset_errors(
        normalized, policy, expected["required_checks"], str(normalized["name"])
    )
    if sorted(normalized.get("allowed_merge_methods") or []) != sorted(
        expected["allowed_merge_methods"]
    ):
        current_errors.append("allowed merge methods drift")
    if current_errors:
        raise IntellectProfileAdminError("; ".join(current_errors))


def ruleset_equal_except_name(before: dict[str, Any], after: dict[str, Any]) -> bool:
    left = dict(before)
    right = dict(after)
    left.pop("name", None)
    right.pop("name", None)
    return left == right


def collect_state(client: GitHubClient, contract: dict[str, Any]) -> dict[str, Any]:
    org = contract["organization"]
    repo = contract["repository"]
    installation = normalize_installation_scope(
        client.request("GET", "/installation/repositories?per_page=100")
    )
    branch = urllib.parse.quote(contract["branch"], safe="")
    branch_data = client.request("GET", f"/repos/{repo}/branches/{branch}")
    main_sha = str(branch_data.get("commit", {}).get("sha") or "")
    if len(main_sha) != 40:
        raise IntellectProfileAdminError("protected-main identity is malformed")
    schemas = {
        row["property_name"]: client.request(
            "GET", f"/orgs/{org}/properties/schema/{row['property_name']}"
        )
        for row in contract["property_schema_extensions"]
    }
    values = normalize_property_values(
        client.request("GET", f"/repos/{repo}/properties/values")
    )
    detail = branch_ruleset(client, repo)
    normalized = normalize_intellect_ruleset(detail)
    validate_ruleset(normalized, contract)
    return {
        "actor": installation,
        "main_sha": main_sha,
        "property_schemas": schemas,
        "property_values": values,
        "ruleset_detail": detail,
        "ruleset": normalized,
    }


def apply_contract(
    client: GitHubClient, contract: dict[str, Any], before: dict[str, Any]
) -> list[dict[str, Any]]:
    org = contract["organization"]
    repo = contract["repository"]
    mutations: list[dict[str, Any]] = []
    for extension in contract["property_schema_extensions"]:
        name = extension["property_name"]
        current = before["property_schemas"][name]
        if current.get("property_name") != name:
            raise IntellectProfileAdminError(f"property identity drift: {name}")
        client.request(
            "PUT",
            f"/orgs/{org}/properties/schema/{name}",
            property_update_payload(current, extension["required_value"]),
        )
        mutations.append(
            {
                "operation": "extend_property_schema",
                "property_name": name,
                "required_value": extension["required_value"],
            }
        )
    client.request(
        "PATCH",
        f"/orgs/{org}/properties/values",
        {
            "repository_names": [contract["repository_name"]],
            "properties": [
                {"property_name": name, "value": value}
                for name, value in contract["repository_property_values"].items()
            ],
        },
    )
    mutations.append(
        {"operation": "apply_repository_property_values", "repository": repo}
    )
    detail = before["ruleset_detail"]
    ruleset_id = detail.get("id")
    if not isinstance(ruleset_id, int):
        raise IntellectProfileAdminError("ruleset detail lacks numeric id")
    client.request(
        "PUT",
        f"/repos/{repo}/rulesets/{ruleset_id}",
        writable_ruleset(detail, contract["ruleset"]["target_name"]),
    )
    mutations.append(
        {
            "operation": "rename_ruleset",
            "ruleset_id": ruleset_id,
            "target_name": contract["ruleset"]["target_name"],
        }
    )
    return mutations


def verify_after(
    before: dict[str, Any], after: dict[str, Any], contract: dict[str, Any]
) -> None:
    if before["main_sha"] != after["main_sha"]:
        raise IntellectProfileAdminError("protected main moved during administration")
    if before["actor"] != after["actor"]:
        raise IntellectProfileAdminError(
            "Release Trust App installation scope changed during administration"
        )
    expected_values = contract["repository_property_values"]
    actual_values = {
        name: after["property_values"].get(name) for name in expected_values
    }
    if actual_values != expected_values:
        raise IntellectProfileAdminError(f"property readback drift: {actual_values!r}")
    for extension in contract["property_schema_extensions"]:
        name = extension["property_name"]
        verify_property_schema_change(
            before["property_schemas"][name],
            after["property_schemas"][name],
            extension["required_value"],
        )
    if after["ruleset"]["name"] != contract["ruleset"]["target_name"]:
        raise IntellectProfileAdminError("ruleset target name missing after apply")
    if not ruleset_equal_except_name(before["ruleset"], after["ruleset"]):
        raise IntellectProfileAdminError(
            "ruleset changed outside the authorized name field"
        )
    validate_ruleset(after["ruleset"], contract)


def build_evidence(
    mode: str,
    contract: dict[str, Any],
    before: dict[str, Any],
    after: dict[str, Any],
    mutations: list[dict[str, Any]],
) -> dict[str, Any]:
    verify_after(before, after, contract)
    evidence = {
        "schema_version": "1.0.0",
        "operation_id": contract["operation_id"],
        "phase": contract["phase"],
        "mode": mode,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "api_version": contract["api_version"],
        "authority": contract["authority"],
        "organization": contract["organization"],
        "repository": contract["repository"],
        "contract_sha256": canonical_sha256(contract),
        "actor": after["actor"],
        "main_sha_before": before["main_sha"],
        "main_sha_after": after["main_sha"],
        "property_schemas_before": before["property_schemas"],
        "property_schemas_after": after["property_schemas"],
        "property_values_before": before["property_values"],
        "property_values_after": after["property_values"],
        "ruleset_before": before["ruleset_detail"],
        "ruleset_after": after["ruleset_detail"],
        "mutations": mutations,
        "verified": True,
        "claim_boundaries": contract["claim_boundaries"],
    }
    serialized = json.dumps(evidence, sort_keys=True)
    if "Authorization" in serialized or "Bearer " in serialized:
        raise IntellectProfileAdminError("evidence contains credential material")
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    return evidence


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("validate", "verify", "apply"), default="validate"
    )
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--digest", type=Path)
    parser.add_argument("--token-env", default="GCL_REPOSITORY_ADMIN_TOKEN")
    parser.add_argument("--wait-seconds", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        contract = load_json(args.contract)
        schema = load_json(args.schema)
        validate_contract(contract, schema)
        if args.mode == "validate":
            print("INTELLECT profile administration contract is valid")
            return 0
        client = GitHubClient(
            os.environ.get(args.token_env, ""), contract["api_version"]
        )
        before = collect_state(client, contract)
        mutations = (
            apply_contract(client, contract, before) if args.mode == "apply" else []
        )
        deadline = time.monotonic() + max(args.wait_seconds, 0)
        while True:
            try:
                after = collect_state(client, contract)
                evidence = build_evidence(
                    args.mode, contract, before, after, mutations
                )
                break
            except IntellectProfileAdminError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(min(15, max(1, int(deadline - time.monotonic()))))
        evidence_path = args.evidence or ROOT / contract["evidence"]["output"]
        digest_path = args.digest or ROOT / contract["evidence"]["digest_output"]
        evidence_path.write_text(
            json.dumps(evidence, indent=2) + "\n", encoding="utf-8"
        )
        digest_path.write_text(
            f"{evidence['evidence_sha256']}  {evidence_path.name}\n",
            encoding="utf-8",
        )
        print(json.dumps(evidence, indent=2))
        return 0
    except (
        OSError,
        json.JSONDecodeError,
        ReleaseTrustError,
        IntellectProfileAdminError,
    ) as exc:
        print(
            f"INTELLECT profile administration failed: {exc}", file=os.sys.stderr
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
