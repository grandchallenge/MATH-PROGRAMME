from __future__ import annotations

import argparse
import copy
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from autonomy_github import (
    AutonomyError,
    Client,
    auto_merge,
    branch,
    delete_branch,
    identity,
    install_bypass,
    json_content,
    pull,
    put_json,
    readback,
    record_disposition,
    required_contexts,
    restore_ruleset,
    verify_scope,
    wait_checks,
    wait_merge,
)

ROOT = Path(__file__).resolve().parents[1]
TRANSITION = ROOT / "governance/administrative_autonomy_transition.json"
REPORT = ROOT / "administrative-autonomy-activation-report.json"
ACTIVATION_PATH = "governance/administrative_autonomy_activation.json"


def now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def sha(value: Any) -> bool:
    text = str(value)
    return len(text) == 40 and all(
        character in "0123456789abcdef" for character in text
    )


def positive_int(value: str, label: str) -> int:
    try:
        result = int(value)
    except ValueError as exc:
        raise AutonomyError(f"{label} is not an integer") from exc
    if result <= 0:
        raise AutonomyError(f"{label} must be positive")
    return result


def validate_transition(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema_version": "1.0.0",
        "transition_id": "MP-ADMIN-AUTONOMY-TRANSITION-001",
        "control_id": "MP-ADMIN-MAINT-001",
        "predecessor_automation_id": "MP-ADMIN-AUTOMATION-CLOSURE-001",
        "repository": "grandchallenge/MATH-PROGRAMME",
        "status": "ARMED_NOT_ACTIVE",
    }
    for key, item in expected.items():
        if value.get(key) != item:
            errors.append(f"{key} drift")

    closeout = value.get("previous_policy_closeout", {})
    if closeout.get("pull_request") != 247:
        errors.append("PR #247 closeout missing")
    if not sha(closeout.get("reviewed_head")) or not sha(
        closeout.get("merge_commit")
    ):
        errors.append("previous policy receipt SHA invalid")
    if closeout.get("automated_authority_used") is not False:
        errors.append("PR #247 must remain a previous-policy merge")

    attempts = value.get("activation_attempts", [])
    expected_attempts = (
        (31070450361, 8955429470),
        (31071759797, 8955883591),
    )
    if len(attempts) < len(expected_attempts):
        errors.append("activation failure history is incomplete")
    else:
        for index, (run_id, artifact_id) in enumerate(expected_attempts):
            attempt = attempts[index]
            if (
                attempt.get("state") != "ACTIVATION_FAILED_CLOSED"
                or attempt.get("authority_created") is not False
                or attempt.get("workflow_run_id") != run_id
                or attempt.get("artifact_id") != artifact_id
                or attempt.get("canary_created") is not False
                or attempt.get("ruleset_bypass_actors_after_failure") != []
            ):
                errors.append(
                    f"activation failure receipt {index + 1} drift"
                )

    agents = value.get("agents", {})
    if not all(
        name in agents
        for name in ("candidate", "administrator", "referee")
    ):
        errors.append(
            "candidate, administrator, and referee offices must be explicit"
        )
    if agents.get("candidate", {}).get("expected_login") == agents.get(
        "referee", {}
    ).get("expected_login"):
        errors.append("candidate and referee identities are not distinct")
    if agents.get("administrator", {}).get(
        "expected_login"
    ) != agents.get("candidate", {}).get("expected_login"):
        errors.append(
            "administrator must be a separately scoped Release Trust token"
        )
    if agents.get("identity_separation_required") is not True:
        errors.append("identity separation must be required")

    authority = value.get("delegated_authority", {})
    if authority.get("automated_human_steward_disposition") is not False:
        errors.append("automation may not impersonate the Human Steward")
    for key in (
        "automated_exact_head_approval",
        "automated_referee_disposition",
        "automated_merge",
        "automated_auto_merge",
    ):
        if authority.get(key) is not True:
            errors.append(f"delegated authority {key} must be explicit")

    approval_record = authority.get("approval_record", {})
    if (
        approval_record.get("mode") != "issue_comment"
        or approval_record.get("github_review_submission_required") is not False
        or approval_record.get(
            "organization_actions_approval_setting_required"
        )
        is not False
        or approval_record.get(
            "required_checks_must_precede_disposition"
        )
        is not True
    ):
        errors.append(
            "Referee approval must use a post-check exact-head issue comment"
        )

    bypass = authority.get("branch_protection_bypass", {})
    if (
        bypass.get("actor")
        != "GCL Release Trust Administration Agent GitHub App identity"
        or bypass.get("mode") != "pull_request"
        or bypass.get("direct_push") is not False
        or bypass.get("candidate_referee_separation_preserved") is not True
        or bypass.get("canary_merge_uses_bypass") is not False
    ):
        errors.append(
            "bypass must use the organization-installed Administration Agent without the canary exercising bypass"
        )

    anchor = authority.get("cadence_anchor_reset", {})
    if (
        anchor.get("mode") != "append_only_transaction"
        or anchor.get("silent_rewrite") is not False
    ):
        errors.append("cadence anchor reset must be append-only")

    if ACTIVATION_PATH not in value.get("scope", {}).get(
        "allowed_paths", []
    ):
        errors.append("activation record path is not in delegated scope")

    boundaries = value.get("claim_boundaries", {})
    if not boundaries or any(
        item is not False for item in boundaries.values()
    ):
        errors.append("claim boundaries must remain false")
    return errors


