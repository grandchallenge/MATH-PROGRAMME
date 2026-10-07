#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Any

try:
    from ci.ns_ci_intake_pr_controller import ControllerError, Github
except ModuleNotFoundError:
    from ns_ci_intake_pr_controller import ControllerError, Github

OWNER = "grandchallenge"
SOLVE = "MATHSOLVE"
PROBLEMS = ("593","595","241","470","1052","99","101","138")
BRANCH_RE = re.compile(r"^lifecycle/erdos-(593|595|241|470|1052|99|101|138)-cohort-closure-001$")
CLERK = "gcl-council-clerk[bot]"
ADVANCEMENT_VALIDATORS = {
    "241": "ci/validate_erdos_241_synthesis.py",
}

def closure_path(problem: str) -> str:
    return f"contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/closures/ERDOS-{problem}-BLIND-COHORT-001.json"

def branch_name(problem: str) -> str:
    return f"lifecycle/erdos-{problem}-cohort-closure-001"

def _content(gh: Github, path: str, ref: str) -> tuple[str,str] | None:
    q=urllib.parse.urlencode({"ref":ref})
    item=gh.get_optional(f"/repos/{OWNER}/{SOLVE}/contents/{path}?{q}")
    if item is None:
        return None
    if not isinstance(item,dict) or item.get("encoding")!="base64":
        raise ControllerError(f"{path}: malformed content response")
    return base64.b64decode(item["content"]).decode("utf-8"), str(item.get("sha",""))

def _main_sha(gh: Github) -> str:
    ref=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/git/ref/heads/main")
    sha=ref.get("object",{}).get("sha") if isinstance(ref,dict) else None
    if not isinstance(sha,str) or not re.fullmatch(r"[0-9a-f]{40}",sha):
        raise ControllerError("MATHSOLVE main SHA unavailable")
    return sha

def _local_sha(root: Path) -> str:
    p=subprocess.run(["git","-C",str(root),"rev-parse","HEAD"],text=True,capture_output=True,check=False)
    if p.returncode:
        raise ControllerError("unable to read protected MATHSOLVE checkout SHA")
    return p.stdout.strip()

def _load_closure_module(root: Path):
    sys.path.insert(0,str(root))
    from ci import erdos_open_cohort_closure as mod  # type: ignore
    return mod

def _find_pr(gh: Github, branch: str, state: str="open") -> dict[str,Any] | None:
    head=urllib.parse.quote(f"{OWNER}:{branch}",safe="")
    out=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/pulls?state={state}&head={head}&base=main")
    if not isinstance(out,list):
        raise ControllerError("closure PR list response malformed")
    return out[0] if out else None

def _create_branch(gh: Github, branch: str, sha: str) -> None:
    existing=gh.get_optional(f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(branch,safe='/')}")
    if existing is None:
        gh.request("POST",f"/repos/{OWNER}/{SOLVE}/git/refs",{"ref":f"refs/heads/{branch}","sha":sha})

def _put_closure(gh: Github, branch: str, problem: str, closure: dict[str,Any]) -> None:
    path=closure_path(problem)
    existing=_content(gh,path,branch)
    payload={
        "message":f"Close ERDOS-{problem} blind cohort for synthesis",
        "content":base64.b64encode((json.dumps(closure,indent=2,sort_keys=True)+"\n").encode()).decode(),
        "branch":branch,
    }
    if existing is not None:
        payload["sha"]=existing[1]
    gh.request("PUT",f"/repos/{OWNER}/{SOLVE}/contents/{path}",payload)

def _compare_files(gh: Github, branch: str) -> list[str]:
    encoded=urllib.parse.quote(f"main...{branch}",safe=".")
    data=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/compare/{encoded}")
    if not isinstance(data,dict):
        raise ControllerError("closure branch compare malformed")
    return sorted(str(x.get("filename")) for x in data.get("files",[]) if isinstance(x,dict))

