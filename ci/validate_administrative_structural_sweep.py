from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RECORD = (
    ROOT
    / "governance"
    / "administrative_structural_sweeps"
    / "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007.json"
)
SCHEMA_PATH = ROOT / "schemas" / "administrative_structural_sweep_v2.schema.json"

BASELINE_EXPECTED = {
    "original_authorized_head": "cc30c7766f9d738dadb3df20ef7a30c78e98ec1c",
    "reset_protected_head": "e8cc9f6142683a095b10d8732e55bb4dab527954",
    "reset_transition_pr": 223,
    "reset_transition_reviewed_head": "0d6ab392dc4c6e160bb87993e482c69964b65afd",
    "implementation_branch": "governance/mp-admin-structural-sweep-2026-08-04-006",
    "branch_ahead_before_reset": 0,
    "branch_behind_before_reset": 20,
    "implementation_commits_discarded": 0,
    "pending_manual_processes_at_reset": 0,
    "cadence_anchor_reset": False,
}

EXPECTATIONS: dict[str, dict[str, Any]] = {'MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-006': {'admin_review': '2026-08-06T18:21:00-07:00',
                                              'due': '2026-08-04T23:09:00-07:00',
                                              'execution_authority': 'Human Steward or delegated Programme '
                                                                     'administrator',
                                              'next_due': '2026-08-05T15:57:00-07:00',
                                              'open_pull_requests': [{'author': 'dependabot[bot]',
                                                                      'base': '92e3e56fda50267a241e120eb337dbbc520e900f',
                                                                      'core_run_id': 30965349028,
                                                                      'draft': False,
                                                                      'gcl_run_id': 30965349284,
                                                                      'head': '6a9c61661337bbd44abd2bcc33ca8bb46e536644',
                                                                      'interference_disposition': 'NON_AUTHORITATIVE_MAINTENANCE_PR_NO_PROTECTED_INTERFERENCE',
                                                                      'merge_authorized': False,
                                                                      'pull_request': 86,
                                                                      'repository': 'grandchallenge/MATHCERT'}],
                                              'p2_count': 2,
                                              'p3_count': 1,
                                              'pilot_review': '2026-08-09T18:21:00-07:00',
                                              'repositories': {'grandchallenge/INTELLECT': {'core_name': 'CI',
                                                                                            'core_run_id': 30965213743,
                                                                                            'disposition_comment_id': None,
                                                                                            'disposition_required': False,
                                                                                            'gcl_run_id': 30965214071,
                                                                                            'latest_transition_pr': 51,
                                                                                            'material_transition': 'TC_FIXTURE_004_REVIEW_REMEDY_PROTECTED_TC_FIXTURE_005_UNBLOCKED',
                                                                                            'merge_commit': '70a0a74502e0480d387d740027e48751286e4bfe',
                                                                                            'protected_head': '70a0a74502e0480d387d740027e48751286e4bfe',
                                                                                            'review_id': 4860177595,
                                                                                            'reviewed_head': 'dbb68b54aaf6df2eced710e6dd3936aa3bb2f7fc',
                                                                                            'reviewer': 'jimsteeg',
                                                                                            'tracker_issue': 21},
                                                               'grandchallenge/MATH-PROGRAMME': {'core_name': 'Programme '
                                                                                                              'policy '
                                                                                                              'checks',
                                                                                                 'core_run_id': 30966946808,
                                                                                                 'disposition_comment_id': 5186832691,
                                                                                                 'disposition_required': True,
                                                                                                 'gcl_run_id': 30966947087,
                                                                                                 'latest_transition_pr': 223,
                                                                                                 'material_transition': 'PR_223_PROTECTED_SOURCE_REVISION_PARTIALLY_ADMITTED_WITH_BLOCKERS',
                                                                                                 'merge_commit': 'e8cc9f6142683a095b10d8732e55bb4dab527954',
                                                                                                 'protected_head': 'e8cc9f6142683a095b10d8732e55bb4dab527954',
                                                                                                 'review_id': 4860283220,
                                                                                                 'reviewed_head': '0d6ab392dc4c6e160bb87993e482c69964b65afd',
                                                                                                 'reviewer': 'jimsteeg',
                                                                                                 'tracker_issue': 182},
                                                               'grandchallenge/MATHCERT': {'core_name': 'Cert checks',
                                                                                           'core_run_id': 30910428434,
                                                                                           'disposition_comment_id': 5179403169,
                                                                                           'disposition_required': True,
                                                                                           'gcl_run_id': 30910429273,
                                                                                           'latest_transition_pr': 85,
                                                                                           'material_transition': 'VGSE_ROUTE_REGISTERED_PENDING_EVIDENCE',
                                                                                           'merge_commit': '92e3e56fda50267a241e120eb337dbbc520e900f',
                                                                                           'protected_head': '92e3e56fda50267a241e120eb337dbbc520e900f',
                                                                                           'review_id': 4854640557,
                                                                                           'reviewed_head': '52b3d6e4958662053683ed3656efdf160c812e6d',
                                                                                           'reviewer': 'jimsteeg',
                                                                                           'tracker_issue': 84},
                                                               'grandchallenge/MATHFORGE': {'core_name': 'Forge checks',
                                                                                            'core_run_id': 30773230270,
                                                                                            'disposition_comment_id': None,
                                                                                            'disposition_required': False,
                                                                                            'gcl_run_id': 30773230485,
                                                                                            'latest_transition_pr': 57,
                                                                                            'material_transition': 'NO_NEW_PROTECTED_TRANSITION_AFTER_PRECEDING_SWEEP_DUE',
                                                                                            'merge_commit': 'da79f89388099749d6a93e03c4364fc018a19197',
                                                                                            'protected_head': 'da79f89388099749d6a93e03c4364fc018a19197',
                                                                                            'review_id': 4840067811,
                                                                                            'reviewed_head': '34c608bb91886f5fb63f07a8e6707f1694f69f44',
                                                                                            'reviewer': 'jimsteeg',
                                                                                            'tracker_issue': 56},
                                                               'grandchallenge/MATHSOLVE': {'core_name': 'Solve checks',
                                                                                            'core_run_id': 30907913946,
                                                                                            'disposition_comment_id': 5178998739,
                                                                                            'disposition_required': True,
                                                                                            'gcl_run_id': 30907915050,
                                                                                            'latest_transition_pr': 99,
                                                                                            'material_transition': 'VGSE_BOUNDED_SOLVE_ACTIVATION_PROTECTED',
                                                                                            'merge_commit': '1ebc9ace360e453fbc3707f6b23032b1c3c561eb',
                                                                                            'protected_head': '1ebc9ace360e453fbc3707f6b23032b1c3c561eb',
                                                                                            'review_id': 4854230081,
                                                                                            'reviewed_head': '5743743fde5eadaa8f1f9f33dcc59d582966e8cf',
                                                                                            'reviewer': 'jimsteeg',
                                                                                            'tracker_issue': 98}},
                                              'status': 'COMPLETE_WITH_REPAIRED_P2_AND_NONBLOCKING_OPEN_PR',
                                              'trackers': {('grandchallenge/INTELLECT', 21): ('REPAIRED_NAVIGATION_ONLY',
                                                                                            True,
                                                                                            True),
                                                           ('grandchallenge/MATH-PROGRAMME', 182): ('CURRENT_NAVIGATION_ONLY',
                                                                                                  False,
                                                                                                  False),
                                                           ('grandchallenge/MATH-PROGRAMME', 183): ('CURRENT_NAVIGATION_ONLY',
                                                                                                  False,
                                                                                                  False)}},
 'MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007': {'admin_review': '2026-08-06T18:21:00-07:00',
                                              'due': '2026-08-05T15:57:00-07:00',
                                              'execution_authority': 'Human Steward-authorized Programme '
                                                                     'administration under MATH-PROGRAMME PR '
                                                                     '#244 comment 5198084851',
                                              'next_due': '2026-08-06T08:45:00-07:00',
                                              'open_pull_requests': [{'author': 'gcl-release-trust[bot]',
                                                                      'base': '6dd51c29b8bcbac812bcf7a4e803b693ac8be69c',
                                                                      'core_run_id': 31048863420,
                                                                      'draft': False,
                                                                      'gcl_run_id': 31048863707,
                                                                      'head': 'ea0d21307724deeffd2b83e714a64b47a4dda40e',
                                                                      'interference_disposition': 'CONTROLLED_MAINTENANCE_CANDIDATE_PENDING_SUCCESSOR_EXACT_HEAD_REVIEW_NO_PROTECTED_EFFECT',
                                                                      'merge_authorized': False,
                                                                      'pull_request': 244,
                                                                      'repository': 'grandchallenge/MATH-PROGRAMME'},
                                                                     {'author': 'dependabot[bot]',
                                                                      'base': '6dd51c29b8bcbac812bcf7a4e803b693ac8be69c',
                                                                      'core_run_id': 31052032657,
                                                                      'draft': False,
                                                                      'gcl_run_id': 31052037004,
                                                                      'head': '97ed54d717b140a29b43eed58ab7d081e56d2662',
                                                                      'interference_disposition': 'NONAUTHORITATIVE_DEPENDABOT_ACTION_UPGRADE_WITH_FAILED_POLICY_CHECK_NO_PROTECTED_INTERFERENCE',
                                                                      'merge_authorized': False,
                                                                      'pull_request': 247,
                                                                      'repository': 'grandchallenge/MATH-PROGRAMME'}],
                                              'p2_count': 2,
                                              'p3_count': 1,
                                              'pilot_review': '2026-08-09T18:21:00-07:00',
                                              'repositories': {'grandchallenge/INTELLECT': {'core_name': 'CI',
                                                                                            'core_run_id': 30965213743,
                                                                                            'disposition_comment_id': None,
                                                                                            'disposition_required': False,
                                                                                            'gcl_run_id': 30965214071,
                                                                                            'latest_transition_pr': 51,
                                                                                            'material_transition': 'NO_NEW_PROTECTED_TRANSITION_AFTER_PRECEDING_SWEEP_DUE',
                                                                                            'merge_commit': '70a0a74502e0480d387d740027e48751286e4bfe',
                                                                                            'protected_head': '70a0a74502e0480d387d740027e48751286e4bfe',
                                                                                            'review_id': 4860177595,
                                                                                            'reviewed_head': 'dbb68b54aaf6df2eced710e6dd3936aa3bb2f7fc',
                                                                                            'reviewer': 'jimsteeg',
                                                                                            'tracker_issue': 21},
                                                               'grandchallenge/MATH-PROGRAMME': {'core_name': 'Programme '
                                                                                                              'policy '
                                                                                                              'checks',
                                                                                                 'core_run_id': 31048745481,
                                                                                                 'disposition_comment_id': 5197539186,
                                                                                                 'disposition_required': True,
                                                                                                 'gcl_run_id': 31048747660,
                                                                                                 'latest_transition_pr': 246,
                                                                                                 'material_transition': 'EUCLID_DIOPHANTINE_E2E_STAGE_2_PROGRAMME_CLOSEOUT_AND_PUBLIC_PROOF_TRACE_PROTECTED',
                                                                                                 'merge_commit': '6dd51c29b8bcbac812bcf7a4e803b693ac8be69c',
                                                                                                 'protected_head': '6dd51c29b8bcbac812bcf7a4e803b693ac8be69c',
                                                                                                 'review_id': 4868833217,
                                                                                                 'reviewed_head': '6b93e72f7a3de505ce981a6ed70b2ec1b9139c5c',
                                                                                                 'reviewer': 'jimsteeg',
                                                                                                 'tracker_issue': 182},
                                                               'grandchallenge/MATHCERT': {'core_name': 'Cert checks',
                                                                                           'core_run_id': 31045780294,
                                                                                           'disposition_comment_id': 5197159308,
                                                                                           'disposition_required': True,
                                                                                           'gcl_run_id': 31045783552,
                                                                                           'latest_transition_pr': 90,
                                                                                           'material_transition': 'CERTIFIED_LINEAR_DIOPHANTINE_EQUIVALENCE_AND_BOUNDED_EXEMPLARS_PROTECTED',
                                                                                           'merge_commit': 'cd69013cf55d4ee96539d28ee27eadef64cca06f',
                                                                                           'protected_head': 'cd69013cf55d4ee96539d28ee27eadef64cca06f',
                                                                                           'review_id': 4868582253,
                                                                                           'reviewed_head': 'f71a1c6b7f39ec0154647e5bae0044cbd040e219',
                                                                                           'reviewer': 'jimsteeg',
                                                                                           'tracker_issue': 89},
                                                               'grandchallenge/MATHFORGE': {'core_name': 'Forge checks',
                                                                                            'core_run_id': 31052158653,
                                                                                            'disposition_comment_id': 5198021528,
                                                                                            'disposition_required': True,
                                                                                            'gcl_run_id': 31052158986,
                                                                                            'latest_transition_pr': 68,
                                                                                            'material_transition': 'EUCLID_BOOK_VII_HEATH_1908_SOURCE_LOCK_AND_BOUNDED_CONCORDANCE_PROTECTED',
                                                                                            'merge_commit': '49071febcacd9c84fe4ff268d4e11d7e0c4ff0e5',
                                                                                            'protected_head': '49071febcacd9c84fe4ff268d4e11d7e0c4ff0e5',
                                                                                            'review_id': 4869251859,
                                                                                            'reviewed_head': '2d81ace04881a67d0e40083806594813f5459f1e',
                                                                                            'reviewer': 'jimsteeg',
                                                                                            'tracker_issue': 67},
                                                               'grandchallenge/MATHSOLVE': {'core_name': 'Solve checks',
                                                                                            'core_run_id': 31041862799,
                                                                                            'disposition_comment_id': 5196680039,
                                                                                            'disposition_required': True,
                                                                                            'gcl_run_id': 31041863371,
                                                                                            'latest_transition_pr': 104,
                                                                                            'material_transition': 'SOLUTION_WITNESS_AND_DIVISIBILITY_OBSTRUCTION_READY_FOR_CERTIFICATION_PROTECTED',
                                                                                            'merge_commit': '66d54d375ae4dfc148888325b6093818669e7c02',
                                                                                            'protected_head': '66d54d375ae4dfc148888325b6093818669e7c02',
                                                                                            'review_id': 4868150308,
                                                                                            'reviewed_head': 'd4bec98dfea28bb605b3f8c642e18dec697ee4a3',
                                                                                            'reviewer': 'jimsteeg',
                                                                                            'tracker_issue': 103}},
                                              'status': 'COMPLETE_WITH_REPAIRED_P2_AND_NONBLOCKING_OPEN_PR',
                                              'trackers': {('grandchallenge/INTELLECT', 21): ('CURRENT_NAVIGATION_ONLY_AUTOMATED_SECTION_SUCCESSOR_RECEIPT_PENDING',
                                                                                            False,
                                                                                            False),
                                                           ('grandchallenge/MATH-PROGRAMME', 182): ('CURRENT_NAVIGATION_ONLY_AUTOMATED_SECTION_SUCCESSOR_RECEIPT_PENDING',
                                                                                                  False,
                                                                                                  False),
                                                           ('grandchallenge/MATH-PROGRAMME', 183): ('CURRENT_NAVIGATION_ONLY_AUTOMATED_SECTION_SUCCESSOR_RECEIPT_PENDING',
                                                                                                  False,
                                                                                                  False)}}}


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

    sweep_id = record.get("sweep_id")
    expected = EXPECTATIONS.get(str(sweep_id))
    if expected is None:
        errors.append("unsupported sweep identity")
        return errors

    require(record.get("status") == expected["status"], "unexpected sweep status")
    require(record.get("scheduled_due_at") == expected["due"], "scheduled deadline drift")
    require(record.get("next_structural_due_at") == expected["next_due"], "next structural deadline drift")
    require(
        record.get("administrative_review_due_at") == expected["admin_review"],
        "administrative review deadline drift",
    )
    require(record.get("pilot_review_due_at") == expected["pilot_review"], "pilot review deadline drift")
    require(
        record.get("execution_authority") == expected["execution_authority"],
        "execution authority drift",
    )
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
    for field, value in BASELINE_EXPECTED.items():
        require(baseline.get(field) == value, f"baseline reset {field} drift")

    repositories = record.get("scope", {}).get("repositories", [])
    observed = {
        item.get("repository"): item
        for item in repositories
        if isinstance(item, dict) and isinstance(item.get("repository"), str)
    }
    expected_repositories = expected["repositories"]
    require(len(repositories) == 5 and len(observed) == 5, "repository inventory is missing or duplicated")
    require(
        set(observed) == set(expected_repositories),
        "repository inventory differs from the five-repository control scope",
    )

    for repository, repository_expected in expected_repositories.items():
        item = observed.get(repository, {})
        for field in (
            "protected_head",
            "reviewed_head",
            "latest_transition_pr",
            "merge_commit",
            "tracker_issue",
            "material_transition",
        ):
            require(
                item.get(field) == repository_expected[field],
                f"{repository}: {field} drift",
            )

        review = item.get("review", {})
        require(review.get("reviewer") == repository_expected["reviewer"], f"{repository}: reviewer drift")
        require(
            review.get("review_id") == repository_expected["review_id"],
            f"{repository}: review identity drift",
        )
        require(review.get("state") == "APPROVED", f"{repository}: latest transition lacks approved review")
        require(review.get("exact_head") is True, f"{repository}: review is not exact-head")

        disposition = item.get("disposition", {})
        required = repository_expected["disposition_required"]
        require(disposition.get("required") is required, f"{repository}: disposition requirement drift")
        require(
            disposition.get("comment_id") == repository_expected["disposition_comment_id"],
            f"{repository}: disposition identity drift",
        )
        if required:
            require(disposition.get("actor") == "fyremael", f"{repository}: required disposition actor mismatch")
            require(disposition.get("exact_head") is True, f"{repository}: required disposition is not exact-head")
        else:
            require(disposition.get("actor") is None, f"{repository}: non-required disposition actor inflated")
            require(disposition.get("exact_head") is None, f"{repository}: non-required disposition exact-head inflated")

        core = item.get("core_workflow", {})
        gcl = item.get("gcl_workflow", {})
        require(core.get("name") == repository_expected["core_name"], f"{repository}: core workflow name drift")
        require(
            core.get("run_id") == repository_expected["core_run_id"] and core.get("conclusion") == "success",
            f"{repository}: core workflow evidence drift or failure",
        )
        require(gcl.get("name") == "GCL conformance", f"{repository}: GCL workflow name drift")
        require(
            gcl.get("run_id") == repository_expected["gcl_run_id"] and gcl.get("conclusion") == "success",
            f"{repository}: GCL workflow evidence drift or failure",
        )

    open_prs = record.get("scope", {}).get("open_pull_requests", [])
    require(open_prs == expected["open_pull_requests"], "open PR evidence differs from the contemporaneous freeze")
    require(
        all(item.get("merge_authorized") is False for item in open_prs if isinstance(item, dict)),
        "open pull request was falsely authorized",
    )

    trackers = record.get("tracker_mirrors", [])
    observed_trackers = {
        (item.get("repository"), item.get("issue")): item
        for item in trackers
        if isinstance(item, dict)
    }
    expected_trackers = expected["trackers"]
    require(
        len(trackers) == 3 and set(observed_trackers) == set(expected_trackers),
        "canonical tracker inventory is missing or duplicated",
    )
    for key, tracker_expected in expected_trackers.items():
        tracker = observed_trackers.get(key, {})
        expected_state, expected_required, expected_completed = tracker_expected
        require(tracker.get("state_at_freeze") == expected_state, f"{key}: tracker state drift")
        require(tracker.get("repair_required") is expected_required, f"{key}: tracker repair requirement drift")
        require(tracker.get("repair_completed") is expected_completed, f"{key}: tracker repair completion drift")

    findings = record.get("findings", {})
    require(findings.get("P0") == [], "P0 finding prevents closure")
    require(findings.get("P1") == [], "P1 finding prevents closure")
    p2 = findings.get("P2", [])
    p3 = findings.get("P3", [])
    require(len(p2) == expected["p2_count"], "bounded P2 findings were omitted or inflated")
    require(len(p3) == expected["p3_count"], "bounded P3 findings were omitted or inflated")
    require(
        all(
            "REPAIRED" in item.get("disposition", "")
            or "CLARIFIED" in item.get("disposition", "")
            for item in p2
        ),
        "a P2 finding lacks a repaired or clarified disposition",
    )

    readiness = record.get("review_readiness", {})
    require(readiness.get("protected_review_clear_to_proceed") is True, "protected review is not clear to proceed")
    require(readiness.get("circuit_breaker_triggered") is False, "circuit breaker was triggered")
    require(readiness.get("waiver_used") is False, "waiver was used")
    require(readiness.get("emergency_authority_used") is False, "emergency authority was used")
    require(
        readiness.get("pending_manual_processes_at_evidence_freeze") == 0,
        "manual process remained pending at evidence freeze",
    )
    require(
        readiness.get("independent_exact_head_review_required") is True,
        "independent exact-head review gate was removed",
    )
    require(
        readiness.get("human_steward_exact_head_disposition_required") is True,
        "Human Steward disposition gate was removed",
    )

    boundaries = record.get("claim_boundaries", {})
    require(boundaries and all(value is False for value in boundaries.values()), "claim boundary inflation detected")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an administrative structural sweep")
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
