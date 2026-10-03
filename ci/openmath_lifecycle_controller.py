#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import shutil
import subprocess
import tempfile
import json
import os
import re
import time
import urllib.parse
from pathlib import Path
from typing import Any

try:
    from ci.ns_ci_intake_pr_controller import ControllerError, Github
except ModuleNotFoundError:
    from ns_ci_intake_pr_controller import ControllerError, Github

OWNER = "grandchallenge"
SOLVE = "MATHSOLVE"
PROGRAMME = "MATH-PROGRAMME"
BRANCH_PREFIX = "intake/openmath-"
RECOVERY_PREFIX = "candidate/openmath-"
DISPATCH_RE = re.compile(r"^(OM26-H([1-7])-WP([0-9]{2}))-IA-([0-9]{3})$")
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
    out: set[str] = set()
    for branch_prefix in (BRANCH_PREFIX, RECOVERY_PREFIX):
        prefix = urllib.parse.quote(f"heads/{branch_prefix}", safe="/")
        refs = gh.get_optional(f"/repos/{OWNER}/{SOLVE}/git/matching-refs/{prefix}")
        if refs is None:
            continue
        if not isinstance(refs, list):
            raise ControllerError("OPENMATH matching refs response malformed")
        for row in refs:
            ref = row.get("ref") if isinstance(row, dict) else None
            if isinstance(ref, str) and ref.startswith("refs/heads/"):
                name = ref[len("refs/heads/"):]
                if name.startswith(branch_prefix):
                    out.add(name)
    return sorted(out)


def dispatch_parts(branch: str) -> tuple[str, str, str]:
    branch_prefix = next(
        (prefix for prefix in (BRANCH_PREFIX, RECOVERY_PREFIX) if branch.startswith(prefix)), None
    )
    if branch_prefix is None:
        raise ControllerError("not a registered OPENMATH lifecycle branch")
    dispatch=branch[len(branch_prefix):].upper()
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


def validate_candidate(gh: Github, branch: str, ref: str | None = None) -> dict[str,Any]:
    dispatch,hill,wp=dispatch_parts(branch)
    source=ref or branch
    base,_,_=base_for(dispatch)
    manifest_path=f"{base}/lifecycle/{dispatch}/MANIFEST.json"
    manifest_item=optional_content(gh,SOLVE,manifest_path,source)
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
    protected=optional_content(gh,SOLVE,manifest_path,"main")
    if protected is None:
        changed=compare_files(gh,branch)
        expected=manifest.get("changed_paths")
        if not isinstance(expected,list) or sorted(expected)!=changed:
            raise ControllerError(f"{dispatch}: branch diff differs from lifecycle manifest")
    else:
        if protected[1] != manifest_blob:
            raise ControllerError(f"{dispatch}: protected lifecycle manifest differs from candidate")
    mandatory=[
        manifest.get("programme_projection_path"),
        f"{base}/raw/{dispatch}/github-comment-{manifest.get('comment_id')}.md",
        f"{base}/receipts/{dispatch}/github-comment-{manifest.get('comment_id')}.json",
        manifest_path,
        ".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json",
        "work_packages/OPENMATH_2026/HILL_LANES.json",
    ]
    for path in mandatory:
        if not isinstance(path,str):
            raise ControllerError(f"{dispatch}: mandatory lifecycle artifact path malformed")
        if protected is not None:
            if optional_content(gh,SOLVE,path,"main") is None:
                raise ControllerError(f"{dispatch}: protected lifecycle artifact missing: {path}")
        elif path not in changed:
            raise ControllerError(f"{dispatch}: mandatory lifecycle artifact missing: {path}")
    projection_text,projection_blob=fetch_content(gh,SOLVE,manifest["programme_projection_path"],source)
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


