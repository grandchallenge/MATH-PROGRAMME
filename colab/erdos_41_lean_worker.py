#!/usr/bin/env python3
"""Colab-side, no-credential, bounded Lean executor. Unadjudicated evidence only."""
import argparse, hashlib, json, subprocess, sys, time
from pathlib import Path

TOOLCHAIN = "leanprover/lean4:v4.29.1"
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def execute(source, receipt, *, timeout=180):
    source, receipt=Path(source), Path(receipt)
    started=time.monotonic()
    data={"schema":"GCL-ERDOS-41-LEAN-COMPUTE/1","source_sha256":sha(source),
          "toolchain":TOOLCHAIN,"status":"RED","authority_effects":{"certification":False,"publication":False,"solve_dispatch":False}}
    try:
        version=subprocess.run(["elan","run",TOOLCHAIN,"lean","--version"],capture_output=True,text=True,timeout=30)
        if version.returncode: raise RuntimeError("Lean toolchain unavailable")
        data["lean_version"]=version.stdout.strip()
        result=subprocess.run(["elan","run",TOOLCHAIN,"lean",str(source)],capture_output=True,text=True,timeout=timeout)
        data.update({"exit_code":result.returncode,"stdout_sha256":hashlib.sha256(result.stdout.encode()).hexdigest(),
                     "stderr_sha256":hashlib.sha256(result.stderr.encode()).hexdigest(),
                     "stdout":result.stdout[:8000],"stderr":result.stderr[:8000]})
        data["status"]="GREEN_LEAN_CHECKED_UNADJUDICATED" if result.returncode==0 else "RED_LEAN"
    except Exception as err:
        data["error"]=type(err).__name__+": "+str(err)[:250]
    data["elapsed_seconds"]=round(time.monotonic()-started,3)
    receipt.write_text(json.dumps(data,sort_keys=True,indent=2)+"\n")
    return 0 if data["status"]=="GREEN_LEAN_CHECKED_UNADJUDICATED" else 1

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--source",default="/content/Erdos41Finite.lean")
    p.add_argument("--receipt",default="/content/erdos41_lean_receipt.json")
    p.add_argument("--timeout",type=int,default=180)
    a=p.parse_args()
    if not 30<=a.timeout<=600: p.error("timeout outside bounded envelope")
    sys.exit(execute(a.source,a.receipt,timeout=a.timeout))
