#!/usr/bin/env python3
from __future__ import annotations

import json
from typing import Any

import validate_workflow_coverage_v3 as v3

RECOVERY_FAILOVER_WORKFLOW = "administrative-maintenance-0813-recovery-failover.yml"
QUALIFICATION_ONLY_WORKFLOW = "administrative-protected-receipt-live-qualification.yml"
CONSTRUCTION_GATE_WORKFLOW = "construction-gate-runtime.yml"
ROLLING_REVIEW_DIRECT_WORKFLOW = "erdos-rolling-review-completion.yml"
THREE_SOURCE_COUNCIL_WORKFLOW = "erdos-three-source-resolution.yml"

v3.legacy.EXPECTED_WORKFLOWS = set(v3.legacy.EXPECTED_WORKFLOWS) | {
    "aether-controls-admin.yml",
    "cmdg-nat-concordance.yml",
    "cmdg-euclid-bridge.yml",
    "cmdg-vertical-spine-v0.yml",
    "cmdg-condensed-cm1.yml",
    "cmdg-condensed-cm2.yml",
    "cmdg-condensed-cm3.yml",
    "cmdg-solid-c05.yml",
    "cmdg-condensed-cm4.yml",
    "cmdg-condensed-cm4-p2.yml",
    "cmdg-condensed-cm4-p2-d.yml",
    "cmdg-condensed-cm4-p2-e.yml",
    "cmdg-condensed-cm4-p3.yml",
    "cmdg-postmerge.yml",
    "visual-pedagogy-representation-repair.yml",
    "pr-visual-status-advisory.yml",
    RECOVERY_FAILOVER_WORKFLOW,
    QUALIFICATION_ONLY_WORKFLOW,
    CONSTRUCTION_GATE_WORKFLOW,
    ROLLING_REVIEW_DIRECT_WORKFLOW,
    THREE_SOURCE_COUNCIL_WORKFLOW,
    "ghos-routing-enforcement.yml",
}

ROOT = v3.ROOT
POLICY_SHARD_REGISTRY = "governance/policy_shard_registry.json"
ROUTED_MARKER_SUCCESSORS = {
    "python3 ci/validate_workflow_coverage.py": "python3 ci/validate_workflow_coverage_v2.py",
    "python3 ci/test_workflow_coverage.py": "python3 ci/test_workflow_coverage_v2.py",
    "python -m unittest discover -s tests -p 'test_*.py'": (
        "python3 ci/run_unittest_modules.py --discover-root tests --pattern test_*.py "
        "--report-json repository-regression-timing.json"
    ),
}


def _normalize_command(command: str) -> str:
    return (
        command.strip()
        .replace("'test_*.py'", "test_*.py")
        .replace('"test_*.py"', "test_*.py")
    )


def _registry_commands(root=ROOT, registry=None) -> set[str]:
    if registry is None:
        path = root / POLICY_SHARD_REGISTRY
        if not path.is_file():
            return set()
        try:
            registry = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return set()
    if not isinstance(registry, dict):
        return set()
    commands: set[str] = set()
    shards = registry.get("shards", {})
    if not isinstance(shards, dict):
        return commands
    for entries in shards.values():
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if isinstance(entry, list) and entry and all(isinstance(part, str) for part in entry):
                commands.add(_normalize_command(" ".join(entry)))
    return commands


def _trigger(workflow: dict[str, Any]) -> dict[str, Any]:
    value = workflow.get("on", {})
    return value if isinstance(value, dict) else {}


def _job(workflow: dict[str, Any], name: str) -> dict[str, Any]:
    jobs = workflow.get("jobs", {})
    if not isinstance(jobs, dict):
        return {}
    value = jobs.get(name, {})
    return value if isinstance(value, dict) else {}


