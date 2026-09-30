#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import time
import urllib.parse
from pathlib import Path
from typing import Any

from ci.ns_ci_intake_pr_controller import ControllerError, Github

OWNER = "grandchallenge"
SOLVE = "MATHSOLVE"
PROGRAMME = "MATH-PROGRAMME"
BRANCH_PREFIX = "intake/openmath-"
DISPATCH_RE = re.compile(r"^(OM26-H([2-7])-WP([0-9]{2}))-IA-([0-9]{3})$")
PIPELINE = ["RETURNED","CAPTURED","REPLAYED","ADJUDICATED","ADVANCED"]


def content_text(item: dict[str, Any]) -> str:
    if item.get("encoding") != "base64" or not isinstance(item.get("content"), str):
        raise ControllerError("GitHub contents response is not base64 text")
    return base64.b64decode(item["content"]).decode("utf-8")


def fetch_content(gh: Github, repo: str, path: str, ref: str) -> tuple[str, str]:
    p = urllib.parse.quote(path, safe="/")
    r = urllib.parse.quote(ref, safe="")
    item = gh.request("GET", f"/repos/{OWNER}/{repo}/contents/{p}?ref={r}")
    if not isinstance(item, dict) or not isinstance(item.get("sha"), str):
        raise ControllerError(f"{repo}:{path}@{ref}: malformed contents response")
    return content_text(item), item["sha"]


def optional_content(gh: Github, repo: str, path: str, ref: str) -> tuple[str, str] | None:
    try:
        return fetch_content(gh, repo, path, ref)
    except ControllerError as exc:
        if "HTTP 404" in str(exc):
            return None
        raise


def branch_names(gh: Github) -> list[str]:
    prefix = urllib.parse.quote(f"heads/{BRANCH_PREFIX}", safe="/")
    refs = gh.get_optional(f"/repos/{OWNER}/{SOLVE}/git/matching-refs/{prefix}")
    if refs is None:
        return []
    if not isinstance(refs, list):
        raise ControllerError("OPENMATH matching refs response malformed")
    out=[]
    for row in refs:
        ref=row.get("ref") if isinstance(row,dict) else None
        if isinstance(ref,str) and ref.startswith("refs/heads/"):
            out.append(ref[len("refs/heads/"):])
    return sorted(set(out))


def dispatch_parts(branch: str) -> tuple[str, str, str]:
    if not branch.startswith(BRANCH_PREFIX):
        raise ControllerError("not an OPENMATH intake branch")
    dispatch=branch[len(BRANCH_PREFIX):].upper()
    match=DISPATCH_RE.fullmatch(dispatch)
    if not match:
        raise ControllerError(f"invalid OPENMATH dispatch branch: {branch}")
    assignment,hill_no,wp,_ia=match.groups()
    return dispatch, f"OM26-H{hill_no}", f"WP{wp}"


def base_for(dispatch: str) -> tuple[str,str,str]:
    m=DISPATCH_RE.fullmatch(dispatch)
    if not m:
        raise ControllerError(f"invalid dispatch: {dispatch}")
    _assignment,hill_no,wp,_ia=m.groups()
    base=f"contributions/OPENMATH-2026/OM26-H{hill_no}/WP{wp}"
    return base,f"OM26-H{hill_no}",f"WP{wp}"


def compare_files(gh: Github, branch: str) -> list[str]:
    encoded=urllib.parse.quote(f"main...{branch}",safe=".")
    value=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/compare/{encoded}")
    files=value.get("files") if isinstance(value,dict) else None
    if not isinstance(files,list):
        raise ControllerError("OPENMATH compare response lacks files")
    return sorted(
        x["filename"] for x in files
        if isinstance(x,dict) and isinstance(x.get("filename"),str)
    )


def find_pr(gh: Github, repo: str, branch: str, state: str="open") -> dict[str,Any] | None:
    head=urllib.parse.quote(f"{OWNER}:{branch}",safe="")
    pulls=gh.request("GET",f"/repos/{OWNER}/{repo}/pulls?state={state}&head={head}&per_page=20")
    if not isinstance(pulls,list):
        raise ControllerError(f"{repo}: PR list response malformed")
    return pulls[0] if pulls else None


