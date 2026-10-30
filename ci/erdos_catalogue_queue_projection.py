#!/usr/bin/env python3
"""Project projection for structurally valid Erdős direct-editorial returns.

Uses gh's authenticated actor, not a mathematical or protected admission authority.
No shell session manipulation; fail closed on ambiguous Project configuration.
"""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import json
import subprocess
import sys

OWNER = "grandchallenge"
REPO = "MATH-PROGRAMME"
PROJECT = "2"
URL_PREFIX = f"https://github.com/{OWNER}/{REPO}/issues/"
STATES = ("RETURNED",)


def gh(*args: str) -> object:
    p = subprocess.run(["gh", *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(f"gh {' '.join(args[:3])}: {p.stderr.strip()}")
    return json.loads(p.stdout)


def graph(query: str, **variables: object) -> dict:
    payload = json.dumps({"query": query, "variables": variables})
    result = subprocess.run(["gh", "api", "graphql", "--input", "-"],
                            input=payload, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"targeted GraphQL query failed: {result.stderr.strip()}")
    response = json.loads(result.stdout)
    if response.get("errors"):
        raise RuntimeError(f"targeted GraphQL errors: {response['errors']}")
    return response["data"]


PROJECT_META_QUERY = """
query($owner: String!, $number: Int!) {
  organization(login: $owner) {
    projectV2(number: $number) {
      id
      fields(first: 100) {
        pageInfo { hasNextPage }
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options { id name }
          }
        }
      }
    }
  }
}
"""

ISSUE_ITEM_QUERY = """
query($owner: String!, $repo: String!, $number: Int!) {
  repository(owner: $owner, name: $repo) {
    issue(number: $number) {
      projectItems(first: 100) {
        pageInfo { hasNextPage }
        nodes {
          id
          project { id number }
          fieldValueByName(name: "Status") {
            ... on ProjectV2ItemFieldSingleSelectValue { name }
          }
        }
      }
    }
  }
}
"""


def project_metadata() -> tuple[str, str, str]:
    project = graph(PROJECT_META_QUERY, owner=OWNER, number=int(PROJECT))[
        "organization"]["projectV2"]
    if not project or project["fields"]["pageInfo"]["hasNextPage"]:
        raise ValueError("Project fields missing or pagination incomplete")
    matches = [(field, option) for field in project["fields"]["nodes"]
               if field and field.get("name") == "Status"
               for option in field.get("options", [])
               if option["name"].upper() == "RETURNED"]
    if len(matches) != 1:
        raise ValueError("expected exactly one RETURNED option on Project Status")
    return project["id"], matches[0][0]["id"], matches[0][1]["id"]


def issue_project_item(issue: int, project_id: str) -> dict:
    data = graph(ISSUE_ITEM_QUERY, owner=OWNER, repo=REPO, number=issue)
    node = data["repository"]["issue"]
    if node is None or node["projectItems"]["pageInfo"]["hasNextPage"]:
        raise ValueError("Issue project membership missing or paginated")
    matches = [item for item in node["projectItems"]["nodes"]
               if item["project"]["id"] == project_id]
    if len(matches) != 1:
        raise ValueError(f"expected one Project item for #{issue}; got {len(matches)}")
    return {"id": matches[0]["id"],
            "status": (matches[0].get("fieldValueByName") or {}).get("name")}


def validate_receipt(report: dict, issue: int) -> dict:
    tasks = [t for t in report.get("tasks", []) if t.get("issue_number") == issue]
    if len(tasks) != 1:
        raise ValueError("issue missing or ambiguous in captured catalogue task registry")
    # Historical event reports retain all revisions. Select only the newest
    # revision per comment before deciding whether a current valid return exists.
    # A tombstone or invalid edited revision revokes its older valid predecessor.
    versions = [r for r in report.get("receipts", []) if r.get("issue_number") == issue]
    by_comment = {}
    for version in versions:
        cid = version.get("comment_id")
        old = by_comment.get(cid)
        if old is None:
            by_comment[cid] = version
            continue
        stamp = (version.get("updated_at") or "",
                 version.get("event_action") == "deleted")
        old_stamp = (old.get("updated_at") or "",
                     old.get("event_action") == "deleted")
        if stamp > old_stamp:
            by_comment[cid] = version
        elif stamp == old_stamp and (
            version.get("comment_body_sha256") != old.get("comment_body_sha256")
            or version.get("validation") != old.get("validation")
        ):
            # Ambiguous same-time revisions must fail closed, never choose a
            # convenient historical success by order of iteration.
            raise ValueError("conflicting equal-timestamp comment revisions")
    rows = [r for r in by_comment.values()
            if r.get("validation") == "STRUCTURALLY_VALID_UNADJUDICATED"
            and r.get("event_action") != "deleted"]
    if len(rows) == 0:
        raise ValueError("expected exactly one current structurally valid return, got 0")
    if len(rows) == 1:
        row = rows[0]
    else:
        try:
            from ci.erdos_return_arbitration import choose
        except ModuleNotFoundError:
            from erdos_return_arbitration import choose
        row = choose(issue, rows)
    expected = f"ERDOS-CATALOGUE-{row['problem_id']:04d}-S01"
    if row.get("task_id") != expected or tasks[0].get("task_id") != expected or not row.get("comment_id"):
        raise ValueError("return binding mismatch")
    return row


def source_issue_gcl_state(issue: int) -> str:
    """Read one exact persisted GCL State field, independent of Project Status."""
    fields=gh("api",f"repos/{OWNER}/{REPO}/issues/{issue}/issue-field-values")
    if not isinstance(fields,list):
        raise ValueError("source GCL State API payload malformed")
    rows=[x for x in fields if isinstance(x,dict)
          and x.get("issue_field_name")=="GCL State"
          and x.get("issue_field_id")==GCL_STATE_FIELD]
    if len(rows)!=1:
        raise ValueError(f"#{issue}: missing/ambiguous GCL State Issue Field")
    state=(rows[0].get("single_select_option") or {}).get("name")
    if state not in ("AVAILABLE","RETURNED"):
        raise ValueError(f"#{issue}: unexpected source GCL State {state}")
    return state


def apply_returned_project_status(issue: int, project_id: str, item: dict,
                                  field_id: str, option_id: str) -> None:
    """Reconcile a lost mutation acknowledgment without replaying the write.

    A failed CLI call may already have changed GitHub. Never treat a transport
    exception as proof the remote operation did not execute. A readback failure
    preserves uncertainty and propagates the original error.
    """
    if str(item.get("status", "")).upper() == "RETURNED":
        return
    try:
        subprocess.run(["gh", "project", "item-edit", "--project-id", project_id,
                        "--id", item["id"], "--field-id", field_id,
                        "--single-select-option-id", option_id], check=True)
    except subprocess.CalledProcessError:
        # This is an uncertain transport/CLI failure, NOT an explicit denial.
        # The only permissible recovery is read-only remote reconciliation.
        actual = issue_project_item(issue, project_id)
        if actual["id"] != item["id"] or str(actual.get("status", "")).upper() != "RETURNED":
            raise


def reconcile(report: dict, issue: int, dry_run: bool) -> dict:
    receipt = validate_receipt(report, issue)
    # For multi-return adjudication, the protected comparison binds *all*
    # candidate comment digests, not merely its selected queue source.
    current = [r for r in report.get("receipts", []) if
               r.get("issue_number") == issue and
               r.get("validation") == "STRUCTURALLY_VALID_UNADJUDICATED"]
    if len({r["comment_id"] for r in current}) > 1:
        for candidate in current:
            live = gh("api", f"repos/{OWNER}/{REPO}/issues/comments/{candidate['comment_id']}")
            if (live.get("issue_url") != f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue}"
                or hashlib.sha256((live.get("body") or "").encode()).hexdigest()
                != candidate["comment_body_sha256"]):
                raise ValueError(f"#{issue}: competing source comment changed since arbitration")
    issue_json = gh("api", f"repos/{OWNER}/{REPO}/issues/{issue}")
    assert isinstance(issue_json, dict)
    labels = {l["name"] for l in issue_json.get("labels", [])}
    if (issue_json.get("state") not in ("open","closed")
            or not {"gcl-job", "gcl-pickup:direct-editorial", "gcl-role:source-audit"} <= labels):
        raise ValueError("issue state/pickup binding failed")
    comment = gh("api", f"repos/{OWNER}/{REPO}/issues/comments/{receipt['comment_id']}")
    if not isinstance(comment, dict) or comment.get("issue_url") != f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue}":
        raise ValueError("comment-to-issue binding failed")
    if not comment.get("body", "").startswith("RESULT/1\n"):
        raise ValueError("return no longer exists or has been edited")
    # Never trust a historical event after a comment edit; verify exact body digest.
    import hashlib
    if hashlib.sha256(comment["body"].encode()).hexdigest() != receipt["comment_body_sha256"]:
        raise ValueError("comment changed since capture; recapture required")
    project_id, field_id, option_id = project_metadata()
    item = issue_project_item(issue, project_id)
    before = {"issue": issue, "comment_id": receipt["comment_id"], "project_item": item["id"],
              "status_before": item.get("status"), "target": "RETURNED", "dry_run": dry_run}
    if issue_json.get("state")=="closed":
        # Existing accepted historical returns (e.g. #1270/#1273) have
        # already been closed and their Worker Queue item is Done. The
        # return's exact source-bound comment was just reverified above.
        # Do not demote a completed item to RETURNED or rewrite its labels.
        if item.get("status")!="Done" or "gcl-state:available" in labels:
            raise ValueError("closed source return lacks terminal Done custody")
        before.update({"target":"PRESERVE_DONE","historical_terminal":True,
                       "verified_status":"Done","available_removed":False})
        return before
    issue_state=source_issue_gcl_state(issue)
    before["gcl_state_before"]=issue_state
    if dry_run:
        return before
    apply_returned_project_status(issue, project_id, item, field_id, option_id)
    if issue_state != "RETURNED":
        payload = json.dumps({"issue_field_values": [
            {"field_id": GCL_STATE_FIELD, "value": "RETURNED"}]})
        try:
            subprocess.run(["gh", "api", "--method", "POST",
                            f"repos/{OWNER}/{REPO}/issues/{issue}/issue-field-values",
                            "--input", "-"], input=payload, text=True,
                           capture_output=True, check=True, timeout=60)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            # A lost acknowledgment does not establish the POST failed.
            # Read back the exact field; never blindly repeat the mutation.
            if source_issue_gcl_state(issue) != "RETURNED":
                raise
    if "gcl-state:available" in labels:
        try:
            subprocess.run(["gh", "api", "--method", "DELETE",
                            f"repos/{OWNER}/{REPO}/issues/{issue}/labels/gcl-state%3Aavailable"],
                           check=True, stdout=subprocess.DEVNULL)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            # Confirm removal through authoritative issue readback.
            refreshed_labels = gh("api", f"repos/{OWNER}/{REPO}/issues/{issue}")
            if "gcl-state:available" in {x["name"] for x in refreshed_labels["labels"]}:
                raise
    final = issue_project_item(issue, project_id)
    if final["id"] != item["id"] or str(final["status"]).upper() != "RETURNED":
        raise RuntimeError("Targeted Project readback does not confirm returned state")
    refreshed = gh("api", f"repos/{OWNER}/{REPO}/issues/{issue}")
    if (refreshed.get("state")!="open"
            or "gcl-state:available" in {l["name"] for l in refreshed["labels"]}
            or source_issue_gcl_state(issue)!="RETURNED"):
        raise RuntimeError("source return Issue Field, label or open custody readback mismatch")
    before["verified_status"] = final.get("status")
    before["verified_gcl_state"]="RETURNED"
    before["available_removed"] = True
    return before