def recovery_failover_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    text = texts.get(RECOVERY_FAILOVER_WORKFLOW)
    if text is None:
        return errors
    workflow = v3.legacy.load_yaml_text(text)
    trigger = _trigger(workflow)
    if set(trigger) != {"pull_request"}:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: trigger must be exactly pull_request")
    pull_request = trigger.get("pull_request", {})
    types = pull_request.get("types", []) if isinstance(pull_request, dict) else []
    if types != ["closed"]:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: pull_request trigger must be closed only")

    job = _job(workflow, "recover")
    if job.get("environment") != v3.PROTECTED_ENVIRONMENT:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: recover job must bind protected environment release-trust")
    expected_permissions = {
        "actions": "read",
        "checks": "read",
        "contents": "read",
        "issues": "write",
        "pull-requests": "write",
    }
    if job.get("permissions") != expected_permissions:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: delegated Referee permissions drift")

    required_markers = (
        "github.event.pull_request.merged == true",
        "startsWith(github.event.pull_request.head.ref, 'control/mp-admin-0813-')",
        v3.APP_ACTION,
        v3.APP_ID,
        v3.APP_KEY,
        "id: write-token",
        "repositories: MATH-PROGRAMME",
        "permission-contents: write",
        "permission-issues: write",
        "permission-pull-requests: write",
        "id: evidence-token",
        "MATHFORGE\n            MATHSOLVE\n            MATHCERT\n            INTELLECT",
        "permission-actions: read",
        "permission-contents: read",
        "permission-issues: read",
        "permission-pull-requests: read",
        "id: admin-token",
        "permission-administration: write",
        "ref: refs/heads/main",
        "persist-credentials: false",
        "CANDIDATE_TOKEN: ${{ steps.write-token.outputs.token }}",
        "EVIDENCE_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "OBSERVABILITY_TOKEN: ${{ steps.evidence-token.outputs.token }}",
        "REFEREE_TOKEN: ${{ github.token }}",
        "ADMIN_TOKEN: ${{ steps.admin-token.outputs.token }}",
        "CANDIDATE_LOGIN: ${{ format('{0}[bot]', steps.write-token.outputs.app-slug) }}",
        "REFEREE_LOGIN: 'github-actions[bot]'",
        "CANDIDATE_APP_ID: ${{ secrets.GCL_RELEASE_TRUST_APP_ID }}",
        "REFEREE_APP_ID: '15368'",
        "Restore exact PR-only Administration actor",
        "from autonomy_github import AutonomyError, Client, identity, install_bypass",
        "ruleset_id = 17137629",
        "administrator.app_id != 4423678",
        '"bypass_mode": "pull_request"',
        "administrative-autonomy-0813-ruleset-actor-restore.json",
        "python ci/administrative_autonomy_0813_closure_preflight.py",
        "--apply",
        "administrative-autonomy-0813-pr-close-recovery.json",
        "retention-days: 90",
    )
    for marker in required_markers:
        if marker not in text:
            errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: missing bounded recovery marker {marker}")

    restore_index = text.find("Restore exact PR-only Administration actor")
    preflight_index = text.find("python ci/administrative_autonomy_0813_closure_preflight.py")
    if restore_index < 0 or preflight_index < 0 or restore_index > preflight_index:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: exact Administration actor restoration must precede exact Aug13 preflight")

    if text.count(v3.APP_ACTION) != 3:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: exactly three separately scoped App tokens are required")
    if text.count("permission-administration: write") != 1:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: exactly one administration-write token is required")
    if text.count("permission-contents: write") != 1:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: exactly one contents-write token is required")
    if text.count("${{ github.token }}") != 1:
        errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: workflow token must be used only as the Referee token")

    for forbidden in (
        "workflow_dispatch:",
        "schedule:",
        "push:",
        "pull_request_target:",
        "administrative_autonomy_runtime.py execute",
        "administrative_maintenance_completion_state.json",
        "gh pr merge",
        "git push origin main",
        "/git/refs/heads/main",
        "permission-checks: write",
    ):
        if forbidden in text:
            errors.append(f"{RECOVERY_FAILOVER_WORKFLOW}: forbidden recovery capability {forbidden}")
    return errors