def ensure_solve_merge(gh: Github, item: dict[str,Any], checkout: Path | None = None) -> dict[str,Any]:
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
    live=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}")
    if live.get("mergeable") is False:
        if checkout is None or not checkout.is_dir():
            raise ControllerError("protected Solve checkout unavailable for candidate refresh")
        refreshed=recover_legacy(gh,item["branch"],checkout,refresh=True)
        item.update(refreshed)
        pr=find_pr(gh,SOLVE,item["branch"])
        if pr is None:
            pr=open_pr(gh,SOLVE,item["branch"],f"OPENMATH lifecycle: {item['dispatch_id']}",
                       "Rebuilt from protected main and the unchanged first-result lock after concurrent lifecycle advancement. No claim promotion.")
    enable_auto_merge(gh,pr)
    merged=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}")
    if not merged.get("merged_at"):
        return {"number":pr["number"],"pending":True,"branch":item["branch"]}
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
        if path == ".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json":
            projection["external_agent_summary"]=json.loads(_text)["mathematics_release_policy"]["summary"]
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
    support_rows=[(r["hill_slot"],slot,a) for r in state["hills"]
                  for slot,a in r.get("supporting_agents",{}).items()]
    if support_rows:
        lines += ["", "## Supporting assignments", "", "| Hill | Packet | Agent and return |", "|---|---|---|"]
        for hill,slot,a in support_rows:
            lines.append(f"| {hill} | {slot} | {a.get('lifecycle')} — {a.get('agent_ref')} / #{a.get('issue_number')} |")
    native = state.get("summary", {}).get("competition", {}).get("native_registration", {})
    if native.get("route_reconciliation"):
        lines += [
            "", "## Official submission route", "",
            f"**Blocker:** {native['blocking_boundary']}", "",
            native["next_action"], "",
            "**Submission cutoff:** 9 p.m. America/Vancouver on 2 October 2026 (04:00 UTC on 3 October).",
            "The ordinary Climb budget message does not establish a competition submission fee.",
        ]
    lines += [
        "",
        "## Current next action",
        "",
        f"**{state['next_action']['description']}**",
        "",
        "Research agenda: [seven-hill objectives and immediate priorities](OPENMATH_2026_RESEARCH_AGENDA.md).",
        "",
        f"**Immediate internal target:** {state['next_action'].get('research_direction', {}).get('internal_priority', 'Read the current research agenda and verify protected evidence before work.')}",
        "",
        f"**Parallel Cert lane:** {state['next_action'].get('research_direction', {}).get('parallel_cert_target', 'Certification remains separate from intake and replay.')}",
        "",
        "Participation uses ordinary authenticated GitHub issue-comment capability. Pseudonymous accounts are sufficient; no GCL organization membership, collaborator invitation, repository write access, or GCL-specific credentials are required. Zero-credential intake is postponed.",
        "",
        "Before substantive work, verify that the participant or an explicitly authorized relay in their environment can post one complete `GCL-RETURN-RELAY/1` envelope to the immutable task’s exact `INTENDED_RETURN` issue. Otherwise stop with `RETURN_TRANSPORT_UNAVAILABLE`. A private conversation alone is not a durable return route.",
        "",
        "Read the [participant entrypoint](https://github.com/grandchallenge/MATHSOLVE/blob/main/handoffs/OPENMATH-2026/CEX_AGENT_ENTRYPOINT.md) and verify the exact current protected lease before launch. A public task link does not allocate a second lease; the first-valid-result lock remains in force.",
        "",
        "The protected OPENMATH lifecycle controller carries valid returns through capture, replay, bounded adjudication, Programme reconciliation, and successor generation without manual evidence transport or controller wake-up. Receipt, acceptance, adjudication, and mathematical certification remain separate.",
        "",
        "See the [outside-participant trial procedure](OPENMATH_2026_PARTICIPANT_TRIAL.md). The trial is optional operational assurance when a genuine outside participant contributes; it is not a prerequisite for internal research or seven-hill participation.",
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
    is_support = projection.get("lane_role") == "SUPPORT"
    support_slot = projection.get("support_slot")
    if is_support and (hill != "OM26-H1" or not isinstance(support_slot,str) or not support_slot):
        raise ControllerError("supporting projection must bind a named H1 slot")
    agents = row.setdefault("supporting_agents", {}) if is_support else row
    agent_key = support_slot if is_support else "external_agent"
    old_agent=agents.get(agent_key,{})
    pred=projection["predecessor"]
    succ=projection["successor"]

    if not is_support:
        row["solve"]["state"]=f"{succ['assignment_id'].rsplit('-',1)[-1]}_LEASED_NOT_LAUNCHED"
        if hill != "OM26-H1":
            row["solve"]["frontier"]="AUTOMATED_REPLAY_CLOSURE_REQUIRED"
        row["solve"]["replay_closure"]="AUTOMATED_REPLAY_CLOSURE_REQUIRED"
    agents[agent_key]={
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
            "predecessor":old_agent.get("predecessor"),
        },
    }
    if not is_support:
        row["next_action"]=f"RECEIVE_VOLUNTARY_RETURN__{succ['assignment_id']}__IMMUTABLE_LINK_IN_RELAY_OUT"

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
    next_action = state.setdefault("next_action", {})
    defaults = {
        "id":"publish_and_receive_voluntary_contributions",
        "selection_rule":"Select each current hill lane whose exact active assignment lifecycle is LEASED_NOT_LAUNCHED.",
        "currently_selected":selected,
        "description":"Keep each registered immutable LINK_IN_RELAY_OUT task available for voluntary participants. GCL may launch its own workers optionally. Valid returns advance automatically through CAPTURED, REPLAYED, ADJUDICATED, and ADVANCED.",
        "completion_test":"Every returned result either reaches ADVANCED automatically or leaves a protected infrastructure blocker; no human evidence shuttling or controller prompt is permitted.",
    }
    for key, value in defaults.items():
        next_action.setdefault(key, value)
    next_action["currently_selected"] = selected
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
    if current is not None and current[0] == content:
        return
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
    receipt_path=f"governance/openmath_2026_lifecycle_reconciliations/{dispatch}.json"
    existing_receipt=optional_content(programme_gh,PROGRAMME,receipt_path,"main")
    if existing_receipt is not None:
        receipt=json.loads(existing_receipt[0])
        if receipt.get("dispatch_id")!=dispatch or receipt.get("result")!="ADVANCED":
            raise ControllerError(f"{dispatch}: protected Programme reconciliation receipt mismatch")
        ref=programme_gh.request("GET",f"/repos/{OWNER}/{PROGRAMME}/git/ref/heads/main")
        return {"already_reconciled":True,"merge_commit_sha":ref.get("object",{}).get("sha"),"number":None}

    branch=f"reconcile/openmath-{dispatch.lower()}"
    pr=find_pr(programme_gh,PROGRAMME,branch)
    if pr is not None:
        live=programme_gh.request("GET",f"/repos/{OWNER}/{PROGRAMME}/pulls/{pr['number']}")
        if live.get("mergeable") is not False:
            enable_auto_merge(programme_gh,pr)
            return {"pending":True,"number":pr["number"]}
    state=apply_projection_to_state(state,projection,solve_sha,blobs)
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
    merged=programme_gh.request("GET",f"/repos/{OWNER}/{PROGRAMME}/pulls/{pr['number']}")
    if not merged.get("merged_at"):
        return {"pending":True,"number":pr["number"]}
    return {"already_reconciled":False,"number":merged["number"],"merge_commit_sha":merged.get("merge_commit_sha")}


