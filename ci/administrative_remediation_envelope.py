#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping

from autonomy_github import AutonomyError, Client, identity, install_bypass

ROOT = Path(__file__).resolve().parents[1]
ENVELOPE_PATH = ROOT / "governance/administrative_remediation_envelope.json"
EXPECTED_ENVELOPE_ID = "MP-ADMIN-REMEDIATION-ENVELOPE-001"
EXPECTED_ISSUE = 615
EXPECTED_REPOSITORY = "grandchallenge/MATH-PROGRAMME"
EXPECTED_RULESET_ID = 17137629
EXPECTED_ACTOR_ID = 4423678
EXPECTED_ACTOR_LOGIN = "gcl-release-trust[bot]"
EXPECTED_ACTOR_TYPE = "Integration"
EXPECTED_BYPASS_MODE = "pull_request"
EXPECTED_AUTHORIZATION_COMMENT_ID = 5349149366


def sha256_json(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_envelope(path: Path = ENVELOPE_PATH) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("envelope_id") != EXPECTED_ENVELOPE_ID:
        raise AutonomyError("remediation envelope id drift")
    if int(value.get("issue") or 0) != EXPECTED_ISSUE:
        raise AutonomyError("remediation envelope issue drift")
    if value.get("state") != "OPEN":
        raise AutonomyError("remediation envelope is not open")
    if value.get("repository") != EXPECTED_REPOSITORY:
        raise AutonomyError("remediation repository drift")
    steward = value.get("human_steward", {})
    if int(steward.get("initial_approval_comment_id") or 0) != EXPECTED_AUTHORIZATION_COMMENT_ID:
        raise AutonomyError("initial Human Steward approval binding drift")
    if steward.get("intermediate_approval_required") is not False:
        raise AutonomyError("intermediate Human Steward approval must remain disabled")
    if steward.get("final_closure_or_reactivation_approval_required") is not True:
        raise AutonomyError("final Human Steward approval boundary drift")
    target = value.get("ruleset_reconciliation", {})
    expected = {
        "ruleset_id": EXPECTED_RULESET_ID,
        "actor_id": EXPECTED_ACTOR_ID,
        "actor_login": EXPECTED_ACTOR_LOGIN,
        "actor_type": EXPECTED_ACTOR_TYPE,
        "bypass_mode": EXPECTED_BYPASS_MODE,
        "direct_protected_push": False,
        "bypass_exercise_authorized": False,
    }
    for key, expected_value in expected.items():
        if target.get(key) != expected_value:
            raise AutonomyError(f"remediation target drift: {key}")
    delegated = value.get("delegated_authority", {})
    for key in (
        "diagnose",
        "bounded_control_plane_repair",
        "repair_pull_requests",
        "exact_head_validation",
        "independent_non_author_review",
        "expected_head_protected_merge_after_review",
        "exact_ruleset_actor_reconciliation",
        "qualification_replay",
        "repeat_until_green_or_scope_expansion",
    ):
        if delegated.get(key) is not True:
            raise AutonomyError(f"delegated remediation authority missing: {key}")
    return value


def normalized_actors(value: Mapping[str, Any]) -> list[tuple[int, str, str]]:
    result: list[tuple[int, str, str]] = []
    for item in value.get("bypass_actors", []) or []:
        result.append(
            (
                int(item["actor_id"]),
                str(item["actor_type"]),
                str(item["bypass_mode"]),
            )
        )
    return sorted(result)


def preserved_body(value: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: value.get(key)
        for key in ("name", "target", "enforcement", "conditions", "rules")
    }


def reconcile_actor(admin_token: str, report_path: Path) -> dict[str, Any]:
    envelope = load_envelope()
    runtime_target = envelope["ruleset_reconciliation"]
    administrator = identity(
        EXPECTED_ACTOR_LOGIN,
        EXPECTED_ACTOR_ID,
        "delegated-remediation-ruleset-reconciliation",
    )
    if administrator.login != EXPECTED_ACTOR_LOGIN or administrator.app_id != EXPECTED_ACTOR_ID:
        raise AutonomyError("Administration actor identity drift")

    client = Client(admin_token)
    before = client.get(f"/repos/{EXPECTED_REPOSITORY}/rulesets/{EXPECTED_RULESET_ID}")
    before_actors = normalized_actors(before)
    desired = (EXPECTED_ACTOR_ID, EXPECTED_ACTOR_TYPE, EXPECTED_BYPASS_MODE)

    if desired in before_actors:
        after = before
        mutation_performed = False
        terminal_state = "RULESET_ACTOR_ALREADY_PRESENT__NO_MUTATION"
    else:
        observed_before, after = install_bypass(
            client,
            EXPECTED_REPOSITORY,
            EXPECTED_RULESET_ID,
            administrator,
        )
        if normalized_actors(observed_before) != before_actors:
            raise AutonomyError("ruleset changed between preflight and reconciliation")
        mutation_performed = True
        terminal_state = "RULESET_ACTOR_RECONCILED"

    after_actors = normalized_actors(after)
    if desired not in after_actors:
        raise AutonomyError("target ruleset actor missing after reconciliation")
    expected_after = sorted(before_actors if desired in before_actors else before_actors + [desired])
    if after_actors != expected_after:
        raise AutonomyError("ruleset actor reconciliation changed unexpected actors")
    if preserved_body(after) != preserved_body(before):
        raise AutonomyError("ruleset actor reconciliation changed non-actor fields")

    report = {
        "schema_version": "1.0.0",
        "envelope_id": EXPECTED_ENVELOPE_ID,
        "control_issue": EXPECTED_ISSUE,
        "initial_human_steward_approval_comment_id": EXPECTED_AUTHORIZATION_COMMENT_ID,
        "repository": EXPECTED_REPOSITORY,
        "ruleset_id": EXPECTED_RULESET_ID,
        "target_actor": {
            "actor_id": EXPECTED_ACTOR_ID,
            "actor_login": EXPECTED_ACTOR_LOGIN,
            "actor_type": EXPECTED_ACTOR_TYPE,
            "bypass_mode": EXPECTED_BYPASS_MODE,
        },
        "actor_present_before": desired in before_actors,
        "actor_present_after": True,
        "mutation_performed": mutation_performed,
        "before_actor_set": before_actors,
        "after_actor_set": after_actors,
        "before_ruleset_digest": sha256_json(before),
        "after_ruleset_digest": sha256_json(after),
        "existing_bypass_actors_preserved": True,
        "non_actor_fields_preserved": True,
        "direct_protected_push": False,
        "bypass_exercised": False,
        "receipt_mutation_performed": False,
        "ledger_mutation_performed": False,
        "mirror_mutation_performed": False,
        "reactivation_authorized": False,
        "terminal_state": terminal_state,
        "runtime_target": runtime_target,
        "run_identity": {
            "github_run_id": os.environ.get("GITHUB_RUN_ID", ""),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
            "github_sha": os.environ.get("GITHUB_SHA", ""),
            "github_workflow_ref": os.environ.get("GITHUB_WORKFLOW_REF", ""),
        },
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    reconcile = sub.add_parser("reconcile-actor")
    reconcile.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "validate":
        value = load_envelope()
        print(json.dumps({"state": "REMEDIATION_ENVELOPE_VALID", "envelope_id": value["envelope_id"]}, sort_keys=True))
        return 0

    token = os.environ.get("ADMIN_WRITE_TOKEN", "")
    if not token:
        raise AutonomyError("ADMIN_WRITE_TOKEN is required")
    reconcile_actor(token, args.report)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"REMEDIATION_ENVELOPE_FAILED_CLOSED__{type(exc).__name__}: {exc}", file=sys.stderr)
        raise
