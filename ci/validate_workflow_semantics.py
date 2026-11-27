#!/usr/bin/env python3
"""Validate semantic workflow, routing, runner, and publication contracts."""
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
    "formal-validation.yml": "formal-validation",
    "pages.yml": "Deploy documentation site",
    "pc-wp04.yml": "PC-WP04 promotion replay",
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
DYNAMIC_SHARD_MATRIX = "${{ fromJSON(needs.impact.outputs.policy_shards) }}"
DYNAMIC_FORMAL_MATRIX = "${{ fromJSON(needs.impact.outputs.formal_matrix) }}"
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


def trigger(workflow: dict[str, Any]) -> dict[str, Any]:
    value = workflow.get("on", {})
    return value if isinstance(value, dict) else {}


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
        if isinstance(job, dict)
        for step in job.get("steps", [])
        if isinstance(step, dict) and step.get("run")
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
    return [
        step
        for step in job.get("steps", [])
        if isinstance(step, dict) and str(step.get("uses", "")).startswith(prefix)
    ]


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
    path = root / "governance/policy_shard_registry.json"
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

    for filename, expected in EXPECTED_NAMES.items():
        actual = str(workflows.get(filename, {}).get("name", ""))
        if actual != expected:
            errors.append(f"{filename}: workflow name must be exactly {expected!r}, found {actual!r}")

    setup_count = 0
    for filename, workflow in workflows.items():
        for job_id, job in workflow.get("jobs", {}).items():
            if not isinstance(job, dict):
                errors.append(f"{filename}:{job_id}: workflow job must be a mapping")
                continue
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
                if not isinstance(step, dict):
                    continue
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
    policy_trigger = trigger(policy)
    schedules = [
        str(item.get("cron"))
        for item in policy_trigger.get("schedule", [])
        if isinstance(item, dict)
    ]
    if schedules != ["43 8 * * *"]:
        errors.append("ci.yml: policy workflow must own only the 43 8 * * * policy sentinel")

    impact = policy.get("jobs", {}).get("impact", {})
    if not marker(job_runs(policy, "impact"), "ci/policy_impact.py classify"):
        errors.append("ci.yml:impact must execute the fail-closed policy impact classifier")
    checkouts = steps_using(impact, "actions/checkout@")
    if len(checkouts) != 1 or str(checkouts[0].get("with", {}).get("fetch-depth", "")) != "0":
        errors.append("ci.yml:impact must use one full-history checkout for exact transition diffing")

    shard_job = policy.get("jobs", {}).get("policy-shard", {})
    matrix = shard_job.get("strategy", {}).get("matrix", {}).get("shard", "")
    if str(matrix) != DYNAMIC_SHARD_MATRIX:
        errors.append("ci.yml:policy-shard must use the classifier-produced dynamic shard matrix")
    shard_runs = job_runs(policy, "policy-shard")
    if not contains_command(shard_runs, POLICY_INSTALL):
        errors.append("ci.yml:policy-shard is missing governed policy dependency command")
    if not marker(shard_runs, "ci/run_policy_shard.py --shard"):
        errors.append("ci.yml:policy-shard must execute the governed shard registry runner")

    # Guard the dedicated queue test ownership and both conditional routes.
    # The required aggregate must distinguish a proven no-op from missing,
    # failed or cancelled affected work.
    queue = policy.get("jobs", {}).get("queue-cutover-contract", {})
    queue_flags = ("queue_pickup", "queue_erdos")
    for flag in queue_flags:
        if impact.get("outputs", {}).get(flag) != "${{ steps.classify.outputs." + flag + " }}":
            errors.append(f"ci.yml:impact missing queue contract route output {flag}")
    queue_if = "needs.impact.result == 'success' && (needs.impact.outputs.queue_pickup == 'true' || needs.impact.outputs.queue_erdos == 'true')"
    if set(needs(queue)) != {"impact"} or queue.get("if") != queue_if:
        errors.append("ci.yml:queue-contract job must use the classifier-produced impact route")
    expected_queue_runs = {
        "python3 ci/test_gcl_queue_class_cutover.py": "queue_pickup",
        "python3 ci/test_erdos_compendium_publication_gate.py": "queue_erdos",
        "python3 ci/test_erdos_compendium_direct_return_projector.py": "queue_erdos",
        "python3 ci/test_erdos_compendium_direct_return_permissions.py": "queue_erdos",
        "python3 ci/test_erdos_compendium_editorial_activate.py": "queue_erdos",
        "PYTHONPATH=. python3 tests/test_erdos_catalogue_queue_projection.py": "queue_erdos",
        "python3 governance/source_erdos_critical_005/validate.py": "queue_erdos",
        "python3 ci/test_erdos_compendium_editorial_replay.py": "queue_erdos",
    }
    queue_steps = [step for step in queue.get("steps", []) if step.get("run")]
    if (len(queue_steps) != len(expected_queue_runs)
            or {str(step["run"]) for step in queue_steps} != set(expected_queue_runs)
            or any(step.get("if") != "needs.impact.outputs." + expected_queue_runs.get(str(step["run"]), "") + " == 'true'"
                   for step in queue_steps)):
        errors.append("ci.yml:queue-contract test ownership or conditional step routing drift")
    aggregate = policy.get("jobs", {}).get("validate-json", {})
    if not {"impact", "policy-shard"}.issubset(needs(aggregate)):
        errors.append("ci.yml:validate-json must aggregate impact and policy-shard")
    if "always()" not in str(aggregate.get("if", "")):
        errors.append("ci.yml:validate-json must run under always()")
    for result_marker in ("needs.impact.result", "needs.policy-shard.result"):
        if not marker(job_runs(policy, "validate-json"), result_marker):
            errors.append(f"ci.yml:validate-json missing result gate {result_marker}")
    if "queue-cutover-contract" not in needs(aggregate):
        errors.append("ci.yml:validate-json must aggregate routed queue-contract")
    queue_gate = """case "${{ needs.impact.outputs.queue_pickup }}:${{ needs.impact.outputs.queue_erdos }}" in
  false:false)
    test "${{ needs.queue-cutover-contract.result }}" = "skipped"
    echo "QUEUE_CONTRACT_UNCHANGED_ATTESTATION_REUSED"
    ;;
  true:true|true:false|false:true)
    test "${{ needs.queue-cutover-contract.result }}" = "success"
    ;;
  *) echo "QUEUE_CONTRACT_ROUTE_INVALID"; exit 1 ;;
esac"""
    def normalized_lines(value: str) -> tuple[str, ...]:
        return tuple(line.strip() for line in value.splitlines() if line.strip())
    gate = normalized_lines(queue_gate)
    runs = [normalized_lines(run) for run in job_runs(policy, "validate-json")]
    if not any(any(lines[i:i+len(gate)] == gate for i in range(len(lines))) for lines in runs):
        errors.append("ci.yml:validate-json missing fail-closed conditional queue-contract result gate")
    for retired in ("log-gcd-lean", "pc-wp04-lean", "union-closed-mathcert"):
        if retired in policy.get("jobs", {}):
            errors.append(f"ci.yml: retired campaign-specific formal job remains instantiated: {retired}")

    routed = registry_shards(root)
    if tuple(routed) != SHARDS:
        errors.append("governed shard registry must enumerate the exact nine policy shards in governed order")
    if REPOSITORY_REGRESSION_COMMAND not in routed.get("repository-regression", set()):
        errors.append("governed repository-regression shard is missing executable coverage command")
    for owner, commands in routed.items():
        if owner != "repository-regression" and REPOSITORY_REGRESSION_COMMAND in commands:
            errors.append(f"full repository regression command must be owned only by repository-regression; found in {owner}")
    all_registry_commands = set().union(*routed.values()) if routed else set()
    for command in (
        "python3 ci/policy_impact.py validate",
        "python3 ci/test_policy_impact.py",
        "python3 ci/formal_validation.py validate",
        "python3 ci/test_formal_validation.py",
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

    uploads = [
        step
        for job in policy.get("jobs", {}).values()
        if isinstance(job, dict)
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

    formal_workflow = workflows.get("formal-validation.yml", {})
    formal_trigger = trigger(formal_workflow)
    if not {"pull_request", "merge_group", "schedule", "workflow_dispatch"}.issubset(formal_trigger):
        errors.append("formal-validation.yml: trigger set is incomplete")
    formal_schedules = [
        str(item.get("cron"))
        for item in formal_trigger.get("schedule", [])
        if isinstance(item, dict)
    ]
    if formal_schedules != ["17 */6 * * *"]:
        errors.append("formal-validation.yml: formal sentinel cron drift")
    if "push" in formal_trigger:
        errors.append("formal-validation.yml: direct protected-main push trigger is forbidden")

    formal_impact = formal_workflow.get("jobs", {}).get("impact", {})
    formal_checkouts = steps_using(formal_impact, "actions/checkout@")
    if len(formal_checkouts) != 1 or str(formal_checkouts[0].get("with", {}).get("fetch-depth", "")) != "0":
        errors.append("formal-validation.yml:impact must use full-history checkout")
    if not marker(job_runs(formal_workflow, "impact"), "ci/formal_validation.py classify"):
        errors.append("formal-validation.yml:impact must execute material formal classifier")

    lane_job = formal_workflow.get("jobs", {}).get("formal-lane", {})
    formal_matrix = lane_job.get("strategy", {}).get("matrix", "")
    if str(formal_matrix) != DYNAMIC_FORMAL_MATRIX:
        errors.append("formal-validation.yml:formal-lane must use classifier-produced dynamic matrix")
    if not marker(job_runs(formal_workflow, "formal-lane"), "ci/formal_validation.py run"):
        errors.append("formal-validation.yml:formal-lane must execute generic lane runner")
    if not steps_using(lane_job, "grandchallenge/lean-action@37f8471aecd2efbeab3b1e1a75ad18fb8f5c1b01"):
        errors.append("formal-validation.yml: formal lanes must use the exact governed Lean action")

    formal_aggregate = formal_workflow.get("jobs", {}).get("formal-validation", {})
    if not {"impact", "formal-lane"}.issubset(needs(formal_aggregate)):
        errors.append("formal-validation.yml: aggregate must depend on impact and formal-lane")
    if "always()" not in str(formal_aggregate.get("if", "")):
        errors.append("formal-validation.yml: aggregate must run under always()")
    if str(formal_aggregate.get("name", "")) != "formal-validation":
        errors.append("formal-validation.yml: required aggregate job name drift")

    retired_aliases = {
        "legacy-log-gcd-context",
        "legacy-pc-wp04-context",
        "legacy-union-closed-context",
    }
    for job_id in retired_aliases:
        if job_id in formal_workflow.get("jobs", {}):
            errors.append(
                f"formal-validation.yml:{job_id}: retired compatibility alias must remain absent"
            )

    pc = workflows.get("pc-wp04.yml", {})
    if set(trigger(pc)) != {"workflow_call", "workflow_dispatch"}:
        errors.append("pc-wp04.yml: promotion replay triggers must be workflow_call plus workflow_dispatch only")
    if not marker(all_runs(pc), "ci/formal_validation.py run --lane pc-wp04 --mode promotion"):
        errors.append("pc-wp04.yml: promotion replay must delegate to generic lane runner")

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
    deploy = pages.get("jobs", {}).get("deploy", {})
    if "needs.build.outputs.publish" not in str(deploy.get("if", "")):
        errors.append("pages.yml: deployment must depend on source-change eligibility output")
    publication = [s for s in build.get("steps", []) if s.get("id") == "publication"]
    if len(publication) != 1 or "ci/pages_publish_gate.py" not in str(publication[0].get("run", "")):
        errors.append("pages.yml: missing bounded site-source publication gate")
    for name in ("Set up Python", "Download and verify policy-validated site",
                 "Configure Pages", "Upload artifact"):
        matches = [s for s in build.get("steps", []) if s.get("name") == name]
        if len(matches) != 1 or "steps.publication.outputs.publish" not in str(matches[0].get("if", "")):
            errors.append("pages.yml: site activity must be skipped when no site inputs changed: " + name)
    page_checkouts = steps_using(build, "actions/checkout@")
    if len(page_checkouts) != 1 or page_checkouts[0].get("with", {}).get("ref") != "refs/heads/main":
        errors.append("pages.yml: privileged checkout must use trusted protected main")
    validation_steps = [s for s in build.get("steps", []) if s.get("name") == "Require validated commit to remain current main"]
    if (len(validation_steps) != 1
            or validation_steps[0].get("id") != "freshness"
            or validation_steps[0].get("env", {}).get("VALIDATED_EVENT_SHA") != "${{ github.event.workflow_run.head_sha }}"
            or "${VALIDATED_EVENT_SHA}" not in str(validation_steps[0].get("run", ""))
            or '"${validated_sha}" != "${current_main_sha}"' not in str(validation_steps[0].get("run", ""))
            or '"${VALIDATED_EVENT_SHA}" != "${current_main_sha}"' not in str(validation_steps[0].get("run", ""))
            or 'current=false' not in str(validation_steps[0].get("run", ""))
            or 'current=true' not in str(validation_steps[0].get("run", ""))
            or len(publication) != 1
            or publication[0].get("if") != "steps.freshness.outputs.current == 'true'"):
        errors.append("pages.yml: trusted main must be checked and stale validated runs must suppress publication")
    page_runs = job_runs(pages, "build")
    if contains_command(page_runs, DOCS_INSTALL) or contains_command(page_runs, "mkdocs build --strict"):
        errors.append("pages.yml: Pages must deploy the policy artifact without rebuilding documentation")
    deploy = pages.get("jobs", {}).get("deploy", {})
    deployment_steps = steps_using(deploy, "actions/deploy-pages@")
    if len(deployment_steps) != 1 or deployment_steps[0].get("id") != "deployment":
        errors.append("pages.yml: deploy must use exactly one deployment step with id=deployment")

    return errors


def main() -> int:
    errors = workflow_semantic_errors()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        print(f"workflow semantic validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1
    print("workflow semantic validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
