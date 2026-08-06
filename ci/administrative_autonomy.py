from __future__ import annotations
import argparse, copy, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from autonomy_github import (
    AutonomyError, Client, approve, auto_merge, branch, delete_branch, identity,
    install_bypass, json_content, pull, put_json, readback, required_contexts,
    restore_ruleset, set_workflow_approval, verify_scope, wait_checks, wait_merge,
    workflow_permissions,
)

ROOT = Path(__file__).resolve().parents[1]
TRANSITION = ROOT / "governance/administrative_autonomy_transition.json"
REPORT = ROOT / "administrative-autonomy-activation-report.json"
ACTIVATION_PATH = "governance/administrative_autonomy_activation.json"

def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def sha(value: Any) -> bool:
    text = str(value)
    return len(text) == 40 and all(x in "0123456789abcdef" for x in text)

def positive_int(value: str, label: str) -> int:
    try:
        result = int(value)
    except ValueError as exc:
        raise AutonomyError(f"{label} is not an integer") from exc
    if result <= 0:
        raise AutonomyError(f"{label} must be positive")
    return result

def validate_transition(value: dict[str, Any]) -> list[str]:
    errors = []
    expected = {
        "schema_version": "1.0.0", "transition_id": "MP-ADMIN-AUTONOMY-TRANSITION-001",
        "control_id": "MP-ADMIN-MAINT-001", "predecessor_automation_id": "MP-ADMIN-AUTOMATION-CLOSURE-001",
        "repository": "grandchallenge/MATH-PROGRAMME", "status": "ARMED_NOT_ACTIVE",
    }
    for key, item in expected.items():
        if value.get(key) != item: errors.append(f"{key} drift")
    closeout = value.get("previous_policy_closeout", {})
    if closeout.get("pull_request") != 247: errors.append("PR #247 closeout missing")
    if not sha(closeout.get("reviewed_head")) or not sha(closeout.get("merge_commit")):
        errors.append("previous policy receipt SHA invalid")
    if closeout.get("automated_authority_used") is not False:
        errors.append("PR #247 must remain a previous-policy merge")
    agents = value.get("agents", {})
    if not all(name in agents for name in ("candidate", "administrator", "referee")):
        errors.append("candidate, administrator, and referee offices must be explicit")
    if agents.get("candidate", {}).get("expected_login") == agents.get("referee", {}).get("expected_login"):
        errors.append("candidate and referee identities are not distinct")
    if agents.get("administrator", {}).get("expected_login") != agents.get("candidate", {}).get("expected_login"):
        errors.append("administrator must be a separately scoped Release Trust token")
    if agents.get("identity_separation_required") is not True:
        errors.append("identity separation must be required")
    authority = value.get("delegated_authority", {})
    if authority.get("automated_human_steward_disposition") is not False:
        errors.append("automation may not impersonate the Human Steward")
    for key in ("automated_exact_head_approval", "automated_referee_disposition", "automated_merge", "automated_auto_merge"):
        if authority.get(key) is not True: errors.append(f"delegated authority {key} must be explicit")
    bypass = authority.get("branch_protection_bypass", {})
    if bypass.get("mode") != "pull_request" or bypass.get("direct_push") is not False:
        errors.append("bypass must be pull-request-only")
    anchor = authority.get("cadence_anchor_reset", {})
    if anchor.get("mode") != "append_only_transaction" or anchor.get("silent_rewrite") is not False:
        errors.append("cadence anchor reset must be append-only")
    if ACTIVATION_PATH not in value.get("scope", {}).get("allowed_paths", []):
        errors.append("activation record path is not in delegated scope")
    boundaries = value.get("claim_boundaries", {})
    if not boundaries or any(x is not False for x in boundaries.values()):
        errors.append("claim boundaries must remain false")
    return errors

