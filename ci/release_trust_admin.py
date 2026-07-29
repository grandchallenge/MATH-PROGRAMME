#!/usr/bin/env python3
"""Apply and verify the Grand Challenge release-trust administration contract."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "governance" / "release_trust_admin_contract.json"
DEFAULT_SCHEMA = ROOT / "schemas" / "release_trust_admin_contract.schema.json"
DEFAULT_EVIDENCE = ROOT / "release-trust-evidence.json"
API_ROOT = "https://api.github.com"
EXPECTED_REPOSITORIES = {
    "grandchallenge/MATHCERT",
    "grandchallenge/MATHSOLVE",
    "grandchallenge/MATH-PROGRAMME",
    "grandchallenge/INTELLECT",
}


class ReleaseTrustError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_contract(contract: dict[str, Any], schema: dict[str, Any]) -> None:
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(contract),
        key=lambda error: list(error.path),
    )
    if errors:
        raise ReleaseTrustError(
            "; ".join(f"{error.json_path}: {error.message}" for error in errors)
        )
    repositories = contract["repositories"]
    names = [entry["repository"] for entry in repositories]
    if len(names) != len(set(names)):
        raise ReleaseTrustError("release-trust contract contains duplicate repositories")
    if set(names) != EXPECTED_REPOSITORIES:
        raise ReleaseTrustError("release-trust repository set drift")
    checks = {entry["repository"]: entry["required_checks"] for entry in repositories}
    expected_checks = {
        "grandchallenge/MATHCERT": ["certify"],
        "grandchallenge/MATHSOLVE": ["ledgers"],
        "grandchallenge/MATH-PROGRAMME": [
            "validate-json",
            "Replay LOG-GCD-001 in Lean",
            "Replay PC-WP04 bounded certificate",
            "Replay pinned Union-Closed MATHCERT evidence",
        ],
        "grandchallenge/INTELLECT": ["test (3.11.14)", "test (3.12.13)"],
    }
    if checks != expected_checks:
        raise ReleaseTrustError("required status-check context set drift")


def protection_payload(policy: dict[str, Any], contexts: list[str]) -> dict[str, Any]:
    return {
        "required_status_checks": {
            "strict": policy["strict_status_checks"],
            "contexts": contexts,
        },
        "enforce_admins": policy["enforce_admins"],
        "required_pull_request_reviews": {
            "dismissal_restrictions": {"users": [], "teams": []},
            "dismiss_stale_reviews": policy["dismiss_stale_reviews"],
            "require_code_owner_reviews": policy["require_code_owner_reviews"],
            "required_approving_review_count": policy["required_approving_reviews"],
            "require_last_push_approval": policy["require_last_push_approval"],
            "bypass_pull_request_allowances": {"users": [], "teams": [], "apps": []},
        },
        "restrictions": None,
        "required_linear_history": policy["required_linear_history"],
        "allow_force_pushes": policy["allow_force_pushes"],
        "allow_deletions": policy["allow_deletions"],
        "block_creations": False,
        "required_conversation_resolution": policy["required_conversation_resolution"],
        "lock_branch": False,
        "allow_fork_syncing": True,
    }


def enabled(value: Any) -> bool:
    if isinstance(value, dict):
        return bool(value.get("enabled"))
    return bool(value)


def actor_names(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    names: list[str] = []
    for actor in value:
        if isinstance(actor, dict):
            names.append(str(actor.get("slug") or actor.get("login") or actor.get("name") or ""))
        elif actor is not None:
            names.append(str(actor))
    return sorted(name for name in names if name)


def normalize_protection(protection: dict[str, Any]) -> dict[str, Any]:
    status = protection.get("required_status_checks") or {}
    contexts = list(status.get("contexts") or [])
    for check in status.get("checks") or []:
        if isinstance(check, dict) and check.get("context"):
            contexts.append(str(check["context"]))
    reviews = protection.get("required_pull_request_reviews") or {}
    bypass = reviews.get("bypass_pull_request_allowances") or {}
    return {
        "url": str(protection.get("url", "")),
        "strict_status_checks": bool(status.get("strict")),
        "required_checks": sorted(set(contexts)),
        "enforce_admins": enabled(protection.get("enforce_admins")),
        "required_approving_reviews": int(reviews.get("required_approving_review_count") or 0),
        "dismiss_stale_reviews": bool(reviews.get("dismiss_stale_reviews")),
        "require_last_push_approval": bool(reviews.get("require_last_push_approval")),
        "require_code_owner_reviews": bool(reviews.get("require_code_owner_reviews")),
        "required_conversation_resolution": enabled(
            protection.get("required_conversation_resolution")
        ),
        "allow_force_pushes": enabled(protection.get("allow_force_pushes")),
        "allow_deletions": enabled(protection.get("allow_deletions")),
        "required_linear_history": enabled(protection.get("required_linear_history")),
        "bypass_actors": {
            "users": actor_names(bypass.get("users")),
            "teams": actor_names(bypass.get("teams")),
            "apps": actor_names(bypass.get("apps")),
        },
    }


def protection_errors(
    normalized: dict[str, Any], policy: dict[str, Any], contexts: list[str]
) -> list[str]:
    errors: list[str] = []
    expected = {
        "strict_status_checks": policy["strict_status_checks"],
        "required_checks": sorted(contexts),
        "enforce_admins": policy["enforce_admins"],
        "required_approving_reviews": policy["required_approving_reviews"],
        "dismiss_stale_reviews": policy["dismiss_stale_reviews"],
        "require_last_push_approval": policy["require_last_push_approval"],
        "require_code_owner_reviews": policy["require_code_owner_reviews"],
        "required_conversation_resolution": policy["required_conversation_resolution"],
        "allow_force_pushes": policy["allow_force_pushes"],
        "allow_deletions": policy["allow_deletions"],
        "required_linear_history": policy["required_linear_history"],
    }
    for key, value in expected.items():
        if normalized.get(key) != value:
            errors.append(f"{key} drift: {normalized.get(key)!r} != {value!r}")
    bypass = normalized.get("bypass_actors", {})
    if any(bypass.get(kind) for kind in ("users", "teams", "apps")):
        errors.append(f"branch protection has bypass actors: {bypass}")
    if not normalized.get("url"):
        errors.append("branch protection has no stable API URL")
    return errors


class GitHubClient:
    def __init__(self, token: str, api_version: str):
        if not token:
            raise ReleaseTrustError("administration token is empty")
        self.headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": api_version,
            "User-Agent": "grandchallenge-release-trust-admin",
        }

    def request(self, method: str, path: str, data: Any | None = None) -> Any:
        body = None if data is None else json.dumps(data).encode("utf-8")
        request = urllib.request.Request(
            f"{API_ROOT}{path}", data=body, headers=self.headers, method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                raw = response.read()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ReleaseTrustError(
                f"GitHub API {method} {path} failed with {exc.code}: {detail}"
            ) from exc


def fetch_public_json(url: str, expected_sha: str) -> dict[str, Any]:
    separator = "&" if "?" in url else "?"
    request = urllib.request.Request(
        f"{url}{separator}expected_sha={urllib.parse.quote(expected_sha)}&ts={int(time.time())}",
        headers={"Cache-Control": "no-cache", "User-Agent": "grandchallenge-release-trust-admin"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        raise ReleaseTrustError(f"public revision marker is unavailable or invalid: {exc}") from exc


def apply_contract(client: GitHubClient, contract: dict[str, Any]) -> None:
    pages = contract["pages"]
    client.request("PATCH", f"/repos/{pages['repository']}", {"homepage": pages["homepage"]})
    policy = contract["branch_policy"]
    for entry in contract["repositories"]:
        repository = entry["repository"]
        branch = urllib.parse.quote(entry["branch"], safe="")
        client.request(
            "PUT",
            f"/repos/{repository}/branches/{branch}/protection",
            protection_payload(policy, entry["required_checks"]),
        )


def latest_pages_run(
    client: GitHubClient, repository: str, workflow_file: str, branch: str, head_sha: str
) -> dict[str, Any] | None:
    query = urllib.parse.urlencode(
        {"branch": branch, "status": "success", "per_page": 100}
    )
    listing = client.request(
        "GET", f"/repos/{repository}/actions/workflows/{workflow_file}/runs?{query}"
    )
    for run in listing.get("workflow_runs", []):
        if run.get("head_sha") == head_sha and run.get("conclusion") == "success":
            return run
    return None


def verify_contract(client: GitHubClient, contract: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    pages = contract["pages"]
    policy = contract["branch_policy"]
    repo_metadata = client.request("GET", f"/repos/{pages['repository']}")
    homepage = str(repo_metadata.get("homepage") or "")
    if homepage.rstrip("/") != pages["homepage"].rstrip("/"):
        errors.append(f"repository homepage drift: {homepage!r} != {pages['homepage']!r}")

    protections: list[dict[str, Any]] = []
    for entry in contract["repositories"]:
        repository = entry["repository"]
        branch = urllib.parse.quote(entry["branch"], safe="")
        raw = client.request("GET", f"/repos/{repository}/branches/{branch}/protection")
        normalized = normalize_protection(raw)
        current_errors = protection_errors(normalized, policy, entry["required_checks"])
        errors.extend(f"{repository}: {message}" for message in current_errors)
        protections.append(
            {
                "repository": repository,
                "branch": entry["branch"],
                "snapshot": normalized,
                "snapshot_sha256": canonical_sha256(normalized),
            }
        )

    branch_data = client.request(
        "GET", f"/repos/{pages['repository']}/branches/{urllib.parse.quote(pages['branch'], safe='')}"
    )
    main_sha = str(branch_data.get("commit", {}).get("sha") or "")
    if len(main_sha) != 40:
        errors.append(f"current main identity is invalid: {main_sha!r}")
    marker = fetch_public_json(pages["revision_marker_url"], main_sha) if main_sha else {}
    if marker.get("repository") != pages["repository"]:
        errors.append("public revision marker repository mismatch")
    if marker.get("head_sha") != main_sha:
        errors.append(
            f"public revision marker is stale: {marker.get('head_sha')!r} != {main_sha!r}"
        )
    pages_run = (
        latest_pages_run(
            client,
            pages["repository"],
            pages["workflow_file"],
            pages["branch"],
            main_sha,
        )
        if main_sha
        else None
    )
    if pages_run is None:
        errors.append(f"no successful Pages workflow run is tied to current main {main_sha}")

    evidence = {
        "schema_version": "1.0.0",
        "evidence_id": "ORG-REL-TRUST-01-EVIDENCE",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "contract_sha256": canonical_sha256(contract),
        "repository_homepage": homepage,
        "current_main_sha": main_sha,
        "public_revision_marker": marker,
        "pages_workflow_run": None
        if pages_run is None
        else {
            "id": pages_run.get("id"),
            "html_url": pages_run.get("html_url"),
            "head_sha": pages_run.get("head_sha"),
            "conclusion": pages_run.get("conclusion"),
            "event": pages_run.get("event"),
            "created_at": pages_run.get("created_at"),
            "updated_at": pages_run.get("updated_at"),
        },
        "branch_protections": protections,
        "verified": not errors,
        "errors": errors,
    }
    evidence["evidence_sha256"] = canonical_sha256(evidence)
    if errors:
        raise ReleaseTrustError("; ".join(errors))
    return evidence


def issue_comment(client: GitHubClient, repository: str, issue: int, body: str) -> None:
    client.request("POST", f"/repos/{repository}/issues/{issue}/comments", {"body": body})


def close_child_issues(client: GitHubClient, contract: dict[str, Any], evidence: dict[str, Any]) -> None:
    repository = contract["pages"]["repository"]
    evidence_sha = evidence["evidence_sha256"]
    pages_run = evidence["pages_workflow_run"] or {}
    issue_comment(
        client,
        repository,
        contract["issues"]["pages"],
        "Release-trust administration passed. "
        f"Homepage and public revision marker match current main `{evidence['current_main_sha']}`; "
        f"Pages run `{pages_run.get('id')}` succeeded. Evidence SHA-256: `{evidence_sha}`.",
    )
    client.request(
        "PATCH",
        f"/repos/{repository}/issues/{contract['issues']['pages']}",
        {"state": "closed", "state_reason": "completed"},
    )
    issue_comment(
        client,
        repository,
        contract["issues"]["protected_branches"],
        "Release-trust administration passed for MATHCERT, MATHSOLVE, MATH-PROGRAMME, and INTELLECT. "
        "Strict required checks, pull-request review, admin enforcement, conversation resolution, "
        f"and zero bypass actors were verified. Evidence SHA-256: `{evidence_sha}`.",
    )
    client.request(
        "PATCH",
        f"/repos/{repository}/issues/{contract['issues']['protected_branches']}",
        {"state": "closed", "state_reason": "completed"},
    )
    issue_comment(
        client,
        repository,
        contract["issues"]["umbrella"],
        "Administrative children #7 and #125 are discharged. Rerun the governed umbrella audit, "
        "admit the exact evidence artifact, set `operational_release_complete: true`, and only then close #6. "
        f"Evidence SHA-256: `{evidence_sha}`.",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("validate", "verify", "apply"), default="validate")
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--token-env", default="GCL_REPOSITORY_ADMIN_TOKEN")
    parser.add_argument("--wait-seconds", type=int, default=0)
    parser.add_argument("--close-child-issues", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        contract = load_json(args.contract)
        schema = load_json(args.schema)
        validate_contract(contract, schema)
        if args.mode == "validate":
            print("release-trust administration contract is valid")
            return 0
        token = os.environ.get(args.token_env, "")
        client = GitHubClient(token, contract["api_version"])
        if args.mode == "apply":
            apply_contract(client, contract)
        deadline = time.monotonic() + max(args.wait_seconds, 0)
        while True:
            try:
                evidence = verify_contract(client, contract)
                break
            except ReleaseTrustError:
                if time.monotonic() >= deadline:
                    raise
                time.sleep(min(30, max(1, int(deadline - time.monotonic()))))
        args.evidence.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(evidence, indent=2))
        if args.close_child_issues:
            close_child_issues(client, contract, evidence)
        return 0
    except (OSError, json.JSONDecodeError, ReleaseTrustError) as exc:
        print(f"release-trust administration failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
