#!/usr/bin/env python3
"""PAAR-C: sandbox-only audit of GCL-ARC-001 role receipt acceptance boundaries.

All GitHub API responses here are synthetic mocks. The test never performs
network writes, claims a genuine review, or promotes a production assertion.
"""
from __future__ import annotations
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "ci"))
from agent_role_receipt import CHECKS, AgentRoleError, verify_agent_role_receipt

H = "a" * 40
SOURCE = "b" * 40
BLOB = "c" * 40
SUBJECT = "d" * 40
MATERIAL = "e" * 64
ACTOR = "fyremael"
PATH = f"governance/agent_execution/reviews/MATH-PROGRAMME-{SUBJECT}.json"
RECEIPT_PATH = f"governance/specialist_receipts/MATH-PROGRAMME-{SUBJECT}.json"

subject = {"repository": "grandchallenge/MATH-PROGRAMME",
           "head_sha": SUBJECT, "material_sha256": MATERIAL}

def fixture():
    passes = []
    for idx, role in enumerate(("VERIFIER", "ADVERSARY", "REFEREE")):
        row = {
            "role": role,
            "logical_pass_id": f"PAAR-TEST-{role}-{idx}",
            "reviewer_system_id": "GPT-6",
            "transport_login": ACTOR,
            "subject_head_sha": SUBJECT,
            "mode": "non_authoring_read_only",
            "read_set": ["synthetic-test-input"],
            "write_set": [],
            "finding": "ACCEPT_BOUNDED",
            "unresolved": [],
            "checks": [{"command": "nonexecuted-example-command", "exit_code": 0,
                        "receipt_sha256": hashlib.sha256(f"{role}-example".encode()).hexdigest()}]
        }
        if role == "ADVERSARY":
            row["negative_controls"] = ["synthetic-negative-control"]
        passes.append(row)
    dossier = {
        "record_type": "GCL_AGENT_REVIEW_DOSSIER_V1",
        "subject": subject,
        "work_class": "MATERIAL_CONTROL",
        "transport_login": ACTOR,
        "claimed_effects": {"mathematical_certification": False,
                            "reserved_authorization": False,
                            "credential_escalation": False},
        "passes": passes
    }
    receipt = {
        "schema_version": "2.0.0",
        "record_type": "GCL_PROTECTED_AGENT_ROLE_ADMISSION_EVIDENCE_V1",
        "source_repository": "grandchallenge/INTELLECT",
        "authority_domain": "PROTECTION",
        "subject": subject,
        "verdict": "ADMISSIBLE_FOR_PROTECTED_ADMISSION",
        "protected_evidence": {"path": PATH, "blob_sha": BLOB},
        "source_review_anchor": {"source_pr_number": 1,
                                 "source_pr_head_sha": H,
                                 "review_dossier_blob_sha": BLOB}
    }
    return dossier, receipt

def execute(dossier, receipt, *, branch_sha=SOURCE, checks_green=True, source_author=ACTOR):
    touched = []
    def api_get(url):
        touched.append(url)
        prefix = "/repos/grandchallenge/INTELLECT/pulls/1"
        if url == prefix:
            return {"merged_at": "2026-10-15T00:00:00Z",
                    "head": {"sha": H}, "base": {"ref": "main"},
                    "changed_files": 1, "user": {"login": source_author}}
        if url == prefix + "/files?per_page=100":
            return [{"filename": PATH, "sha": BLOB, "status": "added"}]
        if url == f"/repos/grandchallenge/INTELLECT/commits/{H}/check-runs?per_page=100":
            return {"total_count": len(CHECKS),
                    "check_runs": [{"name": k, "conclusion": "success" if checks_green else "failure",
                                    "head_sha": H} for k in CHECKS]}
        if url == "/repos/grandchallenge/INTELLECT/git/ref/heads/main":
            return {"object": {"sha": branch_sha}}
        # Explicitly no review endpoint is modeled; a request would fail.
        raise AssertionError("Unexpected or missing GitHub API call: " + url)
    try:
        result = verify_agent_role_receipt(
            receipt=receipt,
            receipt_path=RECEIPT_PATH,
            receipt_blob="f"*40,
            read_protected_json=lambda repo, path, revision: (dossier, BLOB),
            api_get=api_get,
            protected_sha=SOURCE,
            subject_head=SUBJECT,
            material_digest=MATERIAL,
            actual_actor=ACTOR
        )
        return {"accepted": True, "disposition": result["disposition"],
                "queried_native_pr_reviews": any("/reviews" in u for u in touched)}
    except AgentRoleError as exc:
        return {"accepted": False, "reason": str(exc),
                "queried_native_pr_reviews": any("/reviews" in u for u in touched)}

def main():
    d, r = fixture()
    results = {}
    results["synthetic_baseline"] = execute(d, r)
    bad = copy.deepcopy(d)
    bad["passes"][0]["subject_head_sha"] = "0"*40
    results["stale_pass_head"] = execute(bad, r)
    bad = copy.deepcopy(r)
    bad["protected_evidence"]["blob_sha"] = "0"*40
    results["mismatched_blob"] = execute(d, bad)
    results["failed_source_ci"] = execute(d, r, checks_green=False)
    bad = copy.deepcopy(d)
    for p in bad["passes"]:
        p["checks"] = [{"command": "never-run", "exit_code": 0,
                        "receipt_sha256": "0"*64}]
    results["fabricated_unverifiable_check_digests"] = execute(bad, r)
    results["no_source_pr_review_endpoint"] = execute(d, r)
    results["candidate_same_as_source_pr_author"] = execute(d, r, source_author=ACTOR)
    results["changed_source_branch"] = execute(d, r, branch_sha="0"*40)

    expected_negative = ["stale_pass_head", "mismatched_blob",
                         "failed_source_ci", "changed_source_branch"]
    assert results["synthetic_baseline"]["accepted"]
    assert all(not results[x]["accepted"] for x in expected_negative), results
    findings = {
        "record_type": "GCL_PAAR_001_BOUNDARY_OBSERVATION_V1",
        "source": "ci/agent_role_receipt.py at the caller's checkout",
        "method": "pure sandbox mocking trusted protected source/API boundary",
        "actual_authenticated_github_approval_created": False,
        "actual_protected_admission_created": False,
        "scope": "isolated consumer acceptance logic; not an end-to-end forged GitHub merge",
        "results": results,
        "gap_flags": {
            "unreproduced_check_digest_accepted_by_consumer": results["fabricated_unverifiable_check_digests"]["accepted"],
            "native_pr_review_not_queried_by_consumer": not results["no_source_pr_review_endpoint"]["queried_native_pr_reviews"]
        }
    }
    print(json.dumps(findings, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
