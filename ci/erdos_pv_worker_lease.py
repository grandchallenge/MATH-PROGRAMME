#!/usr/bin/env python3
"""Atomic per-problem GitHub reservation/return (not protected execution authority)."""
from __future__ import annotations
import argparse, json, re, subprocess, sys, uuid
from pathlib import Path
from erdos_pv_queue import permitted
from erdos_pv_result_contract import validate_return
from validate_erdos_pv_full_coverage import REG,read
REPO="grandchallenge/MATH-PROGRAMME"
BASE=f"repos/{REPO}"
PREFIX="refs/heads/gcl-pv-claims/"
TASK=re.compile(r"ERDOS-PV-(\d{4})-([ABCD])\Z")

def run(*argv,stdin=None):
 p=subprocess.run(argv,input=stdin,text=True,capture_output=True)
 if p.returncode: raise RuntimeError(f"Command failed {argv[:3]}: {p.stderr[:800]}")
 return p.stdout

def api(method,path,data=None):
 args=["gh","api","--method",method,f"{BASE}/{path}"]
 if data is not None: args+=["--input","-"]
 s=run(*args,stdin=json.dumps(data) if data is not None else None)
 return json.loads(s) if s.strip() else {}

def comments(issue):
 s=run("gh","api","--paginate","--slurp",f"{BASE}/issues/{issue}/comments?per_page=100")
 return [c for page in json.loads(s) for c in page]

def scope(task_id):
 m=TASK.fullmatch(task_id)
 if not m or not 1<=int(m[1])<=1221: raise ValueError("Bad exact task ID")
 n,stage=int(m[1]),m[2]
 reg=read(REG);cohort=reg["cohorts"][(n-1)//100]
 row=read(cohort["packet"])["items"][(n-1)%100]
 if row["problem_id"]!=n or row["stage_work_items"][stage]["task_id"]!=task_id:
  raise ValueError("Manifest task identity drift")
 if not permitted(row,stage): raise ValueError("Task not eligible on protected manifest")
 return {"id":task_id,"number":n,"stage":stage,"row":row,
         "issue":row["stage_work_items"][stage]["issue_number"],"packet":cohort["packet"]}

def ref(s): return PREFIX+s["id"]
def current_ref(s):
 p=subprocess.run(["gh","api",f"{BASE}/git/ref/{ref(s).removeprefix('refs/')}"],
                  text=True,capture_output=True)
 if p.returncode==0: return json.loads(p.stdout)
 if "404" in p.stderr and "Not Found" in p.stderr: return None
 raise RuntimeError(f"Ref readback failed: {p.stderr[:750]}")

def preflight(s):
 issue=api("GET",f"issues/{s['issue']}")
 labels={x["name"] for x in issue.get("labels",[])}
 if issue["state"]!="open" or "gcl-state:available" not in labels or "gcl-state:blocked" in labels:
  raise ValueError("Issue not OPEN and AVAILABLE")
 remote=api("GET",f"contents/{s['packet']}?ref=main")
 local=run("git","hash-object",str(Path(__file__).resolve().parents[1]/s["packet"])).strip()
 if local!=remote["sha"]:raise ValueError("Local manifest differs from protected main")
 cs=comments(s["issue"])
 if any((x.get("body") or "").startswith("RESULT/1\n") and
        f"ASSIGNMENT_ID: {s['id']}" in x["body"] for x in cs):
  raise ValueError("Exact task already returned; do not duplicate")
 return {"source_blob":local,"comments":cs}

def claim(s):
 pre=preflight(s)
 held=current_ref(s)
 if held:return {"result":"HELD","task":s["id"],"sha":held["object"]["sha"]}
 main=api("GET","git/ref/heads/main")["object"]["sha"]
 tree=api("GET",f"git/commits/{main}")["tree"]["sha"]
 actor=run("gh","api","user","--jq",".login").strip()
 message=(f"GCL_PV_RESERVATION/1 task={s['id']} actor={actor} "
          f"source_sha256={s['row']['source_issue_body_sha256']} "
          f"cohort_blob={pre['source_blob']} nonce={uuid.uuid4().hex}")
 commit=api("POST","git/commits",{"message":message,"tree":tree,"parents":[main]})
 try:
  api("POST","git/refs",{"ref":ref(s),"sha":commit["sha"]})
 except RuntimeError as error:
  winner=current_ref(s)
  return {"result":"LOST_RACE_OR_UNCERTAIN","task":s["id"],
          "winner_sha":winner["object"]["sha"] if winner else None,
          "write_error":str(error)[:320]}
 held=current_ref(s)
 if not held or held["object"]["sha"]!=commit["sha"]:
  raise RuntimeError("Claim readback mismatch")
 return {"result":"ACQUIRED","task":s["id"],"actor":actor,
         "ref":ref(s),"claim_sha":commit["sha"],"source_blob":pre["source_blob"]}

def submit(s,sha,body_path):
 held=current_ref(s)
 if not held or held["object"]["sha"]!=sha:
  raise ValueError("Reservation SHA not held")
 actor=run("gh","api","user","--jq",".login").strip()
 msg=api("GET",f"git/commits/{sha}")["message"]
 if (not msg.startswith("GCL_PV_RESERVATION/1 ") or
     f"task={s['id']} " not in msg or f"actor={actor} " not in msg or
     f"source_sha256={s['row']['source_issue_body_sha256']}" not in msg):
  raise ValueError("Lease actor, task or source mismatch")
 live=preflight(s)
 body=Path(body_path).read_text(encoding="utf-8")
 validate_return(s["row"],s["stage"],body,[x.get("body") or "" for x in live["comments"]])
 posted=api("POST",f"issues/{s['issue']}/comments",{"body":body})
 matches=[x for x in comments(s["issue"]) if x.get("body")==body]
 if len(matches)!=1 or matches[0]["id"]!=posted["id"]:
  raise RuntimeError("Result comment uniqueness/readback failed")
 return {"result":"RETURNED","task":s["id"],"comment_id":posted["id"],
         "url":posted["html_url"],"claim_sha":sha,
         "ref_still_held_until_protected_admission":True}

def inspect(s):
 held=current_ref(s)
 hits=[{"id":x["id"],"url":x.get("html_url")} for x in comments(s["issue"])
       if (x.get("body") or "").startswith("RESULT/1\n") and
       f"ASSIGNMENT_ID: {s['id']}" in (x.get("body") or "")]
 return {"result":"INSPECTED","task":s["id"],
         "claim_sha":held["object"]["sha"] if held else None,
         "returns":hits}

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("action",choices=("inspect","claim","return"))
 p.add_argument("task_id")
 p.add_argument("--claim-sha");p.add_argument("--body-file")
 a=p.parse_args()
 s=scope(a.task_id)
 if a.action=="inspect":out=inspect(s)
 elif a.action=="claim":out=claim(s)
 else:
  if not a.claim_sha or not a.body_file:p.error("Need --claim-sha and --body-file")
  out=submit(s,a.claim_sha,a.body_file)
 print(json.dumps(out,sort_keys=True))
if __name__=="__main__":
 try:main()
 except (RuntimeError,ValueError) as exc:
  print(json.dumps({"result":"FAIL_CLOSED","error":str(exc)}))
  sys.exit(2)
