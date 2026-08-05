from __future__ import annotations

import argparse
import hashlib
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
REPOSITORIES = {
    "grandchallenge/MATH-PROGRAMME",
    "grandchallenge/MATHFORGE",
    "grandchallenge/MATHSOLVE",
    "grandchallenge/MATHCERT",
    "grandchallenge/INTELLECT",
}
EXPECTED = {
    "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-006": {
        "blob_sha": "88a910b944470e2d4e87a4d8d2b34c22b137821c",
        "status": "COMPLETE_WITH_REPAIRED_P2_AND_NONBLOCKING_OPEN_PR",
        "due": "2026-08-04T23:09:00-07:00",
        "next_due": "2026-08-05T15:57:00-07:00",
        "p2_count": 2,
        "p3_count": 1,
    },
    "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007": {
        "blob_sha": "51db3bc72c8f371ace530ad5ce11322cd6af326c",
        "status": "COMPLETE_WITH_REPAIRED_P2_AND_NONBLOCKING_OPEN_PR",
        "due": "2026-08-05T15:57:00-07:00",
        "next_due": "2026-08-06T08:45:00-07:00",
        "p2_count": 3,
        "p3_count": 1,
    },
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(record: dict[str, Any]) -> str:
    payload = (json.dumps(record, indent=2) + "\n").encode("utf-8")
    header = f"blob {len(payload)}\0".encode("ascii")
    return hashlib.sha1(header + payload).hexdigest()


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

    sweep_id = str(record.get("sweep_id", ""))
    expected = EXPECTED.get(sweep_id)
    if expected is None:
        errors.append("unsupported sweep identity")
        return errors

    require(git_blob_sha(record) == expected["blob_sha"], "immutable sweep record digest drift")
    require(record.get("status") == expected["status"], "unexpected sweep status")
    require(record.get("scheduled_due_at") == expected["due"], "scheduled deadline drift")
    require(record.get("next_structural_due_at") == expected["next_due"], "next structural deadline drift")
    require(record.get("evidence_mode") == "CONTEMPORANEOUS", "evidence is not contemporaneous")
    require(record.get("cadence") == "PT16H48M", "cadence changed")
    require(record.get("lateness_minutes_at_start") == 0, "on-time start is not recorded exactly")

    try:
        due = datetime.fromisoformat(record["scheduled_due_at"])
        started = datetime.fromisoformat(record["execution_started_at"])
        closed = datetime.fromisoformat(record["evidence_closed_at"])
        next_due = datetime.fromisoformat(record["next_structural_due_at"])
        require(started <= closed <= due, "contemporaneous evidence window is outside the locus")
        require(next_due - due == timedelta(hours=16, minutes=48), "PT16H48M cadence is not preserved")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"invalid sweep chronology: {exc}")

    baseline = record.get("baseline_reset", {})
    require(baseline.get("cadence_anchor_reset") is False, "cadence anchor was reset")
    require(baseline.get("implementation_commits_discarded") == 0, "implementation commits were discarded")
    require(baseline.get("pending_manual_processes_at_reset") == 0, "manual process remained pending at reset")

    repositories = record.get("scope", {}).get("repositories", [])
    names = [item.get("repository") for item in repositories if isinstance(item, dict)]
    require(len(repositories) == 5 and set(names) == REPOSITORIES, "five-repository inventory drift")
    require(len(names) == len(set(names)), "repository inventory is duplicated")
    for item in repositories:
        if not isinstance(item, dict):
            continue
        repository = item.get("repository", "unknown")
        review = item.get("review", {})
        disposition = item.get("disposition", {})
        core = item.get("core_workflow", {})
        gcl = item.get("gcl_workflow", {})
        require(review.get("state") == "APPROVED", f"{repository}: transition review is not approved")
        require(review.get("exact_head") is True, f"{repository}: transition review is not exact-head")
        require(core.get("conclusion") == "success", f"{repository}: core workflow did not succeed")
        require(gcl.get("name") == "GCL conformance", f"{repository}: GCL workflow name drift")
        require(gcl.get("conclusion") == "success", f"{repository}: GCL workflow did not succeed")
        if disposition.get("required") is True:
            require(disposition.get("actor") == "fyremael", f"{repository}: disposition actor mismatch")
            require(disposition.get("exact_head") is True, f"{repository}: disposition is not exact-head")
        else:
            require(disposition.get("comment_id") is None, f"{repository}: non-required disposition inflated")
            require(disposition.get("actor") is None, f"{repository}: non-required disposition actor inflated")
            require(disposition.get("exact_head") is None, f"{repository}: non-required exact-head disposition inflated")

    open_prs = record.get("scope", {}).get("open_pull_requests", [])
    require(
        all(isinstance(item, dict) and item.get("merge_authorized") is False for item in open_prs),
        "an open pull request was falsely merge-authorized",
    )

    trackers = record.get("tracker_mirrors", [])
    tracker_keys = {
        (item.get("repository"), item.get("issue"))
        for item in trackers
        if isinstance(item, dict)
    }
    require(
        len(trackers) == 3
        and tracker_keys
        == {
            ("grandchallenge/MATH-PROGRAMME", 182),
            ("grandchallenge/MATH-PROGRAMME", 183),
            ("grandchallenge/INTELLECT", 21),
        },
        "canonical tracker inventory drift",
    )

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
            if isinstance(item, dict)
        ),
        "a P2 finding lacks a repaired or clarified disposition",
    )

    readiness = record.get("review_readiness", {})
    require(readiness.get("protected_review_clear_to_proceed") is True, "protected review is not clear")
    require(readiness.get("circuit_breaker_triggered") is False, "circuit breaker was triggered")
    require(readiness.get("waiver_used") is False, "waiver was used")
    require(readiness.get("emergency_authority_used") is False, "emergency authority was used")
    require(readiness.get("pending_manual_processes_at_evidence_freeze") == 0, "manual process remained pending")
    require(readiness.get("independent_exact_head_review_required") is True, "independent review gate removed")
    require(readiness.get("human_steward_exact_head_disposition_required") is True, "Steward gate removed")

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
