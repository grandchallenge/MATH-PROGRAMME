#!/usr/bin/env python3
"""Validate semantic workflow identity, dependency, runner, execution, and publication contracts."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_NAMES = {
    "bsd-wp03-substrate.yml": "BSD WP03 substrate replay",
    "bsd-wp04-target.yml": "BSD WP04 target scorecard",
    "ci.yml": "Programme policy checks",
    "pages.yml": "Deploy documentation site",
    "pc-wp04.yml": "PC-WP04 certificate checks",
    "pc-wp05.yml": "PC-WP05 archival checks",
}
PYTHON_MINOR_LINE = "3.12"
POLICY_REQUIREMENTS = ("jsonschema==4.26.0", "PyYAML==6.0.3")
DOCS_REQUIREMENTS = (
    "mkdocs==1.6.1",
    "mkdocs-material==9.7.7",
    "pymdown-extensions==11.0.1",
    "PyYAML==6.0.3",
)
POLICY_INSTALL = "python -m pip install --requirement requirements/policy.txt"
DOCS_INSTALL = "python -m pip install --requirement requirements/docs.txt"
EXTERNAL_POLICY_INSTALL = (
    'python -m pip install --requirement "$GITHUB_WORKSPACE/requirements/policy.txt"'
)
UNIT_TEST_COMMAND = "python -m unittest discover -s tests -p 'test_*.py'"
PINNED_REUSABLE_WORKFLOW = re.compile(r"^[^@\s]+/\.github/workflows/[^@\s]+@[0-9a-f]{40}$")


def load_workflows(root: Path = ROOT) -> dict[str, dict[str, Any]]:
    workflows: dict[str, dict[str, Any]] = {}
    for path in sorted((root / ".github" / "workflows").glob("*.y*ml")):
        data = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        workflows[path.name] = data if isinstance(data, dict) else {}
    return workflows


def job_runs(workflow: dict[str, Any], job_id: str) -> list[str]:
    job = workflow.get("jobs", {}).get(job_id, {})
    return [str(step.get("run", "")) for step in job.get("steps", []) if step.get("run")]


def all_runs(workflow: dict[str, Any]) -> list[str]:
    runs: list[str] = []
    for job in workflow.get("jobs", {}).values():
        runs.extend(str(step.get("run", "")) for step in job.get("steps", []) if step.get("run"))
    return runs


def command_lines(runs: list[str]) -> set[str]:
    return {
        line.strip()
        for run in runs
        for line in run.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def requirement_lines(root: Path, relative: str) -> tuple[str, ...]:
    path = root / relative
    if not path.is_file():
        return ()
    return tuple(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def contains_command(runs: list[str], command: str) -> bool:
    return command in command_lines(runs)


def contains_marker(runs: list[str], marker: str) -> bool:
    return any(marker in line for line in command_lines(runs))


def steps_using(job: dict[str, Any], action_prefix: str) -> list[dict[str, Any]]:
    return [
        step
        for step in job.get("steps", [])
        if str(step.get("uses", "")).startswith(action_prefix)
    ]


def workflow_semantic_errors(
    root: Path = ROOT,
    workflows: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    errors: list[str] = []
    workflows = load_workflows(root) if workflows is None else workflows

    names: list[str] = []
    for filename, expected in EXPECTED_NAMES.items():
        workflow = workflows.get(filename, {})
        actual = str(workflow.get("name", ""))
        names.append(actual)
        if actual != expected:
            errors.append(f"{filename}: workflow name must be exactly {expected!r}, found {actual!r}")
    duplicates = {name for name in names if name and names.count(name) > 1}
    for name in sorted(duplicates):
        errors.append(f"workflow names must be unique; duplicate {name!r}")

    setup_python_steps = 0
    for filename, workflow in workflows.items():
        for job_id, job in workflow.get("jobs", {}).items():
            reusable = str(job.get("uses", ""))
            if reusable:
                if not PINNED_REUSABLE_WORKFLOW.fullmatch(reusable):
                    errors.append(
                        f"{filename}:{job_id}: reusable workflow must use a full commit SHA"
                    )
                continue
            if str(job.get("runs-on", "")) != "ubuntu-24.04":
                errors.append(f"{filename}:{job_id}: runs-on must be pinned to ubuntu-24.04")
            for step in job.get("steps", []):
                if str(step.get("uses", "")).startswith("actions/setup-python@"):
                    setup_python_steps += 1
                    version = str(step.get("with", {}).get("python-version", ""))
                    if version != PYTHON_MINOR_LINE:
                        errors.append(
                            f"{filename}:{job_id}: setup-python must use governed minor line "
                            f"{PYTHON_MINOR_LINE!r}, found {version!r}"
                        )
        for line in command_lines(all_runs(workflow)):
            if "pip install" in line and "--requirement" not in line:
                errors.append(f"{filename}: ad hoc or unpinned pip install is forbidden: {line}")
    if setup_python_steps == 0:
        errors.append("governed workflows must contain at least one setup-python step")

    if requirement_lines(root, "requirements/policy.txt") != POLICY_REQUIREMENTS:
        errors.append("requirements/policy.txt must contain the exact governed policy pins")
    if requirement_lines(root, "requirements/docs.txt") != DOCS_REQUIREMENTS:
        errors.append("requirements/docs.txt must contain the exact governed documentation pins")

    policy = workflows.get("ci.yml", {})
    validate_job = policy.get("jobs", {}).get("validate-json", {})
    validate_runs = job_runs(policy, "validate-json")
    if not contains_command(validate_runs, POLICY_INSTALL):
        errors.append("ci.yml:validate-json must install requirements/policy.txt")
    if not contains_command(validate_runs, DOCS_INSTALL):
        errors.append("ci.yml:validate-json must install requirements/docs.txt")
    for command in (
        UNIT_TEST_COMMAND,
        "python3 ci/validate_policy_reachability.py",
        "python3 ci/test_policy_reachability.py",
        "python3 ci/validate_repository_execution.py",
        "python3 ci/test_repository_execution.py",
        "python3 ci/validate_workflow_semantics.py",
        "python3 ci/test_workflow_semantics.py",
    ):
        if not contains_command(validate_runs, command):
            errors.append(f"ci.yml:validate-json is missing executable coverage command {command}")

    upload_steps = steps_using(validate_job, "actions/upload-artifact@")
    validated_site_steps = [
        step for step in upload_steps if step.get("with", {}).get("name") == "validated-site"
    ]
    if len(validated_site_steps) != 1:
        errors.append("ci.yml:validate-json must upload exactly one validated-site artifact")
    else:
        step = validated_site_steps[0]
        condition = str(step.get("if", ""))
        if "github.event_name == 'push'" not in condition or "github.ref == 'refs/heads/main'" not in condition:
            errors.append("ci.yml: validated-site upload must be limited to pushes on main")
        options = step.get("with", {})
        if str(options.get("retention-days", "")) != "1":
            errors.append("ci.yml: validated-site artifact retention must be exactly one day")
        paths = str(options.get("path", ""))
        for required in ("validated-site.tar.gz", "validated-site.tar.gz.sha256"):
            if required not in paths:
                errors.append(f"ci.yml: validated-site upload is missing {required}")
    for marker in (
        "tar --sort=name",
        "sha256sum validated-site.tar.gz",
        "git show -s --format=%ct HEAD",
    ):
        if not contains_marker(validate_runs, marker):
            errors.append(f"ci.yml: missing deterministic validated-site packaging marker {marker}")

    if not contains_command(job_runs(policy, "pc-wp04-lean"), POLICY_INSTALL):
        errors.append("ci.yml:pc-wp04-lean must install requirements/policy.txt")
    if not contains_command(
        job_runs(policy, "union-closed-mathcert"), EXTERNAL_POLICY_INSTALL
    ):
        errors.append(
            "ci.yml:union-closed-mathcert must install the root policy requirements by absolute workspace path"
        )

    if not contains_command(
        job_runs(workflows.get("pc-wp04.yml", {}), "pc-wp04-lean"), POLICY_INSTALL
    ):
        errors.append("pc-wp04.yml must install requirements/policy.txt")
    if not contains_command(
        job_runs(workflows.get("pc-wp05.yml", {}), "archival-policy"), POLICY_INSTALL
    ):
        errors.append("pc-wp05.yml archival policy must install requirements/policy.txt")

    pages = workflows.get("pages.yml", {})
    concurrency = pages.get("concurrency", {})
    if str(concurrency.get("cancel-in-progress", "")).lower() != "true":
        errors.append("pages.yml: concurrency must cancel stale in-progress publications")
    build = pages.get("jobs", {}).get("build", {})
    build_if = str(build.get("if", ""))
    for clause in (
        "github.event.workflow_run.conclusion == 'success'",
        "github.event.workflow_run.head_branch == 'main'",
        "github.event.workflow_run.event == 'push'",
    ):
        if clause not in build_if:
            errors.append(f"pages.yml: build.if is missing semantic gate {clause}")
    checkout_steps = steps_using(build, "actions/checkout@")
    if len(checkout_steps) != 1:
        errors.append("pages.yml: build must contain exactly one checkout step")
    elif checkout_steps[0].get("with", {}).get("ref") != "${{ github.event.workflow_run.head_sha }}":
        errors.append("pages.yml: checkout must use the validated workflow_run.head_sha")
    build_runs = job_runs(pages, "build")
    if contains_command(build_runs, DOCS_INSTALL) or contains_command(build_runs, "mkdocs build --strict"):
        errors.append("pages.yml: Pages must deploy the policy artifact without resolving dependencies or rebuilding MkDocs")
    for marker in (
        "refs/heads/main:refs/remotes/origin/main",
        "git rev-parse HEAD",
        "git rev-parse refs/remotes/origin/main",
        "actions/runs/{run_id}/artifacts",
        'artifact.get("name") == "validated-site"',
        "hashlib.sha256(artifact_zip)",
        "hashlib.sha256(archive_path.read_bytes())",
        'archive.extractall(site, filter="data")',
    ):
        if not contains_marker(build_runs, marker):
            errors.append(f"pages.yml: missing exact-artifact publication check {marker}")

    deploy = pages.get("jobs", {}).get("deploy", {})
    environment = deploy.get("environment", {})
    if str(environment.get("url", "")) != "${{ steps.deployment.outputs.page_url }}":
        errors.append("pages.yml: deploy environment must expose the deploy-pages page_url output")
    deploy_steps = steps_using(deploy, "actions/deploy-pages@")
    if len(deploy_steps) != 1 or deploy_steps[0].get("id") != "deployment":
        errors.append("pages.yml: deploy-pages step must have id deployment")

    return errors


def main() -> int:
    errors = workflow_semantic_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"workflow semantic validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(
        "workflow names, runners, Python minor line, dependencies, repository execution, "
        "exact artifact promotion, and publication freshness are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
