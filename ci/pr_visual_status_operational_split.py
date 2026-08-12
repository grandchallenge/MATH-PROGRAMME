#!/usr/bin/env python3
"""Credential-split runner for bounded advisory PRVSR Phase 1."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from autonomy_github import AutonomyError, Client
import pr_visual_status_operational as operational
import pr_visual_status_policy as policy
import pr_visual_status_transport as transport


class PublicReadClient:
    """Unauthenticated GET-only client for public-repository fallback reads."""

    def __init__(self, api: str = "https://api.github.com"):
        self.api = api.rstrip("/")

    def get(self, path: str) -> Any:
        req = urllib.request.Request(
            self.api + path,
            method="GET",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "gcl-prvsr-public-read-fallback",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                body = response.read()
                return json.loads(body) if body else None
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")
            raise AutonomyError(f"GET {path} failed: {exc.code} {detail}") from exc


class SplitCredentialClient:
    """Route reads and writes through least-authority credentials."""

    def __init__(
        self,
        source: Client,
        administration: Client,
        publisher: Client | None,
        public_read: PublicReadClient | None = None,
    ):
        self.source = source
        self.administration = administration
        self.publisher = publisher
        self.public_read = public_read or PublicReadClient()

    def get(self, path: str) -> Any:
        if "/rulesets" in path:
            return self.administration.get(path)
        try:
            return self.source.get(path)
        except AutonomyError as exc:
            text = str(exc)
            if " 403 " not in text and " 404 " not in text:
                raise
            return self.public_read.get(path)

    def post(self, path: str, payload: dict[str, Any]) -> Any:
        if self.publisher is None:
            raise operational.OperationalError("publisher credential is unavailable")
        return self.publisher.post(path, payload)

    def patch(self, path: str, payload: dict[str, Any]) -> Any:
        if self.publisher is None:
            raise operational.OperationalError("publisher credential is unavailable")
        return self.publisher.patch(path, payload)


def build_client(
    source_token: str | None,
    administration_token: str | None,
    publisher_token: str | None,
    *,
    publish: bool,
) -> SplitCredentialClient:
    if not source_token:
        raise operational.OperationalError("GITHUB_TOKEN/source credential is required")
    if not administration_token:
        raise operational.OperationalError("GITHUB_ADMIN_TOKEN/administration credential is required")
    if publish and not publisher_token:
        raise operational.OperationalError("GITHUB_PUBLISH_TOKEN/publisher credential is required")
    supplied = [source_token, administration_token]
    if publisher_token:
        supplied.append(publisher_token)
    if len(set(supplied)) != len(supplied):
        raise operational.OperationalError("PRVSR credentials must remain distinct")
    return SplitCredentialClient(
        Client(source_token),
        Client(administration_token),
        Client(publisher_token) if publisher_token else None,
    )


def upsert_publisher_comment(
    client: SplitCredentialClient,
    repo: str,
    pr_number: int,
    body: str,
    publisher_login: str,
) -> int:
    if not publisher_login:
        raise operational.OperationalError("publisher login is unavailable")
    marker = operational.COMMENT_MARKER.format(pr_number=pr_number)
    comments = operational.paged(client, f"/repos/{repo}/issues/{pr_number}/comments?")
    for item in reversed(comments):
        if (
            marker in str(item.get("body") or "")
            and str(item.get("user", {}).get("login") or "") == publisher_login
        ):
            value = client.patch(
                f"/repos/{repo}/issues/comments/{item['id']}",
                {"body": f"{marker}\n{body}"},
            )
            return int(value["id"])
    value = client.post(
        f"/repos/{repo}/issues/{pr_number}/comments",
        {"body": f"{marker}\n{body}"},
    )
    return int(value["id"])


def publish_report(
    client: SplitCredentialClient,
    repo: str,
    pr_number: int,
    report: dict[str, Any],
    output_root: Path,
    config: dict[str, Any],
    publisher_login: str,
) -> dict[str, Any]:
    exact = report["identity"]["exact_head_sha"]
    before = client.get(f"/repos/{repo}/pulls/{pr_number}")
    if str(before.get("head", {}).get("sha") or "") != exact:
        raise operational.OperationalError("target PR head moved before archive publication")
    bundle_dir = transport.write_archive_bundle(
        report, output_root, target_head_before=exact, target_head_after=exact
    )
    archive_dir = transport.archive_relative_dir(report)
    branch = f"{config['archive_branch_prefix']}{pr_number}"
    archive_commit = operational.commit_bundle(
        client, repo, branch, bundle_dir, archive_dir, report["report_id"]
    )
    after = client.get(f"/repos/{repo}/pulls/{pr_number}")
    after_head = str(after.get("head", {}).get("sha") or "")
    if after_head != exact:
        operational.invalidate_receipt(client, repo, branch, archive_dir, after_head)
        raise operational.OperationalError("target PR head moved during publication; receipt invalidated")
    comment = transport.render_verified_pr_comment(bundle_dir)
    comment += (
        f"\nPhase 1 archive branch: `{branch}`\n"
        f"Archive path: `{archive_dir}/`\n"
        "Report generation or archive failure remains advisory and non-blocking.\n"
    )
    return {
        "archive_branch": branch,
        "archive_commit": archive_commit,
        "archive_dir": archive_dir,
        "comment_id": upsert_publisher_comment(
            client, repo, pr_number, comment, publisher_login
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", operational.ALLOWED_REPOSITORY))
    parser.add_argument("--pr", type=int, required=True)
    parser.add_argument("--source-token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--administration-token", default=os.environ.get("GITHUB_ADMIN_TOKEN"))
    parser.add_argument("--publisher-token", default=os.environ.get("GITHUB_PUBLISH_TOKEN"))
    parser.add_argument("--publisher-login", default=os.environ.get("GITHUB_PUBLISHER_LOGIN", ""))
    parser.add_argument("--observed-at")
    parser.add_argument("--output-root", default=".")
    parser.add_argument("--summary")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    try:
        client = build_client(
            args.source_token,
            args.administration_token,
            args.publisher_token,
            publish=args.publish,
        )
        config = operational.load_config()
        report, summary = operational.collect_report(
            client,
            args.repo,
            args.pr,
            args.observed_at or operational.utc_now(),
            config,
        )
        if report is not None:
            if args.publish:
                summary["publication"] = publish_report(
                    client,
                    args.repo,
                    args.pr,
                    report,
                    Path(args.output_root),
                    config,
                    args.publisher_login,
                )
            else:
                path = transport.write_archive_bundle(
                    report,
                    Path(args.output_root),
                    target_head_before=report["identity"]["exact_head_sha"],
                    target_head_after=report["identity"]["exact_head_sha"],
                )
                summary["local_bundle_dir"] = path.as_posix()
        operational.write_summary(args.summary, summary)
        return 0
    except (
        AutonomyError,
        operational.OperationalError,
        policy.ReportError,
        transport.TransportError,
        OSError,
    ) as exc:
        operational.write_summary(
            args.summary,
            {
                "selected": None,
                "repository": args.repo,
                "pr_number": args.pr,
                "error": str(exc),
                "authority_boundary": "ADVISORY_FAILURE__NO_MERGE_BLOCKER_CREATED",
            },
        )
        print(f"PRVSR Phase 1 advisory error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
