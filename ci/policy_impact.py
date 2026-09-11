#!/usr/bin/env python3
"""Fail-closed impact classifier for Programme policy shards.

Formal validation has its own material-closure router in ci/formal_validation.py.
This module classifies only the policy DAG. Unknown policy paths still force the
complete policy shard set.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable

import jsonschema

import formal_validation as formal

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = ROOT / "governance/policy_impact_gating.json"
CONTROL_SCHEMA = ROOT / "schemas/policy_impact_gating.schema.json"
REGISTRY_PATH = ROOT / "governance/policy_shard_registry.json"
REGISTRY_SCHEMA = ROOT / "schemas/policy_shard_registry.schema.json"
CONTRACT_MANIFEST_PATH = ROOT / "governance/contract_test_manifest.json"
ZERO_SHA = "0" * 40
ALL_SHARDS = (
    "core",
    "fixtures",
    "cmdg",
    "oz",
    "administrative",
    "campaigns",
    "contracts",
    "docs",
    "repository-regression",
)
FULL_FANOUT_PATHS = {
    ".github/workflows/ci.yml",
    ".github/workflows/formal-validation.yml",
    ".github/workflows/cmdg-formal-lane-replay.yml",
    ".github/workflows/cmdg-postmerge.yml",
    "ci/formal_validation.py",
    "ci/test_formal_validation.py",
    "ci/policy_impact.py",
    "ci/test_policy_impact.py",
    "ci/validate_policy_reachability.py",
    "ci/test_policy_reachability.py",
    "ci/validate_repository_execution.py",
    "ci/test_repository_execution.py",
    "ci/validate_workflow_semantics.py",
    "ci/test_workflow_semantics.py",
    "governance/formal_validation_registry.json",
    "schemas/formal_validation_registry.schema.json",
    "governance/policy_impact_gating.json",
    "schemas/policy_impact_gating.schema.json",
    "governance/policy_shard_registry.json",
    "schemas/policy_shard_registry.schema.json",
    "governance/contract_test_manifest.json",
    "governance/cmdg_workflow_impact_gating.json",
    "schemas/cmdg_workflow_impact_gating.schema.json",
}
CONTROL_PLANE_PATHS = {
    "ci/run_unittest_modules.py",
    "ci/run_policy_shard.py",
}


class ImpactError(RuntimeError):
    pass


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ImpactError(f"expected object: {path}")
    return value


def normalize_paths(paths: Iterable[str]) -> list[str]:
    out: list[str] = []
    for raw in paths:
        path = str(raw).replace("\\", "/")
        if path.startswith("./"):
            path = path[2:]
        if (
            not path
            or path.startswith("/")
            or path == ".."
            or path.startswith("../")
            or "/../" in path
            or path.endswith("/..")
        ):
            raise ImpactError(f"unsafe changed path: {raw!r}")
        out.append(path)
    return sorted(set(out))


def matches_root(path: str, root: str) -> bool:
    root = root.rstrip("/")
    return path == root or path.startswith(root + "/")


def contract_test_paths() -> set[str]:
    data = load_json(CONTRACT_MANIFEST_PATH)
    if data.get("manifest_id") != "MP-CONTRACT-TEST-MANIFEST-001":
        raise ImpactError("contract-test manifest identity drift")
    rows = data.get("tests")
    if not isinstance(rows, list) or not rows:
        raise ImpactError("contract-test manifest empty")
    out: set[str] = set()
    for row in rows:
        if (
            not isinstance(row, dict)
            or not isinstance(row.get("path"), str)
            or not isinstance(row.get("category"), str)
        ):
            raise ImpactError("invalid contract-test manifest row")
        path = normalize_paths([row["path"]])[0]
        if path in out:
            raise ImpactError(f"duplicate contract-test path: {path}")
        out.add(path)
    return out


def shard_impacts(paths: list[str]) -> tuple[list[str], list[str]]:
    active = {"core"}
    unknown: list[str] = []
    contract_tests = contract_test_paths()
    if any(path in FULL_FANOUT_PATHS for path in paths):
        return list(ALL_SHARDS), []

    for path in paths:
        lower = path.lower()
        matched = False
        if path in CONTROL_PLANE_PATHS:
            active.add("contracts")
            matched = True
        if path.startswith("docs/") or path in {"mkdocs.yml", "requirements/docs.txt"}:
            active.add("docs")
            matched = True
        if path.startswith("handoffs/"):
            active.update({"administrative", "campaigns"})
            matched = True
        if path.startswith("tools/render_visual_pedagogy") and path.endswith(".py"):
            active.update({"contracts", "docs"})
            matched = True
        if path.startswith("fixtures/algebraic/") or path.startswith("fixtures/formal/") or any(
            token in lower for token in ("grobner", "chaidez", "researchmath", "log_gcd")
        ):
            active.add("fixtures")
            matched = True
        if path.startswith("fixtures/cmdg/") or "cmdg" in lower:
            active.add("cmdg")
            matched = True
        if any(token in lower for token in ("administrative", "maintenance", "autonomy")):
            active.add("administrative")
            matched = True
        if any(token in lower for token in ("release_trust", "intellect_profile")) and (
            path.startswith("ci/")
            or path.startswith("tests/")
            or path.startswith("governance/")
            or path.startswith(".github/workflows/")
        ):
            active.update({"administrative", "contracts"})
            matched = True
        if path.startswith("campaigns/") or "campaign" in lower:
            active.add("campaigns")
            matched = True
        if path == "requirements/policy.txt" or path.startswith(".github/workflows/") or path.startswith("experiments/"):
            active.add("contracts")
            matched = True
        if path.startswith("ci/") and any(
            token in lower
            for token in ("programme", "workflow", "policy", "repository_execution", "retired", "formal_validation")
        ):
            active.add("contracts")
            matched = True
        if path.startswith("tests/"):
            if path in contract_tests:
                active.add("contracts")
                if any(token in lower for token in ("documentary", "visual_pedagogy")):
                    active.add("docs")
            elif path.startswith("tests/test_oz"):
                active.add("oz")
            elif "cmdg" in lower:
                active.add("cmdg")
            elif "fixture" in lower:
                active.add("fixtures")
            elif any(token in lower for token in ("administrative", "release_trust", "intellect_profile")):
                active.update({"administrative", "contracts"})
            elif "campaign" in lower:
                active.add("campaigns")
            else:
                unknown.append(path)
            matched = True
        if path.startswith("schemas/") or path.startswith("governance/") or path.startswith("evidence/"):
            active.add("contracts")
            matched = True
        if path.endswith(".md") or path in {"README.md", "CONTRIBUTING.md"}:
            active.add("docs")
            matched = True
        if not matched:
            unknown.append(path)

    if unknown:
        return list(ALL_SHARDS), sorted(set(unknown))
    return [shard for shard in ALL_SHARDS if shard in active], []


def classify_paths(
    paths: Iterable[str],
    *,
    event_name: str = "pull_request",
    schedule: str | None = None,
) -> dict:
    changed = normalize_paths(paths)
    control = load_json(CONTROL_PATH)
    full_cron = str(control["policy_dag"]["full_policy_sentinel_cron"])

    if event_name == "schedule":
        if schedule == full_cron:
            return {
                "event_mode": "full_policy_sentinel",
                "changed_paths": [],
                "unknown_paths": [],
                "policy_shards": list(ALL_SHARDS),
            }
        return {
            "event_mode": "unknown_schedule",
            "changed_paths": [],
            "unknown_paths": [f"schedule:{schedule}"],
            "policy_shards": list(ALL_SHARDS),
        }
    if event_name == "workflow_dispatch":
        return {
            "event_mode": "manual_full",
            "changed_paths": changed,
            "unknown_paths": [],
            "policy_shards": list(ALL_SHARDS),
        }
    if event_name == "merge_group":
        return {
            "event_mode": "merge_group_full",
            "changed_paths": changed,
            "unknown_paths": [],
            "policy_shards": list(ALL_SHARDS),
        }

    shards, unknown = shard_impacts(changed)
    return {
        "event_mode": "transition",
        "changed_paths": changed,
        "unknown_paths": unknown,
        "policy_shards": shards,
    }


def git_changed_paths(base: str, head: str) -> list[str]:
    if not base or not head or base == ZERO_SHA:
        raise ImpactError("transition diff base/head is unavailable")
    completed = subprocess.run(
        ["git", "diff", "--name-only", base, head, "--"],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode:
        raise ImpactError(f"git diff failed: {completed.stderr.strip()}")
    return [line for line in completed.stdout.splitlines() if line.strip()]


def changed_paths_from_event(event_name: str, event: dict) -> list[str]:
    if event_name == "pull_request":
        pr = event.get("pull_request", {})
        return git_changed_paths(
            str(pr.get("base", {}).get("sha") or ""),
            str(pr.get("head", {}).get("sha") or ""),
        )
    if event_name == "push":
        return git_changed_paths(
            str(event.get("before") or ""),
            str(event.get("after") or os.environ.get("GITHUB_SHA") or ""),
        )
    return []


def write_output(path: str | None, result: dict) -> None:
    if not path:
        return
    values = {
        "event_mode": result["event_mode"],
        "policy_shards": json.dumps(result["policy_shards"], separators=(",", ":")),
        "unknown_count": len(result["unknown_paths"]),
    }
    with open(path, "a", encoding="utf-8") as handle:
        for key, value in values.items():
            handle.write(f"{key}={value}\n")


def validate_control() -> None:
    control = load_json(CONTROL_PATH)
    registry = load_json(REGISTRY_PATH)
    jsonschema.validate(control, load_json(CONTROL_SCHEMA))
    jsonschema.validate(registry, load_json(REGISTRY_SCHEMA))
    contract_test_paths()

    if control.get("control_id") != "MP-POLICY-IMPACT-GATING-001":
        raise ImpactError("policy impact control identity drift")
    if control.get("status") != "ACTIVE_ON_PROTECTED_MERGE":
        raise ImpactError("policy impact control status drift")
    if control["classifier"]["unknown_path_behavior"] != "FULL_FANOUT":
        raise ImpactError("unknown policy path behavior must remain FULL_FANOUT")
    if tuple(control["policy_dag"]["shards"]) != ALL_SHARDS:
        raise ImpactError("policy shard roster drift")
    if set(registry.get("shards", {})) != set(ALL_SHARDS):
        raise ImpactError("policy shard registry coverage drift")

    formal_registry = formal.load_registry(ROOT)
    fv = control["formal_validation"]
    if fv["registry"] != "governance/formal_validation_registry.json":
        raise ImpactError("formal validation registry identity drift")
    if fv["required_context"] != formal_registry["required_context"]:
        raise ImpactError("formal validation required context drift")
    if fv["protected_sentinel"]["cron"] != formal_registry["sentinels"]["legacy_formal_cron"]:
        raise ImpactError("formal validation sentinel cron drift")
    if fv["protected_sentinel"]["attestation_substitution"] is not False:
        raise ImpactError("protected formal sentinel may not substitute attestation for replay")

    authority = control["authority_boundary"]
    if authority.get("human_steward_exact_head_authorization_required") is not True:
        raise ImpactError("Human Steward exact-head authorization boundary weakened")
    for key in (
        "required_checks_removed_without_equivalent_successor",
        "formal_proof_closure_weakened",
        "formal_semantic_tcb_weakened",
        "bypass_created",
        "emergency_authority_created",
        "direct_protected_push_authorized",
        "human_steward_impersonation_authorized",
    ):
        if authority.get(key) is not False:
            raise ImpactError(f"authority boundary weakened: {key}")
    if any(value is not False for value in control["claim_boundaries"].values()):
        raise ImpactError("claim boundary weakened")


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    classify = sub.add_parser("classify")
    classify.add_argument("--event-path", default=os.environ.get("GITHUB_EVENT_PATH"))
    classify.add_argument("--event-name", default=os.environ.get("GITHUB_EVENT_NAME", "workflow_dispatch"))
    classify.add_argument("--schedule", default=os.environ.get("GCL_EVENT_SCHEDULE"))
    classify.add_argument("--github-output", default=os.environ.get("GITHUB_OUTPUT"))
    sub.add_parser("validate")
    args = parser.parse_args()

    try:
        if args.command == "validate":
            validate_control()
            print("policy impact gating control: valid")
            return 0
        event = json.loads(Path(args.event_path).read_text(encoding="utf-8")) if args.event_path else {}
        paths = changed_paths_from_event(args.event_name, event)
        result = classify_paths(paths, event_name=args.event_name, schedule=args.schedule)
        write_output(args.github_output, result)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (
        ImpactError,
        formal.FormalValidationError,
        OSError,
        json.JSONDecodeError,
        jsonschema.ValidationError,
        KeyError,
        ValueError,
    ) as exc:
        print(f"policy impact classification error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