# Bounded sources are selected from the captured, content-addressed report.
# No job is allowed to traverse the entire live catalogue mutating one item
# at a time: past production runs timed out after 671/769 verified readbacks.
MAX_BATCH_SIZE = 64


def eligible_issue_ids(report: dict) -> list[int]:
    tasks = report.get("tasks")
    if not isinstance(tasks, list):
        raise ValueError("captured report tasks are missing")
    seen: set[int] = set()
    eligible: list[int] = []
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError("malformed captured task")
        issue = task.get("issue_number")
        if type(issue) is not int or issue < 1 or issue in seen:
            raise ValueError("duplicate or invalid captured task issue")
        seen.add(issue)
        count = task.get("structurally_valid_returns")
        if type(count) is not int or count < 0:
            raise ValueError(f"#{issue}: invalid return count")
        if count == 1:
            eligible.append(issue)
        elif count > 1:
            # A genuinely independent protected specialist decision can
            # authorize one bounded queue source without erasing dissent.
            try:
                validate_receipt(report, issue)
            except ValueError as error:
                if "arbitration missing" in str(error):
                    continue
                raise
            eligible.append(issue)
    return sorted(eligible)


def batch_count(total: int, size: int) -> int:
    if type(size) is not int or not 1 <= size <= MAX_BATCH_SIZE:
        raise ValueError(f"batch size must be 1..{MAX_BATCH_SIZE}")
    return max(1, (total + size - 1) // size)


def select_source_batch(report: dict, *, size: int, index: int) -> tuple[list[int], dict]:
    eligible = eligible_issue_ids(report)
    count = batch_count(len(eligible), size)
    if type(index) is not int or not 0 <= index < count:
        raise ValueError(f"batch index {index} outside [0,{count})")
    first = index * size
    selected = eligible[first:first + size]
    return selected, {
        "index": index, "count": count, "size_limit": size,
        "total_eligible": len(eligible), "start_offset": first,
        "selected_issue_numbers": selected,
    }


def source_batch_manifest(report: dict, size: int, digest: str) -> dict:
    total = len(eligible_issue_ids(report))
    count = batch_count(total, size)
    return {"include": [
        {"index": index, "total_eligible": total, "batch_count": count,
         "report_sha256": digest}
        for index in range(count)
    ]}


def persist_projection_receipt(path: Path | None, record: dict) -> None:
    """Atomic, progressively updated local evidence; Actions archives it even on failure."""
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(path.name + ".partial")
    with partial.open("w", encoding="utf-8") as handle:
        json.dump(record, handle, indent=2, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(partial, path)


def project_source_returns(
    report: dict, issues: list[int], *, dry_run: bool, receipt_path: Path | None,
    report_digest: str, batch_scope: dict | None = None,
) -> tuple[dict, int]:
    """Fail closed, preserving exact verified results and current in-flight issue.

    A protected merge, successful exit, or partially applied mutation is not a
    completed projection. Only a full per-issue authenticated readback is VERIFIED.
    """
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    record = {
        "schema": "GCL-ERDOS-SOURCE-RETURN-PROJECTION/1",
        "status": "RUNNING",
        "verified": False,
        "complete": False,
        "applied": False,
        "dry_run": dry_run,
        "claim_scope": "Project Status, exact GCL State Issue Field and available label only; not mathematical certification or editorial acceptance",
        "report_sha256": report_digest,
        "batch": batch_scope,
        "protected_head": os.environ.get("GITHUB_SHA", ""),
        "workflow_run": (f"https://github.com/{OWNER}/{REPO}/actions/runs/{run_id}" if run_id else None),
        "expected_issue_count": len(issues),
        "processed_count": 0,
        "verified_returned": 0,
        "preserved_done": 0,
        "in_flight_issue": None,
        "results": [],
        "blocker": None,
    }
    persist_projection_receipt(receipt_path, record)
    try:
        if len(set(issues)) != len(issues):
            raise ValueError("duplicate source issue IDs in captured report")
        for issue in issues:
            record["in_flight_issue"] = issue
            persist_projection_receipt(receipt_path, record)
            result = reconcile(report, issue, dry_run)
            # Reconcile performs the protected live issue, comment, field and
            # Project readback before returning. Never count a mere write.
            if not dry_run:
                if result.get("target") == "PRESERVE_DONE":
                    if result.get("verified_status") != "Done" or not result.get("historical_terminal"):
                        raise ValueError(f"#{issue}: terminal custody not reverified")
                    record["preserved_done"] += 1
                elif result.get("target") == "RETURNED":
                    if (result.get("verified_status") != "RETURNED"
                            or result.get("verified_gcl_state") != "RETURNED"
                            or result.get("available_removed") is not True):
                        raise ValueError(f"#{issue}: incomplete returned-state readback")
                    record["verified_returned"] += 1
                else:
                    raise ValueError(f"#{issue}: unknown projection target")
            record["results"].append(result)
            record["processed_count"] += 1
            record["in_flight_issue"] = None
            persist_projection_receipt(receipt_path, record)
            if record["processed_count"] % 25 == 0 or record["processed_count"] == len(issues):
                print(
                    "SOURCE_RETURN_PROGRESS "
                    f"{record['processed_count']}/{len(issues)} "
                    f"returned={record['verified_returned']} "
                    f"preserved_done={record['preserved_done']}",
                    flush=True,
                )
        if dry_run:
            record["status"] = "DRY_RUN_ONLY"
        else:
            record["status"] = "VERIFIED_BATCH" if batch_scope is not None else "VERIFIED"
            record["verified"] = True
            record["complete"] = True
            record["applied"] = True
        persist_projection_receipt(receipt_path, record)
        return record, 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired, KeyError, TypeError) as exc:
        record["status"] = "BLOCKED"
        record["blocker"] = f"{type(exc).__name__}: {exc}"
        persist_projection_receipt(receipt_path, record)
        return record, 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--issue", type=int)
    p.add_argument("--all", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--batch-manifest", action="store_true",
                   help="output deterministic, content-bound GitHub matrix (read only)")
    p.add_argument("--batch-index", type=int)
    p.add_argument("--batch-size", type=int)
    p.add_argument("--expected-report-sha256")
    p.add_argument("--expected-total", type=int)
    p.add_argument("--receipt", type=Path,
                   help="durable progress and exact terminal readback evidence")
    args = p.parse_args()
    try:
        raw = Path(args.report).read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        report = json.loads(raw)
        if not isinstance(report, dict):
            raise ValueError("captured report must be an object")
        if args.batch_manifest:
            if (args.issue is not None or args.all or args.dry_run
                    or args.batch_index is not None or args.receipt is not None
                    or args.expected_total is not None or args.expected_report_sha256):
                raise ValueError("batch manifest must be read-only and unscoped")
            print(json.dumps(source_batch_manifest(report, args.batch_size, digest),
                             separators=(",", ":"), sort_keys=True))
            return 0
        if (args.issue is None) == (not args.all):
            raise ValueError("specify exactly one of --issue or --all")
        if args.expected_report_sha256 and digest != args.expected_report_sha256:
            raise ValueError("snapshot SHA256 differs from manifest; no mutation")
        if args.all and (args.batch_index is None or args.batch_size is None):
            raise ValueError("--all requires exact batch-index and batch-size")
        if args.issue is not None and (args.batch_index is not None or args.batch_size is not None):
            raise ValueError("single issue cannot carry a bulk batch selection")
        if args.all and not args.dry_run and args.receipt is None:
            raise ValueError("bulk mutation requires receipt")
        scope = None
        if args.all:
            issues, scope = select_source_batch(report, size=args.batch_size,
                                                index=args.batch_index)
            if args.expected_total is not None and scope["total_eligible"] != args.expected_total:
                raise ValueError("snapshot eligible count differs from manifest")
        else:
            if type(args.issue) is not int or args.issue < 1:
                raise ValueError("invalid source issue number")
            if args.expected_total is not None:
                raise ValueError("single-issue mode does not accept bulk manifest total")
            issues = [args.issue]
        record, code = project_source_returns(
            report, issues, dry_run=args.dry_run, receipt_path=args.receipt,
            report_digest=digest, batch_scope=scope,
        )
        print(json.dumps({
            "status": record["status"], "verified": record["verified"],
            "processed": record["processed_count"],
            "expected": record["expected_issue_count"],
            "batch": scope,
            "receipt": str(args.receipt) if args.receipt else None,
            "blocker": record["blocker"],
        }, sort_keys=True), flush=True)
        return code
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError,
            subprocess.TimeoutExpired, KeyError, TypeError) as exc:
        if args.receipt is not None:
            persist_projection_receipt(args.receipt, {
                "schema": "GCL-ERDOS-SOURCE-RETURN-PROJECTION/1",
                "status": "BLOCKED", "verified": False, "complete": False,
                "applied": False, "processed_count": 0,
                "blocker": f"{type(exc).__name__}: {exc}",
            })
        print(f"QUEUE_RECONCILIATION_BLOCKED: {exc}", file=sys.stderr, flush=True)
        return 1




