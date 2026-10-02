#!/usr/bin/env python3
"""Validate repository workflow inventory, hardening, formal routing, and publication coverage."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from validate_rh_continuity import rh_continuity_errors

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
ROUTING_REGISTRY = ROOT / ".ghos-routing" / "workflows.json"
FORMAL_REGISTRY = ROOT / "governance" / "formal_validation_registry.json"
IMMUTABLE_ACTION = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
LOCAL_REUSABLE_WORKFLOW = re.compile(r"^\./\.github/workflows/[^/@\s]+[.]ya?ml$")
READ_ONLY_PERMISSIONS = {"contents": "read"}


def _expected_workflows() -> set[str]:
    try:
        registry = json.loads(ROUTING_REGISTRY.read_text(encoding="utf-8"))
        return {
            Path(entry["path"]).name
            for entry in registry.get("workflows", [])
            if isinstance(entry, dict) and isinstance(entry.get("path"), str)
        }
    except (OSError, json.JSONDecodeError, KeyError):
        return set()


# Retained as a mutable compatibility surface because v2/v3 add older
# administrative profiles before invoking this validator.
EXPECTED_WORKFLOWS = _expected_workflows()


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


def _trigger(workflow: dict[str, Any]) -> dict[str, Any]:
    value = workflow.get("on", {})
    return value if isinstance(value, dict) else {}


def _job_hardening_errors(name: str, workflow: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if "concurrency" not in workflow:
        errors.append(f"{name}: explicit concurrency control is required")
    if workflow.get("permissions") != READ_ONLY_PERMISSIONS:
        errors.append(f"{name}: top-level permissions must be exactly contents: read")

    jobs = workflow.get("jobs", {})
    if not isinstance(jobs, dict):
        return errors + [f"{name}: jobs must be a mapping"]
    for job_id, job in jobs.items():
        if not isinstance(job, dict):
            errors.append(f"{name}:{job_id}: job must be a mapping")
            continue
        if "uses" not in job and "timeout-minutes" not in job:
            errors.append(f"{name}:{job_id}: timeout-minutes is required")
        if "uses" in job and not (
            LOCAL_REUSABLE_WORKFLOW.fullmatch(str(job.get("uses", "")))
            or IMMUTABLE_ACTION.fullmatch(str(job.get("uses", "")))
        ):
            errors.append(
                f"{name}:{job_id}: reusable workflow reference must be same-repository local or use a full commit SHA"
            )
        job_permissions = job.get("permissions")
        if name != "pages.yml" and job_permissions not in (None, {}, READ_ONLY_PERMISSIONS):
            errors.append(f"{name}:{job_id}: non-Pages job permissions may not exceed contents: read")
        for step in job.get("steps", []):
            if not isinstance(step, dict):
                continue
            uses = str(step.get("uses", ""))
            if uses and not uses.startswith("./") and not IMMUTABLE_ACTION.fullmatch(uses):
                errors.append(f"{name}:{job_id}: action reference must use a full commit SHA: {uses}")
            if uses.startswith("actions/checkout@"):
                options = step.get("with", {})
                if str(options.get("persist-credentials", "")).lower() != "false":
                    errors.append(f"{name}:{job_id}: checkout must set persist-credentials: false")
    return errors


def external_evidence_errors(root: Path = ROOT, evidence: dict[str, Any] | None = None) -> list[str]:
    if evidence is None:
        evidence = json.loads((root / "evidence/UC-WP02-MATHCERT.json").read_text(encoding="utf-8"))
    schema = json.loads((root / "schemas/cross_repository_evidence.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = [
        f"UC-WP02-MATHCERT{error.json_path}: {error.message}"
        for error in sorted(validator.iter_errors(evidence), key=lambda item: list(item.path))
    ]
    if evidence.get("repository") != "grandchallenge/MATHCERT":
        errors.append("UC-WP02-MATHCERT: repository must be grandchallenge/MATHCERT")
    if evidence.get("command") != ["bash", "ci/check_lean.sh"]:
        errors.append("UC-WP02-MATHCERT: command must run the complete MATHCERT certification gate")
    commit = str(evidence.get("commit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        errors.append("UC-WP02-MATHCERT: commit does not match an immutable 40-hex identity")
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


def _formal_registry_errors(
    root: Path,
    parsed: dict[str, dict[str, Any]],
    evidence: dict[str, Any],
    texts: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    try:
        registry = json.loads((root / "governance/formal_validation_registry.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"formal-validation registry invalid: {exc}"]
    lanes = registry.get("lanes", [])
    by_id = {lane.get("id"): lane for lane in lanes if isinstance(lane, dict)}
    for required in ("log-gcd", "pc-wp04", "union-closed-mathcert", "cmdg-cm4-p3"):
        if required not in by_id:
            errors.append(f"formal-validation registry: missing governed lane {required}")
    union = by_id.get("union-closed-mathcert", {})
    if union:
        if union.get("external_repository") != evidence.get("repository"):
            errors.append("formal-validation registry: Union-Closed external repository must match audited evidence repository")
        if union.get("external_ref") != evidence.get("commit"):
            errors.append("formal-validation registry: Union-Closed external ref must match audited evidence commit")
    p3 = by_id.get("cmdg-cm4-p3", {})
    if p3 and "CMDGCondensedCM4P3*.lean" not in p3.get("formal_sources", []):
        errors.append("formal-validation registry: P3 promotion source closure is incomplete")

    formal = parsed.get("formal-validation.yml")
    if formal:
        trigger = _trigger(formal)
        if not {"pull_request", "merge_group", "schedule", "workflow_dispatch"}.issubset(trigger):
            errors.append("formal-validation.yml: required material-routing triggers are incomplete")
        if "push" in trigger:
            errors.append("formal-validation.yml: direct push trigger is forbidden")
        jobs = formal.get("jobs", {})
        for required in ("impact", "formal-lane", "formal-validation"):
            if required not in jobs:
                errors.append(f"formal-validation.yml: missing required job {required}")
        text = texts.get("formal-validation.yml", "")
        for marker in (
            "ci/formal_validation.py classify",
            "fromJSON(needs.impact.outputs.formal_matrix)",
            "ci/formal_validation.py run",
            "name: formal-validation",
        ):
            if marker not in text:
                errors.append(f"formal-validation.yml: missing formal routing marker {marker}")
    return errors


def workflow_coverage_errors(
    root: Path = ROOT,
    texts: dict[str, str] | None = None,
    evidence: dict[str, Any] | None = None,
) -> list[str]:
    errors: list[str] = []
    texts = workflow_texts(root) if texts is None else texts
    if evidence is None:
        evidence = json.loads((root / "evidence/UC-WP02-MATHCERT.json").read_text(encoding="utf-8"))

    names = set(texts)
    for missing in sorted(EXPECTED_WORKFLOWS - names):
        errors.append(f"workflow inventory: missing governed workflow {missing}")
    for extra in sorted(names - EXPECTED_WORKFLOWS):
        errors.append(f"workflow inventory: unregistered workflow {extra}")

    parsed: dict[str, dict[str, Any]] = {}
    for name, text in texts.items():
        try:
            workflow = load_yaml_text(text)
        except Exception as exc:
            errors.append(f"{name}: invalid workflow YAML: {exc}")
            continue
        parsed[name] = workflow
        errors.extend(_job_hardening_errors(name, workflow))

    policy = parsed.get("ci.yml")
    if policy:
        trigger = _trigger(policy)
        for required in ("pull_request", "push", "merge_group", "workflow_dispatch", "schedule"):
            if required not in trigger:
                errors.append(f"ci.yml: missing {required} trigger")
        push = trigger.get("push", {})
        if not isinstance(push, dict) or "main" not in _as_list(push.get("branches")):
            errors.append("ci.yml: push trigger must cover main")
        required_jobs = {"impact", "policy-shard", "validate-json"}
        for job in sorted(required_jobs - set(policy.get("jobs", {}))):
            errors.append(f"ci.yml: missing required policy job {job}")
        for retired in ("log-gcd-lean", "pc-wp04-lean", "union-closed-mathcert"):
            if retired in policy.get("jobs", {}):
                errors.append(f"ci.yml: retired substantive formal job remains {retired}")
        policy_text = texts["ci.yml"]
        for marker in (
            "ci/policy_impact.py classify",
            "fromJSON(needs.impact.outputs.policy_shards)",
            "ci/run_policy_shard.py --shard",
            "name: validated-site",
            "validated-site.tar.gz.sha256",
            "retention-days: 1",
        ):
            if marker not in policy_text:
                errors.append(f"ci.yml: missing workflow coverage marker {marker}")
        # These contracts are intentionally routed through the policy shard registry.
        for marker in (
            "python3 ci/validate_campaign_replays.py",
            "python3 ci/test_campaign_replays.py",
            "python3 ci/validate_repository_execution.py",
            "python3 ci/test_repository_execution.py",
            "python3 ci/validate_workflow_coverage_v2.py",
            "python3 ci/test_workflow_coverage_v2.py",
            "python3 ci/validate_workflow_semantics.py",
            "python3 ci/test_workflow_semantics.py",
        ):
            if marker not in policy_text:
                errors.append(f"ci.yml: missing workflow coverage marker {marker}")

    errors.extend(_formal_registry_errors(root, parsed, evidence, texts))

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
        jobs = pages.get("jobs", {})
        build = jobs.get("build", {})
        deploy = jobs.get("deploy", {})
        expected_build_permissions = {"actions": "read", "contents": "read", "pages": "write"}
        expected_deploy_permissions = {"pages": "write", "id-token": "write"}
        if build.get("permissions") != expected_build_permissions:
            errors.append("pages.yml: build permissions must be exactly actions: read, contents: read, and pages: write")
        if deploy.get("permissions") != expected_deploy_permissions:
            errors.append("pages.yml: deploy permissions must be exactly pages: write and id-token: write")
        if deploy.get("needs") != "build":
            errors.append("pages.yml: deploy job must depend on build")
        environment = deploy.get("environment", {})
        if not isinstance(environment, dict) or environment.get("name") != "github-pages":
            errors.append("pages.yml: deploy environment must be github-pages")
        pages_text = texts["pages.yml"]
        for marker in (
            "github.event.workflow_run.conclusion == 'success'",
            "github.event.workflow_run.head_branch == 'main'",
            "github.event.workflow_run.event == 'push'",
            "ref: ${{ github.event.workflow_run.head_sha }}",
            "archive_download_url",
            'artifact.get("name") == "validated-site"',
            "workflow artifact digest mismatch",
            "validated-site inner digest mismatch",
            'archive.extractall(site, filter="data")',
        ):
            if marker not in pages_text:
                errors.append(f"pages.yml: missing publication gate {marker}")

    errors.extend(external_evidence_errors(root=root, evidence=evidence))
    errors.extend(rh_continuity_errors(root=root))
    return errors


def main() -> int:
    errors = workflow_coverage_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"workflow coverage validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("workflow coverage: GH-OS inventory, hardened execution, routed policy, material formal validation, exact evidence, Pages publication, and RH continuity are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