def open_pr(gh: Github, repo: str, branch: str, title: str, body: str) -> dict[str,Any]:
    pr=gh.request("POST",f"/repos/{OWNER}/{repo}/pulls",{
        "title":title,"head":branch,"base":"main","body":body
    })
    if not isinstance(pr,dict) or not isinstance(pr.get("number"),int):
        raise ControllerError(f"{repo}: PR creation malformed")
    return pr


def enable_auto_merge(gh: Github, pr: dict[str,Any]) -> None:
    node=pr.get("node_id")
    if not isinstance(node,str):
        raise ControllerError("PR node_id unavailable for auto-merge")
    query="""mutation($id:ID!){enablePullRequestAutoMerge(input:{pullRequestId:$id,mergeMethod:SQUASH}){pullRequest{number}}}"""
    try:
        gh.request("POST","/graphql",{"query":query,"variables":{"id":node}})
    except ControllerError as exc:
        # Idempotent retries may report that auto-merge is already enabled.
        if "already enabled" not in str(exc).lower():
            raise


def wait_merged(gh: Github, repo: str, number: int, timeout: int=2700) -> dict[str,Any]:
    deadline=time.time()+timeout
    last=None
    while time.time()<deadline:
        pr=gh.request("GET",f"/repos/{OWNER}/{repo}/pulls/{number}")
        if isinstance(pr,dict):
            last=pr
            if pr.get("merged_at"):
                return pr
            if pr.get("state")=="closed" and not pr.get("merged_at"):
                raise ControllerError(f"{repo} PR #{number} closed without merge")
        time.sleep(10)
    raise ControllerError(f"{repo} PR #{number} did not merge before timeout; last={last and last.get('mergeable_state')}")


def validate_candidate(gh: Github, branch: str) -> dict[str,Any]:
    dispatch,hill,wp=dispatch_parts(branch)
    base,_,_=base_for(dispatch)
    manifest_path=f"{base}/lifecycle/{dispatch}/MANIFEST.json"
    manifest_item=optional_content(gh,SOLVE,manifest_path,branch)
    if manifest_item is None:
        raise ControllerError(f"{dispatch}: lifecycle MANIFEST missing")
    manifest_text,manifest_blob=manifest_item
    try:
        manifest=json.loads(manifest_text)
    except json.JSONDecodeError as exc:
        raise ControllerError(f"{dispatch}: invalid lifecycle manifest") from exc
    checks={
        "record_type":manifest.get("record_type")=="OPENMATH_LIFECYCLE_CANDIDATE",
        "campaign":manifest.get("campaign")=="OPENMATH-2026",
        "dispatch":manifest.get("dispatch_id")==dispatch,
        "hill":manifest.get("hill")==hill,
        "pipeline":manifest.get("pipeline")==PIPELINE,
        "certification":manifest.get("certification_effect") is False,
        "competition":manifest.get("competition_effect") is False,
    }
    failed=[k for k,v in checks.items() if not v]
    if failed:
        raise ControllerError(f"{dispatch}: lifecycle manifest failed {', '.join(failed)}")
    changed=compare_files(gh,branch)
    expected=manifest.get("changed_paths")
    if not isinstance(expected,list) or sorted(expected)!=changed:
        raise ControllerError(f"{dispatch}: branch diff differs from lifecycle manifest")
    mandatory=[
        manifest.get("programme_projection_path"),
        f"{base}/raw/{dispatch}/github-comment-{manifest.get('comment_id')}.md",
        f"{base}/receipts/{dispatch}/github-comment-{manifest.get('comment_id')}.json",
        manifest_path,
        ".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json",
        "work_packages/OPENMATH_2026/HILL_LANES.json",
    ]
    for path in mandatory:
        if not isinstance(path,str) or path not in changed:
            raise ControllerError(f"{dispatch}: mandatory lifecycle artifact missing: {path}")
    projection_text,projection_blob=fetch_content(gh,SOLVE,manifest["programme_projection_path"],branch)
    projection=json.loads(projection_text)
    if projection.get("pipeline_trace")!=PIPELINE or projection.get("source_dispatch")!=dispatch:
        raise ControllerError(f"{dispatch}: Programme projection identity drift")
    return {
        "dispatch_id":dispatch,"hill":hill,"wp":wp,"branch":branch,
        "manifest_path":manifest_path,"manifest_blob":manifest_blob,
        "projection_path":manifest["programme_projection_path"],"projection_blob":projection_blob,
        "successor_assignment":manifest.get("successor_assignment"),
        "state":"CANDIDATE_VALIDATED",
    }


