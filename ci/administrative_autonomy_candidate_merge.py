from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import administrative_autonomy as base
from autonomy_github import AutonomyError, Client, identity


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "governance/administrative_autonomy_merge_executor_correction.json"
STABILIZATION = ROOT / "governance/administrative_autonomy_stabilization_correction.json"
ROUTING = ROOT / "governance/routine_reviewer_routing.json"


def validate_correction(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema_version": "1.0.0",
        "correction_id": "MP-ADMIN-AUTONOMY-MERGE-EXECUTOR-CORRECTIVE-001",
        "transition_id": "MP-ADMIN-AUTONOMY-TRANSITION-001",
        "repository": "grandchallenge/MATH-PROGRAMME",
        "status": "ARMED_NOT_ACTIVE",
    }
    for key, item in expected.items():
        if value.get(key) != item:
            errors.append(f"{key} drift")

    attempt = value.get("activation_attempt_003", {})
    if (
        attempt.get("workflow_run_id") != 31072643002
        or attempt.get("artifact_id") != 8956258495
        or attempt.get("canary_pull_request") != 255
        or attempt.get("canary_head")
        != "12bc32d77fb3c381dcee3ba6aea52536b62507b8"
        or attempt.get("referee_disposition_comment_id") != 5200565977
        or attempt.get("state") != "ACTIVATION_FAILED_CLOSED"
        or attempt.get("authority_created") is not False
        or attempt.get("canary_closed_unmerged") is not True
        or attempt.get("ruleset_bypass_actors_after_failure") != []
        or attempt.get("rollback_errors") != []
    ):
        errors.append("third activation failure receipt drift")

    control = value.get("corrected_control", {})
    if control.get("approval_decision_actor") != "github-actions[bot]":
        errors.append("Referee approval actor drift")
    if control.get("merge_executor_actor") != "gcl-release-trust[bot]":
        errors.append("Candidate merge executor actor drift")
    if control.get("merge_executor_required_scope") != "pull_requests:write":
        errors.append("Candidate merge executor scope drift")
    if control.get("expected_head_required") is not True:
        errors.append("exact-head merge execution must remain required")
    if control.get("referee_disposition_must_precede_auto_merge") is not True:
        errors.append("Referee disposition must precede auto-merge")
    if control.get("canary_bypass_must_not_be_used") is not True:
        errors.append("activation canary may not use bypass")
    if control.get("direct_protected_push") is not False:
        errors.append("direct protected push must remain prohibited")
    if control.get("human_steward_impersonation") is not False:
        errors.append("Human Steward impersonation must remain prohibited")
    sequence = control.get("sequence", [])
    if not isinstance(sequence, list) or len(sequence) != 5:
        errors.append("merge executor sequence drift")
    elif sequence.index("Referee Agent records exact-head approval disposition") >= sequence.index(
        "Candidate Agent enables exact-head auto-merge"
    ):
        errors.append("Referee disposition ordering drift")

    notification = value.get("manual_review_notification", {})
    if (
        notification.get("reviewer") != "jimsteeg"
        or notification.get("request_reviewers_api_required") is not True
        or notification.get("explicit_mention_comment_required") is not True
    ):
        errors.append("manual reviewer notification contract drift")

    boundaries = value.get("claim_boundaries", {})
    if not boundaries or any(item is not False for item in boundaries.values()):
        errors.append("claim boundaries must remain false")
    return errors


