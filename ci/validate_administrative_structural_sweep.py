from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORD = ROOT / "governance" / "administrative_structural_sweeps" / "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-006.json"
SCHEMA_PATH = ROOT / "schemas" / "administrative_structural_sweep_v2.schema.json"

EXPECTED_SWEEP_ID = "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-006"
EXPECTED_DUE = "2026-08-04T23:09:00-07:00"
EXPECTED_NEXT_DUE = "2026-08-05T15:57:00-07:00"
EXPECTED_ADMIN_REVIEW = "2026-08-06T18:21:00-07:00"
EXPECTED_PILOT_REVIEW = "2026-08-09T18:21:00-07:00"
EXPECTED_BRANCH = "governance/mp-admin-structural-sweep-2026-08-04-006"

EXPECTED_REPOSITORIES: dict[str, dict[str, Any]] = {
    "grandchallenge/MATH-PROGRAMME": {
        "protected_head": "e8cc9f6142683a095b10d8732e55bb4dab527954",
        "reviewed_head": "0d6ab392dc4c6e160bb87993e482c69964b65afd",
        "latest_transition_pr": 223,
        "merge_commit": "e8cc9f6142683a095b10d8732e55bb4dab527954",
        "review_id": 4860283220,
        "disposition_comment_id": 5186832691,
        "core_run_id": 30966946808,
        "gcl_run_id": 30966947087,
    },
    "grandchallenge/MATHFORGE": {
        "protected_head": "da79f89388099749d6a93e03c4364fc018a19197",
        "reviewed_head": "34c608bb91886f5fb63f07a8e6707f1694f69f44",
        "latest_transition_pr": 57,
        "merge_commit": "da79f89388099749d6a93e03c4364fc018a19197",
        "review_id": 4840067811,
        "disposition_comment_id": None,
        "core_run_id": 30773230270,
        "gcl_run_id": 30773230485,
    },
    "grandchallenge/MATHSOLVE": {
        "protected_head": "1ebc9ace360e453fbc3707f6b23032b1c3c561eb",
        "reviewed_head": "5743743fde5eadaa8f1f9f33dcc59d582966e8cf",
        "latest_transition_pr": 99,
        "merge_commit": "1ebc9ace360e453fbc3707f6b23032b1c3c561eb",
        "review_id": 4854230081,
        "disposition_comment_id": 5178998739,
        "core_run_id": 30907913946,
        "gcl_run_id": 30907915050,
    },
    "grandchallenge/MATHCERT": {
        "protected_head": "92e3e56fda50267a241e120eb337dbbc520e900f",
        "reviewed_head": "52b3d6e4958662053683ed3656efdf160c812e6d",
        "latest_transition_pr": 85,
        "merge_commit": "92e3e56fda50267a241e120eb337dbbc520e900f",
        "review_id": 4854640557,
        "disposition_comment_id": 5179403169,
        "core_run_id": 30910428434,
        "gcl_run_id": 30910429273,
    },
    "grandchallenge/INTELLECT": {
        "protected_head": "70a0a74502e0480d387d740027e48751286e4bfe",
        "reviewed_head": "dbb68b54aaf6df2eced710e6dd3936aa3bb2f7fc",
        "latest_transition_pr": 51,
        "merge_commit": "70a0a74502e0480d387d740027e48751286e4bfe",
        "review_id": 4860177595,
        "disposition_comment_id": None,
        "core_run_id": 30965213743,
        "gcl_run_id": 30965214071,
    },
}

EXPECTED_OPEN_PR = {
    "repository": "grandchallenge/MATHCERT",
    "pull_request": 86,
    "author": "dependabot[bot]",
    "head": "6a9c61661337bbd44abd2bcc33ca8bb46e536644",
    "base": "92e3e56fda50267a241e120eb337dbbc520e900f",
    "draft": False,
    "merge_authorized": False,
    "core_run_id": 30965349028,
    "gcl_run_id": 30965349284,
    "interference_disposition": "NON_AUTHORITATIVE_MAINTENANCE_PR_NO_PROTECTED_INTERFERENCE",
}

