from __future__ import annotations

import os
from typing import Any

from administrative_automation import iso_z, parse_datetime
from autonomy_github import AutonomyError, Client, delete_branch, identity
from administrative_autonomy_runtime_github import close_execution_issue, wait_mirror_sync
from administrative_autonomy_receipt_stage import stage_completion_receipt


def runtime_identities(runtime: dict[str, Any]) -> tuple[Any, Any, Any]:
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
    if (
        candidate_identity.app_id == referee_identity.app_id
        or candidate_identity.login == referee_identity.login
    ):
        raise AutonomyError("Candidate and Referee identities are not separate")
    return candidate_identity, administrator_identity, referee_identity


def ruleset_actors(administrator: Client, repo: str, runtime: dict[str, Any]) -> list[dict[str, Any]]:
    live = administrator.get(f"/repos/{repo}/rulesets/{runtime['ruleset_id']}")
    expected = {
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
        for item in live.get("bypass_actors", [])
    ]
    if expected not in actors:
        raise AutonomyError("live pull-request-only Administration actor is absent")
    return actors


def post_protected_readback(
    referee: Client,
    repo: str,
    pull_request: int,
    referee_login: str,
    record_id: str,
    exact_head: str,
    record_disposition_id: int,
    record_merge_sha: str,
    receipt: dict[str, Any],
    mirror_run: int,
    runtime: dict[str, Any],
) -> dict[str, Any]:
    readback = referee.post(
        f"/repos/{repo}/issues/{pull_request}/comments",
        {
            "body": (
                "REFEREE_AGENT_PROTECTED_ADMINISTRATIVE_READBACK_COMPLETE\n\n"
                f"- record: `{record_id}`;\n"
                f"- exact approved record head: `{exact_head}`;\n"
                f"- record disposition comment ID: `{record_disposition_id}`;\n"
                f"- protected record merge commit: `{record_merge_sha}`;\n"
                f"- completion receipt pull request: `{receipt.get('receipt_pull_request')}`;\n"
                f"- completion receipt head: `{receipt.get('receipt_head')}`;\n"
                f"- completion receipt disposition comment ID: `{receipt.get('receipt_disposition_comment_id')}`;\n"
                f"- protected completion receipt merge: `{receipt['receipt_merge_commit']}`;\n"
                f"- mirror synchronization run: `{mirror_run}`;\n"
                f"- ruleset: `{runtime['ruleset_id']}`;\n"
                "- Candidate/Referee/merge actor separation: verified;\n"
                "- bypass used: `false`;\n"
                "- Human Steward identity asserted: `false`;\n"
                "- mathematical or certification authority asserted: `false`."
            )
        },
    )
    if readback.get("user", {}).get("login") != referee_login:
        raise AutonomyError("protected readback actor mismatch")
    return readback


def finish_closure(
    candidate: Client,
    referee: Client,
    administrator: Client,
    observability: Client,
    evidence: Client,
    repo: str,
    runtime: dict[str, Any],
    actors_before: list[dict[str, Any]],
    item: dict[str, Any],
    candidate_login: str,
    referee_login: str,
) -> dict[str, Any]:
    manifest = item["manifest"]
    receipt = stage_completion_receipt(
        candidate,
        referee,
        administrator,
        repo,
        runtime,
        item["record_id"],
        str(manifest["procedure_id"]),
        str(manifest["scheduled_due_at"]),
        item["record_path"],
        item["record"],
        int(item["pull_request"]),
        item["exact_head"],
        item["record_merge_commit"],
        referee_login,
        candidate_login,
    )
    actors_after = ruleset_actors(administrator, repo, runtime)
    if actors_after != actors_before:
        raise AutonomyError("ruleset changed during autonomous maintenance execution")
    mirror_run = wait_mirror_sync(
        observability,
        evidence,
        repo,
        str(receipt["receipt_merge_commit"]),
        str(manifest["procedure_id"]),
        iso_z(parse_datetime(str(manifest["scheduled_due_at"]))),
        runtime,
    )
    readback = post_protected_readback(
        referee,
        repo,
        int(item["pull_request"]),
        referee_login,
        item["record_id"],
        item["exact_head"],
        int(item["record_disposition_comment_id"]),
        item["record_merge_commit"],
        receipt,
        mirror_run,
        runtime,
    )
    close_execution_issue(
        candidate,
        repo,
        int(item["issue_number"]),
        manifest,
        item["record_id"],
        item["exact_head"],
        item["record_merge_commit"],
        int(item["record_disposition_comment_id"]),
        int(readback["id"]),
        mirror_run,
    )
    try:
        delete_branch(candidate, repo, str(manifest["branch"]))
    except AutonomyError as exc:
        if " 422 " not in str(exc) and " 404 " not in str(exc):
            raise
    return {
        **receipt,
        "protected_readback_comment_id": int(readback["id"]),
        "mirror_synchronization_run": mirror_run,
        "ruleset_bypass_actors": actors_after,
    }
