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

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

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
    return report

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
