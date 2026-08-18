from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Import the protected runtime entry first. This installs all durable receipt and
# recovery overlays before the executor/control modules capture their callables.
import administrative_autonomy_runtime  # noqa: F401
import administrative_autonomy_runtime_execute as runtime_execute
from administrative_automation import iso_z
from administrative_autonomy_runtime_contract import (
    ROOT,
    RUNTIME_PATH,
    load_json,
    validate_activation,
    validate_runtime_contract,
)
from administrative_autonomy_runtime_control import (
    finish_closure,
    ruleset_actors,
    runtime_identities,
)
from autonomy_github import AutonomyError, Client

UTC = timezone.utc
DEFAULT_REPORT = ROOT / "administrative-autonomy-0813-closure-preflight.json"
TARGET = {
    "issue_number": 475,
    "pull_request": 476,
    "record_id": "MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-13-001",
    "occurrence_key": "administrative_review:2026-08-13T01:21:00Z",
    "procedure_id": "administrative_review",
    "scheduled_due_at": "2026-08-13T01:21:00Z",
    "exact_head": "1eb3c2cf8375beecc6d84d788ac891402b33757f",
    "record_merge_commit": "7c84b9bf19a1f3e2407860d82965e98fc49512db",
}


def is_exact_target(item: dict[str, Any]) -> bool:
    manifest = item.get("manifest", {})
    return (
        int(item.get("issue_number") or 0) == TARGET["issue_number"]
        and int(item.get("pull_request") or 0) == TARGET["pull_request"]
        and str(item.get("record_id") or "") == TARGET["record_id"]
        and str(item.get("exact_head") or "") == TARGET["exact_head"]
        and str(item.get("record_merge_commit") or "")
        == TARGET["record_merge_commit"]
        and str(manifest.get("occurrence_key") or "") == TARGET["occurrence_key"]
        and str(manifest.get("procedure_id") or "") == TARGET["procedure_id"]
        and str(manifest.get("scheduled_due_at") or "")
        == TARGET["scheduled_due_at"]
    )


def write_report(path: Path, report: dict[str, Any]) -> None:
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


def recover_exact_aug13(report_path: Path) -> int:
    runtime = load_json(RUNTIME_PATH)
    activation = load_json(ROOT / runtime["activation_record"])
    errors = validate_runtime_contract(runtime) + validate_activation(runtime, activation)
    if errors:
        raise AutonomyError("; ".join(errors))

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if repo != runtime["repository"] or os.environ.get("GITHUB_REF") not in {
        "refs/heads/main",
        "",
    }:
        raise AutonomyError("Aug13 closure preflight must execute from protected main")

    candidate_identity, _, referee_identity = runtime_identities(runtime)
    candidate = Client(os.environ.get("CANDIDATE_TOKEN", ""))
    referee = Client(os.environ.get("REFEREE_TOKEN", ""))
    administrator = Client(os.environ.get("ADMIN_TOKEN", ""))
    evidence = Client(os.environ.get("EVIDENCE_TOKEN", ""))
    observability = Client(os.environ.get("OBSERVABILITY_TOKEN", ""))

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "control": "MP-ADMIN-ADMINISTRATIVE-0813-RECEIPT-RECOVERY-001",
        "state": "AUG13_CLOSURE_PREFLIGHT_STARTED",
        "evaluated_at": iso_z(datetime.now(UTC)),
        "exact_target_only": True,
        "ordinary_candidate_execution_allowed": False,
        "recovered": False,
        "authority_created": False,
        "human_steward_identity_asserted": False,
        "bypass_used": False,
    }
    issue = 0
    try:
        recoveries = runtime_execute.pending_closures(
            candidate,
            repo,
            runtime,
            referee_identity.login,
        )
        targets = [item for item in recoveries if is_exact_target(item)]
        if not targets:
            report |= {
                "state": "AUG13_CLOSURE_PREFLIGHT_NO_TARGET",
                "observed_pending_closure_count": len(recoveries),
            }
            write_report(report_path, report)
            return 0
        if len(recoveries) != 1 or len(targets) != 1:
            raise AutonomyError(
                "Aug13 closure preflight requires the exact target to be the sole pending closure"
            )

        item = targets[0]
        issue = int(item["issue_number"])
        actors_before = ruleset_actors(administrator, repo, runtime)
        closure = finish_closure(
            candidate,
            referee,
            administrator,
            observability,
            evidence,
            repo,
            runtime,
            actors_before,
            item,
            candidate_identity.login,
            referee_identity.login,
        )
        report |= {
            "state": "AUG13_CLOSURE_PREFLIGHT_PROTECTED_COMPLETE",
            "completed_at": iso_z(datetime.now(UTC)),
            "recovered": True,
            "authority_created": True,
            "candidate_issue": issue,
            "candidate_pull_request": int(item["pull_request"]),
            "record_id": item["record_id"],
            "record_head": item["exact_head"],
            "record_merge_commit": item["record_merge_commit"],
            "completion_receipt": closure["receipt"],
            "receipt_pull_request": closure["receipt_pull_request"],
            "receipt_head": closure["receipt_head"],
            "receipt_disposition_comment_id": closure[
                "receipt_disposition_comment_id"
            ],
            "receipt_merge_commit": closure["receipt_merge_commit"],
            "protected_readback_comment_id": closure[
                "protected_readback_comment_id"
            ],
            "mirror_synchronization_run": closure["mirror_synchronization_run"],
            "ruleset_bypass_actors": closure["ruleset_bypass_actors"],
            "candidate_actor": candidate_identity.login,
            "referee_actor": referee_identity.login,
            "claim_boundaries": runtime["claim_boundaries"],
        }
        write_report(report_path, report)
        return 0
    except Exception as exc:
        report |= {
            "state": "AUG13_CLOSURE_PREFLIGHT_FAILED_CLOSED",
            "failed_at": iso_z(datetime.now(UTC)),
            "error": str(exc),
            "recovered": False,
            "authority_created": False,
        }
        write_report(report_path, report)
        if issue:
            try:
                candidate.post(
                    f"/repos/{repo}/issues/{issue}/comments",
                    {
                        "body": (
                            "AUG13_CLOSURE_PREFLIGHT_FAILED_CLOSED\n\n"
                            f"- issue: `#{issue}`;\n"
                            f"- error: `{str(exc)[:1000]}`;\n"
                            "- protected completion receipt merge performed: `false`;\n"
                            "- ordinary candidate execution authorized: `false`;\n"
                            "- Human Steward identity asserted: `false`;\n"
                            "- manual or successor controlled triage required."
                        )
                    },
                )
            except Exception:
                pass
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.apply:
        raise AutonomyError("Aug13 closure preflight requires --apply")
    return recover_exact_aug13(args.report)


if __name__ == "__main__":
    raise SystemExit(main())
