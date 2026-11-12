#!/usr/bin/env python3
"""Atomic per-issue adjudication claim. Requires authenticated gh CLI.

A GitHub create-ref is the linearization point: only one contender can create
refs/heads/gcl-adjudication-claims/issue-N. Never steal or auto-expire a claim.
"""
import argparse
import json
import subprocess
import sys
import uuid

REPO = "grandchallenge/MATH-PROGRAMME"
PREFIX = "refs/heads/gcl-adjudication-claims/issue-"

def api(method, path, fields=None):
    cmd = ["gh", "api", "--method", method, f"repos/{REPO}/{path}"]
    if fields is not None:
        cmd += ["--input", "-"]
    result = subprocess.run(cmd, input=json.dumps(fields) if fields is not None else None,
                            text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout) if result.stdout.strip() else {}

def comments(issue):
    # GitHub REST pagination: never rely on first page or search results.
    cmd = ["gh", "api", "--paginate", "--slurp",
           f"repos/{REPO}/issues/{issue}/comments?per_page=100"]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    pages = json.loads(result.stdout)
    return [c for page in pages for c in page], len(pages)

def adjudications(items):
    return [{"id": c["id"], "url": c.get("html_url")} for c in items
            if any(s in (c.get("body") or "").lower()
                   for s in ("source-critical adjudication", "source critical adjudication",
                             "adjudication disposition", "adjudication/1"))]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["acquire", "inspect", "release"])
    p.add_argument("issue", type=int)
    p.add_argument("--claim-sha", help="Exact claim commit SHA, mandatory for release")
    args = p.parse_args()
    if args.issue < 1310:
        p.error("issue must be at least 1310")
    ref = PREFIX + str(args.issue)
    if args.action == "inspect":
        try:
            current = api("GET", "git/ref/" + ref.removeprefix("refs/"))
            print(json.dumps({"result": "HELD", "sha": current["object"]["sha"]}))
        except RuntimeError as e:
            if "404" not in str(e):
                raise
            print(json.dumps({"result": "UNCLAIMED"}))
        return 0
    if args.action == "release":
        if not args.claim_sha:
            p.error("--claim-sha required")
        current = api("GET", "git/ref/" + ref.removeprefix("refs/"))
        if current["object"]["sha"] != args.claim_sha:
            raise RuntimeError("claim SHA mismatch; refusing release")
        # Release only after durable adjudication readback, or explicitly documented abort.
        api("DELETE", "git/" + ref)
        print(json.dumps({"result": "RELEASED", "sha": args.claim_sha}))
        return 0
    issue = api("GET", f"issues/{args.issue}")
    if issue.get("state") != "open":
        print(json.dumps({"result": "INELIGIBLE", "reason": "issue not open"}))
        return 2
    before, pages = comments(args.issue)
    found = adjudications(before)
    if found:
        print(json.dumps({"result": "ALREADY_ADJUDICATED", "comments": found,
                          "count": len(before), "pages": pages}))
        return 3
    main_ref = api("GET", "git/ref/heads/main")
    head = main_ref["object"]["sha"]
    commit = api("GET", f"git/commits/{head}")
    actor = subprocess.run(["gh", "api", "user", "--jq", ".login"],
                           capture_output=True, text=True, check=True).stdout.strip()
    nonce = uuid.uuid4().hex
    claim_commit = api("POST", "git/commits", {
        "message": f"GCL_ADJUDICATION_CLAIM/1 issue={args.issue} actor={actor} nonce={nonce}",
        "tree": commit["tree"]["sha"], "parents": [head]
    })
    try:
        api("POST", "git/refs", {"ref": ref, "sha": claim_commit["sha"]})
    except RuntimeError as e:
        # A 422 race is a losing claim, never authorization to retry or post.
        print(json.dumps({"result": "NOT_ACQUIRED", "error": str(e)}))
        return 4
    current = api("GET", "git/ref/" + ref.removeprefix("refs/"))
    if current["object"]["sha"] != claim_commit["sha"]:
        raise RuntimeError("post-acquisition ref mismatch")
    after, pages_after = comments(args.issue)
    duplicates = adjudications(after)
    print(json.dumps({"result": "ACQUIRED" if not duplicates else "ABORT_EXISTING",
                      "issue": args.issue, "actor": actor, "claim_sha": claim_commit["sha"],
                      "ref": ref, "before_count": len(before), "after_count": len(after),
                      "before_pages": pages, "after_pages": pages_after,
                      "existing": duplicates}))
    return 0 if not duplicates else 5

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, subprocess.CalledProcessError, ValueError) as exc:
        print(json.dumps({"result": "ERROR_FAIL_CLOSED", "error": str(exc)}))
        sys.exit(6)
