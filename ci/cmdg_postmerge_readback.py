#!/usr/bin/env python3
"""Emit a deterministic, non-authoritative CMDG post-merge readback receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "cmdg_postmerge_readback.schema.json"
ROSTER = (
    "cmdg-condensed-cm1.yml",
    "cmdg-condensed-cm2.yml",
    "cmdg-condensed-cm3.yml",
    "cmdg-condensed-cm4-p2-d.yml",
    "cmdg-condensed-cm4-p2-e.yml",
    "cmdg-condensed-cm4-p2.yml",
    "cmdg-condensed-cm4-p3.yml",
    "cmdg-condensed-cm4.yml",
    "cmdg-euclid-bridge.yml",
    "cmdg-nat-concordance.yml",
    "cmdg-solid-c05.yml",
    "cmdg-vertical-spine-v0.yml",
)
SHA = re.compile(r"^[0-9a-f]{40}$")


def receipt_id(repository: str, protected_ref: str, merge_sha: str, classifier_digest: str) -> str:
    identity = "\n".join((repository, protected_ref, merge_sha, classifier_digest))
    return "MP-CMDG-READBACK-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()


def transition_base(event: dict[str, Any]) -> str | None:
    before = str(event.get("before") or "")
    return before if SHA.fullmatch(before) and set(before) != {"0"} else None


def changed_paths(base: str | None, head: str) -> list[str]:
    if base is None:
        return []
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head, "--"],
        cwd=ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode:
        raise RuntimeError(f"git diff failed: {result.stderr.strip()}")
    return sorted({line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()})


def build_receipt(
    *, repository: str, protected_ref: str, merge_sha: str, observed_sha: str,
    classifier_digest: str, event_name: str, event: dict[str, Any],
    policy_shards: list[str], unknown_count: int, impact_result: str,
    suite_results: dict[str, str], run_id: str, run_attempt: int,
) -> dict[str, Any]:
    if set(suite_results) != set(ROSTER):
        raise ValueError("suite result roster drift")
    base = transition_base(event)
    paths = changed_paths(base, merge_sha) if SHA.fullmatch(merge_sha) else []
    cmdg_required = "cmdg" in policy_shards
    integration_ok = (
        impact_result == "success"
        and SHA.fullmatch(merge_sha) is not None
        and observed_sha == merge_sha
        and protected_ref == "refs/heads/main"
    )
    suites_ok = (
        all(result == "success" for result in suite_results.values())
        if cmdg_required
        else all(result == "skipped" for result in suite_results.values())
    )
    terminal = (
        "observed_pass_no_further_governance_action"
        if integration_ok and suites_ok
        else "downstream_hold_requires_compensation"
    )
    receipt = {
        "schema_version": "1.0.0",
        "receipt_id": receipt_id(repository, protected_ref, merge_sha, classifier_digest),
        "repository": repository,
        "protected_ref": protected_ref,
        "merge_sha": merge_sha,
        "observed_sha": observed_sha,
        "transition_base": base,
        "origin_event": event_name,
        "origin_run": {"run_id": run_id, "run_attempt": run_attempt},
        "classifier_digest": classifier_digest,
        "changed_paths": paths,
        "policy_shards": policy_shards,
        "unknown_count": unknown_count,
        "cmdg_required": cmdg_required,
        "suite_results": {name: suite_results[name] for name in ROSTER},
        "terminal_state": terminal,
        "authority_boundary": {
            "integration_facts_only": True,
            "approval_created": False,
            "activation_created": False,
            "ratification_created": False,
            "certification_created": False,
            "promotion_created": False,
        },
    }
    jsonschema.validate(receipt, json.loads(SCHEMA.read_text(encoding="utf-8")))
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-path", required=True)
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--protected-ref", required=True)
    parser.add_argument("--merge-sha", required=True)
    parser.add_argument("--observed-sha", required=True)
    parser.add_argument("--classifier-digest", required=True)
    parser.add_argument("--policy-shards", required=True)
    parser.add_argument("--unknown-count", required=True, type=int)
    parser.add_argument("--impact-result", required=True)
    parser.add_argument("--suite-results", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--run-attempt", required=True, type=int)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    receipt = build_receipt(
        repository=args.repository,
        protected_ref=args.protected_ref,
        merge_sha=args.merge_sha,
        observed_sha=args.observed_sha,
        classifier_digest=args.classifier_digest,
        event_name=args.event_name,
        event=json.loads(Path(args.event_path).read_text(encoding="utf-8")),
        policy_shards=json.loads(args.policy_shards),
        unknown_count=args.unknown_count,
        impact_result=args.impact_result,
        suite_results=json.loads(args.suite_results),
        run_id=args.run_id,
        run_attempt=args.run_attempt,
    )
    Path(args.output).write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