def activation_record(t: dict[str, Any], head: str, candidate: Any, administrator: Any, referee: Any, ruleset: int, prior: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "../schemas/administrative_autonomy_activation.schema.json",
        "schema_version": "1.0.0", "activation_id": "MP-ADMIN-AUTONOMY-ACTIVATION-001",
        "transition_id": t["transition_id"], "repository": t["repository"], "state": "ACTIVE",
        "transition_merge_head": head, "activated_at": now(),
        "candidate_identity": candidate.record(), "administrator_identity": administrator.record(),
        "referee_identity": referee.record(),
        "identity_separation": candidate.app_id != referee.app_id and candidate.login != referee.login,
        "actions_approval": {
            "enabled": True,
            "prior_default_workflow_permissions": prior["default_workflow_permissions"],
            "prior_can_approve_pull_request_reviews": prior["can_approve_pull_request_reviews"],
        },
        "auto_merge": {"repository_enabled": True, "method": "merge", "exact_head_required": True, "armed_before_check_completion": True},
        "ruleset_bypass": {
            "ruleset_id": ruleset, "actor_id": referee.app_id, "actor_type": "Integration",
            "mode": "pull_request", "direct_push": False,
        },
        "canary": {
            "branch": f"automation/administrative-autonomy-activation-{head[:12]}",
            "changed_paths": [ACTIVATION_PATH], "required_checks_source": f"live ruleset {ruleset}",
            "protected_merge_required": True, "post_merge_readback_required": True,
        },
        "authority_boundary": {
            "automated_exact_head_approval": True, "automated_referee_disposition": True,
            "automated_human_steward_disposition": False, "automated_merge": True,
            "automated_auto_merge": True, "branch_protection_bypass": "REFEREE_AGENT_PULL_REQUEST_ONLY",
            "direct_protected_push": False,
        },
        "rollback": {
            "automatic_activation_failure_reversion": True, "ruleset_prior_state_captured": True,
            "actions_prior_state_captured": True, "unmerged_branch_deletion": True,
            "failure_artifact_required": True,
        },
        "claim_boundaries": copy.deepcopy(t["claim_boundaries"]),
    }

