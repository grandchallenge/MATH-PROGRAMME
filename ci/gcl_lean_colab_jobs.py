#!/usr/bin/env python3
"""Protected registry-based GCL Lean/Colab job dispatch."""
import argparse, hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/"governance/lean_colab/JOBS.json"

def jobs():
    source=json.loads(REGISTRY.read_text())
    if source.get("schema")!="GCL-LEAN-COLAB-JOBS/1": raise ValueError("bad registry")
    items={}
    for job in source["jobs"]:
        key=job["id"]
        if key in items or not re.fullmatch(r"[A-Z0-9-]+",key):
            raise ValueError("duplicate or malformed job")
        if job["authority"]!="UNADJUDICATED_COMPUTATIONAL_EVIDENCE_ONLY" or job["accelerator"]!="CPU":
            raise ValueError("unauthorized job")
        if not re.fullmatch(r"ci\.[a-z_0-9]+",job["launcher"]):
            raise ValueError("unregistered launcher")
        for field in ("source","worker"):
            path=(ROOT/job[field]).resolve()
            if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
                raise ValueError("job path escaped/missing")
            if hashlib.sha256(path.read_bytes()).hexdigest()!=job[field+"_sha256"]:
                raise ValueError("source or worker bytes changed")
        allowed = {
            "ERDOS-041-FINITE-001": (
                41, 2536, "leanprover/lean4:v4.29.1",
                "ci.erdos_41_lean_colab_host"),
            "ERDOS-0248-LEAN-REPLAY-001": (
                248, 3204, "leanprover/lean4:v4.33.0",
                "ci.erdos_248_lean_colab_host"),
        }
        if (key not in allowed or
                (job["problem_id"], job["review_issue"], job["toolchain"],
                 job["launcher"]) != allowed[key]):
            raise ValueError("unapproved frozen job/toolchain/issue binding")
        if key == "ERDOS-0248-LEAN-REPLAY-001":
            pinned = {
                "source_repository": "plby/lean-proofs",
                "source_commit": "8822f7ddef30fadbd92e1c6ab4ed897af356af5e",
                "source_blob": "166659f39a435831d1a751718f9a385effcd7dfa",
                "mathlib_commit": "db584cd6d46c92f209a44c0f1c829460d327499d",
                "manifest_blob": "1b7a0663de506f371211df75da206fa2c96befd2",
            }
            if any(job.get(k) != v for k, v in pinned.items()):
                raise ValueError("external proof or mathlib custody mismatch")
            p = (ROOT / job["host"]).resolve()
            if (not p.is_relative_to(ROOT.resolve()) or not p.is_file() or
                    hashlib.sha256(p.read_bytes()).hexdigest() != job["host_sha256"]):
                raise ValueError("registered host bytes changed")
        items[key]=job
    return items

def protected_main():
    if subprocess.check_output(["git","status","--porcelain"],cwd=ROOT).strip():
        raise ValueError("live worktree is dirty")
    local=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    remote=subprocess.check_output(["gh","api","repos/grandchallenge/MATH-PROGRAMME/branches/main","--jq",".commit.sha"],cwd=ROOT,text=True,timeout=40).strip()
    if local!=remote: raise ValueError("live job not at protected main")
    return local

def main():
    p=argparse.ArgumentParser()
    p.add_argument("action",choices=("list","verify","selftest","preflight","execute"))
    p.add_argument("--job")
    a=p.parse_args()
    try:
        found=jobs()
        if a.action in ("list","verify"):
            print(json.dumps({"state":"LOCKED_OFFLINE","jobs":sorted(found)},sort_keys=True))
            return 0
        if a.job not in found: raise ValueError("select a registered --job")
        if a.action=="execute": protected_main()
        argv=[sys.executable,"-m",found[a.job]["launcher"]]
        if a.action=="selftest": argv+=["--selftest"]
        if a.action=="execute": argv+=["--execute"]
        return subprocess.run(argv,cwd=ROOT,check=False).returncode
    except (ValueError,OSError,subprocess.CalledProcessError) as e:
        print("GCL_LEAN_COLAB_BLOCKED: "+str(e)[:250],file=sys.stderr)
        return 1

if __name__=="__main__":raise SystemExit(main())