def verify_advanced(programme_gh: Github, projection: dict[str,Any]) -> None:
    dispatch=projection["source_dispatch"]
    receipt_path=f"governance/openmath_2026_lifecycle_reconciliations/{dispatch}.json"
    receipt_text,_=fetch_content(programme_gh,PROGRAMME,receipt_path,"main")
    receipt=json.loads(receipt_text)
    if (receipt.get("dispatch_id")!=dispatch
            or receipt.get("hill")!=projection["hill"]
            or receipt.get("result")!="ADVANCED"
            or receipt.get("pipeline")!=PIPELINE):
        raise ControllerError(f"{dispatch}: Programme protected completion receipt invalid")
    state_text,_=fetch_content(programme_gh,PROGRAMME,"governance/openmath_2026_campaign_state.json","main")
    state=json.loads(state_text)
    hill=next(x for x in state["hills"] if x["hill_slot"]==projection["hill"])
    agent=(hill.get("supporting_agents",{}).get(projection.get("support_slot"),{})
           if projection.get("lane_role")=="SUPPORT" else hill.get("external_agent",{}))
    current=agent.get("assignment_id")
    successor=projection["successor"]["assignment_id"]
    # The successor may itself later complete; a protected per-dispatch receipt
    # remains authoritative evidence that this transition reached ADVANCED.
    if current!=successor:
        ancestors=agent.get("predecessor",{})
        while ancestors.get("assignment_id")!=successor and isinstance(ancestors.get("predecessor"),dict):
            ancestors=ancestors["predecessor"]
        if ancestors.get("assignment_id")!=successor:
            raise ControllerError(f"{dispatch}: protected successor was lost")



