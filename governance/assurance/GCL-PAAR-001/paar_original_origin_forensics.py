#!/usr/bin/env python3
"""Bounded GCL-PAAR-001 historical CHAD origin forensics, never attestation.

A protected Git dossier and matching files do not prove a command was
executed by the claimed original system. The live inspection is scoped.
"""
from __future__ import annotations
import argparse
import base64
import collections
import datetime
import hashlib
import json
import re
import sqlite3
import subprocess
from pathlib import Path

ORIGIN="grandchallenge/INTELLECT"
PR=121
SUBJECT="e577477b656c6865698d5dbc18962e2810f53a26"
DOSSIER_PATH=f"governance/agent_execution/reviews/MATH-PROGRAMME-{SUBJECT}.json"
DOSSIER_BLOB="4b3d108922ed9cf345d6407d81a216a93da697c1"
EXPECTED={
    "VERIFIER":("verifier.stderr",
                "6911b42399b43e37b097888660a5f386fc6294d23088649fcbc03dc453e5bb06"),
    "ADVERSARY":("adversary.stderr",
                 "62e6bd3a77554540929dd26eab6204ab86056dc07bacce00a71e4482e9f4bcb8"),
    "REFEREE":("referee.stdout",
               "eb067ed4a0c2e2b16807e6a025d3537f65c45ed9c732c3650c3a3c1a70f77a85"),
}
WINDOW=("2026-10-15T08:08","2026-10-15T08:12")

class EvidenceError(ValueError):
    pass

def require(condition, reason):
    if not condition: raise EvidenceError(reason)

def sha256(raw):
    return hashlib.sha256(raw).hexdigest()

def gh(path):
    result=subprocess.run(["gh","api",path.lstrip("/")],
        text=True,capture_output=True,check=True,timeout=30)
    return json.loads(result.stdout)

def verify_files(dossier, files, source_git_blob):
    require(source_git_blob==DOSSIER_BLOB,"protected source dossier blob drift")
    require(isinstance(dossier,dict) and dossier.get("record_type")=="GCL_AGENT_REVIEW_DOSSIER_V1"
            and (dossier.get("subject") or {}).get("head_sha")==SUBJECT,
            "historical dossier identity mismatch")
    passes=dossier.get("passes")
    require(isinstance(passes,list) and len(passes)==3,"historical role count drift")
    output=[]
    for role_pass, (role,(filename,expected)) in zip(passes,EXPECTED.items()):
        checks=role_pass.get("checks")
        require(role_pass.get("role")==role
                and isinstance(checks,list) and len(checks)==1
                and checks[0].get("exit_code")==0
                and checks[0].get("receipt_sha256")==expected,
                "protected logical role or declared output digest drift")
        raw=files.get(filename)
        require(type(raw) is bytes and sha256(raw)==expected,
                "historical raw output missing or tampered: "+role)
        output.append({"role":role,"filename":filename,
                       "sha256":expected,"bytes":len(raw),
                       "dossier_declared_digest_matches":True,
                       "original_execution_service_attested":False})
    return output

def inspect_journal(dbfile):
    connection=sqlite3.connect(f"file:{dbfile}?mode=ro",uri=True)
    try:
        rows=connection.execute(
            "SELECT phase,receipt,exit_code FROM events "
            "WHERE utc >= ? AND utc < ? AND operation = 'run_bash'",
            WINDOW).fetchall()
        return {"window_start_utc":WINDOW[0],"window_end_utc":WINDOW[1],
                "events":len(rows),
                "phases":dict(collections.Counter(row[0] for row in rows)),
                "entries_with_embedded_receipt":sum(row[1] is not None for row in rows),
                "entries_with_command_and_output_binding":0,
                "reason":"console row schema contains event hash/run-id/time, operation, phase, optional receipt and exit code; inspected window has no embedded receipts or command transcript",
                "execution_origin_attested":False}
    finally:
        connection.close()