def activate(check_timeout: int, merge_timeout: int) -> int:
    t = json.loads(TRANSITION.read_text())
    errors = validate_transition(t)
    if errors: raise AutonomyError("; ".join(errors))
    repo, head = os.getenv("GITHUB_REPOSITORY", ""), os.getenv("GITHUB_SHA", "")
    if repo != t["repository"] or not sha(head) or os.getenv("GITHUB_REF") != "refs/heads/main":
        raise AutonomyError("activation must execute from protected main")
    candidate, referee, admin = (
        Client(os.getenv("CANDIDATE_TOKEN", "")),
        Client(os.getenv("REFEREE_TOKEN", "")),
        Client(os.getenv("ADMIN_TOKEN", "")),
    )
    candidate_app_id = positive_int(os.getenv("CANDIDATE_APP_ID", ""), "CANDIDATE_APP_ID")
    referee_app_id = positive_int(os.getenv("REFEREE_APP_ID", ""), "REFEREE_APP_ID")
    ci = identity(candidate, candidate_app_id, "candidate")
    ai = identity(admin, candidate_app_id, "administrator")
    ri = identity(referee, referee_app_id, "referee")
    expected = t["agents"]
    if ci.login != expected["candidate"]["expected_login"] or ai.login != expected["administrator"]["expected_login"] or ri.login != expected["referee"]["expected_login"]:
        raise AutonomyError(f"agent identity drift: {ci.login}; {ai.login}; {ri.login}")
    if ci.app_id == ri.app_id or ci.login == ri.login:
        raise AutonomyError("Candidate and Referee identities are not independent")
    existing = json_content(referee, repo, ACTIVATION_PATH, "main")
    if existing and existing.get("state") == "ACTIVE" and existing.get("transition_id") == t["transition_id"]:
        report = {"schema_version": "1.0.0", "state": "ACTIVE_ALREADY_PROTECTED", "observed_at": now(), "activation_record": existing}
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
        return 0
    if admin.get(f"/repos/{repo}").get("allow_auto_merge") is not True:
        raise AutonomyError("repository auto-merge is disabled")
    ruleset_id = int(os.getenv("AUTONOMY_RULESET_ID", "17137629"))
    prior = workflow_permissions(admin, repo)
    before_ruleset, actions_changed, rules_changed, pr, merged = None, False, False, None, None
    branch_name = ""
    report = {"schema_version": "1.0.0", "state": "ACTIVATION_STARTED", "transition_head": head, "started_at": now()}
    try:
        set_workflow_approval(admin, repo, prior, True)
        after_permissions = workflow_permissions(admin, repo)
        if after_permissions.get("can_approve_pull_request_reviews") is not True:
            raise AutonomyError("Actions approval permission readback failed")
        actions_changed = after_permissions != prior
        before_ruleset, live_ruleset = install_bypass(admin, repo, ruleset_id, ri)
        rules_changed = live_ruleset.get("bypass_actors") != before_ruleset.get("bypass_actors")
        record = activation_record(t, head, ci, ai, ri, ruleset_id, prior)
        branch_name = record["canary"]["branch"]
        branch(candidate, repo, branch_name, head)
        canary_head = put_json(candidate, repo, branch_name, ACTIVATION_PATH, record)
        pr = pull(candidate, repo, branch_name, head)
        pr = candidate.get(f"/repos/{repo}/pulls/{pr['number']}")
        if pr["head"]["sha"] != canary_head or pr["user"]["login"] != ci.login:
            raise AutonomyError("Candidate Agent canary identity or head mismatch")
        verify_scope(candidate, repo, pr, ACTIVATION_PATH)
        auto_merge(referee, pr["node_id"], canary_head)
        checks = wait_checks(referee, repo, canary_head, required_contexts(live_ruleset), check_timeout)
        review = approve(referee, repo, pr["number"], canary_head)
        merged = wait_merge(referee, repo, pr["number"], canary_head, merge_timeout)
        readback(referee, repo, ACTIVATION_PATH, record, timeout=300)
        comment = referee.post(f"/repos/{repo}/issues/{pr['number']}/comments", {"body": (
            "REFEREE_AGENT_PROTECTED_READBACK_COMPLETE\n\n"
            f"- exact reviewed head: `{canary_head}`;\n- review ID: `{review['id']}`;\n"
            f"- protected merge commit: `{merged['merge_commit_sha']}`;\n- live ruleset ID: `{ruleset_id}`;\n"
            "- bypass: Referee Agent integration, `pull_request` only;\n"
            "- protected activation state: `ACTIVE`;\n- Human Steward impersonation: prohibited and not used."
        )})
        report |= {
            "state": "ACTIVE_PROTECTED_READBACK_COMPLETE", "completed_at": now(),
            "canary_pull_request": pr["number"], "canary_head": canary_head, "checks": checks,
            "review_id": review["id"], "merge_commit": merged["merge_commit_sha"],
            "readback_comment_id": comment["id"], "ruleset_id": ruleset_id,
        }
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))
        return 0
    except Exception as exc:
        rollback = []
        if merged is None:
            if pr and not pr.get("merged"):
                try: candidate.patch(f"/repos/{repo}/pulls/{pr['number']}", {"state": "closed"})
                except Exception as item: rollback.append(f"close PR: {item}")
            if branch_name:
                try: delete_branch(candidate, repo, branch_name)
                except Exception as item: rollback.append(f"delete branch: {item}")
            if before_ruleset is not None and rules_changed:
                try: restore_ruleset(admin, repo, ruleset_id, before_ruleset)
                except Exception as item: rollback.append(f"restore ruleset: {item}")
            if actions_changed:
                try: set_workflow_approval(admin, repo, prior, prior["can_approve_pull_request_reviews"])
                except Exception as item: rollback.append(f"restore Actions permission: {item}")
            state, authority_created = "ACTIVATION_FAILED_CLOSED", False
        else:
            state, authority_created = "ACTIVATION_MERGED_READBACK_INCOMPLETE", True
        report |= {"state": state, "failed_at": now(), "error": str(exc), "rollback_errors": rollback, "authority_created": authority_created}
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
        raise

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("validate", "activate"))
    parser.add_argument("--check-timeout-seconds", type=int, default=3300)
    parser.add_argument("--merge-timeout-seconds", type=int, default=900)
    args = parser.parse_args(argv)
    value = json.loads(TRANSITION.read_text())
    errors = validate_transition(value)
    if args.command == "validate":
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("administrative autonomy transition valid")
        return 0
    return activate(args.check_timeout_seconds, args.merge_timeout_seconds)

if __name__ == "__main__":
    raise SystemExit(main())
