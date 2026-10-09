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

REPO = "grandchallenge/MATH-PROGRAMME"
SHA = re.compile(r"[0-9a-f]{40}\Z")
ROUTES = {
    "MATHEMATICAL": ("grandchallenge/MATHCERT", "certificates/"),
    "SOURCE_SEMANTIC": ("grandchallenge/MATHFORGE", "governance/"),
    "PROTECTION": ("grandchallenge/INTELLECT", "governance/"),
}
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
        # GitHub Contents API wraps RFC 4648 base64 with newlines. Only strip\n        # its canonical line breaks; reject every other invalid encoded byte.\n        encoded = item["content"]\n        if not isinstance(encoded, str):\n            raise ReceiptError("GitHub content encoding is not text")\n        content = base64.b64decode(encoded.replace("\\n", "").replace("\\r", ""), validate=True)
        record = json.loads(content)
    except (KeyError, ValueError, TypeError) as err:
        raise ReceiptError("protected record content invalid") from err
    if not isinstance(record, dict):
        raise ReceiptError("protected receipt is not an object")
    return record, blob


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
    if domain not in ROUTES:
        raise ReceiptError("unknown specialist domain")
    owner, evidence_prefix = ROUTES[domain]
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
    if (proof_record.get("record_type") != "GCL_DOMAIN_INDEPENDENT_REVIEW_V1" or
            proof_record.get("authority_domain") != domain or
            proof_record.get("subject_repository") != REPO or
            proof_record.get("subject_sha") != head or
            proof_record.get("material_fingerprint") != fingerprint or
            proof_record.get("disposition") != "INDEPENDENT_REVIEW_ACCEPTED"):
        raise ReceiptError("underlying specialist review not positively bound")
    reviewer = proof_record.get("reviewer_identity")
    if not isinstance(reviewer, str) or not reviewer.strip():
        raise ReceiptError("independent reviewer identity not attested")
    if reviewer.casefold() == candidate_author.casefold():
        raise ReceiptError("candidate author cannot be sole specialist reviewer")
    declared_independence = proof_record.get("review_independence")
    expected_independence = (
        "INDEPENDENT_NON_AUTHOR" if domain == "MATHEMATICAL"
        else "ROLE_SCOPED_NON_AUTHOR_SPECIALIST"
    )
    if declared_independence != expected_independence:
        raise ReceiptError("required specialist-review independence not attested")
    if not isinstance(record.get("review_scope"), str) or not record["review_scope"].strip():
        raise ReceiptError("missing specialist-reviewed claim/scope")
    if record["review_scope"] != proof_record.get("review_scope"):
        raise ReceiptError("specialist reviewed scope differs from receipt")
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
        "subject_sha": head,
        "material_fingerprint": fingerprint,
        "authority": {
            "independent_scientific_validation_performed_by_this_controller": False,
            "new_certification_created": False,
            "github_approval_created": False,
            "substantive_review_replaced": False,
        },
    }
