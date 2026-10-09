#!/usr/bin/env python3
"""Protected, read-only material-admission shadow classifier.

This controller cannot approve, issue a required status, or certify mathematics.
Candidate Git data is inert; all executable code and profile data come from
protected main. A future ruleset cutover is a *separate* governed operation.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from agent_material_profiles import MaterialAdmissionError, classify_text, load_registry
from agent_routine_review import RoutineReviewError, api, delegated_classification
from specialist_receipt_adapter import ReceiptError, protected_specialist_receipt

REPOSITORY = "grandchallenge/MATH-PROGRAMME"
CONTROL = "GCL-AGENT-ADMISSION-SPECIALIST-001"
REPORT = Path("material-admission-shadow.json")
SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
QUEUE_REF_PREFIX = "refs/heads/gh-readonly-queue/main/"


class ShadowError(ValueError):
    pass


def git(root: Path, *args: str, binary: bool = False) -> str | bytes:
    command = ["git", "-C", str(root), *args]
    done = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          timeout=40, check=False)
    if done.returncode:
        raise ShadowError("protected Git read failed: " + args[0])
    return done.stdout if binary else done.stdout.decode("utf-8").strip()


def reserved_path(path: str) -> bool:
    return path.startswith((
        ".github/workflows/", ".ghos-routing/", "governance/release_trust",
        "governance/constitutional", "schemas/release_trust",
    )) or path in (
        "ci/agent_routine_review.py", "ci/agent_material_profiles.py",
        "ci/specialist_admission_shadow.py", "mkdocs.yml",
    )


def classify_paths(paths: list[str]) -> str:
    if any(reserved_path(path) for path in paths):
        return "RESERVED_OR_CONTROL_PLANE_PENDING"
    return "SPECIALIST_REVIEW_PENDING"


def specialist_domain(paths: list[str]) -> str | None:
    """Only exact coherent path-based authority routes; ambiguity is pending."""
    if not paths:
        return None
    def classify(path: str) -> str | None:
        if reserved_path(path):
            return "PROTECTION"
        if path.startswith(("fixtures/formal/", "fixtures/cmdg/")) or path.endswith(".lean"):
            return "MATHEMATICAL"
        if path.startswith("governance/source_"):
            return "SOURCE_SEMANTIC"
        return None
    classes = {classify(path) for path in paths}
    return classes.pop() if len(classes) == 1 else None


def observe_specialist_receipt(head: str, files: list[dict], paths: list[str],
                               token: str) -> dict:
    """Recognize protected domain evidence but never change admission authority."""
    domain = specialist_domain(paths)
    if domain is None:
        return {"disposition": "SPECIALIST_REVIEW_PENDING",
                "reason": "unmapped/mixed specialist domain", "subject_sha": head}
    try:
        proof = protected_specialist_receipt(
            head=head, files=files, domain=domain,
            api_get=lambda path: api("GET", path, token=token),
        )
    except (ReceiptError, RoutineReviewError) as err:
        return {"disposition": "SPECIALIST_REVIEW_PENDING",
                "domain": domain, "reason": str(err), "subject_sha": head}
    return {"disposition": "SPECIALIST_EVIDENCE_RECOGNIZED_SHADOW",
            "domain": domain, "evidence": proof, "subject_sha": head}


def shadow_pr(event: dict, token: str) -> dict:
    number = event.get("number")
    if not isinstance(number, int) or number <= 0:
        raise ShadowError("missing numeric pull request identifier")
    prefix = f"/repos/{REPOSITORY}"
    pr = api("GET", f"{prefix}/pulls/{number}", token=token)
    head = (pr.get("head") or {}).get("sha")
    if not isinstance(head, str) or not SHA_RE.fullmatch(head):
        raise ShadowError("unbound PR head SHA")
    files = api("GET", f"{prefix}/pulls/{number}/files?per_page=100", token=token)
    if not isinstance(files, list):
        raise ShadowError("malformed changed-file manifest")
    count = pr.get("changed_files")
    if not isinstance(count, int) or count < 1:
        raise ShadowError("missing changed-file count")
    if len(files) != count:
        return {"disposition": "SPECIALIST_REVIEW_PENDING",
                "reason": "changed-file enumeration not exhaustive",
                "changed_files": count, "subject_sha": head}
    paths = [row.get("filename", "") for row in files]
    if not all(isinstance(path, str) and path for path in paths):
        raise ShadowError("invalid changed-file path")
    try:
        decision = delegated_classification(
            pr, files, head, token=token, prefix=prefix,
        )
    except (MaterialAdmissionError, RoutineReviewError) as err:
        observation = observe_specialist_receipt(head, files, paths,\n                                                os.environ.get("SPECIALIST_READ_TOKEN") or token)
        if observation["disposition"] == "SPECIALIST_REVIEW_PENDING":
            observation["path_class"] = classify_paths(paths)
        return {"changed_files": count, "paths": paths, **observation}
    fresh = api("GET", f"{prefix}/pulls/{number}", token=token)
    if ((fresh.get("head") or {}).get("sha") != head or
            (fresh.get("base") or {}).get("sha") != (pr.get("base") or {}).get("sha")):
        raise ShadowError("subject moved during protected classification")
    return {"disposition": "ROUTINE_CANDIDATE_ONLY", "evidence": decision,
            "subject_sha": head, "changed_files": count}


def shadow_merge_group(event: dict, root: Path, env: dict[str, str]) -> dict:
    group = event.get("merge_group") or {}
    sha = env.get("GITHUB_SHA", "")
    ref = env.get("GITHUB_REF", "")
    if not SHA_RE.fullmatch(sha) or not ref.startswith(QUEUE_REF_PREFIX):
        raise ShadowError("not a native Programme merge-queue candidate")
    if group.get("head_sha") != sha or group.get("head_ref") != ref:
        raise ShadowError("queue event and runtime identity disagree")
    if group.get("base_ref") != "refs/heads/main":
        raise ShadowError("queue does not target protected main")
    base = git(root, "rev-parse", "HEAD")
    if not SHA_RE.fullmatch(base):
        raise ShadowError("protected baseline missing")
    git(root, "fetch", "--no-tags", "--force", "origin",
        "+" + ref + ":refs/remotes/origin/gcl-shadow")
    fetched = git(root, "rev-parse", "refs/remotes/origin/gcl-shadow")
    if fetched != sha:
        raise ShadowError("queue ref changed during protected fetch")
    git(root, "merge-base", "--is-ancestor", base, sha)
    names = git(root, "diff", "--no-renames", "--name-status", "-z",
                base, sha, binary=True).split(b"\x00")
    records = [v for v in names if v]
    if len(records) != 2 or records[0] != b"M":
        paths = [value.decode("utf-8", errors="replace") for value in records[1::2]]
        return {"disposition": classify_paths(paths),
                "reason": "merge group not exactly one modified documentation file",
                "subject_sha": sha, "protected_base": base, "paths": paths}
    try:
        path = records[1].decode("utf-8")
        old = git(root, "show", f"{base}:{path}", binary=True)
        new = git(root, "show", f"{sha}:{path}", binary=True)
        evidence = classify_text(path, old, new, load_registry())
    except (MaterialAdmissionError, UnicodeDecodeError) as err:
        return {"disposition": classify_paths([records[1].decode("utf-8", errors="replace")]),
                "reason": str(err), "subject_sha": sha, "protected_base": base}
    # Another base movement is a new subject: fail closed rather than publishing
    # a stale group classification as if it were current.
    if git(root, "ls-remote", "origin", "refs/heads/main").split()[0] != base:
        raise ShadowError("protected main moved during group classification")
    return {"disposition": "ROUTINE_CANDIDATE_ONLY", "evidence": evidence,
            "subject_sha": sha, "protected_base": base}


def evaluate(event: dict, env: dict[str, str]) -> dict:
    mode = env.get("GITHUB_EVENT_NAME")
    if mode == "pull_request_target":
        decision = shadow_pr(event, env["GITHUB_TOKEN"])
    elif mode == "merge_group":
        decision = shadow_merge_group(event, Path(env["PROTECTED_REPO"]), env)
    else:
        raise ShadowError("unexpected event")
    return {
        "control_id": CONTROL,
        "mode": "OBSERVE_ONLY_NOT_REQUIRED",
        "event": mode,
        "decision": decision,
        "authority": {
            "github_approval": False, "required_check_satisfied": False,
            "independent_review": False, "mathematical_certification": False,
            "merge_queue_bypass": False,
        },
    }


if __name__ == "__main__":
    try:
        with open(os.environ["GITHUB_EVENT_PATH"], encoding="utf-8") as f:
            report = evaluate(json.load(f), os.environ)
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, sort_keys=True))
    except (ShadowError, RoutineReviewError, MaterialAdmissionError,
            OSError, KeyError, ValueError, subprocess.TimeoutExpired) as exc:
        print("Fail closed shadow controller: " + str(exc), file=sys.stderr)
        sys.exit(1)