# Protected, source-bound rolling critical-review completion lane.
try:
    from ci import erdos_rolling_review_queue as old
except ModuleNotFoundError:
    import erdos_rolling_review_queue as old

ROOT = Path(__file__).resolve().parents[1]
ROSTER = ROOT / "governance/erdos_catalogue/ROLLING_RESEARCH_024.json"
TARGET = {11:(2520,"REVISE"),12:(2521,"REVISE"),14:(2522,"REVISE"),
          15:(2523,"REVISE"),17:(2529,"SOURCE_ACCEPTED"),
          18:(2525,"SOURCE_ACCEPTED"),25:(2527,"SOURCE_ACCEPTED"),
          30:(2530,"SOURCE_ACCEPTED"),32:(2531,"SOURCE_ACCEPTED"),
          33:(2532,"SOURCE_ACCEPTED"),36:(2533,"SOURCE_ACCEPTED"),
          39:(2534,"SOURCE_ACCEPTED"),40:(2535,"SOURCE_ACCEPTED"),
          41:(2536,"REVISE")}
REVISE_LABEL = "gcl-review:revise"
CORRECTED_LABEL = "gcl-review:source-corrected"
# Immutable Council Clerk source-correction overlays on the five original
# REVISE critical reviews. The REVIEW/1 comments remain historically REVISE;
# these later authenticated Clerk receipts control the *current* label.
# Scope is exact; no catalogue result becomes mathematical certification.
COUNCIL_CORRECTIONS = {
    2520:(11,6215166656,"GCL-CRITICAL-SOURCE-RESOLUTION/1",
          "NEW_GIT_BLOB_SHA1: 16aec61d2da71e38d2891540a78d3ce2cdba1051",2695),
    2521:(12,6215167768,"GCL-CRITICAL-SOURCE-RESOLUTION/1",
          "NEW_GIT_BLOB_SHA1: a14ad253fea0fda4ac4191e3a6747d6939e528ac",2695),
    2523:(15,6215168942,"GCL-CRITICAL-SOURCE-RESOLUTION/1",
          "NEW_GIT_BLOB_SHA1: a6e6fbe3d39a8982daad15d70f6f458a8c801ac4",2695),
    2522:(14,6257398101,"GCL-CRITICAL-SOURCE-RESOLUTION/FINAL-TWO/1",
          "LEAN_SOURCE_SHA256: 2dc6778835adb8c2052d183f7ce98b79a93630e42dfdb968d9435bbfcce7d47d",2760),
    2536:(41,6257398962,"GCL-CRITICAL-SOURCE-RESOLUTION/FINAL-TWO/1",
          "LEAN_SOURCE_SHA256: 66f82861886a78102e49e02a2092dcc48729317acfdd0977a2cd42504bd0ec49",2759),
}
GCL_STATE_FIELD = 47953501

