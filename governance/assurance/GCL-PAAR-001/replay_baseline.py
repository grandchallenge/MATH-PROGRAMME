#!/usr/bin/env python3
"""GCL-PAAR-001 bounded snapshot consistency and optionally authenticated live blobs.

Offline mode never confers source authenticity; live mode checks exact pinned
GitHub artifacts but does not assert estate-wide governance enforcement.
"""
from __future__ import annotations
import argparse
import copy
import json
import re
import subprocess
from pathlib import Path

B = Path(__file__).resolve().parent
EXPECTED = {"CONTROL", "MATH-PROGRAMME", "MATHSOLVE", "MATHCERT", "INTELLECT", "MATHFORGE"}


def demand(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def verify_snapshot(a: dict) -> dict:
    demand(a.get("record_type") == "GCL_ASSERTION_ASSURANCE_BOUNDED_BASELINE/1",
           "record type changed")
    demand(a.get("workstream_id") == "GCL-PAAR-001", "workstream identity changed")
    repos = a.get("repository_readbacks")
    demand(isinstance(repos, dict) and set(repos) == EXPECTED,
           "repository population differs")
    total = 0
    for name, row in repos.items():
        demand(row.get("repository") == "grandchallenge/" + name, "repository identity")
        demand(row.get("protected_main") is True, "protection observation missing")
        sha = row.get("protected_main_sha", "")
        demand(re.fullmatch("[0-9a-f]{40}", sha) is not None, "head invalid")
        files = row.get("files", [])
        demand(len(files) >= 1 and len({f["path"] for f in files}) == len(files),
               "missing or duplicate blob sources")
        for f in files:
            demand(re.fullmatch("[0-9a-f]{40}", f.get("git_blob_sha1", "")) is not None,
                   "blob missing")
            demand(f.get("size_bytes", 0) > 0, "empty control")
            demand(f.get("immutable_url") ==
                   "https://github.com/grandchallenge/" + name + "/blob/" +
                   sha + "/" + f["path"], "immutable URL mismatch")
            total += 1
    demand(total == 14, "sampled control population changed")
    p = a.get("sampled_operational_case", {})
    demand(p.get("source_repository_head") ==
           repos["MATH-PROGRAMME"]["protected_main_sha"], "operational head mismatch")
    demand(p.get("source_return_count") == 168 and
           p.get("original_project_returned_count") == 168 and
           p.get("outstanding_available_label_count") == 0,
           "sampled source lifecycle contradiction")
    demand(p.get("protected_public_unaccepted_drafts") == 168 and
           p.get("live_browser_pages_passed") == 173 and
           p.get("live_math_expressions_rendered") == 2807,
           "sampled public evidence mismatch")
    demand(p.get("ec007_v2_count") == 0 and
           p.get("independent_critical_reviews_approved") == 0,
           "unsupported status promotion")
    demand(a.get("integrity_disposition") ==
           "EXISTING_INVARIANT_PARTIALLY_CONFIRMED__ESTATE_WIDE_ASSURANCE_REMAINS_OPEN",
           "unsupported full assurance status")
    e = a.get("governance_effects", {})
    demand(all(e.get(k) == 0 for k in
               ["state_mutations", "certifications", "review_approvals",
                "admission_changes", "new_enforcement_policies"]),
           "unjustified governance effect")
    return {"repositories": len(repos), "pinned_files": total,
            "sampled_returned": 168, "sampled_public_unaccepted": 168,
            "estate_wide_certified": False}


def hostile_controls(obj: dict) -> int:
    cases = []
    bad = copy.deepcopy(obj)
    bad["repository_readbacks"]["INTELLECT"]["files"][0]["git_blob_sha1"] = "0" * 39
    cases.append(bad)
    bad = copy.deepcopy(obj)
    bad["sampled_operational_case"]["ec007_v2_count"] = 168
    cases.append(bad)
    bad = copy.deepcopy(obj)
    bad["sampled_operational_case"]["source_repository_head"] = "0" * 40
    cases.append(bad)
    bad = copy.deepcopy(obj)
    bad["integrity_disposition"] = "ESTATE_WIDE_CERTIFIED"
    cases.append(bad)
    for case in cases:
        try:
            verify_snapshot(case)
        except ValueError:
            continue
        raise AssertionError("offline receipt negative control incorrectly accepted")
    return len(cases)


def call_gh(path: str) -> dict:
    result = subprocess.run(["gh", "api", path], text=True, capture_output=True,
                            timeout=30, check=True)
    return json.loads(result.stdout)


def enforce_native_review_requirement(rules: object, minimum: int = 1) -> int:
    """Fail closed unless effective branch rules require nonauthor GitHub review.

    This validates only the native GitHub review count, not the scientific
    or logical independence of the reviewer or the adequacy of its findings.
    """
    demand(isinstance(rules, list), "effective branch rules missing")
    counts = []
    for r in rules:
        if not isinstance(r, dict) or r.get("type") != "pull_request":
            continue
        parameters = r.get("parameters")
        if not isinstance(parameters, dict):
            continue
        count = parameters.get("required_approving_review_count")
        if type(count) is int and count >= 0:
            counts.append(count)
    demand(counts and max(counts) >= minimum,
           "INTELLECT lacks mandatory native nonauthor approving review")
    return max(counts)


def verify_live(a: dict) -> dict:
    observed = {}
    for name, row in a["repository_readbacks"].items():
        base = "repos/grandchallenge/" + name
        current = call_gh(base + "/branches/main")
        demand(current["protected"] is True, name + " current main unprotected")
        current_sha = current["commit"]["sha"]
        count = 0
        for f in row["files"]:
            d = call_gh(base + "/contents/" + f["path"] + "?ref=" +
                        row["protected_main_sha"])
            demand(d.get("sha") == f["git_blob_sha1"], name + ": blob drift " + f["path"])
            count += 1
        observed[name] = {"protected": True, "pinned_artifacts_reverified": count,
                          "head_current": current_sha,
                          "head_changed_since_snapshot": current_sha != row["protected_main_sha"]}
        if name == "INTELLECT":
            effective = call_gh(base + "/rules/branches/main")
            observed[name]["required_native_approving_reviews"] = (
                enforce_native_review_requirement(effective))
    return observed


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--offline", action="store_true")
    group.add_argument("--live", action="store_true")
    args = parser.parse_args()
    obj = json.loads((B / "AUDIT_BASELINE.json").read_text(encoding="utf-8"))
    passed = verify_snapshot(obj)
    negatives = hostile_controls(obj)
    output = {"record_type": "GCL_PAAR_001_ASSURANCE_REPLAY_RESULT/1",
              "result": "PASS_BOUNDED_ONLY", "source": "AUDIT_BASELINE.json",
              "offline_positive": passed, "hostile_snapshot_controls_rejected": negatives,
              "global_integrity_certified": False,
              "record_authority": "SAMPLED_AUDIT_EVIDENCE_NOT_GOVERNANCE_CERTIFICATION"}
    if args.live:
        output["authenticated_exact_source_readback"] = verify_live(obj)
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