def verify_locked_source_comment(
    receipt: dict[str, Any],
    raw_text: str,
    comment_body: str,
    dispatch: str,
) -> None:
    normalize=lambda value: value[:-1] if value.endswith("\n") else value
    transport=receipt.get("return_transport")
    if transport=="GCL-RETURN-RELAY/1":
        relay=receipt.get("relay_provenance")
        if not isinstance(relay,dict):
            raise ControllerError(f"{dispatch}: relay provenance missing from locked receipt")
        envelope=relay.get("envelope_utf8")
        if not isinstance(envelope,str):
            raise ControllerError(f"{dispatch}: locked relay envelope missing")
        if normalize(comment_body)!=normalize(envelope):
            raise ControllerError(f"{dispatch}: source relay envelope differs from locked receipt")
        prefix="GCL-RETURN-RELAY/1\n"
        begin="\nBEGIN_RESULT\n"
        end="\nEND_RESULT"
        if not envelope.startswith(prefix) or envelope.count(begin)!=1 or envelope.count(end)!=1:
            raise ControllerError(f"{dispatch}: locked relay envelope framing invalid")
        inner=envelope.split(begin,1)[1].rsplit(end,1)[0]
        if normalize(raw_text)!=normalize(inner):
            raise ControllerError(f"{dispatch}: protected raw differs from locked relay inner result")
        if relay.get("envelope_sha256")!=hashlib.sha256(envelope.encode("utf-8")).hexdigest():
            raise ControllerError(f"{dispatch}: locked relay envelope digest mismatch")
        if relay.get("inner_result_sha256")!=hashlib.sha256(inner.encode("utf-8")).hexdigest():
            raise ControllerError(f"{dispatch}: locked relay inner-result digest mismatch")
        return
    if normalize(comment_body)!=normalize(raw_text):
        raise ControllerError(f"{dispatch}: protected raw differs from source comment")