def validate_candidate(gh: Github, solve_root: Path, branch: str) -> dict[str,Any]:
    m=BRANCH_RE.fullmatch(branch)
    if not m:
        raise ControllerError(f"unregistered ERDOS closure branch: {branch}")
    problem=m.group(1)
    path=closure_path(problem)
    if _compare_files(gh,branch)!=[path]:
        raise ControllerError(f"ERDOS-{problem}: closure candidate diff is not exactly {path}")
    got=_content(gh,path,branch)
    if got is None:
        raise ControllerError(f"ERDOS-{problem}: closure candidate missing")
    closure=json.loads(got[0])
    mod=_load_closure_module(solve_root)
    errors=mod.validate_closure(problem,closure)
    if errors:
        raise ControllerError(f"ERDOS-{problem}: invalid closure candidate: {'; '.join(errors)}")
    if _content(gh,path,"main") is not None:
        raise ControllerError(f"ERDOS-{problem}: closure already protected on main")
    ref=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(branch,safe='/')}")
    head=ref.get("object",{}).get("sha") if isinstance(ref,dict) else None
    if not isinstance(head,str):
        raise ControllerError("closure branch head unavailable")
    return {"problem":problem,"branch":branch,"path":path,"head_sha":head,"closure":closure}

def _approval_exists(gh: Github, pr_number: int, head_sha: str) -> bool:
    reviews=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/pulls/{pr_number}/reviews?per_page=100")
    if not isinstance(reviews,list):
        raise ControllerError("closure review list malformed")
    for review in reviews:
        if not isinstance(review,dict):
            continue
        user=review.get("user")
        login=user.get("login") if isinstance(user,dict) else None
        if login==CLERK and review.get("state")=="APPROVED" and review.get("commit_id")==head_sha:
            return True
    return False

def _merge(gh: Github, pr_number: int, head_sha: str, problem: str) -> dict[str,Any]:
    out=gh.request("PUT",f"/repos/{OWNER}/{SOLVE}/pulls/{pr_number}/merge",{
        "sha":head_sha,
        "merge_method":"squash",
        "commit_title":f"Close ERDOS-{problem} blind cohort for synthesis (#{pr_number})",
        "commit_message":"Mechanical blind-cohort closure from protected R1+A1 evidence. No mathematical adjudication, literature promotion, certification, or parent-problem effect.",
    })
    if not isinstance(out,dict) or out.get("merged") is not True:
        raise ControllerError(f"ERDOS-{problem}: protected closure merge did not complete: {out!r}")
    return out

def _advanced_state(solve_root: Path, problem: str) -> dict[str,Any]:
    validator=ADVANCEMENT_VALIDATORS.get(problem)
    if validator is None:
        return {"state":"SYNTHESIS_READY_NEEDS_REGISTERED_PLUGIN"}
    path=solve_root/validator
    if not path.is_file():
        return {"state":"REGISTERED_PLUGIN_MISSING","validator":validator}
    p=subprocess.run([sys.executable,str(path)],cwd=solve_root,text=True,capture_output=True,check=False,timeout=300)
    if p.returncode==0:
        return {"state":"ADVANCED","validator":validator,"validator_output":p.stdout.strip()[-1000:]}
    return {"state":"REGISTERED_PLUGIN_NOT_SATISFIED","validator":validator,"validator_output":(p.stdout+p.stderr).strip()[-2000:]}

