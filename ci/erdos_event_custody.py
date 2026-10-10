#!/usr/bin/env python3
"""Durable append-only GitHub issue evidence custody; isolated operational canary.

No source-claim, Project, Forge/Solve/Cert, or protected admission authority.
"""
from __future__ import annotations
import argparse
import base64
import copy
import hashlib
import json
import os
import subprocess
from pathlib import Path

OWNER = "grandchallenge"
REPO = "MATH-PROGRAMME"
LEDGER = 2499
CANARY = 2500  # Dedicated operational fixture issue; never a research assignment.
PREFIX = "GCL-ERDOS-EVENT/1"


def gh(*args: str, payload: dict | None = None):
    result = subprocess.run(
        ["gh", "api", *args],
        input=json.dumps(payload) if payload is not None else None,
        capture_output=True, text=True, check=True, timeout=120,
    )
    return json.loads(result.stdout)


def record(event: dict) -> dict:
    comment = event["comment"]
    issue = event["issue"]
    action = event["action"]
    if event["repository"]["full_name"] != f"{OWNER}/{REPO}":
        raise ValueError("repository mismatch")
    if issue.get("number") == LEDGER or issue.get("pull_request"):
        raise ValueError("not a catalogue comment")
    if not issue.get("title", "").startswith("[GCL-ERDOS] ERDOS-CATALOGUE-"):
        raise ValueError("not a catalogue task")
    if action not in {"created", "edited", "deleted"}:
        raise ValueError("unsupported action")
    if action == "created" and not (comment.get("body") or "").startswith("RESULT/1\n"):
        raise ValueError("not a RESULT/1 creation")
    if not isinstance(comment.get("id"), int):
        raise ValueError("missing authenticated comment identifier")
    raw = json.dumps(event, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    digest = hashlib.sha256(raw).hexdigest()
    key_input = f"{issue['number']}:{comment['id']}:{action}:{comment.get('updated_at')}:{hashlib.sha256((comment.get('body') or '').encode()).hexdigest()}"
    key = hashlib.sha256(key_input.encode()).hexdigest()
    return {"key": key, "digest": digest, "raw": base64.b64encode(raw).decode(),
            "issue": issue["number"], "comment": comment["id"], "action": action}


def append(event: dict) -> dict:
    evidence = record(event)
    replies = gh(f"repos/{OWNER}/{REPO}/issues/{LEDGER}/comments?per_page=100", "--paginate", "--slurp")
    flattened = [item for page in replies for item in page]
    marker = f"{PREFIX}\nKEY: {evidence['key']}\n"
    found = [c for c in flattened if (c.get("body") or "").startswith(marker)]
    if len(found) > 1:
        raise ValueError("duplicate ledger entry violates uniqueness")
    if found:
        if f"PAYLOAD_SHA256: {evidence['digest']}\n" not in found[0]["body"]:
            raise ValueError("ledger record identity collision")
        return {"status": "EXISTS", "ledger_comment": found[0]["id"], "key": evidence["key"]}
    text = (marker + f"PAYLOAD_SHA256: {evidence['digest']}\n"
            + f"ISSUE: {evidence['issue']}\nCOMMENT: {evidence['comment']}\n"
            + f"ACTION: {evidence['action']}\n"
            + f"PAYLOAD_BASE64: {evidence['raw']}\n"
            + "AUTHORITY: OPERATIONAL_EVENT_CUSTODY_ONLY\n")
    posted = gh("-X", "POST", f"repos/{OWNER}/{REPO}/issues/{LEDGER}/comments",
                "--input", "-", payload={"body": text})
    verify = gh(f"repos/{OWNER}/{REPO}/issues/comments/{posted['id']}")
    if verify.get("body") != text:
        raise ValueError("ledger readback digest mismatch")
    return {"status": "APPENDED", "ledger_comment": posted["id"], "key": evidence["key"]}


def canary(event: dict) -> dict:
    """Actual GitHub comment event, synthetic in-memory registry; never projection."""
    from ci import erdos_catalogue_programme_intake as intake
    if event["repository"]["full_name"] != f"{OWNER}/{REPO}":
        raise ValueError("canary repository mismatch")
    if event["issue"]["number"] != CANARY or event["issue"]["title"] != "[GCL-CANARY] RESULT/1 intake event acceptance":
        raise ValueError("unexpected canary issue")
    if event["action"] not in ("created", "edited"):
        raise ValueError("unexpected canary action")
    registry = copy.deepcopy(intake.load_registry())
    row = registry["issues"][0]
    original = gh(f"repos/{OWNER}/{REPO}/issues/{row['issue_number']}")
    if intake.sha(original["body"] or "") != row["issue_body_sha256"]:
        raise ValueError("original research issue source lock drift")
    row["issue_number"] = CANARY
    synthetic = copy.deepcopy(event)
    synthetic["issue"] = copy.deepcopy(original)
    synthetic["issue"]["number"] = CANARY
    # The genuine issue title/body are reused solely in memory to test exact intake bindings.
    synthetic["comment"]["issue_url"] = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{CANARY}"
    receipt, _ = intake.capture(synthetic, registry)
    expected = "STRUCTURALLY_VALID_UNADJUDICATED"
    if receipt["validation"] != expected or any(receipt["authority_effects"].values()):
        raise ValueError(f"positive canary rejected or asserted authority: {receipt['errors']}")
    # Exactly the same event delivered twice must produce one receipt.
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as directory:
        report = intake.build_report(registry, [synthetic, copy.deepcopy(synthetic)], Path(directory))
        if len(report["receipts"]) != 1:
            raise ValueError("duplicate event not idempotent")
    return {"status": "PASS", "event_action": event["action"],
            "comment_id": event["comment"]["id"], "receipt": receipt["validation"],
            "duplicate_receipts": len(report["receipts"]), "authority": "NONE"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, required=True)
    parser.add_argument("--mode", choices=["ledger", "canary"], required=True)
    args = parser.parse_args()
    event = json.loads(args.event.read_text())
    result = append(event) if args.mode == "ledger" else canary(event)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
