#!/usr/bin/env python3
"""PAAR-C bounded independent platform replay and GitHub run-origin readback.

Capturing through GitHub Actions corroborates an independent *platform*
execution. It does not attest CHAD's earlier execution or certify mathematics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

REPOSITORY = "grandchallenge/MATH-PROGRAMME"
WORKFLOW_PATH = ".github/workflows/paar-execution-origin.yml"
RECORD_TYPE = "GCL_PAAR_C_PLATFORM_EXECUTION_WITNESS/1"
JOB_NAME = "Protected PAAR-C bounded replay"
ARTIFACT_PREFIX = "paar-c-origin-"
ALLOWED_COMMANDS = (
    ("VERIFIER", ("python3", "-m", "unittest", "-q",
                  "tests.test_paar_role_evidence_v2")),
    ("ADVERSARY", ("python3", "-m", "unittest", "-q",
                   "tests.test_agent_routine_review")),
    ("REFEREE", ("python3",
                 "governance/assurance/GCL-PAAR-001/replay_baseline.py", "--offline")),
)
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA64 = re.compile(r"[0-9a-f]{64}\Z")


class OriginError(ValueError):
    pass


def demand(ok: bool, reason: str) -> None:
    if not ok:
        raise OriginError(reason)


def fingerprint(files: list[dict]) -> str:
    demand(isinstance(files, list) and 0 < len(files) < 100,
           "missing or truncated source manifest")
    manifest = []
    for entry in files:
        path, status, sha = entry.get("filename"), entry.get("status"), entry.get("sha")
        demand(isinstance(path, str) and path and not path.startswith("/")
               and ".." not in path.split("/") and status in
               ("modified", "added", "removed", "renamed"),
               "unsafe source manifest")
        if status != "removed":
            demand(isinstance(sha, str) and SHA40.fullmatch(sha),
                   "invalid Git blob in source manifest")
        manifest.append({"path": path, "status": status, "blob_sha": sha or "",
                         "previous_filename": entry.get("previous_filename") or ""})
    demand(len({e["path"] for e in manifest}) == len(manifest),
           "duplicate source path")
    raw = json.dumps(sorted(manifest, key=lambda x: x["path"]),
                     sort_keys=True, separators=(",",":"),ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()


def git_head(path: Path) -> str:
    return subprocess.check_output(("git", "rev-parse", "HEAD"),
                                   cwd=path, text=True, timeout=15).strip()


def source_binding(api_get, pr_number: int, candidate_sha: str,
                   material_sha256: str) -> dict:
    demand(type(pr_number) is int and pr_number > 0, "invalid PR number")
    demand(isinstance(candidate_sha, str) and SHA40.fullmatch(candidate_sha),
           "invalid candidate head")
    demand(isinstance(material_sha256, str) and SHA64.fullmatch(material_sha256),
           "invalid material hash")
    prefix = f"/repos/{REPOSITORY}/pulls/{pr_number}"
    pr = api_get(prefix)
    demand(isinstance(pr, dict) and pr.get("merged_at")
           and (pr.get("head") or {}).get("sha") == candidate_sha
           and (pr.get("base") or {}).get("ref") == "main"
           and ((pr.get("head") or {}).get("repo") or {}).get("full_name") == REPOSITORY,
           "candidate not exact-head merged in authorized repository")
    files = api_get(prefix + "/files?per_page=100")
    demand(isinstance(files,list) and len(files) == pr.get("changed_files")
           and fingerprint(files) == material_sha256,
           "candidate material SHA-256 drift")
    return {"repository": REPOSITORY, "pr_number": pr_number,
            "head_sha": candidate_sha, "material_sha256": material_sha256}


def capture(*, api_get, candidate_dir: Path, output_file: Path,
            pr_number: int, candidate_sha: str, material_sha256: str,
            environment: dict[str, str]) -> dict:
    bind = source_binding(api_get, pr_number, candidate_sha, material_sha256)
    demand(git_head(candidate_dir) == environment.get("GITHUB_SHA"), "trusted checkout head mismatch")
    demand(environment.get("GITHUB_ACTIONS") == "true"
           and environment.get("GITHUB_REPOSITORY") == REPOSITORY
           and environment.get("GITHUB_EVENT_NAME") == "workflow_dispatch"
           and environment.get("GITHUB_REF") == "refs/heads/main"
           and environment.get("RUNNER_ENVIRONMENT") == "github-hosted"
           and isinstance(environment.get("GITHUB_RUN_ID"),str)
           and environment["GITHUB_RUN_ID"].isdigit()
           and environment.get("GITHUB_RUN_ATTEMPT","").isdigit()
           and isinstance(environment.get("GITHUB_SHA"),str)
           and SHA40.fullmatch(environment["GITHUB_SHA"]),
           "not trusted workflow-dispatch execution environment")
    workflow_ref = environment.get("GITHUB_WORKFLOW_REF","")
    demand(workflow_ref == REPOSITORY+"/"+WORKFLOW_PATH+"@refs/heads/main",
           "untrusted workflow definition")
    current = api_get(f"/repos/{REPOSITORY}/branches/main")
    demand(current.get("protected") is True and
           current.get("commit",{}).get("sha") == environment["GITHUB_SHA"],
           "trusted checkout does not match protected main")
    manifest = api_get(f"/repos/{REPOSITORY}/pulls/{pr_number}/files?per_page=100")
    blobs = []
    for entry in manifest:
        demand(entry["status"] != "removed", "removed source file not replayable")
        actual = subprocess.check_output(("git", "rev-parse", "HEAD:"+entry["filename"]),
                                         cwd=candidate_dir,text=True,timeout=15).strip()
        demand(actual == entry["sha"], "trusted source blob differs from reviewed candidate")
        blobs.append({"path":entry["filename"], "sha":actual})
    blobs.sort(key=lambda x:x["path"])
    child_env = {k: environment[k] for k in ("PATH","HOME","TMPDIR")
                 if k in environment}
    child_env.update({"PYTHONPATH":str(candidate_dir.resolve()),"CI":"true"})
    observed = []
    for role, command in ALLOWED_COMMANDS:
        completed = subprocess.run(command, cwd=candidate_dir, text=True,
                                   errors="strict", capture_output=True,
                                   env=child_env,timeout=90,check=False)
        demand(completed.returncode == 0,role+" runner failed")
        selected = "stderr" if completed.stderr.strip() else "stdout"
        data = getattr(completed, selected).encode("utf-8")
        demand(0 < len(data) <= 131072,role+" output absent/oversize")
        if role in ("VERIFIER","ADVERSARY"):
            expected = 14 if role == "VERIFIER" else 36
            demand(f"Ran {expected} tests" in (completed.stdout+completed.stderr)
                   and "OK" in (completed.stdout+completed.stderr),
                   role+" missing expected test results")
        if role == "REFEREE":
            parsed = json.loads(completed.stdout)
            demand(parsed.get("result") == "PASS_BOUNDED_ONLY"
                   and parsed.get("global_integrity_certified") is False,
                   "referee replay invalid or falsely certified")
        observed.append({"role":role,"command":list(command),"exit_code":0,
                         "selected_stream":selected,"stdout":completed.stdout,
                         "stderr":completed.stderr,
                         "selected_sha256":hashlib.sha256(data).hexdigest()})
    proof={"record_type":RECORD_TYPE,"source":bind,
           "workflow_path":WORKFLOW_PATH,"protected_source_blobs":blobs,
           "workflow_sha":environment["GITHUB_SHA"],
           "run_id":int(environment["GITHUB_RUN_ID"]),
           "run_attempt":int(environment["GITHUB_RUN_ATTEMPT"]),
           "run_event":"workflow_dispatch",
           "runner_environment":"github-hosted",
           "producer_code":"protected-main-workflow",
           "executions":observed,"limits":{
               "independent_platform_replay":True,
               "original_chad_execution_attested":False,
               "scientific_certification":False,
               "gcl_wide_assurance_certified":False}}
    output_file.parent.mkdir(parents=True,exist_ok=True)
    output_file.write_text(json.dumps(proof,indent=2,sort_keys=True)+"\n")
    return proof


def verify_witness(*, api_get, witness: dict, run_id: int) -> dict:
    """Check a separately downloaded artifact against authentic GitHub run data."""
    demand(type(run_id) is int and run_id > 0 and
           isinstance(witness,dict) and witness.get("record_type") == RECORD_TYPE,
           "invalid execution witness")
    demand(witness.get("run_id") == run_id, "artifact from another run")
    attempt = witness.get("run_attempt")
    demand(type(attempt) is int and attempt > 0, "invalid run attempt")
    run = api_get(f"/repos/{REPOSITORY}/actions/runs/{run_id}")
    demand(isinstance(run,dict) and run.get("repository",{}).get("full_name") == REPOSITORY
           and run.get("event") == "workflow_dispatch"
           and run.get("status") == "completed" and run.get("conclusion") == "success"
           and run.get("path") == WORKFLOW_PATH
           and run.get("head_branch") == "main"
           and run.get("run_attempt") == attempt,
           "GitHub did not corroborate trusted run identity/status")
    workflow_sha = run.get("head_sha")
    demand(isinstance(workflow_sha,str) and SHA40.fullmatch(workflow_sha)
           and witness.get("workflow_sha") == workflow_sha
           and witness.get("workflow_path") == WORKFLOW_PATH
           and witness.get("run_event") == "workflow_dispatch"
           and witness.get("runner_environment") == "github-hosted"
           and witness.get("producer_code") == "protected-main-workflow",
           "trusted workflow identity mismatch")
    main = api_get(f"/repos/{REPOSITORY}/branches/main")
    current_sha = main.get("commit", {}).get("sha") if isinstance(main, dict) else None
    demand(main.get("protected") is True and isinstance(current_sha, str)
           and SHA40.fullmatch(current_sha),
           "protected main missing or no longer protected")
    # A successful GitHub-hosted historical run survives subsequent protected
    # admissions only if the workflow commit remains an actual ancestor of
    # protected main. Compare authenticated GitHub history, not a claimed
    # ancestor field inside the worker-uploaded witness.
    if current_sha == workflow_sha:
        historical_ancestry = "CURRENT_PROTECTED_HEAD"
    else:
        compare = api_get(
            f"/repos/{REPOSITORY}/compare/{workflow_sha}...{current_sha}")
        demand(isinstance(compare, dict)
               and compare.get("status") == "ahead"
               and type(compare.get("ahead_by")) is int
               and compare["ahead_by"] > 0
               and type(compare.get("behind_by")) is int
               and compare["behind_by"] == 0
               and (compare.get("base_commit") or {}).get("sha") == workflow_sha
               and (compare.get("merge_base_commit") or {}).get("sha") == workflow_sha,
               "workflow origin not ancestor of current protected main")
        historical_ancestry = "VERIFIED_PROTECTED_ANCESTOR"
    response = api_get(f"/repos/{REPOSITORY}/actions/runs/{run_id}/jobs?per_page=100")
    jobs = response.get("jobs") if isinstance(response,dict) else None
    demand(isinstance(jobs,list) and response.get("total_count",101) <= 100,
           "incomplete authenticated job enumeration")
    matching = [job for job in jobs
                if job.get("name") == JOB_NAME and job.get("head_sha") == workflow_sha
                and job.get("conclusion") == "success"
                and job.get("status") == "completed"
                and job.get("runner_group_name") == "GitHub Actions"]
    demand(len(matching) == 1, "no successful GitHub-hosted protected replay job")
    steps = matching[0].get("steps") or []
    for name in ("Run independent bounded assertions", "Upload execution origin artifact"):
        demand(any(s.get("name") == name and s.get("conclusion") == "success"
                   and s.get("status") == "completed" for s in steps),
               "missing actual trusted runner step: "+name)
    artifact_list = api_get(f"/repos/{REPOSITORY}/actions/runs/{run_id}/artifacts?per_page=100")
    artifacts = artifact_list.get("artifacts") if isinstance(artifact_list,dict) else None
    demand(isinstance(artifacts,list) and artifact_list.get("total_count",101) <= 100,
           "incomplete artifact listing")
    name = f"{ARTIFACT_PREFIX}{run_id}-{attempt}"
    found = [a for a in artifacts if a.get("name") == name
             and a.get("expired") is False
             and (a.get("workflow_run") or {}).get("id") == run_id]
    demand(len(found) == 1, "GitHub workflow run artifact missing or expired")
    source = witness.get("source") or {}
    binding = source_binding(api_get, source.get("pr_number"),
                             source.get("head_sha"), source.get("material_sha256"))
    demand(source == binding, "artifact source binding drift")
    manifest = api_get(f"/repos/{REPOSITORY}/pulls/{source['pr_number']}/files?per_page=100")
    expected = sorted(({"path":e["filename"],"sha":e["sha"]} for e in manifest),
                      key=lambda x:x["path"])
    demand(witness.get("protected_source_blobs") == expected,
           "runner source blob list not source-bound")
    for entry in expected:
        path = urllib.parse.quote(entry["path"],safe="/")
        obj = api_get(f"/repos/{REPOSITORY}/contents/{path}?ref={workflow_sha}")
        demand(obj.get("sha") == entry["sha"],
               "protected workflow code differs from exact candidate blob")
    executions = witness.get("executions")
    demand(isinstance(executions,list) and len(executions) == len(ALLOWED_COMMANDS),
           "wrong role-execution count")
    for item, (role,command) in zip(executions,ALLOWED_COMMANDS):
        demand(isinstance(item,dict) and item.get("role") == role
               and item.get("command") == list(command)
               and type(item.get("exit_code")) is int and item.get("exit_code") == 0
               and item.get("selected_stream") in ("stderr","stdout")
               and isinstance(item.get("stderr"),str)
               and isinstance(item.get("stdout"),str),
               "role command or bounded output invalid")
        data = item[item["selected_stream"]].encode("utf-8")
        demand(0 < len(data) <= 131072 and
               hashlib.sha256(data).hexdigest() == item.get("selected_sha256"),
               "execution output SHA-256 drift")
        if role in ("VERIFIER","ADVERSARY"):
            expected = 14 if role == "VERIFIER" else 36
            combined = item["stdout"]+item["stderr"]
            demand(f"Ran {expected} tests" in combined and "OK" in combined,
                   "expected test result missing: "+role)
        else:
            try:
                result = json.loads(item["stdout"])
            except (ValueError,TypeError) as error:
                raise OriginError("referee JSON cannot be replayed") from error
            demand(result.get("result") == "PASS_BOUNDED_ONLY" and
                   result.get("global_integrity_certified") is False,
                   "referee claimed unsupported certification")
    demand(witness.get("limits") == {
        "independent_platform_replay": True,
        "original_chad_execution_attested": False,
        "scientific_certification": False,
        "gcl_wide_assurance_certified": False,
    }, "untrue or expanded origin witness claims")
    return {"result":"PASS_BOUNDED_PLATFORM_ORIGIN_REPLAY",
            "run_id":run_id,"run_attempt":attempt,
            "artifact_id":found[0]["id"],"artifact_name":name,
            "trusted_workflow_head":workflow_sha,
            "current_protected_main":current_sha,
            "protected_history_relation":historical_ancestry,"source":binding,
            "roles_verified":[r for r,_ in ALLOWED_COMMANDS],
            "execution_service":"GitHub-hosted Actions",
            "historical_chad_execution_attested":False,
            "gcl_wide_assurance_certified":False}


def gh_api(path: str) -> dict:
    completed = subprocess.run(("gh","api",path.lstrip("/")),
                               capture_output=True,text=True,timeout=35,check=True)
    return json.loads(completed.stdout)


def cli() -> None:
    parser=argparse.ArgumentParser()
    subs=parser.add_subparsers(dest="action",required=True)
    c=subs.add_parser("capture")
    c.add_argument("--candidate-dir",type=Path,required=True)
    c.add_argument("--output-file",type=Path,required=True)
    c.add_argument("--pr-number",type=int,required=True)
    c.add_argument("--candidate-sha",required=True)
    c.add_argument("--material-sha256",required=True)
    v=subs.add_parser("verify-live")
    v.add_argument("--run-id",type=int,required=True)
    args=parser.parse_args()
    if args.action=="capture":
        proof=capture(api_get=gh_api,candidate_dir=args.candidate_dir,
                      output_file=args.output_file,pr_number=args.pr_number,
                      candidate_sha=args.candidate_sha,
                      material_sha256=args.material_sha256,
                      environment=dict(os.environ))
        print(json.dumps({"status":"CAPTURED_ON_GITHUB_HOSTED_RUNNER",
                          "run_id":proof["run_id"],"subject":proof["source"],
                          "roles":[i["role"] for i in proof["executions"]]},
                         sort_keys=True))
    else:
        with tempfile.TemporaryDirectory(prefix="gcl-paar-origin-") as temporary:
            meta=gh_api(f"/repos/{REPOSITORY}/actions/runs/{args.run_id}")
            attempt=meta.get("run_attempt")
            demand(type(attempt) is int and attempt>0, "missing run attempt")
            name=f"{ARTIFACT_PREFIX}{args.run_id}-{attempt}"
            subprocess.run(("gh","run","download",str(args.run_id),
                            "-R",REPOSITORY,"-n",name,"-D",temporary),
                           check=True,timeout=90,capture_output=True,text=True)
            file=Path(temporary)/"witness.json"
            demand(file.is_file(), "downloaded artifact has no witness.json")
            result=verify_witness(api_get=gh_api,
                    witness=json.loads(file.read_text()),run_id=args.run_id)
            print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == "__main__":
    cli()
