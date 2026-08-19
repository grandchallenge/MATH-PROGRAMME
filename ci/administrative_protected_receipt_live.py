from __future__ import annotations

"""Live, read-only integration boundary for the generic protected-receipt protocol.

The administrative-review receipt lane is intentionally suspended here. This
module may classify live state and emit qualification diagnostics, but it does
not create receipt, ledger, mirror, ruleset, bypass, or Human Steward authority.
"""

import argparse
import copy
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import sys
import tempfile
import urllib.parse
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from administrative_protected_receipt_adapters import (
    ConfigObservation,
    ConfigurationAdapter,
    DesiredConfiguration,
    GitHubFacts,
    GitHubStateAdapter,
    RulesetActor,
)
from administrative_protected_receipt_engine import (
    AuthoritativeFrontier,
    DerivedFrontier,
    MirrorAdapter,
    MirrorResult,
)
from administrative_protected_receipt_model import (
    ActorIdentity,
    ActorRole,
    Capability,
    CapabilitySet,
    ConfigState,
    DispositionState,
    LaneState,
    MirrorState,
    ProductState,
    ReviewState,
    failure_diagnostic,
    require_runtime_modules,
    sha256_json,
    validate_role_separation,
)
from autonomy_github import AutonomyError, Client, json_content

ADMINISTRATIVE_REVIEW_PROCEDURE = "administrative_review"
STATE_PATH = "governance/administrative_maintenance_completion_state.json"
DEFAULT_DIAGNOSTIC_PATH = Path("administrative-protected-receipt-diagnostic.json")
DEFAULT_QUALIFICATION_REPORT = Path("administrative-protected-receipt-qualification.json")
DEFAULT_INTEGRATION_MERGE = "8ff752b4f2ac28d87575d4f4ef48f564fb18837b"
DEFAULT_RECEIPT_PR = 596
_FRONTIER_RE = re.compile(r"- `(?P<procedure>[^`]+)` completed through: `(?P<due>[^`]+)`")


class SuspendedReceiptLaneError(AutonomyError):
    def __init__(self, diagnostic: Mapping[str, Any]) -> None:
        self.diagnostic = dict(diagnostic)
        super().__init__(json.dumps(self.diagnostic, sort_keys=True, separators=(",", ":")))


class QualificationFailure(AutonomyError):
    def __init__(self, code: str, detail: str) -> None:
        self.code = code
        self.detail = detail
        super().__init__(f"{code}: {detail}")


class LiveClientProvider:
    """Adapt the existing bounded Client to the generic typed GitHub adapter."""

    def __init__(
        self,
        client: Client,
        *,
        required_checks: Sequence[str] = (),
        mutation_allowed: bool = False,
    ) -> None:
        self.client = client
        self.required_checks = tuple(required_checks)
        self.mutation_allowed = mutation_allowed

    def pull_request(self, repository: str, pr_number: int) -> Mapping[str, Any]:
        value = copy.deepcopy(self.client.get(f"/repos/{repository}/pulls/{pr_number}"))
        value["required_checks"] = list(self.required_checks)
        return value

    def branch_sha(self, repository: str, branch: str) -> str:
        encoded = urllib.parse.quote(branch, safe="")
        value = self.client.get(f"/repos/{repository}/git/ref/heads/{encoded}")
        return str(value.get("object", {}).get("sha") or "")

    def is_ancestor(self, repository: str, ancestor: str, descendant: str) -> bool | None:
        if not ancestor or not descendant:
            return None
        if ancestor == descendant:
            return True
        try:
            value = self.client.get(f"/repos/{repository}/compare/{ancestor}...{descendant}")
        except Exception:
            return None
        status = str(value.get("status") or "").lower()
        if status in {"ahead", "identical"}:
            return True
        if status in {"behind", "diverged"}:
            return False
        return None

    def check_runs(self, repository: str, head_sha: str) -> Sequence[Mapping[str, Any]]:
        value = self.client.get(f"/repos/{repository}/commits/{head_sha}/check-runs?per_page=100")
        runs = value.get("check_runs", []) if isinstance(value, Mapping) else []
        return [
            {
                "name": str(item.get("name") or ""),
                "head_sha": str(item.get("head_sha") or head_sha),
                "status": item.get("status"),
                "conclusion": item.get("conclusion"),
            }
            for item in runs
        ]

    def reviews(self, repository: str, pr_number: int) -> Sequence[Mapping[str, Any]]:
        return self.client.get(f"/repos/{repository}/pulls/{pr_number}/reviews?per_page=100")

    def issue_comments(self, repository: str, issue_number: int) -> Sequence[Mapping[str, Any]]:
        return self.client.get(f"/repos/{repository}/issues/{issue_number}/comments?per_page=100")

    def update_branch(self, repository: str, pr_number: int, expected_head_sha: str) -> Mapping[str, Any]:
        if not self.mutation_allowed:
            raise AutonomyError("protected-receipt live provider is read-only")
        self.client.put(
            f"/repos/{repository}/pulls/{pr_number}/update-branch",
            {"expected_head_sha": expected_head_sha},
        )
        pull = self.client.get(f"/repos/{repository}/pulls/{pr_number}")
        return {"head_sha": str(pull.get("head", {}).get("sha") or "")}