def mutation(*args, data=None):
    p=subprocess.run(["gh",*args],input=(json.dumps(data) if data is not None else None),
                     capture_output=True,text=True,timeout=75)
    if p.returncode:
        raise RuntimeError(f"mutation {args[:3]}: {p.stderr[:350]}")
    return p.stdout

def roster_rows(data):
    all_tasks=old.candidates(data)
    result={t["problem"]:t for t in all_tasks if t["problem"] in TARGET}
    if len(result)!=14 or set(result)!=set(TARGET):
        raise ValueError("protected roster: exact 14 binding mismatch")
    for n,t in result.items():
        if t["issue"]!=TARGET[n][0]:
            raise ValueError(f"protected issue bound changed #{n}")
    return result

def review_comment(issue, expected):
    comments=old.gh("api",f"repos/grandchallenge/MATH-PROGRAMME/issues/{issue}/comments?per_page=100")
    if not isinstance(comments,list) or len(comments)>=100:
        raise ValueError("ambiguous/paginated comments")
    selected=[c for c in comments if (c.get("body") or "").startswith("GCL-CRITICAL-REVIEW/1\n")]
    if len(selected)!=1:
        raise ValueError(f"#{issue}: missing/duplicate critical review")
    c=selected[0]
    ds=[s.partition(":")[2].strip() for s in c["body"].splitlines() if s.startswith("DISPOSITION:")]
    if ds!=[expected] or c.get("user",{}).get("login")!="fyremael":
        raise ValueError(f"#{issue}: disposition/actor drift")
    if c.get("id") is None or not c.get("html_url","").endswith(f"#issuecomment-{c['id']}"):
        raise ValueError(f"#{issue}: review provenance drift")
    return {"comment_id":c["id"],"comment_sha256":hashlib.sha256(c["body"].encode()).hexdigest()}

