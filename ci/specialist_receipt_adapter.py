#!/usr/bin/env python3
"""Verify candidate specialist evidence against protected domain authority.

Not a theorem prover, permission grant or claim-promotion controller. Only
previously admitted records on domain-authorized protected main may count.
Missing/ambiguous/incorrect authority fails closed. Caller owns enforcement.
"""
from __future__ import annotations
import base64
import hashlib
import json
import re
import urllib.parse
from typing import Any, Callable

from specialist_domains import REPOSITORY as REPO, load_domains

SHA = re.compile(r"[0-9a-f]{40}\\Z")
PREFIX = "governance/material_admission_receipts/"
RECORD_TYPE = "GCL_PROTECTED_SPECIALIST_ADMISSION_EVIDENCE"


class ReceiptError(ValueError):
    pass


def _sha(value: object) -> str:
    if not isinstance(value, str) or not SHA.fullmatch(value):
        raise ReceiptError("missing exact SHA-1 identity")
    return value


def material_fingerprint(files: list[dict[str, Any]]) -> str:
    """Canonical full GitHub manifest; cannot be selected by candidate PR text."""
    if not files or len(files) > 100:
        raise ReceiptError("unknown or truncated file list")
    out = []
    for f in files:
        path = f.get("filename")
        status = f.get("status")
        if not isinstance(path, str) or not path or "\x00" in path or path.startswith("/"):
            raise ReceiptError("invalid path")
        if status not in ("modified", "added", "removed", "renamed"):
            raise ReceiptError("unrecognized file modification")
        if f.get("previous_filename") and status != "renamed":
            raise ReceiptError("inconsistent renaming evidence")
        sha = f.get("sha")
        if status != "removed":
            sha = _sha(sha)
        elif sha is not None:
            sha = _sha(sha)
        out.append({"path": path, "status": status,
                    "blob_sha": sha or "", "previous_filename": f.get("previous_filename") or ""})
    if len(set(x["path"] for x in out)) != len(out):
        raise ReceiptError("duplicate changed-file paths")
    payload = json.dumps(sorted(out, key=lambda x: x["path"]), sort_keys=True,
                         separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest()


def _protected_json(
    api_get: Callable[[str], Any], repository: str, path: str, revision: str
) -> tuple[dict, str]:
    if not path or path.startswith("/") or ".." in path.split("/") or not path.endswith(".json"):
        raise ReceiptError("unsupported protected record path")
    record_url = f"/repos/{repository}/contents/{urllib.parse.quote(path, safe='/')}?ref={_sha(revision)}"
    item = api_get(record_url)
    if not isinstance(item, dict) or item.get("type") != "file" or item.get("encoding") != "base64":
        raise ReceiptError("protected record not a GitHub blob")
    blob = _sha(item.get("sha"))
    try:
        # GitHub Contents API wraps base64 with newlines. Only strip
        # canonical line breaks; reject other invalid encoded bytes.
        encoded = item["content"]
        if not isinstance(encoded, str):
            raise ReceiptError("GitHub content encoding is not text")
        content = base64.b64decode(encoded.replace("\n", "").replace("\r", ""), validate=True)
        record = json.loads(content)
    except (KeyError, ValueError, TypeError) as err:
        raise ReceiptError("protected record content invalid") from err
    if not isinstance(record, dict):
        raise ReceiptError("protected receipt is not an object")
    return record, blob


def _verify_review_origin(
    api_get: Callable[[str], Any], repository: str,
    proof_path: str, proof_blob: str, proof_record: dict,
    reviewer: str, candidate_author: str,
) -> dict[str, Any]:
    """Verify the stated reviewer actually approved the exact domain evidence.

    GitHub approval corroborates record provenance; it never substitutes for
    the mathematical/domain review represented by that separately protected
    evidence.
    """
    anchor = proof_record.get("review_anchor")
    if not isinstance(anchor, dict):
        raise ReceiptError("missing authenticated source review anchor")
    n = anchor.get("source_pr_number")
    r_id = anchor.get("review_id")
    if type(n) is not int or n <= 0 or type(r_id) is not int or r_id <= 0:
        raise ReceiptError("invalid domain PR/review identifier")
    source_head = _sha(anchor.get("source_pr_head_sha"))
    if anchor.get("reviewer_login") != reviewer:
        raise ReceiptError("attested reviewer identity mismatch")
    prefix = f"/repos/{repository}/pulls/{n}"
    pr = api_get(prefix)
    if (not isinstance(pr, dict) or not pr.get("merged_at") or
            (pr.get("head") or {}).get("sha") != source_head or
            (pr.get("base") or {}).get("ref") != "main"):
        raise ReceiptError("source review PR not merged at exact reviewed head")
    author = ((pr.get("user") or {}).get("login") or "")
    if not author or author.casefold() == reviewer.casefold():
        raise ReceiptError("source PR author cannot act as own reviewer")
    if not isinstance(pr.get("changed_files"), int) or not 1 <= pr["changed_files"] < 100:
        raise ReceiptError("source PR changed-file count not bounded")
    changed = api_get(prefix + "/files?per_page=100")
    if not isinstance(changed, list) or len(changed) != pr["changed_files"]:
        raise ReceiptError("source PR exact file list missing or truncated")
    if not any(
        isinstance(item, dict) and item.get("filename") == proof_path
        and item.get("status") in ("added", "modified")
        and item.get("sha") == proof_blob for item in changed
    ):
        raise ReceiptError("reviewed domain PR does not contain evidence blob")
    reviews = api_get(prefix + "/reviews?per_page=100")
    if not isinstance(reviews, list) or len(reviews) >= 100:
        raise ReceiptError("domain PR review list missing or truncated")
    reviewer_reviews = [
        item for item in reviews if isinstance(item, dict)
        and (item.get("user") or {}).get("login") == reviewer
    ]
    if not reviewer_reviews:
        raise ReceiptError("no authenticated independent domain review")
    # The latest state of that reviewer is authoritative, not an old approval
    # followed by CHANGES_REQUESTED or DISMISSED.
    last = max(reviewer_reviews, key=lambda row: (row.get("submitted_at") or "", row.get("id") or 0))
    if (last.get("id") != r_id or last.get("state") != "APPROVED"
            or last.get("commit_id") != source_head):
        raise ReceiptError("domain review not approved on exact current source head")
    return {"source_pr_number": n, "source_pr_head_sha": source_head,
            "authenticated_review_id": r_id, "reviewer_login": reviewer}



def _verify_solve_integrity(
    api_get: Callable[[str], Any], repository: str, protected_head: str,
    receipt: dict, proof: dict, proof_path: str,
) -> dict[str, Any]:
    """Inspect actual protected capture -> replay -> adjudication evidence.

    Solve verifies execution fidelity and the disposition of a *provisional*
    result. Only Cert may turn a mathematical proof into a certified claim.
    """
    value = receipt.get("solve_execution")
    if not isinstance(value, dict) or proof.get("solve_execution") != value:
        raise ReceiptError("Solve execution evidence missing or scope mismatch")
    if set(value) != {
        "schema_version", "dispatch_id", "result_ref", "result_sha256",
        "capture", "replay", "adjudication", "claim_effects",
    } or value["schema_version"] != "1.0.0":
        raise ReceiptError("Solve execution binding schema invalid")
    for key in ("dispatch_id", "result_ref"):
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ReceiptError("Solve missing dispatch or result identity")
    result_sha = value.get("result_sha256")
    if not isinstance(result_sha, str) or not re.fullmatch(r"[a-f0-9]{64}", result_sha):
        raise ReceiptError("Solve result digest missing")
    no_claim = {
        "mathematical_claim_effect": False,
        "certification_effect": False,
        "publication_effect": False,
        "source_semantic_effect": False,
        "security_authority_effect": False,
    }
    if value.get("claim_effects") != no_claim:
        raise ReceiptError("Solve evidence attempted to promote claim or authority")
    bound = {}
    paths = []
    for name in ("capture", "replay", "adjudication"):
        ref = value.get(name)
        if not isinstance(ref, dict) or set(ref) != {"path", "blob_sha"}:
            raise ReceiptError("Solve missing exact capture/replay/adjudication source lock")
        path = ref.get("path")
        if not isinstance(path, str) or not path.startswith("contributions/") or not path.endswith(".json"):
            raise ReceiptError("Solve evidence not under protected contributions")
        if path == proof_path or path in paths:
            raise ReceiptError("Solve evidence self-reference or duplicate")
        paths.append(path)
        locked = _sha(ref.get("blob_sha"))
        document, actual_blob = _protected_json(api_get, repository, path, protected_head)
        if actual_blob != locked:
            raise ReceiptError("Solve evidence source lock changed")
        if document.get("dispatch_id") != value["dispatch_id"] or document.get("result_ref") != value["result_ref"]:
            raise ReceiptError("Solve dispatch/return lineage mismatch")
        bound[name] = document
    captured, replayed, adjudicated = (bound[name] for name in ("capture", "replay", "adjudication"))
    if (captured.get("record_type") != "GCL_SOLVE_CAPTURE_RECEIPT_V1" or
            captured.get("result_sha256") != result_sha):
        raise ReceiptError("Solve capture digest or type is not verified")
    if (replayed.get("record_type") != "GCL_SOLVE_REPLAY_RECEIPT_V1" or
            replayed.get("input_result_sha256") != result_sha or
            replayed.get("capture_blob_sha") != value["capture"]["blob_sha"] or
            replayed.get("replay_pass") is not True):
        raise ReceiptError("Solve replay does not independently bind captured input")
    if (adjudicated.get("record_type") != "GCL_SOLVE_ADJUDICATION_RECEIPT_V1" or
            adjudicated.get("replay_blob_sha") != value["replay"]["blob_sha"] or
            adjudicated.get("adjudication_disposition") != "REPLAYED_AND_ADJUDICATED" or
            not isinstance(adjudicated.get("adjudication_id"), str) or
            not adjudicated["adjudication_id"].strip() or
            adjudicated.get("claim_effects") != no_claim):
        raise ReceiptError("Solve adjudication invalid or attempted claim promotion")
    return {
        "domain": "SOLUTION_INTEGRITY",
        "dispatch_id": value["dispatch_id"],
        "result_ref": value["result_ref"],
        "result_sha256": result_sha,
        "capture_blob_sha": value["capture"]["blob_sha"],
        "replay_blob_sha": value["replay"]["blob_sha"],
        "adjudication_blob_sha": value["adjudication"]["blob_sha"],
        "adjudication_id": adjudicated["adjudication_id"],
        "claim_effects": no_claim,
        "mathematical_certification": False,
    }


def protected_specialist_receipt(
    *, head: str, files: list[dict], domain: str,
    api_get: Callable[[str], Any], candidate_author: str,
) -> dict[str, Any]:
    """Verify a bound domain receipt; never accept one from the candidate branch.

    The returned finding recognizes protected-review evidence only. Its truth
    remains within the domain owner's previously adjudicated claim scope.
    """
    _sha(head)
    if not isinstance(candidate_author, str) or not candidate_author.strip():
        raise ReceiptError("missing attributable candidate author")
    domains = load_domains()
    if domain not in domains:
        raise ReceiptError("unknown specialist domain")
    route = domains[domain]
    owner, evidence_prefix = route["repository"], route["evidence_prefix"]
    fingerprint = material_fingerprint(files)
    ref = api_get(f"/repos/{owner}/git/ref/heads/main")
    protected_sha = _sha(((ref or {}).get("object") or {}).get("sha"))
    name = f"{PREFIX}MATH-PROGRAMME-{head}.json"
    record, receipt_blob = _protected_json(api_get, owner, name, protected_sha)
    if (record.get("schema_version"), record.get("record_type"),
        record.get("authority_domain"), record.get("source_repository")) != (
        "1.0.0", RECORD_TYPE, domain, owner,
    ):
        raise ReceiptError("domain or schema not authoritative")
    target = record.get("subject") or {}
    if (target.get("repository"), target.get("head_sha"), target.get("material_fingerprint")) != (
        REPO, head, fingerprint,
    ):
        raise ReceiptError("specialist evidence does not bind candidate material")
    if record.get("verdict") != "ADMISSIBLE_FOR_PROTECTED_ADMISSION":
        raise ReceiptError("specialist did not issue positive admissibility")
    proof = record.get("protected_evidence") or {}
    p = proof.get("path")
    if not isinstance(p, str) or not p.startswith(evidence_prefix):
        raise ReceiptError("domain evidence has wrong source path")
    _sha(proof.get("blob_sha"))
    if proof.get("path") == name:
        raise ReceiptError("self-referential receipt")
    proof_record, proof_blob = _protected_json(api_get, owner, p, protected_sha)
    if proof_blob != proof["blob_sha"]:
        raise ReceiptError("protected underlying evidence byte identity drift")
    # The receipt must not point to an unrelated protected JSON object.
    # A second, independently admitted review artifact has to bind the exact
    # candidate bytes and the same domain with a positive scoped disposition.
    expected_disposition = (
        "ROLE_SCOPED_REVIEW_ACCEPTED" if domain == "SOLUTION_INTEGRITY"
        else "INDEPENDENT_REVIEW_ACCEPTED"
    )
    if (proof_record.get("record_type") != route["review_record_type"] or
            proof_record.get("authority_domain") != domain or
            proof_record.get("subject_repository") != REPO or
            proof_record.get("subject_sha") != head or
            proof_record.get("material_fingerprint") != fingerprint or
            proof_record.get("disposition") != expected_disposition):
        raise ReceiptError("underlying specialist review not positively bound")
    reviewer = proof_record.get("reviewer_identity")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ReceiptError("independent reviewer identity not attested")
    if reviewer.casefold() == candidate_author.casefold():
        raise ReceiptError("candidate author cannot be sole specialist reviewer")
    declared_independence = proof_record.get("review_independence")
    expected_independence = route["independence"]
    if declared_independence != expected_independence:
        raise ReceiptError("required specialist-review independence not attested")
    if not isinstance(record.get("review_scope"), str) or not record["review_scope"].strip():
        raise ReceiptError("missing specialist-reviewed claim/scope")
    if record["review_scope"] != proof_record.get("review_scope"):
        raise ReceiptError("specialist reviewed scope differs from receipt")
    solve_evidence = None
    if domain == "SOLUTION_INTEGRITY":
        if record["review_scope"] != route["review_scope"]:
            raise ReceiptError("Solve review must be execution integrity only")
        solve_evidence = _verify_solve_integrity(
            api_get, owner, protected_sha, record, proof_record, p,
        )
    origin = _verify_review_origin(
        api_get, owner, p, proof_blob, proof_record, reviewer, candidate_author,
    )
    # Reconfirm current protected branch has not moved during retrieval.
    now = api_get(f"/repos/{owner}/git/ref/heads/main")
    if _sha(((now or {}).get("object") or {}).get("sha")) != protected_sha:
        raise ReceiptError("specialist source main moved during verification")
    return {
        "disposition": "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED",
        "source_repository": owner,
        "protected_commit_sha": protected_sha,
        "protected_receipt_path": name,
        "protected_receipt_blob": receipt_blob,
        "protected_underlying_blob": proof_blob,
        "domain": domain,
        "review_scope": record["review_scope"],
        "solve_execution_evidence": solve_evidence,
        "authenticated_review_origin": origin,
        "subject_sha": head,
        "material_fingerprint": fingerprint,
        "authority": {
            "independent_scientific_validation_performed_by_this_controller": False,
            "new_certification_created": False,
            "github_approval_created": False,
            "substantive_review_replaced": False,
        },
    }