def legacy_source(gh: Github, branch: str) -> dict[str, Any] | None:
    """Read an already-locked legacy return without altering its original branch."""
    if not branch.startswith((BRANCH_PREFIX, RECOVERY_PREFIX)):
        return None
    dispatch, hill, wp = dispatch_parts(branch)
    base, _, _ = base_for(dispatch)
    raw_dir = urllib.parse.quote(f"{base}/raw/{dispatch}", safe="/")
    receipt_dir = urllib.parse.quote(f"{base}/receipts/{dispatch}", safe="/")
    raw_files = gh.get_optional(f"/repos/{OWNER}/{SOLVE}/contents/{raw_dir}?ref={urllib.parse.quote(branch)}")
    receipt_files = gh.get_optional(f"/repos/{OWNER}/{SOLVE}/contents/{receipt_dir}?ref={urllib.parse.quote(branch)}")
    if raw_files is None and receipt_files is None:
        return None
    if not isinstance(raw_files, list) or not isinstance(receipt_files, list):
        raise ControllerError(f"{dispatch}: legacy raw/receipt directories malformed")
    raw = [x["name"] for x in raw_files if isinstance(x,dict)
           and re.fullmatch(r"github-comment-[0-9]+[.]md", str(x.get("name","")))]
    receipts = [x["name"] for x in receipt_files if isinstance(x,dict)
                and re.fullmatch(r"github-comment-[0-9]+[.]json", str(x.get("name","")))]
    if len(raw) != 1 or len(receipts) != 1:
        raise ControllerError(f"{dispatch}: legacy first-result lock is ambiguous")
    cid = int(raw[0].removeprefix("github-comment-").removesuffix(".md"))
    if receipts[0] != f"github-comment-{cid}.json":
        raise ControllerError(f"{dispatch}: locked raw/receipt comment identities differ")
    raw_path = f"{base}/raw/{dispatch}/{raw[0]}"
    receipt_path = f"{base}/receipts/{dispatch}/{receipts[0]}"
    raw_text, raw_blob = fetch_content(gh, SOLVE, raw_path, branch)
    receipt_text, receipt_blob = fetch_content(gh, SOLVE, receipt_path, branch)
    receipt = json.loads(receipt_text)
    if any((
        receipt.get("dispatch_id") != dispatch,
        receipt.get("assignment_id") != dispatch.rsplit("-IA-",1)[0],
        receipt.get("github_comment_id") != cid,
        receipt.get("raw_artifact_path") != raw_path,
        receipt.get("schema_result") != "valid",
        receipt.get("canonical_claim_effect") is not False,
        receipt.get("handling_state") != "received_unadjudicated",
        receipt.get("result_protocol") != "GCL-CONTRIBUTION-RESULT/1",
    )):
        raise ControllerError(f"{dispatch}: legacy receipt identity/claim checks failed")
    comment = gh.request("GET",f"/repos/{OWNER}/{SOLVE}/issues/comments/{cid}")
    if not isinstance(comment,dict) or comment.get("id") != cid or not isinstance(comment.get("body"),str):
        raise ControllerError(f"{dispatch}: source GitHub comment unavailable")
    verify_locked_source_comment(receipt,raw_text,comment["body"],dispatch)
    if comment.get("issue_url","").rsplit("/",1)[-1] != str(receipt.get("github_issue_number")):
        raise ControllerError(f"{dispatch}: source issue identity mismatch")
    branch_ref = gh.request(
        "GET",f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(branch,safe='/')}"
    )
    source_commit=branch_ref.get("object",{}).get("sha")
    if not isinstance(source_commit,str) or not re.fullmatch(r"[0-9a-f]{40}",source_commit):
        raise ControllerError(f"{dispatch}: source branch identity missing")
    return {
        "dispatch_id":dispatch,"hill":hill,"wp":wp,"branch":branch,
        "raw_text":raw_text,"receipt_text":receipt_text,"receipt":receipt,
        "raw_path":raw_path,"receipt_path":receipt_path,
        "raw_blob":raw_blob,"receipt_blob":receipt_blob,
        "source_commit":source_commit,"comment_id":cid,
    }


def _solve_generator(checkout: Path) -> Any:
    script=checkout / "ci/openmath_lifecycle_candidate.py"
    if not script.is_file():
        raise ControllerError("pinned Solve lifecycle generator checkout unavailable")
    spec=importlib.util.spec_from_file_location("openmath_solve_candidate_recovery",script)
    if spec is None or spec.loader is None:
        raise ControllerError("unable to load protected Solve candidate generator")
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _refresh_solve_checkout(checkout: Path) -> None:
    for cmd in (
        ["git","-C",str(checkout),"fetch","--depth=1","origin","main"],
        ["git","-C",str(checkout),"reset","--hard","FETCH_HEAD"],
    ):
        proc=subprocess.run(cmd,text=True,capture_output=True,timeout=120,check=False)
        if proc.returncode:
            raise ControllerError(f"unable to refresh protected Solve checkout: {proc.stderr[-500:]}")


def _existing_successor_issue(gh: Github, title: str) -> dict[str, Any] | None:
    query=urllib.parse.quote(f'repo:{OWNER}/{SOLVE} in:title "{title.split()[2]}"')
    result=gh.request("GET",f"/search/issues?q={query}&per_page=100")
    matches=[x for x in result.get("items",[]) if x.get("title")==title and "pull_request" not in x]
    if len(matches)>1:
        raise ControllerError("multiple successor issues share exact identity")
    return matches[0] if matches else None


