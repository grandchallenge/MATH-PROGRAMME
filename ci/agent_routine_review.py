#!/usr/bin/env python3
"""Protected, deliberately narrow machine reviewer for a reversible MkDocs image removal.

This is a routine delegated mechanical disposition, NOT independent mathematical review.
Unknown changes fail closed. GitHub's review rule and native merge queue remain active.
"""
from __future__ import annotations

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from agent_material_profiles import (
    MaterialAdmissionError, classify_text, load_registry,
)
from specialist_receipt_adapter import (
    ReceiptError, protected_specialist_receipt,
)

REPOSITORY = "grandchallenge/MATH-PROGRAMME"
APP_REVIEWER = "gcl-release-trust[bot]"
REMOVE_EXACTLY = (
    "## The GCL continuity fabric\n"
    "\n"
    "![GCL Agent Continuity fabric showing the relationship between the canonical governance layer, specialised repositories, and protected admission.](assets/gcl-agent-continuity-fabric.png)\n"
    "\n"
    "This public orientation diagram shows how the canonical policy and bounded-operation layers relate to the specialised MATHFORGE, MATHSOLVE, and MATHCERT repositories. The artwork is explanatory, not operative: repository-local policy, protected records, validators, and exact-head evidence remain authoritative. It does not grant authority, certify mathematics, or imply authority inheritance across repositories.\n"
    "\n"
)
REQUIRED_HEAD_CONTEXTS = frozenset({
    "validate-json", "formal-validation / formal-validation",
    "policy / policy", "security / action-policy", "routing-enforcement",
})


class RoutineReviewError(RuntimeError):
    pass


def api(method: str, path: str, *, token: str, payload: dict | None = None) -> Any:
    if not token:
        raise RoutineReviewError("missing authorized token")
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com" + path,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "gcl-routine-review-001",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise RoutineReviewError(
            f"GitHub {method} {path.split('?')[0]} returned HTTP {exc.code}"
        ) from exc


def removed_patch_text(patch: str) -> str:
    """Recover just deleted lines from a GitHub unified patch, excluding file headers."""
    lines = patch.splitlines(keepends=True)
    return "".join(line[1:] for line in lines if line.startswith("-") and not line.startswith("---"))


def eligible_image_removal(pr: dict, files: list[dict], pinned_head: str) -> None:
    if pr.get("state") != "open" or pr.get("draft"):
        raise RoutineReviewError("PR not open and ready")
    head = pr.get("head") or {}
    if head.get("sha") != pinned_head or not (len(pinned_head) == 40):
        raise RoutineReviewError("PR head changed from exact candidate")
    if (head.get("repo") or {}).get("full_name") != REPOSITORY:
        raise RoutineReviewError("candidate outside authorized repository")
    if (pr.get("base") or {}).get("ref") != "main":
        raise RoutineReviewError("PR does not target protected main")
    if (pr.get("user") or {}).get("login") == APP_REVIEWER:
        raise RoutineReviewError("reviewer App cannot approve its own change")
    if pr.get("changed_files") != 1 or len(files) != 1:
        raise RoutineReviewError("exactly one tracked documentation file required")
    f = files[0]
    if (f.get("filename"), f.get("status"), f.get("additions"), f.get("deletions")) != (
        "docs/index.md", "modified", 0, 6
    ):
        raise RoutineReviewError("file scope, addition, or deletion count drift")
    patch = f.get("patch") or ""
    if any(line.startswith("+") and not line.startswith("+++") for line in patch.splitlines()):
        raise RoutineReviewError("unexpected added line")
    if removed_patch_text(patch) != REMOVE_EXACTLY:
        raise RoutineReviewError("deletion content not precisely the admitted image section")