def classify_receipt_pull_for_sync(
    candidate: Client,
    repository: str,
    pull_request: int,
    declared_base_snapshot: str,
    *,
    update_control_permitted: bool,
) -> GitHubFacts:
    provider = LiveClientProvider(candidate, mutation_allowed=False)
    return GitHubStateAdapter(provider).classify_pr(
        repository,
        pull_request,
        declared_base_snapshot,
        update_control_permitted=update_control_permitted,
    )


def runtime_capability_sets(runtime: Mapping[str, Any]) -> tuple[CapabilitySet, CapabilitySet, CapabilitySet]:
    candidate_raw = runtime["candidate_identity"]
    admin_raw = runtime["administrator_identity"]
    referee_raw = runtime["referee_identity"]
    candidate = CapabilitySet(
        ActorRole.CANDIDATE,
        ActorIdentity(
            str(candidate_raw["login"]),
            int(candidate_raw["app_id"]),
            str(candidate_raw["token_role"]),
        ),
        frozenset(
            {
                Capability.READ_EVIDENCE,
                Capability.WRITE_CANDIDATE,
                Capability.UPDATE_CANDIDATE_BRANCH,
                Capability.MERGE_PULL_REQUEST_EXACT_HEAD,
            }
        ),
    )
    administration = CapabilitySet(
        ActorRole.ADMINISTRATION,
        ActorIdentity(
            str(admin_raw["login"]),
            int(admin_raw["app_id"]),
            str(admin_raw["token_role"]),
        ),
        frozenset({Capability.READ_CONFIGURATION}),
    )
    referee = CapabilitySet(
        ActorRole.REFEREE,
        ActorIdentity(
            str(referee_raw["login"]),
            int(referee_raw["app_id"]),
            str(referee_raw["token_role"]),
        ),
        frozenset({Capability.READ_EVIDENCE, Capability.RECORD_REFEREE_DISPOSITION}),
    )
    failures = validate_role_separation(candidate, referee, administration)
    if failures:
        raise AutonomyError("protected-receipt capability separation failed: " + "; ".join(failures))
    return candidate, administration, referee


def _capability_dict(value: CapabilitySet) -> dict[str, Any]:
    return {
        "role": value.role.value,
        "identity": {
            "login": value.identity.login,
            "app_id": value.identity.app_id,
            "token_role": value.identity.token_role,
        },
        "capabilities": sorted(cap.value for cap in value.capabilities),
    }


def read_only_configuration_preflight(
    administrator: Client,
    repository: str,
    runtime: Mapping[str, Any],
) -> ConfigObservation:
    desired = DesiredConfiguration(
        int(runtime["ruleset_id"]),
        RulesetActor(
            int(runtime["administrator_identity"]["app_id"]),
            "Integration",
            "pull_request",
        ),
        direct_protected_push=False,
    )
    try:
        raw = administrator.get(f"/repos/{repository}/rulesets/{desired.ruleset_id}")
    except Exception:
        raw = None
    return ConfigurationAdapter().observe(desired, raw)


def authoritative_frontier(
    ledger: Mapping[str, Any], procedure_id: str, protected_head: str
) -> AuthoritativeFrontier:
    procedure = ledger.get("procedures", {}).get(procedure_id)
    if not isinstance(procedure, Mapping):
        raise AutonomyError(f"protected completion ledger missing procedure: {procedure_id}")
    return AuthoritativeFrontier(
        procedure_id,
        str(procedure.get("completed_through_utc") or ""),
        int(procedure.get("receipt_count") or 0),
        sha256_json(ledger),
        protected_head,
    )


