#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

OWNER="grandchallenge"
REPO="MATHSOLVE"
API="https://api.github.com"
PREFIX="maintenance/gcl-erdos3-lease-expiry-"
BRANCH_RE=re.compile(r"^maintenance/gcl-erdos3-lease-expiry-gcl-erdos3-e3-v03-ia-([0-9]{3})-e([0-9]+)$")

class ControllerError(RuntimeError):
    pass

@dataclass
class Github:
    token: str
    def request(self, method: str, path: str, payload: dict[str,Any] | None=None) -> Any:
        data=None
        headers={
            "Accept":"application/vnd.github+json",
            "Authorization":f"Bearer {self.token}",
            "X-GitHub-Api-Version":"2022-11-28",
            "User-Agent":"gcl-erdos3-lease-expiry-pr-controller",
        }
        if payload is not None:
            data=json.dumps(payload).encode()
            headers["Content-Type"]="application/json"
        req=urllib.request.Request(API+path,data=data,headers=headers,method=method)
        try:
            with urllib.request.urlopen(req,timeout=30) as response:
                raw=response.read()
        except urllib.error.HTTPError as exc:
            body=exc.read().decode("utf-8","replace")
            raise ControllerError(f"{method} {path} failed: HTTP {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise ControllerError(f"{method} {path} failed: {exc}") from exc
        return json.loads(raw.decode()) if raw else None
    def optional(self,path:str)->Any|None:
        try:
            return self.request("GET",path)
        except ControllerError as exc:
            if "HTTP 404" in str(exc):
                return None
            raise

def content_text(item:dict[str,Any])->str:
    if item.get("encoding")!="base64" or not isinstance(item.get("content"),str):
        raise ControllerError("contents response is not base64 text")
    return base64.b64decode(item["content"]).decode()

def fetch_text(gh:Github,path:str,ref:str)->tuple[str,str]:
    ep=urllib.parse.quote(path,safe="/")
    er=urllib.parse.quote(ref,safe="")
    item=gh.request("GET",f"/repos/{OWNER}/{REPO}/contents/{ep}?ref={er}")
    if not isinstance(item,dict) or not isinstance(item.get("sha"),str):
        raise ControllerError(f"malformed contents response for {path}")
    return content_text(item),item["sha"]

def fetch_json(gh:Github,path:str,ref:str)->dict[str,Any]:
    text,_=fetch_text(gh,path,ref)
    try:
        obj=json.loads(text)
    except json.JSONDecodeError as exc:
        raise ControllerError(f"{path}: invalid JSON") from exc
    if not isinstance(obj,dict):
        raise ControllerError(f"{path}: expected JSON object")
    return obj

def list_branches(gh:Github)->list[str]:
    prefix=urllib.parse.quote(f"heads/{PREFIX}",safe="/")
    refs=gh.optional(f"/repos/{OWNER}/{REPO}/git/matching-refs/{prefix}")
    if refs is None:
        return []
    if not isinstance(refs,list):
        raise ControllerError("matching refs response is not list")
    out=[]
    for row in refs:
        ref=row.get("ref") if isinstance(row,dict) else None
        if isinstance(ref,str) and ref.startswith("refs/heads/"):
            out.append(ref[len("refs/heads/"):])
    return sorted(set(out))

def find_open_pr(gh:Github,branch:str)->dict[str,Any]|None:
    head=urllib.parse.quote(f"{OWNER}:{branch}",safe="")
    rows=gh.request("GET",f"/repos/{OWNER}/{REPO}/pulls?state=open&head={head}&per_page=10")
    if not isinstance(rows,list):
        raise ControllerError("pull list response is not list")
    return rows[0] if rows else None

def compare(gh:Github,branch:str)->dict[str,Any]:
    encoded=urllib.parse.quote(f"main...{branch}",safe=".")
    row=gh.request("GET",f"/repos/{OWNER}/{REPO}/compare/{encoded}")
    if not isinstance(row,dict):
        raise ControllerError("compare response malformed")
    return row

def parse_utc(value:Any,label:str)->datetime:
    if not isinstance(value,str) or not value.endswith("Z"):
        raise ControllerError(f"{label} invalid UTC timestamp")
    try:
        return datetime.fromisoformat(value[:-1]+"+00:00").astimezone(timezone.utc)
    except ValueError as exc:
        raise ControllerError(f"{label} invalid UTC timestamp") from exc

def validate_candidate(gh:Github,branch:str)->dict[str,Any]:
    m=BRANCH_RE.fullmatch(branch)
    if not m:
        raise ControllerError("branch does not match registered lease-expiry syntax")
    serial=int(m.group(1))
    epoch=int(m.group(2))
    dispatch_id=f"GCL-ERDOS3-E3-V03-IA-{serial:03d}"
    dispatch_path=f"work_packages/GCL_ERDOS3/dispatches/{dispatch_id}.json"

    main_dispatch=fetch_json(gh,dispatch_path,"main")
    if main_dispatch.get("dispatch_id")!=dispatch_id or main_dispatch.get("assignment_id")!="E3-V03":
        raise ControllerError(f"{dispatch_id}: protected dispatch identity mismatch")
    if main_dispatch.get("lease_epoch")!=epoch:
        raise ControllerError(f"{dispatch_id}: branch epoch does not match protected dispatch")

    # If an earlier/manual bounded recovery already protected this expiry, do not open another PR.
    if main_dispatch.get("state")=="LEASE_EXPIRED__NO_RETURN":
        return {"branch":branch,"dispatch_id":dispatch_id,"lease_epoch":epoch,"state":"ALREADY_PROTECTED"}

    if main_dispatch.get("state")!="DISPATCHED__AWAITING_RETURN":
        raise ControllerError(f"{dispatch_id}: protected dispatch is not awaiting return")
    if main_dispatch.get("lease_policy_id")!="GCL-IA-LEASE-25M-24M-001":
        raise ControllerError(f"{dispatch_id}: lease policy mismatch")
    if main_dispatch.get("replay_budget_ordinal")!=1:
        raise ControllerError(f"{dispatch_id}: replay ordinal drift")

    cmp=compare(gh,branch)
    files=cmp.get("files")
    if not isinstance(files,list):
        raise ControllerError(f"{dispatch_id}: compare response lacks files")
    changed=sorted(
        row["filename"] for row in files
        if isinstance(row,dict) and isinstance(row.get("filename"),str)
    )
    allowed=sorted([
        "work_packages/GCL_ERDOS3/CAMPAIGN.json",
        "work_packages/GCL_ERDOS3/FRONTIER.json",
        dispatch_path,
    ])
    if changed!=allowed:
        raise ControllerError(f"{dispatch_id}: expiry branch changed-file set mismatch: {changed}")

    branch_dispatch=fetch_json(gh,dispatch_path,branch)
    checks={
        "dispatch_id":branch_dispatch.get("dispatch_id")==dispatch_id,
        "assignment_id":branch_dispatch.get("assignment_id")=="E3-V03",
        "state":branch_dispatch.get("state")=="LEASE_EXPIRED__NO_RETURN",
        "dispatch_status":branch_dispatch.get("dispatch_status")=="LEASE_EXPIRED__NO_RETURN",
        "lease_epoch":branch_dispatch.get("lease_epoch")==epoch,
        "lease_policy_id":branch_dispatch.get("lease_policy_id")=="GCL-IA-LEASE-25M-24M-001",
        "replay_budget_ordinal":branch_dispatch.get("replay_budget_ordinal")==1,
        "replay_budget_consumed":branch_dispatch.get("replay_budget_consumed") is False,
        "mathematical_replay_completed":branch_dispatch.get("mathematical_replay_completed") is False,
        "valid_result_count_at_expiry":branch_dispatch.get("valid_result_count_at_expiry")==0,
        "stale_return_fenced":branch_dispatch.get("stale_return_fenced") is True,
    }
    failed=sorted(k for k,v in checks.items() if not v)
    if failed:
        raise ControllerError(f"{dispatch_id}: expired dispatch validation failed: {', '.join(failed)}")
    activation=branch_dispatch.get("lease_activation_comment_id")
    if not isinstance(activation,int):
        raise ControllerError(f"{dispatch_id}: activation comment id missing")
    start=parse_utc(branch_dispatch.get("lease_started_at_observed"),"lease_started_at_observed")
    expiry=parse_utc(branch_dispatch.get("lease_expires_at_observed"),"lease_expires_at_observed")
    if int((expiry-start).total_seconds())!=25*60:
        raise ControllerError(f"{dispatch_id}: observed lease duration is not 25 minutes")

    campaign=fetch_json(gh,"work_packages/GCL_ERDOS3/CAMPAIGN.json",branch)
    if campaign.get("status")!="ACTIVE__E3_V03_LEASE_EXPIRED":
        raise ControllerError(f"{dispatch_id}: campaign expiry status mismatch")
    if campaign.get("dispatch_state")!="VERIFY_LEASE_EXPIRED__REISSUE_REQUIRED":
        raise ControllerError(f"{dispatch_id}: campaign dispatch state mismatch")
    if campaign.get("active_dispatches")!={}:
        raise ControllerError(f"{dispatch_id}: expired dispatch remains active")
    lease_key=f"E3-V03-LEASE-{epoch:03d}"
    completed=campaign.get("completed_dispatches",{}).get(lease_key,{})
    if completed.get("dispatch_id")!=dispatch_id or completed.get("valid_result_count")!=0 or completed.get("replay_budget_consumed") is not False:
        raise ControllerError(f"{dispatch_id}: campaign completion receipt mismatch")

    frontier=fetch_json(gh,"work_packages/GCL_ERDOS3/FRONTIER.json",branch)
    nodes={row.get("id"):row for row in frontier.get("nodes",[]) if isinstance(row,dict)}
    v03=nodes.get("E3-V-B03",{})
    if v03.get("status")!="LEASE_EXPIRED__REISSUE_REQUIRED" or v03.get("replay_budget_consumed")!=0:
        raise ControllerError(f"{dispatch_id}: verification node expiry/replay state mismatch")
    candidate=nodes.get("E3-Q4-GLUING-RADIUS",{})
    if candidate.get("status")!="FORMULATED_PENDING_VERIFY":
        raise ControllerError(f"{dispatch_id}: expiry branch altered candidate promotion state")
    if frontier.get("active_frontier")!=["E3-Q4-DENSITY-LOSS"]:
        raise ControllerError(f"{dispatch_id}: expiry branch altered active frontier")

    existing=find_open_pr(gh,branch)
    return {
        "branch":branch,
        "dispatch_id":dispatch_id,
        "lease_epoch":epoch,
        "activation_comment_id":activation,
        "lease_started_at":branch_dispatch["lease_started_at_observed"],
        "lease_expires_at":branch_dispatch["lease_expires_at_observed"],
        "state":"OPEN_PR_EXISTS" if existing else "PR_REQUIRED",
    }

def open_pr(gh:Github,item:dict[str,Any])->dict[str,Any]:
    title=f"GCL-ERDOS3: reconcile silent V03 lease epoch {item['lease_epoch']}"
    body=(
        f"Bounded Release Trust lifecycle PR for {item['dispatch_id']}.\n\n"
        f"- activation comment: \`{item['activation_comment_id']}\`\n"
        f"- lease start: \`{item['lease_started_at']}\`\n"
        f"- lease expiry: \`{item['lease_expires_at']}\`\n"
        "- valid RESULT/1 count at expiry: \`0\`\n"
        "- mathematical replay budget consumed: \`false\`\n"
        "- canonical claim effect: NONE\n"
        "- frontier promotion effect: NONE\n\n"
        "This controller only opens the ordinary PR for an already-created and validated lifecycle branch. "
        "Protected MATHSOLVE CI owns admission. No mathematics is adjudicated or promoted here."
    )
    pr=gh.request("POST",f"/repos/{OWNER}/{REPO}/pulls",{
        "title":title,"head":item["branch"],"base":"main","body":body
    })
    if not isinstance(pr,dict) or not isinstance(pr.get("number"),int):
        raise ControllerError("pull request creation returned malformed response")
    return pr

def run(apply:bool)->dict[str,Any]:
    token=os.environ.get("MATHSOLVE_LEASE_EXPIRY_PR_TOKEN") or os.environ.get("MATHSOLVE_INTAKE_PR_TOKEN","")
    if not token:
        raise ControllerError("MATHSOLVE_LEASE_EXPIRY_PR_TOKEN is empty")
    gh=Github(token)
    report={
        "schema_version":"1.0.0",
        "controller":"MP_GCL_ERDOS3_LEASE_EXPIRY_PR_CONTROLLER_001",
        "target_repository":f"{OWNER}/{REPO}",
        "apply":apply,
        "authority":{"contents":"read","pull_requests":"write","merge":False,"review":False,"campaign_mutation":False,"mathematical_adjudication":False},
        "branches":[],"opened_prs":[],"errors":[],"authority_created":False,
    }
    for branch in list_branches(gh):
        try:
            item=validate_candidate(gh,branch)
            report["branches"].append(item)
            if item["state"]!="PR_REQUIRED" or not apply:
                continue
            pr=open_pr(gh,item)
            report["opened_prs"].append({
                "dispatch_id":item["dispatch_id"],"lease_epoch":item["lease_epoch"],
                "branch":branch,"pr_number":pr["number"],"pr_url":pr.get("html_url")
            })
        except ControllerError as exc:
            report["errors"].append({"branch":branch,"error":str(exc)})
    return report

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--apply",action="store_true")
    ap.add_argument("--report",type=Path,required=True)
    args=ap.parse_args()
    try:
        report=run(args.apply)
    except ControllerError as exc:
        report={"schema_version":"1.0.0","controller":"MP_GCL_ERDOS3_LEASE_EXPIRY_PR_CONTROLLER_001","apply":args.apply,"fatal_error":str(exc),"authority_created":False}
        args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
        print(str(exc),file=sys.stderr)
        return 2
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps(report,sort_keys=True))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
