"""GCL-ARC-001 PROTECTION-only acyclic agent role review consumer.

The dossier is committed and protected BEFORE the separate receipt refers to
the known source PR head. A shared transport account is not a specialist role.
"""
from __future__ import annotations
import hashlib
import re

ORIGIN = "grandchallenge/INTELLECT"
PASS_ROLES = ("VERIFIER", "ADVERSARY", "REFEREE")
CHECKS = {"test (3.11.14)", "test (3.12.13)", "policy / policy",
          "security / action-policy", "routing-enforcement"}


# Exact historical GCL-ARC-001 receipt admitted before executable output was
# made part of the protected consumer contract. No new V1 receipts are allowed.
LEGACY_V1 = {
    "subject_head": "e577477b656c6865698d5dbc18962e2810f53a26",
    "material_sha256": "e8254dbd487e59529d64e67b7832066cb4ff3a5437421e7b073b3effdd4822f0",
    "receipt_blob": "9e9d5448034a552afbeff838e63d302a1ad324f2",
    "dossier_blob": "4b3d108922ed9cf345d6407d81a216a93da697c1",
    "source_pr": 121,
    "source_head": "69f89aa56c373a5978e58740fb60a9a2e6b32a3d",
}
NEW_RECEIPT = "GCL_PROTECTED_AGENT_ROLE_ADMISSION_EVIDENCE_V2"
NEW_DOSSIER = "GCL_AGENT_REVIEW_DOSSIER_V2"
EXECUTION_RECORD = "GCL_PROTECTED_ROLE_EXECUTION_OUTPUT_V1"


class AgentRoleError(ValueError):
    pass


def demand(ok, reason):
    if not ok:
        raise AgentRoleError(reason)


def verify_execution_output(*, check, specialist_pass, index, subject,
                            read_protected_json, protected_sha):
    """Reconcile protected output bytes; do not equate matching output with actual execution."""
    role = specialist_pass["role"]
    path = ("governance/agent_execution/executions/"
            f"MATH-PROGRAMME-{subject['head_sha']}/{role.lower()}-{index}.json")
    ref = check.get("execution_evidence")
    demand(isinstance(ref, dict) and set(ref) == {"path", "blob_sha"}
           and ref.get("path") == path
           and isinstance(ref.get("blob_sha"), str)
           and re.fullmatch(r"[a-f0-9]{40}", ref["blob_sha"]),
           "execution evidence path or blob missing")
    execution, actual_blob = read_protected_json(ORIGIN, path, protected_sha)
    demand(actual_blob == ref["blob_sha"], "execution evidence protected blob drift")
    demand(isinstance(execution, dict)
           and execution.get("record_type") == EXECUTION_RECORD
           and execution.get("subject") == subject
           and execution.get("role") == role
           and execution.get("logical_pass_id") == specialist_pass["logical_pass_id"]
           and execution.get("reviewer_system_id") == specialist_pass["reviewer_system_id"]
           and execution.get("transport_login") == specialist_pass["transport_login"]
           and execution.get("mode") == "non_authoring_read_only"
           and execution.get("command") == check["command"]
           and type(execution.get("exit_code")) is int
           and execution.get("exit_code") == check["exit_code"]
           and execution.get("finding") == "PASS",
           "protected execution identity, scope or result mismatch")
    environment = execution.get("environment")
    demand(isinstance(environment, dict)
           and all(isinstance(environment.get(k), str) and environment[k].strip()
                   for k in ("python", "os", "toolchain")),
           "execution toolchain provenance incomplete")
    time = execution.get("observed_utc")
    demand(isinstance(time, str) and re.fullmatch(
           r"20[0-9]{2}-[01][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]Z", time),
           "execution UTC observation missing")
    output = execution.get("output")
    demand(isinstance(output, dict) and set(output) == {"stdout", "stderr", "selected_stream"}
           and output.get("selected_stream") in ("stdout", "stderr")
           and isinstance(output.get("stdout"), str)
           and isinstance(output.get("stderr"), str),
           "protected execution output missing or malformed")
    demand(all(len(output[k].encode("utf-8")) <= 131072 for k in ("stdout", "stderr"))
           and len(output[output["selected_stream"]].encode("utf-8")) > 0,
           "protected execution output empty or oversized")
    digest = hashlib.sha256(output[output["selected_stream"]].encode("utf-8")).hexdigest()
    demand(digest == check["receipt_sha256"],
           "declared command digest does not match protected raw output")
    return {"path": path, "blob_sha": actual_blob, "receipt_sha256": digest}