def required_contexts_green(check_runs: list[dict], statuses: list[dict]) -> None:
    succeeded: set[str] = set()
    failed: set[str] = set()
    for run in check_runs:
        name = str(run.get("name") or "")
        if name in REQUIRED_HEAD_CONTEXTS:
            if run.get("status") == "completed" and run.get("conclusion") == "success":
                succeeded.add(name)
            else:
                failed.add(name)
    for status in statuses:
        name = str(status.get("context") or "")
        if name in REQUIRED_HEAD_CONTEXTS:
            if status.get("state") == "success":
                succeeded.add(name)
            else:
                failed.add(name)
    missing = REQUIRED_HEAD_CONTEXTS - succeeded
    if failed or missing:
        raise RoutineReviewError(
            "required exact-head admission evidence incomplete: "
            + repr({"failed_or_pending": sorted(failed), "missing": sorted(missing)})
        )


def candidate_number(event: dict, event_name: str) -> tuple[int, str] | None:
    if event_name == "workflow_dispatch":
        value = (event.get("inputs") or {}).get("pr_number")
        if value is None or not str(value).isdigit():
            return None
        return int(value), ""
    if event_name == "workflow_run":
        run = event.get("workflow_run") or {}
        if run.get("event") != "pull_request" or run.get("conclusion") != "success":
            return None
        if (run.get("repository") or {}).get("full_name") != REPOSITORY:
            return None
        prs = run.get("pull_requests") or []
        if len(prs) != 1:
            return None
        return int(prs[0]["number"]), str(run.get("head_sha") or "")
    return None



def fetch_exact_file(prefix: str, path: str, revision: str,
                     token: str) -> tuple[bytes, str]:
    """Read a Git blob via a pinned commit, not an untrusted PR patch."""
    if not re.fullmatch(r"[a-f0-9]{40}", revision):
        raise RoutineReviewError("unbound commit identity")
    quoted = urllib.parse.quote(path, safe="/")
    value = api(
        "GET", f"{prefix}/contents/{quoted}?ref={revision}", token=token,
    )
    if value.get("type") != "file" or value.get("encoding") != "base64":
        raise RoutineReviewError("GitHub contents response is not a file")
    blob_sha = value.get("sha")
    if not isinstance(blob_sha, str) or not re.fullmatch(r"[a-f0-9]{40}", blob_sha):
        raise RoutineReviewError("GitHub file has no blob identity")
    try:
        payload = base64.b64decode(value["content"], validate=False)
    except (ValueError, KeyError) as exc:
        raise RoutineReviewError("malformed base64 GitHub contents") from exc
    if value.get("size") != len(payload):
        raise RoutineReviewError("declared file size differs from file bytes")
    return payload, blob_sha


def delegated_classification(pr: dict, files: list[dict], head: str,
                             *, token: str, prefix: str) -> dict:
    """Conservative alternative to legacy exact image-section review."""
    if pr.get("state") != "open" or pr.get("draft"):
        raise RoutineReviewError("PR is not ready")
    if (pr.get("head") or {}).get("sha") != head or not re.fullmatch(r"[a-f0-9]{40}", head):
        raise RoutineReviewError("head SHA drift")
    if (pr.get("head") or {}).get("repo", {}).get("full_name") != REPOSITORY:
        raise RoutineReviewError("not an internal Programme candidate")
    base = pr.get("base") or {}
    if base.get("ref") != "main" or not re.fullmatch(r"[a-f0-9]{40}", str(base.get("sha") or "")):
        raise RoutineReviewError("unbound protected base identity")
    if (pr.get("user") or {}).get("login") in (None, "", APP_REVIEWER, "gcl-release-trust"):
        raise RoutineReviewError("review token cannot approve its author")
    if pr.get("changed_files") != 1 or len(files) != 1:
        raise RoutineReviewError("unknown or multifile material closure")
    entry = files[0]
    if entry.get("status") != "modified" or entry.get("previous_filename"):
        raise RoutineReviewError("renames and new/deleted files excluded")
    path = entry.get("filename")
    if not isinstance(path, str):
        raise RoutineReviewError("malformed path")
    before, _ = fetch_exact_file(prefix, path, base["sha"], token)
    after, blob = fetch_exact_file(prefix, path, head, token)
    if blob != entry.get("sha"):
        raise RoutineReviewError("changed-file blob does not match exact head")
    return classify_text(path, before, after, load_registry())