def run(solve_root: Path, apply: bool) -> dict[str,Any]:
    token=os.environ.get("MATHSOLVE_ERDOS_LIFECYCLE_TOKEN","")
    if not token:
        raise ControllerError("MATHSOLVE_ERDOS_LIFECYCLE_TOKEN is empty")
    gh=Github(token)
    main_sha=_main_sha(gh)
    local_sha=_local_sha(solve_root)
    if local_sha!=main_sha:
        raise ControllerError(f"protected MATHSOLVE checkout drift: local={local_sha} main={main_sha}")
    mod=_load_closure_module(solve_root)
    report={
        "schema_version":"1.0.0",
        "controller":"GCL_ERDOS_OPEN_POSTPROTECT_LIFECYCLE",
        "apply":apply,
        "protected_main_sha":main_sha,
        "states":[],
        "errors":[],
        "authority_created":False,
    }
    for problem in PROBLEMS:
        path=closure_path(problem)
        try:
            protected=_content(gh,path,"main")
            if protected is not None:
                closure=json.loads(protected[0])
                errors=mod.validate_closure(problem,closure)
                if errors:
                    raise ControllerError(f"protected closure invalid: {'; '.join(errors)}")
                report["states"].append({"problem":problem,"state":"BLIND_COHORT_CLOSED",**_advanced_state(solve_root,problem)})
                continue
            try:
                closure=mod.build_closure(problem,main_sha,"2026-10-06")
            except ValueError as exc:
                if "R1+A1 protected minimum not satisfied" in str(exc):
                    report["states"].append({"problem":problem,"state":"WAITING_FOR_PROTECTED_R1_A1"})
                    continue
                raise
            branch=branch_name(problem)
            if apply:
                _create_branch(gh,branch,main_sha)
                _put_closure(gh,branch,problem,closure)
            candidate=validate_candidate(gh,solve_root,branch) if apply else {
                "problem":problem,"branch":branch,"path":path,"closure":closure
            }
            pr=_find_pr(gh,branch)
            if pr is None and apply:
                pr=gh.request("POST",f"/repos/{OWNER}/{SOLVE}/pulls",{
                    "title":f"Close ERDOS-{problem} blind cohort for synthesis",
                    "head":branch,"base":"main",
                    "body":"Mechanical R1+A1 blind-cohort closure generated from protected schema-valid evidence. This opens synthesis only. It does not adjudicate mathematics, establish literature status, certify a claim, or affect the parent Erdős problem.",
                })
            if not isinstance(pr,dict):
                report["states"].append({**candidate,"state":"CLOSURE_CANDIDATE_READY"})
                continue
            live=gh.request("GET",f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}")
            head=live.get("head",{}).get("sha") if isinstance(live,dict) else None
            if head!=candidate.get("head_sha"):
                raise ControllerError(f"ERDOS-{problem}: closure PR head drift")
            if not _approval_exists(gh,int(pr["number"]),str(head)):
                report["states"].append({**candidate,"pr_number":pr["number"],"state":"AWAITING_COUNCIL_CLERK_DOCUMENTARY_REVIEW"})
                continue
            if apply:
                merged=_merge(gh,int(pr["number"]),str(head),problem)
                report["states"].append({**candidate,"pr_number":pr["number"],"state":"PROTECTED_CLOSURE_MERGED","merge_commit_sha":merged.get("sha")})
            else:
                report["states"].append({**candidate,"pr_number":pr["number"],"state":"READY_FOR_PROTECTED_CLOSURE_MERGE"})
        except Exception as exc:
            report["errors"].append({"problem":problem,"error":str(exc)})
    try:
        report["states"].append(_run_canary(gh, solve_root, main_sha, apply))
    except Exception as exc:
        report["errors"].append({"problem":"GCL-E2E-CANARY-001","error":str(exc)})
    try:
        report["states"].append(_run_canary2(gh, solve_root, main_sha, apply))
    except Exception as exc:
        report["errors"].append({"problem":"GCL-E2E-CANARY-002","error":str(exc)})
    return report


CANARY_CLOSURE_BRANCH = "lifecycle/gcl-e2e-canary-001-cohort-closure"
CANARY_ADVANCE_BRANCH = "lifecycle/gcl-e2e-canary-001-advance"
CANARY_CLOSURE_PATH = "contributions/GCL-E2E-CANARY-001/closure.json"
CANARY_REPLAY_PATH = "contributions/GCL-E2E-CANARY-001/replay.json"
CANARY_ADJUDICATION_PATH = "contributions/GCL-E2E-CANARY-001/adjudication.json"
CANARY_SUCCESSOR_PATH = "work_packages/GCL_E2E_CANARY/GCL_E2E_CANARY_002.md"

def _load_canary_module(root: Path):
    sys.path.insert(0, str(root))
    from ci import gcl_e2e_canary as mod  # type: ignore
    return mod

def _put_text(gh: Github, branch: str, path: str, text: str, message: str) -> None:
    existing = _content(gh, path, branch)
    payload = {
        "message": message,
        "content": base64.b64encode(text.encode("utf-8")).decode(),
        "branch": branch,
    }
    if existing is not None:
        payload["sha"] = existing[1]
    gh.request("PUT", f"/repos/{OWNER}/{SOLVE}/contents/{path}", payload)

