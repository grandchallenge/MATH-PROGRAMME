#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from jsonschema import Draft202012Validator

from autonomy_github import AutonomyError, Client, required_contexts

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = ROOT / "governance/administrative_autonomy_low_friction_control.json"
CONTROL_SCHEMA_PATH = ROOT / "schemas/administrative_autonomy_low_friction_control.schema.json"
EXPECTED_CONTROL_ID = "MP-ADMIN-LOW-FRICTION-001"
EXPECTED_REPOSITORY = "grandchallenge/MATH-PROGRAMME"
EXPECTED_ISSUE = 633
EXPECTED_AUTHORIZATION_COMMENT_ID = 5362883052
EXPECTED_CANDIDATE_LOGIN = "gcl-release-trust[bot]"
EXPECTED_CANDIDATE_APP_ID = 4423678
EXPECTED_REFEREE_LOGIN = "github-actions[bot]"
EXPECTED_REFEREE_APP_ID = 15368
EXPECTED_RULESET_ID = 17137629
EXPECTED_BASE = "main"
AUTHORIZATION_PREFIX = "HUMAN STEWARD AUTHORIZATION — MP-ADMIN-LOW-FRICTION-001"
AUTHORIZATION_SLOGAN = (
    "Human Steward once at the authority boundary; machines may iterate internally "
    "until terminal proof or a genuinely new authority boundary."
)
REFEREE_PREFIX = "REFEREE_AGENT_APPROVED_EXACT_HEAD_LOW_FRICTION_ROUTINE"
TERMINAL_PREFIX = "LOW_FRICTION_TERMINAL_RECEIPT — MP-ADMIN-LOW-FRICTION-001"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
MARKDOWN_LINK_RE = re.compile(
    r"^\s*(?:"
    r"!?\[[^\]\n]*\]\([^\n]+\)"
    r"|\[!?\[[^\]\n]*\]\([^\n]+\)\]\([^\n]+\)"
    r"|<img\b[^>]*>"
    r")\s*$",
    re.IGNORECASE,
)

STATES = (
    "DISCOVERED",
    "CLASSIFIED",
    "SYNC_REQUIRED",
    "CHECKS_PENDING",
    "REVIEW_READY",
    "REFEREE_DISPOSED",
    "STABILIZING",
    "MERGED",
    "READBACK_VERIFIED",
    "TERMINAL",
)
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "DISCOVERED": {"CLASSIFIED"},
    "CLASSIFIED": {"SYNC_REQUIRED", "CHECKS_PENDING"},
    "SYNC_REQUIRED": {"CLASSIFIED"},
    "CHECKS_PENDING": {"REVIEW_READY", "CLASSIFIED"},
    "REVIEW_READY": {"REFEREE_DISPOSED", "CLASSIFIED"},
    "REFEREE_DISPOSED": {"STABILIZING", "CLASSIFIED"},
    "STABILIZING": {"MERGED", "CLASSIFIED"},
    "MERGED": {"READBACK_VERIFIED"},
    "READBACK_VERIFIED": {"TERMINAL"},
    "TERMINAL": set(),
}


@dataclass
class Trace:
    pr: int
    state: str = "DISCOVERED"
    events: list[dict[str, Any]] = field(default_factory=list)

    def transition(self, new_state: str, **details: Any) -> None:
        if new_state not in STATES:
            raise AutonomyError(f"unknown lifecycle state: {new_state}")
        if new_state not in ALLOWED_TRANSITIONS[self.state]:
            raise AutonomyError(
                f"forbidden lifecycle transition: {self.state}->{new_state}"
            )
        self.events.append({"from": self.state, "to": new_state, **details})
        self.state = new_state


