#!/usr/bin/env python3
"""Reconcile authenticated Erdős source returns into an existing bulk editorial intake.

Read-only GitHub interaction. The output file is a proposed manifest for normal
protected review, never a mathematical certificate or automatic admission.
No new issues, leases, labels, or branch mutations are created.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO = "grandchallenge/MATH-PROGRAMME"
ISSUES = "https://api.github.com/repos/" + REPO + "/issues/"
REQUIRED_SECTIONS = (
    "## Exact statement and normalization",
    "## Dated status and primary evidence",
    "## Strongest verified interface",
    "## Proposed bounded successor task",
    "## Prerequisites and blocker",
    "## Reuse and claim boundary",
)


def token() -> str:
    value = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if value:
        return value
    result = subprocess.run(
        ["gh", "auth", "token"], check=True, capture_output=True, text=True
    )
    value = result.stdout.strip()
    if not value:
        raise RuntimeError("No authenticated GitHub token")
    return value


def get_comments(issue_number: int, auth: str) -> list[dict]:
    """Fetch ALL pages so newer returns cannot be silently omitted."""
    result: list[dict] = []
    page = 1
    while True:
        url = ISSUES + str(issue_number) + "/comments?per_page=100&page=" + str(page)
        request = urllib.request.Request(
            url,
            headers={
                "Authorization": "Bearer " + auth,
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read())
        if not isinstance(data, list):
            raise ValueError("Unexpected GitHub issue-comment format")
        result.extend(data)
        if len(data) < 100:
            return result
        page += 1
        if page > 100:
            raise RuntimeError("Issue-comment pagination safety bound")


def valid_return(item: dict, comment: dict) -> bool:
    """Only accept actual posted RESULT/1, never mere mentions of the marker."""
    body = comment.get("body")
    author = comment.get("user") or {}
    if not isinstance(body, str) or not isinstance(author.get("login"), str):
        return False
    normalized = body.replace("\r\n", "\n").lstrip()
    if not normalized.startswith("RESULT/1\n"):
        return False
    n = item["problem_id"]
    expected = "ERDOS-CATALOGUE-" + f"{n:04d}" + "-S01"
    if not re.search(
        r"(?m)^ASSIGNMENT_ID: " + re.escape(expected) + r"\s*$", normalized
    ):
        return False
    if not re.search(
        r"(?m)^PROBLEM_ID: " + str(n) + r"\s*$", normalized
    ):
        return False
    if not re.search(
        r"(?m)^DISPOSITION: (SOURCE_LOCK_READY|BOUNDED_TASK_DESIGNED|STATUS_CONFLICT|EXACT_BLOCKER|PARTIAL)\s*$",
        normalized,
    ):
        return False
    return all(section in normalized for section in REQUIRED_SECTIONS)


def reconcile(manifest: dict, auth: str, workers: int = 12) -> tuple[dict, dict]:
    if manifest.get("record_type") != "ERDOS_COMPENDIUM_BULK_INTAKE/1":
        raise ValueError("Unexpected intake record type")
    items = manifest["items"]
    if (not isinstance(items, list) or len(items) != manifest["target_count"]
            or len({x["problem_id"] for x in items}) != len(items)):
        raise ValueError("Malformed or duplicate batch items")

    def one(item: dict) -> tuple[int, str | None, str | None]:
        comments = get_comments(item["audit_issue"], auth)
        eligible = [c for c in comments if valid_return(item, c)]
        if not eligible:
            return item["problem_id"], None, None
        latest = max(eligible, key=lambda c: c["id"])
        expected_prefix = "https://github.com/" + REPO + "/issues/" + str(item["audit_issue"])
        url = latest.get("html_url")
        if (not isinstance(url, str) or not re.fullmatch(
            re.escape(expected_prefix) + r"#issuecomment-[0-9]+", url
        )):
            raise ValueError("GitHub returned an invalid comment link")
        return item["problem_id"], url, latest["user"]["login"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(one, items))
    by_id = {n: (url, author) for n, url, author in results}
    ready = 0
    authors: set[str] = set()
    for item in items:
        url, author = by_id[item["problem_id"]]
        before = item["source_return"]
        if before is not None and url is None:
            raise ValueError("Previously captured source return disappeared for #" +
                             str(item["problem_id"]))
        if before is not None and url != before:
            # Do not silently replace previously cited source evidence.
            raise ValueError("Source return changed: inspect issue #" +
                             str(item["problem_id"]))
        item["source_return"] = url
        item["evidence_state"] = (
            "RESULT_PRESENT_UNADJUDICATED" if url else "NO_RESULT_AT_READBACK"
        )
        ready += bool(url)
        if author:
            authors.add(author)
    if isinstance(manifest.get("source_queue_readback"), dict):
        manifest["source_queue_readback"]["post_initial_source_return_count"] = ready
    manifest["observed_date"] = dt.datetime.now(dt.timezone.utc).date().isoformat()
    manifest["status_semantics"] = (
        f"{ready} authenticated issue-bound RESULT/1 source returns; "
        f"{len(items)-ready} without returns at this readback. "
        "These are source EVIDENCE ONLY: no automatic article acceptance, "
        "mathematical proof certification, or protected-merge authority."
    )
    summary = {
        "cohort_id": manifest["cohort_id"],
        "slots": len(items),
        "source_ready_unadjudicated": ready,
        "no_return": len(items) - ready,
        "authenticated_source_author_count": len(authors),
        "date": manifest["observed_date"],
        "authority": "READ_ONLY_LIVE_GITHUB_RECONCILIATION",
    }
    return manifest, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()
    if args.manifest.resolve() == args.output.resolve():
        parser.error("Write a separate proposed manifest; never overwrite source in place")
    if not 1 <= args.workers <= 16:
        parser.error("workers must be within 1..16")
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    proposed, report = reconcile(manifest, token(), args.workers)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(proposed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
