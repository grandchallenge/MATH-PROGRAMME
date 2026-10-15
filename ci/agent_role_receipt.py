"""GCL-ARC-001 PROTECTION-only acyclic agent role review consumer.

The dossier is committed and protected BEFORE the separate receipt refers to
the known source PR head. A shared transport account is not a specialist role.
"""
from __future__ import annotations
import re

ORIGIN = "grandchallenge/INTELLECT"
PASS_ROLES = ("VERIFIER", "ADVERSARY", "REFEREE")
CHECKS = {"test (3.11.14)", "test (3.12.13)", "policy / policy",
          "security / action-policy", "routing-enforcement"}


class AgentRoleError(ValueError):
    pass


def demand(ok, reason):
    if not ok:
        raise AgentRoleError(reason)


def verify_agent_role_receipt(*, receipt, receipt_path, receipt_blob,
                              read_protected_json, api_get, protected_sha,
                              subject_head, material_digest, actual_actor):
    subject = {"repository": "grandchallenge/MATH-PROGRAMME",
               "head_sha": subject_head, "material_sha256": material_digest}
    demand(receipt.get("schema_version") == "2.0.0" and
           receipt.get("record_type") == "GCL_PROTECTED_AGENT_ROLE_ADMISSION_EVIDENCE_V1"
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
    demand(dossier.get("record_type") == "GCL_AGENT_REVIEW_DOSSIER_V1"
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
        for c in checks:
            demand(isinstance(c, dict)
                   and isinstance(c.get("command"), str) and c["command"].strip()
                   and type(c.get("exit_code")) is int and c["exit_code"] == 0
                   and isinstance(c.get("receipt_sha256"), str)
                   and re.fullmatch(r"[a-f0-9]{64}", c["receipt_sha256"]),
                   "failed or missing specialist test receipt")
        if p["role"] == "ADVERSARY":
            demand(isinstance(p.get("negative_controls"), list)
                   and p["negative_controls"], "no hostile negative controls")
    anchor = receipt.get("source_review_anchor") or {}
    n, head = anchor.get("source_pr_number"), anchor.get("source_pr_head_sha")
    demand(type(n) is int and n > 0 and isinstance(head, str)
           and re.fullmatch(r"[a-f0-9]{40}", head)
           and anchor.get("review_dossier_blob_sha") == blob,
           "later receipt does not bind known source review")
    url = f"/repos/{ORIGIN}/pulls/{n}"
    pr = api_get(url)
    demand(isinstance(pr, dict) and pr.get("merged_at")
           and (pr.get("head") or {}).get("sha") == head
           and (pr.get("base") or {}).get("ref") == "main"
           and type(pr.get("changed_files")) is int
           and 0 < pr["changed_files"] < 100, "source PR not protected merged")
    changes = api_get(url + "/files?per_page=100")
    demand(isinstance(changes, list) and len(changes) == pr["changed_files"]
           and any(f.get("filename") == path and f.get("sha") == blob
                   and f.get("status") in ("added", "modified") for f in changes),
           "source PR did not introduce exact dossier")
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