@dataclass(frozen=True)
class Classification:
    pr: int
    head: str
    branch: str
    changed_paths: tuple[str, ...]
    additions: int
    deletions: int
    asset_paths: tuple[str, ...]
    markdown_paths: tuple[str, ...]

    def record(self) -> dict[str, Any]:
        return {
            "pr": self.pr,
            "head": self.head,
            "branch": self.branch,
            "changed_paths": list(self.changed_paths),
            "additions": self.additions,
            "deletions": self.deletions,
            "asset_paths": list(self.asset_paths),
            "markdown_paths": list(self.markdown_paths),
        }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_control(control: Mapping[str, Any]) -> list[str]:
    schema = load_json(CONTROL_SCHEMA_PATH)
    errors = [
        "control schema: "
        + "/".join(str(part) for part in error.absolute_path)
        + f": {error.message}"
        for error in Draft202012Validator(schema).iter_errors(control)
    ]
    if control.get("control_id") != EXPECTED_CONTROL_ID:
        errors.append("low-friction control id drift")
    if int(control.get("issue") or 0) != EXPECTED_ISSUE:
        errors.append("low-friction control issue drift")
    if control.get("repository") != EXPECTED_REPOSITORY:
        errors.append("low-friction repository drift")
    if control.get("base_branch") != EXPECTED_BASE:
        errors.append("low-friction base branch drift")
    auth = control.get("authorization", {})
    if int(auth.get("authorization_comment_id") or 0) != EXPECTED_AUTHORIZATION_COMMENT_ID:
        errors.append("low-friction authorization comment drift")
    if auth.get("intermediate_human_steward_checkpoint_required") is not False:
        errors.append("intermediate Human Steward checkpoint must remain disabled")
    if auth.get("terminal_exact_head_human_steward_checkpoint_required") is not False:
        errors.append("terminal Human Steward re-checkpoint must remain disabled")
    if auth.get("bounded_terminal_admission_delegated") is not True:
        errors.append("bounded terminal admission must remain delegated")
    identity = control.get("identity", {})
    if identity.get("candidate_login") != EXPECTED_CANDIDATE_LOGIN:
        errors.append("Candidate identity drift")
    if int(identity.get("candidate_app_id") or 0) != EXPECTED_CANDIDATE_APP_ID:
        errors.append("Candidate app id drift")
    if identity.get("referee_login") != EXPECTED_REFEREE_LOGIN:
        errors.append("Referee identity drift")
    if int(identity.get("referee_app_id") or 0) != EXPECTED_REFEREE_APP_ID:
        errors.append("Referee app id drift")
    if EXPECTED_CANDIDATE_LOGIN == EXPECTED_REFEREE_LOGIN:
        errors.append("Candidate and Referee identities are not separated")
    ruleset = control.get("ruleset", {})
    if int(ruleset.get("id") or 0) != EXPECTED_RULESET_ID:
        errors.append("low-friction ruleset id drift")
    if ruleset.get("bypass_mode") != "pull_request":
        errors.append("ruleset bypass mode must remain pull_request")
    if ruleset.get("ruleset_mutation_authorized") is not False:
        errors.append("ruleset mutation must remain unauthorized")
    if ruleset.get("direct_protected_push_authorized") is not False:
        errors.append("direct protected push must remain unauthorized")
    hard = control.get("hard_exclusions", {})
    if not hard or any(value is not True for value in hard.values()):
        errors.append("all low-friction hard exclusions must remain true")
    lifecycle = control.get("lifecycle", {})
    for key in (
        "automatic_mark_ready",
        "automatic_referee_disposition",
        "automatic_expected_head_merge",
        "automatic_protected_readback",
        "automatic_terminal_receipt",
        "behind_sync",
        "revalidate_after_head_change",
        "redisposition_after_head_change",
    ):
        if lifecycle.get(key) is not True:
            errors.append(f"required lifecycle automation disabled: {key}")
    return errors


def validate_command() -> int:
    errors = validate_control(load_json(CONTROL_PATH))
    runtime = (ROOT / "ci/administrative_autonomy_runtime.py")
    candidate_workflow = ROOT / ".github/workflows/administrative-maintenance-candidate.yml"
    if not runtime.is_file():
        errors.append("protected administrative runtime entrypoint is missing")
    else:
        text = runtime.read_text(encoding="utf-8")
        for marker in (
            "import administrative_autonomy_low_friction as low_friction",
            "low_friction.sweep(low_report)",
            "ADMIN_READ_TOKEN",
            "ADMIN_TOKEN",
            "human_steward_checkpoint_requested",
        ):
            if marker not in text:
                errors.append(f"low-friction runtime integration marker missing: {marker}")
    if not candidate_workflow.is_file():
        errors.append("protected candidate heartbeat workflow is missing")
    else:
        text = candidate_workflow.read_text(encoding="utf-8")
        for marker in ("- cron: '7 * * * *'", "- cron: '17 * * * *'", "- cron: '27 * * * *'", "- cron: '47 * * * *'"):
            if marker not in text:
                errors.append(f"protected heartbeat marker missing: {marker}")
    if (ROOT / ".github/workflows/administrative-maintenance-low-friction.yml").exists():
        errors.append("parallel low-friction privileged workflow must not exist")
    if errors:
        for error in errors:
            print(error)
        return 1
    print("MP-ADMIN-LOW-FRICTION-001 control and embedded runtime: valid")
    return 0


def require_live_authorization(referee: Client, control: Mapping[str, Any]) -> dict[str, Any]:
    auth = control["authorization"]
    comment_id = int(auth["authorization_comment_id"])
    comment = referee.get(f"/repos/{EXPECTED_REPOSITORY}/issues/comments/{comment_id}")
    if int(comment.get("id") or 0) != comment_id:
        raise AutonomyError("Human Steward authorization comment identity drift")
    if comment.get("user", {}).get("login") != auth["human_steward_login"]:
        raise AutonomyError("Human Steward authorization actor drift")
    body = str(comment.get("body") or "")
    if not body.startswith(str(auth["authorization_prefix"])):
        raise AutonomyError("Human Steward authorization prefix drift")
    if str(auth["required_slogan"]) not in body:
        raise AutonomyError("Human Steward authorization slogan drift")
    if "no second Human Steward exact-head checkpoint is required" not in body:
        raise AutonomyError("low-friction terminal delegation is absent from authorization")
    return comment


def _safe_markdown_patch(patch: str | None) -> bool:
    if not patch:
        return False
    changed = 0
    for raw in patch.splitlines():
        if raw.startswith(("+++", "---", "@@")):
            continue
        if not raw.startswith(("+", "-")):
            continue
        text = raw[1:]
        if not text.strip():
            continue
        changed += 1
        if not MARKDOWN_LINK_RE.fullmatch(text):
            return False
    return changed > 0


def _path_forbidden(path: str, config: Mapping[str, Any]) -> bool:
    if path in set(config["forbidden_exact_paths"]):
        return True
    return any(path.startswith(prefix) for prefix in config["forbidden_path_prefixes"])


