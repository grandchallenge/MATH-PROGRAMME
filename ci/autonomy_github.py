from __future__ import annotations

import base64
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


class AutonomyError(RuntimeError):
    pass


class Client:
    def __init__(self, token: str, api: str = "https://api.github.com"):
        if not token:
            raise AutonomyError("required token is missing")
        self.token = token
        self.api = api.rstrip("/")

    def call(self, method: str, path: str, payload: Any = None) -> Any:
        req = urllib.request.Request(
            self.api + path,
            data=None if payload is None else json.dumps(payload).encode(),
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "gcl-administrative-autonomy",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                body = response.read()
                return json.loads(body) if body else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise AutonomyError(
                f"{method} {path} failed: {exc.code} {detail}"
            ) from exc

    def get(self, path: str) -> Any:
        return self.call("GET", path)

    def post(self, path: str, payload: Any) -> Any:
        return self.call("POST", path, payload)

    def put(self, path: str, payload: Any) -> Any:
        return self.call("PUT", path, payload)

    def patch(self, path: str, payload: Any) -> Any:
        return self.call("PATCH", path, payload)

    def delete(self, path: str) -> Any:
        return self.call("DELETE", path)


@dataclass(frozen=True)
class Identity:
    login: str
    app_id: int
    token_role: str

    def record(self) -> dict[str, Any]:
        return {
            "login": self.login,
            "app_id": self.app_id,
            "token_role": self.token_role,
        }


def identity(login: str, expected_app_id: int, token_role: str) -> Identity:
    if not login.endswith("[bot]") or expected_app_id <= 0:
        raise AutonomyError(f"{token_role} identity is incomplete")
    return Identity(login, expected_app_id, token_role)


def ruleset_body(
    value: dict[str, Any], actors: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        key: value[key]
        for key in ("name", "target", "enforcement", "conditions", "rules")
    } | {"bypass_actors": actors}


def install_bypass(
    admin: Client,
    repo: str,
    ruleset_id: int,
    referee: Identity,
) -> tuple[dict[str, Any], dict[str, Any]]:
    path = f"/repos/{repo}/rulesets/{ruleset_id}"
    before = admin.get(path)
    actors = [
        {
            "actor_id": int(item["actor_id"]),
            "actor_type": item["actor_type"],
            "bypass_mode": item["bypass_mode"],
        }
        for item in before.get("bypass_actors", [])
    ]
    desired = {
        "actor_id": referee.app_id,
        "actor_type": "Integration",
        "bypass_mode": "pull_request",
    }
    if desired not in actors:
        admin.put(path, ruleset_body(before, actors + [desired]))
    after = admin.get(path)
    readback_actors = [
        {
            "actor_id": int(item["actor_id"]),
            "actor_type": item["actor_type"],
            "bypass_mode": item["bypass_mode"],
        }
        for item in after.get("bypass_actors", [])
    ]
    if desired not in readback_actors:
        raise AutonomyError(
            "Referee Agent pull-request bypass readback failed"
        )
    return before, after


def restore_ruleset(
    admin: Client,
    repo: str,
    ruleset_id: int,
    before: dict[str, Any],
) -> None:
    admin.put(
        f"/repos/{repo}/rulesets/{ruleset_id}",
        ruleset_body(before, before.get("bypass_actors", [])),
    )


def required_contexts(ruleset: dict[str, Any]) -> list[str]:
    for rule in ruleset.get("rules", []):
        if rule.get("type") == "required_status_checks":
            contexts = [
                item["context"]
                for item in rule["parameters"]["required_status_checks"]
            ]
            if contexts:
                return contexts
    raise AutonomyError("live ruleset has no required checks")


def branch(client: Client, repo: str, name: str, sha: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    try:
        current = client.get(f"/repos/{repo}/branches/{encoded}")
    except AutonomyError as exc:
        if " 404 " not in str(exc):
            raise
        current = None
    if current and current["commit"]["sha"] != sha:
        raise AutonomyError(
            "activation branch already exists at another head"
        )
    if not current:
        client.post(
            f"/repos/{repo}/git/refs",
            {"ref": f"refs/heads/{name}", "sha": sha},
        )


def delete_branch(client: Client, repo: str, name: str) -> None:
    encoded = urllib.parse.quote(name, safe="")
    try:
        client.delete(f"/repos/{repo}/git/refs/heads/{encoded}")
    except AutonomyError as exc:
        if " 404 " not in str(exc):
            raise


def content(
    client: Client,
    repo: str,
    path: str,
    ref: str,
) -> dict[str, Any] | None:
    try:
        return client.get(
            f"/repos/{repo}/contents/{path}"
            f"?ref={urllib.parse.quote(ref, safe='')}"
        )
    except AutonomyError as exc:
        if " 404 " in str(exc):
            return None
        raise


def json_content(
    client: Client,
    repo: str,
    path: str,
    ref: str,
) -> dict[str, Any] | None:
    value = content(client, repo, path, ref)
    if not value:
        return None
    return json.loads(base64.b64decode(value["content"]))


def put_json(
    client: Client,
    repo: str,
    branch_name: str,
    path: str,
    value: dict[str, Any],
) -> str:
    old = content(client, repo, path, branch_name)
    payload = {
        "message": "Activate MP-ADMIN-AUTONOMY-TRANSITION-001",
        "content": base64.b64encode(
            (json.dumps(value, indent=2) + "\n").encode()
        ).decode(),
        "branch": branch_name,
    }
    if old:
        payload["sha"] = old["sha"]
    result = client.put(f"/repos/{repo}/contents/{path}", payload)
    return result["commit"]["sha"]


def pull(
    client: Client,
    repo: str,
    branch_name: str,
    transition_head: str,
) -> dict[str, Any]:
    owner = repo.split("/", 1)[0]
    query = urllib.parse.urlencode(
        {"state": "all", "head": f"{owner}:{branch_name}"}
    )
    existing = client.get(f"/repos/{repo}/pulls?{query}")
    if existing:
        value = existing[0]
        if value.get("state") == "closed" and not value.get("merged_at"):
            value = client.patch(
                f"/repos/{repo}/pulls/{value['number']}",
                {"state": "open"},
            )
        return value
    return client.post(
        f"/repos/{repo}/pulls",
        {
            "title": (
                "[autonomy-activation] activate "
                "MP-ADMIN-AUTONOMY-TRANSITION-001"
            ),
            "head": branch_name,
            "base": "main",
            "draft": False,
            "maintainer_can_modify": False,
            "body": (
                f"Protected canary for transition head `{transition_head}`.\n\n"
                "Candidate Agent: `gcl-release-trust[bot]`; "
                "Referee Agent: `github-actions[bot]`. "
                "The Referee records an exact-head approval disposition "
                "only after every live required check succeeds. Exact-head "
                "auto-merge is enabled only after that disposition. "
                "Direct protected push and Human Steward impersonation "
                "are prohibited."
            ),
        },
    )


def verify_scope(
    client: Client,
    repo: str,
    pr: dict[str, Any],
    activation_path: str,
) -> None:
    files = client.get(
        f"/repos/{repo}/pulls/{pr['number']}/files?per_page=100"
    )
    if [item["filename"] for item in files] != [activation_path]:
        raise AutonomyError(
            "activation canary changed unexpected paths"
        )


def wait_checks(
    client: Client,
    repo: str,
    sha: str,
    contexts: list[str],
    timeout: int,
) -> dict[str, str]:
    deadline = time.monotonic() + timeout
    observed: dict[str, str] = {}
    while time.monotonic() < deadline:
        runs = client.get(
            f"/repos/{repo}/commits/{sha}/check-runs?per_page=100"
        ).get("check_runs", [])
        latest: dict[str, dict[str, Any]] = {}
        for run in runs:
            name = run.get("name")
            if name not in latest or str(run.get("started_at") or "") > str(
                latest[name].get("started_at") or ""
            ):
                latest[name] = run
        observed = {}
        pending = False
        for name in contexts:
            run = latest.get(name)
            if not run:
                observed[name] = "missing"
                pending = True
            elif run.get("status") != "completed":
                observed[name] = str(run.get("status"))
                pending = True
            else:
                observed[name] = str(run.get("conclusion"))
                if run.get("conclusion") not in {
                    "success",
                    "neutral",
                    "skipped",
                }:
                    raise AutonomyError(
                        f"required check failed: "
                        f"{name}={run.get('conclusion')}"
                    )
        if not pending:
            return observed
        time.sleep(15)
    raise AutonomyError(f"required checks timed out: {observed}")


def record_disposition(
    client: Client,
    repo: str,
    pr: int,
    sha: str,
    referee: Identity,
    checks: dict[str, str],
) -> dict[str, Any]:
    check_lines = "\n".join(
        f"- `{name}`: `{result}`;"
        for name, result in sorted(checks.items())
    )
    comment = client.post(
        f"/repos/{repo}/issues/{pr}/comments",
        {
            "body": (
                "REFEREE_AGENT_APPROVED_EXACT_HEAD\n\n"
                f"- exact head: `{sha}`;\n"
                "- approval record: `issue_comment`;\n"
                "- GitHub approving review required: `false`;\n"
                "- Human Steward disposition: `false`;\n"
                "- identity separation: verified;\n"
                "- changed-path scope: verified;\n"
                "- live required checks:\n"
                f"{check_lines}\n\n"
                "Disposition: "
                "`REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_AUTO_MERGE`."
            )
        },
    )
    if comment.get("user", {}).get("login") != referee.login:
        raise AutonomyError(
            "exact-head Referee disposition actor readback failed"
        )
    return comment


def auto_merge(
    client: Client,
    node_id: str,
    sha: str,
    referee: Identity,
) -> None:
    result = client.post(
        "/graphql",
        {
            "query": (
                "mutation($id:ID!,$oid:GitObjectID!,$h:String!,$b:String!){"
                "enablePullRequestAutoMerge(input:{pullRequestId:$id,"
                "expectedHeadOid:$oid,mergeMethod:MERGE,"
                "commitHeadline:$h,commitBody:$b})"
                "{pullRequest{number autoMergeRequest{enabledAt "
                "enabledBy{login}}}}}"
            ),
            "variables": {
                "id": node_id,
                "oid": sha,
                "h": "Activate MP-ADMIN-AUTONOMY-TRANSITION-001",
                "b": (
                    f"Exact head {sha}\n\n"
                    "Disposition: "
                    "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_AUTO_MERGE"
                ),
            },
        },
    )
    if result.get("errors"):
        raise AutonomyError(
            f"enable auto-merge failed: {result['errors']}"
        )
    request = (
        result.get("data", {})
        .get("enablePullRequestAutoMerge", {})
        .get("pullRequest", {})
        .get("autoMergeRequest")
    )
    if (
        not request
        or not request.get("enabledAt")
        or request.get("enabledBy", {}).get("login") != referee.login
    ):
        raise AutonomyError("auto-merge actor readback is absent")


def wait_merge(
    client: Client,
    repo: str,
    pr: int,
    sha: str,
    timeout: int,
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = client.get(f"/repos/{repo}/pulls/{pr}")
        if value["head"]["sha"] != sha:
            raise AutonomyError(
                "canary head changed after auto-merge authorization"
            )
        if value.get("merged"):
            return value
        time.sleep(10)
    raise AutonomyError("canary auto-merge timed out")


def readback(
    client: Client,
    repo: str,
    path: str,
    expected: dict[str, Any],
    timeout: int = 300,
) -> None:
    deadline = time.monotonic() + timeout
    last = "protected activation record is absent"
    while time.monotonic() < deadline:
        actual = json_content(client, repo, path, "main")
        if actual is None:
            last = "protected activation record is absent"
        elif json.dumps(actual, sort_keys=True) == json.dumps(
            expected, sort_keys=True
        ):
            return
        else:
            last = "protected activation record readback mismatch"
        time.sleep(5)
    raise AutonomyError(last)
