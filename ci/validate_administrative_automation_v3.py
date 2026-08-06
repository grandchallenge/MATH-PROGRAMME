from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Callable

from jsonschema import Draft202012Validator, FormatChecker

import validate_administrative_automation_v2 as routed

implementation = routed.implementation
ROOT = Path(__file__).resolve().parents[1]
_original_validate_workflows = implementation.validate_workflows
RUNTIME_EXTENSION_PATHS = [
    ROOT / "ci" / "prepare_administrative_candidate_v3.py",
    ROOT / "ci" / "synchronize_administrative_completion_v3.py",
]
FORBIDDEN_RUNTIME_CAPABILITIES = (
    "/merges",
    "merge_pull_request",
    "enable_auto_merge",
    "dismiss_pull_request_review",
    "branch_protection_rule",
)
ATTESTATION_PATH = ROOT / "governance" / "administrative_maintenance_automation_post_merge_attestation.json"
ATTESTATION_SCHEMA_PATH = ROOT / "schemas" / "administrative_maintenance_automation_post_merge_attestation.schema.json"
TERMINAL_CLOSURE_PATH = ROOT / "governance" / "administrative_maintenance_automation_terminal_closure.json"
TERMINAL_CLOSURE_SCHEMA_PATH = ROOT / "schemas" / "administrative_maintenance_automation_terminal_closure.schema.json"
COMPLETION_STATE_PATH = ROOT / "governance" / "administrative_maintenance_completion_state.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
AncestorCheck = Callable[[str, str], bool]


def validate_workflows_v3(config: dict) -> list[str]:
    compatibility = copy.deepcopy(config)
    validation_permissions = compatibility["workflow_permissions"].pop("automation_validation")
    errors = _original_validate_workflows(compatibility)

    validation_text = (ROOT / ".github" / "workflows" / "administrative-maintenance-automation-validation.yml").read_text(encoding="utf-8")
    observed = implementation.workflow_permissions(validation_text)
    if observed != validation_permissions:
        errors.append(f"automation_validation: workflow permission drift: {observed} != {validation_permissions}")

    candidate = (ROOT / ".github" / "workflows" / "administrative-maintenance-candidate.yml").read_text(encoding="utf-8")
    synchronization = (ROOT / ".github" / "workflows" / "administrative-maintenance-synchronization.yml").read_text(encoding="utf-8")
    active_runtime = "python ci/administrative_autonomy_runtime.py execute --report" in candidate
    credential = config.get("credential_contract", {})
    environment = credential.get("environment", "")
    if environment != "release-trust":
        errors.append(f"credential_contract: protected environment drift: {environment!r} != 'release-trust'")
    for workflow_name, text in (("candidate", candidate), ("synchronization", synchronization)):
        for marker in (
            credential.get("action", ""),
            f"secrets.{credential.get('app_id_secret', '')}",
            f"secrets.{credential.get('private_key_secret', '')}",
            f"environment: {environment}",
        ):
            if not marker or marker not in text:
                errors.append(f"{workflow_name}: missing credential-contract marker {marker}")
        if text.count(f"environment: {environment}") != 1:
            errors.append(f"{workflow_name}: protected environment must occur exactly once")
        workflow_token_allowed = (
            workflow_name == "candidate"
            and active_runtime
            and text.count("${{ github.token }}") == 1
            and "REFEREE_TOKEN: ${{ github.token }}" in text
        )
        if "${{ github.token }}" in text and not workflow_token_allowed:
            errors.append(f"{workflow_name}: write path may not use workflow token")

    candidate_entrypoint = (
        "python ci/prepare_administrative_candidate_v4.py --apply"
        if active_runtime
        else "python ci/prepare_administrative_candidate_v3.py --apply"
    )
    for marker in (
        "EVIDENCE_GITHUB_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "repositories: MATH-PROGRAMME",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        candidate_entrypoint,
    ):
        if marker not in candidate:
            errors.append(f"candidate: missing split-token marker {marker}")

    synchronization_entrypoint = (
        "python ci/synchronize_administrative_completion_v4.py --apply"
        if active_runtime
        else "python ci/synchronize_administrative_completion_v3.py --apply"
    )
    for marker in (
        "repositories: INTELLECT",
        "CROSS_REPOSITORY_MAINTENANCE_TOKEN: ${{ steps.intellect-token.outputs.token }}",
        "permission-actions: read",
        synchronization_entrypoint,
    ):
        if marker not in synchronization:
            errors.append(f"synchronization: missing split-token marker {marker}")

    for path in RUNTIME_EXTENSION_PATHS:
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_RUNTIME_CAPABILITIES:
            if token in text:
                errors.append(f"{path.name}: forbidden authority capability token {token}")
    return errors