def classify_pull(
    pull: Mapping[str, Any],
    files: Iterable[Mapping[str, Any]],
    control: Mapping[str, Any],
) -> Classification:
    config = control["classification"]
    number = int(pull.get("number") or 0)
    if number <= 0:
        raise AutonomyError("candidate pull request number is missing")
    if pull.get("state") != "open":
        raise AutonomyError("candidate pull request is not open")
    if pull.get("base", {}).get("ref") != control["base_branch"]:
        raise AutonomyError("candidate base branch drift")
    head = pull.get("head", {})
    branch = str(head.get("ref") or "")
    head_sha = str(head.get("sha") or "")
    if not branch.startswith(str(config["branch_prefix"])):
        raise AutonomyError("candidate branch is outside low-friction namespace")
    if not SHA_RE.fullmatch(head_sha):
        raise AutonomyError("candidate exact head is invalid")
    head_repo = str(head.get("repo", {}).get("full_name") or "")
    if head_repo != control["repository"]:
        raise AutonomyError("low-friction candidates must be same-repository branches")
    body = str(pull.get("body") or "")
    if str(config["opt_in_marker"]) not in body:
        raise AutonomyError("low-friction opt-in marker is missing")
    login = str(pull.get("user", {}).get("login") or "")
    if login not in set(config["allowed_candidate_logins"]):
        raise AutonomyError("candidate author is outside low-friction allowlist")

    file_list = list(files)
    if not file_list:
        raise AutonomyError("low-friction candidate has no changed files")
    if len(file_list) > int(config["maximum_changed_files"]):
        raise AutonomyError("low-friction changed-file limit exceeded")
    additions = sum(int(item.get("additions") or 0) for item in file_list)
    deletions = sum(int(item.get("deletions") or 0) for item in file_list)
    if additions > int(config["maximum_additions"]):
        raise AutonomyError("low-friction addition limit exceeded")
    if deletions > int(config["maximum_deletions"]):
        raise AutonomyError("low-friction deletion limit exceeded")

    exact = set(config["allowed_exact_paths"])
    asset_prefix = str(config["allowed_asset_prefix"])
    asset_exts = set(config["allowed_asset_extensions"])
    paths: list[str] = []
    assets: list[str] = []
    markdown: list[str] = []
    for item in file_list:
        path = str(item.get("filename") or "")
        if not path or _path_forbidden(path, config):
            raise AutonomyError(f"low-friction forbidden path: {path}")
        paths.append(path)
        if path in exact:
            if path != "README.md" or not _safe_markdown_patch(item.get("patch")):
                raise AutonomyError("README changes must be Markdown link/image-only")
            markdown.append(path)
            continue
        if path.startswith(asset_prefix):
            suffix = Path(path).suffix.lower()
            if suffix not in asset_exts:
                raise AutonomyError(f"unsupported low-friction asset type: {path}")
            if str(item.get("status") or "") not in {"added", "modified", "renamed"}:
                raise AutonomyError(f"asset deletion is not low-friction admissible: {path}")
            assets.append(path)
            continue
        raise AutonomyError(f"path is outside low-friction presentation scope: {path}")
    return Classification(
        pr=number,
        head=head_sha,
        branch=branch,
        changed_paths=tuple(paths),
        additions=additions,
        deletions=deletions,
        asset_paths=tuple(assets),
        markdown_paths=tuple(markdown),
    )


def check_snapshot(
    check_runs: Iterable[Mapping[str, Any]],
    required: Iterable[str],
    accepted: set[str],
) -> tuple[str, dict[str, str]]:
    latest: dict[str, Mapping[str, Any]] = {}
    for run in check_runs:
        name = str(run.get("name") or "")
        if not name:
            continue
        old = latest.get(name)
        if old is None or str(run.get("started_at") or "") > str(old.get("started_at") or ""):
            latest[name] = run
    observed: dict[str, str] = {}
    pending = False
    for name in required:
        run = latest.get(name)
        if run is None:
            observed[name] = "missing"
            pending = True
            continue
        status = str(run.get("status") or "missing")
        if status != "completed":
            observed[name] = status
            pending = True
            continue
        conclusion = str(run.get("conclusion") or "missing")
        observed[name] = conclusion
        if conclusion not in accepted:
            return "failed", observed
    return ("pending" if pending else "green"), observed


def live_required_contexts(admin_read: Client, control: Mapping[str, Any]) -> tuple[list[str], dict[str, Any]]:
    ruleset_id = int(control["ruleset"]["id"])
    value = admin_read.get(f"/repos/{EXPECTED_REPOSITORY}/rulesets/{ruleset_id}")
    if int(value.get("id") or ruleset_id) != ruleset_id:
        raise AutonomyError("live low-friction ruleset identity drift")
    desired = (
        EXPECTED_CANDIDATE_APP_ID,
        str(control["ruleset"]["actor_type"]),
        str(control["ruleset"]["bypass_mode"]),
    )
    actors = {
        (int(item["actor_id"]), str(item["actor_type"]), str(item["bypass_mode"]))
        for item in value.get("bypass_actors", [])
    }
    if control["ruleset"]["existing_candidate_actor_required"] is True and desired not in actors:
        raise AutonomyError("existing PR-only Candidate ruleset actor is absent")
    return required_contexts(value), value


def current_pull(client: Client, pr: int) -> dict[str, Any]:
    return client.get(f"/repos/{EXPECTED_REPOSITORY}/pulls/{pr}")


def pull_files(client: Client, pr: int) -> list[dict[str, Any]]:
    files = client.get(f"/repos/{EXPECTED_REPOSITORY}/pulls/{pr}/files?per_page=100")
    if not isinstance(files, list) or len(files) >= 100:
        raise AutonomyError("low-friction changed-file inspection is not bounded")
    return files


