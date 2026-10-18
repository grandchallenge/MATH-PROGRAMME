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
        if job["toolchain"]!="leanprover/lean4:v4.29.1":
            raise ValueError("unapproved toolchain")
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
