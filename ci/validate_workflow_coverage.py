#!/usr/bin/env python3
"""Validate repository workflow reachability, deployment gating, and external evidence."""
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
IMMUTABLE_ACTION = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")
READ_ONLY_PERMISSIONS = {"contents": "read"}
EXPECTED_WORKFLOWS = {
    "bsd-wp03-substrate.yml",
    "bsd-wp04-target.yml",
    "ci.yml",
    "gcl-conformance.yml",
    "oz-next-004-independent-review.yml",
    "oz-rt-apery-brow.yml",
    "pages.yml",
    "pc-wp04.yml",
    "pc-wp05.yml",
    "release-trust-admin.yml",
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


def _job_hardening_errors(name: str, workflow: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if "concurrency" not in workflow:
        errors.append(f"{name}: explicit concurrency control is required")
    if workflow.get("permissions") != READ_ONLY_PERMISSIONS:
        errors.append(f"{name}: top-level permissions must be exactly contents: read")

    for job_id, job in workflow.get("jobs", {}).items():
        if "uses" not in job and "timeout-minutes" not in job:
            errors.append(f"{name}:{job_id}: timeout-minutes is required")
        if "uses" in job and not IMMUTABLE_ACTION.fullmatch(str(job.get("uses", ""))):
            errors.append(
                f"{name}:{job_id}: reusable workflow reference must use a full commit SHA"
            )
        job_permissions = job.get("permissions")
        if name != "pages.yml" and job_permissions not in (None, {}, READ_ONLY_PERMISSIONS):
            errors.append(
                f"{name}:{job_id}: non-Pages job permissions may not exceed contents: read"
            )
        for step in job.get("steps", []):
            uses = str(step.get("uses", ""))
            if uses and not uses.startswith("./") and not IMMUTABLE_ACTION.fullmatch(uses):
                errors.append(f"{name}:{job_id}: action reference must use a full commit SHA: {uses}")
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
        except Exception as exc:  # pragma: no cover
            errors.append(f"{name}: invalid workflow YAML: {exc}")
            continue
        parsed[name] = workflow
        errors.extend(_job_hardening_errors(name, workflow))

    policy = parsed.get("ci.yml")
    if policy:
        trigger = _trigger(policy)
        for required in ("pull_request", "push", "workflow_dispatch"):
            if required not in trigger:
                errors.append(f"ci.yml: missing {required} trigger")
        if "main" not in _as_list(trigger.get("push", {}).get("branches")):
            errors.append("ci.yml: push trigger must cover main")
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
            "python3 ci/validate_repository_execution.py",
            "python3 ci/test_repository_execution.py",
            "python -m unittest discover -s tests -p 'test_*.py'",
            "python3 ci/validate_workflow_coverage.py",
            "python3 ci/test_workflow_coverage.py",
            "evidence/UC-WP02-MATHCERT.json",
            "fixtures/formal/PC-WP04",
            "bash ci/check_lean.sh",
            "name: validated-site",
            "validated-site.tar.gz.sha256",
            "retention-days: 1",
        ):
            if marker not in policy_text:
                errors.append(f"ci.yml: missing workflow coverage marker {marker}")

        external_job = policy.get("jobs", {}).get("union-closed-mathcert", {})
        external_checkouts = []
        for step in external_job.get("steps", []):
            uses = str(step.get("uses", ""))
            options = step.get("with", {})
            if uses.startswith("actions/checkout@") and options.get("repository"):
                external_checkouts.append(options)
        if len(external_checkouts) != 1:
            errors.append(
                "ci.yml: union-closed-mathcert must contain exactly one explicit external checkout"
            )
        else:
            checkout = external_checkouts[0]
            if checkout.get("repository") != evidence.get("repository"):
                errors.append(
                    "ci.yml: external checkout repository must match audited evidence repository"
                )
            if checkout.get("ref") != evidence.get("commit"):
                errors.append("ci.yml: external checkout ref must match audited evidence commit")
            if checkout.get("path") != "external/MATHCERT":
                errors.append("ci.yml: external checkout path must be external/MATHCERT")

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
        expected_build_permissions = {
            "actions": "read",
            "contents": "read",
            "pages": "write",
        }
        expected_deploy_permissions = {"pages": "write", "id-token": "write"}
        if build.get("permissions") != expected_build_permissions:
            errors.append(
                "pages.yml: build permissions must be exactly actions: read, contents: read, and pages: write"
            )
        if deploy.get("permissions") != expected_deploy_permissions:
            errors.append(
                "pages.yml: deploy permissions must be exactly pages: write and id-token: write"
            )
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

    admin = parsed.get("release-trust-admin.yml")
    if admin:
        trigger = _trigger(admin)
        if set(trigger) != {"workflow_dispatch"}:
            errors.append("release-trust-admin.yml: administration must be manually dispatched only")
        admin_text = texts["release-trust-admin.yml"]
        for marker in (
            "environment: release-trust",
            "actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1",
            "app-id: ${{ secrets.GCL_RELEASE_TRUST_APP_ID }}",
            "private-key: ${{ secrets.GCL_RELEASE_TRUST_PRIVATE_KEY }}",
            "GCL_REPOSITORY_ADMIN_TOKEN: ${{ steps.app-token.outputs.token }}",
            "python ci/release_trust_admin.py --mode validate",
            "--wait-seconds 1200",
            "--close-child-issues",
            "name: release-trust-evidence",
            "retention-days: 90",
        ):
            if marker not in admin_text:
                errors.append(f"release-trust-admin.yml: missing administration gate {marker}")

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
        "workflow inventory, least-privilege permissions, immutable actions, repository execution, "
        "exact artifact publication, release-trust administration, RH continuity, and external evidence are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
