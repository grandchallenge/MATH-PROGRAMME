#!/usr/bin/env python3
"""Narrow post-merge migration of MATH-PROGRAMME formal required contexts.

This operation mutates only the required-status-check context list in the exact
Programme ruleset. Every other writable ruleset field must survive unchanged.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any

from release_trust_admin import GitHubClient, ReleaseTrustError, branch_ruleset

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "governance" / "programme_formal_context_migration.json"
EXPECTED_OPERATION = "MP-PROGRAMME-FORMAL-CONTEXT-MIGRATION-001"
WRITABLE_TOP_LEVEL = ("name", "target", "enforcement", "bypass_actors", "conditions", "rules")


class MigrationError(RuntimeError):
    pass


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def load_contract(path: Path = DEFAULT_CONTRACT) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise MigrationError("migration contract root must be an object")
    required = {
        "schema_version",
        "operation_id",
        "repository",
        "ruleset_id",
        "ruleset_name",
        "from_required_checks",
        "to_required_checks",
        "preservation_rule",
        "idempotent_target_allowed",
        "authority_boundary",
    }
    missing = sorted(required - value.keys())
    if missing:
        raise MigrationError("migration contract missing: " + ", ".join(missing))
    if value["schema_version"] != "1.0.0" or value["operation_id"] != EXPECTED_OPERATION:
        raise MigrationError("migration contract identity drift")
    if value["repository"] != "grandchallenge/MATH-PROGRAMME":
        raise MigrationError("migration repository drift")
    if value["ruleset_id"] != 17137629 or value["ruleset_name"] != "Programme profile - main":
        raise MigrationError("Programme ruleset identity drift")
    if value["preservation_rule"] != "MUTATE_ONLY_REQUIRED_STATUS_CHECK_CONTEXT_LIST":
        raise MigrationError("migration preservation rule drift")
    if value["idempotent_target_allowed"] is not True:
        raise MigrationError("idempotent target must remain allowed")
    if any(flag is not False for flag in value["authority_boundary"].values()):
        raise MigrationError("migration authority boundary widened")
    expected_from = [
        "validate-json",
        "Replay LOG-GCD-001 in Lean",
        "Replay PC-WP04 bounded certificate",
        "Replay pinned Union-Closed MATHCERT evidence",
        "policy / policy",
        "security / action-policy",
    ]
    expected_to = [
        "validate-json",
        "formal-validation / formal-validation",
        "policy / policy",
        "security / action-policy",
    ]
    if value["from_required_checks"] != expected_from or value["to_required_checks"] != expected_to:
        raise MigrationError("required-context migration set drift")
    return value


def _status_rule(detail: dict[str, Any]) -> dict[str, Any]:
    matches = [
        rule
        for rule in detail.get("rules", [])
        if isinstance(rule, dict) and rule.get("type") == "required_status_checks"
    ]
    if len(matches) != 1:
        raise MigrationError(f"expected one required_status_checks rule, found {len(matches)}")
    parameters = matches[0].get("parameters")
    if not isinstance(parameters, dict):
        raise MigrationError("required_status_checks parameters are malformed")
    return matches[0]


def required_contexts(detail: dict[str, Any]) -> list[str]:
    parameters = _status_rule(detail)["parameters"]
    checks = parameters.get("required_status_checks")
    if not isinstance(checks, list):
        raise MigrationError("required_status_checks list is malformed")
    contexts = []
    for row in checks:
        if not isinstance(row, dict) or not isinstance(row.get("context"), str):
            raise MigrationError("required status-check row is malformed")
        contexts.append(row["context"])
    return contexts


def writable_payload(detail: dict[str, Any], contexts: list[str]) -> dict[str, Any]:
    missing = [key for key in WRITABLE_TOP_LEVEL if key not in detail]
    if missing:
        raise MigrationError("ruleset detail lacks writable fields: " + ", ".join(missing))
    payload = {key: copy.deepcopy(detail[key]) for key in WRITABLE_TOP_LEVEL}
    parameters = _status_rule(payload)["parameters"]
    parameters["required_status_checks"] = [{"context": context} for context in contexts]
    return payload


def preservation_projection(detail: dict[str, Any]) -> dict[str, Any]:
    payload = {key: copy.deepcopy(detail[key]) for key in WRITABLE_TOP_LEVEL if key in detail}
    parameters = _status_rule(payload)["parameters"]
    parameters["required_status_checks"] = "<MIGRATED_CONTEXT_LIST>"
    return payload


def validate_live_identity(detail: dict[str, Any], contract: dict[str, Any]) -> None:
    if detail.get("id") != contract["ruleset_id"]:
        raise MigrationError(
            f"Programme ruleset id drift: {detail.get('id')!r} != {contract['ruleset_id']!r}"
        )
    if detail.get("name") != contract["ruleset_name"]:
        raise MigrationError("Programme ruleset name drift")
    if detail.get("target") != "branch" or detail.get("enforcement") != "active":
        raise MigrationError("Programme ruleset is not active branch protection")


def migrate(client: GitHubClient, contract: dict[str, Any], *, apply: bool) -> dict[str, Any]:
    repository = contract["repository"]
    before = branch_ruleset(client, repository)
    validate_live_identity(before, contract)
    before_contexts = required_contexts(before)
    source = contract["from_required_checks"]
    target = contract["to_required_checks"]
    if before_contexts not in (source, target):
        raise MigrationError(f"unexpected live required contexts: {before_contexts!r}")
    before_projection = preservation_projection(before)
    before_projection_sha = canonical_sha256(before_projection)

    mutation_performed = False
    if before_contexts == source:
        if not apply:
            raise MigrationError("Programme ruleset still has legacy formal contexts")
        payload = writable_payload(before, target)
        client.request(
            "PUT",
            f"/repos/{repository}/rulesets/{contract['ruleset_id']}",
            payload,
        )
        mutation_performed = True

    after = branch_ruleset(client, repository)
    validate_live_identity(after, contract)
    after_contexts = required_contexts(after)
    if after_contexts != target:
        raise MigrationError(f"target required contexts not installed: {after_contexts!r}")
    after_projection = preservation_projection(after)
    after_projection_sha = canonical_sha256(after_projection)
    if after_projection != before_projection:
        raise MigrationError("ruleset changed outside the required-status-check context list")

    return {
        "schema_version": "1.0.0",
        "operation_id": contract["operation_id"],
        "repository": repository,
        "ruleset_id": contract["ruleset_id"],
        "ruleset_name": contract["ruleset_name"],
        "mutation_performed": mutation_performed,
        "before_required_checks": before_contexts,
        "after_required_checks": after_contexts,
        "preservation_projection_sha256_before": before_projection_sha,
        "preservation_projection_sha256_after": after_projection_sha,
        "preservation_verified": True,
        "authority_boundary": contract["authority_boundary"],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("validate", "verify", "apply"), default="validate")
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--token-env", default="GCL_REPOSITORY_ADMIN_TOKEN")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        contract = load_contract(args.contract)
        if args.mode == "validate":
            print("Programme formal-context migration contract is valid")
            return 0
        token = os.environ.get(args.token_env, "")
        client = GitHubClient(token, "2022-11-28")
        evidence = migrate(client, contract, apply=args.mode == "apply")
        if args.evidence:
            args.evidence.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(evidence, indent=2, sort_keys=True))
        return 0
    except (OSError, json.JSONDecodeError, ReleaseTrustError, MigrationError) as exc:
        print(f"Programme formal-context migration failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