def wait_mergeable_state(
    client: Client,
    pr: int,
    expected_head: str,
    control: Mapping[str, Any],
) -> tuple[str, dict[str, Any]]:
    lifecycle = control["lifecycle"]
    deadline = time.monotonic() + int(lifecycle["merge_state_wait_seconds"])
    poll = int(lifecycle["poll_interval_seconds"])
    last = "unknown"
    while time.monotonic() < deadline:
        pull = current_pull(client, pr)
        observed = str(pull.get("head", {}).get("sha") or "")
        if observed != expected_head:
            return "head_changed", pull
        state = str(pull.get("mergeable_state") or "unknown").lower()
        last = state
        if state != "unknown":
            return state, pull
        time.sleep(poll)
    raise AutonomyError(f"low-friction merge-state readback timed out: {last}")


def synchronize_behind(
    candidate: Client,
    observer: Client,
    pull: Mapping[str, Any],
    control: Mapping[str, Any],
) -> dict[str, Any]:
    pr = int(pull["number"])
    observed_head = str(pull.get("head", {}).get("sha") or "")
    if not SHA_RE.fullmatch(observed_head):
        raise AutonomyError("BEHIND synchronization observed invalid head")
    candidate.put(
        f"/repos/{EXPECTED_REPOSITORY}/pulls/{pr}/update-branch",
        {"expected_head_sha": observed_head},
    )
    lifecycle = control["lifecycle"]
    deadline = time.monotonic() + int(lifecycle["head_change_wait_seconds"])
    poll = int(lifecycle["poll_interval_seconds"])
    while time.monotonic() < deadline:
        time.sleep(poll)
        fresh = current_pull(observer, pr)
        new_head = str(fresh.get("head", {}).get("sha") or "")
        if new_head != observed_head:
            if not SHA_RE.fullmatch(new_head):
                raise AutonomyError("BEHIND synchronization produced invalid head")
            return {
                "previous_head": observed_head,
                "synchronized_head": new_head,
                "expected_head_used": True,
            }
    raise AutonomyError("BEHIND synchronization did not change the candidate head")


def wait_checks_or_restart(
    observer: Client,
    pr: int,
    head: str,
    contexts: list[str],
    control: Mapping[str, Any],
) -> tuple[str, dict[str, str], dict[str, Any]]:
    lifecycle = control["lifecycle"]
    deadline = time.monotonic() + int(lifecycle["required_checks_wait_seconds"])
    poll = int(lifecycle["poll_interval_seconds"])
    accepted = set(lifecycle["accepted_check_conclusions"])
    last: dict[str, str] = {}
    while time.monotonic() < deadline:
        pull = current_pull(observer, pr)
        observed_head = str(pull.get("head", {}).get("sha") or "")
        if observed_head != head:
            return "head_changed", last, pull
        merge_state = str(pull.get("mergeable_state") or "unknown").lower()
        if merge_state == "behind":
            return "behind", last, pull
        runs = observer.get(
            f"/repos/{EXPECTED_REPOSITORY}/commits/{head}/check-runs?per_page=100"
        ).get("check_runs", [])
        status, last = check_snapshot(runs, contexts, accepted)
        if status == "failed":
            failed = {name: result for name, result in last.items() if result not in accepted and result not in {"missing", "queued", "in_progress", "requested", "waiting", "pending"}}
            raise AutonomyError(f"low-friction exact-head required check failed: {failed or last}")
        if status == "green":
            return "green", last, pull
        time.sleep(poll)
    raise AutonomyError(f"low-friction exact-head checks timed out: {last}")


def mark_ready(candidate: Client, pull: Mapping[str, Any], expected_head: str) -> None:
    if pull.get("draft") is not True:
        return
    node_id = str(pull.get("node_id") or "")
    if not node_id:
        raise AutonomyError("draft candidate has no GraphQL node id")
    result = candidate.post(
        "/graphql",
        {
            "query": "mutation($id:ID!){markPullRequestReadyForReview(input:{pullRequestId:$id}){pullRequest{number isDraft headRefOid}}}",
            "variables": {"id": node_id},
        },
    )
    if result.get("errors"):
        raise AutonomyError(f"mark-ready mutation failed: {result['errors']}")
    value = result.get("data", {}).get("markPullRequestReadyForReview", {}).get("pullRequest", {})
    if value.get("isDraft") is not False or value.get("headRefOid") != expected_head:
        raise AutonomyError("candidate did not become review-ready at the exact head")


def referee_disposition_present(
    referee: Client,
    pr: int,
    head: str,
    referee_login: str,
) -> dict[str, Any] | None:
    comments = referee.get(f"/repos/{EXPECTED_REPOSITORY}/issues/{pr}/comments?per_page=100")
    marker = f"- exact head: `{head}`;"
    for item in comments:
        body = str(item.get("body") or "")
        if (
            item.get("user", {}).get("login") == referee_login
            and body.startswith(REFEREE_PREFIX)
            and marker in body
            and "LOW_FRICTION_ROUTINE_EXPECTED_HEAD_PROTECTED_MERGE" in body
        ):
            return item
    return None


