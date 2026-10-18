#!/usr/bin/env python3
"""Bounded, read-only catalogue capture. Worker statements remain unadjudicated."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "governance/erdos_catalogue/REGISTRY.json"
REPOSITORY = "grandchallenge/MATH-PROGRAMME"
MARKER = "RESULT/1"
KEYS = {"ASSIGNMENT_ID", "PROBLEM_ID", "DISPOSITION", "CONTEXT_CLASS", "TIMEBOX_OBSERVED"}
DISPOSITIONS = {
    "SOURCE_LOCK_READY": "SOURCE_REVIEW_REQUIRED",
    "BOUNDED_TASK_DESIGNED": "WORK_DESIGN_REVIEW_REQUIRED",
    "STATUS_CONFLICT": "STATUS_RECONCILIATION_REQUIRED",
    "EXACT_BLOCKER": "WORKER_REPORTED_BLOCKER",
    "PARTIAL": "PARTIAL_RETURN_RECORDED",
}
SECTIONS = (
    "Exact statement and normalization", "Dated status and primary evidence",
    "Strongest verified interface", "Proposed bounded successor task",
    "Prerequisites and blocker", "Reuse and claim boundary",
)
NO_AUTHORITY = {
    "source_semantics_accepted": False, "solve_dispatch_authorized": False,
    "mathematical_claim_accepted": False, "certification": False,
    "publication": False, "canonical_repository_mutation": False,
}
LABELS = {"gcl-job", "gcl-pickup:direct-editorial", "gcl-role:source-audit", "gcl-collab:cooperative"}


class IntakeError(ValueError):
    pass


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def assignment(problem: int) -> str:
    return f"ERDOS-CATALOGUE-{problem:04d}-S01"


def load_registry(root: Path = ROOT) -> dict:
    data = json.loads((root / REGISTRY).read_text(encoding="utf-8"))
    if data.get("repository") != REPOSITORY or data.get("authority_effects") != NO_AUTHORITY:
        raise IntakeError("registry repository/authority boundary drift")
    rows = data.get("issues", [])
    if len(rows) != 1221 or any(type(r.get("problem_id")) is not int for r in rows) or {r.get("problem_id") for r in rows} != set(range(1, 1222)):
        raise IntakeError("registry must cover exactly problems 1..1221")
    numbers = [r.get("issue_number") for r in rows]
    if len(set(numbers)) != 1221 or any(type(n) is not int or n <= 0 for n in numbers):
        raise IntakeError("duplicate or invalid issue number")
    for row in rows:
        if not re.fullmatch(r"[a-f0-9]{64}", row.get("issue_body_sha256", "")):
            raise IntakeError("invalid issue-body source lock")
    return data


def parse_return(body: str, problem: int) -> dict:
    if not body.startswith(MARKER + "\n"):
        raise IntakeError("comment must start exactly RESULT/1 followed by a newline")
    first = body.find("\n## ")
    if first < 0:
        raise IntakeError("required report sections missing")
    fields = {}
    for line in body[len(MARKER) + 1:first].splitlines():
        if not line.strip():
            continue
        match = re.fullmatch(r"([A-Z_]+):[ \t]*(.+)", line)
        if not match or match[1] not in KEYS or match[1] in fields:
            raise IntakeError("invalid, duplicate, or unsupported return header")
        fields[match[1]] = match[2].strip()
    if set(fields) != KEYS:
        raise IntakeError("missing required return header")
    if fields["ASSIGNMENT_ID"] != assignment(problem) or fields["PROBLEM_ID"] != str(problem):
        raise IntakeError("return assignment/problem does not match bound issue")
    if fields["DISPOSITION"] not in DISPOSITIONS:
        raise IntakeError("unsupported worker-reported disposition")
    if fields["CONTEXT_CLASS"] != "ZERO_CONTEXT" or fields["TIMEBOX_OBSERVED"] not in {"YES", "NO"}:
        raise IntakeError("invalid context/timebox declaration")
    headings = list(re.finditer(r"^## (.+)$", body, re.MULTILINE))
    names = [m[1] for m in headings]
    if names != list(SECTIONS):
        raise IntakeError("report sections must match the issue contract exactly and in order")
    sections = {}
    for i, heading in enumerate(headings):
        end = headings[i+1].start() if i+1 < len(headings) else len(body)
        text = body[heading.end():end].strip()
        if not text or text in {"...", "TODO", "TBD"} or re.fullmatch(r"<[^>]+>", text):
            raise IntakeError(f"empty or placeholder section: {heading[1]}")
        sections[heading[1]] = text
    return {"worker_reported_disposition": fields["DISPOSITION"],
            "next_review": DISPOSITIONS[fields["DISPOSITION"]],
            "context_class_declared": fields["CONTEXT_CLASS"],
            "context_independence_verified": False,
            "timebox_observed_declared": fields["TIMEBOX_OBSERVED"], "sections": sections}


def capture(event: dict, registry: dict) -> tuple[dict, str]:
    issue, comment = event.get("issue", {}), event.get("comment", {})
    number, cid = issue.get("number"), comment.get("id")
    matches = [r for r in registry["issues"] if r["issue_number"] == number]
    if len(matches) != 1 or issue.get("pull_request"):
        raise IntakeError("event is not a uniquely bound catalogue issue")
    row = matches[0]
    problem = row["problem_id"]
    if (event.get("repository") or {}).get("full_name") != REPOSITORY:
        raise IntakeError("event repository mismatch")
    if type(cid) is not int or cid <= 0:
        raise IntakeError("invalid authenticated comment identity")
    actor = comment.get("user") or {}
    if type(actor.get("id")) is not int or actor["id"] <= 0 or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_\[\]-]*", actor.get("login", "")):
        raise IntakeError("authenticated GitHub comment actor required")
    body = comment.get("body")
    if not isinstance(body, str) or len(body.encode("utf-8")) > 262144:
        raise IntakeError("comment body missing or exceeds capture limit")
    digest = sha(body)
    action = event.get("action", "snapshot")
    if action not in {"created", "edited", "deleted", "snapshot"}:
        raise IntakeError("unsupported comment event action")
    labels = {l["name"] for l in issue.get("labels", [])}
    receipt = {
        "record_type": "ERDOS_CATALOGUE_COMMENT_RECEIPT", "schema_version": "1.0.0",
        "task_id": assignment(problem), "problem_id": problem, "issue_number": number,
        "comment_id": cid, "comment_url": f"https://github.com/{REPOSITORY}/issues/{number}#issuecomment-{cid}",
        "actor": {"id": actor["id"], "login": actor["login"], "type": actor.get("type")},
        "event_action": action, "created_at": comment.get("created_at"), "updated_at": comment.get("updated_at"),
        "comment_body_sha256": digest, "bound_issue_body_sha256": row["issue_body_sha256"],
        "authority_effects": dict(NO_AUTHORITY), "custody": "CAPTURED_UNADJUDICATED",
        "validation": "REJECTED", "errors": [],
    }
    receipt["event_actor"] = event.get("sender") or {"id":actor["id"],"login":actor["login"],"type":actor.get("type")}
    try:
        if sha(issue.get("body") or "") != row["issue_body_sha256"]:
            raise IntakeError("bound issue-body source lock changed")
        if not issue.get("title", "").startswith(f"[GCL-ERDOS] {assignment(problem)} — Problem {problem}:"):
            raise IntakeError("bound issue title drift")
        if not LABELS <= labels:
            raise IntakeError("direct-editorial pickup labels missing")
        if comment.get("issue_url") not in {None, f"https://api.github.com/repos/{REPOSITORY}/issues/{number}"}:
            raise IntakeError("comment belongs to a different issue")
        receipt.update(parse_return(body, problem))
        receipt["validation"] = "STRUCTURALLY_VALID_UNADJUDICATED"
    except IntakeError as error:
        receipt["errors"].append(str(error))
        receipt["next_review"] = "RETURN_FORMAT_OR_BINDING_REVIEW_REQUIRED"
    if action == "deleted":
        receipt["validation"] = "DELETED_RETURN_REVIEW_REQUIRED"
        receipt["next_review"] = "RETURN_DELETION_REVIEW_REQUIRED"
    # Versioned filenames never replace an earlier body/revision/tombstone.
    revision = sha(json.dumps({"action":action,"updated_at":receipt["updated_at"],"event_actor":receipt["event_actor"]},sort_keys=True))[:16]
    receipt["revision_identity"] = revision
    receipt["raw_path"] = f"returns/{assignment(problem)}/comment-{cid}-{digest}-{action}-{revision}.md"
    return receipt, body


def build_report(registry: dict, events: list[dict], output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    versions, rejected_events = {}, []
    for event in events:
        try:
            receipt, body = capture(event, registry)
        except IntakeError as error:
            rejected_events.append({"reason": str(error), "issue_number": (event.get("issue") or {}).get("number"), "comment_id": (event.get("comment") or {}).get("id")})
            continue
        key = (receipt["comment_id"], receipt["comment_body_sha256"], receipt["event_action"],receipt["revision_identity"])
        versions[key] = receipt
        raw = output / receipt["raw_path"]
        raw.parent.mkdir(parents=True, exist_ok=True)
        if raw.exists() and raw.read_bytes() != body.encode("utf-8"):
            raise IntakeError("raw evidence path collision")
        raw.write_bytes(body.encode("utf-8"))
        raw.with_suffix(".json").write_text(json.dumps(receipt, indent=2)+"\n", encoding="utf-8")
    receipts = sorted(versions.values(), key=lambda r: (r["problem_id"], r["comment_id"], r.get("updated_at") or "", r["event_action"], r["comment_body_sha256"]))
    latest = {}
    for receipt in receipts:
        cid = receipt["comment_id"]
        old = latest.get(cid)
        stamp = (receipt.get("updated_at") or "", receipt["event_action"] == "deleted")
        if old is None or stamp > (old.get("updated_at") or "", old["event_action"] == "deleted"):
            latest[cid] = receipt
        elif stamp == (old.get("updated_at") or "", old["event_action"] == "deleted") and old["comment_body_sha256"] != receipt["comment_body_sha256"]:
            # Equal timestamp conflicting revisions cannot be silently selected.
            receipt["validation"] = "CONFLICTING_REVISION_REVIEW_REQUIRED"
            receipt["next_review"] = "RETURN_REVISION_REVIEW_REQUIRED"
            latest[cid] = receipt
    for receipt in receipts:
        (output / receipt["raw_path"]).with_suffix(".json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    tasks = []
    for row in registry["issues"]:
        problem = row["problem_id"]
        current = [r for r in latest.values() if r["problem_id"] == problem]
        valid = [r for r in current if r["validation"] == "STRUCTURALLY_VALID_UNADJUDICATED"]
        tasks.append({"task_id": assignment(problem), "problem_id": problem, "issue_number": row["issue_number"],
                      "issue_url": f"https://github.com/{REPOSITORY}/issues/{row['issue_number']}",
                      "state": "AWAITING_RETURN" if not current else "RETURN_REVIEW_REQUIRED",
                      "comment_ids": sorted(r["comment_id"] for r in current),
                      "structurally_valid_returns": len(valid), "review_routes": sorted({r["next_review"] for r in current}),
                      "multiple_contributor_returns": len(valid)>1, "authority_effects": dict(NO_AUTHORITY)})
    report = {"record_type": "ERDOS_CATALOGUE_INTAKE_REPORT", "schema_version": "1.0.0",
              "registry_id": registry["registry_id"], "authority_effects": dict(NO_AUTHORITY),
              "custody": "WORKFLOW_ARTIFACT_OR_BOUNDED_OPERATOR_OUTPUT_NOT_PROTECTED_ADMISSION",
              "source_semantic_adjudication": "NOT_PERFORMED", "tasks": tasks, "receipts": receipts,
              "rejected_events": rejected_events, "summary": {
                  "catalogue_tasks": len(tasks), "tasks_with_returns": sum(bool(t["comment_ids"]) for t in tasks),
                  "comment_versions_captured": len(receipts), "structurally_valid_current_returns": sum(t["structurally_valid_returns"] for t in tasks),
                  "review_routes": dict(Counter(r["next_review"] for r in latest.values()))}}
    (output / "CAPTURED_EVENTS.json").write_text(json.dumps(events,indent=2)+"\n",encoding="utf-8")
    (output / "REPORT.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    summary = ["# Erdős catalogue intake", "", "Captured evidence remains unadjudicated. Source acceptance and Solve dispatch require separate governed disposition.", "", f"Tasks: {len(tasks)}; tasks with returns: {report['summary']['tasks_with_returns']}; captured versions: {len(receipts)}.", "", "| Task | Next review | Current returns |", "| --- | --- | ---: |"]
    summary += [f"| [{t['task_id']}]({t['issue_url']}) | {', '.join(t['review_routes'])} | {len(t['comment_ids'])} |" for t in tasks if t["comment_ids"]]
    (output / "SUMMARY.md").write_text("\n".join(summary)+"\n",encoding="utf-8")
    return report


def api(path: str, paginate: bool = False) -> Any:
    cmd = ["gh", "api", path]
    if paginate:
        cmd += ["--paginate", "--slurp"]
    result = subprocess.run(cmd, check=True, capture_output=True, encoding="utf-8", timeout=120)
    return json.loads(result.stdout)


def live_snapshot(registry: dict) -> list[dict]:
    # One repository-wide comment scan, never 1,221 empty per-issue scans.
    pages = api(f"repos/{REPOSITORY}/issues/comments?since={registry['comments_since']}&per_page=100", True)
    bound = {r["issue_number"] for r in registry["issues"]}
    issues, events = {}, []
    for page in pages:
        for comment in page:
            match = re.fullmatch(rf"https://api.github.com/repos/{re.escape(REPOSITORY)}/issues/(\d+)", comment.get("issue_url", ""))
            if not match or int(match[1]) not in bound or not (comment.get("body") or "").startswith(MARKER+"\n"):
                continue
            number = int(match[1])
            if number not in issues:
                issues[number] = api(f"repos/{REPOSITORY}/issues/{number}")
            events.append({"repository":{"full_name":REPOSITORY}, "action":"snapshot", "issue":issues[number], "comment":comment})
    return events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--event", type=Path)
    parser.add_argument("--events", type=Path, help="ordered captured events including historical edited/deleted versions")
    parser.add_argument("--live-snapshot", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    registry = load_registry(args.repo_root)
    modes = sum(bool(v) for v in (args.event,args.events,args.live_snapshot))
    if modes != 1:
        parser.error("choose exactly one of --event, --events or --live-snapshot")
    events = live_snapshot(registry) if args.live_snapshot else json.loads((args.events or args.event).read_text(encoding="utf-8"))
    if args.event:
        events = [events]
    if not isinstance(events,list) or any(not isinstance(e,dict) for e in events):
        raise IntakeError("events input must be a list of captured GitHub event objects")
    report = build_report(registry, events, args.output)
    print(json.dumps(report["summary"],sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