def validate_canary_candidate(gh: Github, solve_root: Path, branch: str) -> dict[str,Any]:
    mod = _load_canary_module(solve_root)
    if branch == CANARY_CLOSURE_BRANCH:
        changed = _compare_files(gh, branch)
        if changed != [CANARY_CLOSURE_PATH]:
            raise ControllerError(f"canary closure candidate diff mismatch: {changed}")
        got = _content(gh, CANARY_CLOSURE_PATH, branch)
        if got is None:
            raise ControllerError("canary closure candidate missing")
        closure = json.loads(got[0])
        errors = mod.validate_closure(closure)
        if errors:
            raise ControllerError("canary closure invalid: " + "; ".join(errors))
        if _content(gh, CANARY_CLOSURE_PATH, "main") is not None:
            raise ControllerError("canary closure already protected")
        ref = gh.request("GET", f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(branch,safe='/')}")
        head = ref.get("object",{}).get("sha") if isinstance(ref,dict) else None
        if not isinstance(head,str):
            raise ControllerError("canary closure head unavailable")
        return {"kind":"CANARY_CLOSURE","branch":branch,"head_sha":head,"path":CANARY_CLOSURE_PATH}
    if branch == CANARY_ADVANCE_BRANCH:
        expected = sorted([CANARY_REPLAY_PATH, CANARY_ADJUDICATION_PATH, CANARY_SUCCESSOR_PATH])
        changed = _compare_files(gh, branch)
        if changed != expected:
            raise ControllerError(f"canary advancement candidate diff mismatch: {changed}")
        replay_item = _content(gh, CANARY_REPLAY_PATH, branch)
        adj_item = _content(gh, CANARY_ADJUDICATION_PATH, branch)
        successor_item = _content(gh, CANARY_SUCCESSOR_PATH, branch)
        if replay_item is None or adj_item is None or successor_item is None:
            raise ControllerError("canary advancement candidate incomplete")
        replay = json.loads(replay_item[0])
        adj = json.loads(adj_item[0])
        errors = mod.validate_bundle(replay, adj, successor_item[0])
        if errors:
            raise ControllerError("canary advancement invalid: " + "; ".join(errors))
        if any(_content(gh, path, "main") is not None for path in expected):
            raise ControllerError("canary advancement already partly protected")
        ref = gh.request("GET", f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(branch,safe='/')}")
        head = ref.get("object",{}).get("sha") if isinstance(ref,dict) else None
        if not isinstance(head,str):
            raise ControllerError("canary advancement head unavailable")
        return {"kind":"CANARY_ADVANCE","branch":branch,"head_sha":head,"paths":expected}
    raise ControllerError(f"unregistered canary lifecycle branch: {branch}")

