from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from administrative_automation import iso_z
from autonomy_github import AutonomyError, Client, json_content, required_contexts, wait_checks
from administrative_autonomy_runtime_contract import (
    ALLOWED_REPOSITORIES, ROOT, RUNTIME_PATH, build_record, load_json,
    record_path_for, repository_state, validate_activation, validate_record,
    validate_runtime_contract,
)
from administrative_autonomy_runtime_github import (
    eligible_candidates, exact_head_merge, list_directory_names, mark_ready,
    put_record, record_referee_disposition, update_execution_issue,
    verify_scope, wait_clean, wait_record_readback,
)
from administrative_autonomy_receipt_stage import pending_closures, wait_pull_head
from administrative_autonomy_runtime_control import (
    finish_closure, ruleset_actors, runtime_identities,
)

REPORT_PATH = ROOT / "administrative-autonomy-runtime-report.json"
UTC = timezone.utc


def validate_command() -> int:
    runtime = load_json(RUNTIME_PATH)
    activation = load_json(ROOT / runtime["activation_record"])
    errors = validate_runtime_contract(runtime) + validate_activation(runtime, activation)
    if errors:
        for error in errors:
            print(error)
        return 1
    print("administrative autonomy runtime integration: valid")
    return 0


def execute(report_path: Path) -> int:
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
        raise AutonomyError("runtime must execute from protected main")

    candidate_identity, _, referee_identity = runtime_identities(runtime)
    candidate = Client(os.environ.get("CANDIDATE_TOKEN", ""))
    referee = Client(os.environ.get("REFEREE_TOKEN", ""))
    administrator = Client(os.environ.get("ADMIN_TOKEN", ""))
    evidence = Client(os.environ.get("EVIDENCE_TOKEN", ""))
    observability = Client(os.environ.get("OBSERVABILITY_TOKEN", ""))
    actors_before = ruleset_actors(administrator, repo, runtime)
    now = datetime.now(UTC)

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "state": "AUTONOMOUS_RUNTIME_STARTED",
        "evaluated_at": iso_z(now),
        "authority_created": False,
        "merge_performed": False,
        "human_steward_identity_asserted": False,
    }
    issue = 0
    pr = 0
    branch = ""
    record_merge_performed = False
    record_merge_sha = ""
    try:
        recoveries = pending_closures(
            candidate, repo, runtime, referee_identity.login
        )
        if len(recoveries) > 1:
            raise AutonomyError(
                "multiple protected maintenance closures require fail-closed triage"
            )
        if recoveries:
            item = recoveries[0]
            issue = int(item["issue_number"])
            pr = int(item["pull_request"])
            branch = str(item["manifest"]["branch"])
            record_merge_performed = True
            record_merge_sha = str(item["record_merge_commit"])
            report |= {
                "state": "AUTONOMOUS_PROTECTED_CLOSURE_RECOVERY_STARTED",
                "candidate_pull_request": pr,
                "candidate_issue": issue,
                "candidate_branch": branch,
                "record_id": item["record_id"],
                "candidate_head": item["exact_head"],
                "protected_record_merge_commit": record_merge_sha,
                "record_merge_performed": True,
            }
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
                "state": "ACTIVE_AUTONOMOUS_PROTECTED_READBACK_RECOVERED",
                "completed_at": iso_z(datetime.now(UTC)),
                "completion_receipt": closure["receipt"],
                "receipt_pull_request": closure["receipt_pull_request"],
                "receipt_head": closure["receipt_head"],
                "receipt_disposition_comment_id": closure[
                    "receipt_disposition_comment_id"
                ],
                "protected_completion_receipt_merge": closure[
                    "receipt_merge_commit"
                ],
                "protected_readback_comment_id": closure[
                    "protected_readback_comment_id"
                ],
                "mirror_synchronization_run": closure[
                    "mirror_synchronization_run"
                ],
                "ruleset_id": runtime["ruleset_id"],
                "ruleset_bypass_actors": closure["ruleset_bypass_actors"],
                "bypass_used": False,
                "candidate_actor": candidate_identity.login,
                "referee_actor": referee_identity.login,
                "merge_actor": candidate_identity.login,
                "merge_performed": True,
                "authority_created": True,
                "claim_boundaries": runtime["claim_boundaries"],
            }
            report_path.write_text(
                json.dumps(report, indent=2) + "\n", encoding="utf-8"
            )
            print(json.dumps(report, indent=2))
            return 0

        eligible = eligible_candidates(candidate, repo, runtime, now)
        if not eligible:
            report |= {
                "state": "NO_ELIGIBLE_FROZEN_CANDIDATE",
                "activation_state": activation["state"],
            }
            report_path.write_text(
                json.dumps(report, indent=2) + "\n", encoding="utf-8"
            )
            print(json.dumps(report, indent=2))
            return 0
        if len(eligible) != 1:
            raise AutonomyError(
                "multiple frozen maintenance candidates require fail-closed triage"
            )

        pull, manifest = eligible[0]
        pr = int(pull["number"])
        branch = str(manifest["branch"])
        issue = int(manifest["issue_number"])
        report |= {
            "candidate_pull_request": pr,
            "candidate_issue": issue,
            "candidate_branch": branch,
        }

        layout = runtime["record_layout"][manifest["procedure_id"]]
        existing_names = list_directory_names(
            candidate, repo, layout["directory"]
        )
        record_id, record_path = record_path_for(
            runtime, manifest, existing_names
        )
        existing_record = json_content(candidate, repo, record_path, branch)
        if existing_record:
            record = existing_record
            errors = validate_record(record)
            if errors:
                raise AutonomyError("; ".join(errors))
            final_head = str(pull["head"]["sha"])
        else:
            state = repository_state(
                evidence, sorted(ALLOWED_REPOSITORIES)
            )
            record = build_record(
                runtime, activation, manifest, record_id, state, now
            )
            errors = validate_record(record)
            if errors:
                raise AutonomyError("; ".join(errors))
            final_head = put_record(
                candidate, repo, branch, record_path, record
            )

        candidate.patch(
            f"/repos/{repo}/pulls/{pr}",
            {
                "title": f"{runtime['scope']['final_title_prefix']} {record_id}",
                "body": (
                    f"Finalizes bounded autonomous administrative record `{record_id}` for issue #{issue}.\n\n"
                    f"- occurrence: `{manifest['occurrence_key']}`;\n"
                    f"- exact head after finalization: `{final_head}`;\n"
                    f"- protected activation: `{activation['activation_id']}` / `{activation['state']}`;\n"
                    "- Candidate and merge executor: `gcl-release-trust[bot]`;\n"
                    "- Referee: `github-actions[bot]`;\n"
                    "- Human Steward disposition: not required and not asserted;\n"
                    "- bypass exercise: prohibited;\n"
                    "- mathematical and certification authority: excluded."
                ),
                "maintainer_can_modify": False,
            },
        )
        updated = wait_pull_head(
            candidate,
            repo,
            pr,
            final_head,
            int(runtime["merge_control"]["maximum_stabilization_wait_seconds"]),
            int(runtime["merge_control"]["poll_interval_seconds"]),
        )
        if updated.get("draft") is True:
            mark_ready(candidate, str(updated["node_id"]))
        verify_scope(
            candidate,
            repo,
            pr,
            manifest["manifest_path"],
            record_path,
            runtime["scope"],
        )
        update_execution_issue(
            candidate, repo, issue, manifest, record_id, final_head
        )

        live_ruleset = administrator.get(
            f"/repos/{repo}/rulesets/{runtime['ruleset_id']}"
        )
        contexts = required_contexts(live_ruleset)
        checks = wait_checks(
            referee,
            repo,
            final_head,
            contexts,
            int(runtime["merge_control"]["maximum_check_wait_seconds"]),
        )
        disposition = record_referee_disposition(
            referee,
            repo,
            pr,
            final_head,
            record_id,
            checks,
            referee_identity.login,
        )
        post_checks = wait_clean(
            candidate,
            referee,
            repo,
            str(updated["node_id"]),
            final_head,
            referee_identity.login,
            contexts,
            runtime["merge_control"],
            time.monotonic(),
        )
        merged = exact_head_merge(
            candidate,
            repo,
            pr,
            final_head,
            record_id,
            candidate_identity.login,
        )
        record_merge_performed = True
        record_merge_sha = str(merged["merge_commit_sha"])
        report |= {
            "record_merge_performed": True,
            "merge_performed": True,
            "protected_record_merge_commit": record_merge_sha,
        }
        wait_record_readback(
            candidate,
            repo,
            record_path,
            record,
            int(runtime["merge_control"]["maximum_protected_readback_wait_seconds"]),
            int(runtime["merge_control"]["poll_interval_seconds"]),
        )
        item = {
            "manifest": manifest,
            "record": record,
            "record_id": record_id,
            "record_path": record_path,
            "issue_number": issue,
            "pull_request": pr,
            "exact_head": final_head,
            "record_merge_commit": record_merge_sha,
            "record_disposition_comment_id": int(disposition["id"]),
        }
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
            "state": "ACTIVE_AUTONOMOUS_PROTECTED_READBACK_COMPLETE",
            "completed_at": iso_z(datetime.now(UTC)),
            "record_id": record_id,
            "record_path": record_path,
            "candidate_head": final_head,
            "required_checks": checks,
            "post_disposition_checks": post_checks,
            "referee_disposition_comment_id": int(disposition["id"]),
            "protected_record_merge_commit": record_merge_sha,
            "completion_receipt": closure["receipt"],
            "receipt_pull_request": closure["receipt_pull_request"],
            "receipt_head": closure["receipt_head"],
            "receipt_required_checks": closure.get("receipt_checks"),
            "receipt_post_disposition_checks": closure.get(
                "receipt_post_disposition_checks"
            ),
            "receipt_disposition_comment_id": closure[
                "receipt_disposition_comment_id"
            ],
            "protected_completion_receipt_merge": closure[
                "receipt_merge_commit"
            ],
            "protected_readback_comment_id": closure[
                "protected_readback_comment_id"
            ],
            "mirror_synchronization_run": closure[
                "mirror_synchronization_run"
            ],
            "ruleset_id": runtime["ruleset_id"],
            "ruleset_bypass_actors": closure["ruleset_bypass_actors"],
            "bypass_used": False,
            "candidate_actor": candidate_identity.login,
            "referee_actor": referee_identity.login,
            "merge_actor": candidate_identity.login,
            "human_steward_identity_asserted": False,
            "merge_performed": True,
            "authority_created": True,
            "claim_boundaries": runtime["claim_boundaries"],
        }
        report_path.write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        print(json.dumps(report, indent=2))
        return 0
    except Exception as exc:
        report |= {
            "state": "AUTONOMOUS_RUNTIME_FAILED_CLOSED",
            "failed_at": iso_z(datetime.now(UTC)),
            "error": str(exc),
            "authority_created": False,
            "merge_performed": record_merge_performed,
            "record_merge_performed": record_merge_performed,
            "protected_record_merge_commit": record_merge_sha or None,
            "human_steward_identity_asserted": False,
        }
        report_path.write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        if issue:
            try:
                candidate.post(
                    f"/repos/{repo}/issues/{issue}/comments",
                    {
                        "body": (
                            "AUTONOMOUS_ADMINISTRATIVE_RUNTIME_FAILED_CLOSED\n\n"
                            f"- pull request: `#{pr}`;\n"
                            f"- branch: `{branch}`;\n"
                            f"- error: `{str(exc)[:1000]}`;\n"
                            f"- protected record merge performed: `{str(record_merge_performed).lower()}`;\n"
                            f"- protected record merge commit: `{record_merge_sha or 'none'}`;\n"
                            "- Human Steward identity asserted: `false`;\n"
                            "- manual or successor automated triage required."
                        )
                    },
                )
            except Exception:
                pass
        print(json.dumps(report, indent=2))
        raise


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    execute_parser = sub.add_parser("execute")
    execute_parser.add_argument("--report", type=Path, default=REPORT_PATH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.command == "validate":
        return validate_command()
    return execute(args.report)


if __name__ == "__main__":
    raise SystemExit(main())