def activation_record(
    transition: dict[str, Any],
    head: str,
    candidate: Any,
    administrator: Any,
    referee: Any,
    ruleset_id: int,
) -> dict[str, Any]:
    return {
        "$schema": "../schemas/administrative_autonomy_activation.schema.json",
        "schema_version": "1.0.0",
        "activation_id": "MP-ADMIN-AUTONOMY-ACTIVATION-001",
        "transition_id": transition["transition_id"],
        "repository": transition["repository"],
        "state": "ACTIVE",
        "transition_merge_head": head,
        "activated_at": now(),
        "candidate_identity": candidate.record(),
        "administrator_identity": administrator.record(),
        "referee_identity": referee.record(),
        "identity_separation": (
            candidate.app_id != referee.app_id
            and candidate.login != referee.login
        ),
        "referee_disposition": {
            "mode": "issue_comment",
            "actor_login": referee.login,
            "github_review_submission_required": False,
            "organization_actions_approval_setting_required": False,
            "exact_head_required": True,
            "required_checks_must_precede_disposition": True,
            "recorded_before_auto_merge": True,
        },
        "auto_merge": {
            "repository_enabled": True,
            "method": "merge",
            "exact_head_required": True,
            "armed_after_required_checks": True,
            "armed_after_referee_disposition": True,
        },
        "ruleset_bypass": {
            "ruleset_id": ruleset_id,
            "actor_id": administrator.app_id,
            "actor_login": administrator.login,
            "actor_role": "Administration Agent",
            "actor_type": "Integration",
            "mode": "pull_request",
            "direct_push": False,
            "canary_merge_uses_bypass": False,
        },
        "canary": {
            "branch": (
                "automation/administrative-autonomy-activation-"
                f"{head[:12]}"
            ),
            "changed_paths": [ACTIVATION_PATH],
            "required_checks_source": f"live ruleset {ruleset_id}",
            "protected_merge_required": True,
            "post_merge_readback_required": True,
        },
        "authority_boundary": {
            "automated_exact_head_approval": True,
            "automated_referee_disposition": True,
            "automated_human_steward_disposition": False,
            "automated_merge": True,
            "automated_auto_merge": True,
            "branch_protection_bypass": (
                "RELEASE_TRUST_ADMINISTRATION_AGENT_PULL_REQUEST_ONLY"
            ),
            "direct_protected_push": False,
        },
        "rollback": {
            "automatic_activation_failure_reversion": True,
            "ruleset_prior_state_captured": True,
            "unmerged_branch_deletion": True,
            "failure_artifact_required": True,
        },
        "claim_boundaries": copy.deepcopy(
            transition["claim_boundaries"]
        ),
    }