def main_has_manifest(gh: Github, item: dict[str,Any]) -> bool:
    return optional_content(gh,SOLVE,item["manifest_path"],"main") is not None


def protected_raw_exists(gh: Github, dispatch: str) -> bool:
    base, _hill, _wp = base_for(dispatch)
    raw_dir = urllib.parse.quote(f"{base}/raw/{dispatch}", safe="/")
    items = gh.get_optional(f"/repos/{OWNER}/{SOLVE}/contents/{raw_dir}?ref=main")
    if items is None:
        return False
    if not isinstance(items, list):
        raise ControllerError(f"{dispatch}: protected raw directory response malformed")
    return any(
        isinstance(row, dict)
        and isinstance(row.get("name"), str)
        and re.fullmatch(r"github-comment-[0-9]+[.]md", row["name"])
        for row in items
    )


def ensure_solve_merge(gh: Github, item: dict[str,Any]) -> dict[str,Any]:
    if main_has_manifest(gh,item):
        # Find the historical merged PR if available; main SHA is sufficient otherwise.
        ref=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/git/ref/heads/main")
        sha=ref.get("object",{}).get("sha") if isinstance(ref,dict) else None
        return {"merge_commit_sha":sha,"number":None,"already_protected":True}
    pr=find_pr(gh,SOLVE,item["branch"])
    if pr is None:
        pr=open_pr(
            gh,SOLVE,item["branch"],
            f"OPENMATH lifecycle: {item['dispatch_id']}",
            "Protected lifecycle candidate generated from one validated RESULT/1. "
            "The candidate carries the return through CAPTURED, REPLAYED, bounded ADJUDICATED, "
            "and ADVANCED successor state. No certification or competition authority is created.",
        )
    enable_auto_merge(gh,pr)
    merged=wait_merged(gh,SOLVE,pr["number"])
    return {
        "merge_commit_sha":merged.get("merge_commit_sha"),
        "number":merged["number"],
        "already_protected":False,
    }


def live_solve_projection(gh: Github, item: dict[str,Any]) -> tuple[dict[str,Any],dict[str,str]]:
    projection_text,_=fetch_content(gh,SOLVE,item["projection_path"],"main")
    projection=json.loads(projection_text)
    paths=[
        "work_packages/OPENMATH_2026/HILL_LANES.json",
        ".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json",
        ".gcl/campaigns/OPENMATH-2026/LIFECYCLE_CONTRACT.json",
        "handoffs/OPENMATH-2026/CEX_TRANSPORT_CONTRACT.md",
        item["manifest_path"],
        item["projection_path"],
    ]
    blobs={}
    for path in paths:
        _text,sha=fetch_content(gh,SOLVE,path,"main")
        blobs[path]=sha
    return projection,blobs


