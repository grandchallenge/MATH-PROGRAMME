from __future__ import annotations

import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from administrative_automation import derive_completion_state, load_json, validate_completion_state, validate_config

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "governance" / "administrative_maintenance_automation.json"
STATE_PATH = ROOT / "governance" / "administrative_maintenance_completion_state.json"
REPAIR_RECORD_PATH = (
    ROOT
    / "governance"
    / "administrative_receipt_repairs"
    / "MP-ADMIN-RECEIPT-REPAIR-244-001.json"
)
CANDIDATE_WORKFLOW = ROOT / ".github" / "workflows" / "administrative-maintenance-candidate.yml"
SYNC_WORKFLOW = ROOT / ".github" / "workflows" / "administrative-maintenance-synchronization.yml"
DISPATCH_WORKFLOW = ROOT / ".github" / "workflows" / "administrative-maintenance-dispatch.yml"
VALIDATION_WORKFLOW = ROOT / ".github" / "workflows" / "administrative-maintenance-automation-validation.yml"
SYNC_SCRIPT_PATH = ROOT / "ci" / "synchronize_administrative_completion.py"
SCRIPT_PATHS = [
    ROOT / "ci" / "administrative_automation.py",
    ROOT / "ci" / "administrative_receipts.py",
    ROOT / "ci" / "prepare_administrative_candidate.py",
    SYNC_SCRIPT_PATH,
    ROOT / "ci" / "dispatch_administrative_maintenance_v2.py",
]
SCHEMA_PATHS = [
    ROOT / "schemas" / "administrative_maintenance_automation.schema.json",
    ROOT / "schemas" / "administrative_maintenance_completion_state.schema.json",
    ROOT / "schemas" / "administrative_receipt_repair_244.schema.json",
]


def workflow_permissions(text: str) -> dict[str, str]:
    match = re.search(r"(?m)^permissions:\s*\n((?:  [a-z-]+:\s*[a-z]+\s*\n)+)", text)
    if not match:
        return {}
    return {key: value for key, value in re.findall(r"(?m)^  ([a-z-]+):\s*([a-z]+)\s*$", match.group(1))}


def validate_refresh_trigger_redundancy(text: str) -> list[str]:
    errors: list[str] = []
    minutes: set[int] = set()
    for cron in re.findall(r"cron:\s*'([^']+)'", text):
        match = re.fullmatch(r"([0-5]?\d)\s+\*\s+\*\s+\*\s+\*", cron.strip())
        if match:
            minutes.add(int(match.group(1)))
    ordered = sorted(minutes)
    if len(ordered) < 4:
        errors.append(
            "candidate workflow requires at least four distinct recurring hourly trigger offsets"
        )
        return errors
    gaps = [later - earlier for earlier, later in zip(ordered, ordered[1:])]
    gaps.append(ordered[0] + 60 - ordered[-1])
    if max(gaps) > 20:
        errors.append(
            f"candidate workflow recurring trigger gap exceeds 20 minutes: {ordered}"
        )
    return errors


def validate_workflows(config: dict) -> list[str]:
    errors: list[str] = []
    candidate = CANDIDATE_WORKFLOW.read_text(encoding="utf-8")
    sync = SYNC_WORKFLOW.read_text(encoding="utf-8")
    dispatch = DISPATCH_WORKFLOW.read_text(encoding="utf-8")
    validation = VALIDATION_WORKFLOW.read_text(encoding="utf-8")
    expected_permissions = config["workflow_permissions"]
    observed = {
        "candidate_preparation": workflow_permissions(candidate),
        "completion_synchronization": workflow_permissions(sync),
        "dispatcher": workflow_permissions(dispatch),
        "automation_validation": workflow_permissions(validation),
    }
    for key, expected in expected_permissions.items():
        if observed.get(key) != expected:
            errors.append(f"{key}: workflow permission drift: {observed.get(key)} != {expected}")
    for cron in [*config["preparation_crons_utc"], config["hourly_refresh_cron_utc"]]:
        if f"cron: '{cron}'" not in candidate:
            errors.append(f"candidate workflow missing protected preparation cron: {cron}")
    errors.extend(validate_refresh_trigger_redundancy(candidate))
    if "workflow_dispatch:" not in candidate:
        errors.append("candidate workflow missing explicit workflow_dispatch recovery path")
    provenance_markers = (
        "administrative-maintenance-trigger.json",
        "github.event.schedule",
        "GITHUB_EVENT_NAME",
        "GITHUB_RUN_ID",
        "GITHUB_RUN_ATTEMPT",
    )
    for marker in provenance_markers:
        if marker not in candidate:
            errors.append(f"candidate workflow missing trigger provenance marker: {marker}")
    if "pull_request:" in candidate or "pull_request_target:" in candidate:
        errors.append("write-capable candidate workflow must not execute pull-request code")
    if "pull_request:" in sync or "pull_request_target:" in sync:
        errors.append("write-capable synchronizer must not execute pull-request code")
    if "dispatch_administrative_maintenance_v2.py" not in dispatch:
        errors.append("dispatcher does not consume receipt-derived completion")
    if "validate_administrative_automation.py" not in validation:
        errors.append("automation validator is not workflow-reachable")
    for path, text in (
        (CANDIDATE_WORKFLOW, candidate),
        (SYNC_WORKFLOW, sync),
        (DISPATCH_WORKFLOW, dispatch),
        (VALIDATION_WORKFLOW, validation),
    ):
        for action in re.findall(r"(?m)^\s*-?\s*uses:\s*([^\s]+)\s*$", text):
            if "@" not in action or not re.fullmatch(r"[^@]+@[0-9a-f]{40}", action):
                errors.append(f"{path.name}: unpinned action {action}")
        if "set -euo pipefail" not in text:
            errors.append(f"{path.name}: shell path is not fail closed")
    forbidden_permissions = {"administration", "checks", "deployments", "packages", "security-events"}
    for key, permissions in observed.items():
        extra = forbidden_permissions & set(permissions)
        if extra:
            errors.append(f"{key}: excessive permissions {sorted(extra)}")
    return errors


