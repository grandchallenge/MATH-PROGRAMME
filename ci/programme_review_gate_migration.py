#!/usr/bin/env python3
"""One-shot narrow migration: eliminate routine Programme non-author PR review.

Only two pull_request review parameters may change. Protected CI, existing
GitHub App bypass scope, branch conditions, merge queue and specialist claim
certification remain unchanged. Runs only with short-lived Release Trust
administration token from the protected workflow.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_trust_admin import GitHubClient, branch_ruleset

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "governance/programme_review_gate_migration.json"
WRITABLE = ("name", "target", "enforcement", "bypass_actors", "conditions", "rules")


def load_contract() -> dict:
    c = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    if not isinstance(c, dict) or set(c) != {
        "schema_version", "operation_id", "authority", "repository",
        "ruleset_id", "ruleset_name", "from", "to",
        "retained_check_contexts", "retained_merge_queue_ruleset_id",
        "retained_merge_queue_check", "preserve_every_other_writable_ruleset_field",
        "enforce_no_new_bypass_actors", "authorization_boundary", "nonpromotion"
    }:
        raise ValueError("exact-scope migration schema drift")
    if (c["schema_version"] != "1.0.0" or
            c["operation_id"] != "MP-ROUTINE-REVIEW-GATE-REMOVAL-001" or
            c["authority"] != "MP-STREAMLINED-EXECUTION-001" or
            c["repository"] != "grandchallenge/MATH-PROGRAMME" or
            c["ruleset_id"] != 17137629 or
            c["ruleset_name"] != "Programme profile - main"):
        raise ValueError("migration identity drift")
    if c["from"] != {"required_approving_review_count": 1,
                     "require_last_push_approval": True}:
        raise ValueError("unexpected source review policy")
    if c["to"] != {"required_approving_review_count": 0,
                   "require_last_push_approval": False}:
        raise ValueError("unexpected target review policy")
    if c["retained_check_contexts"] != [
            "validate-json", "formal-validation / formal-validation",
            "policy / policy", "security / action-policy"
    ]:
        raise ValueError("required CI contract drift")
    if (c["retained_merge_queue_ruleset_id"] != 21969152 or
            c["retained_merge_queue_check"] != "routing-enforcement" or
            c["preserve_every_other_writable_ruleset_field"] is not True or
            c["enforce_no_new_bypass_actors"] is not True or
            any(value is not False for value in c["authorization_boundary"].values())):
        raise ValueError("migration authority boundary drift")
    return c


def review_params(detail: dict) -> dict:
    rules = [r for r in detail["rules"] if r["type"] == "pull_request"]
    if len(rules) != 1:
        raise ValueError("expected exactly one Programme PR ruleset entry")
    return rules[0]["parameters"]


def check_detail(detail: dict, c: dict) -> None:
    if (detail.get("id") != 17137629 or detail.get("name") != c["ruleset_name"]
            or detail.get("target") != "branch"
            or detail.get("enforcement") != "active"):
        raise ValueError("wrong or inactive Programme branch ruleset")
    contexts = [
        x["context"] for r in detail["rules"] if r["type"] == "required_status_checks"
        for x in r["parameters"]["required_status_checks"]
    ]
    if contexts != c["retained_check_contexts"]:
        raise ValueError("current Programme required checks drift")
    bypass = detail.get("bypass_actors")
    if bypass != [{"actor_id": 4423678, "actor_type": "Integration",
                   "bypass_mode": "pull_request"}]:
        raise ValueError("unexpected or expanded Programme bypass actors")


def check_merge_queue(detail: dict, c: dict) -> None:
    if (detail.get("id") != c["retained_merge_queue_ruleset_id"]
            or detail.get("enforcement") != "active"):
        raise ValueError("GH-OS merge queue identity/enforcement drift")
    required = [
        x["context"] for r in detail["rules"] if r["type"] == "required_status_checks"
        for x in r["parameters"]["required_status_checks"]
    ]
    if required != [c["retained_merge_queue_check"]]:
        raise ValueError("merge-queue required routing check changed")
    if len([r for r in detail["rules"] if r["type"] == "merge_queue"]) != 1:
        raise ValueError("GH-OS merge queue rule missing")


def projected(detail: dict) -> dict:
    result = {key: copy.deepcopy(detail[key]) for key in WRITABLE}
    if any(rule["type"] == "pull_request" for rule in result["rules"]):
        params = review_params(result)
        for key in ("required_approving_review_count", "require_last_push_approval"):
            params[key] = "<NARROW_REVIEW_MIGRATION>"
    return result


def migrate(client: GitHubClient, *, apply: bool) -> dict:
    c = load_contract()
    before = branch_ruleset(client, c["repository"])
    queue_before = client.request("GET", "/repos/grandchallenge/MATH-PROGRAMME/rulesets/21969152")
    check_detail(before, c)
    check_merge_queue(queue_before, c)
    before_state = {k: review_params(before)[k] for k in c["from"]}
    if before_state not in (c["from"], c["to"]):
        raise ValueError("live Programme review state is neither exact predecessor nor target")

    did_mutate = False
    if before_state == c["from"] and apply:
        candidate = {key: copy.deepcopy(before[key]) for key in WRITABLE}
        review_params(candidate).update(c["to"])
        client.request("PUT", "/repos/grandchallenge/MATH-PROGRAMME/rulesets/17137629", candidate)
        did_mutate = True

    after = branch_ruleset(client, c["repository"]) if apply else before
    queue_after = client.request("GET", "/repos/grandchallenge/MATH-PROGRAMME/rulesets/21969152")
    check_detail(after, c)
    check_merge_queue(queue_after, c)
    if projected(after) != projected(before):
        raise ValueError("outside-scope Programme ruleset mutation detected")
    if projected(queue_before) != projected(queue_after):
        raise ValueError("GH-OS merge queue changed during narrow review migration")
    if apply and {k: review_params(after)[k] for k in c["to"]} != c["to"]:
        raise ValueError("target review count or last-pusher readback failed")

    return {
        "record_type": "MP_ROUTINE_REVIEW_GATE_MIGRATION_RECEIPT",
        "programme_ruleset_id": 17137629,
        "ghos_queue_ruleset_id": 21969152,
        "before_review": before_state,
        "after_review": {k: review_params(after)[k] for k in c["to"]},
        "mutated": did_mutate,
        "protected_status_checks_preserved": True,
        "merge_queue_preserved": True,
        "other_writable_ruleset_fields_preserved": True,
        "specialist_certification_authority_changed": False,
        "live_verified": apply,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("validate", "apply", "verify"), required=True)
    parser.add_argument("--receipt", type=Path, default=Path("programme-review-gate-receipt.json"))
    args = parser.parse_args()
    load_contract()
    if args.mode == "validate":
        print("PASS: exact narrow review-gate contract")
    else:
        token = os.environ.get("GCL_REPOSITORY_ADMIN_TOKEN", "")
        if not token:
            raise SystemExit("missing short-lived delegated administration token")
        client = GitHubClient(token, "2022-11-28")
        result = migrate(client, apply=args.mode == "apply")
        args.receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
        print(json.dumps(result, sort_keys=True))