def _run_canary(gh: Github, solve_root: Path, main_sha: str, apply: bool) -> dict[str,Any]:
    mod = _load_canary_module(solve_root)
    protected_closure = _content(gh, CANARY_CLOSURE_PATH, "main")
    if protected_closure is None:
        try:
            closure = mod.build_closure(main_sha, "2026-10-06")
        except ValueError as exc:
            if "protected RESULT/1 absent" in str(exc):
                return {"canary":"GCL-E2E-CANARY-001","state":"WAITING_FOR_PROTECTED_RESULT"}
            raise
        pr = _find_pr(gh, CANARY_CLOSURE_BRANCH)
        if apply and pr is None:
            _create_branch(gh, CANARY_CLOSURE_BRANCH, main_sha)
            _put_text(gh, CANARY_CLOSURE_BRANCH, CANARY_CLOSURE_PATH, json.dumps(closure,indent=2,sort_keys=True)+"\n", "Close GCL E2E canary cohort for deterministic replay")
        candidate = validate_canary_candidate(gh, solve_root, CANARY_CLOSURE_BRANCH) if apply else {"kind":"CANARY_CLOSURE","branch":CANARY_CLOSURE_BRANCH}
        if pr is None and apply:
            pr = gh.request("POST", f"/repos/{OWNER}/{SOLVE}/pulls", {
                "title":"Close GCL E2E canary cohort for deterministic replay",
                "head":CANARY_CLOSURE_BRANCH, "base":"main",
                "body":"Mechanical one-member production canary cohort closure from protected RESULT/1 evidence. No mathematical, certification, publication, or external claim authority."
            })
        if not isinstance(pr,dict):
            return {**candidate,"state":"CLOSURE_CANDIDATE_READY"}
        live = gh.request("GET", f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}")
        head = live.get("head",{}).get("sha") if isinstance(live,dict) else None
        if head != candidate.get("head_sha"):
            raise ControllerError("canary closure PR head drift")
        if not _approval_exists(gh, int(pr["number"]), str(head)):
            return {**candidate,"pr_number":pr["number"],"state":"AWAITING_COUNCIL_CLERK_DOCUMENTARY_REVIEW"}
        if apply:
            out = gh.request("PUT", f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}/merge", {
                "sha":head,"merge_method":"squash",
                "commit_title":f"Close GCL E2E canary cohort (#{pr['number']})",
                "commit_message":"Mechanical canary cohort closure only. No mathematical or certification authority."
            })
            if not isinstance(out,dict) or out.get("merged") is not True:
                raise ControllerError(f"canary closure protected merge failed: {out!r}")
            return {**candidate,"pr_number":pr["number"],"state":"PROTECTED_CLOSURE_MERGED","merge_commit_sha":out.get("sha")}
        return {**candidate,"pr_number":pr["number"],"state":"READY_FOR_PROTECTED_CLOSURE_MERGE"}

    closure = json.loads(protected_closure[0])
    errors = mod.validate_closure(closure)
    if errors:
        raise ControllerError("protected canary closure invalid: " + "; ".join(errors))
    replay_main = _content(gh, CANARY_REPLAY_PATH, "main")
    adj_main = _content(gh, CANARY_ADJUDICATION_PATH, "main")
    successor_main = _content(gh, CANARY_SUCCESSOR_PATH, "main")
    if replay_main is not None and adj_main is not None and successor_main is not None:
        replay = json.loads(replay_main[0])
        adj = json.loads(adj_main[0])
        errors = mod.validate_bundle(replay, adj, successor_main[0])
        if errors:
            raise ControllerError("protected canary advancement invalid: " + "; ".join(errors))
        return {"canary":"GCL-E2E-CANARY-001","state":"ADVANCED","replay_pass":replay.get("replay_pass"),"adjudication":adj.get("disposition"),"successor":adj.get("selected_successor")}
    if any(x is not None for x in (replay_main, adj_main, successor_main)):
        raise ControllerError("partial protected canary advancement bundle")

    replay = mod.build_replay()
    adj = mod.build_adjudication(replay)
    successor = mod.successor_text()
    if replay.get("replay_pass") is not True or adj.get("disposition") != "ADVANCE":
        return {"canary":"GCL-E2E-CANARY-001","state":"DETERMINISTIC_REPLAY_REJECTED","replay":replay}
    pr = _find_pr(gh, CANARY_ADVANCE_BRANCH)
    if apply and pr is None:
        _create_branch(gh, CANARY_ADVANCE_BRANCH, main_sha)
        _put_text(gh, CANARY_ADVANCE_BRANCH, CANARY_REPLAY_PATH, json.dumps(replay,indent=2,sort_keys=True)+"\n", "Record GCL E2E canary deterministic replay")
        _put_text(gh, CANARY_ADVANCE_BRANCH, CANARY_ADJUDICATION_PATH, json.dumps(adj,indent=2,sort_keys=True)+"\n", "Record GCL E2E canary deterministic adjudication")
        _put_text(gh, CANARY_ADVANCE_BRANCH, CANARY_SUCCESSOR_PATH, successor, "Materialize precommitted GCL E2E canary successor")
    candidate = validate_canary_candidate(gh, solve_root, CANARY_ADVANCE_BRANCH) if apply else {"kind":"CANARY_ADVANCE","branch":CANARY_ADVANCE_BRANCH}
    if pr is None and apply:
        pr = gh.request("POST", f"/repos/{OWNER}/{SOLVE}/pulls", {
            "title":"Advance GCL E2E canary after deterministic replay",
            "head":CANARY_ADVANCE_BRANCH,"base":"main",
            "body":"Deterministically generated replay, bounded adjudication, and the precommitted successor for the production E2E canary. No mathematical, certification, publication, or external claim authority."
        })
    if not isinstance(pr,dict):
        return {**candidate,"state":"ADVANCEMENT_CANDIDATE_READY"}
    live = gh.request("GET", f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}")
    head = live.get("head",{}).get("sha") if isinstance(live,dict) else None
    if head != candidate.get("head_sha"):
        raise ControllerError("canary advancement PR head drift")
    if not _approval_exists(gh, int(pr["number"]), str(head)):
        return {**candidate,"pr_number":pr["number"],"state":"AWAITING_COUNCIL_CLERK_DOCUMENTARY_REVIEW"}
    if apply:
        out = gh.request("PUT", f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}/merge", {
            "sha":head,"merge_method":"squash",
            "commit_title":f"Advance GCL E2E canary after deterministic replay (#{pr['number']})",
            "commit_message":"Deterministic canary replay/adjudication and precommitted successor only. No external authority."
        })
        if not isinstance(out,dict) or out.get("merged") is not True:
            raise ControllerError(f"canary advancement protected merge failed: {out!r}")
        return {**candidate,"pr_number":pr["number"],"state":"PROTECTED_ADVANCEMENT_MERGED","merge_commit_sha":out.get("sha")}
    return {**candidate,"pr_number":pr["number"],"state":"READY_FOR_PROTECTED_ADVANCEMENT_MERGE"}


