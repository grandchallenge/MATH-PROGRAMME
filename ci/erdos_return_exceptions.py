#!/usr/bin/env python3
"""Bounded, loss-preserving handling of invalid and competing catalogue returns."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

try:
    from ci import erdos_catalogue_programme_intake as intake
    from ci.erdos_catalogue_queue_projection import persist_projection_receipt
except ModuleNotFoundError:
    import erdos_catalogue_programme_intake as intake
    from erdos_catalogue_queue_projection import persist_projection_receipt

SCHEMA = "GCL-ERDOS-RETURN-EXCEPTION/1"
LIMIT = 16
EXTRAS = {"PINNED_CATALOGUE", "PINNED_SOURCE_REVISION",
          "PRIMARY_SOURCE_AUDIT_DEPTH", "PRIMARY_AUDIT_DEPTH", "AUDIT_DATE_UTC"}
ALIASES = {
    "Strongest verified interface and finite lemma": "Strongest verified interface",
    "Dated status and source evidence": "Dated status and primary evidence",
    "Strongest verified finite interface": "Strongest verified interface",
    "Prerequisites and critical source hold": "Prerequisites and blocker",
}


def sha(content):
    return hashlib.sha256(content).hexdigest()


def current(report, issue):
    """Reject conflicting equal-time edits rather than selecting arbitrarily."""
    latest = {}
    for r in report.get("receipts", []):
        if r.get("issue_number") != issue:
            continue
        cid = r["comment_id"]
        stamp = (r.get("updated_at") or "", r.get("event_action") == "deleted")
        old = latest.get(cid)
        if old is None or stamp > (old.get("updated_at") or "", old.get("event_action") == "deleted"):
            latest[cid] = r
        elif stamp == (old.get("updated_at") or "", old.get("event_action") == "deleted") and (
            r.get("comment_body_sha256"), r.get("validation")
        ) != (old.get("comment_body_sha256"), old.get("validation")):
            raise ValueError(f"#{issue} conflicting current revisions")
    return list(latest.values())


def exceptions(report):
    tasks = report.get("tasks", [])
    if not isinstance(tasks, list) or len({t["issue_number"] for t in tasks}) != len(tasks):
        raise ValueError("duplicate or invalid task roster")
    result = []
    for task in tasks:
        issue = task["issue_number"]
        rows = current(report, issue)
        good = [r for r in rows if r["validation"] == "STRUCTURALLY_VALID_UNADJUDICATED"]
        bad = [r for r in rows if r["validation"] != "STRUCTURALLY_VALID_UNADJUDICATED"]
        if (bad and not good) or len(good) > 1:
            result.append(issue)
    return sorted(result)


def manifest(report, size, digest):
    if type(size) is not int or not 1 <= size <= LIMIT:
        raise ValueError("exception batch size must be 1..16")
    ids = exceptions(report)
    n = max(1, (len(ids) + size - 1) // size)
    return {"include": [
        {"index": i, "count": n, "total": len(ids), "size": size,
         "report_sha256": digest, "issues": ids[i*size:(i+1)*size]}
        for i in range(n)
    ]}


def normalize(text, problem, cid, original_sha, issue):
    """Reorder known headings, relocate recognized metadata, preserve all section text."""
    if sha(text.encode()) != original_sha or not text.startswith("RESULT/1\n"):
        raise ValueError("source changed")
    headings = list(re.finditer(r"^## (.+)$", text, re.M))
    if len(headings) != len(intake.SECTIONS):
        raise ValueError("requires all six substantive sections")
    fields, extra = {}, []
    for line in text[:headings[0].start()].splitlines()[1:]:
        if not line.strip():
            continue
        match = re.fullmatch(r"([A-Z_]+):[ \t]*(.+)", line)
        if not match:
            raise ValueError("malformed header")
        key, value = match.groups()
        if key in intake.KEYS and key not in fields:
            fields[key] = value.strip()
        elif key in EXTRAS and not any(x.startswith(key + ":") for x in extra):
            extra.append(line)
        else:
            raise ValueError(f"duplicate or unsafe header {key}")
    if (set(fields) != intake.KEYS
        or fields["ASSIGNMENT_ID"] != intake.assignment(problem)
        or fields["PROBLEM_ID"] != str(problem)):
        raise ValueError("original source identity/headers not trustworthy")
    sections = {}
    for i, heading in enumerate(headings):
        name = ALIASES.get(heading[1], heading[1])
        end = headings[i+1].start() if i+1 < len(headings) else len(text)
        body = text[heading.end():end].strip()
        if name not in intake.SECTIONS or name in sections or not body:
            raise ValueError(f"unmapped, empty or repeated section {name}")
        sections[name] = body
    if set(sections) != set(intake.SECTIONS):
        raise ValueError("one or more substantive source sections missing")
    if extra:
        sections["Dated status and primary evidence"] += (
            "\n\nOriginal worker metadata (verbatim, informational only):\n" + "\n".join(extra))
    sections["Reuse and claim boundary"] += (
        "\n\nGCL DERIVED FORMATTING COPY ONLY. Not a second independent worker return,"
        " source acceptance, or mathematical certification.\n"
        f"Original: https://github.com/{intake.REPOSITORY}/issues/{issue}#issuecomment-{cid}\n"
        f"Original SHA-256: {original_sha}\n")
    head = "RESULT/1\n" + "\n".join(f"{key}: {fields[key]}" for key in (
        "ASSIGNMENT_ID", "PROBLEM_ID", "DISPOSITION", "CONTEXT_CLASS", "TIMEBOX_OBSERVED"))
    derived = head + "\n\n" + "\n\n".join(
        f"## {key}\n\n{sections[key]}" for key in intake.SECTIONS) + "\n"
    intake.parse_return(derived, problem)
    if len(derived.encode()) > 262144:
        raise ValueError("repair too large")
    for i, heading in enumerate(headings):
        end = headings[i+1].start() if i+1 < len(headings) else len(text)
        if text[heading.end():end].strip() not in derived:
            raise ValueError("a substantive source section was lost")
    if any(s not in derived for s in extra):
        raise ValueError("source metadata lost")
    return derived


def gh(endpoint, *, post=None):
    command = ["gh", "api"]
    if post is None:
        command += [endpoint]
    else:
        command += ["--method", "POST", endpoint, "--input", "-"]
    p = subprocess.run(command, input=post, check=True, capture_output=True,
                       text=True, timeout=90)
    return json.loads(p.stdout)


def process_issue(report, issue, *, apply):
    rows = current(report, issue)
    good = [r for r in rows if r["validation"] == "STRUCTURALLY_VALID_UNADJUDICATED"]
    bad = [r for r in rows if r["validation"] != "STRUCTURALLY_VALID_UNADJUDICATED"]
    if not ((bad and not good) or len(good) > 1):
        raise ValueError(f"#{issue}: task no longer qualifies as exception")
    item = next(t for t in report["tasks"] if t["issue_number"] == issue)
    problem = item["problem_id"]
    source = good if len(good) > 1 else bad
    bindings = []
    for row in source:
        comment = gh(f"repos/{intake.REPOSITORY}/issues/comments/{row['comment_id']}")
        original = comment.get("body") or ""
        if (comment.get("issue_url") !=
            f"https://api.github.com/repos/{intake.REPOSITORY}/issues/{issue}"
            or sha(original.encode()) != row["comment_body_sha256"]):
            raise ValueError(f"#{issue}: source edited or reassigned after capture")
        bindings.append((row, original))
    issue_json = gh(f"repos/{intake.REPOSITORY}/issues/{issue}")
    registry = intake.load_registry()
    source_row = next(r for r in registry["issues"] if r["issue_number"] == issue)
    labels = {r["name"] for r in issue_json.get("labels",[])}
    if (issue_json.get("number") != issue or
        intake.sha(issue_json.get("body") or "") != source_row["issue_body_sha256"]
        or not issue_json.get("title","").startswith(
            f"[GCL-ERDOS] {intake.assignment(problem)} — Problem {problem}:")
        or not intake.LABELS <= labels):
        raise ValueError(f"#{issue}: protected task/source binding changed")
    if len(good) > 1:
        kind = "MULTIPLE_VALID"
        reason = "Competing valid source claims require source specialist adjudication"
    else:
        kind = "SOURCE_INTEGRITY"
        try:
            if len(bindings) != 1:
                raise ValueError("multiple invalid source comments require specialist review")
            row, original = bindings[0]
            derived = normalize(original, problem, row["comment_id"],
                                row["comment_body_sha256"], issue)
            kind = "MECHANICAL_REPAIR"
            reason = "Exact formatting normalization; no source content omitted"
        except ValueError as exc:
            reason = str(exc)
    if kind == "MECHANICAL_REPAIR":
        allowed = {"invalid, duplicate, or unsupported return header",
                   "report sections must match the issue contract exactly and in order"}
        if not (set(bindings[0][0].get("errors", [])) <= allowed
                and bindings[0][0].get("errors")):
            kind = "SOURCE_INTEGRITY"
            reason = "non-format source validation error requires specialist review"
    if kind == "MECHANICAL_REPAIR":
        body = derived
    else:
        # No new task; route to specialist on its existing source issue.
        details = "\n".join(f"- {r['comment_id']} / SHA256 {r['comment_body_sha256']}"
                            for r,_ in bindings)
        body = (f"GCL-RETURN-EXCEPTION/1\nISSUE: {issue}\n"
                f"PROBLEM: {problem}\nTYPE: {kind}\n"
                f"REVIEW: REQUIRED, NO SOURCE ACCEPTANCE\n"
                f"DETAIL: {reason}\nBOUND SOURCE COMMENTS:\n{details}\n"
                "NEXT: Independent source-semantic specialist must compare the"
                " complete original evidence and return a source-bound finding."
                " Preserve competing contributions; do not select by recency.\n")
    prior = gh(f"repos/{intake.REPOSITORY}/issues/{issue}/comments?per_page=100")
    if len(prior) >= 100:
        raise ValueError(f"#{issue}: comment pagination ambiguous")
    matches = [c for c in prior if c.get("body") == body]
    if len(matches)>1:
        raise ValueError(f"#{issue}: duplicate derived comments")
    if len(matches)==1:
        posted = matches[0]
        effect = "ALREADY_EXISTS"
    elif not apply:
        return {"issue":issue,"kind":kind,"effect":"DRY_RUN",
                "original_comments":[r["comment_id"] for r,_ in bindings],
                "reason":reason,"derived_sha256":sha(body.encode())}
    else:
        posted = gh(f"repos/{intake.REPOSITORY}/issues/{issue}/comments",
                    post=json.dumps({"body":body}))
        effect = "POSTED"
    confirmed = gh(f"repos/{intake.REPOSITORY}/issues/comments/{posted['id']}")
    if (confirmed.get("body") != body or
        confirmed.get("issue_url") != f"https://api.github.com/repos/{intake.REPOSITORY}/issues/{issue}"):
        raise ValueError(f"#{issue}: authenticated comment readback failed")
    if kind == "MECHANICAL_REPAIR":
        intake.parse_return(confirmed["body"],problem)
    return {"issue":issue,"kind":kind,"effect":effect,
            "original_comments":[r["comment_id"] for r,_ in bindings],
            "derived_sha256":sha(body.encode()),"posted_comment_id":posted["id"],
            "reason":reason, "readback":True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--manifest",action="store_true")
    parser.add_argument("--batch-size",type=int,default=16)
    parser.add_argument("--batch-index",type=int)
    parser.add_argument("--expected-sha")
    parser.add_argument("--apply",action="store_true")
    parser.add_argument("--receipt",type=Path)
    args=parser.parse_args()
    raw=args.report.read_bytes()
    report=json.loads(raw)
    digest=sha(raw)
    parts=manifest(report,args.batch_size,digest)
    if args.apply and (
        os.getenv("GITHUB_ACTIONS") != "true"
        or os.getenv("GITHUB_REF") != "refs/heads/main"
        or os.getenv("GITHUB_REPOSITORY") != intake.REPOSITORY
        or os.getenv("GCL_RETURN_EXCEPTION_CONTROL") != "protected-main"):
        raise ValueError("only protected workflow may publish derived returns")
    if args.manifest:
        if args.apply or args.batch_index is not None or args.receipt:
            raise ValueError("manifest cannot write")
        print(json.dumps(parts,separators=(",",":"),sort_keys=True))
        return 0
    if args.receipt is None or args.batch_index is None or args.expected_sha != digest:
        raise ValueError("exact source hash, batch index, and receipt required")
    if not 0 <= args.batch_index < len(parts["include"]):
        raise ValueError("out-of-range batch")
    entry=parts["include"][args.batch_index]
    record={"schema":SCHEMA,"status":"RUNNING","verified":False,"applied":False,
            "report_sha256":digest,"protected_head":os.getenv("GITHUB_SHA",""),
            "run_id":os.getenv("GITHUB_RUN_ID",""),"batch":entry,"results":[],
            "in_flight_issue":None,"blocker":None}
    persist_projection_receipt(args.receipt,record)
    try:
        for issue in entry["issues"]:
            record["in_flight_issue"]=issue
            persist_projection_receipt(args.receipt,record)
            outcome=process_issue(report,issue,apply=args.apply)
            record["results"].append(outcome)
            record["in_flight_issue"]=None
            persist_projection_receipt(args.receipt,record)
        record["status"]="VERIFIED_BATCH" if args.apply else "DRY_RUN_ONLY"
        record["verified"]=args.apply
        record["applied"]=args.apply
    except (ValueError,RuntimeError,OSError,KeyError,subprocess.CalledProcessError,
            subprocess.TimeoutExpired) as exc:
        record["status"]="BLOCKED"
        record["blocker"]=f"{type(exc).__name__}: {exc}"
    persist_projection_receipt(args.receipt,record)
    print(json.dumps({k:v for k,v in record.items() if k!="results"},sort_keys=True))
    return 0 if record["status"] in {"VERIFIED_BATCH","DRY_RUN_ONLY"} else 1


if __name__=="__main__":
    raise SystemExit(main())
