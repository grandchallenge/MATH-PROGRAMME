#!/usr/bin/env python3
"""Validate semantic workflow, routing, replay, runner, and publication contracts."""
from __future__ import annotations

import json
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
EXTERNAL_POLICY_INSTALL = 'python -m pip install --requirement "$GITHUB_WORKSPACE/requirements/policy.txt"'
PINNED_REUSABLE_WORKFLOW = re.compile(r"^[^@\s]+/\.github/workflows/[^@\s]+@[0-9a-f]{40}$")
LOCAL_REUSABLE_WORKFLOW = re.compile(r"^\./\.github/workflows/[^@\s]+[.]ya?ml$")
SHARDS = (
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
REPOSITORY_REGRESSION_COMMAND = (
    "python3 ci/run_unittest_modules.py --discover-root tests --pattern test_*.py "
    "--report-json repository-regression-timing.json"
)


def load_workflows(root: Path = ROOT) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for path in sorted((root / ".github" / "workflows").glob("*.y*ml")):
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        out[path.name] = value if isinstance(value, dict) else {}
    return out


def job_runs(workflow: dict[str, Any], job_id: str) -> list[str]:
    return [
        str(step.get("run", ""))
        for step in workflow.get("jobs", {}).get(job_id, {}).get("steps", [])
        if step.get("run")
    ]


def all_runs(workflow: dict[str, Any]) -> list[str]:
    return [
        str(step.get("run", ""))
        for job in workflow.get("jobs", {}).values()
        for step in job.get("steps", [])
        if step.get("run")
    ]


def command_lines(runs: list[str]) -> set[str]:
    return {
        line.strip()
        for run in runs
        for line in run.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def contains_command(runs: list[str], command: str) -> bool:
    return command in command_lines(runs)


def marker(runs: list[str], value: str) -> bool:
    return any(value in line for line in command_lines(runs))


def steps_using(job: dict[str, Any], prefix: str) -> list[dict[str, Any]]:
    return [step for step in job.get("steps", []) if str(step.get("uses", "")).startswith(prefix)]


def requirement_lines(root: Path, relative: str) -> tuple[str, ...]:
    path = root / relative
    if not path.is_file():
        return ()
    return tuple(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    )


def registry_shards(root: Path) -> dict[str, set[str]]:
    path = root / "governance" / "policy_shard_registry.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    out: dict[str, set[str]] = {}
    for shard, entries in data.get("shards", {}).items():
        if not isinstance(entries, list):
            continue
        out[str(shard)] = {
            " ".join(str(part) for part in command)
            for command in entries
            if isinstance(command, list) and command
        }
    return out


def needs(job: dict[str, Any]) -> set[str]:
    value = job.get("needs", [])
    if isinstance(value, list):
        return {str(item) for item in value}
    return {str(value)} if value else set()


def workflow_semantic_errors(
    root: Path = ROOT,
    workflows: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    errors: list[str] = []
    workflows = load_workflows(root) if workflows is None else workflows
    names: list[str] = []

    for filename, expected in EXPECTED_NAMES.items():
        actual = str(workflows.get(filename, {}).get("name", ""))
        names.append(actual)
        if actual != expected:
            errors.append(f"{filename}: workflow name must be exactly {expected!r}, found {actual!r}")
    for name in sorted({name for name in names if name and names.count(name) > 1}):
        errors.append(f"workflow names must be unique; duplicate {name!r}")

    setup_count = 0
    for filename, workflow in workflows.items():
        for job_id, job in workflow.get("jobs", {}).items():
            reusable = str(job.get("uses", ""))
            if reusable:
                if not (
                    LOCAL_REUSABLE_WORKFLOW.fullmatch(reusable)
                    or PINNED_REUSABLE_WORKFLOW.fullmatch(reusable)
                ):
                    errors.append(
                        f"{filename}:{job_id}: reusable workflow must be same-repository local or use a full commit SHA"
                    )
                continue
            if str(job.get("runs-on", "")) != "ubuntu-24.04":
                errors.append(f"{filename}:{job_id}: runs-on must be pinned to ubuntu-24.04")
            for step in job.get("steps", []):
                if str(step.get("uses", "")).startswith("actions/setup-python@"):
                    setup_count += 1
                    if str(step.get("with", {}).get("python-version", "")) != PYTHON_MINOR_LINE:
                        errors.append(
                            f"{filename}:{job_id}: setup-python must use governed minor line {PYTHON_MINOR_LINE!r}"
                        )
        for line in command_lines(all_runs(workflow)):
            if "pip install" in line and "--requirement" not in line:
                errors.append(f"{filename}: ad hoc or unpinned pip install is forbidden: {line}")

    if not setup_count:
        errors.append("governed workflows must contain at least one setup-python step")
    if requirement_lines(root, "requirements/policy.txt") != POLICY_REQUIREMENTS:
        errors.append("requirements/policy.txt must contain the exact governed policy pins")
    if requirement_lines(root, "requirements/docs.txt") != DOCS_REQUIREMENTS:
        errors.append("requirements/docs.txt must contain the exact governed documentation pins")

    policy = workflows.get("ci.yml", {})
    triggers = policy.get("on", {})
    schedules = str(triggers.get("schedule", "")) if isinstance(triggers, dict) else ""
    for cron in ("17 */6 * * *", "43 8 * * *"):
        if cron not in schedules:
            errors.append(f"ci.yml: missing protected policy sentinel cron {cron}")

    impact = policy.get("jobs", {}).get("impact", {})
    if not marker(job_runs(policy, "impact"), "ci/policy_impact.py classify"):
        errors.append("ci.yml:impact must execute the fail-closed policy impact classifier")
    impact_checkouts = steps_using(impact, "actions/checkout@")
    if len(impact_checkouts) != 1 or str(impact_checkouts[0].get("with", {}).get("fetch-depth", "")) != "0":
        errors.append("ci.yml:impact must use one full-history checkout for exact transition diffing")

    shard_job = policy.get("jobs", {}).get("policy-shard", {})
    matrix = shard_job.get("strategy", {}).get("matrix", {}).get("shard", [])
    if tuple(str(item) for item in matrix) != SHARDS:
        errors.append("ci.yml:policy-shard matrix must enumerate every governed shard exactly once")
    shard_runs = job_runs(policy, "policy-shard")
    if not contains_command(shard_runs, POLICY_INSTALL):
        errors.append("ci.yml:policy-shard is missing governed policy dependency command")
    if not contains_command(shard_runs, DOCS_INSTALL):
        errors.append("ci.yml:policy-shard is missing governed docs dependency command")
    if not marker(shard_runs, "ci/run_policy_shard.py --shard"):
        errors.append("ci.yml:policy-shard must execute the governed shard registry runner")
    if not marker(shard_runs, "VERIFIED_POLICY_SHARD_NO_OP"):
        errors.append("ci.yml:policy-shard must make irrelevant shard no-op explicit")

    routed = registry_shards(root)
    if tuple(routed) != SHARDS:
        errors.append("governed shard registry must enumerate the exact nine policy shards in governed order")
    if REPOSITORY_REGRESSION_COMMAND not in routed.get("repository-regression", set()):
        errors.append(
            "governed repository-regression shard is missing executable coverage command "
            + REPOSITORY_REGRESSION_COMMAND
        )
    for owner, commands in routed.items():
        if owner != "repository-regression" and REPOSITORY_REGRESSION_COMMAND in commands:
            errors.append(
                "full repository regression command must be owned only by repository-regression; "
                f"found in {owner}"
            )
    all_registry_commands = set().union(*routed.values()) if routed else set()
    for command in (
        "python3 ci/validate_policy_reachability.py",
        "python3 ci/test_policy_reachability.py",
        "python3 ci/validate_repository_execution.py",
        "python3 ci/test_repository_execution.py",
        "python3 ci/validate_workflow_semantics.py",
        "python3 ci/test_workflow_semantics.py",
        "mkdocs build --strict",
    ):
        if command not in all_registry_commands:
            errors.append(f"governed shard registry is missing executable coverage command {command}")

    aggregate = policy.get("jobs", {}).get("validate-json", {})
    if not {"impact", "policy-shard"}.issubset(needs(aggregate)):
        errors.append("ci.yml:validate-json must aggregate impact and policy-shard")
    if "always()" not in str(aggregate.get("if", "")):
        errors.append("ci.yml:validate-json must run under always() to fail closed on upstream results")
    aggregate_runs = job_runs(policy, "validate-json")
    for result_marker in ("needs.impact.result", "needs.policy-shard.result"):
        if not marker(aggregate_runs, result_marker):
            errors.append(f"ci.yml:validate-json aggregator is missing result gate {result_marker}")

    uploads = [
        step
        for job in policy.get("jobs", {}).values()
        for step in steps_using(job, "actions/upload-artifact@")
    ]
    site_uploads = [step for step in uploads if step.get("with", {}).get("name") == "validated-site"]
    if len(site_uploads) != 1:
        errors.append("ci.yml must upload exactly one validated-site artifact")
    else:
        upload = site_uploads[0]
        condition = str(upload.get("if", ""))
        for required in (
            "matrix.shard == 'docs'",
            "github.event_name == 'push'",
            "github.ref == 'refs/heads/main'",
        ):
            if required not in condition:
                errors.append(f"ci.yml: validated-site upload condition is missing {required}")
        if str(upload.get("with", {}).get("retention-days", "")) != "1":
            errors.append("ci.yml: validated-site artifact retention must be exactly one day")

    for job_id, lane in {
        "log-gcd-lean": "log-gcd",
        "pc-wp04-lean": "pc-wp04",
        "union-closed-mathcert": "union-closed-mathcert",
    }.items():
        job = policy.get("jobs", {}).get(job_id, {})
        runs = job_runs(policy, job_id)
        if "impact" not in needs(job):
            errors.append(f"ci.yml:{job_id} must depend on impact classification")
        for required in (
            f"formal_replay_attestation.py digest --lane {lane}",
            f"formal_replay_gate.py decide --lane {lane}",
            '--mode "${MODE}"',
        ):
            if not marker(runs, required):
                errors.append(f"ci.yml:{job_id} missing formal replay impact-gate marker {required}")
        if not marker(runs, "formal_replay_gate.py emit-receipt"):
            errors.append(f"ci.yml:{job_id} must emit protected replay receipts through the schedule-aware gate")

    if not contains_command(job_runs(policy, "pc-wp04-lean"), POLICY_INSTALL):
        errors.append("ci.yml:pc-wp04-lean must install requirements/policy.txt")
    if not contains_command(job_runs(policy, "union-closed-mathcert"), EXTERNAL_POLICY_INSTALL):
        errors.append("ci.yml:union-closed-mathcert must install the root policy requirements by absolute workspace path")
    for job_id in ("log-gcd-lean", "pc-wp04-lean"):
        if not marker(job_runs(policy, job_id), "lake build"):
            errors.append(f"ci.yml:{job_id} must retain full Lean replay path")
    if not marker(job_runs(policy, "union-closed-mathcert"), "bash ci/check_lean.sh"):
        errors.append("ci.yml:union-closed-mathcert must retain pinned external replay path")

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
    checkouts = steps_using(build, "actions/checkout@")
    if len(checkouts) != 1:
        errors.append("pages.yml: build must contain exactly one checkout step")
    elif checkouts[0].get("with", {}).get("ref") != "${{ github.event.workflow_run.head_sha }}":
        errors.append("pages.yml: checkout must use the validated workflow_run.head_sha")
    build_runs = job_runs(pages, "build")
    if contains_command(build_runs, DOCS_INSTALL) or contains_command(build_runs, "mkdocs build --strict"):
        errors.append("pages.yml: Pages must deploy the policy artifact without resolving dependencies or rebuilding MkDocs")
    deploy = pages.get("jobs", {}).get("deploy", {})
    environment = deploy.get("environment", {})
    if str(environment.get("url", "")) != "${{ steps.deployment.outputs.page_url }}":
        errors.append("pages.yml: deploy environment must expose the deploy-pages page_url output")
    deployment_steps = steps_using(deploy, "actions/deploy-pages@")
    if len(deployment_steps) != 1 or deployment_steps[0].get("id") != "deployment":
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
        "workflow names, nine-shard impact routing, formal replay gates, runners, dependencies, "
        "repository-regression ownership, and publication freshness are valid"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