def synchronize_successor_issue(
    gh: Github,
    issue: dict[str, Any],
    expected_body: str,
    dispatch: str,
) -> dict[str, Any]:
    number=issue.get("number")
    if not isinstance(number,int):
        raise ControllerError(f"{dispatch}: existing successor issue lacks numeric identity")
    current_body=issue.get("body")
    if current_body==expected_body and issue.get("state")=="open":
        return issue
    comments=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/issues/{number}/comments?per_page=100")
    if not isinstance(comments,list):
        raise ControllerError(f"{dispatch}: successor issue comments response malformed")
    if comments:
        raise ControllerError(
            f"{dispatch}: successor issue contract drift after participation; refuse to rewrite return surface"
        )
    payload={"body":expected_body}
    if issue.get("state")!="open":
        payload["state"]="open"
    updated=gh.request("PATCH",f"/repos/{OWNER}/{SOLVE}/issues/{number}",payload)
    if not isinstance(updated,dict) or updated.get("body")!=expected_body or updated.get("state")!="open":
        raise ControllerError(f"{dispatch}: successor issue contract synchronization failed")
    return updated


def recover_legacy(gh: Github, branch: str, checkout: Path, refresh: bool = False) -> dict[str, Any]:
    """Promote locked old-format evidence into a new, protected lifecycle candidate."""
    src=legacy_source(gh,branch)
    if src is None:
        raise ControllerError(f"{branch}: no recoverable locked legacy result")
    dispatch=src["dispatch_id"]
    recovery_branch=f"{RECOVERY_PREFIX}{dispatch.lower()}"
    if protected_raw_exists(gh,dispatch):
        raise ControllerError(f"{dispatch}: raw already protected but no lifecycle manifest; manual integrity inspection required")

    _refresh_solve_checkout(checkout)
    generator=_solve_generator(checkout)
    with tempfile.TemporaryDirectory(prefix="om26-recovery-") as temp:
        root=Path(temp)
        candidate_root=root/"solve"
        shutil.copytree(checkout,candidate_root,ignore=shutil.ignore_patterns(".git"))
        intake_dir=root/"intake"
        intake_dir.mkdir()
        (intake_dir/"RAW.md").write_text(src["raw_text"],encoding="utf-8")
        (intake_dir/"RECEIPT.json").write_text(src["receipt_text"],encoding="utf-8")
        meta={
            "dispatch_id":dispatch,"comment_id":src["comment_id"],
            "raw_repo_path":src["raw_path"],"receipt_repo_path":src["receipt_path"],
        }
        (intake_dir/"META.json").write_text(json.dumps(meta,indent=2)+"\n",encoding="utf-8")

        registry=json.loads(
            (candidate_root/".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json").read_text(encoding="utf-8")
        )
        item=next((x for x in registry["assignments"] if x.get("assignment_id")==src["receipt"]["assignment_id"]),None)
        if item is None or item.get("state") not in ("LEASED_NOT_LAUNCHED","LAUNCHED","RETURNED","CAPTURED"):
            raise ControllerError(f"{dispatch}: legacy assignment no longer open")
        lease=item.get("lease",{})
        if lease.get("dispatch_id")!=dispatch or lease.get("agent_ref")!=src["receipt"]["agent_ref"]:
            raise ControllerError(f"{dispatch}: legacy return disagrees with live protected lease")
        p=generator.plan(intake_dir)
        title=p["issue_title"]
        issue=_existing_successor_issue(gh,title)
        if issue is None:
            issue=gh.request("POST",f"/repos/{OWNER}/{SOLVE}/issues",{
                "title":title,"body":p["issue_body"]
            })
        else:
            issue=synchronize_successor_issue(gh,issue,p["issue_body"],dispatch)
        issue_number=issue.get("number")
        issue_url=issue.get("html_url")
        if not isinstance(issue_number,int) or not isinstance(issue_url,str):
            raise ControllerError(f"{dispatch}: successor issue creation failed")
        manifest=generator.apply_candidate(candidate_root,intake_dir,issue_number,issue_url)

        if not refresh:
            provenance_path=f"contributions/OPENMATH-2026/{src['hill']}/{src['wp']}/lifecycle/{dispatch}/LEGACY_SOURCE.json"
            provenance={
                "schema_version":"1.0.0",
                "record_type":"OPENMATH_LEGACY_INTAKE_RECOVERY",
                "dispatch_id":dispatch,
                "source_branch":branch,
                "source_commit":src["source_commit"],
                "raw_path":src["raw_path"],
                "raw_git_blob_sha1":src["raw_blob"],
                "receipt_path":src["receipt_path"],
                "receipt_git_blob_sha1":src["receipt_blob"],
                "comment_id":src["comment_id"],
                "successor_issue_number":issue_number,
                "claim_effect":"NONE",
            }
            provenance_file=candidate_root/provenance_path
            provenance_file.parent.mkdir(parents=True,exist_ok=True)
            provenance_file.write_text(json.dumps(provenance,indent=2)+"\n",encoding="utf-8")
            manifest_path=f"contributions/OPENMATH-2026/{src['hill']}/{src['wp']}/lifecycle/{dispatch}/MANIFEST.json"
            manifest["changed_paths"]=sorted(set(manifest["changed_paths"]+[provenance_path]))
            manifest["legacy_provenance_path"]=provenance_path
            (candidate_root/manifest_path).write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")
        branch_ref=gh.get_optional(
            f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(recovery_branch,safe='/')}"
        )
        if branch_ref is None:
            main_ref=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/git/ref/heads/main")
            sha=main_ref.get("object",{}).get("sha")
            if not isinstance(sha,str):
                raise ControllerError("live Solve main ref unavailable")
            gh.request("POST",f"/repos/{OWNER}/{SOLVE}/git/refs",{
                "ref":f"refs/heads/{recovery_branch}","sha":sha
            })
        launch_path=f"handoffs/OPENMATH-2026/launch/{p['successor_assignment']}.md"
        successor_registry=json.loads((candidate_root/".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json").read_text(encoding="utf-8"))
        successor=next(x for x in successor_registry["assignments"] if x.get("assignment_id")==p["successor_assignment"])
        for task_path in (successor["work_package"], launch_path):
            put_file(
                gh,SOLVE,recovery_branch,task_path,
                (candidate_root/task_path).read_text(encoding="utf-8"),
                f"OPENMATH: publish immutable successor task for {dispatch}",
            )
        pin_ref=gh.request(
            "GET",f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(recovery_branch,safe='/')}"
        )
        content_commit=pin_ref.get("object",{}).get("sha")
        if not isinstance(content_commit,str) or not re.fullmatch(r"[0-9a-f]{40}",content_commit):
            raise ControllerError(f"{dispatch}: immutable successor commit not available")
        generator.finalize_pin(candidate_root,dispatch,content_commit)

        for path in manifest["changed_paths"]:
            if path==launch_path:
                continue
            file=candidate_root/path
            if not file.is_file():
                raise ControllerError(f"{dispatch}: missing generated candidate artifact {path}")
            put_file(
                gh,SOLVE,recovery_branch,path,file.read_text(encoding="utf-8"),
                f"OPENMATH lifecycle: {dispatch} {file.name}",
            )
    result=validate_candidate(gh,recovery_branch)
    result["source_branch"]=branch
    result["source_commit"]=src["source_commit"]
    return result



