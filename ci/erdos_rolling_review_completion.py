#!/usr/bin/env python3
"""Project already-issued GCL critical reviews to RETURNED; do not certify math.

Run only through protected release-trust Council Clerk with Project write token.
No new assignment, worker RESULT/1, Solve lease or source admission is created.
All 14 issues are preflighted before writes. Partial writes can be replayed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
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
REVISION_LEDGER = ROOT / "governance/erdos_catalogue/CRITICAL_REVIEW_REVISIONS_20261013.json"
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
    ledger=json.loads(REVISION_LEDGER.read_text(encoding="utf-8"))
    pairs={(i["problem"],i["review_issue"]) for i in ledger["items"]}
    required={(n,issue) for n,(issue,disposition) in TARGET.items()
              if disposition=="REVISE"}
    if (ledger.get("schema")!="GCL-ERDOS-CRITICAL-SOURCE-REVISIONS/1" or
        ledger.get("count")!=5 or pairs!=required or
        any(i["status"]!="SOURCE_CORRECTION_REQUIRED" for i in ledger["items"])):
        raise ValueError("protected five-revision ledger drift")
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

def main():
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

if __name__=="__main__":
    sys.exit(main())