def council_correction(issue: int, problem: int) -> dict | None:
    """Verify current, exact protected Council disposition, not original REVIEW/1.

    The Clerk comments are immutable sources of corrected-source status;
    ordinary worker comments and review labels are never admission evidence.
    """
    lock=COUNCIL_CORRECTIONS.get(issue)
    if lock is None:
        return None
    expected_problem, cid, prefix, material, pr=lock
    if expected_problem!=problem:
        raise ValueError(f"#{issue}: Council problem source identity drift")
    comments=old.gh("api",f"repos/grandchallenge/MATH-PROGRAMME/issues/{issue}/comments?per_page=100")
    if not isinstance(comments,list) or len(comments)>=100:
        raise ValueError(f"#{issue}: Council correction comment pagination incomplete")
    notes=[c for c in comments if c.get("id")==cid]
    if len(notes)!=1:
        raise ValueError(f"#{issue}: missing protected Council correction receipt")
    note=notes[0]
    body=note.get("body") or ""
    expected_lines=(prefix, f"ERDOS_PROBLEM: {problem}",f"REVIEW_ISSUE: #{issue}",
                    "DISPOSITION: SOURCE_CORRECTION_ACCEPTED",
                    f"PROTECTED_SOURCE_LOCK_PR: https://github.com/grandchallenge/MATH-PROGRAMME/pull/{pr}",
                    material, "MATHEMATICAL_CERTIFICATION: FALSE",
                    "OPEN_PROBLEM_STATUS: UNCHANGED")
    if (note.get("user",{}).get("login")!="gcl-council-clerk[bot]"
            or not body.startswith(prefix+"\n")
            or any(line not in body.splitlines() for line in expected_lines)
            or not note.get("html_url","").endswith(f"#issuecomment-{cid}")):
        raise ValueError(f"#{issue}: Council Clerk authority or source receipt drift")
    return {"comment_id":cid,"comment_sha256":hashlib.sha256(body.encode()).hexdigest()}


