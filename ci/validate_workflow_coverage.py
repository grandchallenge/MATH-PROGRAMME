#!/usr/bin/env python3
"""Validate repository workflow reachability, deployment gating, and external evidence."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from validate_rh_continuity import rh_continuity_errors

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
EXPECTED_WORKFLOWS = {
    "bsd-wp03-substrate.yml",
    "bsd-wp04-target.yml",
    "ci.yml",
    "pages.yml",
    "pc-wp04.yml",
    "pc-wp05.yml",
}


def load_yaml_text(text: str) -> dict[str, Any]:
    data = yaml.load(text, Loader=yaml.BaseLoader)
    if not isinstance(data, dict):
        raise ValueError("workflow root must be a mapping")
    return data


def workflow_texts(root: Path = ROOT) -> dict[str, str]:
    return {
        path.name: path.read_text(encoding="utf-8")
        for path in sorted((root / ".github" / "workflows").glob("*.y*ml"))
    }


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value is None:
        return []
    return [str(value)]


def _checkout_errors(name: str, workflow: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for job_id, job in workflow.get("jobs", {}).items():
        if "timeout-minutes" not in job:
            errors.append(f"{name}:{job_id}: timeout-minutes is required")
        for step in job.get("steps", []):
            uses = str(step.get("uses", ""))
            if uses.startswith("actions/checkout@"):
                options = step.get("with", {})
                if str(options.get("persist-credentials", "")).lower() != "false":
                    errors.append(
                        f"{name}:{job_id}: checkout must set persist-credentials: false"
                    )
    return errors


def _trigger(workflow: dict[str, Any]) -> dict[str, Any]:
    value = workflow.get("on", {})
    return value if isinstance(value, dict) else {}


def external_evidence_errors(root: Path = ROOT, evidence: dict[str, Any] | None = None) -> list[str]:
    if evidence is None:
        evidence = json.loads((root / "evidence/UC-WP02-MATHCERT.json").read_text(encoding="utf-8"))
    schema = json.loads(
        (root / "schemas/cross_repository_evidence.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    errors = [
        f"UC-WP02-MATHCERT{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(evidence), key=lambda item: list(item.path))
    ]
    if evidence.get("repository") != "grandchallenge/MATHCERT":
        errors.append("UC-WP02-MATHCERT: repository must be grandchallenge/MATHCERT")
    if evidence.get("command") != ["bash", "ci/check_lean.sh"]:
        errors.append("UC-WP02-MATHCERT: command must run the complete MATHCERT certification gate")
    required_paths = {
        "MathCert/Domains/UnionClosed/Basic.lean",
        "MathCert/Domains/UnionClosed/FranklStatement.lean",
        "MathCert/Domains/UnionClosed/SingletonCase.lean",
        "certificates/exact/union_closed_n_le_4.json",
        "ci/replay_certificates.py",
        "ci/check_lean.sh",
    }
    if not required_paths <= set(evidence.get("paths", [])):
        errors.append("UC-WP02-MATHCERT: required formal and bounded replay paths are incomplete")
    return errors


def workflow_coverage_errors(
    root: Path = ROOT,
    texts: dict[str, str] | None = None,
    evidence: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    texts = workflow_texts(root) if texts is None else texts
    names = set(texts)
    for missing in sorted(EXPECTED_WORKFLOWS - names):
        errors.append(f"workflow inventory: missing governed workflow {missing}")
    for extra in sorted(names - EXPECTED_WORKFLOWS):
        errors.append(f"workflow inventory: unregistered workflow {extra}")

    parsed: dict[str, dict[str, Any]] = {}
    for name, text in texts.items():
        try:
            workflow = load_yaml_text(text)
        except Exception as exc:  # pragma: no cover - defensive parser boundary
            errors.append(f"{name}: invalid workflow YAML: {exc}")
            continue
        parsed[name] = workflow
        errors.extend(_checkout_errors(name, workflow))
        if "permissions" not in workflow:
            errors.append(f"{name}: explicit least-privilege permissions are required")

    policy = parsed.get("ci.yml")
    if policy:
        trigger = _trigger(policy)
        for required in ("pull_request", "push", "workflow_dispatch"):
            if required not in trigger:
                errors.append(f"ci.yml: missing {required} trigger")
        if "main" not in _as_list(trigger.get("push", {}).get("branches")):
            errors.append("ci.yml: push trigger must cover main")
        if policy.get("permissions", {}).get("contents") != "read":
            errors.append("ci.yml: contents permission must be read")
        required_jobs = {
            "validate-json",
            "log-gcd-lean",
            "pc-wp04-lean",
            "union-closed-mathcert",
        }
        missing_jobs = required_jobs - set(policy.get("jobs", {}))
        for job in sorted(missing_jobs):
            errors.append(f"ci.yml: missing required policy job {job}")
        policy_text = texts["ci.yml"]
        for marker in (
            "python3 ci/validate_campaign_replays.py",
            "python3 ci/test_campaign_replays.py",
            "python3 ci/validate_workflow_coverage.py",
            "python3 ci/test_workflow_coverage.py",
            "evidence/UC-WP02-MATHCERT.json",
            "fixtures/formal/PC-WP04",
        ):
            if marker not in policy_text:
                errors.append(f"ci.yml: missing workflow coverage marker {marker}")

    pages = parsed.get("pages.yml")
    if pages:
        trigger = _trigger(pages)
        if set(trigger) != {"workflow_run"}:
            errors.append("pages.yml: deployment must be triggered only by workflow_run")
        workflow_run = trigger.get("workflow_run", {})
        if "Programme policy checks" not in _as_list(workflow_run.get("workflows")):
            errors.append("pages.yml: deployment must depend on Programme policy checks")
        if "completed" not in _as_list(workflow_run.get("types")):
            errors.append("pages.yml: workflow_run trigger must wait for completion")
        pages_text = texts["pages.yml"]
        for marker in (
            "github.event.workflow_run.conclusion == 'success'",
            "github.event.workflow_run.head_branch == 'main'",
            "github.event.workflow_run.event == 'push'",
            "ref: ${{ github.event.workflow_run.head_sha }}",
        ):
            if marker not in pages_text:
                errors.append(f"pages.yml: missing publication gate {marker}")

    errors.extend(external_evidence_errors(root, evidence))
    errors.extend(rh_continuity_errors(root))
    return errors


def main() -> int:
    errors = workflow_coverage_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"workflow coverage validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        "workflow inventory, campaign replay reachability, RH continuity, deployment gate, "
        "and external evidence are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