def _local_programme_reconciled(programme_root: Path | None, dispatch: str) -> bool:
    if programme_root is None:
        return False
    path=programme_root/"governance/openmath_2026_lifecycle_reconciliations"/f"{dispatch}.json"
    if not path.is_file():
        return False
    try:
        receipt=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ControllerError(f"{dispatch}: local Programme reconciliation receipt is invalid JSON") from exc
    if (receipt.get("dispatch_id")!=dispatch
            or receipt.get("result")!="ADVANCED"
            or receipt.get("pipeline")!=PIPELINE):
        raise ControllerError(f"{dispatch}: local Programme reconciliation receipt is invalid")
    return True


def candidate_sources(
    gh: Github,
    solve_checkout: Path | None = None,
    programme_root: Path | None = None,
) -> list[tuple[str, str | None]]:
    """Return only lifecycle transitions that still require protected work.

    Prefer the already-checked-out protected Solve state over REST for registry
    and manifest inspection. This keeps the Release Trust installation budget
    proportional to live work instead of historical campaign size.
    """
    registry_path=(solve_checkout/".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json"
                   if solve_checkout is not None else None)
    if registry_path is not None and registry_path.is_file():
        registry=json.loads(registry_path.read_text(encoding="utf-8"))
        local_solve=True
    else:
        text,_=fetch_content(gh,SOLVE,".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json","main")
        registry=json.loads(text)
        local_solve=False

    protected_by_dispatch: dict[str, tuple[str, str | None]]={}
    protected_manifest_dispatches: set[str]=set()
    for assignment in registry.get("assignments",[]):
        if assignment.get("lifecycle",{}).get("pipeline_state") != "ADVANCED":
            continue
        dispatch=assignment.get("lease",{}).get("dispatch_id")
        if not isinstance(dispatch,str) or DISPATCH_RE.fullmatch(dispatch) is None:
            raise ControllerError("protected ADVANCED assignment has invalid dispatch identity")
        base,_,_=base_for(dispatch)
        manifest_path=f"{base}/lifecycle/{dispatch}/MANIFEST.json"
        if local_solve:
            manifest_exists=(solve_checkout/manifest_path).is_file()
        else:
            manifest_exists=optional_content(gh,SOLVE,manifest_path,"main") is not None
        if not manifest_exists:
            continue
        protected_manifest_dispatches.add(dispatch)
        if not _local_programme_reconciled(programme_root,dispatch):
            protected_by_dispatch[dispatch]=(f"{BRANCH_PREFIX}{dispatch.lower()}","main")

    live=[]
    for branch in branch_names(gh):
        dispatch,_,_=dispatch_parts(branch)
        if dispatch in protected_by_dispatch:
            continue
        if dispatch in protected_manifest_dispatches and _local_programme_reconciled(programme_root,dispatch):
            continue
        live.append((branch,None))
    return sorted(protected_by_dispatch.values())+sorted(live)


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
    recovered: set[str] = set()
    solve_checkout=Path(os.environ.get("MATHSOLVE_CHECKOUT_DIR",""))
    programme_root=Path(__file__).resolve().parents[1]
    if solve_checkout.is_dir():
        _refresh_solve_checkout(solve_checkout)
    for branch,source_ref in candidate_sources(solve_gh,solve_checkout,programme_root):
        try:
            dispatch, hill, wp = dispatch_parts(branch)
            if dispatch in recovered:
                continue
            try:
                item=validate_candidate(solve_gh,branch,source_ref)
            except ControllerError as exc:
                if "lifecycle MANIFEST missing" not in str(exc) or not branch.startswith(BRANCH_PREFIX):
                    raise
                if protected_raw_exists(solve_gh,dispatch):
                    report["processed"].append({
                        "dispatch_id":dispatch,"hill":hill,"wp":wp,
                        "branch":branch,"state":"LEGACY_ALREADY_PROTECTED",
                    })
                    continue
                if not apply:
                    report["processed"].append({
                        "dispatch_id":dispatch,"hill":hill,"wp":wp,
                        "branch":branch,"state":"LEGACY_RECOVERY_REQUIRED",
                    })
                    continue
                if not solve_checkout.is_dir():
                    raise ControllerError("protected Solve checkout unavailable for legacy recovery")
                item=recover_legacy(solve_gh,branch,solve_checkout)
                recovered.add(dispatch)
            if not apply:
                report["processed"].append({**item,"state":"VALIDATED_DRY_RUN"})
                continue
            solve_merge=ensure_solve_merge(solve_gh,item,solve_checkout)
            if solve_merge.get("pending"):
                report["processed"].append({**item,"state":"AWAITING_PROTECTED_SOLVE_MERGE","solve_merge":solve_merge})
                return report
            solve_sha=solve_merge.get("merge_commit_sha")
            if not isinstance(solve_sha,str):
                ref=solve_gh.request("GET",f"/repos/{OWNER}/{SOLVE}/git/ref/heads/main")
                solve_sha=ref.get("object",{}).get("sha")
            projection,blobs=live_solve_projection(solve_gh,item)
            programme_merge=ensure_programme_reconciliation(programme_gh,projection,solve_sha,blobs)
            if programme_merge.get("pending"):
                report["processed"].append({**item,"state":"AWAITING_PROTECTED_PROGRAMME_MERGE","solve_merge":solve_merge,"programme_merge":programme_merge})
                return report
            verify_advanced(programme_gh,projection)
            recovered.add(dispatch)
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