def schema_errors(schema_path: Path, record_path: Path, prefix: str) -> tuple[list[str], dict]:
    errors: list[str] = []
    record: dict = {}
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        record = json.loads(record_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for failure in sorted(validator.iter_errors(record), key=lambda item: list(item.absolute_path)):
            location = ".".join(str(part) for part in failure.absolute_path) or "$"
            errors.append(f"{prefix}:{location}: {failure.message}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{prefix}: unreadable record or schema: {exc}")
    return errors, record


def validate_post_merge_attestation() -> list[str]:
    errors, record = schema_errors(ATTESTATION_SCHEMA_PATH, ATTESTATION_PATH, "post_merge_attestation")
    if errors:
        return errors
    detail = record.get("failure_detail", "")
    if "release-trust" not in detail or "GCL_RELEASE_TRUST_APP_ID" not in detail:
        errors.append("post_merge_attestation: failure detail must bind the protected environment and unavailable App ID")
    if record.get("remediation_state") != "PENDING_PROTECTED_REMEDIATION_MERGE":
        errors.append("post_merge_attestation: historical remediation record must preserve its pending state")
    if record.get("protected_completion_declared") is not False:
        errors.append("post_merge_attestation: historical protected completion must remain false")
    return errors


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    return hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()


def is_ancestor(ancestor: str, descendant: str) -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return completed.returncode == 0


def completion_progression_errors(
    evidence: dict,
    completion: dict,
    validation_head: str,
    ancestor_check: AncestorCheck,
) -> list[str]:
    """Validate forward-only live-state progression from an immutable closure snapshot."""
    errors: list[str] = []
    current_derivation = completion.get("derived_from_protected_head")
    historical_observed = evidence.get("observed_protected_head")

    if not isinstance(current_derivation, str) or not SHA_RE.fullmatch(current_derivation):
        return ["terminal_closure: current completion derivation head is invalid"]
    if not isinstance(historical_observed, str) or not SHA_RE.fullmatch(historical_observed):
        return ["terminal_closure: historical observed protected head is invalid"]
    if not SHA_RE.fullmatch(validation_head):
        return ["terminal_closure: validation head is invalid"]

    if not ancestor_check(historical_observed, current_derivation):
        errors.append(
            "terminal_closure: current completion derivation head does not descend from the historical terminal head"
        )
    if not ancestor_check(current_derivation, validation_head):
        errors.append(
            "terminal_closure: current completion derivation head is not ancestral to validation head"
        )
    return errors


def validate_terminal_closure() -> list[str]:
    errors, record = schema_errors(
        TERMINAL_CLOSURE_SCHEMA_PATH,
        TERMINAL_CLOSURE_PATH,
        "terminal_closure",
    )
    if errors:
        return errors

    try:
        historical = json.loads(ATTESTATION_PATH.read_text(encoding="utf-8"))
        completion = json.loads(COMPLETION_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"terminal_closure: dependency unreadable: {exc}"]

    historical_ref = record["historical_attestation"]
    if historical_ref["blob_sha"] != git_blob_sha(ATTESTATION_PATH):
        errors.append("terminal_closure: historical attestation blob mismatch")
    if historical.get("disposition_timing") != historical_ref["disposition_timing"]:
        errors.append("terminal_closure: historical disposition timing drift")
    if historical.get("protected_completion_declared") is not historical_ref["historical_protected_completion_declared"]:
        errors.append("terminal_closure: historical completion state drift")

    evidence = record["post_merge_evidence"]
    if evidence["completion_semantics_changed"] is not False:
        errors.append("terminal_closure: fixed-point readback must report unchanged semantics")
    if evidence["completion_state_pull_request"] is not None:
        errors.append("terminal_closure: terminal readback must not create a completion-state PR")
    if evidence["open_successor_completion_state_prs"] != 0:
        errors.append("terminal_closure: successor completion-state PR count must be zero")
    if evidence["mirrors_current"] is not True:
        errors.append("terminal_closure: all configured mirrors must be current")
    if record.get("protected_completion_declared") is not True:
        errors.append("terminal_closure: protected completion must be declared")

    if (ROOT / ".git").exists():
        current_head = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        observed = evidence["observed_protected_head"]
        errors.extend(completion_progression_errors(evidence, completion, current_head, is_ancestor))
        if not is_ancestor(observed, current_head):
            errors.append("terminal_closure: observed protected head is not ancestral to validation head")
        for field in (
            "environment_binding_remediation",
            "completion_state_transition",
            "fixed_point_remediation",
        ):
            merge_commit = record[field]["merge_commit"]
            if not is_ancestor(merge_commit, observed):
                errors.append(f"terminal_closure: {field} merge is not ancestral to observed protected head")
        if not is_ancestor(evidence["completion_derivation_head"], observed):
            errors.append("terminal_closure: retained derivation head is not ancestral to observed protected head")
    return errors


validate_workflows = validate_workflows_v3
implementation.validate_workflows = validate_workflows_v3


def main() -> int:
    result = routed.main()
    if result:
        return result
    errors = [*validate_post_merge_attestation(), *validate_terminal_closure()]
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"administrative automation closure validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("administrative automation historical attestation and terminal closure overlay are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