def record_referee_disposition(
    referee: Client,
    classification: Classification,
    checks: Mapping[str, str],
    referee_login: str,
) -> dict[str, Any]:
    existing = referee_disposition_present(
        referee, classification.pr, classification.head, referee_login
    )
    if existing:
        return existing
    check_lines = "\n".join(
        f"- `{name}`: `{result}`;" for name, result in sorted(checks.items())
    )
    body = (
        f"{REFEREE_PREFIX}\n\n"
        f"- control: `{EXPECTED_CONTROL_ID}`;\n"
        f"- exact head: `{classification.head}`;\n"
        f"- branch: `{classification.branch}`;\n"
        "- Human Steward re-checkpoint: `false`;\n"
        "- machine classification: `ROUTINE_PRESENTATION_ONLY`;\n"
        "- Candidate/Referee separation: `verified`;\n"
        "- direct protected push: `false`;\n"
        "- ruleset mutation: `false`;\n"
        "- required exact-head checks:\n"
        f"{check_lines}\n\n"
        "Disposition: `LOW_FRICTION_ROUTINE_EXPECTED_HEAD_PROTECTED_MERGE`."
    )
    comment = referee.post(
        f"/repos/{EXPECTED_REPOSITORY}/issues/{classification.pr}/comments",
        {"body": body},
    )
    if comment.get("user", {}).get("login") != referee_login:
        raise AutonomyError("low-friction Referee actor readback failed")
    return comment


def stabilize_after_disposition(
    observer: Client,
    pr: int,
    head: str,
    contexts: list[str],
    control: Mapping[str, Any],
) -> tuple[str, dict[str, str], dict[str, Any]]:
    lifecycle = control["lifecycle"]
    accepted = set(lifecycle["accepted_check_conclusions"])
    required_state = str(lifecycle["required_pre_merge_state"])
    settle = int(lifecycle["post_disposition_stabilization_seconds"])
    deadline = time.monotonic() + int(lifecycle["merge_state_wait_seconds"])
    poll = int(lifecycle["poll_interval_seconds"])
    stable_since: float | None = None
    last_checks: dict[str, str] = {}
    last_pull: dict[str, Any] = {}
    while time.monotonic() < deadline:
        pull = current_pull(observer, pr)
        last_pull = pull
        if str(pull.get("head", {}).get("sha") or "") != head:
            return "head_changed", last_checks, pull
        merge_state = str(pull.get("mergeable_state") or "unknown").lower()
        if merge_state == "behind":
            return "behind", last_checks, pull
        if merge_state in {"dirty", "unstable"}:
            raise AutonomyError(f"low-friction candidate became {merge_state} after disposition")
        runs = observer.get(
            f"/repos/{EXPECTED_REPOSITORY}/commits/{head}/check-runs?per_page=100"
        ).get("check_runs", [])
        check_state, last_checks = check_snapshot(runs, contexts, accepted)
        if check_state == "failed":
            raise AutonomyError(f"low-friction checks regressed after disposition: {last_checks}")
        clean = check_state == "green" and merge_state == required_state and pull.get("draft") is False
        if clean:
            if stable_since is None:
                stable_since = time.monotonic()
            if time.monotonic() - stable_since >= settle:
                return "stable", last_checks, pull
        else:
            stable_since = None
        time.sleep(poll)
    raise AutonomyError(
        f"low-friction post-disposition stabilization timed out: merge_state={last_pull.get('mergeable_state')} checks={last_checks}"
    )


def expected_head_merge(
    candidate: Client,
    pr: int,
    head: str,
    candidate_login: str,
) -> dict[str, Any]:
    result = candidate.put(
        f"/repos/{EXPECTED_REPOSITORY}/pulls/{pr}/merge",
        {
            "sha": head,
            "merge_method": "merge",
            "commit_title": f"Merge PR #{pr}: {EXPECTED_CONTROL_ID} routine maintenance",
            "commit_message": (
                f"Machine-classified routine presentation maintenance.\n\n"
                f"exact head {head}\n"
                "Disposition: LOW_FRICTION_ROUTINE_EXPECTED_HEAD_PROTECTED_MERGE"
            ),
        },
    )
    if result.get("merged") is not True:
        raise AutonomyError(f"low-friction expected-head merge failed: {result.get('message')}")
    pull = current_pull(candidate, pr)
    if pull.get("merged") is not True or pull.get("head", {}).get("sha") != head:
        raise AutonomyError("low-friction merge readback mismatch")
    merged_by = str(pull.get("merged_by", {}).get("login") or "")
    if merged_by != candidate_login:
        raise AutonomyError(f"low-friction merge executor drift: {merged_by}")
    return pull


def validate_protected_readback_payload(
    pull: Mapping[str, Any],
    commit: Mapping[str, Any],
    compare: Mapping[str, Any],
    expected_head: str,
    candidate_login: str,
) -> dict[str, Any]:
    if pull.get("merged") is not True:
        raise AutonomyError("protected readback says PR is not merged")
    if pull.get("head", {}).get("sha") != expected_head:
        raise AutonomyError("protected readback exact-head mismatch")
    if pull.get("merged_by", {}).get("login") != candidate_login:
        raise AutonomyError("protected readback merge-executor mismatch")
    merge_sha = str(pull.get("merge_commit_sha") or "")
    if not SHA_RE.fullmatch(merge_sha):
        raise AutonomyError("protected readback merge SHA is invalid")
    if str(commit.get("sha") or "") != merge_sha:
        raise AutonomyError("protected merge commit identity mismatch")
    verification = commit.get("commit", {}).get("verification", {})
    if verification.get("verified") is not True or verification.get("reason") != "valid":
        raise AutonomyError("protected merge commit is not signed/verified")
    parents = {str(item.get("sha") or "") for item in commit.get("parents", [])}
    if expected_head not in parents:
        raise AutonomyError("protected merge commit does not bind exact candidate head")
    status = str(compare.get("status") or "")
    if status not in {"ahead", "identical"}:
        raise AutonomyError("protected merge commit is not an ancestor of protected main")
    return {
        "merge_sha": merge_sha,
        "signature_verified": True,
        "signature_reason": "valid",
        "exact_head_parent": True,
        "protected_main_contains_merge": True,
        "protected_main_compare_status": status,
    }