def status_options():
    data=old.gh("project","field-list","2","--owner","grandchallenge","--format","json")
    fields=[f for f in data["fields"] if f["name"]=="Status"]
    if len(fields)!=1 or fields[0]["id"]!=old.PROJECT_STATUS_FIELD_ID:
        raise ValueError("protected Project Status field identity drift")
    options={o["name"]:o["id"] for o in fields[0]["options"]}
    if not options.get("Todo") or not options.get("RETURNED"):
        raise ValueError("Project Status option missing")
    return options

def preflight():
    tasks=roster_rows(json.loads(ROSTER.read_text(encoding="utf-8")))
    opts=status_options()
    rows=[]
    for problem,(issue,disposition) in TARGET.items():
        src=old.verified_source_issue(tasks[problem])
        comments=review_comment(issue,disposition)
        labels={x["name"] for x in src["labels"]}
        state=old.issue_fields(issue).get("GCL State")
        if state not in ("AVAILABLE","RETURNED"):
            raise ValueError(f"#{issue}: unexpected Issue GCL State: {state}")
        item=old.project_item_for_issue(issue)
        if item is None:
            raise ValueError(f"#{issue}: missing Project #2 membership")
        project=old.project_status(item)
        if project.get("name") not in ("Todo","RETURNED"):
            raise ValueError(f"#{issue}: unexpected Project status {project}")
        if project["optionId"]!=opts[project["name"]]:
            raise ValueError(f"#{issue}: Project option ID drift")
        correction=council_correction(issue,problem)
        if disposition=="REVISE":
            if correction is None or CORRECTED_LABEL not in labels or REVISE_LABEL in labels:
                raise ValueError(f"#{issue}: Council correction must remain authoritative")
        elif REVISE_LABEL in labels or CORRECTED_LABEL in labels or correction is not None:
            raise ValueError(f"#{issue}: source-accepted label/correction inconsistency")
        rows.append({"problem":problem,"issue":issue,"disposition":disposition,
                     "comment":comments,"council_correction":correction,
                     "project_item":item,"project_status":project["name"],
                     "gcl_state":state,"available_label":"gcl-state:available" in labels,
                     "revise_label":REVISE_LABEL in labels})
    if len(rows)!=14 or sum(r["disposition"]=="REVISE" for r in rows)!=5:
        raise ValueError("exact disposition census changed")
    return {"project_id":old.PROJECT_ID,"status_field":old.PROJECT_STATUS_FIELD_ID,
            "returned_option":opts["RETURNED"],"rows":rows}

