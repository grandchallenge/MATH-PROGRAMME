from __future__ import annotations

"""Live, read-only integration boundary for the generic protected-receipt protocol.

The administrative-review receipt lane is intentionally suspended here.  This
module may classify live state and emit qualification diagnostics, but it does
not create receipt, ledger, mirror, ruleset, bypass, or Human Steward authority.
"""

import argparse
import copy
import json
import os
import re
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
    LaneState,
    MirrorState,
    ProductState,
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
_FRONTIER_RE = re.compile(r"- `(?P<procedure>[^`]+)` completed through: `(?P<due>[^`]+)`")


class SuspendedReceiptLaneError(AutonomyError):
    def __init__(self, diagnostic: Mapping[str, Any]) -> None:
        self.diagnostic = dict(diagnostic)
        super().__init__(json.dumps(self.diagnostic, sort_keys=True, separators=(",", ":")))


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
            value = self.client.get(
                f"/repos/{repository}/compare/{ancestor}...{descendant}"
            )
        except Exception:
            return None
        status = str(value.get("status") or "").lower()
        if status in {"ahead", "identical"}:
            return True
        if status in {"behind", "diverged"}:
            return False
        return None

    def check_runs(self, repository: str, head_sha: str) -> Sequence[Mapping[str, Any]]:
        value = self.client.get(
            f"/repos/{repository}/commits/{head_sha}/check-runs?per_page=100"
        )
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


def live_read_only_qualification(report_path: Path) -> int:
    require_runtime_modules(("jsonschema",))
    root = Path(__file__).resolve().parents[1]
    runtime = json.loads(
        (root / "governance" / "administrative_autonomy_runtime_integration.json").read_text(
            encoding="utf-8"
        )
    )
    repository = str(runtime["repository"])
    runtime_capability_sets(runtime)
    candidate = Client(os.environ.get("CANDIDATE_TOKEN", ""))
    administrator = Client(os.environ.get("ADMIN_TOKEN", ""))
    evidence = Client(os.environ.get("EVIDENCE_TOKEN", ""))
    provider = LiveClientProvider(candidate)
    protected_head = provider.branch_sha(repository, "main")
    config = read_only_configuration_preflight(administrator, repository, runtime)
    ledger = json_content(candidate, repository, STATE_PATH, "main")
    if ledger is None:
        raise AutonomyError("protected completion ledger is absent")

    mirror_results: list[dict[str, Any]] = []
    for mirror in runtime.get("mirrors", []):
        mirror_repo = str(mirror["repository"])
        issue_number = int(mirror["issue"])
        try:
            issue = evidence.get(f"/repos/{mirror_repo}/issues/{issue_number}")
            body = str(issue.get("body") or "")
            result = classify_mirror_issue(
                body,
                ledger,
                ADMINISTRATIVE_REVIEW_PROCEDURE,
                protected_head,
            )
        except Exception as exc:
            result = MirrorResult(
                state=MirrorState.MIRROR_UNAVAILABLE,
                receipt_chain_complete=False,
                protected_completion_claim=False,
                reason=f"mirror read failed: {type(exc).__name__}",
            )
        mirror_results.append(
            {
                "repository": mirror_repo,
                "issue": issue_number,
                "state": result.state.value,
                "reason": result.reason,
                "protected_completion_claim": result.protected_completion_claim,
            }
        )

    report = {
        "schema_version": "1.0.0",
        "state": "SUSPENDED_INTEGRATION_READ_ONLY_QUALIFIED"
        if config.state == ConfigState.CONVERGED
        else "SUSPENDED_INTEGRATION_FAILED_CLOSED",
        "lane_state": LaneState.SUSPENDED.value,
        "protected_head": protected_head,
        "configuration_state": config.state.value,
        "configuration_target_present": config.target_present,
        "mirror_results": mirror_results,
        "authority_created": False,
        "mutation_performed": False,
        "ruleset_mutation_performed": False,
        "receipt_mutation_performed": False,
        "ledger_mutation_performed": False,
        "mirror_mutation_performed": False,
        "bypass_exercised": False,
        "direct_protected_push": False,
        "human_steward_identity_asserted": False,
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if config.state == ConfigState.CONVERGED else 1


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    qualify = sub.add_parser("qualify")
    qualify.add_argument("--report", type=Path, default=DEFAULT_QUALIFICATION_REPORT)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "qualify":
        return live_read_only_qualification(args.report)
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