def render_status(state: dict[str,Any]) -> str:
    lines=[
        "# OPENMATH-2026 — Current Campaign State",
        "",
        "> **Canonical machine authority:** `governance/openmath_2026_campaign_state.json`",
        ">",
        "> This page is a human projection of that record. It is not a second source of truth.",
        "",
        "## Current topology",
        "",
        "OPENMATH-2026 has exactly seven first-class current hill lanes: **H1, H2, H3, H4, H5, H6, H7**.",
        "",
        "## Campaign summary",
        "",
        f"- Hills: **{state['summary']['hill_count']}**",
        f"- Independent-agent state: **{state['summary']['external_agents']['accepted']} ACCEPTED; {state['summary']['external_agents']['leased_not_launched']} LEASED_NOT_LAUNCHED**",
        f"- Official competition submissions: **{state['summary']['competition']['submitted_hills']}**",
        "",
        "## Seven-hill control board",
        "",
        "| Hill | Problem | Independent agent | Competition |",
        "|---|---|---|---|",
    ]
    for row in state["hills"]:
        agent=row.get("external_agent",{})
        competition=row.get("competition",{})
        lines.append(
            f"| {row['hill_slot'].replace('OM26-','')} | {row['title']} | "
            f"**{agent.get('lifecycle')}** — {agent.get('agent_ref')} / #{agent.get('issue_number')} | "
            f"{competition.get('official_submission','NOT_SUBMITTED')} |"
        )
    lines += [
        "",
        "## Current next action",
        "",
        "**Launch each exact active lease whose protected lifecycle is `LEASED_NOT_LAUNCHED` from its registered immutable task URL.**",
        "",
        "Returns use `GCL-RETURN-RELAY/1`. The protected OPENMATH lifecycle controller carries valid returns through capture, replay, bounded adjudication, Programme reconciliation, and successor generation without manual evidence transport or controller wake-up.",
        "",
        "## CORE CLARITY rule",
        "",
        "Operational state and declared campaign state are one protected system. The frozen lifecycle is:",
        "",
        "`READY → LAUNCHED → RETURNED → CAPTURED → REPLAYED → ADJUDICATED → ADVANCED`",
        "",
    ]
    return "\n".join(lines)


def apply_projection_to_state(state: dict[str,Any], projection: dict[str,Any], solve_sha: str, blobs: dict[str,str]) -> dict[str,Any]:
    hill=projection["hill"]
    row=next(x for x in state["hills"] if x["hill_slot"]==hill)
    old_agent=row.get("external_agent",{})
    pred=projection["predecessor"]
    succ=projection["successor"]

    row["solve"]["state"]=f"{succ['assignment_id'].rsplit('-',1)[-1]}_LEASED_NOT_LAUNCHED"
    row["solve"]["frontier"]="AUTOMATED_REPLAY_CLOSURE_REQUIRED"
    row["external_agent"]={
        "assignment_id":succ["assignment_id"],
        "dispatch_id":succ["dispatch_id"],
        "agent_ref":succ["agent_ref"],
        "issue_number":succ["issue_number"],
        "lifecycle":"LEASED_NOT_LAUNCHED",
        "launch_evidence":None,
        "return_evidence":None,
        "adjudication":"NOT_STARTED",
        "predecessor":{
            "assignment_id":pred["assignment_id"],
            "agent_ref":pred["agent_ref"],
            "issue_number":old_agent.get("issue_number"),
            "lifecycle":"ACCEPTED",
            "adjudication":pred["adjudication"],
            "accepted_claims":pred.get("accepted_claims",[]),
        },
    }
    row["next_action"]=f"LAUNCH_EXACT_ACTIVE_LEASE__{succ['assignment_id']}__IMMUTABLE_LINK_IN_RELAY_OUT"

    summary=projection["external_agent_summary"]
    state["summary"]["external_agents"]={
        "captured_pending_adjudication":0,
        "leased_not_launched":int(summary.get("leased_not_launched_agents",0)),
        "launched_without_return":int(summary.get("launched_agents",0)),
        "accepted":int(summary.get("accepted_agents",0)),
    }
    selected=[
        x["hill_slot"] for x in state["hills"]
        if x.get("external_agent",{}).get("lifecycle")=="LEASED_NOT_LAUNCHED"
    ]
    state["next_action"]={
        "id":"launch_pending_exact_hill_leases",
        "selection_rule":"Select each current hill lane whose exact active assignment lifecycle is LEASED_NOT_LAUNCHED.",
        "currently_selected":selected,
        "description":"Launch each selected lane from its registered immutable LINK_IN_RELAY_OUT task URL. Valid returns are carried automatically through CAPTURED, REPLAYED, ADJUDICATED, and ADVANCED.",
        "completion_test":"Every returned result either reaches ADVANCED automatically or leaves a protected infrastructure blocker; no human evidence shuttling or controller prompt is permitted.",
    }
    state.setdefault("automation",{})["openmath_lifecycle"]={
        "contract":"READY→LAUNCHED→RETURNED→CAPTURED→REPLAYED→ADJUDICATED→ADVANCED",
        "last_transition_dispatch":projection["source_dispatch"],
        "last_transition_hill":hill,
        "last_transition_result":"ADVANCED",
        "manual_transport_required":False,
        "manual_controller_wake_required":False,
    }
    state["domain_bindings"]["solve"]["observed_main"]=solve_sha
    artifacts=state["domain_bindings"]["solve"]["artifacts"]
    amap={x["path"]:x for x in artifacts}
    for path,sha in blobs.items():
        amap[path]={"path":path,"git_blob_sha1":sha}
    state["domain_bindings"]["solve"]["artifacts"]=list(amap.values())
    return state