def protected_readback(
    observer: Client,
    pr: int,
    expected_head: str,
    candidate_login: str,
    control: Mapping[str, Any],
) -> dict[str, Any]:
    lifecycle = control["lifecycle"]
    deadline = time.monotonic() + int(lifecycle["protected_readback_wait_seconds"])
    poll = int(lifecycle["poll_interval_seconds"])
    last = "protected readback not yet available"
    while time.monotonic() < deadline:
        pull = current_pull(observer, pr)
        if pull.get("merged") is not True:
            last = "PR not yet merged"
            time.sleep(poll)
            continue
        merge_sha = str(pull.get("merge_commit_sha") or "")
        try:
            commit = observer.get(f"/repos/{EXPECTED_REPOSITORY}/commits/{merge_sha}")
            compare = observer.get(
                f"/repos/{EXPECTED_REPOSITORY}/compare/{merge_sha}...{EXPECTED_BASE}"
            )
            return validate_protected_readback_payload(
                pull, commit, compare, expected_head, candidate_login
            )
        except AutonomyError as exc:
            last = str(exc)
            time.sleep(poll)
    raise AutonomyError(f"protected readback timed out: {last}")


def terminal_receipt_present(referee: Client, pr: int, head: str, merge_sha: str) -> dict[str, Any] | None:
    comments = referee.get(f"/repos/{EXPECTED_REPOSITORY}/issues/{pr}/comments?per_page=100")
    for item in comments:
        body = str(item.get("body") or "")
        if (
            item.get("user", {}).get("login") == EXPECTED_REFEREE_LOGIN
            and body.startswith(TERMINAL_PREFIX)
            and f"- exact head: `{head}`;" in body
            and f"- protected merge: `{merge_sha}`;" in body
        ):
            return item
    return None


def record_terminal_receipt(
    referee: Client,
    classification: Classification,
    disposition_id: int,
    checks: Mapping[str, str],
    sync_events: list[dict[str, Any]],
    readback: Mapping[str, Any],
    trace: Trace,
) -> dict[str, Any]:
    merge_sha = str(readback["merge_sha"])
    existing = terminal_receipt_present(
        referee, classification.pr, classification.head, merge_sha
    )
    if existing:
        return existing
    body = (
        f"{TERMINAL_PREFIX}\n\n"
        f"- exact head: `{classification.head}`;\n"
        f"- protected merge: `{merge_sha}`;\n"
        f"- Referee disposition comment: `{disposition_id}`;\n"
        f"- internal head synchronizations: `{len(sync_events)}`;\n"
        f"- exact-head checks: `{json.dumps(dict(sorted(checks.items())), sort_keys=True)}`;\n"
        "- signed protected merge: `verified`;\n"
        "- merge ancestor of protected main: `verified`;\n"
        "- direct protected push: `false`;\n"
        "- ruleset mutation: `false`;\n"
        "- Human Steward intermediate or terminal re-checkpoint: `false`;\n"
        f"- lifecycle terminal state: `{trace.state}`.\n\n"
        "Disposition: `LOW_FRICTION_ROUTINE_PROTECTED_COMPLETE`."
    )
    comment = referee.post(
        f"/repos/{EXPECTED_REPOSITORY}/issues/{classification.pr}/comments",
        {"body": body},
    )
    if comment.get("user", {}).get("login") != EXPECTED_REFEREE_LOGIN:
        raise AutonomyError("terminal receipt actor readback failed")
    return comment


def already_terminal(referee: Client, pr: int, pull: Mapping[str, Any]) -> dict[str, Any] | None:
    if pull.get("merged") is not True:
        return None
    head = str(pull.get("head", {}).get("sha") or "")
    merge_sha = str(pull.get("merge_commit_sha") or "")
    if not head or not merge_sha:
        return None
    return terminal_receipt_present(referee, pr, head, merge_sha)


def runtime_clients(control: Mapping[str, Any]) -> tuple[Client, Client, Client, str]:
    candidate_login = os.environ.get("CANDIDATE_LOGIN", "")
    referee_login = os.environ.get("REFEREE_LOGIN", "")
    candidate_app_id = int(os.environ.get("CANDIDATE_APP_ID", "0") or 0)
    referee_app_id = int(os.environ.get("REFEREE_APP_ID", "0") or 0)
    if candidate_login != control["identity"]["candidate_login"]:
        raise AutonomyError("runtime Candidate login drift")
    if candidate_app_id != int(control["identity"]["candidate_app_id"]):
        raise AutonomyError("runtime Candidate app id drift")
    if referee_login != control["identity"]["referee_login"]:
        raise AutonomyError("runtime Referee login drift")
    if referee_app_id != int(control["identity"]["referee_app_id"]):
        raise AutonomyError("runtime Referee app id drift")
    if candidate_login == referee_login or candidate_app_id == referee_app_id:
        raise AutonomyError("runtime Candidate/Referee separation failed")
    admin_token = os.environ.get("ADMIN_READ_TOKEN") or os.environ.get("ADMIN_TOKEN", "")
    return (
        Client(os.environ.get("CANDIDATE_TOKEN", "")),
        Client(os.environ.get("REFEREE_TOKEN", "")),
        Client(admin_token),
        candidate_login,
    )


