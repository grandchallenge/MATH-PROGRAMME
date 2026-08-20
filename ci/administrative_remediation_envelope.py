#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Mapping

from autonomy_github import (
    AutonomyError,
    Client,
    auto_merge,
    identity,
    install_bypass,
    record_disposition,
    required_contexts,
    wait_checks,
    wait_merge,
)

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
EXPECTED_HUMAN_STEWARD_LOGIN = "fyremael"
EXPECTED_REFEREE_LOGIN = "github-actions[bot]"
EXPECTED_REFEREE_APP_ID = 15368
EXPECTED_REMEDIATION_BRANCH_PREFIX = "remediation/mp-admin-"
EXPECTED_BASE_BRANCH = "main"
APPROVAL_PREFIX = "HUMAN STEWARD INITIAL APPROVAL — DELEGATED REMEDIATION ENVELOPE"
APPROVAL_FINAL_BOUNDARY = "Final administrative-review reactivation/incident closure remains reserved to the Human Steward."


def sha256_json(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def run_identity() -> dict[str, str]:
    return {
        "github_run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
        "github_sha": os.environ.get("GITHUB_SHA", ""),
        "github_workflow_ref": os.environ.get("GITHUB_WORKFLOW_REF", ""),
    }


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
    expected_target = {
        "ruleset_id": EXPECTED_RULESET_ID,
        "actor_id": EXPECTED_ACTOR_ID,
        "actor_login": EXPECTED_ACTOR_LOGIN,
        "actor_type": EXPECTED_ACTOR_TYPE,
        "bypass_mode": EXPECTED_BYPASS_MODE,
        "direct_protected_push": False,
        "bypass_exercise_authorized": False,
    }
    for key, expected_value in expected_target.items():
        if target.get(key) != expected_value:
            raise AutonomyError(f"remediation target drift: {key}")

    review = value.get("delegated_review", {})
    expected_review = {
        "referee_login": EXPECTED_REFEREE_LOGIN,
        "referee_app_id": EXPECTED_REFEREE_APP_ID,
        "mode": "issue_comment",
        "github_review_submission_required": False,
        "required_checks_source": "live_ruleset_17137629",
        "exact_head_required": True,
        "expected_head_auto_merge_required": True,
        "post_merge_readback_required": True,
    }
    for key, expected_value in expected_review.items():
        if review.get(key) != expected_value:
            raise AutonomyError(f"delegated review drift: {key}")

    delegated = value.get("delegated_authority", {})
    for key in (
        "diagnose",
        "bounded_control_plane_repair",
        "repair_pull_requests",
        "exact_head_validation",
        "independent_non_author_review",
        "referee_agent_exact_head_disposition",
        "expected_head_protected_merge_after_review",
        "referee_expected_head_auto_merge",
        "automatic_resume_after_merged_remediation_pr",
        "exact_ruleset_actor_reconciliation",
        "qualification_replay",
        "repeat_until_green_or_scope_expansion",
    ):
        if delegated.get(key) is not True:
            raise AutonomyError(f"delegated remediation authority missing: {key}")
    return value


def path_allowed(path: str, envelope: Mapping[str, Any]) -> bool:
    if path in set(envelope.get("allowed_exact_paths", []) or []):
        return True
    return any(
        path.startswith(str(prefix))
        for prefix in envelope.get("allowed_path_prefixes", []) or []
    )


def require_live_initial_approval(referee: Client) -> dict[str, Any]:
    comment = referee.get(
        f"/repos/{EXPECTED_REPOSITORY}/issues/comments/{EXPECTED_AUTHORIZATION_COMMENT_ID}"
    )
    if comment.get("user", {}).get("login") != EXPECTED_HUMAN_STEWARD_LOGIN:
        raise AutonomyError("initial Human Steward approval actor drift")
    body = str(comment.get("body") or "")
    if not body.startswith(APPROVAL_PREFIX):
        raise AutonomyError("initial Human Steward approval marker drift")
    if APPROVAL_FINAL_BOUNDARY not in body:
        raise AutonomyError("final Human Steward boundary is not retained")
    return comment


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


def admit_pull_request(
    referee_token: str,
    admin_read_token: str,
    pr_number: int,
    expected_head: str,
    report_path: Path,
) -> dict[str, Any]:
    envelope = load_envelope()
    referee = Client(referee_token)
    administrator = Client(admin_read_token)
    referee_identity = identity(
        EXPECTED_REFEREE_LOGIN,
        EXPECTED_REFEREE_APP_ID,
        "delegated-remediation-referee",
    )
    approval = require_live_initial_approval(referee)

    pull = referee.get(f"/repos/{EXPECTED_REPOSITORY}/pulls/{pr_number}")
    if pull.get("state") != "open":
        raise AutonomyError("remediation pull request is not open")
    if pull.get("draft") is True:
        raise AutonomyError("remediation pull request is still draft")
    if pull.get("base", {}).get("ref") != EXPECTED_BASE_BRANCH:
        raise AutonomyError("remediation pull request base drift")
    if pull.get("head", {}).get("sha") != expected_head:
        raise AutonomyError("remediation exact head changed before admission")
    branch = str(pull.get("head", {}).get("ref") or "")
    if not branch.startswith(EXPECTED_REMEDIATION_BRANCH_PREFIX):
        raise AutonomyError("remediation branch namespace drift")

    files = referee.get(
        f"/repos/{EXPECTED_REPOSITORY}/pulls/{pr_number}/files?per_page=100"
    )
    if not isinstance(files, list) or not files:
        raise AutonomyError("remediation pull request has no changed files")
    if len(files) >= 100:
        raise AutonomyError("remediation changed-file set exceeds bounded inspection page")
    changed_paths = [str(item.get("filename") or "") for item in files]
    forbidden = [path for path in changed_paths if not path_allowed(path, envelope)]
    if forbidden:
        raise AutonomyError(f"remediation path scope drift: {forbidden}")

    live_ruleset = administrator.get(
        f"/repos/{EXPECTED_REPOSITORY}/rulesets/{EXPECTED_RULESET_ID}"
    )
    if int(live_ruleset.get("id") or EXPECTED_RULESET_ID) != EXPECTED_RULESET_ID:
        raise AutonomyError("live ruleset identity drift")
    contexts = required_contexts(live_ruleset)
    checks = wait_checks(
        referee,
        EXPECTED_REPOSITORY,
        expected_head,
        contexts,
        1800,
    )

    disposition = record_disposition(
        referee,
        EXPECTED_REPOSITORY,
        pr_number,
        expected_head,
        referee_identity,
        checks,
    )
    auto_merge(
        referee,
        str(pull.get("node_id") or ""),
        expected_head,
        referee_identity,
    )
    merged = wait_merge(
        referee,
        EXPECTED_REPOSITORY,
        pr_number,
        expected_head,
        600,
    )
    if merged.get("merged") is not True:
        raise AutonomyError("remediation expected-head auto-merge did not complete")
    if merged.get("head", {}).get("sha") != expected_head:
        raise AutonomyError("remediation merged head readback mismatch")

    report = {
        "schema_version": "1.0.0",
        "state": "REMEDIATION_PR_PROTECTED_MERGE_COMPLETE",
        "envelope_id": EXPECTED_ENVELOPE_ID,
        "control_issue": EXPECTED_ISSUE,
        "initial_human_steward_approval_comment_id": int(approval["id"]),
        "human_steward_identity_asserted_by_runtime": False,
        "pull_request": pr_number,
        "branch": branch,
        "exact_head": expected_head,
        "changed_paths": changed_paths,
        "required_checks": checks,
        "referee_actor": EXPECTED_REFEREE_LOGIN,
        "referee_disposition_comment_id": int(disposition["id"]),
        "github_review_submission_required": False,
        "expected_head_auto_merge_enabled": True,
        "merge_commit_sha": str(merged.get("merge_commit_sha") or ""),
        "direct_protected_push": False,
        "bypass_exercised": False,
        "receipt_mutation_performed": False,
        "ledger_mutation_performed": False,
        "mirror_mutation_performed": False,
        "reactivation_authorized": False,
        "run_identity": run_identity(),
    }
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return report


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
        "run_identity": run_identity(),
    }
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    return report