def create_branch(gh: Github, repo: str, branch: str) -> str:
    main=gh.request("GET",f"/repos/{OWNER}/{repo}/git/ref/heads/main")
    sha=main.get("object",{}).get("sha") if isinstance(main,dict) else None
    if not isinstance(sha,str):
        raise ControllerError(f"{repo}: main ref unavailable")
    existing=gh.get_optional(f"/repos/{OWNER}/{repo}/git/ref/heads/{urllib.parse.quote(branch,safe='/')}")
    if existing is None:
        gh.request("POST",f"/repos/{OWNER}/{repo}/git/refs",{"ref":f"refs/heads/{branch}","sha":sha})
    return sha


def put_file(gh: Github, repo: str, branch: str, path: str, content: str, message: str) -> None:
    current=optional_content(gh,repo,path,branch)
    payload={
        "message":message,
        "content":base64.b64encode(content.encode("utf-8")).decode("ascii"),
        "branch":branch,
    }
    if current is not None:
        payload["sha"]=current[1]
    p=urllib.parse.quote(path,safe="/")
    gh.request("PUT",f"/repos/{OWNER}/{repo}/contents/{p}",payload)


def ensure_programme_reconciliation(
    programme_gh: Github,
    projection: dict[str,Any],
    solve_sha: str,
    blobs: dict[str,str],
) -> dict[str,Any]:
    dispatch=projection["source_dispatch"]
    state_text,_=fetch_content(programme_gh,PROGRAMME,"governance/openmath_2026_campaign_state.json","main")
    state=json.loads(state_text)
    if state.get("automation",{}).get("openmath_lifecycle",{}).get("last_transition_dispatch")==dispatch:
        ref=programme_gh.request("GET",f"/repos/{OWNER}/{PROGRAMME}/git/ref/heads/main")
        return {"already_reconciled":True,"merge_commit_sha":ref.get("object",{}).get("sha"),"number":None}

    state=apply_projection_to_state(state,projection,solve_sha,blobs)
    branch=f"reconcile/openmath-{dispatch.lower()}"
    create_branch(programme_gh,PROGRAMME,branch)
    put_file(
        programme_gh,PROGRAMME,branch,
        "governance/openmath_2026_campaign_state.json",
        json.dumps(state,indent=2)+"\n",
        f"OPENMATH: reconcile lifecycle {dispatch}",
    )
    put_file(
        programme_gh,PROGRAMME,branch,
        "docs/campaigns/OPENMATH_2026_STATUS.md",
        render_status(state),
        f"OPENMATH: project lifecycle {dispatch}",
    )
    receipt={
        "schema_version":"1.0.0",
        "record_type":"OPENMATH_LIFECYCLE_PROGRAMME_RECONCILIATION",
        "dispatch_id":dispatch,
        "hill":projection["hill"],
        "pipeline":PIPELINE,
        "result":"ADVANCED",
        "solve_protected_main":solve_sha,
        "manual_transport_required":False,
        "manual_controller_wake_required":False,
        "claim_boundary":"Programme state reconciliation only; no new certification or competition authority.",
    }
    put_file(
        programme_gh,PROGRAMME,branch,
        f"governance/openmath_2026_lifecycle_reconciliations/{dispatch}.json",
        json.dumps(receipt,indent=2)+"\n",
        f"OPENMATH: receipt lifecycle {dispatch}",
    )
    pr=find_pr(programme_gh,PROGRAMME,branch)
    if pr is None:
        pr=open_pr(
            programme_gh,PROGRAMME,branch,
            f"OPENMATH lifecycle reconcile: {dispatch}",
            "Automatic Core Clarity projection after protected Solve lifecycle advancement. "
            "No mathematical certification or competition authority is created.",
        )
    enable_auto_merge(programme_gh,pr)
    merged=wait_merged(programme_gh,PROGRAMME,pr["number"])
    return {"already_reconciled":False,"number":merged["number"],"merge_commit_sha":merged.get("merge_commit_sha")}