def execute_pr(pr: int, report_path: Path) -> dict[str, Any]:
    control = load_json(CONTROL_PATH)
    errors = validate_control(control)
    if errors:
        raise AutonomyError("; ".join(errors))
    if os.environ.get("GITHUB_REPOSITORY", EXPECTED_REPOSITORY) != EXPECTED_REPOSITORY:
        raise AutonomyError("runtime repository drift")
    candidate, referee, admin_read, candidate_login = runtime_clients(control)
    authorization = require_live_authorization(referee, control)
    contexts, ruleset = live_required_contexts(admin_read, control)
    trace = Trace(pr=pr)
    sync_events: list[dict[str, Any]] = []
    final_checks: dict[str, str] = {}
    disposition: dict[str, Any] | None = None

    initial = current_pull(referee, pr)
    terminal = already_terminal(referee, pr, initial)
    if terminal:
        report = {
            "schema_version": "1.0.0",
            "control_id": EXPECTED_CONTROL_ID,
            "state": "ALREADY_TERMINAL",
            "pr": pr,
            "terminal_receipt_comment_id": int(terminal["id"]),
            "human_steward_checkpoint_requested": False,
        }
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return report

    maximum = int(control["lifecycle"]["maximum_internal_head_iterations"])
    for iteration in range(1, maximum + 1):
        pull = current_pull(referee, pr)
        if pull.get("merged") is True:
            raise AutonomyError("candidate merged without a low-friction terminal receipt")
        classification = classify_pull(pull, pull_files(referee, pr), control)
        if trace.state == "DISCOVERED":
            trace.transition("CLASSIFIED", iteration=iteration, head=classification.head)
        elif trace.state != "CLASSIFIED":
            trace.transition("CLASSIFIED", iteration=iteration, head=classification.head)

        merge_state, fresh = wait_mergeable_state(referee, pr, classification.head, control)
        if merge_state == "head_changed":
            continue
        if merge_state == "behind":
            trace.transition("SYNC_REQUIRED", iteration=iteration, head=classification.head)
            event = synchronize_behind(candidate, referee, fresh, control)
            sync_events.append({"iteration": iteration, **event})
            trace.transition("CLASSIFIED", iteration=iteration, head=event["synchronized_head"], cause="behind_sync")
            continue
        if merge_state == "dirty":
            raise AutonomyError("low-friction candidate has merge conflicts")

        trace.transition("CHECKS_PENDING", iteration=iteration, head=classification.head)
        check_state, checks, checked_pull = wait_checks_or_restart(
            referee, pr, classification.head, contexts, control
        )
        final_checks = checks
        if check_state == "head_changed":
            trace.transition("CLASSIFIED", iteration=iteration, head=checked_pull.get("head", {}).get("sha"), cause="head_changed_during_checks")
            continue
        if check_state == "behind":
            trace.transition("CLASSIFIED", iteration=iteration, head=classification.head, cause="behind_during_checks")
            merge_state, fresh = wait_mergeable_state(referee, pr, classification.head, control)
            if merge_state != "behind":
                continue
            trace.transition("SYNC_REQUIRED", iteration=iteration, head=classification.head)
            event = synchronize_behind(candidate, referee, fresh, control)
            sync_events.append({"iteration": iteration, **event})
            trace.transition("CLASSIFIED", iteration=iteration, head=event["synchronized_head"], cause="behind_sync_after_checks")
            continue

        mark_ready(candidate, checked_pull, classification.head)
        readied = current_pull(referee, pr)
        if str(readied.get("head", {}).get("sha") or "") != classification.head:
            trace.transition("CLASSIFIED", iteration=iteration, head=readied.get("head", {}).get("sha"), cause="head_changed_at_ready")
            continue
        if readied.get("draft") is True:
            raise AutonomyError("candidate remained draft after automatic ready transition")
        trace.transition("REVIEW_READY", iteration=iteration, head=classification.head)

        merge_state, fresh = wait_mergeable_state(referee, pr, classification.head, control)
        if merge_state == "head_changed":
            trace.transition("CLASSIFIED", iteration=iteration, head=fresh.get("head", {}).get("sha"), cause="head_changed_before_referee")
            continue
        if merge_state == "behind":
            trace.transition("CLASSIFIED", iteration=iteration, head=classification.head, cause="behind_before_referee")
            trace.transition("SYNC_REQUIRED", iteration=iteration, head=classification.head)
            event = synchronize_behind(candidate, referee, fresh, control)
            sync_events.append({"iteration": iteration, **event})
            trace.transition("CLASSIFIED", iteration=iteration, head=event["synchronized_head"], cause="behind_sync_before_referee")
            continue
        if merge_state == "dirty":
            raise AutonomyError("candidate became conflicted before Referee disposition")

        disposition = record_referee_disposition(
            referee, classification, checks, EXPECTED_REFEREE_LOGIN
        )
        trace.transition(
            "REFEREE_DISPOSED",
            iteration=iteration,
            head=classification.head,
            disposition_id=int(disposition["id"]),
        )
        trace.transition("STABILIZING", iteration=iteration, head=classification.head)
        stable_state, stable_checks, stable_pull = stabilize_after_disposition(
            referee, pr, classification.head, contexts, control
        )
        final_checks = stable_checks or final_checks
        if stable_state == "head_changed":
            trace.transition("CLASSIFIED", iteration=iteration, head=stable_pull.get("head", {}).get("sha"), cause="head_changed_after_referee")
            continue
        if stable_state == "behind":
            trace.transition("CLASSIFIED", iteration=iteration, head=classification.head, cause="behind_after_referee")
            merge_state, fresh = wait_mergeable_state(referee, pr, classification.head, control)
            if merge_state == "behind":
                trace.transition("SYNC_REQUIRED", iteration=iteration, head=classification.head)
                event = synchronize_behind(candidate, referee, fresh, control)
                sync_events.append({"iteration": iteration, **event})
                trace.transition("CLASSIFIED", iteration=iteration, head=event["synchronized_head"], cause="behind_sync_after_referee")
            continue

        exact = current_pull(referee, pr)
        reclassified = classify_pull(exact, pull_files(referee, pr), control)
        if reclassified.head != classification.head:
            trace.transition("CLASSIFIED", iteration=iteration, head=reclassified.head, cause="head_changed_at_merge_boundary")
            continue
        if referee_disposition_present(referee, pr, classification.head, EXPECTED_REFEREE_LOGIN) is None:
            raise AutonomyError("exact-head Referee disposition disappeared before merge")
        merged = expected_head_merge(
            candidate, pr, classification.head, candidate_login
        )
        trace.transition(
            "MERGED",
            iteration=iteration,
            head=classification.head,
            merge_sha=merged.get("merge_commit_sha"),
        )
        readback = protected_readback(
            referee, pr, classification.head, candidate_login, control
        )
        trace.transition(
            "READBACK_VERIFIED",
            iteration=iteration,
            head=classification.head,
            merge_sha=readback["merge_sha"],
        )
        trace.transition("TERMINAL", iteration=iteration, head=classification.head)
        receipt = record_terminal_receipt(
            referee,
            classification,
            int(disposition["id"]),
            final_checks,
            sync_events,
            readback,
            trace,
        )
        report = {
            "schema_version": "1.0.0",
            "control_id": EXPECTED_CONTROL_ID,
            "state": "LOW_FRICTION_ROUTINE_PROTECTED_COMPLETE",
            "control_issue": EXPECTED_ISSUE,
            "authorization_comment_id": int(authorization["id"]),
            "human_steward_checkpoint_requested": False,
            "classification": classification.record(),
            "required_contexts": contexts,
            "ruleset_id": int(ruleset.get("id") or EXPECTED_RULESET_ID),
            "required_checks": final_checks,
            "sync_events": sync_events,
            "referee_disposition_comment_id": int(disposition["id"]),
            "terminal_receipt_comment_id": int(receipt["id"]),
            "readback": readback,
            "lifecycle": trace.events,
            "terminal_state": trace.state,
            "candidate_login": candidate_login,
            "referee_login": EXPECTED_REFEREE_LOGIN,
            "direct_protected_push": False,
            "ruleset_mutation": False,
            "bypass_widening_or_exercise": False,
        }
        report_path.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(report, indent=2, sort_keys=True))
        return report

    raise AutonomyError(
        f"low-friction internal head iteration limit exhausted after {maximum} attempts; this is a terminal exception, not a Human Steward approval request"
    )