def specialist_domain_for_file_manifest(files: list[dict]) -> str:
    """Fail closed on mixed, unclassified or provenance-ambiguous changes."""
    if not files or len(files) > 100:
        raise RoutineReviewError("no exact candidate file inventory")
    def domain(path: str) -> str | None:
        if path.startswith((
            ".github/workflows/", ".ghos-routing/", "ci/agent_",
            "ci/specialist_", "schemas/release_trust",
            "governance/release_trust",
        )) or path == "mkdocs.yml":
            return "PROTECTION"
        if path.startswith(("fixtures/formal/", "fixtures/cmdg/")) or path.endswith(".lean"):
            return "MATHEMATICAL"
        if path.startswith("governance/source_"):
            return "SOURCE_SEMANTIC"
        return None
    domains = {domain(str(row.get("filename") or "")) for row in files}
    if len(domains) != 1 or None in domains:
        raise RoutineReviewError("candidate specialist class unresolved or mixed")
    return domains.pop()


def verify_specialist_envelope(pr: dict, files: list[dict], head: str) -> None:
    if pr.get("state") != "open" or pr.get("draft"):
        raise RoutineReviewError("candidate is not ready")
    if not re.fullmatch(r"[0-9a-f]{40}", head):
        raise RoutineReviewError("invalid candidate SHA")
    if (pr.get("head") or {}).get("sha") != head:
        raise RoutineReviewError("head mismatch")
    if (pr.get("head") or {}).get("repo", {}).get("full_name") != REPOSITORY:
        raise RoutineReviewError("external candidate is ineligible")
    if (pr.get("base") or {}).get("ref") != "main":
        raise RoutineReviewError("candidate base is not protected main")
    if not re.fullmatch(r"[0-9a-f]{40}", str((pr.get("base") or {}).get("sha") or "")):
        raise RoutineReviewError("missing protected base identity")
    if (pr.get("user") or {}).get("login") in ("", None, APP_REVIEWER, "gcl-release-trust"):
        raise RoutineReviewError("App self-authorship excluded")
    if pr.get("changed_files") != len(files) or not (1 <= len(files) <= 100):
        raise RoutineReviewError("changed-file inventory incomplete")


def exact_specialist_disposition(pr: dict, files: list[dict], head: str,
                                 *, read_token: str) -> dict:
    """Consume only already protected domain reviews, not PR comments."""
    verify_specialist_envelope(pr, files, head)
    domain = specialist_domain_for_file_manifest(files)
    source_token = os.environ.get("SPECIALIST_READ_TOKEN", "")
    if not source_token or not read_token:
        raise RoutineReviewError("specialist source credential unavailable")
    return protected_specialist_receipt(
        head=head, files=files, domain=domain,
        api_get=lambda path: api("GET", path, token=source_token),
    )


def review_body(head: str, decision: dict) -> str:
    """Exact-head mechanical permission with explicit noncertifying provenance."""
    mode = decision.get("disposition")
    if mode not in ("ROUTINE_BOUNDED", "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED"):
        raise RoutineReviewError("unauthorized reviewer disposition")
    if mode == "ROUTINE_BOUNDED":
        scope = (
            "Verifier and Adversary are non-authoring read-only *logical* "
            "audit passes of this protected controller, not separately "
            "independent theorem specialists."
        )
    else:
        scope = (
            "This controller recognized a prior separately protected "
            "domain-owned exact-material specialist receipt. The role review, "
            "its epistemic merit, and the original claim scope are owned "
            "by the source repository; the App does not generate them."
        )
    return (
        "GCL-DELEGATED-MATERIAL-ADMISSION-001 / "
        + mode + " / GitHub mechanical approval only.\n"
        + f"Exact PR head: {head}\n"
        + scope + "\n"
        + "No new mathematical certification, source-semantic adjudication, "
        "constitutional/security authority, or external-claim promotion "
        "is created. GH-OS native merge queue remains authoritative.\n"
        + "Bound evidence (JSON):\n```json\n"
        + json.dumps(decision, sort_keys=True, indent=2)
        + "\n```"
    )


