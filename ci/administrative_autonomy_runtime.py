from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from administrative_automation import iso_z, parse_datetime
from autonomy_github import AutonomyError, Client, delete_branch, identity, json_content, required_contexts, wait_checks
from administrative_autonomy_runtime_contract import (
    ALLOWED_REPOSITORIES, ROOT, RUNTIME_PATH,
    build_record, load_json, record_path_for, repository_state,
    validate_activation, validate_record, validate_runtime_contract,
)
from administrative_autonomy_runtime_github import (
    check_runs_state, close_execution_issue, eligible_candidates, exact_head_merge, list_directory_names,
    mark_ready, put_record, record_referee_disposition, update_execution_issue,
    verify_scope, wait_clean, wait_mirror_sync, wait_record_readback,
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
    if repo != runtime["repository"] or os.environ.get("GITHUB_REF") not in {"refs/heads/main", ""}:
        raise AutonomyError("runtime must execute from protected main")

    candidate_identity = identity(
        os.environ.get("CANDIDATE_LOGIN", ""),
        int(os.environ.get("CANDIDATE_APP_ID", "0")),
        "candidate-and-merge-executor",
    )
    administrator_identity = identity(
        os.environ.get("ADMIN_LOGIN", ""),
        int(os.environ.get("CANDIDATE_APP_ID", "0")),
        "ruleset-readback",
    )
    referee_identity = identity(
        os.environ.get("REFEREE_LOGIN", ""),
        int(os.environ.get("REFEREE_APP_ID", "0")),
        "referee",
    )
    if candidate_identity.login != runtime["candidate_identity"]["login"]:
        raise AutonomyError("Candidate runtime identity drift")
    if administrator_identity.login != runtime["administrator_identity"]["login"]:
        raise AutonomyError("Administration runtime identity drift")
    if referee_identity.login != runtime["referee_identity"]["login"]:
        raise AutonomyError("Referee runtime identity drift")
    if candidate_identity.app_id == referee_identity.app_id or candidate_identity.login == referee_identity.login:
        raise AutonomyError("Candidate and Referee identities are not separate")

    candidate = Client(os.environ.get("CANDIDATE_TOKEN", ""))
    referee = Client(os.environ.get("REFEREE_TOKEN", ""))
    administrator = Client(os.environ.get("ADMIN_TOKEN", ""))
    evidence = Client(os.environ.get("EVIDENCE_TOKEN", ""))
    observability = Client(os.environ.get("OBSERVABILITY_TOKEN", ""))
    now = datetime.now(UTC)
    eligible = eligible_candidates(candidate, repo, runtime, now)
    if not eligible:
        report = {
            "schema_version": "1.0.0",
            "state": "NO_ELIGIBLE_FROZEN_CANDIDATE",
            "evaluated_at": iso_z(now),
            "activation_state": activation["state"],
            "authority_created": False,
        }
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 0
    if len(eligible) != 1:
        raise AutonomyError("multiple frozen maintenance candidates require fail-closed triage")

    pull, manifest = eligible[0]
    pr = int(pull["number"])
    branch = manifest["branch"]
    issue = int(manifest["issue_number"])
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "state": "AUTONOMOUS_RUNTIME_STARTED",
        "evaluated_at": iso_z(now),
        "candidate_pull_request": pr,
        "candidate_issue": issue,
        "candidate_branch": branch,
        "authority_created": False,
    }
    try:
        layout = runtime["record_layout"][manifest["procedure_id"]]
        existing_names = list_directory_names(candidate, repo, layout["directory"])
        record_id, record_path = record_path_for(runtime, manifest, existing_names)
        existing_record = json_content(candidate, repo, record_path, branch)
        if existing_record:
            record = existing_record
            errors = validate_record(record)
            if errors:
                raise AutonomyError("; ".join(errors))
            final_head = pull["head"]["sha"]
        else:
            state = repository_state(evidence, sorted(ALLOWED_REPOSITORIES))
            record = build_record(runtime, activation, manifest, record_id, state, now)
            errors = validate_record(record)
            if errors:
                raise AutonomyError("; ".join(errors))
            final_head = put_record(candidate, repo, branch, record_path, record)

        updated = candidate.patch(
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
        if updated.get("head", {}).get("sha") != final_head:
            raise AutonomyError("finalized maintenance head readback mismatch")
        if updated.get("draft") is True:
            mark_ready(candidate, updated["node_id"])
        verify_scope(candidate, repo, pr, manifest["manifest_path"], record_path, runtime["scope"])
        update_execution_issue(
            candidate,
            repo,
            issue,
            manifest,
            record_id,
            final_head,
        )

        live_ruleset = administrator.get(f"/repos/{repo}/rulesets/{runtime['ruleset_id']}")
        expected_actor = {
            "actor_id": runtime["administrator_identity"]["app_id"],
            "actor_type": "Integration",
            "bypass_mode": "pull_request",
        }
        actors = [
            {
                "actor_id": int(item["actor_id"]),
                "actor_type": item["actor_type"],
                "bypass_mode": item["bypass_mode"],
            }
            for item in live_ruleset.get("bypass_actors", [])
        ]
        if expected_actor not in actors:
            raise AutonomyError("live pull-request-only Administration actor is absent")
        contexts = required_contexts(live_ruleset)
        checks = wait_checks(referee, repo, final_head, contexts, int(runtime["merge_control"]["maximum_check_wait_seconds"]))
        disposition = record_referee_disposition(
            referee,
            repo,
            pr,
            final_head,
            record_id,
            checks,
            referee_identity.login,
        )
        disposition_at = time.monotonic()
        post_checks = wait_clean(
            candidate,
            referee,
            repo,
            updated["node_id"],
            final_head,
            referee_identity.login,
            contexts,
            runtime["merge_control"],
            disposition_at,
        )
        merged = exact_head_merge(candidate, repo, pr, final_head, record_id, candidate_identity.login)
        merge_sha = str(merged["merge_commit_sha"])
        wait_record_readback(
            candidate,
            repo,
            record_path,
            record,
            int(runtime["merge_control"]["maximum_protected_readback_wait_seconds"]),
            int(runtime["merge_control"]["poll_interval_seconds"]),
        )
        ruleset_after = administrator.get(f"/repos/{repo}/rulesets/{runtime['ruleset_id']}")
        actors_after = [
            {
                "actor_id": int(item["actor_id"]),
                "actor_type": item["actor_type"],
                "bypass_mode": item["bypass_mode"],
            }
            for item in ruleset_after.get("bypass_actors", [])
        ]
        if actors_after != actors:
            raise AutonomyError("ruleset changed during autonomous maintenance execution")
        sync_run = wait_mirror_sync(
            observability,
            evidence,
            repo,
            merge_sha,
            manifest["procedure_id"],
            iso_z(parse_datetime(manifest["scheduled_due_at"])),
            runtime,
        )
        readback = referee.post(
            f"/repos/{repo}/issues/{pr}/comments",
            {
                "body": (
                    "REFEREE_AGENT_PROTECTED_ADMINISTRATIVE_READBACK_COMPLETE\n\n"
                    f"- record: `{record_id}`;\n"
                    f"- exact approved head: `{final_head}`;\n"
                    f"- disposition comment ID: `{disposition['id']}`;\n"
                    f"- protected merge commit: `{merge_sha}`;\n"
                    f"- mirror synchronization run: `{sync_run}`;\n"
                    f"- ruleset: `{runtime['ruleset_id']}`;\n"
                    "- Candidate/Referee/merge actor separation: verified;\n"
                    "- bypass used: `false`;\n"
                    "- Human Steward identity asserted: `false`;\n"
                    "- mathematical or certification authority asserted: `false`."
                )
            },
        )
        if readback.get("user", {}).get("login") != referee_identity.login:
            raise AutonomyError("protected readback actor mismatch")
        close_execution_issue(
            candidate,
            repo,
            issue,
            manifest,
            record_id,
            final_head,
            merge_sha,
            int(disposition["id"]),
            int(readback["id"]),
            sync_run,
        )
        delete_branch(candidate, repo, branch)
        report |= {
            "state": "ACTIVE_AUTONOMOUS_PROTECTED_READBACK_COMPLETE",
            "completed_at": iso_z(datetime.now(UTC)),
            "record_id": record_id,
            "record_path": record_path,
            "candidate_head": final_head,
            "required_checks": checks,
            "post_disposition_checks": post_checks,
            "referee_disposition_comment_id": int(disposition["id"]),
            "protected_merge_commit": merge_sha,
            "protected_readback_comment_id": int(readback["id"]),
            "mirror_synchronization_run": sync_run,
            "ruleset_id": runtime["ruleset_id"],
            "ruleset_bypass_actors": actors_after,
            "bypass_used": False,
            "candidate_actor": candidate_identity.login,
            "referee_actor": referee_identity.login,
            "merge_actor": candidate_identity.login,
            "human_steward_identity_asserted": False,
            "authority_created": True,
            "claim_boundaries": runtime["claim_boundaries"],
        }
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 0
    except Exception as exc:
        report |= {
            "state": "AUTONOMOUS_RUNTIME_FAILED_CLOSED",
            "failed_at": iso_z(datetime.now(UTC)),
            "error": str(exc),
            "authority_created": False,
            "merge_performed": False,
            "human_steward_identity_asserted": False,
        }
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        try:
            candidate.post(
                f"/repos/{repo}/issues/{issue}/comments",
                {
                    "body": (
                        "AUTONOMOUS_ADMINISTRATIVE_RUNTIME_FAILED_CLOSED\n\n"
                        f"- pull request: `#{pr}`;\n"
                        f"- branch: `{branch}`;\n"
                        f"- error: `{str(exc)[:1000]}`;\n"
                        "- merge performed: `false`;\n"
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
