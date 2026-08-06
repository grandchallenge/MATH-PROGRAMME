from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import administrative_autonomy as base
from autonomy_github import AutonomyError, Client, auto_merge as github_auto_merge, identity


ROOT = Path(__file__).resolve().parents[1]
CORRECTION = ROOT / "governance/administrative_autonomy_merge_executor_correction.json"


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


def candidate_auto_merge(
    _referee_client: Client,
    node_id: str,
    sha: str,
    _referee_identity: Any,
) -> None:
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
    errors = validate_correction(correction)
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
    expected_login = correction["corrected_control"]["merge_executor_actor"]
    if login != expected_login:
        raise AutonomyError("Candidate merge executor identity drift")

    executor = identity(login, app_id, "candidate-merge-executor")
    github_auto_merge(Client(token), node_id, sha, executor)


def main() -> int:
    correction = json.loads(CORRECTION.read_text(encoding="utf-8"))
    errors = validate_correction(correction)
    if errors:
        raise AutonomyError("; ".join(errors))
    base.auto_merge = candidate_auto_merge
    return base.main(["activate"])


if __name__ == "__main__":
    raise SystemExit(main())
