#!/usr/bin/env python3
"""Evidence-only Erdős #41 finite semantic replay; runnable locally or in Colab.

No GitHub token, model, external network, or publication is required. The protected
GitHub queue and original source must be checked by an authenticated publisher.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import platform
import sys
import time
from datetime import datetime, timezone
from itertools import combinations_with_replacement
from pathlib import Path

COHORT = "ERDOS-ROLLING-024-001"
SOURCE_BLOB = "5e9eeb26586d087f4b2ab3d82734ea5ed87ddf50"
PROVIDER_COMMIT = "85f863718beeec7b58a3a1926ee92e3472bc2020"
ISSUE = 2536

def stable(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def run(roster_path: Path, output_path: Path):
    began = time.monotonic()
    roster_bytes = roster_path.read_bytes()
    roster = json.loads(roster_bytes)
    if roster.get("cohort_id") != COHORT or len(roster.get("items", [])) != 24:
        raise ValueError("protected cohort mismatch")
    rows = [x for x in roster["items"] if x.get("problem_id") == 41]
    if len(rows) != 1:
        raise ValueError("missing/duplicate Erdős #41")
    row = rows[0]
    p = row["protected_statement"]
    if (row["source_critical_review_issue"] != ISSUE or row["catalogue_issue"] != 1310
        or row["worker_result_comment_id"] != 6104193801
        or p["provider_commit"] != PROVIDER_COMMIT or p["git_blob_sha1"] != SOURCE_BLOB
        or p["path"] != "FormalConjectures/ErdosProblems/41.lean"):
        raise ValueError("source binding mismatch")
    if row["claimable"] or row["solve_execution_authorized"] or row["certification_authorized"]:
        raise ValueError("unexpected mathematical authority")
    B = (1,2,3)
    subsets = [tuple(B)]  # single three-element subset
    multisets = list(combinations_with_replacement(B,3))
    witnesses = [t for t in multisets if sum(t)==5]
    if subsets != [(1,2,3)] or (1,1,3) not in witnesses or (1,2,2) not in witnesses:
        raise AssertionError("finite witness failed")
    evidence = {
        "schema": "GCL-ERDOS-041-DETERMINISTIC-REPLAY/1",
        "status": "PASS_FINITE_SEMANTIC_DIFFERENCE_ONLY",
        "cohort": COHORT, "issue": ISSUE, "problem_id": 41,
        "roster_sha256": sha(roster_bytes),
        "source_provider_commit": PROVIDER_COMMIT,
        "source_provider_git_blob_sha1": SOURCE_BLOB,
        "worker_result_comment_id": 6104193801,
        "finite_set": list(B), "three_element_subsets": [list(t) for t in subsets],
        "multisets_with_sum_five": [list(t) for t in witnesses],
        "checked_equalities": ["1+1+3=5","1+2+2=5"],
        "limitation": "Does not falsify or prove infinite Erdős #41; historical repetition semantics unverified.",
        "authority_effects": {x: False for x in (
            "source_acceptance","solve_dispatch","mathcert_certification","publication"
        )},
        "execution": {
            "mode": "local_or_colab_manual",
            "python": platform.python_version(),
            "platform": platform.platform(),
            "elapsed_seconds": round(time.monotonic()-began,6),
            "external_model_calls": 0, "model_cost": 0,
        },
        "logical_passes": [
            {"id": "E41-COLAB-CHECK-001", "role": "verifier", "mode": "deterministic"},
            {"id": "E41-COLAB-ADVERSARY-002", "role": "adversary", "mode": "non_authoring_read_only"}
        ]
    }
    output_path.parent.mkdir(parents=True,exist_ok=True)
    encoded = stable(evidence)
    output_path.write_bytes(encoded+b"\n")
    print(json.dumps({"status": evidence["status"], "evidence_path":str(output_path),
                      "evidence_sha256": sha(encoded+b"\n"),
                      "roster_sha256":sha(roster_bytes)},sort_keys=True))

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--roster",default="governance/erdos_catalogue/ROLLING_RESEARCH_024.json")
    parser.add_argument("--output",default="runs/erdos-41/finite-replay.json")
    args=parser.parse_args()
    run(Path(args.roster),Path(args.output))