def ensure_revision_label():
    labels=old.gh("label","list","--repo","grandchallenge/MATH-PROGRAMME",
                  "--limit","1000","--json","name")
    if REVISE_LABEL not in {x["name"] for x in labels}:
        mutation("label","create",REVISE_LABEL,"--repo","grandchallenge/MATH-PROGRAMME",
                 "--color","FBCA04","--description",
                 "Critical source review requires protected correction; not a Solve job")
    labels=old.gh("label","list","--repo","grandchallenge/MATH-PROGRAMME",
                  "--limit","1000","--json","name")
    if REVISE_LABEL not in {x["name"] for x in labels}:
        raise ValueError("revise tracking label readback failed")

def apply(data):
    ensure_revision_label()
    out=[]
    for row in data["rows"]:
        n=row["issue"]
        if row["project_status"]!="RETURNED":
            mutation("project","item-edit","--id",row["project_item"],
                     "--project-id",old.PROJECT_ID,"--field-id",old.PROJECT_STATUS_FIELD_ID,
                     "--single-select-option-id",data["returned_option"])
        if row["gcl_state"]!="RETURNED":
            mutation("api",f"repos/grandchallenge/MATH-PROGRAMME/issues/{n}/issue-field-values",
                     "--method","POST","--input","-",
                     data={"issue_field_values":[{"field_id":GCL_STATE_FIELD,
                                                  "value":"RETURNED"}]})
        if row["available_label"]:
            mutation("api",f"repos/grandchallenge/MATH-PROGRAMME/issues/{n}/labels/gcl-state%3Aavailable",
                     "--method","DELETE")
        # Never restore a historical REVISE label after protected Council
        # source-correction acceptance. Preflight verifies all five receipts.
        if row["disposition"]=="REVISE" and not row["council_correction"]:
            raise ValueError(f"#{n}: unresolved historical revision cannot be projected")
        item=old.project_item_for_issue(n)
        status=old.project_status(item)
        field=old.issue_fields(n)
        obj=old.issue(n)
        lbl={x["name"] for x in obj["labels"]}
        # Confirm review content has not changed during reconciliation.
        comment=review_comment(n,row["disposition"])
        correction=council_correction(n,row["problem"])
        if (item!=row["project_item"] or
            status!={"name":"RETURNED","optionId":data["returned_option"]} or
            field.get("GCL State")!="RETURNED" or
            "gcl-state:available" in lbl or
            REVISE_LABEL in lbl or
            (CORRECTED_LABEL in lbl)!=(row["disposition"]=="REVISE") or
            obj["state"]!="open" or comment!=row["comment"] or
            correction!=row["council_correction"]):
            raise ValueError(f"#{n}: post-write authenticated readback failed")
        out.append({"issue":n,"disposition":row["disposition"],"comment_id":comment["comment_id"],
                    "project_status":"RETURNED","gcl_state":"RETURNED",
                    "source_correction_open":False,
                    "source_correction_accepted":bool(row["council_correction"])})
    if (len(out)!=14 or any(x["source_correction_open"] for x in out)
            or sum(x["source_correction_accepted"] for x in out)!=5):
        raise ValueError("final 14 reviews / five protected Council corrections mismatch")
    return out

