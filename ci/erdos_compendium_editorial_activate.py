#!/usr/bin/env python3
"""Admit only three source-grounded Erdős Compendium EDITOR jobs to Project #2.

Independent editorial issue pickup stays direct (no /claim); RESULT/1 is
repository evidence, not acceptance. Must run with protected Council Clerk
scoped GitHub App token. --dry-run is read-only.
"""
from __future__ import annotations
import argparse
import json
import os
import re
from pathlib import Path
import subprocess
import sys

REPO = "grandchallenge/MATH-PROGRAMME"
PROJECT_ID = "PVT_kwDOB9Ao_c4Blwur"
QUEUE_FIELD_ID = "PVTSSF_lADOB9Ao_c4BlwurzhlJkjI"
ISSUE_FIELDS = {"GCL State":47953501, "GCL Campaign":47953502,
                "GCL Role":47953503, "GCL Collaboration":47953504,
                "GCL Phase":47953505, "GCL Cohort":47953514}
CAMPAIGN = "ERDOS-COMPENDIUM-EDITORIAL-001"
# Exact protected three-item subset; #2555 is intentionally excluded.
DOCKETS = {
    2556: (7,1276,"ERDOS-CATALOGUE-0007-S01"),
    2557: (9,1278,"ERDOS-CATALOGUE-0009-S01"),
    2558: (10,1279,"ERDOS-CATALOGUE-0010-S01"),
}
REQUIRED = {"gcl-job","gcl-pickup:direct-editorial",
            "gcl-role:constructive","gcl-collab:cooperative"}
OPTIONS = {"GCL State":"AVAILABLE","GCL Campaign":CAMPAIGN,
           "GCL Role":"CONSTRUCTIVE","GCL Collaboration":"COOPERATIVE",
           "GCL Phase":"SHARED","GCL Cohort":"ERDOS-COMPENDIUM-EDITORIAL-TRANCHE-001"}


def gh(*args: str, payload: dict | None = None):
    cmd=["gh",*args]
    proc=subprocess.run(cmd,input=json.dumps(payload) if payload is not None else None,
                        capture_output=True,text=True,timeout=90,check=False)
    if proc.returncode:
        raise ValueError(f"authenticated GitHub request failed: {proc.stderr[:450]}")
    return json.loads(proc.stdout) if proc.stdout.strip() else {}


def fields(n: int) -> dict:
    data=gh("api",f"repos/{REPO}/issues/{n}/issue-field-values")
    if not isinstance(data,list) or len(data)!=len({x.get("issue_field_id") for x in data}):
        raise ValueError(f"#{n} has unreadable/duplicated organization Issue Fields")
    return {x["issue_field_name"]:(x.get("single_select_option") or {}).get("name",x.get("value"))
            for x in data}


def issue(n: int) -> dict:
    return gh("api",f"repos/{REPO}/issues/{n}")


def project_record(n: int) -> dict:
    """Read exactly one Project #2 item, or prove that it has not been added."""
    q="""query($n:Int!){
      repository(owner:"grandchallenge",name:"MATH-PROGRAMME"){
        issue(number:$n){
          projectItems(first:100){
            pageInfo{hasNextPage}
            nodes{
              id
              project{id}
              fieldValueByName(name:"Queue Class"){
                ... on ProjectV2ItemFieldSingleSelectValue{name optionId}
              }
            }
          }
        }
      }
    }"""
    response=gh("api","graphql","-f",f"query={q}","-F",f"n={n}")
    link=((response.get("data") or {}).get("repository") or {}).get("issue")
    if not isinstance(link,dict):
        raise ValueError(f"#{n} has no authoritative GitHub issue/project binding")
    connection=link.get("projectItems") or {}
    if (connection.get("pageInfo") or {}).get("hasNextPage"):
        raise ValueError(f"#{n} Project item membership truncated")
    rows=[x for x in connection.get("nodes",[]) if (x.get("project") or {}).get("id")==PROJECT_ID]
    if len(rows)>1:
        raise ValueError(f"#{n} duplicate Project #2 items")
    if not rows:
        return {"id":None, "queue_class":None}
    row=rows[0]
    option=row.get("fieldValueByName") or {}
    queue_class=option.get("name")
    if not isinstance(row.get("id"),str) or not row["id"].startswith("PVTI_"):
        raise ValueError(f"#{n} malformed Project #2 item ID")
    if queue_class not in (None,"Editorial"):
        raise ValueError(f"#{n} conflicting live Queue Class {queue_class!r}; no mutation")
    return {"id":row["id"],"queue_class":queue_class}


