#!/usr/bin/env python3
"""Apply and verify the Grand Challenge release-trust administration contract."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import sys
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from github_http import build_github_opener

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
RULESET_NAMES = {
    "grandchallenge/MATHCERT": "Cert profile - main",
    "grandchallenge/MATHSOLVE": "Solve profile - main",
    "grandchallenge/MATH-PROGRAMME": "Programme profile - main",
    "grandchallenge/INTELLECT": "Provider profile - main",
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
        "grandchallenge/MATHCERT": [
            "certify",
            "policy / policy",
            "security / action-policy",
        ],
        "grandchallenge/MATHSOLVE": [
            "ledgers",
            "policy / policy",
            "security / action-policy",
        ],
        "grandchallenge/MATH-PROGRAMME": [
            "validate-json",
            "Replay LOG-GCD-001 in Lean",
            "Replay PC-WP04 bounded certificate",
            "Replay pinned Union-Closed MATHCERT evidence",
            "policy / policy",
            "security / action-policy",
        ],
        "grandchallenge/INTELLECT": [
            "test (3.11.14)",
            "test (3.12.13)",
            "policy / policy",
            "security / action-policy",
        ],
    }
    if checks != expected_checks:
        raise ReleaseTrustError("required status-check context set drift")


def ruleset_payload(
    name: str, policy: dict[str, Any], contexts: list[str]
) -> dict[str, Any]:
    rules: list[dict[str, Any]] = [
        {"type": "deletion"},
        {"type": "non_fast_forward"},
        {
            "type": "pull_request",
            "parameters": {
                "allowed_merge_methods": ["merge", "squash"],
                "dismiss_stale_reviews_on_push": policy["dismiss_stale_reviews"],
                "require_code_owner_review": policy["require_code_owner_reviews"],
                "require_last_push_approval": policy["require_last_push_approval"],
                "required_approving_review_count": policy["required_approving_reviews"],
                "required_review_thread_resolution": policy[
                    "required_conversation_resolution"
                ],
                "required_reviewers": [],
                "dismissal_restriction": {"enabled": False, "allowed_actors": []},
            },
        },
        {
            "type": "required_status_checks",
            "parameters": {
                "do_not_enforce_on_create": False,
                "strict_required_status_checks_policy": policy["strict_status_checks"],
                "required_status_checks": [
                    {"context": context} for context in contexts
                ],
            },
        },
    ]
    if policy["required_linear_history"]:
        rules.append({"type": "required_linear_history"})
    return {
        "name": name,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {
            "ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}
        },
        "rules": rules,
    }


def normalize_ruleset(ruleset: dict[str, Any]) -> dict[str, Any]:
    rules = {
        str(rule.get("type")): rule
        for rule in ruleset.get("rules", [])
        if isinstance(rule, dict)
    }
    status = rules.get("required_status_checks", {}).get("parameters", {})
    reviews = rules.get("pull_request", {}).get("parameters", {})
    bypass = ruleset.get("bypass_actors") or []
    conditions = ruleset.get("conditions") or {}
    ref_name = conditions.get("ref_name") or {}
    return {
        "name": str(ruleset.get("name") or ""),
        "target": str(ruleset.get("target") or ""),
        "enforcement": str(ruleset.get("enforcement") or ""),
        "ref_include": sorted(str(value) for value in ref_name.get("include") or []),
        "ref_exclude": sorted(str(value) for value in ref_name.get("exclude") or []),
        "url": str(
            (ruleset.get("_links") or {}).get("self", {}).get("href")
            or ruleset.get("source")
            or ""
        ),
        "strict_status_checks": bool(status.get("strict_required_status_checks_policy")),
        "required_checks": sorted(
            str(check.get("context"))
            for check in status.get("required_status_checks", [])
            if isinstance(check, dict) and check.get("context")
        ),
        "enforce_admins": not bool(bypass),
        "required_approving_reviews": int(
            reviews.get("required_approving_review_count") or 0
        ),
        "dismiss_stale_reviews": bool(reviews.get("dismiss_stale_reviews_on_push")),
        "require_last_push_approval": bool(
            reviews.get("require_last_push_approval")
        ),
        "require_code_owner_reviews": bool(reviews.get("require_code_owner_review")),
        "required_conversation_resolution": bool(
            reviews.get("required_review_thread_resolution")
        ),
        "allow_force_pushes": "non_fast_forward" not in rules,
        "allow_deletions": "deletion" not in rules,
        "required_linear_history": "required_linear_history" in rules,
        "bypass_actors": {
            "users": [],
            "teams": [],
            "apps": [
                str(actor.get("actor_id"))
                for actor in bypass
                if isinstance(actor, dict)
            ],
        },
    }


def ruleset_errors(
    normalized: dict[str, Any],
    policy: dict[str, Any],
    contexts: list[str],
    expected_name: str,
) -> list[str]:
    errors: list[str] = []
    structural_expectations = {
        "name": expected_name,
        "target": "branch",
        "enforcement": "active",
        "ref_include": ["~DEFAULT_BRANCH"],
        "ref_exclude": [],
    }
    for key, value in structural_expectations.items():
        if normalized.get(key) != value:
            errors.append(f"{key} drift: {normalized.get(key)!r} != {value!r}")
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
        errors.append(f"repository ruleset has bypass actors: {bypass}")
    if not normalized.get("url"):
        errors.append("repository ruleset has no stable API identity")
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
        self.opener = build_github_opener()

    @staticmethod
    def url(path_or_url: str) -> str:
        return path_or_url if path_or_url.startswith("https://") else f"{API_ROOT}{path_or_url}"

    def request_bytes(self, method: str, path_or_url: str, data: Any | None = None) -> bytes:
        body = None if data is None else json.dumps(data).encode("utf-8")
        request = urllib.request.Request(
            self.url(path_or_url), data=body, headers=self.headers, method=method
        )
        try:
            with self.opener.open(request, timeout=90) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise ReleaseTrustError(
                f"GitHub API {method} {path_or_url} failed with {exc.code}: {detail}"
            ) from exc

    def request(self, method: str, path_or_url: str, data: Any | None = None) -> Any:
        raw = self.request_bytes(method, path_or_url, data)
        return json.loads(raw) if raw else None


def fetch_public_bytes(url: str, expected_sha: str) -> bytes:
    separator = "&" if "?" in url else "?"
    request = urllib.request.Request(
        f"{url}{separator}expected_sha={urllib.parse.quote(expected_sha)}&ts={int(time.time())}",
        headers={
            "Accept-Encoding": "identity",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "grandchallenge-release-trust-admin",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            return response.read()
    except urllib.error.URLError as exc:
        raise ReleaseTrustError(f"public Pages site is unavailable: {exc}") from exc


def branch_ruleset(client: GitHubClient, repository: str) -> dict[str, Any]:
    listing = client.request("GET", f"/repos/{repository}/rulesets")
    candidates = [
        item
        for item in listing
        if item.get("target") == "branch" and item.get("enforcement") == "active"
    ]
    if len(candidates) != 1:
        raise ReleaseTrustError(
            f"{repository}: expected exactly one active branch ruleset, found "
            f"{len(candidates)}"
        )
    ruleset_id = candidates[0].get("id")
    if not ruleset_id:
        raise ReleaseTrustError(f"{repository}: active branch ruleset has no id")
    return client.request("GET", f"/repos/{repository}/rulesets/{ruleset_id}")


def apply_contract(client: GitHubClient, contract: dict[str, Any]) -> None:
    pages = contract["pages"]
    client.request("PATCH", f"/repos/{pages['repository']}", {"homepage": pages["homepage"]})
    policy = contract["branch_policy"]
    for entry in contract["repositories"]:
        repository = entry["repository"]
        current = branch_ruleset(client, repository)
        ruleset_id = current["id"]
        client.request(
            "PUT",
            f"/repos/{repository}/rulesets/{ruleset_id}",
            ruleset_payload(
                RULESET_NAMES[repository], policy, entry["required_checks"]
            ),
        )


def latest_workflow_run(
    client: GitHubClient,
    repository: str,
    workflow_file: str,
    branch: str,
    head_sha: str,
    event: str,
) -> dict[str, Any] | None:
    query = urllib.parse.urlencode(
        {"branch": branch, "event": event, "status": "success", "per_page": 100}
    )
    listing = client.request(
        "GET", f"/repos/{repository}/actions/workflows/{workflow_file}/runs?{query}"
    )
    for run in listing.get("workflow_runs", []):
        if run.get("head_sha") == head_sha and run.get("conclusion") == "success":
            return run
    return None


def validated_site_index(
    client: GitHubClient,
    repository: str,
    policy_run_id: int,
    artifact_name: str,
    archive_name: str,
    checksum_name: str,
) -> tuple[bytes, dict[str, Any]]:
    listing = client.request(
        "GET", f"/repos/{repository}/actions/runs/{policy_run_id}/artifacts?per_page=100"
    )
    matches = [
        artifact
        for artifact in listing.get("artifacts", [])
        if artifact.get("name") == artifact_name and not artifact.get("expired")
    ]
    if len(matches) != 1:
        raise ReleaseTrustError(
            f"expected exactly one unexpired {artifact_name} artifact for run {policy_run_id}, found {len(matches)}"
        )
    artifact = matches[0]
    declared_digest = str(artifact.get("digest") or "")
    if not declared_digest.startswith("sha256:"):
        raise ReleaseTrustError(f"workflow artifact lacks a SHA-256 digest: {declared_digest!r}")
    artifact_zip = client.request_bytes("GET", str(artifact["archive_download_url"]))
    outer_sha = hashlib.sha256(artifact_zip).hexdigest()
    if outer_sha != declared_digest.split(":", 1)[1]:
        raise ReleaseTrustError("workflow artifact SHA-256 mismatch")

    with zipfile.ZipFile(io.BytesIO(artifact_zip)) as bundle:
        names = set(bundle.namelist())
        if archive_name not in names or checksum_name not in names:
            raise ReleaseTrustError("validated-site artifact is missing archive or checksum")
        archive_bytes = bundle.read(archive_name)
        checksum_fields = bundle.read(checksum_name).decode("utf-8").split()
    if len(checksum_fields) != 2 or checksum_fields[1] != archive_name:
        raise ReleaseTrustError("validated-site checksum record is malformed")
    inner_sha = hashlib.sha256(archive_bytes).hexdigest()
    if inner_sha != checksum_fields[0]:
        raise ReleaseTrustError("validated-site inner SHA-256 mismatch")

    index_bytes: bytes | None = None
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
        for member in archive.getmembers():
            normalized = member.name.lstrip("./")
            if normalized == "index.html":
                handle = archive.extractfile(member)
                if handle is None:
                    raise ReleaseTrustError("validated-site index.html is not a regular file")
                index_bytes = handle.read()
                break
    if index_bytes is None:
        raise ReleaseTrustError("validated-site archive has no index.html")
    return index_bytes, {
        "artifact_id": artifact.get("id"),
        "artifact_url": artifact.get("url"),
        "artifact_sha256": outer_sha,
        "site_archive_sha256": inner_sha,
        "index_sha256": hashlib.sha256(index_bytes).hexdigest(),
    }


def verify_contract(client: GitHubClient, contract: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    pages = contract["pages"]
    policy = contract["branch_policy"]
    repo_metadata = client.request("GET", f"/repos/{pages['repository']}")
    homepage = str(repo_metadata.get("homepage") or "")
    if homepage.rstrip("/") != pages["homepage"].rstrip("/"):
        errors.append(f"repository homepage drift: {homepage!r} != {pages['homepage']!r}")

    rulesets: list[dict[str, Any]] = []
    for entry in contract["repositories"]:
        repository = entry["repository"]
        raw = branch_ruleset(client, repository)
        normalized = normalize_ruleset(raw)
        current_errors = ruleset_errors(
            normalized,
            policy,
            entry["required_checks"],
            RULESET_NAMES[repository],
        )
        errors.extend(f"{repository}: {message}" for message in current_errors)
        rulesets.append(
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

    policy_run = (
        latest_workflow_run(
            client,
            pages["repository"],
            pages["policy_workflow_file"],
            pages["branch"],
            main_sha,
            "push",
        )
        if main_sha
        else None
    )
    pages_run = (
        latest_workflow_run(
            client,
            pages["repository"],
            pages["pages_workflow_file"],
            pages["branch"],
            main_sha,
            "workflow_run",
        )
        if main_sha
        else None
    )
    if policy_run is None:
        errors.append(f"no successful policy workflow run is tied to current main {main_sha}")
    if pages_run is None:
        errors.append(f"no successful Pages workflow run is tied to current main {main_sha}")

    artifact_evidence: dict[str, Any] | None = None
    live_index_sha = ""
    if policy_run is not None:
        expected_index, artifact_evidence = validated_site_index(
            client,
            pages["repository"],
            int(policy_run["id"]),
            pages["artifact_name"],
            pages["archive_name"],
            pages["checksum_name"],
        )
        live_index = fetch_public_bytes(pages["public_url"], main_sha)
        live_index_sha = hashlib.sha256(live_index).hexdigest()
        if live_index != expected_index:
            errors.append(
                "public Pages index does not byte-match the current-main validated-site artifact: "
                f"{live_index_sha} != {artifact_evidence['index_sha256']}"
            )

    def run_evidence(run: dict[str, Any] | None) -> dict[str, Any] | None:
        if run is None:
            return None
        return {
            "id": run.get("id"),
            "html_url": run.get("html_url"),
            "head_sha": run.get("head_sha"),
            "conclusion": run.get("conclusion"),
            "event": run.get("event"),
            "created_at": run.get("created_at"),
            "updated_at": run.get("updated_at"),
        }

    evidence = {
        "schema_version": "1.0.0",
        "evidence_id": "ORG-REL-TRUST-01-EVIDENCE",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "contract_sha256": canonical_sha256(contract),
        "repository_homepage": homepage,
        "current_main_sha": main_sha,
        "policy_workflow_run": run_evidence(policy_run),
        "pages_workflow_run": run_evidence(pages_run),
        "validated_site_artifact": artifact_evidence,
        "live_index_sha256": live_index_sha,
        "repository_rulesets": rulesets,
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
    artifact = evidence["validated_site_artifact"] or {}
    issue_comment(
        client,
        repository,
        contract["issues"]["pages"],
        "Release-trust administration passed. "
        f"Homepage matches; Pages run `{pages_run.get('id')}` succeeded for current main "
        f"`{evidence['current_main_sha']}`; the live index byte-matches validated-site artifact "
        f"`{artifact.get('artifact_id')}` at SHA-256 `{artifact.get('index_sha256')}`. "
        f"Evidence SHA-256: `{evidence_sha}`.",
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