def remediation_envelope_errors(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    text = texts.get(QUALIFICATION_ONLY_WORKFLOW)
    if text is None:
        return errors
    workflow = v3.legacy.load_yaml_text(text)
    trigger = _trigger(workflow)
    if set(trigger) != {"workflow_dispatch", "issue_comment", "pull_request_target"}:
        errors.append(
            f"{QUALIFICATION_ONLY_WORKFLOW}: trigger must be workflow_dispatch plus issue_comment plus pull_request_target"
        )
    issue_comment = trigger.get("issue_comment", {})
    issue_types = issue_comment.get("types", []) if isinstance(issue_comment, dict) else []
    if issue_types != ["created"]:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: issue_comment trigger must be created only")
    pull_request_target = trigger.get("pull_request_target", {})
    types = pull_request_target.get("types", []) if isinstance(pull_request_target, dict) else []
    expected_types = ["closed", "opened", "reopened", "synchronize", "ready_for_review"]
    if types != expected_types:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: pull_request_target trigger set drift")

    admit = _job(workflow, "admit")
    qualify = _job(workflow, "qualify")
    expected_admit_permissions = {
        "checks": "read",
        "contents": "read",
        "issues": "write",
        "pull-requests": "write",
    }
    if admit.get("permissions") != expected_admit_permissions:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: delegated Referee admission permissions drift")
    if admit.get("environment") != v3.PROTECTED_ENVIRONMENT:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: admit job must bind protected environment release-trust")
    expected_qualify_permissions = {"contents": "read", "issues": "write"}
    if qualify.get("permissions") != expected_qualify_permissions:
        errors.append(
            f"{QUALIFICATION_ONLY_WORKFLOW}: qualification job permissions must be contents-read plus issue-status-write only"
        )
    if qualify.get("environment") != v3.PROTECTED_ENVIRONMENT:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: qualify job must bind protected environment release-trust")

    required_markers = (
        "github.event_name == 'pull_request_target'",
        "github.event.action != 'closed'",
        "github.event.pull_request.draft == false",
        "startsWith(github.event.pull_request.head.ref, 'remediation/mp-admin-')",
        "github.event_name == 'issue_comment'",
        "github.event.issue.pull_request != null",
        "contains(fromJSON('[\"OWNER\",\"MEMBER\",\"COLLABORATOR\"]'), github.event.comment.author_association)",
        "startsWith(github.event.comment.body, 'DELEGATED_REMEDIATION_ADMIT ')",
        "DELEGATED_REMEDIATION_ADMIT ([0-9a-f]{40})",
        "Resolve exact admission target",
        "Mint bounded Candidate merge-executor token",
        "id: candidate-merge-token",
        "permission-contents: write",
        "permission-pull-requests: write",
        "permission-administration: read",
        "Check out trusted protected implementation",
        "ref: refs/heads/main",
        "REFEREE_TOKEN: ${{ github.token }}",
        "ADMIN_READ_TOKEN: ${{ steps.admin-read-token.outputs.token }}",
        "CANDIDATE_MERGE_TOKEN: ${{ steps.candidate-merge-token.outputs.token }}",
        "CANDIDATE_LOGIN: ${{ format('{0}[bot]', steps.candidate-merge-token.outputs.app-slug) }}",
        "administrative_remediation_envelope.py admit-pull-request",
        '--pr "${{ steps.target.outputs.pr_number }}"',
        '--head "${{ steps.target.outputs.expected_head }}"',
        "Publish durable admission result",
        "DELEGATED REMEDIATION ADMISSION RESULT — MP-ADMIN-REMEDIATION-ENVELOPE-001",
        "administrative-remediation-admission.json",
        "permission-contents: read",
        "permission-pull-requests: read",
        "permission-issues: read",
        "permission-administration: write",
        "administrative_remediation_envelope.py reconcile-actor",
        "administrative_protected_receipt_live.py qualify",
        "GCL_PROTECTED_RECEIPT_CONFIG_EVIDENCE: administrative-remediation-ruleset-reconciliation.json",
        "--control-id MP-ADMIN-REMEDIATION-ENVELOPE-001",
        "--control-issue 615",
        "--authorization-comment-id 5349149366",
        "--receipt-pr 596",
        "--integration-merge 8ff752b4f2ac28d87575d4f4ef48f564fb18837b",
        "Publish durable remediation result",
        "STATUS_TOKEN: ${{ github.token }}",
        "https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/issues/615/comments",
        "DELEGATED REMEDIATION RUN RESULT — MP-ADMIN-REMEDIATION-ENVELOPE-001",
        "Safety readback: no #596 mutation",
        "retention-days: 90",
    )
    for marker in required_markers:
        if marker not in text:
            errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: missing remediation envelope marker {marker}")

    if text.count(v3.APP_ACTION) != 6:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly six separately scoped App tokens are required")
    if text.count("${{ github.token }}") != 3:
        errors.append(
            f"{QUALIFICATION_ONLY_WORKFLOW}: workflow token must be used exactly for Referee admission, admission-status publication, and qualification-status publication"
        )
    if text.count("permission-administration: write") != 1:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly one actor-reconciliation administration-write token is required")
    if text.count("permission-administration: read") != 2:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly two separately minted administration-read observation tokens are required")
    if text.count("permission-contents: write") != 1:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly one Candidate contents-write merge token is required")
    if text.count("permission-pull-requests: write") != 1:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: exactly one Candidate pull-request-write merge token is required")
    if "permission-issues: write" in text:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: App tokens may not receive issues-write")

    target_index = text.find("Resolve exact admission target")
    admission_index = text.find("administrative_remediation_envelope.py admit-pull-request")
    admission_status_index = text.find("Publish durable admission result")
    reconciliation_index = text.find("administrative_remediation_envelope.py reconcile-actor")
    qualification_index = text.find("administrative_protected_receipt_live.py qualify")
    status_index = text.find("Publish durable remediation result")
    evidence_index = text.find("Preserve remediation and qualification evidence")
    if min(
        target_index,
        admission_index,
        admission_status_index,
        reconciliation_index,
        qualification_index,
        status_index,
        evidence_index,
    ) < 0:
        errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: remediation sequence is incomplete")
    elif not target_index < admission_index < admission_status_index < reconciliation_index < qualification_index < status_index < evidence_index:
        errors.append(
            f"{QUALIFICATION_ONLY_WORKFLOW}: exact target resolution and Referee admission must precede admission audit, actor reconciliation, qualification, durable status, and retained evidence"
        )

    for forbidden in (
        "schedule:",
        "push:",
        "workflow_run:",
        "repository_dispatch:",
        "pull_request:\n",
        "permission-checks: write",
        "administrative_autonomy_runtime.py execute",
        "administrative_autonomy_0813_closure_preflight.py",
        "administrative_maintenance_completion_state.json",
        "gh pr merge",
        "git push origin main",
        "/git/refs/heads/main",
    ):
        if forbidden in text:
            errors.append(f"{QUALIFICATION_ONLY_WORKFLOW}: forbidden remediation capability {forbidden}")
    return errors

def erdos_forge_copilot_pilot_errors(texts: dict[str, str]) -> list[str]:
    """Explicit, claim-free, cost-bounded exception to generic read-only workflow rule.

    This does NOT grant certification, source acceptance, or a Solve lease.
    Only the named jobs in the existing registered persistent controller qualify.
    """
    key = "erdos-catalogue-queue-projection.yml"
    source = texts.get(key)
    if source is None:
        return []
    wf = v3.legacy.load_yaml_text(source)
    jobs = wf.get("jobs", {})
    expected = {"reconcile", "ledger", "canary",
                "forge-pilot-review", "forge-pilot-evidence"}
    if set(jobs) != expected:
        return [f"{key}: Forge pilot requires exact five-job topology"]
    agent = _job(wf, "forge-pilot-review")
    publisher = _job(wf, "forge-pilot-evidence")
    errors: list[str] = []
    if agent.get("permissions") != {
        "contents": "read", "issues": "read", "copilot-requests": "write"
    }:
        errors.append(f"{key}: AI model job must be repository-read and copilot-only")
    if publisher.get("permissions") != {
        "contents": "read", "issues": "write", "actions": "read"
    }:
        errors.append(f"{key}: trusted publisher must lack copilot-requests permission")
    for name, job in (("forge-pilot-review", agent), ("forge-pilot-evidence", publisher)):
        raw_timeout = str(job.get("timeout-minutes", ""))
        bound = 12 if name == "forge-pilot-review" else 5
        if not raw_timeout.isdecimal() or not (1 <= int(raw_timeout) <= bound):
            errors.append(f"{key}: {name} exceeds bounded timeout")
        condition = str(job.get("if", ""))
        if "github.event_name == 'push'" not in condition:
            errors.append(f"{key}: {name} cannot incur scheduled/repeated AI action")
        if job.get("runs-on") != "ubuntu-24.04":
            errors.append(f"{key}: {name} needs bounded approved runner")
        steps = job.get("steps", [])
        main_checkout = [z for z in steps if
                         str(z.get("uses", "")).startswith("actions/checkout@") and
                         z.get("with", {}).get("ref") == "main" and
                         str(z.get("with", {}).get("persist-credentials", "")).lower() == "false"]
        if len(main_checkout) != 1:
            errors.append(f"{key}: {name} must checkout protected main without retained credential")
    if agent.get("needs") != ["reconcile"]:
        errors.append(f"{key}: Forge pilot must follow queue reconciler")
    if publisher.get("needs") != ["forge-pilot-review"]:
        errors.append(f"{key}: evidence publication must follow independent model run")
    agent_text = str(agent)
    publisher_text = str(publisher)
    for required in (
        "ci/erdos_forge_copilot_pilot.py prepare",
        "steps.prep.outputs.ready",
        "npm install -g @github/copilot@1.0.66",
        "--model=gpt-5.4 --max-ai-credits=30 --no-auto-update",
        "--available-tools=read",
        "--deny-tool=shell",
        "--deny-tool=write",
        "--deny-tool=url",
        "--disable-builtin-mcps",
        "--no-ask-user",
        "--no-auto-update",
        "timeout 420s",
        "copilot-requests",
        "GITHUB_TOKEN",
        "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
    ):
        if required not in agent_text:
            errors.append(f"{key}: missing protected read-only AI boundary {required}")
    for forbidden in ("gh pr merge", "git push", "--allow-all", "permission-contents: write"):
        if forbidden in agent_text or forbidden in publisher_text:
            errors.append(f"{key}: forbidden pilot capability {forbidden}")
    for required in (
        "ci/erdos_forge_copilot_pilot.py publish",
        "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
        "GH_TOKEN",
    ):
        if required not in publisher_text:
            errors.append(f"{key}: missing separately-scoped evidence publisher {required}")
    if "copilot" in str(publisher.get("permissions", {})) or "issues" not in str(publisher.get("permissions", {})):
        errors.append(f"{key}: agent credentials may not appear in evidence publisher")
    return errors


def rolling_review_direct_errors(texts: dict[str, str]) -> list[str]:
    """Fail closed on any widened, unaudited direct Council Clerk entry point."""
    key = ROLLING_REVIEW_DIRECT_WORKFLOW
    source = texts.get(key)
    if source is None:
        return []
    workflow = v3.legacy.load_yaml_text(source)
    errors: list[str] = []
    if _trigger(workflow) != {"workflow_dispatch": ""}:
        errors.append(f"{key}: only explicit workflow_dispatch from main is permitted")
    if workflow.get("permissions") != {"contents": "read"}:
        errors.append(f"{key}: top-level GitHub token must be contents read only")
    if set(workflow.get("jobs", {})) != {"council-clerk-complete-reviews"}:
        errors.append(f"{key}: unexpected job topology")
    job = _job(workflow, "council-clerk-complete-reviews")
    if (job.get("environment") != "release-trust"
            or job.get("permissions") != {"contents": "read"}
            or "refs/heads/main" not in str(job.get("if", ""))
            or "grandchallenge/MATH-PROGRAMME" not in str(job.get("if", ""))):
        errors.append(f"{key}: missing protected-source/release-trust job envelope")
    steps = job.get("steps") or []
    if len(steps) != 6 or not all(isinstance(x, dict) for x in steps):
        errors.append(f"{key}: expected exactly six protected transaction steps")
        return errors
    checkout, python, tests, credential, execute, receipt = steps
    if (checkout.get("uses") !=
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
            or checkout.get("with") != {"ref": "main", "persist-credentials": "false"}):
        errors.append(f"{key}: wrong immutable protected-main checkout")
    if (python.get("uses") !=
            "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97"
            or python.get("with") != {"python-version": "3.12"}):
        errors.append(f"{key}: unapproved Python bootstrap")
    if "tests/test_erdos_catalogue_queue_projection.py" not in str(tests.get("run", "")):
        errors.append(f"{key}: missing hostile exact-14 controller test")
    token = credential.get("with") or {}
    if (credential.get("uses") !=
            "actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1"
            or token.get("owner") != "grandchallenge"
            or token.get("repositories") != "MATH-PROGRAMME"
            or token.get("permission-issues") != "write"
            or token.get("permission-organization-projects") != "write"
            or set(token) != {"app-id", "private-key", "owner", "repositories",
                              "permission-issues", "permission-organization-projects"}
            or "GCL_COUNCIL_CLERK_APP_ID" not in str(token["app-id"])
            or "GCL_COUNCIL_CLERK_PRIVATE_KEY" not in str(token["private-key"])):
        errors.append(f"{key}: Council Clerk token permission or identity drift")
    run = str(execute.get("run", ""))
    env = execute.get("env") or {}
    if (env.get("GCL_CONTROLLER_ID") != "erdos-rolling-review-completion"
            or "steps.council.outputs.token" not in str(env.get("GH_TOKEN", ""))
            or "ci/erdos_catalogue_queue_projection.py" not in run
            or "--review-completion --apply" not in run
            or "--receipt rolling-critical-reviews/receipt.json" not in run
            or "test -n" not in run):
        errors.append(f"{key}: unrecognized exact-14 bounded controller invocation")
    if (receipt.get("uses") !=
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"
            or receipt.get("if") != "always()"
            or receipt.get("with", {}).get("path") !=
               "rolling-critical-reviews/receipt.json"):
        errors.append(f"{key}: controller completion/blocker receipt not retained")
    for forbidden in ("gh pr merge", "gh project item-edit", "gh api --method PUT",
                      "permission-administration", "secrets.GCL_RELEASE_TRUST"):
        if forbidden in source:
            errors.append(f"{key}: forbidden broad control-plane capability {forbidden}")
    return errors


def three_source_council_errors(texts: dict[str, str]) -> list[str]:
    """Protect source remediation from widened authorities or manual bypass."""
    key = THREE_SOURCE_COUNCIL_WORKFLOW
    source = texts.get(key)
    if source is None:
        return []
    workflow = v3.legacy.load_yaml_text(source)
    errors: list[str] = []
    if _trigger(workflow) != {'workflow_dispatch': ''}:
        errors.append(f'{key}: only on-demand protected-main execution allowed')
    if workflow.get('permissions') != {'contents': 'read'}:
        errors.append(f'{key}: unscoped GitHub Actions permissions')
    if set(workflow.get('jobs', {})) != {'council-clerk-source-remediation'}:
        errors.append(f'{key}: unexpected job topology')
    job = _job(workflow, 'council-clerk-source-remediation')
    if (job.get('environment') != 'release-trust'
            or job.get('permissions') != {'contents': 'read'}
            or 'refs/heads/main' not in str(job.get('if',''))
            or 'grandchallenge/MATH-PROGRAMME' not in str(job.get('if',''))):
        errors.append(f'{key}: lost protected Council environment')
    steps = job.get('steps') or []
    if len(steps) != 7 or not all(isinstance(x,dict) for x in steps):
        errors.append(f'{key}: expected exactly seven bounded steps')
        return errors
    checkout,python,tests,credential,preflight,apply,receipt=steps
    if (checkout.get('uses') != 'actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1'
            or checkout.get('with') != {'ref':'main','persist-credentials':'false'}):
        errors.append(f'{key}: checkout not protected and credential-free')
    if (python.get('uses') != 'actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97'
            or python.get('with') != {'python-version':'3.12'}):
        errors.append(f'{key}: unpinned runtime bootstrap')
    test=str(tests.get('run',''))
    if ('governance/source_erdos_critical_005/validate.py' not in test
            or 'tests/test_erdos_three_source_resolution.py' not in test):
        errors.append(f'{key}: hostile controls or source hash checks missing')
    token=credential.get('with') or {}
    if (credential.get('uses') != 'actions/create-github-app-token@bcd2ba49218906704ab6c1aa796996da409d3eb1'
            or token.get('owner')!='grandchallenge'
            or token.get('repositories')!='MATH-PROGRAMME'
            or token.get('permission-issues')!='write'
            or token.get('permission-organization-projects')!='read'
            or set(token)!={'app-id','private-key','owner','repositories','permission-issues','permission-organization-projects'}
            or 'GCL_COUNCIL_CLERK_APP_ID' not in str(token.get('app-id',''))
            or 'GCL_COUNCIL_CLERK_PRIVATE_KEY' not in str(token.get('private-key',''))):
        errors.append(f'{key}: Council Clerk role or least privileges changed')
    for step,needs_apply,path in ((preflight,False,'preflight.json'),(apply,True,'receipt.json')):
        env=step.get('env') or {}
        run=str(step.get('run',''))
        if (env.get('GCL_CONTROLLER_ID')!='erdos-three-source-resolution'
                or 'steps.council.outputs.token' not in str(env.get('GH_TOKEN',''))
                or 'ci/erdos_three_source_resolution.py' not in run
                or f'--receipt artifacts/erdos-three-source-resolution/{path}' not in run
                or ('--apply' in run)!=needs_apply):
            errors.append(f'{key}: missing exact bounded Council operation')
    if (receipt.get('uses')!='actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a'
            or receipt.get('if')!='always()'
            or receipt.get('with',{}).get('path')!='artifacts/erdos-three-source-resolution'):
        errors.append(f'{key}: source-adjudication receipt retention missing')
    for forbidden in ('permission-administration','gh pr merge','gh project item-edit',
                      'git push','pull_request_target','secrets.GCL_RELEASE_TRUST'):
        if forbidden in source:
            errors.append(f'{key}: forbidden control plane capability {forbidden}')
    return errors


def workflow_coverage_errors(root=ROOT, texts=None, evidence=None, registry=None):
    texts = v3.legacy.workflow_texts(root) if texts is None else texts
    errors = v3.workflow_coverage_errors(root=root, texts=texts, evidence=evidence)
    pilot_errors = erdos_forge_copilot_pilot_errors(texts)
    delegated_permission_errors = {
        f"{RECOVERY_FAILOVER_WORKFLOW}:recover: non-Pages job permissions may not exceed contents: read",
        f"{QUALIFICATION_ONLY_WORKFLOW}:admit: non-Pages job permissions may not exceed contents: read",
        f"{QUALIFICATION_ONLY_WORKFLOW}:qualify: non-Pages job permissions may not exceed contents: read",
        "erdos-catalogue-intake.yml:capture: non-Pages job permissions may not exceed contents: read",
        "erdos-catalogue-queue-projection.yml:reconcile: non-Pages job permissions may not exceed contents: read",
    }
    if not pilot_errors:
        delegated_permission_errors |= {
            "erdos-catalogue-queue-projection.yml:forge-pilot-review: non-Pages job permissions may not exceed contents: read",
            "erdos-catalogue-queue-projection.yml:forge-pilot-evidence: non-Pages job permissions may not exceed contents: read",
        }
    errors = [error for error in errors if error not in delegated_permission_errors]
    errors.extend(pilot_errors)
    errors.extend(recovery_failover_errors(texts))
    errors.extend(remediation_envelope_errors(texts))
    errors.extend(rolling_review_direct_errors(texts))
    errors.extend(three_source_council_errors(texts))
    queue_projection = texts.get("erdos-catalogue-queue-projection.yml")
    if queue_projection is not None:
        workflow = v3.legacy.load_yaml_text(queue_projection)
        jobs = workflow.get("jobs", {})
        projection = _job(workflow, "reconcile")
        if (workflow.get("permissions") != {"contents": "read"} or
                set(jobs) != {"reconcile", "ledger", "canary",
                              "forge-pilot-review", "forge-pilot-evidence"}):
            errors.append("erdos queue projection: unrecognized workflow or write scope")
        ledger = _job(workflow, "ledger")
        canary = _job(workflow, "canary")
        if ledger.get("permissions") != {"contents": "read"} or canary.get("permissions") != {"contents": "read"}:
            errors.append("erdos event custody: only base contents-read job permissions allowed")
        ledger_text = str(ledger)
        canary_text = str(canary)
        for required in (
            "ci/erdos_event_custody.py --mode ledger",
            "steps.ledger-token.outputs.token",
            "secrets.GCL_COUNCIL_CLERK_APP_ID",
            "secrets.GCL_COUNCIL_CLERK_PRIVATE_KEY",
            "permission-issues",
        ):
            if required not in ledger_text:
                errors.append(f"erdos event custody: missing bounded ledger marker {required}")
        for required in ("ci/erdos_event_custody.py --mode canary", "github.token", "2500"):
            if required not in canary_text:
                errors.append(f"erdos event canary: missing isolated acceptance marker {required}")
        if "permission-organization-projects" in ledger_text or "steps.queue-token.outputs.token" in ledger_text:
            errors.append("erdos event custody: ledger must not use Project mutation token")
        if projection.get("permissions") != {"contents": "read", "issues": "write"}:
            errors.append("erdos queue projection: exact job write permissions required")
        steps = projection.get("steps", [])
        runs = "\\n".join(str(step.get("run", "")) for step in steps)
        if ("ci/erdos_catalogue_programme_intake.py --live-snapshot" not in runs
                or "ci/erdos_catalogue_queue_projection.py --report" not in runs
                or "steps.queue-token.outputs.token" not in queue_projection
                or "permission-organization-projects: write" not in queue_projection
                or "permission-issues: write" not in queue_projection
                or "secrets.GCL_COUNCIL_CLERK_APP_ID" not in queue_projection
                or "secrets.GCL_COUNCIL_CLERK_PRIVATE_KEY" not in queue_projection):
            errors.append("erdos queue projection: evidence source / scoped credential binding drift")
    catalogue = texts.get("erdos-catalogue-intake.yml")
    if catalogue is not None:
        workflow = v3.legacy.load_yaml_text(catalogue)
        capture = _job(workflow, "capture")
        if capture.get("permissions") != {"contents":"read","issues":"read"}:
            errors.append("erdos-catalogue-intake.yml:capture: permissions must be contents-read and issues-read only")
        if set(workflow.get("jobs", {})) != {"test", "capture"}:
            errors.append("erdos-catalogue-intake.yml: unexpected capture topology")
        checkouts = [step for step in capture.get("steps", []) if step.get("uses", "").startswith("actions/checkout@")]
        if len(checkouts) != 1 or checkouts[0].get("with", {}).get("ref") != "main":
            errors.append("erdos-catalogue-intake.yml:capture: trusted-main checkout required")
        if "write" in json.dumps(capture.get("permissions", {})):
            errors.append("erdos-catalogue-intake.yml:capture: repository mutation is forbidden")
        if "secrets." in catalogue or "secrets[" in catalogue:
            errors.append("erdos-catalogue-intake.yml: repository secrets are outside the read-only capture envelope")

    commands = _registry_commands(root=root, registry=registry)
    prefix = "ci.yml: missing workflow coverage marker "
    retained: list[str] = []
    for error in errors:
        if not error.startswith(prefix):
            retained.append(error)
            continue
        marker = error[len(prefix) :]
        routed = ROUTED_MARKER_SUCCESSORS.get(marker, marker)
        if _normalize_command(routed) in commands:
            continue
        retained.append(error)
    return retained


def main() -> int:
    errors = workflow_coverage_errors()
    if errors:
        for error in errors:
            print(error, file=__import__("sys").stderr)
        print(
            f"workflow coverage v3 validation failed with {len(errors)} error(s)",
            file=__import__("sys").stderr,
        )
        return 1
    print(
        "workflow coverage v3: direct workflow and governed shard-registry execution roots, "
        "active bounded administrative runtime, separated Candidate and Referee identities, "
        "protected expected-head PR merge, exact Aug13 PR-close recovery failover, trusted-main "
        "delegated remediation Referee admission with trusted comment fallback, Candidate expected-head merge, "
        "post-merge qualification, durable admission and issue-status audit, mirror-only synchronization, "
        "manual control-plane gates, and claim boundaries are valid"
    )
    return 0


__all__ = [
    "ROOT",
    "RECOVERY_FAILOVER_WORKFLOW",
    "QUALIFICATION_ONLY_WORKFLOW",
    "recovery_failover_errors",
    "remediation_envelope_errors",
    "workflow_coverage_errors",
    "main",
]

if __name__ == "__main__":
    raise SystemExit(main())