def validate_stabilization(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "schema_version": "1.0.0",
        "correction_id": "MP-ADMIN-AUTONOMY-STABILIZATION-CORRECTIVE-001",
        "transition_id": "MP-ADMIN-AUTONOMY-TRANSITION-001",
        "repository": "grandchallenge/MATH-PROGRAMME",
        "status": "ARMED_NOT_ACTIVE",
    }
    for key, item in expected.items():
        if value.get(key) != item:
            errors.append(f"stabilization {key} drift")

    attempt = value.get("activation_attempt_004", {})
    if (
        attempt.get("workflow_run_id") != 31073561283
        or attempt.get("artifact_id") != 8956623063
        or attempt.get("artifact_sha256")
        != "5acf88b8fb6b2ddc04ba235eaef074b5bf64fc5f2bb0879c46a414dac3b1d737"
        or attempt.get("transition_head")
        != "7274c1c3207423aea4fab3111e2c63a054eb5908"
        or attempt.get("canary_pull_request") != 257
        or attempt.get("canary_head")
        != "9b3ebae6f8c13d930bad4f648a16df969c67cf33"
        or attempt.get("referee_disposition_comment_id") != 5200676673
        or attempt.get("state") != "ACTIVATION_FAILED_CLOSED"
        or attempt.get("failure_class")
        != "TRANSIENT_POST_DISPOSITION_MERGE_STATE_UNSTABLE"
        or attempt.get("authority_created") is not False
        or attempt.get("canary_closed_unmerged") is not True
        or attempt.get("canary_branch_present_after_failure") is not False
        or attempt.get("ruleset_bypass_actors_after_failure") != []
        or attempt.get("rollback_errors") != []
    ):
        errors.append("fourth activation failure receipt drift")

    control = value.get("corrected_control", {})
    required = {
        "approval_decision_actor": "github-actions[bot]",
        "merge_executor_actor": "gcl-release-trust[bot]",
        "merge_executor_required_scope": "pull_requests:write",
        "required_pre_merge_state": "CLEAN",
        "merge_method": "merge",
        "merge_api": "REST exact-head ordinary merge",
    }
    for key, item in required.items():
        if control.get(key) != item:
            errors.append(f"stabilization control {key} drift")
    for key in (
        "referee_disposition_must_precede_merge",
        "wait_for_all_check_runs_after_disposition",
        "exact_head_revalidated_each_poll",
        "referee_disposition_revalidated_each_poll",
        "auto_merge_authority_retained",
        "canary_bypass_must_not_be_used",
    ):
        if control.get(key) is not True:
            errors.append(f"stabilization control {key} must be true")
    for key in (
        "auto_merge_used_for_clean_canary",
        "direct_protected_push",
        "human_steward_impersonation",
    ):
        if control.get(key) is not False:
            errors.append(f"stabilization control {key} must be false")
    if control.get("accepted_check_conclusions") != [
        "success",
        "neutral",
        "skipped",
    ]:
        errors.append("accepted check conclusions drift")
    if control.get("maximum_stabilization_wait_seconds") != 300:
        errors.append("stabilization timeout drift")
    if control.get("poll_interval_seconds") != 5:
        errors.append("stabilization poll interval drift")
    sequence = control.get("sequence", [])
    if not isinstance(sequence, list) or len(sequence) != 6:
        errors.append("stabilization sequence drift")
    elif sequence.index("Referee Agent records exact-head approval disposition") >= sequence.index(
        "Candidate Agent performs exact-head ordinary merge"
    ):
        errors.append("stabilization merge ordering drift")

    notification = value.get("manual_review_notification", {})
    if (
        notification.get("reviewer") != "jimsteeg"
        or notification.get("request_reviewers_api_required") is not True
        or notification.get("explicit_mention_comment_required") is not True
        or notification.get("exact_head_required") is not True
    ):
        errors.append("stabilization reviewer notification drift")

    boundaries = value.get("claim_boundaries", {})
    if not boundaries or any(item is not False for item in boundaries.values()):
        errors.append("stabilization claim boundaries must remain false")
    return errors