EXPECTED_TRACKERS = {
    ("grandchallenge/MATH-PROGRAMME", 182),
    ("grandchallenge/MATH-PROGRAMME", 183),
    ("grandchallenge/INTELLECT", 21),
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_record(record: dict[str, Any]) -> list[str]:
    schema = _load(SCHEMA_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"schema: {'/'.join(str(part) for part in error.absolute_path)}: {error.message}"
        for error in validator.iter_errors(record)
    ]

    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    require(record.get("sweep_id") == EXPECTED_SWEEP_ID, "unexpected sweep identity")
    require(record.get("scheduled_due_at") == EXPECTED_DUE, "scheduled deadline drift")
    require(record.get("next_structural_due_at") == EXPECTED_NEXT_DUE, "next structural deadline drift")
    require(record.get("administrative_review_due_at") == EXPECTED_ADMIN_REVIEW, "administrative review deadline drift")
    require(record.get("pilot_review_due_at") == EXPECTED_PILOT_REVIEW, "pilot review deadline drift")
    require(record.get("evidence_mode") == "CONTEMPORANEOUS", "evidence is not classified as contemporaneous")
    require(record.get("cadence") == "PT16H48M", "cadence changed")
    require(record.get("lateness_minutes_at_start") == 0, "on-time start is not recorded exactly")

    try:
        due = datetime.fromisoformat(record["scheduled_due_at"])
        started = datetime.fromisoformat(record["execution_started_at"])
        closed = datetime.fromisoformat(record["evidence_closed_at"])
        next_due = datetime.fromisoformat(record["next_structural_due_at"])
        require(started <= closed <= due, "contemporaneous evidence window is outside the scheduled locus")
        require(next_due - due == timedelta(hours=16, minutes=48), "next deadline does not preserve PT16H48M")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid sweep chronology: {exc}")

    baseline = record.get("baseline_reset", {})
    require(baseline.get("original_authorized_head") == "cc30c7766f9d738dadb3df20ef7a30c78e98ec1c", "original start head drift")
    require(baseline.get("reset_protected_head") == "e8cc9f6142683a095b10d8732e55bb4dab527954", "reset protected head drift")
    require(baseline.get("reset_transition_pr") == 223, "reset transition PR drift")
    require(baseline.get("reset_transition_reviewed_head") == "0d6ab392dc4c6e160bb87993e482c69964b65afd", "reset reviewed head drift")
    require(baseline.get("implementation_branch") == EXPECTED_BRANCH, "implementation branch drift")
    require(baseline.get("branch_ahead_before_reset") == 0, "reset discarded unrecorded branch work")
    require(baseline.get("implementation_commits_discarded") == 0, "implementation commit loss recorded")
    require(baseline.get("pending_manual_processes_at_reset") == 0, "manual process remained pending at reset")
    require(baseline.get("cadence_anchor_reset") is False, "cadence anchor was reset")

    repositories = record.get("scope", {}).get("repositories", [])
    observed = {
        item.get("repository"): item
        for item in repositories
        if isinstance(item, dict) and isinstance(item.get("repository"), str)
    }
    require(len(repositories) == 5 and len(observed) == 5, "repository inventory is missing or duplicated")
    require(set(observed) == set(EXPECTED_REPOSITORIES), "repository inventory differs from the five-repository control scope")

    for repository, expected in EXPECTED_REPOSITORIES.items():
        item = observed.get(repository, {})
        for field in ("protected_head", "reviewed_head", "latest_transition_pr", "merge_commit"):
            require(item.get(field) == expected[field], f"{repository}: {field} drift")
        review = item.get("review", {})
        require(review.get("review_id") == expected["review_id"], f"{repository}: review identity drift")
        require(review.get("state") == "APPROVED", f"{repository}: latest transition lacks approved review")
        require(review.get("exact_head") is True, f"{repository}: review is not exact-head")
        disposition = item.get("disposition", {})
        require(disposition.get("comment_id") == expected["disposition_comment_id"], f"{repository}: disposition identity drift")
        if disposition.get("required"):
            require(disposition.get("actor") == "fyremael", f"{repository}: required disposition actor mismatch")
            require(disposition.get("exact_head") is True, f"{repository}: required disposition is not exact-head")
            require(disposition.get("comment_id") is not None, f"{repository}: required disposition is missing")
        core = item.get("core_workflow", {})
        gcl = item.get("gcl_workflow", {})
        require(core.get("run_id") == expected["core_run_id"] and core.get("conclusion") == "success", f"{repository}: core workflow evidence drift or failure")
        require(gcl.get("run_id") == expected["gcl_run_id"] and gcl.get("conclusion") == "success", f"{repository}: GCL workflow evidence drift or failure")

    open_prs = record.get("scope", {}).get("open_pull_requests", [])
    require(len(open_prs) == 1, "open PR evidence was omitted or inflated")
    if len(open_prs) == 1:
        require(open_prs[0] == EXPECTED_OPEN_PR, "open PR evidence differs from the contemporaneous freeze")
        require(open_prs[0].get("merge_authorized") is False, "open maintenance PR was falsely authorized")

    trackers = record.get("tracker_mirrors", [])
    tracker_keys = {(item.get("repository"), item.get("issue")) for item in trackers if isinstance(item, dict)}
    require(tracker_keys == EXPECTED_TRACKERS and len(trackers) == 3, "canonical tracker inventory is missing or duplicated")
    intellect = next((item for item in trackers if item.get("repository") == "grandchallenge/INTELLECT"), {})
    require(intellect.get("repair_required") is True, "INTELLECT tracker defect was omitted")
    require(intellect.get("repair_completed") is True, "INTELLECT tracker repair is incomplete")

    findings = record.get("findings", {})
    require(findings.get("P0") == [], "P0 finding prevents closure")
    require(findings.get("P1") == [], "P1 finding prevents closure")
    require(len(findings.get("P2", [])) == 2, "bounded P2 findings were omitted or inflated")
    require(all("REPAIRED" in item.get("disposition", "") or "CLARIFIED" in item.get("disposition", "") for item in findings.get("P2", [])), "a P2 finding lacks a repaired or clarified disposition")

    readiness = record.get("review_readiness", {})
    require(readiness.get("protected_review_clear_to_proceed") is True, "protected review is not clear to proceed")
    require(readiness.get("circuit_breaker_triggered") is False, "circuit breaker was triggered")
    require(readiness.get("waiver_used") is False, "waiver was used")
    require(readiness.get("emergency_authority_used") is False, "emergency authority was used")
    require(readiness.get("pending_manual_processes_at_evidence_freeze") == 0, "manual process remained pending at evidence freeze")
    require(readiness.get("independent_exact_head_review_required") is True, "independent exact-head review gate was removed")
    require(readiness.get("human_steward_exact_head_disposition_required") is True, "Human Steward disposition gate was removed")

    boundaries = record.get("claim_boundaries", {})
    require(boundaries and all(value is False for value in boundaries.values()), "claim boundary inflation detected")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the current administrative structural sweep")
    parser.add_argument("record", nargs="?", type=Path, default=DEFAULT_RECORD)
    args = parser.parse_args()
    record = _load(args.record)
    errors = validate_record(record)
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f"{record['sweep_id']}: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
