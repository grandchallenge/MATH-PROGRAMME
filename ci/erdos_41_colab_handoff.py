#!/usr/bin/env python3
"""Bind a verified Erdős Colab execution to unadjudicated GCL intake custody.

This module never contacts GitHub, claims a queue lease, or posts a comment.
It is invoked only after the existing erdos_colab_host_runner.verify_artifacts.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_handoff(directory: Path, verified: dict) -> dict:
    if verified.get("state") != "GREEN_ENGINEERING_UNADJUDICATED":
        raise ValueError("not verified for Colab evidence handoff")
    if verified.get("subject") != "ERDOS-024-41" or verified.get("backend") not in ("witness_only","local_transformers"):
        raise ValueError("wrong queue subject/backend")
    if verified.get("authority_effects") is None or any(verified["authority_effects"].values()):
        raise ValueError("attempted claim authority in handoff")
    if verified["backend"] == "witness_only" and verified.get("role_pass_count") != 0:
        raise ValueError("witness probe cannot claim AI review")
    if verified["backend"] == "local_transformers" and verified.get("role_pass_count") != 2:
        raise ValueError("missing model review passes")
    task=json.loads((directory/"task.json").read_text())
    result=json.loads((directory/"erdos_review_result.json").read_text())
    if task.get("problem_id")!=41 or task.get("review_issue")!=2536 or result.get("review_issue")!=2536:
        raise ValueError("source mismatch")
    if result.get("source_comment_sha256")!=task.get("source_comment_sha256"):
        raise ValueError("original return digest mismatch")
    bundle={
        "schema":"GCL-ERDOS-041-COLAB-INTAKE-HANDOFF/1",
        "status":"AWAITING_EXISTING_AUTHENTICATED_INTAKE",
        "issue":2536,"problem_id":41,
        "backend":verified["backend"],"role_pass_count":verified["role_pass_count"],
        "source_comment_sha256":task["source_comment_sha256"],
        "task_sha256":sha(directory/"task.json"),
        "job_sha256":sha(directory/"job.json"),
        "result_file_sha256":sha(directory/"erdos_review_result.json"),
        "receipt_file_sha256":sha(directory/"erdos_review_receipt.json"),
        "result_content_sha256":verified["result_sha256"],
        "authority_effects":verified["authority_effects"],
        "note":"No issue write or mathematical authority. Existing authenticated host intake must verify queue freshness and accept or reject."
    }
    target=directory/"colab-intake-handoff.json"
    with target.open("x",encoding="utf-8") as handle:
        json.dump(bundle,handle,sort_keys=True,indent=2)
        handle.write("\n")
    return {"handoff":str(target),"handoff_sha256":sha(target),"status":bundle["status"]}