def demand_native_source_review(api_get, *, url, source_head, source_author):
    """Require current nonauthor GitHub APPROVED review on exact source PR head."""
    reviews = api_get(url + "/reviews?per_page=100")
    demand(isinstance(reviews, list) and len(reviews) < 100,
           "source PR review history missing or truncated")
    latest = {}
    for review in reviews:
        if not isinstance(review, dict):
            continue
        reviewer = (review.get("user") or {}).get("login")
        if not isinstance(reviewer, str) or not reviewer.strip():
            continue
        key = reviewer.casefold()
        prior = latest.get(key)
        rank = lambda item: (item.get("submitted_at") or "", item.get("id") or 0)
        if prior is None or rank(review) > rank(prior):
            latest[key] = review
    passed = [row for name, row in latest.items()
              if name != source_author.casefold()
              and row.get("state") == "APPROVED"
              and row.get("commit_id") == source_head]
    demand(bool(passed), "no current nonauthor native approval on source PR head")
    return sorted(row["user"]["login"] for row in passed)


def verify_agent_role_receipt(*, receipt, receipt_path, receipt_blob,
                              read_protected_json, api_get, protected_sha,
                              subject_head, material_digest, actual_actor):
    subject = {"repository": "grandchallenge/MATH-PROGRAMME",
               "head_sha": subject_head, "material_sha256": material_digest}
    record_type = receipt.get("record_type")
    legacy = record_type == "GCL_PROTECTED_AGENT_ROLE_ADMISSION_EVIDENCE_V1"
    modern = record_type == NEW_RECEIPT
    demand((legacy or modern)
           and receipt.get("schema_version") == ("2.0.0" if legacy else "3.0.0")
           and receipt.get("source_repository") == ORIGIN
           and receipt.get("authority_domain") == "PROTECTION"
           and receipt.get("subject") == subject
           and receipt.get("verdict") == "ADMISSIBLE_FOR_PROTECTED_ADMISSION",
           "source authority or subject mismatch")
    proof = receipt.get("protected_evidence") or {}
    path = f"governance/agent_execution/reviews/MATH-PROGRAMME-{subject_head}.json"
    demand(proof.get("path") == path and path != receipt_path,
           "protected dossier path mismatch")
    blob = proof.get("blob_sha")
    demand(isinstance(blob, str) and re.fullmatch(r"[a-f0-9]{40}", blob),
           "invalid protected dossier blob")
    dossier, actual_blob = read_protected_json(ORIGIN, path, protected_sha)
    demand(actual_blob == blob, "dossier byte identity drift")
    if legacy:
        demand((subject_head, material_digest, receipt_blob, blob) == (
            LEGACY_V1["subject_head"], LEGACY_V1["material_sha256"],
            LEGACY_V1["receipt_blob"], LEGACY_V1["dossier_blob"]),
            "new unverified legacy V1 role evidence forbidden")
    demand(dossier.get("record_type") == (
               "GCL_AGENT_REVIEW_DOSSIER_V1" if legacy else NEW_DOSSIER)
           and dossier.get("subject") == subject
           and dossier.get("work_class") == "MATERIAL_CONTROL"
           and dossier.get("transport_login") == actual_actor,
           "dossier identity or review scope changed")
    demand(dossier.get("claimed_effects") == {
        "mathematical_certification": False,
        "reserved_authorization": False,
        "credential_escalation": False}, "agent review claimed reserved authority")
    demand(not any(x in dossier for x in (
        "review_anchor", "source_pr_head_sha", "source_pr_review_id", "own_commit_sha")),
        "self-referential source PR metadata")
    passes = dossier.get("passes")
    demand(isinstance(passes, list) and len(passes) == 3
           and [p.get("role") if isinstance(p, dict) else None for p in passes]
           == list(PASS_ROLES), "ordered logical specialist passes required")
    ids = set()
    verified_execution_outputs = []
    for p in passes:
        ident = p.get("logical_pass_id")
        demand(isinstance(ident, str) and ident.strip() and ident not in ids,
               "duplicate or absent logical pass ID")
        ids.add(ident)
        demand(isinstance(p.get("reviewer_system_id"), str)
               and p["reviewer_system_id"].strip()
               and p.get("transport_login") == actual_actor
               and p.get("subject_head_sha") == subject_head
               and p.get("mode") == "non_authoring_read_only"
               and p.get("write_set") == []
               and isinstance(p.get("read_set"), list) and p["read_set"],
               "review role, immutable source, or read-only gate failed")
        demand(p.get("finding") == "ACCEPT_BOUNDED" and p.get("unresolved") == [],
               "unresolved expert objection")
        checks = p.get("checks")
        demand(isinstance(checks, list) and checks, "no specialist check evidence")
        for index, c in enumerate(checks):
            demand(isinstance(c, dict)
                   and isinstance(c.get("command"), str) and c["command"].strip()
                   and type(c.get("exit_code")) is int and c["exit_code"] == 0
                   and isinstance(c.get("receipt_sha256"), str)
                   and re.fullmatch(r"[a-f0-9]{64}", c["receipt_sha256"]),
                   "failed or missing specialist test receipt")
            if modern:
                verified_execution_outputs.append(verify_execution_output(
                    check=c, specialist_pass=p, index=index, subject=subject,
                    read_protected_json=read_protected_json,
                    protected_sha=protected_sha))
        if p["role"] == "ADVERSARY":
            demand(isinstance(p.get("negative_controls"), list)
                   and p["negative_controls"], "no hostile negative controls")
    anchor = receipt.get("source_review_anchor") or {}
    n, head = anchor.get("source_pr_number"), anchor.get("source_pr_head_sha")
    demand(type(n) is int and n > 0 and isinstance(head, str)
           and re.fullmatch(r"[a-f0-9]{40}", head)
           and anchor.get("review_dossier_blob_sha") == blob,
           "later receipt does not bind known source review")
    if legacy:
        demand(n == LEGACY_V1["source_pr"] and head == LEGACY_V1["source_head"],
               "legacy source review outside exact historical allowlist")
    url = f"/repos/{ORIGIN}/pulls/{n}"
    pr = api_get(url)
    demand(isinstance(pr, dict) and pr.get("merged_at")
           and (pr.get("head") or {}).get("sha") == head
           and (pr.get("base") or {}).get("ref") == "main"
           and type(pr.get("changed_files")) is int
           and 0 < pr["changed_files"] < 100, "source PR not protected merged")
    source_author = ((pr.get("user") or {}).get("login") or "")
    if modern:
        demand(bool(source_author), "protected source PR author missing")
        native_reviewers = demand_native_source_review(
            api_get, url=url, source_head=head, source_author=source_author)
    else:
        native_reviewers = []
    changes = api_get(url + "/files?per_page=100")
    demand(isinstance(changes, list) and len(changes) == pr["changed_files"]
           and any(f.get("filename") == path and f.get("sha") == blob
                   and f.get("status") in ("added", "modified") for f in changes),
           "source PR did not introduce exact dossier")
    if modern:
        demand(all(any(
            isinstance(f, dict) and f.get("filename") == x["path"]
            and f.get("sha") == x["blob_sha"]
            and f.get("status") in ("added", "modified") for f in changes
        ) for x in verified_execution_outputs),
        "reviewed source PR did not introduce exact execution outputs")
    data = api_get(f"/repos/{ORIGIN}/commits/{head}/check-runs?per_page=100")
    runs = data.get("check_runs") if isinstance(data, dict) else None
    demand(isinstance(runs, list) and data.get("total_count", 101) <= 100,
           "protected source check history incomplete")
    for name in CHECKS:
        demand(any(c.get("name") == name and c.get("conclusion") == "success"
                   and c.get("head_sha") == head for c in runs),
               "missing actual protected source check: " + name)
    ref = api_get(f"/repos/{ORIGIN}/git/ref/heads/main")
    demand(((ref or {}).get("object") or {}).get("sha") == protected_sha,
           "source branch moved during readback")
    return {
        "disposition": "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED",
        "source_repository": ORIGIN,
        "protected_commit_sha": protected_sha,
        "protected_receipt_path": receipt_path,
        "protected_receipt_blob": receipt_blob,
        "protected_underlying_blob": blob,
        "domain": "PROTECTION",
        "review_scope": "SECURITY_AND_GOVERNANCE_REVIEW",
        "subject_sha": subject_head,
        "material_fingerprint": material_digest,
        "execution_evidence": {
            "status": "EXACT_PROTECTED_OUTPUT_RECONCILED" if modern else
                      "HISTORICAL_LOCKED_V1_NO_CONSUMER_OUTPUT_CHECK",
            "protected_outputs": verified_execution_outputs,
            "native_source_reviewers": native_reviewers,
            "independent_execution_certified": False,
        },
        "authenticated_review_origin": {
            "source_pr_number": n, "source_pr_head_sha": head,
            "review_dossier_blob_sha": blob,
            "agent_roles_verified": list(PASS_ROLES),
            "mechanical_trust": "protected source CI and main merge",
            "github_user_multiplication_required": False
        },
        "authority": {
            "independent_scientific_validation_performed_by_this_controller": False,
            "new_certification_created": False,
            "github_approval_created": False,
            "substantive_review_replaced": False
        }
    }