def verify_advanced(programme_gh: Github, projection: dict[str,Any]) -> None:
    state_text,_=fetch_content(programme_gh,PROGRAMME,"governance/openmath_2026_campaign_state.json","main")
    state=json.loads(state_text)
    auto=state.get("automation",{}).get("openmath_lifecycle",{})
    if auto.get("last_transition_dispatch")!=projection["source_dispatch"] or auto.get("last_transition_result")!="ADVANCED":
        raise ControllerError("Programme protected state did not reach ADVANCED")
    hill=next(x for x in state["hills"] if x["hill_slot"]==projection["hill"])
    if hill.get("external_agent",{}).get("assignment_id")!=projection["successor"]["assignment_id"]:
        raise ControllerError("Programme successor projection mismatch")


def run(apply: bool) -> dict[str,Any]:
    solve_token=os.environ.get("MATHSOLVE_LIFECYCLE_TOKEN","")
    programme_token=os.environ.get("MATH_PROGRAMME_LIFECYCLE_TOKEN","")
    if not solve_token or not programme_token:
        raise ControllerError("lifecycle controller tokens are unavailable")
    solve_gh=Github(solve_token)
    programme_gh=Github(programme_token)
    report={
        "schema_version":"1.0.0",
        "controller":"OPENMATH_UNATTENDED_LIFECYCLE_CONTROLLER",
        "pipeline":PIPELINE,
        "apply":apply,
        "processed":[],
        "errors":[],
        "authority_created":False,
    }
    for branch in branch_names(solve_gh):
        try:
            try:
                item=validate_candidate(solve_gh,branch)
            except ControllerError as exc:
                if "lifecycle MANIFEST missing" not in str(exc):
                    raise
                dispatch, hill, wp = dispatch_parts(branch)
                if not protected_raw_exists(solve_gh, dispatch):
                    raise
                report["processed"].append({
                    "dispatch_id": dispatch,
                    "hill": hill,
                    "wp": wp,
                    "branch": branch,
                    "state": "LEGACY_ALREADY_PROTECTED",
                })
                continue
            if not apply:
                report["processed"].append({**item,"state":"VALIDATED_DRY_RUN"})
                continue
            solve_merge=ensure_solve_merge(solve_gh,item)
            solve_sha=solve_merge.get("merge_commit_sha")
            if not isinstance(solve_sha,str):
                ref=solve_gh.request("GET",f"/repos/{OWNER}/{SOLVE}/git/ref/heads/main")
                solve_sha=ref.get("object",{}).get("sha")
            projection,blobs=live_solve_projection(solve_gh,item)
            programme_merge=ensure_programme_reconciliation(programme_gh,projection,solve_sha,blobs)
            verify_advanced(programme_gh,projection)
            report["processed"].append({
                **item,
                "solve_merge":solve_merge,
                "programme_merge":programme_merge,
                "state":"ADVANCED",
            })
        except (ControllerError,KeyError,ValueError,json.JSONDecodeError) as exc:
            report["errors"].append({"branch":branch,"error":str(exc)})
    return report


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--apply",action="store_true")
    parser.add_argument("--report",type=Path,required=True)
    args=parser.parse_args()
    try:
        report=run(args.apply)
    except ControllerError as exc:
        report={"schema_version":"1.0.0","controller":"OPENMATH_UNATTENDED_LIFECYCLE_CONTROLLER","fatal_error":str(exc),"authority_created":False}
        args.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        print(str(exc),file=os.sys.stderr)
        return 2
    args.report.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,sort_keys=True))
    return 1 if report["errors"] else 0


if __name__=="__main__":
    raise SystemExit(main())