def validate_effective_reviewer_routing(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if value.get("control_id") != "MP-ROUTINE-REVIEWER-ROUTING-001":
        errors.append("routine reviewer routing identity drift")
    if value.get("status") != "ACTIVE_SUBJECT_TO_GI_STEWARD_0002":
        errors.append("routine reviewer routing status drift")
    routing = value.get("effective_routing", {})
    expected = {
        "mandatory_routine_reviewers": [],
        "reviewer_request_api_allowed": False,
        "ordinary_human_steward": "fyremael",
        "recovery_owner": "jimsteeg",
        "exact_recovery_operation_required": True,
    }
    if routing != expected:
        errors.append("effective routine reviewer routing drift")
    historical = value.get("superseded_historical_fields", [])
    expected_paths = {
        "governance/administrative_autonomy_merge_executor_correction.json",
        "governance/administrative_autonomy_runtime_integration.json",
        "governance/administrative_autonomy_stabilization_correction.json",
    }
    if (
        {item.get("path") for item in historical if isinstance(item, dict)} != expected_paths
        or any(item.get("json_pointer") != "/manual_review_notification" or item.get("routing_effect") is not False for item in historical if isinstance(item, dict))
    ):
        errors.append("historical reviewer field supersession drift")
    if any(value.get("authority_boundary", {}).values()):
        errors.append("routine reviewer routing authority boundary weakened")
    return errors


def _pull_request_snapshot(client: Client, node_id: str) -> dict[str, Any]:
    result = client.post(
        "/graphql",
        {
            "query": (
                "query($id:ID!){node(id:$id){... on PullRequest{"
                "number state isDraft headRefOid mergeStateStatus}}}"
            ),
            "variables": {"id": node_id},
        },
    )
    if result.get("errors"):
        raise AutonomyError(f"pull-request state query failed: {result['errors']}")
    value = result.get("data", {}).get("node")
    if not isinstance(value, dict):
        raise AutonomyError("pull-request state query returned no pull request")
    return value


def _referee_disposition_present(
    client: Client,
    repo: str,
    number: int,
    sha: str,
    referee_login: str,
) -> bool:
    comments = client.get(f"/repos/{repo}/issues/{number}/comments?per_page=100")
    expected_head = f"- exact head: `{sha}`;"
    for comment in comments:
        if (
            comment.get("user", {}).get("login") == referee_login
            and str(comment.get("body") or "").startswith(
                "REFEREE_AGENT_APPROVED_EXACT_HEAD"
            )
            and expected_head in str(comment.get("body") or "")
            and "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_AUTO_MERGE"
            in str(comment.get("body") or "")
        ):
            return True
    return False


def _check_runs_state(
    client: Client,
    repo: str,
    sha: str,
    accepted: set[str],
) -> tuple[bool, dict[str, str]]:
    runs = client.get(
        f"/repos/{repo}/commits/{sha}/check-runs?per_page=100"
    ).get("check_runs", [])
    if not runs:
        return False, {"check-runs": "missing"}
    observed: dict[str, str] = {}
    pending = False
    for run in runs:
        name = str(run.get("name") or "unnamed")
        status = str(run.get("status") or "missing")
        conclusion = run.get("conclusion")
        observed[name] = status if status != "completed" else str(conclusion)
        if status != "completed":
            pending = True
        elif conclusion not in accepted:
            raise AutonomyError(
                f"post-disposition check run failed: {name}={conclusion}"
            )
    return not pending, observed


def _wait_for_clean_merge_state(
    candidate: Client,
    referee: Client,
    node_id: str,
    sha: str,
    referee_login: str,
    control: dict[str, Any],
) -> int:
    repo = os.getenv("GITHUB_REPOSITORY", "")
    if repo != "grandchallenge/MATH-PROGRAMME":
        raise AutonomyError("stabilization repository identity drift")
    deadline = time.monotonic() + int(
        control["maximum_stabilization_wait_seconds"]
    )
    poll = int(control["poll_interval_seconds"])
    accepted = set(control["accepted_check_conclusions"])
    last: dict[str, Any] = {}
    while time.monotonic() < deadline:
        snapshot = _pull_request_snapshot(candidate, node_id)
        number = int(snapshot.get("number") or 0)
        if (
            snapshot.get("state") != "OPEN"
            or snapshot.get("isDraft") is not False
            or snapshot.get("headRefOid") != sha
            or number <= 0
        ):
            raise AutonomyError(
                "canary pull request changed before stabilized merge"
            )
        if not _referee_disposition_present(
            referee,
            repo,
            number,
            sha,
            referee_login,
        ):
            raise AutonomyError(
                "exact-head Referee disposition is absent during stabilization"
            )
        settled, checks = _check_runs_state(
            referee,
            repo,
            sha,
            accepted,
        )
        last = {
            "merge_state": snapshot.get("mergeStateStatus"),
            "checks": checks,
        }
        if settled and snapshot.get("mergeStateStatus") == control[
            "required_pre_merge_state"
        ]:
            return number
        time.sleep(poll)
    raise AutonomyError(
        f"post-disposition stabilization timed out: {last}"
    )


def candidate_exact_head_merge(
    referee_client: Client,
    node_id: str,
    sha: str,
    referee_identity: Any,
) -> None:
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
    stabilization = json.loads(STABILIZATION.read_text(encoding="utf-8"))
    routing = json.loads(ROUTING.read_text(encoding="utf-8"))
    errors = validate_correction(correction) + validate_stabilization(
        stabilization
    ) + validate_effective_reviewer_routing(routing)
    if errors:
        raise AutonomyError("; ".join(errors))

    token = os.getenv("CANDIDATE_TOKEN", "")
    login = os.getenv("CANDIDATE_LOGIN", "")
    app_id_text = os.getenv("CANDIDATE_APP_ID", "")
    if not token:
        raise AutonomyError("Candidate merge executor token is missing")
    try:
        app_id = int(app_id_text)
    except ValueError as exc:
        raise AutonomyError("Candidate merge executor app ID is invalid") from exc
    control = stabilization["corrected_control"]
    if login != control["merge_executor_actor"]:
        raise AutonomyError("Candidate merge executor identity drift")
    executor = identity(login, app_id, "candidate-merge-executor")
    candidate = Client(token)
    number = _wait_for_clean_merge_state(
        candidate,
        referee_client,
        node_id,
        sha,
        referee_identity.login,
        control,
    )
    repo = os.getenv("GITHUB_REPOSITORY", "")
    result = candidate.put(
        f"/repos/{repo}/pulls/{number}/merge",
        {
            "sha": sha,
            "merge_method": control["merge_method"],
            "commit_title": "Activate MP-ADMIN-AUTONOMY-TRANSITION-001",
            "commit_message": (
                f"Exact head {sha}\n\n"
                "Disposition: REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE"
            ),
        },
    )
    if result.get("merged") is not True:
        raise AutonomyError(
            f"Candidate exact-head merge failed: {result.get('message')}"
        )
    readback = candidate.get(f"/repos/{repo}/pulls/{number}")
    if (
        readback.get("merged") is not True
        or readback.get("head", {}).get("sha") != sha
        or readback.get("merged_by", {}).get("login") != executor.login
    ):
        raise AutonomyError("Candidate exact-head merge actor readback failed")


def corrected_activation_record(*args: Any, **kwargs: Any) -> dict[str, Any]:
    record = ORIGINAL_ACTIVATION_RECORD(*args, **kwargs)
    record["referee_disposition"].pop("recorded_before_auto_merge", None)
    record["referee_disposition"][
        "recorded_before_merge_execution"
    ] = True
    record["auto_merge"] = {
        "repository_enabled": True,
        "authority_retained": True,
        "used_for_canary": False,
        "reason": "post-disposition checks settle before CLEAN exact-head merge",
    }
    record["canary"][
        "post_disposition_check_stabilization_required"
    ] = True
    record["canary"]["required_pre_merge_state"] = "CLEAN"
    record["canary"]["merge_executor"] = "gcl-release-trust[bot]"
    return record


ORIGINAL_ACTIVATION_RECORD = base.activation_record


def main() -> int:
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
    stabilization = json.loads(STABILIZATION.read_text(encoding="utf-8"))
    routing = json.loads(ROUTING.read_text(encoding="utf-8"))
    errors = validate_correction(correction) + validate_stabilization(
        stabilization
    ) + validate_effective_reviewer_routing(routing)
    if errors:
        raise AutonomyError("; ".join(errors))
    base.auto_merge = candidate_exact_head_merge
    base.activation_record = corrected_activation_record
    return base.main(["activate"])


if __name__ == "__main__":
    raise SystemExit(main())
