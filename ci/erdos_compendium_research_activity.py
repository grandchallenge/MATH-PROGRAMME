#!/usr/bin/env python3
"""One-pass recent Erdős research-activity discovery for editorial triage.

Metadata is *not* accepted mathematical status. Never promote automatically.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TITLE_ID = re.compile(r"(?i)(?:ERDOS[-_ ]|ERD[ŐO]S\s*(?:PROBLEM\s*)?#?\s*)(\d{1,4})(?!\d)")

def read_activity(registry: dict, sources: dict[str, dict], *, limit: int = 60) -> dict:
    if limit < 1 or limit > 100:
        raise ValueError("bounded output limit required")
    by_issue = {x["issue_number"]: x["problem_id"] for x in registry["issues"]}
    ids = set(by_issue.values())
    if len(ids) != 1221:
        raise ValueError("catalogue identity drift")
    hits = []
    truncation = False
    for repo, page in sources.items():
        if repo not in {"MATH-PROGRAMME", "MATHSOLVE", "MATHCERT"}:
            raise ValueError("unregistered source")
        if not isinstance(page.get("items"), list) or not isinstance(page.get("total_count"), int):
            raise ValueError("missing search pagination evidence")
        if page["total_count"] > len(page["items"]):
            truncation = True
        for item in page["items"]:
            if "pull_request" in item:
                continue
            title = item.get("title", "")
            number = item.get("number")
            if repo == "MATH-PROGRAMME" and number in by_issue:
                n = by_issue[number]
            else:
                found = TITLE_ID.search(title)
                if not found:
                    continue
                n = int(found.group(1))
            if n not in ids:
                continue
            hits.append({
                "problem_id": n,
                "repository": "grandchallenge/" + repo,
                "issue_number": number,
                "source_updated_at": item.get("updated_at"),
                "source_url": item.get("html_url"),
                "triage_state": "RECENT_RESEARCH_ACTIVITY_UNADJUDICATED",
                "mathematical_authority": False,
            })
    hits.sort(key=lambda x: (x["source_updated_at"] or "", x["repository"], x["issue_number"]), reverse=True)
    return {
        "record_type": "ERDOS_COMPENDIUM_RECENT_RESEARCH_ACTIVITY/1",
        "authority": "READ_ONLY_INDEXED_ISSUE_METADATA",
        "sampled_repositories": sorted(sources),
        "matching_source_issues_observed": len(hits),
        "truncated_input": truncation,
        "activity_candidates": hits[:limit],
        "automatic_status_promotion": False,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--registry", type=Path, required=True)
    for repo in ("programme", "solve", "cert"):
        p.add_argument("--" + repo + "-issues", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    registry = json.loads(args.registry.read_text(encoding="utf-8"))
    sources = {
        "MATH-PROGRAMME": json.loads(args.programme_issues.read_text(encoding="utf-8")),
        "MATHSOLVE": json.loads(args.solve_issues.read_text(encoding="utf-8")),
        "MATHCERT": json.loads(args.cert_issues.read_text(encoding="utf-8")),
    }
    data = read_activity(registry, sources)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("Recent Erdős issue updates to triage:", data["matching_source_issues_observed"])
    if data["truncated_input"]:
        print("::warning::Recent issue search truncated; treat as a sample, not exhaustive monitoring")

if __name__ == "__main__":
    main()