CANARY2_CLOSURE_BRANCH = "lifecycle/gcl-e2e-canary-002-cohort-closure"
CANARY2_ADVANCE_BRANCH = "lifecycle/gcl-e2e-canary-002-advance"
CANARY2_CLOSURE_PATH = "contributions/GCL-E2E-CANARY-002/closure.json"
CANARY2_REPLAY_PATH = "contributions/GCL-E2E-CANARY-002/replay.json"
CANARY2_ADJUDICATION_PATH = "contributions/GCL-E2E-CANARY-002/adjudication.json"
CANARY2_SUCCESSOR_PATH = "work_packages/GCL_E2E_CANARY/GCL_E2E_CANARY_003.md"

def _load_canary2_module(root: Path):
    sys.path.insert(0, str(root))
    from ci import gcl_e2e_canary_002 as mod  # type: ignore
    return mod

def _put_text2(gh: Github, branch: str, path: str, text: str, message: str) -> None:
    existing = _content(gh, path, branch)
    payload = {
        "message": message,
        "content": base64.b64encode(text.encode("utf-8")).decode(),
        "branch": branch,
    }
    if existing is not None:
        payload["sha"] = existing[1]
    gh.request("PUT", f"/repos/{OWNER}/{SOLVE}/contents/{path}", payload)

def validate_canary2_candidate(gh: Github, solve_root: Path, branch: str) -> dict[str,Any]:
    mod = _load_canary2_module(solve_root)
    if branch == CANARY2_CLOSURE_BRANCH:
        changed = _compare_files(gh, branch)
        if changed != [CANARY2_CLOSURE_PATH]:
            raise ControllerError(f"canary closure candidate diff mismatch: {changed}")
        got = _content(gh, CANARY2_CLOSURE_PATH, branch)
        if got is None:
            raise ControllerError("canary closure candidate missing")
        closure = json.loads(got[0])
        errors = mod.validate_closure(closure)
        if errors:
            raise ControllerError("canary closure invalid: " + "; ".join(errors))
        if _content(gh, CANARY2_CLOSURE_PATH, "main") is not None:
            raise ControllerError("canary closure already protected")
        ref = gh.request("GET", f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(branch,safe='/')}")
        head = ref.get("object",{}).get("sha") if isinstance(ref,dict) else None
        if not isinstance(head,str):
            raise ControllerError("canary closure head unavailable")
        return {"kind":"CANARY2_CLOSURE","branch":branch,"head_sha":head,"path":CANARY2_CLOSURE_PATH}
    if branch == CANARY2_ADVANCE_BRANCH:
        expected = sorted([CANARY2_REPLAY_PATH, CANARY2_ADJUDICATION_PATH, CANARY2_SUCCESSOR_PATH])
        changed = _compare_files(gh, branch)
        if changed != expected:
            raise ControllerError(f"canary advancement candidate diff mismatch: {changed}")
        replay_item = _content(gh, CANARY2_REPLAY_PATH, branch)
        adj_item = _content(gh, CANARY2_ADJUDICATION_PATH, branch)
        successor_item = _content(gh, CANARY2_SUCCESSOR_PATH, branch)
        if replay_item is None or adj_item is None or successor_item is None:
            raise ControllerError("canary advancement candidate incomplete")
        replay = json.loads(replay_item[0])
        adj = json.loads(adj_item[0])
        errors = mod.validate_bundle(replay, adj, successor_item[0])
        if errors:
            raise ControllerError("canary advancement invalid: " + "; ".join(errors))
        if any(_content(gh, path, "main") is not None for path in expected):
            raise ControllerError("canary advancement already partly protected")
        ref = gh.request("GET", f"/repos/{OWNER}/{SOLVE}/git/ref/heads/{urllib.parse.quote(branch,safe='/')}")
        head = ref.get("object",{}).get("sha") if isinstance(ref,dict) else None
        if not isinstance(head,str):
            raise ControllerError("canary advancement head unavailable")
        return {"kind":"CANARY2_ADVANCE","branch":branch,"head_sha":head,"paths":expected}
    raise ControllerError(f"unregistered canary lifecycle branch: {branch}")

