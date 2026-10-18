#!/usr/bin/env python3
"""Authenticated-host Colab Lean launch; no GitHub/Colab credentials in payload."""
import argparse, hashlib, json, os, subprocess, tempfile, uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"experiments/erdos-024/lean/Erdos41Finite.lean"
WORKER=ROOT/"colab/erdos_41_lean_worker.py"
TOOLCHAIN="leanprover/lean4:v4.29.1"
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cli(argv,timeout=100):
    p=subprocess.run(argv,capture_output=True,text=True,timeout=timeout)
    if p.returncode: raise RuntimeError("Colab operation failed: "+argv[2])
def launch(colab,folder):
    session="gcl-e41-lean-"+uuid.uuid4().hex[:12]
    prefix=[colab,"--auth=oauth2"]
    allocated=False
    try:
        cli(prefix+["new","-s",session]);allocated=True
        for local,remote in ((SOURCE,"/content/Erdos41Finite.lean"),(WORKER,"/content/erdos_41_lean_worker.py")):
            cli(prefix+["upload","-s",session,str(local),remote])
        # Colab CLI execution uses IPython; run worker with clean argv.
        snippet=("import runpy,sys;sys.argv=['/content/erdos_41_lean_worker.py'];"+
                 "runpy.run_path('/content/erdos_41_lean_worker.py',run_name='__main__')")
        launcher=folder/"launch.py"
        launcher.write_text(snippet+"\n")
        cli(prefix+["exec","-s",session,"-f",str(launcher),"--timeout","240"],timeout=300)
        cli(prefix+["download","-s",session,"/content/erdos41_lean_receipt.json",str(folder/"receipt.json")])
    finally:
        if allocated: cli(prefix+["stop","-s",session])
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--selftest",action="store_true",help="offline governed host and worker contract tests; no GitHub/Colab allocation")
    p.add_argument("--execute",action="store_true")
    p.add_argument("--colab",default="colab")
    p.add_argument("--output",type=Path,default=ROOT/"runs/erdos-41-lean")
    args=p.parse_args()
    if args.selftest:
        from unittest import TestLoader, TextTestRunner
        suite = TestLoader().loadTestsFromNames((
            "tests.test_erdos_41_lean_colab",
            "tests.test_erdos_41_lean_colab_host",
        ))
        result = TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            raise SystemExit(1)
        print(json.dumps({"state": "SELFTEST_GREEN_NO_GITHUB_NO_COLAB", "tests": result.testsRun,
                          "source_sha256": digest(SOURCE), "worker_sha256": digest(WORKER),
                          "toolchain": TOOLCHAIN}))
        return
    # Existing source-lock and authenticated Project queue are mandatory at live kickoff.
    from ci.erdos_forge_copilot_pilot import gh,review_ready,comment_history,selected_record,ROSTER
    row=selected_record(json.loads(ROSTER.read_text()))
    issue=gh("repos/grandchallenge/MATH-PROGRAMME/issues/2536")
    fields=gh("repos/grandchallenge/MATH-PROGRAMME/issues/2536/issue-field-values")
    allowed,reason=review_ready(issue,fields,comment_history(2536))
    if not allowed: raise RuntimeError("authenticated queue preflight blocked: "+reason)
    if row["source_critical_review_issue"]!=2536: raise RuntimeError("queue source changed")
    identity={"schema":"GCL-ERDOS-41-LEAN-LAUNCH/1","source_sha256":digest(SOURCE),
              "worker_sha256":digest(WORKER),"toolchain":TOOLCHAIN,
              "queue":"AVAILABLE","authority":"UNADJUDICATED_COMPUTE_ONLY"}
    if not args.execute:
        print(json.dumps({"state":"PREPARED_NO_COLAB_ALLOCATION",**identity}));return
    args.output.mkdir(parents=True,exist_ok=True)
    ticket=args.output/(".attempted-"+identity["source_sha256"]+"-"+identity["worker_sha256"])
    fd=os.open(ticket,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
    os.close(fd)
    run=args.output/uuid.uuid4().hex;run.mkdir()
    try:
        launch(args.colab,run)
        receipt=json.loads((run/"receipt.json").read_text())
        if receipt.get("source_sha256")!=identity["source_sha256"] or receipt.get("toolchain")!=TOOLCHAIN or receipt.get("status")!="GREEN_LEAN_CHECKED_UNADJUDICATED" or receipt.get("exit_code")!=0 or any(receipt.get("authority_effects",{}).values()) or not str(receipt.get("lean_version","")).startswith("Lean (version 4.29.1,") or (receipt.get("elan_provisioning")=="installed_pinned_release" and receipt.get("elan_archive_sha256")!="42b94d4244e8353142c456ec0e4ca6528fd898a6c604d4059f494e706e431f63"):
            raise RuntimeError("untrusted or failed Lean receipt")
        print(json.dumps({"state":"VERIFIED_UNADJUDICATED","receipt_sha256":digest(run/"receipt.json"),"run_dir":str(run),**identity}))
    except Exception:
        print(json.dumps({"state":"RED","run_dir":str(run),"ticket":str(ticket)}))
        raise
if __name__=="__main__":main()