def main() -> int:
    with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as file:
        event = json.load(file)
    resolved = candidate_number(event, os.environ.get("GITHUB_EVENT_NAME", ""))
    if resolved is None:
        print("No single eligible pull request bound to trusted workflow event; no action")
        return 0
    number, event_sha = resolved
    read_token = os.environ.get("GITHUB_TOKEN", "")
    review_token = os.environ.get("REVIEW_APP_TOKEN", "")
    prefix = f"/repos/{REPOSITORY}"
    pr = api("GET", f"{prefix}/pulls/{number}", token=read_token)
    head = str((pr.get("head") or {}).get("sha") or "")
    if event_sha and head != event_sha:
        raise RoutineReviewError("event SHA not current PR head")
    files = api("GET", f"{prefix}/pulls/{number}/files?per_page=100", token=read_token)
    # The protected registry supplies the sole authority for generic routine
    # profiles. Candidate PR text and branch content are never loaded as policy.
    # A material specialist route is permitted only with *preexisting*
    # domain-protected evidence bound to the complete candidate material.
    # The fallback cannot turn any unclassified edit into routine authority.
    try:
        evidence = delegated_classification(
            pr, files, head, token=read_token, prefix=prefix,
        )
        disposition = "ROUTINE_BOUNDED"
    except (MaterialAdmissionError, RoutineReviewError):
        evidence = exact_specialist_disposition(
            pr, files, head, read_token=read_token,
        )
        disposition = "PROTECTED_DOMAIN_EVIDENCE_RECOGNIZED"
    checks = api("GET", f"{prefix}/commits/{head}/check-runs?per_page=100", token=read_token)
    statuses = api("GET", f"{prefix}/commits/{head}/status", token=read_token)
    if checks.get("total_count", 0) > 100:
        raise RoutineReviewError("check run pagination unknown")
    required_contexts_green(checks.get("check_runs", []), statuses.get("statuses", []))
    reviews = api("GET", f"{prefix}/pulls/{number}/reviews?per_page=100", token=read_token)
    if len(reviews) >= 100:
        raise RoutineReviewError("review pagination unknown")
    if any(
        (r.get("user") or {}).get("login") == APP_REVIEWER
        and r.get("state") == "APPROVED" and r.get("commit_id") == head
        for r in reviews
    ):
        print("Already reviewed at exact head; idempotent no-op")
        return 0
    fresh = api("GET", f"{prefix}/pulls/{number}", token=read_token)
    if ((fresh.get("head") or {}).get("sha") != head or
            (fresh.get("base") or {}).get("sha") != (pr.get("base") or {}).get("sha") or
            fresh.get("state") != "open"):
        raise RoutineReviewError("PR mutated during admission preflight")
    response = api("POST", f"{prefix}/pulls/{number}/reviews", token=review_token, payload={
        "event": "APPROVE",
        "commit_id": head,
        "body": review_body(head, {"disposition": disposition, "material_evidence": evidence}),
    })
    if response.get("state") != "APPROVED":
        raise RoutineReviewError("GitHub did not record an approved App review")
    print(f"Agent-driven bounded routine review recorded on PR #{number} at {head}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RoutineReviewError, ReceiptError, MaterialAdmissionError, OSError, KeyError, ValueError) as error:
        print("Fail closed: " + str(error), file=sys.stderr)
        sys.exit(1)