def review_completion_main():
    ap=argparse.ArgumentParser()
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run",action="store_true")
    group.add_argument("--apply",action="store_true")
    ap.add_argument("--receipt",required=True)
    args=ap.parse_args()
    path=Path(args.receipt)
    path.parent.mkdir(parents=True,exist_ok=True)
    receipt={"schema":"GCL-ERDOS-REVIEW-COMPLETION-RECEIPT/1",
             "complete":False,"applied":False,"error":None}
    try:
        if args.apply and (
            os.environ.get("GITHUB_ACTIONS") != "true" or
            os.environ.get("GITHUB_REPOSITORY") != "grandchallenge/MATH-PROGRAMME" or
            os.environ.get("GITHUB_REF") != "refs/heads/main" or
            os.environ.get("GCL_CONTROLLER_ID") != "erdos-rolling-review-completion" or
            not os.environ.get("GH_TOKEN")):
            raise ValueError("untrusted apply context: protected Council Clerk workflow required")
        pre=preflight()
        receipt["preflight"]=pre
        if args.apply:
            receipt["transitions"]=apply(pre)
            receipt["applied"]=True
        receipt["complete"]=True
    except (RuntimeError,ValueError,KeyError,TypeError,OSError,
            subprocess.TimeoutExpired) as error:
        receipt["error"]=str(error)
    path.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"complete":receipt["complete"],"applied":receipt["applied"],
                      "error":receipt["error"],"receipt":str(path)},sort_keys=True))
    return 0 if receipt["complete"] else 1



if __name__ == "__main__":
    if "--review-completion" in sys.argv:
        sys.argv.remove("--review-completion")
        raise SystemExit(review_completion_main())
    raise SystemExit(main())
