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
    if len(rows) != 1:
        raise ValueError(f"expected exactly one current structurally valid return, got {len(rows)}")
    row = rows[0]
    expected = f"ERDOS-CATALOGUE-{row['problem_id']:04d}-S01"
    if row.get("task_id") != expected or tasks[0].get("task_id") != expected or not row.get("comment_id"):
        raise ValueError("return binding mismatch")
    return row


def reconcile(report: dict, issue: int, dry_run: bool) -> dict:
    receipt = validate_receipt(report, issue)
    issue_json = gh("api", f"repos/{OWNER}/{REPO}/issues/{issue}")
    assert isinstance(issue_json, dict)
    labels = {l["name"] for l in issue_json.get("labels", [])}
    if issue_json.get("state") != "open" or not {"gcl-job", "gcl-pickup:direct-editorial", "gcl-role:source-audit"} <= labels:
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
    if dry_run:
        return before
    if str(item.get("status", "")).upper() != "RETURNED":
        subprocess.run(["gh", "project", "item-edit", "--project-id", project_id,
                        "--id", item["id"], "--field-id", field_id,
                        "--single-select-option-id", option_id], check=True)
    if "gcl-state:available" in labels:
        subprocess.run(["gh", "api", "--method", "DELETE",
                        f"repos/{OWNER}/{REPO}/issues/{issue}/labels/gcl-state%3Aavailable"],
                       check=True, stdout=subprocess.DEVNULL)
    final = issue_project_item(issue, project_id)
    if final["id"] != item["id"] or str(final["status"]).upper() != "RETURNED":
        raise RuntimeError("Targeted Project readback does not confirm returned state")
    refreshed = gh("api", f"repos/{OWNER}/{REPO}/issues/{issue}")
    if "gcl-state:available" in {l["name"] for l in refreshed["labels"]}:
        raise RuntimeError("issue availability label persists")
    before["verified_status"] = final.get("status")
    before["available_removed"] = True
    return before


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True)
    p.add_argument("--issue", type=int)
    p.add_argument("--all", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    try:
        with open(args.report, encoding="utf-8") as f:
            report = json.load(f)
        if (args.issue is None) == (not args.all):
            raise ValueError("specify exactly one of --issue or --all")
        issues = [args.issue] if args.issue is not None else [t["issue_number"] for t in report.get("tasks", []) if t.get("structurally_valid_returns") == 1]
        results = []
        for issue in issues:
            results.append(reconcile(report, issue, args.dry_run))
        print(json.dumps(results, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError, KeyError) as exc:
        print(f"QUEUE_RECONCILIATION_BLOCKED: {exc}", file=sys.stderr)
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
        if disposition=="SOURCE_ACCEPTED" and REVISE_LABEL in labels:
            raise ValueError(f"#{issue}: inappropriate revision label")
        rows.append({"problem":problem,"issue":issue,"disposition":disposition,
                     "comment":comments,"project_item":item,"project_status":project["name"],
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
        if row["disposition"]=="REVISE" and not row["revise_label"]:
            mutation("api",f"repos/grandchallenge/MATH-PROGRAMME/issues/{n}/labels",
                     "--method","POST","--input","-",
                     data={"labels":[REVISE_LABEL]})
        item=old.project_item_for_issue(n)
        status=old.project_status(item)
        field=old.issue_fields(n)
        obj=old.issue(n)
        lbl={x["name"] for x in obj["labels"]}
        # Confirm review content has not changed during reconciliation.
        comment=review_comment(n,row["disposition"])
        if (item!=row["project_item"] or
            status!={"name":"RETURNED","optionId":data["returned_option"]} or
            field.get("GCL State")!="RETURNED" or
            "gcl-state:available" in lbl or
            (REVISE_LABEL in lbl)!=(row["disposition"]=="REVISE") or
            obj["state"]!="open" or comment!=row["comment"]):
            raise ValueError(f"#{n}: post-write authenticated readback failed")
        out.append({"issue":n,"disposition":row["disposition"],"comment_id":comment["comment_id"],
                    "project_status":"RETURNED","gcl_state":"RETURNED",
                    "source_correction_open":row["disposition"]=="REVISE"})
    if len(out)!=14 or sum(x["source_correction_open"] for x in out)!=5:
        raise ValueError("final 14/5 verified census failed")
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