def eligible_sweep_prs(referee: Client, control: Mapping[str, Any]) -> list[int]:
    pulls = referee.get(f"/repos/{EXPECTED_REPOSITORY}/pulls?state=open&per_page=100")
    config = control["classification"]
    result: list[int] = []
    for pull in pulls:
        branch = str(pull.get("head", {}).get("ref") or "")
        body = str(pull.get("body") or "")
        if branch.startswith(str(config["branch_prefix"])) and str(config["opt_in_marker"]) in body:
            result.append(int(pull["number"]))
    if len(result) > 10:
        raise AutonomyError("low-friction sweep found more than ten eligible PRs; fail-closed triage required")
    return result


def sweep(report_path: Path) -> dict[str, Any]:
    control = load_json(CONTROL_PATH)
    errors = validate_control(control)
    if errors:
        raise AutonomyError("; ".join(errors))
    _, referee, _, _ = runtime_clients(control)
    require_live_authorization(referee, control)
    prs = eligible_sweep_prs(referee, control)
    outcomes: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for pr in prs:
        child = report_path.with_name(f"{report_path.stem}-pr-{pr}{report_path.suffix}")
        try:
            outcomes.append(execute_pr(pr, child))
        except Exception as exc:
            failures.append({"pr": pr, "error": str(exc)})
    report = {
        "schema_version": "1.0.0",
        "control_id": EXPECTED_CONTROL_ID,
        "state": "SWEEP_COMPLETE" if not failures else "SWEEP_COMPLETED_WITH_FAIL_CLOSED_EXCEPTIONS",
        "eligible_prs": prs,
        "outcomes": outcomes,
        "failures": failures,
        "human_steward_checkpoint_requested": False,
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if failures:
        raise AutonomyError(f"low-friction sweep retained fail-closed exceptions: {failures}")
    return report


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser()
    sub = value.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    execute = sub.add_parser("execute")
    execute.add_argument("--pr", type=int, required=True)
    execute.add_argument("--report", type=Path, required=True)
    sweep_parser = sub.add_parser("sweep")
    sweep_parser.add_argument("--report", type=Path, required=True)
    return value


def write_failure(path: Path | None, command: str, exc: Exception) -> None:
    if path is None:
        return
    value = {
        "schema_version": "1.0.0",
        "control_id": EXPECTED_CONTROL_ID,
        "state": "LOW_FRICTION_FAILED_CLOSED",
        "command": command,
        "error": str(exc),
        "human_steward_checkpoint_requested": False,
        "new_authority_boundary": False,
    }
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(sys.argv[1:] if argv is None else argv)
    if args.command == "validate":
        return validate_command()
    report = args.report
    try:
        if args.command == "execute":
            execute_pr(args.pr, report)
        else:
            sweep(report)
        return 0
    except Exception as exc:
        write_failure(report, args.command, exc)
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
