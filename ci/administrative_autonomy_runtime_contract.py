from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from administrative_automation import canonical_digest, iso_z, parse_datetime
from autonomy_github import AutonomyError, Client

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_PATH = ROOT / "governance" / "administrative_autonomy_runtime_integration.json"
RUNTIME_SCHEMA_PATH = ROOT / "schemas" / "administrative_autonomy_runtime_integration.schema.json"
RECORD_SCHEMA_PATH = ROOT / "schemas" / "administrative_autonomous_maintenance_record.schema.json"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_REPOSITORIES = {
    "grandchallenge/MATH-PROGRAMME",
    "grandchallenge/MATHFORGE",
    "grandchallenge/MATHSOLVE",
    "grandchallenge/MATHCERT",
    "grandchallenge/INTELLECT",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(value: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    return [
        f"schema: {'/'.join(str(part) for part in error.absolute_path)}: {error.message}"
        for error in validator.iter_errors(value)
    ]


def validate_runtime_contract(runtime: dict[str, Any]) -> list[str]:
    errors = schema_errors(runtime, load_json(RUNTIME_SCHEMA_PATH))
    automated = set(runtime.get("automated_procedures", []))
    manual = set(runtime.get("manual_procedures", []))
    if automated & manual:
        errors.append("automated and manual procedure sets overlap")
    if "pilot_review" not in manual or "constitutional_review" not in manual:
        errors.append("pilot and constitutional review must remain manual")
    if runtime.get("candidate_identity", {}).get("app_id") == runtime.get("referee_identity", {}).get("app_id"):
        errors.append("Candidate and Referee app identities collide")
    if runtime.get("candidate_identity", {}).get("login") == runtime.get("referee_identity", {}).get("login"):
        errors.append("Candidate and Referee logins collide")
    authority = runtime.get("authority_boundary", {})
    if authority.get("automated_human_steward_disposition") is not False:
        errors.append("Human Steward impersonation is prohibited")
    if authority.get("control_plane_change") is not False or authority.get("scope_expansion") is not False:
        errors.append("routine runtime may not change the control plane or scope")
    boundaries = runtime.get("claim_boundaries", {})
    if not boundaries or any(item is not False for item in boundaries.values()):
        errors.append("runtime claim boundaries must remain false")
    return errors


def validate_activation(runtime: dict[str, Any], activation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "activation_id": runtime["activation_id"],
        "transition_id": runtime["transition_id"],
        "repository": runtime["repository"],
        "state": runtime["activation_state_required"],
    }
    for key, value in expected.items():
        if activation.get(key) != value:
            errors.append(f"activation {key} drift")
    if activation.get("identity_separation") is not True:
        errors.append("protected activation identity separation is absent")
    identities = (
        ("candidate_identity", runtime["candidate_identity"]),
        ("administrator_identity", runtime["administrator_identity"]),
        ("referee_identity", runtime["referee_identity"]),
    )
    for field, expected_identity in identities:
        actual = activation.get(field, {})
        if actual.get("login") != expected_identity["login"] or actual.get("app_id") != expected_identity["app_id"]:
            errors.append(f"activation {field} drift")
    bypass = activation.get("ruleset_bypass", {})
    if (
        bypass.get("ruleset_id") != runtime["ruleset_id"]
        or bypass.get("actor_id") != runtime["administrator_identity"]["app_id"]
        or bypass.get("mode") != "pull_request"
        or bypass.get("direct_push") is not False
        or bypass.get("canary_merge_uses_bypass") is not False
    ):
        errors.append("protected activation ruleset boundary drift")
    authority = activation.get("authority_boundary", {})
    if authority.get("automated_human_steward_disposition") is not False:
        errors.append("protected activation permits Human Steward impersonation")
    if authority.get("direct_protected_push") is not False:
        errors.append("protected activation permits direct protected push")
    boundaries = activation.get("claim_boundaries", {})
    if not boundaries or any(item is not False for item in boundaries.values()):
        errors.append("protected activation claim boundaries drift")
    return errors


def manifest_digest(manifest: dict[str, Any]) -> str:
    return hashlib.sha256((json.dumps(manifest, sort_keys=True, separators=(",", ":"))).encode("utf-8")).hexdigest()


def record_path_for(runtime: dict[str, Any], manifest: dict[str, Any], existing_names: list[str]) -> tuple[str, str]:
    first = runtime["first_production_occurrence"]
    if manifest["occurrence_key"] == first["occurrence_key"]:
        record_id = first["record_id"]
    else:
        layout = runtime["record_layout"][manifest["procedure_id"]]
        date = parse_datetime(manifest["scheduled_due_at"]).strftime("%Y-%m-%d")
        prefix = layout["id_prefix"]
        pattern = re.compile(
            rf"^{re.escape(prefix)}-{re.escape(date)}-([0-9]{{3}})[.]json$"
        )
        sequence = 1
        for name in existing_names:
            match = pattern.fullmatch(name)
            if match:
                sequence = max(sequence, int(match.group(1)) + 1)
        record_id = f"{prefix}-{date}-{sequence:03d}"
    directory = runtime["record_layout"][manifest["procedure_id"]]["directory"]
    return record_id, f"{directory}/{record_id}.json"


def repository_state(client: Client, repositories: list[str]) -> list[dict[str, Any]]:
    if set(repositories) != ALLOWED_REPOSITORIES or len(repositories) != 5:
        raise AutonomyError("five-repository evidence scope drift")
    result: list[dict[str, Any]] = []
    for repository in repositories:
        repo = client.get(f"/repos/{repository}")
        default_branch = str(repo.get("default_branch") or "")
        if default_branch != "main":
            raise AutonomyError(f"{repository}: default branch drift")
        branch = client.get(f"/repos/{repository}/branches/main")
        pulls = client.get(f"/repos/{repository}/pulls?state=open&per_page=100")
        result.append(
            {
                "repository": repository,
                "default_branch": "main",
                "protected_head": branch["commit"]["sha"],
                "open_pull_requests": [
                    {
                        "number": int(item["number"]),
                        "head": item["head"]["sha"],
                        "base": item["base"]["sha"],
                        "draft": bool(item["draft"]),
                        "author": item["user"]["login"],
                    }
                    for item in pulls
                ],
            }
        )
    return sorted(result, key=lambda item: item["repository"])


def build_record(
    runtime: dict[str, Any],
    activation: dict[str, Any],
    manifest: dict[str, Any],
    record_id: str,
    state: list[dict[str, Any]],
    now: datetime,
) -> dict[str, Any]:
    due = parse_datetime(manifest["scheduled_due_at"])
    lateness = max(0, int((now - due).total_seconds() // 60))
    mirrors = [
        {**item, "synchronization_required": True}
        for item in runtime["mirrors"]
    ]
    candidate = runtime["candidate_identity"]
    administrator = runtime["administrator_identity"]
    referee = runtime["referee_identity"]
    return {
        "$schema": "../../schemas/administrative_autonomous_maintenance_record.schema.json",
        "schema_version": "1.0.0",
        "record_id": record_id,
        "procedure_id": manifest["procedure_id"],
        "control_id": runtime["control_id"],
        "runtime_id": runtime["runtime_id"],
        "status": "COMPLETE_AUTONOMOUS",
        "scheduled_due_at": iso_z(due),
        "execution_started_at": iso_z(now),
        "evidence_closed_at": iso_z(now),
        "evidence_mode": "CONTEMPORANEOUS",
        "lateness_minutes_at_start": lateness,
        "source_candidate": {
            "occurrence_key": manifest["occurrence_key"],
            "manifest_path": manifest["manifest_path"],
            "manifest_digest": manifest_digest(manifest),
            "prepared_at": manifest["generated_at"],
            "freeze_at": manifest["freeze_at"],
            "source_protected_head": manifest["source_protected_head"],
            "issue_number": int(manifest["issue_number"]),
            "pull_request_number": int(manifest["pull_request_number"]),
            "branch": manifest["branch"],
        },
        "activation_binding": {
            "activation_id": activation["activation_id"],
            "state": activation["state"],
            "transition_merge_head": activation["transition_merge_head"],
            "ruleset_id": runtime["ruleset_id"],
            "candidate_identity": candidate,
            "administrator_identity": administrator,
            "referee_identity": referee,
            "identity_separation": True,
        },
        "repository_state": state,
        "execution_contract": {
            "candidate_author": candidate["login"],
            "referee_actor": referee["login"],
            "merge_executor": candidate["login"],
            "expected_head_required": True,
            "required_checks_source": f"live ruleset {runtime['ruleset_id']}",
            "referee_disposition_before_merge": True,
            "post_disposition_check_stabilization": True,
            "clean_state_required": True,
            "bypass_used": False,
            "direct_protected_push": False,
            "human_steward_disposition_required": False,
            "human_steward_identity_asserted": False,
        },
        "tracker_mirrors": mirrors,
        "authority_boundary": {
            "routine_bounded_administrative_completion": True,
            "automated_exact_head_referee_disposition": True,
            "automated_merge": True,
            "automated_human_steward_disposition": False,
            "control_plane_change": False,
            "scope_expansion": False,
        },
        "claim_boundaries": dict(runtime["claim_boundaries"]),
    }


def validate_record(record: dict[str, Any]) -> list[str]:
    errors = schema_errors(record, load_json(RECORD_SCHEMA_PATH))
    repositories = record.get("repository_state", [])
    names = [item.get("repository") for item in repositories if isinstance(item, dict)]
    if len(names) != 5 or set(names) != ALLOWED_REPOSITORIES or len(names) != len(set(names)):
        errors.append("record repository inventory drift")
    boundaries = record.get("claim_boundaries", {})
    if not boundaries or any(item is not False for item in boundaries.values()):
        errors.append("record claim boundary inflation")
    execution = record.get("execution_contract", {})
    if execution.get("human_steward_identity_asserted") is not False:
        errors.append("record asserts Human Steward identity")
    if execution.get("bypass_used") is not False:
        errors.append("record falsely exercises bypass")
    return errors