def editorial_option_id() -> str:
    """Get the live Editorial option, never invent a Project field choice."""
    data=gh("project","field-list","2","--owner","grandchallenge","--format","json")
    fields_list=data.get("fields") or []
    matches=[f for f in fields_list
             if f.get("name")=="Queue Class" and f.get("id")==QUEUE_FIELD_ID]
    if len(matches)!=1:
        raise ValueError("live Project Queue Class field identity missing or ambiguous")
    options=[x.get("id") for x in matches[0].get("options",[])
             if x.get("name")=="Editorial"]
    if len(options)!=1 or not re.fullmatch(r"[0-9a-f]{8}",str(options[0])):
        raise ValueError("live Editorial Project option ID missing or ambiguous")
    return options[0]


def bind_editorial_items(rows: list[dict]) -> None:
    """Create only missing bound items, classify, then verify all before pickup."""
    option=editorial_option_id()
    for row in rows:
        n=row["issue"]
        current=project_record(n)
        if current["id"] is None:
            # The three exact issues have already passed ALL source/identity
            # checks. No generic Project membership publication is permitted.
            added=gh("project","item-add","2","--owner","grandchallenge",
                     "--url",f"https://github.com/{REPO}/issues/{n}",
                     "--format","json")
            new_id=added.get("id")
            current=project_record(n)
            if new_id!=current["id"] or not isinstance(new_id,str):
                raise ValueError(f"#{n} Project attachment identity readback failed")
        if current["queue_class"] is None:
            gh("project","item-edit","--id",current["id"],
               "--project-id",PROJECT_ID,"--field-id",QUEUE_FIELD_ID,
               "--single-select-option-id",option)
        confirmed=project_record(n)
        if confirmed["id"]!=current["id"] or confirmed["queue_class"]!="Editorial":
            raise ValueError(f"#{n} Project Editorial class write/readback failed")
        row["project_item"]=confirmed["id"]
        row["project_class"]="Editorial"
    # Bind all three before exposing ANY one to a worker.
    if len(rows)!=len(DOCKETS) or len({x["project_item"] for x in rows})!=len(DOCKETS):
        raise ValueError("three unique Project Editorial bindings not established")
    for row in rows:
        actual=project_record(row["issue"])
        if actual!={"id":row["project_item"],"queue_class":"Editorial"}:
            raise ValueError(f"#{row['issue']} Project membership changed during activation")


def source_return(problem:int,source_issue:int,assignment:str)->int:
    data=gh("api",f"repos/{REPO}/issues/{source_issue}")
    if data.get("state")!="open" or data.get("pull_request"):
        raise ValueError(f"#{source_issue}: protected source docket not open")
    records=gh("api",f"repos/{REPO}/issues/{source_issue}/comments?per_page=100")
    if not isinstance(records,list) or len(records)>=100:
        raise ValueError(f"#{source_issue}: incomplete source-return comment history")
    matching=[x for x in records if isinstance(x.get("body"),str)
              and x["body"].startswith("RESULT/1\n")
              and f"ASSIGNMENT_ID: {assignment}\n" in x["body"]
              and f"PROBLEM_ID: {problem}\n" in x["body"]]
    if len(matching)!=1 or not matching[0].get("id") or not (matching[0].get("user") or {}).get("login"):
        raise ValueError(f"#{source_issue}: no unique authenticated bound source return")
    return matching[0]["id"]