def inspect_commander_receipts(receipts_dir):
    paths=sorted(Path(receipts_dir).glob("*.json"))
    shapes=collections.Counter()
    for p in paths:
        entry=json.loads(p.read_text())
        d=entry.get("data",{})
        require(isinstance(d,dict),"unexpected operator receipt layout")
        shapes.update([",".join(sorted(d.keys()))])
    # A Commander metadata/status receipt is not a signed original Bash
    # invocation record even if it contains an operator name.
    command_bound=sum("command_sha256" in json.loads(p.read_text()).get("data",{})
                      for p in paths)
    return {"metadata_receipts_examined":len(paths),
            "command_bound_receipts":command_bound,
            "field_shapes":dict(shapes),
            "evidence_limit":"scoped local receipt directory; not a complete all-time execution inventory",
            "independent_original_execution_attested":False}

def classify(dossier, local_outputs, dossier_blob, journal, receipts, source_reviews):
    outputs=verify_files(dossier,local_outputs,dossier_blob)
    require(journal["entries_with_embedded_receipt"]==0
            and receipts["command_bound_receipts"]==0,
            "additional command-bound historical evidence demands separate investigation")
    require(isinstance(source_reviews,list),"source review API absent")
    return {
      "record_type":"GCL_PAAR_C_HISTORICAL_ORIGIN_ASSESSMENT/1",
      "subject":{"repository":"grandchallenge/MATH-PROGRAMME",
                 "pr_number":2624,"head_sha":SUBJECT,
                 "source_repository":ORIGIN,"source_pr":PR,
                 "dossier_git_blob":DOSSIER_BLOB},
      "output_digests":outputs,
      "journal_scope":journal,
      "commander_receipt_scope":receipts,
      "historical_native_source_approving_reviews":sum(
         row.get("state")=="APPROVED" for row in source_reviews),
      "assessment":"HISTORICAL_OUTPUT_HASH_MATCH_ORIGINAL_EXECUTION_ORIGIN_UNATTESTED",
      "original_command_execution_authenticated":False,
      "independent_reviewer_system_authenticated":False,
      "later_platform_replay_is_original_execution_proof":False,
      "protected_dossier_authentic":True,
      "requires_provenance_upgrade":True,
      "limitations":[
          "Matching output hashes do not prove invocation or operator identity",
          "Filesystem modification times are not independent attestation",
          "Console events contain no command or raw output linkage",
          "Commander metadata receipts contain no matched command invocation",
          "No native review or separate runner authentication is inferred",
          "Later GitHub hosted execution is a distinct, not historical, run",
          "Other unexamined evidence sources cannot be ruled out"
      ],
      "next_required_origin_proof":"Independent contemporaneous exact-command, source, output, time, actor and run identity; otherwise retain historical UNATTESTED status",
      "scope_of_result":"Bounded forensic finding; not estate-wide certification"
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--evidence-dir",type=Path,required=True)
    parser.add_argument("--console-db",type=Path,required=True)
    parser.add_argument("--commander-receipts-dir",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    remote=gh(f"/repos/{ORIGIN}/contents/{DOSSIER_PATH}")
    require(remote.get("sha")==DOSSIER_BLOB,"protected dossier SHA mismatch")
    dossier=json.loads(base64.b64decode(remote["content"]))
    pr=gh(f"/repos/{ORIGIN}/pulls/{PR}")
    require(pr.get("merged_at") and pr["head"]["sha"]==
            "69f89aa56c373a5978e58740fb60a9a2e6b32a3d",
            "source PR head or protected merge drift")
    reviews=gh(f"/repos/{ORIGIN}/pulls/{PR}/reviews?per_page=100")
    files={name:(args.evidence_dir/name).read_bytes() for name,_ in EXPECTED.values()}
    report=classify(dossier,files,remote["sha"],inspect_journal(args.console_db),
                    inspect_commander_receipts(args.commander_receipts_dir),reviews)
    report["observed_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n")
    print(json.dumps({"assessment":report["assessment"],"matched_outputs":len(report["output_digests"]),
       "journal_events":report["journal_scope"]["events"],
       "commander_receipts":report["commander_receipt_scope"]["metadata_receipts_examined"],
       "original_execution_authenticated":False},sort_keys=True))

if __name__=="__main__":main()