def validate_fixed_point_contract() -> list[str]:
    text = SYNC_SCRIPT_PATH.read_text(encoding="utf-8")
    required = {
        "semantic comparison": "def completion_semantics(",
        "ancestry verifier": "def git_is_ancestor(",
        "derivation stabilizer": "def stabilize_completion_derivation(",
        "semantic equality gate": "if previous is None or completion_semantics(previous) != completion_semantics(completion):",
        "ancestry enforcement": "if not ancestry_check(root, retained_head, evaluated_head):",
        "runtime stabilization": "completion = stabilize_completion_derivation(ROOT, derived_completion, previous, head)",
        "separate evaluation-head evidence": '"protected_head": head',
        "separate derivation-head evidence": '"completion_derivation_head": completion["derived_from_protected_head"]',
        "no-successor equality gate": "if current == completion:\n        return None",
    }
    return [
        f"fixed-point contract missing {name}"
        for name, marker in required.items()
        if marker not in text
    ]


def validate_scripts() -> list[str]:
    errors: list[str] = []
    forbidden = (
        "/merges",
        "merge_pull_request",
        "enable_auto_merge",
        "merge_method",
        "dismiss_pull_request_review",
        "branch_protection_rule",
    )
    for path in SCRIPT_PATHS:
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                errors.append(f"{path.name}: forbidden authority capability token {token}")
    sync = SYNC_SCRIPT_PATH.read_text(encoding="utf-8")
    if "CREDENTIAL_MISSING_PATCH_RETAINED" not in sync:
        errors.append("cross-repository credential absence is not explicit and fail closed")
    candidate = (ROOT / "ci" / "prepare_administrative_candidate.py").read_text(encoding="utf-8")
    if '"draft": True' not in candidate:
        errors.append("candidate PR creation is not draft-only")
    errors.extend(validate_fixed_point_contract())
    return errors


def validate_repair_record() -> list[str]:
    errors: list[str] = []
    if not REPAIR_RECORD_PATH.is_file():
        return ["MP-ADMIN-RECEIPT-REPAIR-244-001 record missing"]
    schema_path = ROOT / "schemas" / "administrative_receipt_repair_244.schema.json"
    schema = load_json(schema_path)
    record = load_json(REPAIR_RECORD_PATH)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(record), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "$"
        errors.append(f"receipt repair schema violation at {location}: {error.message}")
    if record.get("failure_evidence", {}).get("completion_registry_advanced") is not False:
        errors.append("receipt repair rewrites pre-repair completion state")
    if record.get("failure_evidence", {}).get("tracking_issue_closed") is not False:
        errors.append("receipt repair closes issue #243 before protected readback")
    return errors


def main() -> int:
    errors: list[str] = []
    config = load_json(CONFIG_PATH)
    state = load_json(STATE_PATH)
    errors.extend(validate_config(config))
    errors.extend(validate_completion_state(state))
    errors.extend(validate_workflows(config))
    errors.extend(validate_scripts())
    errors.extend(validate_repair_record())
    for schema in SCHEMA_PATHS:
        try:
            json.loads(schema.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{schema.name}: invalid JSON schema: {exc}")
    if (ROOT / ".git").exists():
        import subprocess

        head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        try:
            derived = derive_completion_state(ROOT, config, head)
            errors.extend(validate_completion_state(derived, state))
        except Exception as exc:
            errors.append(f"protected receipt derivation failed: {exc}")
    if errors:
        for error in errors:
            print(error)
        return 1
    print("MP-ADMIN-AUTOMATION-CLOSURE-001: valid")
    print("MP-ADMIN-RECEIPT-REPAIR-244-001: valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