def preflight() -> list[dict]:
    rows=[]
    for n,(problem,source_id,assignment) in DOCKETS.items():
        data=issue(n)
        labels={x["name"] for x in data.get("labels",[])}
        if (data.get("state")!="open" or data.get("pull_request")
            or not (data.get("title") or "").startswith(f"EC-ED0{n-2554} — Erdős #{problem} — ")
            or not REQUIRED.issubset(labels)
            or {x for x in labels if x.startswith("gcl-pickup:")}
               != {"gcl-pickup:direct-editorial"}
            or {x for x in labels if x.startswith("gcl-state:")}
               not in (set(), {"gcl-state:available"})):
            raise ValueError(f"#{n} editorial identity, pickup or lifecycle drift")
        if "gcl-state:available" in labels and any(
            fields(n).get(k)!=v for k,v in OPTIONS.items()
        ):
            raise ValueError(f"#{n} AVAILABLE label without complete Issue Field readback")
        values=fields(n)
        if values and any(k in values and values[k]!=v for k,v in OPTIONS.items()):
            raise ValueError(f"#{n} organization Issue Field unexpectedly disagrees")
        comments=gh("api",f"repos/{REPO}/issues/{n}/comments?per_page=100")
        if not isinstance(comments,list) or len(comments)>=100 or any(
            (x.get("body") or "").startswith("RESULT/1\n") for x in comments
        ):
            raise ValueError(f"#{n} previously returned or unbounded comment history")
        item=project_record(n)   # absence is staged; wrong class fails closed
        evidence=source_return(problem,source_id,assignment)
        rows.append({"issue":n,"problem":problem,
                     "project_item":item["id"],"project_class":item["queue_class"],
                     "source_issue":source_id,"source_comment":evidence,
                     "was_available": "gcl-state:available" in labels})
    return rows


def apply(rows:list[dict]):
    payload={"issue_field_values":[{"field_id":ISSUE_FIELDS[k],"value":v}
                                   for k,v in OPTIONS.items()]}
    for row in rows:
        n=row["issue"]
        if not row["was_available"]:
            gh("api",f"repos/{REPO}/issues/{n}/issue-field-values",
               "--method","POST","--input","-",payload=payload)
            if any(fields(n).get(k)!=v for k,v in OPTIONS.items()):
                raise ValueError(f"#{n} metadata write/readback failed; availability withheld")
            gh("api",f"repos/{REPO}/issues/{n}/labels",
               "--method","POST","--input","-",
               payload={"labels":["gcl-state:available"]})
        readback=fields(n)
        if any(readback.get(k)!=v for k,v in OPTIONS.items()):
            raise ValueError(f"#{n} authoritative state/campaign/role readback failed")
        data=issue(n)
        labels={x["name"] for x in data.get("labels",[])}
        if ("gcl-state:available" not in labels
            or labels.intersection({"gcl-state:blocked","gcl-state:reserved","gcl-state:returned"})
            or project_record(n)!={"id":row["project_item"],"queue_class":"Editorial"}):
            raise ValueError(f"#{n} post-activation Issue/Project readback failed")


def main() -> int:
    p=argparse.ArgumentParser()
    mode=p.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply",action="store_true")
    mode.add_argument("--dry-run",action="store_true")
    p.add_argument("--receipt",type=Path,required=True)
    args=p.parse_args()
    receipt={"record_type":"ERDOS_COMPENDIUM_EDITORIAL_ADMISSION/1",
             "campaign":CAMPAIGN,"issues":list(DOCKETS),
             "applied":False,"verified":False,"source_sha":os.getenv("GITHUB_SHA"),
             "boundary":"no RESULT/1, chapter acceptance or mathematical authority"}
    try:
        if args.apply and not os.environ.get("GH_TOKEN"):
            raise ValueError("missing scoped Council Clerk token")
        rows=preflight()  # EVERY source and issue identity before FIRST mutation
        receipt["preflight"]=rows
        if args.apply:
            bind_editorial_items(rows)
            receipt["bound_project_items"] = [r["project_item"] for r in rows]
            apply(rows)
            receipt["applied"]=True
            receipt["verified"]=True
        else:
            receipt["dry_run"]=True
        print("EDITORIAL_ADMISSION",json.dumps({"applied":receipt["applied"],
                                                 "issues":list(DOCKETS)},sort_keys=True))
        returncode=0
    except (ValueError,KeyError,OSError,TypeError,subprocess.SubprocessError) as error:
        receipt["blocker"]=str(error)
        print("EDITORIAL_ADMISSION_BLOCKED",str(error),file=sys.stderr)
        returncode=2
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return returncode


if __name__=="__main__":
    raise SystemExit(main())
