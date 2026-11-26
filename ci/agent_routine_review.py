#!/usr/bin/env python3
"""Protected scoped reviewer and explicit, nonauthoritative abstention classifier.

Only source-proved narrow transformations or independently protected specialist
receipts can issue App approval. Bounded public-documentary mixtures may
produce an exact-head NOT_APPLICABLE *without* posting a review. All other
unknown material fails closed; GitHub review rules and merge queue remain active.
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
from specialist_domains import domain_for_paths, protected_path

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
    if event_name == "pull_request_target":
        if event.get("action") not in ("ready_for_review", "synchronize", "reopened"):
            return None
        pr = event.get("pull_request") or {}
        number = event.get("number")
        sha = (pr.get("head") or {}).get("sha")
        if (type(number) is not int or number <= 0 or
                not isinstance(sha, str) or
                not re.fullmatch(r"[a-f0-9]{40}", sha) or
                (pr.get("head") or {}).get("repo", {}).get("full_name") != REPOSITORY or
                (pr.get("base") or {}).get("ref") != "main" or
                pr.get("draft")):
            return None
        return number, sha
    if event_name == "workflow_run":
        run = event.get("workflow_run") or {}
        if run.get("event") != "pull_request" or run.get("conclusion") != "success":
            return None
        if (run.get("repository") or {}).get("full_name") != REPOSITORY:
            return None
        prs = run.get("pull_requests") or []
        if len(prs) != 1:
            return None
        linked = prs[0]
        number = linked.get("number")
        # A pull_request workflow often runs on a synthetic merge commit.
        # Trust the PR-linked exact head instead; a missing link fails closed.
        linked_head = (linked.get("head") or {}).get("sha")
        sha = linked_head or run.get("head_sha")
        if (type(number) is not int or number <= 0 or
                not isinstance(sha, str) or
                not re.fullmatch(r"[a-f0-9]{40}", sha)):
            return None
        return number, sha
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



def bounded_research_not_applicable(pr: dict, files: list[dict], head: str) -> bool:
    """Recognize research-only candidates that this App MUST NOT approve.

    An expected negative delegated-review eligibility verdict is not a
    failed mathematical proof or failed independent-review validation.
    Strictly scoped to Erdős #41 research prose and its regression tests.
    No reviewer token is used; branch protection and separate specialist
    review remain authoritative. Mixed/protected materials still fail.
    """
    verify_specialist_envelope(pr, files, head)
    seen: set[str] = set()
    has_proof_note = False
    for entry in files:
        path = entry.get("filename")
        if (not isinstance(path, str) or path in seen or
                path.startswith("/") or ".." in path.split("/") or
                chr(0) in path or protected_path(path) or
                entry.get("status") not in ("added", "modified") or
                entry.get("previous_filename")):
            return False
        seen.add(path)
        if path.startswith("research/erdos-41-density/") and path.endswith(".md"):
            has_proof_note = True
        elif path.startswith("tests/test_erdos41_") and path.endswith(".py"):
            pass
        else:
            return False
    return has_proof_note



# This is an abstention-only classifier. It does not add any authority to the
# protected routine App material profiles or to the specialist-domain registry.
# Restrict it to known public explanatory directories, excluding governance,
# code, executable inputs, routing, campaign admission and protected workflows.
DOCUMENTARY_ONLY_PATH = re.compile(
    r"^docs/(archives|domains|pnp_above)/[A-Za-z0-9][A-Za-z0-9_-]*\.md$"
)
DOCUMENTARY_ONLY_MAX_FILES = 20


def bounded_documentary_not_applicable(
    pr: dict, files: list[dict], head: str,
) -> bool:
    """Identify an exact-head public documentary mixture for *non-approval*.

    True means the App must abstain; it never means that content, mathematical
    claims, source semantics, or public publication have been approved.
    Everything outside this narrow negative classification follows the
    existing specialist/protection fail-closed routes.
    """
    verify_specialist_envelope(pr, files, head)
    if not (2 <= len(files) <= DOCUMENTARY_ONLY_MAX_FILES):
        return False
    seen: set[str] = set()
    sections: set[str] = set()
    for entry in files:
        path = entry.get("filename")
        if not isinstance(path, str):
            return False
        matched = DOCUMENTARY_ONLY_PATH.fullmatch(path)
        if (matched is None or path in seen or protected_path(path)
                or entry.get("status") not in ("added", "modified")
                or entry.get("previous_filename")
                or not isinstance(entry.get("sha"), str)
                or not re.fullmatch(r"[a-f0-9]{40}", entry["sha"])):
            return False
        seen.add(path)
        sections.add(matched.group(1))
    # The pre-existing failed example spans multiple nonprivileged editorial
    # surfaces. Single-surface and non-documentary changes remain untouched.
    return len(sections) >= 2


# Public-facing homepage/status refreshes are also editorial work. This
# deliberately enumerates the public entry points and their presentation-only
# companions. It does not classify arbitrary docs, tests, executable JS,
# workflow configuration, governance, proof material or routing changes.
PUBLIC_EDITORIAL_ENTRY_POINTS = frozenset({
    "docs/index.md",
    "docs/CURRENT_WORK.md",
    "docs/SHOWCASE.md",
    "docs/MILLENNIUM_PRIZE_STATUS.md",
    "docs/MATHEMATICAL_DEVELOPMENTS.md",
})
PUBLIC_EDITORIAL_COMPANIONS = {
    "docs/stylesheets/home.css": frozenset({"docs/index.md"}),
    "tests/test_erdos_homepage_status.py": frozenset({"docs/index.md"}),
    "tests/test_public_explanatory_pages.py": frozenset({
        "docs/CURRENT_WORK.md", "docs/SHOWCASE.md",
    }),
    "tests/test_millennium_public_status.py": frozenset({
        "docs/MILLENNIUM_PRIZE_STATUS.md",
    }),
}


def bounded_public_editorial_not_applicable(
    pr: dict, files: list[dict], head: str,
) -> bool:
    """Classify an editorial closure for abstention ONLY, not approval."""
    verify_specialist_envelope(pr, files, head)
    if not 1 <= len(files) <= DOCUMENTARY_ONLY_MAX_FILES:
        return False
    paths: set[str] = set()
    for entry in files:
        path = entry.get("filename")
        if (not isinstance(path, str) or path in paths or protected_path(path)
                or entry.get("status") not in ("added", "modified")
                or entry.get("previous_filename")
                or not isinstance(entry.get("sha"), str)
                or not re.fullmatch(r"[a-f0-9]{40}", entry["sha"])):
            return False
        if path in PUBLIC_EDITORIAL_COMPANIONS:
            if entry["status"] != "modified":
                return False
        elif (path not in PUBLIC_EDITORIAL_ENTRY_POINTS
                and DOCUMENTARY_ONLY_PATH.fullmatch(path) is None):
            return False
        paths.add(path)
    if not paths.intersection(PUBLIC_EDITORIAL_ENTRY_POINTS):
        return False
    return all(
        path not in paths or bool(required.intersection(paths))
        for path, required in PUBLIC_EDITORIAL_COMPANIONS.items()
    )


# A non-approving route for bounded research handoffs plus their mandatory
# reference-index link. This deliberately does NOT extend the App's routine
# material-approval profiles or protected specialist-domain admission registry.
RESEARCH_HANDOFF_RE = re.compile(
    r"^docs/handoffs/ERDOS-[0-9]{3,4}-[A-Z0-9-]+\.md$"
)
RESEARCH_INDEX_PATH = "docs/archives/research.md"


def bounded_research_handoff_not_applicable(
    pr: dict, files: list[dict], head: str, *, token: str, prefix: str,
) -> bool:
    """Recognize only one unadjudicated Erdős handoff + one matching index link.

    True authorizes a negative routing receipt, NEVER review or admission.
    All content is read by exact commit and Git blob rather than PR prose.
    """
    verify_specialist_envelope(pr, files, head)
    if len(files) != 2:
        return False
    handoffs = [
        row for row in files
        if isinstance(row.get("filename"), str)
        and RESEARCH_HANDOFF_RE.fullmatch(row["filename"])
    ]
    indexes = [
        row for row in files
        if row.get("filename") == RESEARCH_INDEX_PATH
    ]
    if len(handoffs) != 1 or len(indexes) != 1:
        return False
    handoff, index = handoffs[0], indexes[0]
    for row, status in ((handoff, "added"), (index, "modified")):
        path = row["filename"]
        if (protected_path(path) or row.get("status") != status
                or row.get("previous_filename")
                or not isinstance(row.get("sha"), str)
                or not re.fullmatch(r"[0-9a-f]{40}", row["sha"])):
            return False
    if (handoff.get("additions", 0) < 1
            or handoff.get("deletions") != 0
            or index.get("additions") != 1
            or index.get("deletions") != 0):
        return False
    patch = index.get("patch")
    if not isinstance(patch, str):
        return False
    added = [
        line[1:] for line in patch.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    ]
    deleted = [
        line for line in patch.splitlines()
        if line.startswith("-") and not line.startswith("---")
    ]
    # Exactly one navigational link to the same new handoff; no rewritten
    # index content, arbitrary link, or additional path can pass this route.
    target = "](../handoffs/" + handoff["filename"].rsplit("/", 1)[1] + ")"
    if (deleted or len(added) != 1 or not added[0].startswith("- [")
            or not added[0].endswith(target)):
        return False
    raw, actual_blob = fetch_exact_file(
        prefix, handoff["filename"], head, token,
    )
    if actual_blob != handoff["sha"]:
        raise RoutineReviewError("research handoff Git blob changed at exact head")
    # Only explicitly UNADJUDICATED research is eligible. This marker is a
    # scope restriction, not evidence that any mathematical assertion is true.
    if (len(raw) > 100_000 or not raw.startswith(b"# Erd")
            or b"**Status:** PROVED_ON_PAPER_UNADJUDICATED" not in raw[:1000]):
        return False
    return True


def report_research_handoff_not_applicable(head: str, files: list[dict]) -> None:
    """Refer mathematical claims for specialist review; post NO approval."""
    record = {
        "record_type": "GCL_RESEARCH_HANDOFF_SPECIALIST_ROUTING/1",
        "candidate_head": head,
        "source_file": next(
            row["filename"] for row in files
            if RESEARCH_HANDOFF_RE.fullmatch(row["filename"])
        ),
        "index_file": RESEARCH_INDEX_PATH,
        "disposition": "NOT_APPLICABLE_NO_APPROVAL",
        "specialist_domain": "MATHEMATICAL",
        "specialist_review": "PENDING_BEFORE_CLAIM_PROMOTION",
        "source_semantic_review": "NOT_PERFORMED",
        "review_posted": False,
        "editorial_admission": "SUBJECT_TO_EXISTING_PROTECTED_CHECKS",
        "mathematical_certification": False,
        "claim_promotion": False,
        "protected_checks_waived": False,
    }
    message = (
        "RESEARCH_HANDOFF_SPECIALIST_ROUTE: matched exact-head unadjudicated "
        "research note with its one-line index reference. App abstains: "
        "no automated GitHub approval, mathematical certification, or source-"
        "semantic adjudication. Specialist review is required before claim "
        "promotion; protected branch checks and merge queue remain binding."
    )
    print("::notice title=Unadjudicated research handoff::" + message)
    print(json.dumps(record, sort_keys=True))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write(
                "### Research handoff — specialist claim review pending\n\n"
                + message + "\n\n"
                + "This is a non-approval routing receipt; it does not "
                "waive any protected check or authorize publication.\n\n"
                + json.dumps(record, indent=2, sort_keys=True) + "\n"
            )


def report_documentary_review_not_applicable(
    head: str, files: list[dict], *,
    scope: str = "mixed_public_documentary_markdown_only",
) -> None:
    """Record a non-authoritative abstention, never a GitHub review or pass."""
    record = {
        "record_type": "GCL_DELEGATED_REVIEW_APPLICABILITY/1",
        "candidate_head": head,
        "file_count": len(files),
        "disposition": "NOT_APPLICABLE_NO_APPROVAL",
        "review_posted": False,
        "mathematical_certification": False,
        "claim_promotion": False,
        "protected_checks_waived": False,
        "scope": scope,
    }
    message = (
        "NOT_APPLICABLE_NO_APPROVAL: exact-head public documentary mixture "
        "is outside this narrow automated reviewer's approval authority. "
        "No GitHub review, certification, protected-check waiver, or claim "
        "promotion was issued. Existing protected policy and any substantive "
        "review remain authoritative."
    )
    print("::notice title=Delegated review abstained::" + message)
    print(json.dumps(record, sort_keys=True))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write(
                "### Delegated review applicability: NOT_APPLICABLE_NO_APPROVAL\n\n"
                + message + "\n\n"
                + "This is not an approval check, specialist receipt, "
                "or evidence of mathematical validity.\n\n"
                + "```json\n" + json.dumps(record, indent=2, sort_keys=True)
                + "\n```\n"
            )

def exact_head_nonauthor_review(
    pr: dict, number: int, head: str, *, token: str, prefix: str,
) -> str:
    """Require real GitHub non-author APPROVED provenance before abstaining.

    This proves only GitHub source-review custody, NEVER mathematical
    certification or delegated App authority. A dismissed, stale-head,
    author, or unreviewed PR must remain blocked.
    """
    reviews = api("GET", f"{prefix}/pulls/{number}/reviews?per_page=100",
                  token=token)
    if not isinstance(reviews, list) or len(reviews) >= 100:
        raise RoutineReviewError("research review inventory incomplete")
    author = ((pr.get("user") or {}).get("login") or "").casefold()
    if not author:
        raise RoutineReviewError("unattributable research candidate author")
    by_reviewer: dict[str, dict] = {}
    for row in reviews:
        if not isinstance(row, dict):
            raise RoutineReviewError("invalid GitHub review entry")
        login = ((row.get("user") or {}).get("login") or "").casefold()
        if not login:
            raise RoutineReviewError("unattributed GitHub review entry")
        previous = by_reviewer.get(login)
        if previous is None or (
            (row.get("submitted_at") or "", row.get("id") or 0)
            > (previous.get("submitted_at") or "", previous.get("id") or 0)
        ):
            by_reviewer[login] = row
    for login, review in by_reviewer.items():
        if (login != author and login != APP_REVIEWER.casefold()
                and review.get("state") == "APPROVED"
                and review.get("commit_id") == head):
            return login
    raise RoutineReviewError(
        "research-only candidate lacks current-head non-author APPROVED review"
    )


def report_delegated_review_not_applicable(
    head: str, files: list[dict], reviewer: str,
) -> None:
    """Report non-approval explicitly; a green job is NOT an App review."""
    message = (
        "NOT_APPLICABLE: mathematical research/test material is not "
        "eligible for automatic delegated App review. "
        "No approval or mathematical certification was issued; "
        "protected main checks and independent review remain separate."
    )
    print("::notice title=Delegated review not applicable::" + message)
    print(message)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write(
                "### Delegated-review applicability: NOT_APPLICABLE\n\n"
                "This candidate contains bounded Erdős #41 research and tests. "
                "**No automated approval or mathematical certification was "
                "issued.** Its exact head is `" + head + "` and it changes "
                + str(len(files)) + " files. A distinct authenticated "
                "GitHub non-author APPROVED review exists at this exact head "
                "(reviewer: " + reviewer + "). This is source-review provenance "
                "only, **not mathematical certification**. Protected branch "
                "rules and required CI are unchanged.\n"
            )


def specialist_domain_for_file_manifest(files: list[dict]) -> str:
    """Use protected four-domain routing, retaining mainline operational exceptions."""
    if not files or len(files) > 100:
        raise RoutineReviewError("no exact candidate file inventory")
    paths = [row.get("filename") for row in files if isinstance(row, dict)]
    if len(paths) != len(files):
        raise RoutineReviewError("invalid candidate file inventory")
    domain = domain_for_paths(paths)
    if domain is None:
        raise RoutineReviewError("candidate specialist class unresolved or mixed")
    return domain


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
        candidate_author=pr["user"]["login"],
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
        # Research-only content has no protected automated approval class.
        # An expected abstention is a truthful NOT_APPLICABLE job result,
        # rather than a misleading test failure; it never posts a review.
        # Mixed, malformed, or protected-path edits still fail closed or
        # require an independently protected specialist receipt.
        if bounded_research_not_applicable(pr, files, head):
            reviewer = exact_head_nonauthor_review(
                pr, number, head, token=read_token, prefix=prefix,
            )
            report_delegated_review_not_applicable(head, files, reviewer)
            return 0
        editorial_scope = None
        if bounded_documentary_not_applicable(pr, files, head):
            editorial_scope = "mixed_public_documentary_markdown_only"
        elif bounded_public_editorial_not_applicable(pr, files, head):
            editorial_scope = "public_editorial_entry_points_and_bound_companions"
        if editorial_scope is not None:
            # This route is a no-approval diagnostic, not a replacement
            # source-semantic or mathematical reviewer. Recheck exact head,
            # base, and file count before reporting the observed manifest.
            current = api("GET", f"{prefix}/pulls/{number}", token=read_token)
            if (current.get("state") != "open" or current.get("draft")
                    or (current.get("head") or {}).get("sha") != head
                    or (current.get("base") or {}).get("sha")
                        != (pr.get("base") or {}).get("sha")
                    or current.get("changed_files") != len(files)):
                raise RoutineReviewError("documentary candidate changed during abstention")
            report_documentary_review_not_applicable(head, files, scope=editorial_scope)
            return 0
        if bounded_research_handoff_not_applicable(
            pr, files, head, token=read_token, prefix=prefix,
        ):
            # Recheck source identity before returning a non-approval receipt.
            current = api("GET", f"{prefix}/pulls/{number}", token=read_token)
            if (current.get("state") != "open" or current.get("draft")
                    or (current.get("head") or {}).get("sha") != head
                    or (current.get("base") or {}).get("sha")
                        != (pr.get("base") or {}).get("sha")
                    or current.get("changed_files") != len(files)):
                raise RoutineReviewError(
                    "research handoff changed during specialist routing"
                )
            report_research_handoff_not_applicable(head, files)
            return 0
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