def derived_frontier_from_issue_body(body: str, procedure_id: str) -> DerivedFrontier:
    matches = [m for m in _FRONTIER_RE.finditer(body) if m.group("procedure") == procedure_id]
    if len(matches) != 1:
        return DerivedFrontier(None, available=bool(body))
    return DerivedFrontier(matches[0].group("due"))


def classify_mirror_issue(
    body: str,
    ledger: Mapping[str, Any],
    procedure_id: str,
    protected_head: str,
) -> MirrorResult:
    return MirrorAdapter().classify(
        authoritative_frontier(ledger, procedure_id, protected_head),
        derived_frontier_from_issue_body(body, procedure_id),
    )


def _diagnostic_path() -> Path:
    raw = os.environ.get("GCL_PROTECTED_RECEIPT_DIAGNOSTIC", "")
    return Path(raw) if raw else DEFAULT_DIAGNOSTIC_PATH


def emit_diagnostic(value: Mapping[str, Any]) -> None:
    path = _diagnostic_path()
    path.write_text(json.dumps(dict(value), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def lane_suspension_diagnostic(
    *, phase: str, procedure_id: str, occurrence: str | None = None
) -> dict[str, Any]:
    state = ProductState(lane=LaneState.SUSPENDED)
    inputs = [f"procedure:{procedure_id}", f"phase:{phase}"]
    if occurrence:
        inputs.append(f"occurrence:{occurrence}")
    return failure_diagnostic(
        transition_id="ADMINISTRATIVE_REVIEW_SUSPENSION_GATE",
        state=state,
        predicate="procedure_id != administrative_review while suspended",
        inputs=inputs,
        code="ADMINISTRATIVE_REVIEW_RECEIPT_LANE_SUSPENDED",
    )


def suspended_pending_closures(*args: Any, base: Callable[..., list[dict[str, Any]]], **kwargs: Any) -> list[dict[str, Any]]:
    values = list(base(*args, **kwargs))
    kept: list[dict[str, Any]] = []
    for item in values:
        manifest = item.get("manifest", {})
        if str(manifest.get("procedure_id") or "") == ADMINISTRATIVE_REVIEW_PROCEDURE:
            emit_diagnostic(
                lane_suspension_diagnostic(
                    phase="pending_closure",
                    procedure_id=ADMINISTRATIVE_REVIEW_PROCEDURE,
                    occurrence=str(manifest.get("occurrence_key") or "") or None,
                )
            )
            continue
        kept.append(item)
    return kept


def suspended_eligible_candidates(*args: Any, base: Callable[..., list[Any]], **kwargs: Any) -> list[Any]:
    values = list(base(*args, **kwargs))
    kept: list[Any] = []
    for item in values:
        try:
            manifest = item[1]
        except Exception:
            kept.append(item)
            continue
        if str(manifest.get("procedure_id") or "") == ADMINISTRATIVE_REVIEW_PROCEDURE:
            emit_diagnostic(
                lane_suspension_diagnostic(
                    phase="eligible_candidate",
                    procedure_id=ADMINISTRATIVE_REVIEW_PROCEDURE,
                    occurrence=str(manifest.get("occurrence_key") or "") or None,
                )
            )
            continue
        kept.append(item)
    return kept


def suspended_stage_completion_receipt(
    candidate: Client,
    referee: Client,
    administrator: Client,
    repo: str,
    runtime: dict[str, Any],
    record_id: str,
    procedure_id: str,
    due: str,
    record_path: str,
    record: dict[str, Any],
    source_pull_request: int,
    source_head: str,
    source_merge_sha: str,
    referee_login: str,
    candidate_login: str,
    *,
    base: Callable[..., dict[str, Any]],
) -> dict[str, Any]:
    if procedure_id == ADMINISTRATIVE_REVIEW_PROCEDURE:
        diagnostic = lane_suspension_diagnostic(
            phase="stage_completion_receipt",
            procedure_id=procedure_id,
            occurrence=f"{procedure_id}:{due}",
        )
        emit_diagnostic(diagnostic)
        raise SuspendedReceiptLaneError(diagnostic)
    return base(
        candidate,
        referee,
        administrator,
        repo,
        runtime,
        record_id,
        procedure_id,
        due,
        record_path,
        record,
        source_pull_request,
        source_head,
        source_merge_sha,
        referee_login,
        candidate_login,
    )


def validate_runtime_environment(
    *,
    python_version: tuple[int, int] | None = None,
    system_name: str | None = None,
    os_release: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    version = python_version or (sys.version_info.major, sys.version_info.minor)
    system = system_name or platform.system()
    release = dict(os_release or _read_os_release())
    if version != (3, 12):
        raise QualificationFailure("ENVIRONMENT_PYTHON_MISMATCH", f"required 3.12, observed {version[0]}.{version[1]}")
    if system != "Linux" or release.get("ID") != "ubuntu" or release.get("VERSION_ID") != "24.04":
        raise QualificationFailure(
            "ENVIRONMENT_RUNNER_MISMATCH",
            f"required Ubuntu 24.04/Linux, observed {system}/{release.get('ID')}/{release.get('VERSION_ID')}",
        )
    return {
        "python": f"{version[0]}.{version[1]}",
        "python_full": platform.python_version(),
        "system": system,
        "distribution": release.get("ID"),
        "distribution_version": release.get("VERSION_ID"),
        "runner_os": os.environ.get("RUNNER_OS"),
        "runner_arch": os.environ.get("RUNNER_ARCH"),
        "image_os": os.environ.get("ImageOS"),
    }


def _read_os_release(path: Path = Path("/etc/os-release")) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        if "=" not in raw or raw.lstrip().startswith("#"):
            continue
        key, value = raw.split("=", 1)
        values[key] = value.strip().strip('"')
    return values


def dependency_identity(root: Path) -> dict[str, Any]:
    require_runtime_modules(("jsonschema",))
    requirement_path = root / "requirements" / "policy.txt"
    if not requirement_path.exists():
        raise QualificationFailure("ENVIRONMENT_DEPENDENCY_FAILURE", "requirements/policy.txt is absent")
    return {
        "requirements_path": "requirements/policy.txt",
        "requirements_sha256": hashlib.sha256(requirement_path.read_bytes()).hexdigest(),
        "jsonschema_version": importlib.metadata.version("jsonschema"),
    }


def declared_base_from_candidate_head(candidate: Client, repository: str, head_sha: str) -> str:
    commit = candidate.get(f"/repos/{repository}/commits/{head_sha}")
    parents = commit.get("parents", []) if isinstance(commit, Mapping) else []
    if len(parents) != 1 or not isinstance(parents[0], Mapping):
        raise QualificationFailure("RECEIPT_DECLARED_BASE_UNKNOWN", "receipt candidate must have exactly one parent")
    value = str(parents[0].get("sha") or "")
    if not value:
        raise QualificationFailure("RECEIPT_DECLARED_BASE_UNKNOWN", "receipt candidate parent SHA is absent")
    return value


def _review_state(provider: LiveClientProvider, repository: str, pr_number: int, head_sha: str) -> ReviewState:
    reviews = list(provider.reviews(repository, pr_number))
    approved = [x for x in reviews if str(x.get("state") or x.get("review") or "").upper() == "APPROVED"]
    if any(str(x.get("commit_id") or x.get("head_sha") or "") == head_sha for x in approved):
        return ReviewState.PRESENT_FOR_HEAD
    if approved:
        return ReviewState.STALE_FOR_HEAD
    return ReviewState.ABSENT


def _facts_dict(facts: GitHubFacts) -> dict[str, Any]:
    return {
        "current_base_sha": facts.current_base_sha,
        "candidate_head_sha": facts.candidate_head_sha,
        "candidate_recorded_base_sha": facts.candidate_recorded_base_sha,
        "branch_state": facts.branch_state.value,
        "conflict_state": facts.conflict_state.value,
        "check_state": facts.check_state.value,
        "update_branch_state": facts.update_branch_state.value,
        "raw_advisory": dict(facts.raw_advisory),
    }


def suspension_guard_trace() -> dict[str, Any]:
    called: list[str] = []
    old = os.environ.get("GCL_PROTECTED_RECEIPT_DIAGNOSTIC")
    with tempfile.TemporaryDirectory() as td:
        os.environ["GCL_PROTECTED_RECEIPT_DIAGNOSTIC"] = str(Path(td) / "diagnostic.json")
        try:
            pending = suspended_pending_closures(
                base=lambda: [{"manifest": {"procedure_id": ADMINISTRATIVE_REVIEW_PROCEDURE, "occurrence_key": "qualification"}}]
            )
            eligible = suspended_eligible_candidates(
                base=lambda: [({"number": DEFAULT_RECEIPT_PR}, {"procedure_id": ADMINISTRATIVE_REVIEW_PROCEDURE, "occurrence_key": "qualification"})]
            )
            stage_blocked = False
            try:
                suspended_stage_completion_receipt(
                    object(), object(), object(), "r", {}, "record", ADMINISTRATIVE_REVIEW_PROCEDURE,
                    "2026-08-13T01:21:00Z", "record.json", {}, DEFAULT_RECEIPT_PR,
                    "a" * 40, "b" * 40, "ref", "candidate",
                    base=lambda *args: called.append("stage"),
                )
            except SuspendedReceiptLaneError:
                stage_blocked = True
        finally:
            if old is None:
                os.environ.pop("GCL_PROTECTED_RECEIPT_DIAGNOSTIC", None)
            else:
                os.environ["GCL_PROTECTED_RECEIPT_DIAGNOSTIC"] = old
    return {
        "pending_closure_blocked": pending == [],
        "eligible_candidate_blocked": eligible == [],
        "receipt_staging_blocked": stage_blocked and not called,
        "candidate_synchronization_unavailable": True,
        "protected_merge_unavailable": True,
        "ledger_mutation_unavailable": True,
        "mirror_advancement_unavailable": True,
        "ruleset_mutation_unavailable": True,
        "direct_protected_push_unavailable": True,
        "bypass_unavailable": True,
        "human_steward_synthesis_unavailable": True,
    }


def _mirror_observations(
    evidence: Client,
    runtime: Mapping[str, Any],
    ledger: Mapping[str, Any],
    protected_head: str,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for mirror in runtime.get("mirrors", []):
        mirror_repo = str(mirror["repository"])
        issue_number = int(mirror["issue"])
        derived = DerivedFrontier(None, available=False)
        try:
            issue = evidence.get(f"/repos/{mirror_repo}/issues/{issue_number}")
            body = str(issue.get("body") or "")
            derived = derived_frontier_from_issue_body(body, ADMINISTRATIVE_REVIEW_PROCEDURE)
            result = classify_mirror_issue(body, ledger, ADMINISTRATIVE_REVIEW_PROCEDURE, protected_head)
        except Exception as exc:
            result = MirrorResult(
                state=MirrorState.MIRROR_UNAVAILABLE,
                receipt_chain_complete=False,
                protected_completion_claim=False,
                reason=f"mirror read failed: {type(exc).__name__}",
            )
        output.append(
            {
                "repository": mirror_repo,
                "issue": issue_number,
                "derived_frontier": derived.observed_through_utc,
                "state": result.state.value,
                "reason": result.reason,
                "protected_completion_claim": result.protected_completion_claim,
            }
        )
    return output


def collect_live_snapshot(
    *,
    candidate: Client,
    administrator: Client,
    evidence: Client,
    repository: str,
    runtime: Mapping[str, Any],
    protected_head: str,
    receipt_pr: int,
    integration_merge: str,
) -> dict[str, Any]:
    provider = LiveClientProvider(candidate, mutation_allowed=False)
    integration_ancestor = provider.is_ancestor(repository, integration_merge, protected_head)
    if integration_ancestor is not True:
        raise QualificationFailure(
            "PROTECTED_INTEGRATION_ANCESTRY_FAILURE",
            f"{integration_merge} is not a verified ancestor of {protected_head}",
        )
    candidate_caps, admin_caps, referee_caps = runtime_capability_sets(runtime)
    config = read_only_configuration_preflight(administrator, repository, runtime)
    if config.state != ConfigState.CONVERGED:
        raise QualificationFailure("CONFIGURATION_NOT_CONVERGED", config.reason or config.state.value)
    ledger = json_content(candidate, repository, STATE_PATH, "main")
    if ledger is None:
        raise QualificationFailure("PROTECTED_LEDGER_ABSENT", "protected completion ledger is absent")
    frontier = authoritative_frontier(ledger, ADMINISTRATIVE_REVIEW_PROCEDURE, protected_head)
    pull = provider.pull_request(repository, receipt_pr)
    receipt_head = str(pull.get("head", {}).get("sha") or "")
    if not receipt_head:
        raise QualificationFailure("RECEIPT_HEAD_ABSENT", f"PR #{receipt_pr} head is absent")
    declared_base = declared_base_from_candidate_head(candidate, repository, receipt_head)
    facts = GitHubStateAdapter(provider).classify_pr(
        repository,
        receipt_pr,
        declared_base,
        update_control_permitted=False,
    )
    review_state = _review_state(provider, repository, receipt_pr, receipt_head)
    disposition_state = DispositionState.NOT_REQUIRED_BY_CONTROL
    return {
        "protected_head": protected_head,
        "protected_integration_merge": integration_merge,
        "protected_integration_is_ancestor": True,
        "configuration": {
            "state": config.state.value,
            "ruleset_id": int(runtime["ruleset_id"]),
            "actor_id": int(runtime["administrator_identity"]["app_id"]),
            "actor_type": "Integration",
            "bypass_mode": "pull_request",
            "observed_digest": config.observed_digest,
            "target_present": config.target_present,
            "non_target_digest": config.non_target_digest,
            "body_digest": config.body_digest,
            "mutation_performed": False,
        },
        "identities": {
            "candidate": _capability_dict(candidate_caps),
            "administration": _capability_dict(admin_caps),
            "referee": _capability_dict(referee_caps),
            "role_separation_valid": True,
        },
        "receipt_pull": {
            "number": receipt_pr,
            "observation_classification": "OBSERVATION_ONLY__NO_MUTATION",
            "head_sha": receipt_head,
            "declared_base_sha": declared_base,
            "state": str(pull.get("state") or ""),
            "merged": bool(pull.get("merged")),
            "facts": _facts_dict(facts),
            "review_state": review_state.value,
            "disposition_state": disposition_state.value,
            "synchronization_performed": False,
            "merge_performed": False,
        },
        "authoritative_frontier": {
            "procedure_id": frontier.procedure_id,
            "completed_through_utc": frontier.completed_through_utc,
            "receipt_count": frontier.receipt_count,
            "ledger_digest": frontier.source_digest,
            "protected_head": frontier.protected_head,
        },
        "mirror_results": _mirror_observations(evidence, runtime, ledger, protected_head),
        "suspension_guard_trace": suspension_guard_trace(),
        "safety": {
            "authority_created": False,
            "mutation_performed": False,
            "receipt_mutation_performed": False,
            "ledger_mutation_performed": False,
            "mirror_mutation_performed": False,
            "ruleset_mutation_performed": False,
            "bypass_exercised": False,
            "direct_protected_push": False,
            "human_steward_identity_asserted": False,
            "reactivation_authorized": False,
        },
    }


def _stable_snapshot_digest(snapshot: Mapping[str, Any]) -> str:
    return sha256_json(snapshot)


def require_stable_protected_head(start_head: str, observed_head: str, phase: str) -> None:
    if observed_head != start_head:
        raise QualificationFailure(
            "PROTECTED_MAIN_MOVED",
            f"protected main moved during {phase}: {start_head} -> {observed_head}",
        )


def live_read_only_qualification(
    report_path: Path,
    *,
    control_id: str = "UNBOUND_CONTROL",
    control_issue: int | None = None,
    authorization_comment_id: int | None = None,
    receipt_pr: int = DEFAULT_RECEIPT_PR,
    integration_merge: str = DEFAULT_INTEGRATION_MERGE,
) -> int:
    root = Path(__file__).resolve().parents[1]
    report: dict[str, Any] = {
        "schema_version": "2.0.0",
        "control_id": control_id,
        "control_issue": control_issue,
        "authorization_comment_id": authorization_comment_id,
        "run_identity": {
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
            "github_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "github_workflow_ref": os.environ.get("GITHUB_WORKFLOW_REF"),
            "github_sha": os.environ.get("GITHUB_SHA"),
        },
        "lane_state": LaneState.SUSPENDED.value,
        "authority_created": False,
        "mutation_performed": False,
        "reactivation_authorized": False,
    }
    try:
        report["environment"] = validate_runtime_environment()
        report["dependencies"] = dependency_identity(root)
        runtime = json.loads(
            (root / "governance" / "administrative_autonomy_runtime_integration.json").read_text(encoding="utf-8")
        )
        repository = str(runtime["repository"])
        candidate = Client(os.environ.get("CANDIDATE_TOKEN", ""))
        administrator = Client(os.environ.get("ADMIN_TOKEN", ""))
        evidence = Client(os.environ.get("EVIDENCE_TOKEN", ""))
        provider = LiveClientProvider(candidate, mutation_allowed=False)
        start_head = provider.branch_sha(repository, "main")
        if not start_head:
            raise QualificationFailure("PROTECTED_HEAD_ABSENT", "protected main head is absent")
        report["protected_head_start"] = start_head
        first = collect_live_snapshot(
            candidate=candidate,
            administrator=administrator,
            evidence=evidence,
            repository=repository,
            runtime=runtime,
            protected_head=start_head,
            receipt_pr=receipt_pr,
            integration_merge=integration_merge,
        )
        second_head = provider.branch_sha(repository, "main")
        require_stable_protected_head(start_head, second_head, "first-to-second-pass readback")
        second = collect_live_snapshot(
            candidate=candidate,
            administrator=administrator,
            evidence=evidence,
            repository=repository,
            runtime=runtime,
            protected_head=second_head,
            receipt_pr=receipt_pr,
            integration_merge=integration_merge,
        )
        end_head = provider.branch_sha(repository, "main")
        report["protected_head_end"] = end_head
        require_stable_protected_head(start_head, end_head, "final readback")
        first_digest = _stable_snapshot_digest(first)
        second_digest = _stable_snapshot_digest(second)
        report["first_pass"] = first
        report["second_pass"] = second
        report["idempotency"] = {
            "first_digest": first_digest,
            "second_digest": second_digest,
            "stable": first_digest == second_digest,
        }
        if first_digest != second_digest:
            raise QualificationFailure("IDEMPOTENT_REENTRY_MISMATCH", "first and second read-only snapshots differ")
        report["state"] = "LIVE_QUALIFICATION_GREEN__REACTIVATION_NOT_AUTHORIZED"
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        code = exc.code if isinstance(exc, QualificationFailure) else "LIVE_QUALIFICATION_EXCEPTION"
        detail = exc.detail if isinstance(exc, QualificationFailure) else f"{type(exc).__name__}: {exc}"
        report.setdefault("protected_head_end", report.get("protected_head_start"))
        report["state"] = f"LIVE_QUALIFICATION_FAILED_CLOSED__{code}"
        report["failure"] = {"code": code, "detail": detail}
        diagnostic = failure_diagnostic(
            transition_id="LIVE_QUALIFICATION_COORDINATOR",
            state=ProductState(lane=LaneState.SUSPENDED),
            predicate="complete qualification under stable protected state",
            inputs=[
                f"control:{control_id}",
                f"control_issue:{control_issue}",
                f"authorization_comment:{authorization_comment_id}",
                f"receipt_pr:{receipt_pr}",
                f"integration_merge:{integration_merge}",
            ],
            code=code,
        )
        diagnostic["detail"] = detail
        emit_diagnostic(diagnostic)
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    qualify = sub.add_parser("qualify")
    qualify.add_argument("--report", type=Path, default=DEFAULT_QUALIFICATION_REPORT)
    qualify.add_argument("--control-id", required=False, default=os.environ.get("GCL_LIVE_QUAL_CONTROL_ID", "UNBOUND_CONTROL"))
    qualify.add_argument("--control-issue", type=int, required=False, default=int(os.environ.get("GCL_LIVE_QUAL_CONTROL_ISSUE", "0")) or None)
    qualify.add_argument("--authorization-comment-id", type=int, required=False, default=int(os.environ.get("GCL_LIVE_QUAL_AUTHORIZATION_COMMENT_ID", "0")) or None)
    qualify.add_argument("--receipt-pr", type=int, default=DEFAULT_RECEIPT_PR)
    qualify.add_argument("--integration-merge", default=DEFAULT_INTEGRATION_MERGE)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "qualify":
        return live_read_only_qualification(
            args.report,
            control_id=args.control_id,
            control_issue=args.control_issue,
            authorization_comment_id=args.authorization_comment_id,
            receipt_pr=args.receipt_pr,
            integration_merge=args.integration_merge,
        )
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