def write_failure_report(command: str, path: Path | None, exc: Exception) -> None:
    if path is None:
        return
    value = {
        "schema_version": "1.0.0",
        "state": "REMEDIATION_ENVELOPE_FAILED_CLOSED",
        "command": command,
        "error_type": type(exc).__name__,
        "error": str(exc),
        "authority_created": False,
        "human_steward_identity_asserted_by_runtime": False,
        "direct_protected_push": False,
        "bypass_exercised": False,
        "reactivation_authorized": False,
        "run_identity": run_identity(),
    }
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")

    admit = sub.add_parser("admit-pull-request")
    admit.add_argument("--pr", type=int, required=True)
    admit.add_argument("--head", required=True)
    admit.add_argument("--report", type=Path, required=True)

    reconcile = sub.add_parser("reconcile-actor")
    reconcile.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv)

    if args.command == "validate":
        value = load_envelope()
        print(
            json.dumps(
                {"state": "REMEDIATION_ENVELOPE_VALID", "envelope_id": value["envelope_id"]},
                sort_keys=True,
            )
        )
        return 0

    if args.command == "admit-pull-request":
        referee_token = os.environ.get("REFEREE_TOKEN", "")
        admin_read_token = os.environ.get("ADMIN_READ_TOKEN", "")
        if not referee_token or not admin_read_token:
            raise AutonomyError("REFEREE_TOKEN and ADMIN_READ_TOKEN are required")
        admit_pull_request(
            referee_token,
            admin_read_token,
            args.pr,
            args.head,
            args.report,
        )
        return 0

    token = os.environ.get("ADMIN_WRITE_TOKEN", "")
    if not token:
        raise AutonomyError("ADMIN_WRITE_TOKEN is required")
    reconcile_actor(token, args.report)
    return 0


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    report_path: Path | None = None
    if "--report" in sys.argv:
        try:
            report_path = Path(sys.argv[sys.argv.index("--report") + 1])
        except (ValueError, IndexError):
            report_path = None
    try:
        raise SystemExit(main())
    except Exception as exc:
        write_failure_report(command, report_path, exc)
        print(
            f"REMEDIATION_ENVELOPE_FAILED_CLOSED__{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise
