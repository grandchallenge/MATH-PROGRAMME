from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Callable

from administrative_autonomy_receipt_stage import (
    STATE_PATH,
    completion_has_receipt,
    receipt_for,
)
from administrative_autonomy_runtime_contract import validate_record
from autonomy_github import AutonomyError, content, json_content

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = (
    ROOT
    / "governance"
    / "administrative_review_0813_receipt_recovery_control.json"
)

PendingFunction = Callable[[Any, str, dict[str, Any], str], list[dict[str, Any]]]


def load_control() -> dict[str, Any]:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def _require_control(control: dict[str, Any]) -> None:
    if control.get("control_id") != "MP-ADMIN-ADMINISTRATIVE-0813-RECEIPT-RECOVERY-001":
        raise AutonomyError("Aug13 administrative receipt recovery control identity drift")
    if control.get("issue") != 554:
        raise AutonomyError("Aug13 administrative receipt recovery issue identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        raise AutonomyError("Aug13 administrative receipt recovery control is not active")
    if control.get("repository") != "grandchallenge/MATH-PROGRAMME":
        raise AutonomyError("Aug13 administrative receipt recovery repository drift")
    if control.get("protected_base_at_opening") != "39b11cba696f5719c6e7b437d4940d129f762822":
        raise AutonomyError("Aug13 administrative receipt recovery opening-base drift")

    correction = control.get("correction", {})
    required = {
        "closed_issue_re_admission_exact_target_only": True,
        "protected_record_reuse_required": True,
        "record_reexecution_allowed": False,
        "record_remerge_allowed": False,
        "ordinary_receipt_stage_required": True,
        "completion_state_only_receipt_pr_required": True,
        "administrative_frontier_advance_exactly_one_locus": True,
        "structural_frontier_preserved": True,
        "mirror_readback_required": True,
        "duplicate_receipt_prohibited": True,
        "deadline_reset": False,
        "cadence_anchor_reset": False,
        "issue_522_or_pr_523_execution_authorized": False,
    }
    for key, expected in required.items():
        if correction.get(key) != expected:
            raise AutonomyError(f"Aug13 administrative receipt recovery control drift: {key}")

    authority = control.get("authority_boundary", {})
    if authority.get("human_steward_exact_head_authorization_required") is not True:
        raise AutonomyError("Aug13 administrative receipt recovery Human Steward gate drift")
    prohibited = (
        "historical_record_merge_is_authority_for_new_control",
        "candidate_branch_is_authority",
        "direct_protected_push_authorized",
        "bypass_created",
        "general_closed_issue_recovery_authority_created",
        "general_late_recovery_authority_created",
        "issue_522_or_pr_523_authority_created",
    )
    if any(authority.get(key) is not False for key in prohibited):
        raise AutonomyError("Aug13 administrative receipt recovery authority boundary drift")

    claims = control.get("claim_boundaries", {})
    if not claims or any(value is not False for value in claims.values()):
        raise AutonomyError("Aug13 administrative receipt recovery claim boundary drift")


def _require_ancestor(candidate: Any, repo: str, ancestor: str) -> None:
    comparison = candidate.get(f"/repos/{repo}/compare/{ancestor}...main")
    merge_base = str(comparison.get("merge_base_commit", {}).get("sha") or "")
    if merge_base != ancestor:
        raise AutonomyError(
            f"Aug13 administrative receipt recovery ancestry failed for {ancestor}"
        )


def _target_receipt(
    control: dict[str, Any], record: dict[str, Any]
) -> dict[str, Any]:
    occurrence = control["occurrence"]
    return receipt_for(
        str(occurrence["procedure_id"]),
        str(occurrence["due_at_utc"]),
        str(occurrence["record_path"]),
        record,
        str(occurrence["record_merge_commit"]),
        str(occurrence["reviewed_head"]),
        int(occurrence["candidate_pull_request"]),
    )


def _load_target(
    candidate: Any, repo: str, control: dict[str, Any]
) -> dict[str, Any] | None:
    _require_control(control)
    occurrence = control["occurrence"]

    completion = json_content(candidate, repo, STATE_PATH, "main")
    if completion is None:
        raise AutonomyError("Aug13 administrative receipt recovery completion ledger is absent")
    procedure = completion.get("procedures", {}).get("administrative_review")
    if not isinstance(procedure, dict):
        raise AutonomyError("Aug13 administrative receipt recovery ledger procedure is absent")

    due = str(occurrence["due_at_utc"])
    same_due = [
        item
        for item in procedure.get("receipts", [])
        if str(item.get("scheduled_due_at") or "") == due
    ]
    if len(same_due) > 1:
        raise AutonomyError("duplicate Aug13 administrative completion receipts")

    raw_record = content(candidate, repo, str(occurrence["record_path"]), "main")
    if raw_record is None:
        raise AutonomyError("Aug13 protected administrative record is absent")
    if str(raw_record.get("sha") or "") != str(occurrence["record_blob_sha"]):
        raise AutonomyError("Aug13 protected administrative record blob drift")
    record = json.loads(base64.b64decode(raw_record["content"]))
    errors = validate_record(record)
    if errors:
        raise AutonomyError("; ".join(errors))

    expected_source = {
        "occurrence_key": occurrence["occurrence_key"],
        "issue_number": occurrence["candidate_issue"],
        "pull_request_number": occurrence["candidate_pull_request"],
        "branch": occurrence["candidate_branch"],
        "source_protected_head": occurrence["original_source_protected_head"],
    }
    source = record.get("source_candidate", {})
    if (
        record.get("record_id") != occurrence["record_id"]
        or record.get("procedure_id") != occurrence["procedure_id"]
        or record.get("scheduled_due_at") != due
        or record.get("status") != "COMPLETE_AUTONOMOUS"
        or any(source.get(key) != value for key, value in expected_source.items())
    ):
        raise AutonomyError("Aug13 protected administrative record identity drift")

    receipt = _target_receipt(control, record)
    if same_due:
        if not completion_has_receipt(completion, receipt):
            raise AutonomyError("conflicting Aug13 administrative completion receipt")
        return None

    if procedure.get("completed_through_utc") != occurrence["expected_prior_frontier_utc"]:
        raise AutonomyError("Aug13 administrative predecessor frontier drift")

    manifest = json_content(candidate, repo, str(occurrence["manifest_path"]), "main")
    if manifest is None:
        raise AutonomyError("Aug13 administrative candidate manifest is absent")
    manifest_expected = {
        "state": "CANDIDATE_PREPARED",
        "occurrence_key": occurrence["occurrence_key"],
        "procedure_id": occurrence["procedure_id"],
        "scheduled_due_at": due,
        "source_protected_head": occurrence["original_source_protected_head"],
        "branch": occurrence["candidate_branch"],
        "manifest_path": occurrence["manifest_path"],
        "issue_number": occurrence["candidate_issue"],
        "pull_request_number": occurrence["candidate_pull_request"],
    }
    if any(manifest.get(key) != value for key, value in manifest_expected.items()):
        raise AutonomyError("Aug13 administrative candidate manifest identity drift")

    issue = candidate.get(f"/repos/{repo}/issues/{occurrence['candidate_issue']}")
    issue_body = str(issue.get("body") or "")
    if (
        issue.get("state") != "closed"
        or issue.get("state_reason") != "completed"
        or f"administrative-candidate:{occurrence['occurrence_key']}" not in issue_body
    ):
        raise AutonomyError("Aug13 administrative issue closure identity drift")

    pull = candidate.get(f"/repos/{repo}/pulls/{occurrence['candidate_pull_request']}")
    if (
        pull.get("merged") is not True
        or str(pull.get("head", {}).get("sha") or "") != occurrence["reviewed_head"]
        or str(pull.get("merge_commit_sha") or "") != occurrence["record_merge_commit"]
    ):
        raise AutonomyError("Aug13 administrative protected PR identity drift")

    reviews = candidate.get(
        f"/repos/{repo}/pulls/{occurrence['candidate_pull_request']}/reviews?per_page=100"
    )
    review_matches = [
        item
        for item in reviews
        if int(item.get("id") or 0) == int(occurrence["independent_review"])
    ]
    if len(review_matches) != 1:
        raise AutonomyError("Aug13 administrative independent review identity drift")
    review = review_matches[0]
    if (
        review.get("state") != "APPROVED"
        or str(review.get("commit_id") or "") != occurrence["reviewed_head"]
        or str(review.get("user", {}).get("login") or "") != "jimsteeg"
        or str(review.get("author_association") or "") not in {"MEMBER", "CONTRIBUTOR"}
    ):
        raise AutonomyError("Aug13 administrative independent review drift")

    steward_comments = candidate.get(
        f"/repos/{repo}/issues/{occurrence['candidate_issue']}/comments?per_page=100"
    )
    steward_matches = [
        item
        for item in steward_comments
        if int(item.get("id") or 0)
        == int(occurrence["human_steward_disposition_comment"])
    ]
    if len(steward_matches) != 1:
        raise AutonomyError("Aug13 administrative Human Steward disposition identity drift")
    steward = steward_matches[0]
    steward_body = str(steward.get("body") or "")
    required_markers = (
        "AUTHORIZE_EXACT_HEAD_PROTECTED_MERGE__NO_OTHER_AUTHORITY",
        occurrence["occurrence_key"],
        f"PR: #{occurrence['candidate_pull_request']}",
        occurrence["reviewed_head"],
        occurrence["human_steward_bound_base"],
        str(occurrence["independent_review"]),
    )
    if (
        str(steward.get("user", {}).get("login") or "") != "fyremael"
        or str(steward.get("author_association") or "") != "MEMBER"
        or not all(marker in steward_body for marker in required_markers)
    ):
        raise AutonomyError("Aug13 administrative Human Steward disposition drift")

    _require_ancestor(candidate, repo, str(occurrence["original_source_protected_head"]))
    _require_ancestor(candidate, repo, str(occurrence["record_merge_commit"]))
    _require_ancestor(candidate, repo, str(control["protected_base_at_opening"]))

    return {
        "manifest": manifest,
        "record": record,
        "record_id": str(occurrence["record_id"]),
        "record_path": str(occurrence["record_path"]),
        "issue_number": int(occurrence["candidate_issue"]),
        "pull_request": int(occurrence["candidate_pull_request"]),
        "exact_head": str(occurrence["reviewed_head"]),
        "record_merge_commit": str(occurrence["record_merge_commit"]),
        "record_disposition_comment_id": int(
            occurrence["human_steward_disposition_comment"]
        ),
        "receipt_present": False,
        "receipt": receipt,
    }


def pending_closures(
    candidate: Any,
    repo: str,
    runtime: dict[str, Any],
    referee_login: str,
    base: PendingFunction,
) -> list[dict[str, Any]]:
    """Re-admit only the closed Aug13 protected record for receipt completion.

    The exact predecessor receipt has priority while absent. After it is
    protected, this wrapper becomes transparent and delegates to the existing
    protected closure classifier.
    """

    control = load_control()
    target = _load_target(candidate, repo, control)
    if target is not None:
        return [target]
    return base(candidate, repo, runtime, referee_login)