def _run_canary2(gh: Github, solve_root: Path, main_sha: str, apply: bool) -> dict[str,Any]:
    mod = _load_canary2_module(solve_root)
    protected_closure = _content(gh, CANARY2_CLOSURE_PATH, "main")
    if protected_closure is None:
        try:
            closure = mod.build_closure(main_sha, "2026-10-07")
        except ValueError as exc:
            if "protected RESULT/1 absent" in str(exc):
                return {"canary":"GCL-E2E-CANARY-002","state":"WAITING_FOR_PROTECTED_RESULT"}
            raise
        pr = _find_pr(gh, CANARY2_CLOSURE_BRANCH)
        if apply and pr is None:
            _create_branch(gh, CANARY2_CLOSURE_BRANCH, main_sha)
            _put_text2(gh, CANARY2_CLOSURE_BRANCH, CANARY2_CLOSURE_PATH, json.dumps(closure,indent=2,sort_keys=True)+"\n", "Close GCL E2E canary cohort for deterministic replay")
        candidate = validate_canary2_candidate(gh, solve_root, CANARY2_CLOSURE_BRANCH) if apply else {"kind":"CANARY2_CLOSURE","branch":CANARY2_CLOSURE_BRANCH}
        if pr is None and apply:
            pr = gh.request("POST", f"/repos/{OWNER}/{SOLVE}/pulls", {
                "title":"Close GCL E2E canary cohort for deterministic replay",
                "head":CANARY2_CLOSURE_BRANCH, "base":"main",
                "body":"Mechanical one-member production canary cohort closure from protected RESULT/1 evidence. No mathematical, certification, publication, or external claim authority."
            })
        if not isinstance(pr,dict):
            return {**candidate,"state":"CLOSURE_CANDIDATE_READY"}
        live = gh.request("GET", f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}")
        head = live.get("head",{}).get("sha") if isinstance(live,dict) else None
        if head != candidate.get("head_sha"):
            raise ControllerError("canary closure PR head drift")
        if not _approval_exists(gh, int(pr["number"]), str(head)):
            return {**candidate,"pr_number":pr["number"],"state":"AWAITING_COUNCIL_CLERK_DOCUMENTARY_REVIEW"}
        if apply:
            out = gh.request("PUT", f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}/merge", {
                "sha":head,"merge_method":"squash",
                "commit_title":f"Close GCL E2E canary cohort (#{pr['number']})",
                "commit_message":"Mechanical canary cohort closure only. No mathematical or certification authority."
            })
            if not isinstance(out,dict) or out.get("merged") is not True:
                raise ControllerError(f"canary closure protected merge failed: {out!r}")
            return {**candidate,"pr_number":pr["number"],"state":"PROTECTED_CLOSURE_MERGED","merge_commit_sha":out.get("sha")}
        return {**candidate,"pr_number":pr["number"],"state":"READY_FOR_PROTECTED_CLOSURE_MERGE"}

    closure = json.loads(protected_closure[0])
    errors = mod.validate_closure(closure)
    if errors:
        raise ControllerError("protected canary closure invalid: " + "; ".join(errors))
    replay_main = _content(gh, CANARY2_REPLAY_PATH, "main")
    adj_main = _content(gh, CANARY2_ADJUDICATION_PATH, "main")
    successor_main = _content(gh, CANARY2_SUCCESSOR_PATH, "main")
    if replay_main is not None and adj_main is not None and successor_main is not None:
        replay = json.loads(replay_main[0])
        adj = json.loads(adj_main[0])
        errors = mod.validate_bundle(replay, adj, successor_main[0])
        if errors:
            raise ControllerError("protected canary advancement invalid: " + "; ".join(errors))
        return {"canary":"GCL-E2E-CANARY-002","state":"ADVANCED","replay_pass":replay.get("replay_pass"),"adjudication":adj.get("disposition"),"successor":adj.get("selected_successor")}
    if any(x is not None for x in (replay_main, adj_main, successor_main)):
        raise ControllerError("partial protected canary advancement bundle")

    replay = mod.build_replay()
    adj = mod.build_adjudication(replay)
    successor = mod.successor_text()
    if replay.get("replay_pass") is not True or adj.get("disposition") != "ADVANCE":
        return {"canary":"GCL-E2E-CANARY-002","state":"DETERMINISTIC_REPLAY_REJECTED","replay":replay}
    pr = _find_pr(gh, CANARY2_ADVANCE_BRANCH)
    if apply and pr is None:
        _create_branch(gh, CANARY2_ADVANCE_BRANCH, main_sha)
        _put_text2(gh, CANARY2_ADVANCE_BRANCH, CANARY2_REPLAY_PATH, json.dumps(replay,indent=2,sort_keys=True)+"\n", "Record GCL E2E canary deterministic replay")
        _put_text2(gh, CANARY2_ADVANCE_BRANCH, CANARY2_ADJUDICATION_PATH, json.dumps(adj,indent=2,sort_keys=True)+"\n", "Record GCL E2E canary deterministic adjudication")
        _put_text2(gh, CANARY2_ADVANCE_BRANCH, CANARY2_SUCCESSOR_PATH, successor, "Materialize precommitted GCL E2E canary successor")
    candidate = validate_canary2_candidate(gh, solve_root, CANARY2_ADVANCE_BRANCH) if apply else {"kind":"CANARY2_ADVANCE","branch":CANARY2_ADVANCE_BRANCH}
    if pr is None and apply:
        pr = gh.request("POST", f"/repos/{OWNER}/{SOLVE}/pulls", {
            "title":"Advance GCL E2E canary after deterministic replay",
            "head":CANARY2_ADVANCE_BRANCH,"base":"main",
            "body":"Deterministically generated replay, bounded adjudication, and the precommitted successor for the production E2E canary. No mathematical, certification, publication, or external claim authority."
        })
    if not isinstance(pr,dict):
        return {**candidate,"state":"ADVANCEMENT_CANDIDATE_READY"}
    live = gh.request("GET", f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}")
    head = live.get("head",{}).get("sha") if isinstance(live,dict) else None
    if head != candidate.get("head_sha"):
        raise ControllerError("canary advancement PR head drift")
    if not _approval_exists(gh, int(pr["number"]), str(head)):
        return {**candidate,"pr_number":pr["number"],"state":"AWAITING_COUNCIL_CLERK_DOCUMENTARY_REVIEW"}
    if apply:
        out = gh.request("PUT", f"/repos/{OWNER}/{SOLVE}/pulls/{pr['number']}/merge", {
            "sha":head,"merge_method":"squash",
            "commit_title":f"Advance GCL E2E canary after deterministic replay (#{pr['number']})",
            "commit_message":"Deterministic canary replay/adjudication and precommitted successor only. No external authority."
        })
        if not isinstance(out,dict) or out.get("merged") is not True:
            raise ControllerError(f"canary advancement protected merge failed: {out!r}")
        return {**candidate,"pr_number":pr["number"],"state":"PROTECTED_ADVANCEMENT_MERGED","merge_commit_sha":out.get("sha")}
    return {**candidate,"pr_number":pr["number"],"state":"READY_FOR_PROTECTED_ADVANCEMENT_MERGE"}

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--solve-root",type=Path,required=True)
    ap.add_argument("--apply",action="store_true")
    ap.add_argument("--report",type=Path,required=True)
    args=ap.parse_args()
    try:
        report=run(args.solve_root.resolve(),args.apply)
        rc=0
    except Exception as exc:
        report={"schema_version":"1.0.0","controller":"GCL_ERDOS_OPEN_POSTPROTECT_LIFECYCLE","fatal_error":str(exc),"authority_created":False}
        rc=2
    args.report.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(report,sort_keys=True))
    return rc

if __name__=="__main__":
    raise SystemExit(main())