def activate(check_timeout: int, merge_timeout: int) -> int:
    transition = json.loads(TRANSITION.read_text(encoding="utf-8"))
    errors = validate_transition(transition)
    if errors:
        raise AutonomyError("; ".join(errors))

    repo = os.getenv("GITHUB_REPOSITORY", "")
    head = os.getenv("GITHUB_SHA", "")
    if (
        repo != transition["repository"]
        or not sha(head)
        or os.getenv("GITHUB_REF") != "refs/heads/main"
    ):
        raise AutonomyError(
            "activation must execute from protected main"
        )

    candidate = Client(os.getenv("CANDIDATE_TOKEN", ""))
    referee = Client(os.getenv("REFEREE_TOKEN", ""))
    admin = Client(os.getenv("ADMIN_TOKEN", ""))

    candidate_app_id = positive_int(
        os.getenv("CANDIDATE_APP_ID", ""),
        "CANDIDATE_APP_ID",
    )
    referee_app_id = positive_int(
        os.getenv("REFEREE_APP_ID", ""),
        "REFEREE_APP_ID",
    )
    candidate_identity = identity(
        os.getenv("CANDIDATE_LOGIN", ""),
        candidate_app_id,
        "candidate",
    )
    administrator_identity = identity(
        os.getenv("ADMIN_LOGIN", ""),
        candidate_app_id,
        "administrator",
    )
    referee_identity = identity(
        os.getenv("REFEREE_LOGIN", ""),
        referee_app_id,
        "referee",
    )

    expected = transition["agents"]
    if (
        candidate_identity.login
        != expected["candidate"]["expected_login"]
        or administrator_identity.login
        != expected["administrator"]["expected_login"]
        or referee_identity.login
        != expected["referee"]["expected_login"]
    ):
        raise AutonomyError(
            "agent identity drift: "
            f"{candidate_identity.login}; "
            f"{administrator_identity.login}; "
            f"{referee_identity.login}"
        )
    if (
        candidate_identity.app_id == referee_identity.app_id
        or candidate_identity.login == referee_identity.login
    ):
        raise AutonomyError(
            "Candidate and Referee identities are not independent"
        )

    existing = json_content(
        referee,
        repo,
        ACTIVATION_PATH,
        "main",
    )
    if (
        existing
        and existing.get("state") == "ACTIVE"
        and existing.get("transition_id")
        == transition["transition_id"]
    ):
        report = {
            "schema_version": "1.0.0",
            "state": "ACTIVE_ALREADY_PROTECTED",
            "observed_at": now(),
            "activation_record": existing,
        }
        REPORT.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(report, indent=2))
        return 0

    if admin.get(f"/repos/{repo}").get("allow_auto_merge") is not True:
        raise AutonomyError("repository auto-merge is disabled")

    ruleset_id = int(
        os.getenv("AUTONOMY_RULESET_ID", "17137629")
    )
    before_ruleset: dict[str, Any] | None = None
    rules_changed = False
    pr: dict[str, Any] | None = None
    merged: dict[str, Any] | None = None
    branch_name = ""
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "state": "ACTIVATION_STARTED",
        "transition_head": head,
        "started_at": now(),
    }

    try:
        before_ruleset, live_ruleset = install_bypass(
            admin,
            repo,
            ruleset_id,
            administrator_identity,
        )
        rules_changed = (
            live_ruleset.get("bypass_actors")
            != before_ruleset.get("bypass_actors")
        )

        record = activation_record(
            transition,
            head,
            candidate_identity,
            administrator_identity,
            referee_identity,
            ruleset_id,
        )
        branch_name = record["canary"]["branch"]
        branch(candidate, repo, branch_name, head)
        canary_head = put_json(
            candidate,
            repo,
            branch_name,
            ACTIVATION_PATH,
            record,
        )

        pr = pull(candidate, repo, branch_name, head)
        pr = candidate.get(
            f"/repos/{repo}/pulls/{pr['number']}"
        )
        if (
            pr["head"]["sha"] != canary_head
            or pr["user"]["login"] != candidate_identity.login
        ):
            raise AutonomyError(
                "Candidate Agent canary identity or head mismatch"
            )
        verify_scope(candidate, repo, pr, ACTIVATION_PATH)

        checks = wait_checks(
            referee,
            repo,
            canary_head,
            required_contexts(live_ruleset),
            check_timeout,
        )
        disposition = record_disposition(
            referee,
            repo,
            pr["number"],
            canary_head,
            referee_identity,
            checks,
        )
        auto_merge(
            referee,
            pr["node_id"],
            canary_head,
            referee_identity,
        )
        merged = wait_merge(
            referee,
            repo,
            pr["number"],
            canary_head,
            merge_timeout,
        )
        readback(
            referee,
            repo,
            ACTIVATION_PATH,
            record,
            timeout=300,
        )

        comment = referee.post(
            f"/repos/{repo}/issues/{pr['number']}/comments",
            {
                "body": (
                    "REFEREE_AGENT_PROTECTED_READBACK_COMPLETE\n\n"
                    f"- exact approved head: `{canary_head}`;\n"
                    f"- approval disposition comment ID: "
                    f"`{disposition['id']}`;\n"
                    f"- protected merge commit: "
                    f"`{merged['merge_commit_sha']}`;\n"
                    f"- live ruleset ID: `{ruleset_id}`;\n"
                    "- bypass actor: GCL Release Trust Administration "
                    "Agent integration, `pull_request` only;\n"
                    "- canary merge used bypass: `false`;\n"
                    "- protected activation state: `ACTIVE`;\n"
                    "- GitHub approving review used: `false`;\n"
                    "- Human Steward impersonation: prohibited "
                    "and not used."
                )
            },
        )
        if (
            comment.get("user", {}).get("login")
            != referee_identity.login
        ):
            raise AutonomyError(
                "protected readback comment actor mismatch"
            )

        report |= {
            "state": "ACTIVE_PROTECTED_READBACK_COMPLETE",
            "completed_at": now(),
            "canary_pull_request": pr["number"],
            "canary_head": canary_head,
            "checks": checks,
            "disposition_comment_id": disposition["id"],
            "merge_commit": merged["merge_commit_sha"],
            "readback_comment_id": comment["id"],
            "ruleset_id": ruleset_id,
            "bypass_actor_id": administrator_identity.app_id,
            "canary_merge_used_bypass": False,
        }
        REPORT.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(report, indent=2))
        return 0

    except Exception as exc:
        rollback_errors: list[str] = []
        if merged is None:
            if pr and not pr.get("merged"):
                try:
                    candidate.patch(
                        f"/repos/{repo}/pulls/{pr['number']}",
                        {"state": "closed"},
                    )
                except Exception as item:
                    rollback_errors.append(f"close PR: {item}")
            if branch_name:
                try:
                    delete_branch(
                        candidate,
                        repo,
                        branch_name,
                    )
                except Exception as item:
                    rollback_errors.append(
                        f"delete branch: {item}"
                    )
            if before_ruleset is not None and rules_changed:
                try:
                    restore_ruleset(
                        admin,
                        repo,
                        ruleset_id,
                        before_ruleset,
                    )
                except Exception as item:
                    rollback_errors.append(
                        f"restore ruleset: {item}"
                    )
            state = "ACTIVATION_FAILED_CLOSED"
            authority_created = False
        else:
            state = "ACTIVATION_MERGED_READBACK_INCOMPLETE"
            authority_created = True

        report |= {
            "state": state,
            "failed_at": now(),
            "error": str(exc),
            "rollback_errors": rollback_errors,
            "authority_created": authority_created,
        }
        REPORT.write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=("validate", "activate"),
    )
    parser.add_argument(
        "--check-timeout-seconds",
        type=int,
        default=3300,
    )
    parser.add_argument(
        "--merge-timeout-seconds",
        type=int,
        default=900,
    )
    args = parser.parse_args(argv)

    value = json.loads(TRANSITION.read_text(encoding="utf-8"))
    errors = validate_transition(value)
    if args.command == "validate":
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("administrative autonomy transition valid")
        return 0
    return activate(
        args.check_timeout_seconds,
        args.merge_timeout_seconds,
    )


if __name__ == "__main__":
    raise SystemExit(main())
