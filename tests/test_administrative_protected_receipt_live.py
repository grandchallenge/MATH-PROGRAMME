from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from administrative_protected_receipt_adapters import ConfigurationAdapter, DesiredConfiguration, GitHubStateAdapter, RulesetActor
from administrative_protected_receipt_engine import AuthoritativeFrontier, DerivedFrontier, MirrorAdapter
from administrative_protected_receipt_live import (
    ADMINISTRATIVE_REVIEW_PROCEDURE,
    LiveClientProvider,
    QualificationFailure,
    SuspendedReceiptLaneError,
    _stable_snapshot_digest,
    classify_receipt_pull_for_sync,
    read_only_configuration_preflight,
    require_stable_protected_head,
    runtime_capability_sets,
    suspension_guard_trace,
    suspended_eligible_candidates,
    suspended_pending_closures,
    suspended_stage_completion_receipt,
    validate_runtime_environment,
)
from administrative_protected_receipt_model import (
    BranchState,
    Capability,
    ConfigState,
    ConflictState,
    MirrorState,
)


class FakeClient:
    def __init__(self) -> None:
        self.current = "b" * 40
        self.declared = "a" * 40
        self.head = "1" * 40
        self.mergeable = True
        self.merge_state = "blocked"
        self.puts = []
        self.ruleset = {
            "id": 17137629,
            "name": "main",
            "target": "branch",
            "enforcement": "active",
            "conditions": {},
            "rules": [],
            "bypass_actors": [
                {"actor_id": 4423678, "actor_type": "Integration", "bypass_mode": "pull_request"}
            ],
        }

    def get(self, path: str):
        if path.endswith("/pulls/10"):
            return {
                "number": 10,
                "state": "open",
                "merged": False,
                "mergeable": self.mergeable,
                "mergeable_state": self.merge_state,
                "head": {"sha": self.head, "ref": "automation/maintenance/receipt-x"},
                "base": {"ref": "main"},
            }
        if path.endswith("/git/ref/heads/main"):
            return {"object": {"sha": self.current}}
        if "/compare/" in path:
            pair = path.split("/compare/", 1)[1]
            ancestor, descendant = pair.split("...", 1)
            if ancestor == self.current and descendant == self.head:
                return {"status": "diverged"}
            if ancestor == self.declared and descendant in {self.head, self.current}:
                return {"status": "ahead"}
            return {"status": "mystery"}
        if "/check-runs?" in path:
            return {"check_runs": []}
        if path.endswith("/rulesets/17137629"):
            return self.ruleset
        if "/reviews?" in path or "/comments?" in path:
            return []
        raise AssertionError(path)

    def put(self, path: str, payload: dict):
        self.puts.append((path, payload))
        raise AssertionError("read-only preflight must not mutate")


class DivergedClient(FakeClient):
    def get(self, path: str):
        if "/compare/" in path:
            return {"status": "behind"}
        return super().get(path)


class LiveProtectedReceiptTests(unittest.TestCase):
    def runtime(self):
        return {
            "ruleset_id": 17137629,
            "candidate_identity": {"login": "gcl-release-trust[bot]", "app_id": 4423678, "token_role": "candidate-and-merge-executor"},
            "administrator_identity": {"login": "gcl-release-trust[bot]", "app_id": 4423678, "token_role": "ruleset-readback"},
            "referee_identity": {"login": "github-actions[bot]", "app_id": 15368, "token_role": "referee"},
        }

    def test_blocked_is_advisory_while_ancestry_is_typed_behind(self):
        client = FakeClient()
        facts = classify_receipt_pull_for_sync(client, "grandchallenge/MATH-PROGRAMME", 10, client.declared, update_control_permitted=True)
        self.assertEqual(BranchState.BEHIND_CURRENT_BASE, facts.branch_state)
        self.assertEqual(ConflictState.CONFLICT_FREE, facts.conflict_state)
        self.assertEqual("blocked", facts.raw_advisory["mergeable_state"])

    def test_current_base_is_typed_clean_even_if_advisory_blocked(self):
        client = FakeClient(); client.head = client.current
        facts = classify_receipt_pull_for_sync(client, "grandchallenge/MATH-PROGRAMME", 10, client.declared, update_control_permitted=False)
        self.assertEqual(BranchState.AT_CURRENT_BASE, facts.branch_state)
        self.assertEqual(ConflictState.CONFLICT_FREE, facts.conflict_state)

    def test_diverged_from_declared_base_is_typed_diverged(self):
        client = DivergedClient()
        facts = classify_receipt_pull_for_sync(client, "grandchallenge/MATH-PROGRAMME", 10, client.declared, update_control_permitted=False)
        self.assertEqual(BranchState.DIVERGED_FROM_DECLARED_BASE, facts.branch_state)

    def test_true_content_conflict_is_typed_conflict(self):
        client = FakeClient(); client.mergeable = False
        facts = classify_receipt_pull_for_sync(client, "grandchallenge/MATH-PROGRAMME", 10, client.declared, update_control_permitted=True)
        self.assertEqual(ConflictState.CONFLICTED, facts.conflict_state)

    def test_unknown_ancestry_fails_closed_as_unknown(self):
        client = FakeClient()
        unknown_snapshot = "c" * 40
        facts = classify_receipt_pull_for_sync(client, "grandchallenge/MATH-PROGRAMME", 10, unknown_snapshot, update_control_permitted=True)
        self.assertEqual(BranchState.UNKNOWN, facts.branch_state)

    def test_live_provider_is_read_only(self):
        client = FakeClient()
        provider = LiveClientProvider(client)
        with self.assertRaises(Exception):
            provider.update_branch("grandchallenge/MATH-PROGRAMME", 10, client.head)
        self.assertEqual([], client.puts)

    def test_empty_required_checks_do_not_call_check_runs(self):
        class NoCheckRunsClient(FakeClient):
            def get(self, path: str):
                if "/check-runs?" in path:
                    raise AssertionError("empty required checks must not call check-runs")
                return super().get(path)

        provider = LiveClientProvider(NoCheckRunsClient())
        state = GitHubStateAdapter(provider).classify_checks(
            "grandchallenge/MATH-PROGRAMME", "1" * 40, ()
        )
        self.assertEqual("PASSING", state.value)

    def test_integration_ancestry_present_and_unknown_are_distinct(self):
        client = FakeClient(); provider = LiveClientProvider(client)
        self.assertTrue(provider.is_ancestor("grandchallenge/MATH-PROGRAMME", client.declared, client.current))
        self.assertIsNone(provider.is_ancestor("grandchallenge/MATH-PROGRAMME", "c" * 40, client.current))

    def test_runtime_capabilities_keep_candidate_and_admin_roles_separate(self):
        candidate, admin, referee = runtime_capability_sets(self.runtime())
        self.assertIn(Capability.WRITE_CANDIDATE, candidate.capabilities)
        self.assertIn(Capability.READ_CONFIGURATION, admin.capabilities)
        self.assertNotIn(Capability.WRITE_CONFIGURATION, admin.capabilities)
        self.assertNotEqual(candidate.identity.token_role, admin.identity.token_role)
        self.assertNotEqual(candidate.identity.login, referee.identity.login)

    def test_configuration_preflight_converged_without_mutation(self):
        client = FakeClient()
        observed = read_only_configuration_preflight(client, "grandchallenge/MATH-PROGRAMME", self.runtime())
        self.assertEqual(ConfigState.CONVERGED, observed.state)
        self.assertEqual([], client.puts)

    def test_configuration_adapter_missing_actor_is_drifted(self):
        desired = DesiredConfiguration(17137629, RulesetActor(4423678, "Integration", "pull_request"))
        raw = {"id": 17137629, "name": "main", "target": "branch", "enforcement": "active", "conditions": {}, "rules": [], "bypass_actors": []}
        self.assertEqual(ConfigState.DRIFTED, ConfigurationAdapter().observe(desired, raw).state)
        self.assertEqual(ConfigState.UNKNOWN, ConfigurationAdapter().observe(desired, None).state)

    def test_mirror_ahead_of_protected_ledger_is_conflicted(self):
        a = AuthoritativeFrontier("administrative_review", "2026-08-10T01:21:00Z", 3, "digest", "h")
        d = DerivedFrontier("2026-08-16T01:21:00Z")
        self.assertEqual(MirrorState.MIRROR_CONFLICTED, MirrorAdapter().classify(a, d).state)

    def test_canonical_environment_contract(self):
        observed = validate_runtime_environment(
            python_version=(3, 12),
            system_name="Linux",
            os_release={"ID": "ubuntu", "VERSION_ID": "24.04"},
        )
        self.assertEqual("3.12", observed["python"])
        with self.assertRaisesRegex(QualificationFailure, "ENVIRONMENT_PYTHON_MISMATCH"):
            validate_runtime_environment(
                python_version=(3, 13),
                system_name="Linux",
                os_release={"ID": "ubuntu", "VERSION_ID": "24.04"},
            )
        with self.assertRaisesRegex(QualificationFailure, "ENVIRONMENT_RUNNER_MISMATCH"):
            validate_runtime_environment(
                python_version=(3, 12),
                system_name="Linux",
                os_release={"ID": "ubuntu", "VERSION_ID": "22.04"},
            )

    def test_protected_head_movement_fails_closed(self):
        require_stable_protected_head("a" * 40, "a" * 40, "test")
        with self.assertRaisesRegex(QualificationFailure, "PROTECTED_MAIN_MOVED"):
            require_stable_protected_head("a" * 40, "b" * 40, "test")

    def test_snapshot_digest_supports_idempotent_second_pass(self):
        first = {"protected_head": "a" * 40, "value": [1, 2, 3]}
        second = {"value": [1, 2, 3], "protected_head": "a" * 40}
        self.assertEqual(_stable_snapshot_digest(first), _stable_snapshot_digest(second))
        second["value"] = [1, 2, 4]
        self.assertNotEqual(_stable_snapshot_digest(first), _stable_snapshot_digest(second))

    def test_suspension_filters_admin_review_before_execution(self):
        with tempfile.TemporaryDirectory() as td:
            old = os.environ.get("GCL_PROTECTED_RECEIPT_DIAGNOSTIC")
            os.environ["GCL_PROTECTED_RECEIPT_DIAGNOSTIC"] = str(Path(td) / "diag.json")
            try:
                closures = suspended_pending_closures(base=lambda: [{"manifest": {"procedure_id": ADMINISTRATIVE_REVIEW_PROCEDURE, "occurrence_key": "x"}}])
                candidates = suspended_eligible_candidates(base=lambda: [({"number": 1}, {"procedure_id": ADMINISTRATIVE_REVIEW_PROCEDURE, "occurrence_key": "y"})])
                self.assertEqual([], closures)
                self.assertEqual([], candidates)
                value = json.loads((Path(td) / "diag.json").read_text())
                self.assertFalse(value["authority_created"])
                self.assertEqual("ADMINISTRATIVE_REVIEW_RECEIPT_LANE_SUSPENDED", value["failure_code"])
            finally:
                if old is None:
                    os.environ.pop("GCL_PROTECTED_RECEIPT_DIAGNOSTIC", None)
                else:
                    os.environ["GCL_PROTECTED_RECEIPT_DIAGNOSTIC"] = old

    def test_stage_guard_fails_before_base_effect(self):
        called = []
        with tempfile.TemporaryDirectory() as td:
            old = os.environ.get("GCL_PROTECTED_RECEIPT_DIAGNOSTIC")
            os.environ["GCL_PROTECTED_RECEIPT_DIAGNOSTIC"] = str(Path(td) / "diag.json")
            try:
                with self.assertRaises(SuspendedReceiptLaneError):
                    suspended_stage_completion_receipt(
                        object(), object(), object(), "r", {}, "record",
                        ADMINISTRATIVE_REVIEW_PROCEDURE, "2026-01-01T00:00:00Z",
                        "record.json", {}, 1, "a" * 40, "b" * 40, "ref", "cand",
                        base=lambda *args: called.append(args),
                    )
                self.assertEqual([], called)
            finally:
                if old is None:
                    os.environ.pop("GCL_PROTECTED_RECEIPT_DIAGNOSTIC", None)
                else:
                    os.environ["GCL_PROTECTED_RECEIPT_DIAGNOSTIC"] = old

    def test_full_suspension_trace_exposes_no_effect_path(self):
        trace = suspension_guard_trace()
        self.assertTrue(trace)
        self.assertTrue(all(trace.values()))

    def test_generic_production_runtime_has_no_aug13_literal_dependencies(self):
        text = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(encoding="utf-8")
        for literal in ("#475", "#476", "#596", "2026-08-13", "import administrative_autonomy_runtime_administrative_review_0813_receipt_recovery"):
            self.assertNotIn(literal, text)

    def test_workflow_admin_token_preserves_protected_credential_contract(self):
        text = (ROOT / ".github" / "workflows" / "administrative-maintenance-candidate.yml").read_text(encoding="utf-8")
        self.assertIn("permission-administration: write", text)

    def test_qualification_workflow_is_delegated_remediation_then_read_only_qualification(self):
        text = (ROOT / ".github" / "workflows" / "administrative-protected-receipt-live-qualification.yml").read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("pull_request_target:", text)
        self.assertNotIn("\n  pull_request:\n", text)
        self.assertIn("types:\n      - closed", text)
        self.assertIn("Check out trusted protected implementation", text)
        self.assertIn("ref: refs/heads/main", text)
        self.assertIn("startsWith(github.event.pull_request.head.ref, 'remediation/mp-admin-')", text)
        for forbidden_trigger in ("schedule:", "push:", "workflow_run:", "repository_dispatch:"):
            self.assertNotIn(forbidden_trigger, text)
        self.assertIn("runs-on: ubuntu-24.04", text)
        self.assertIn("python-version: '3.12'", text)
        self.assertIn("python -m pip install --requirement requirements/policy.txt", text)
        self.assertIn("Mint bounded Candidate merge-executor token", text)
        self.assertEqual(1, text.count("permission-contents: write"))
        self.assertEqual(1, text.count("permission-pull-requests: write"))
        self.assertIn("permission-administration: write", text)
        self.assertIn("permission-administration: read", text)
        self.assertNotIn("permission-checks: write", text)
        self.assertNotIn("permission-issues: write", text)
        self.assertIn("administrative_remediation_envelope.py validate", text)
        self.assertIn("administrative_remediation_envelope.py admit-pull-request", text)
        self.assertIn("administrative_remediation_envelope.py reconcile-actor", text)
        self.assertIn("administrative_protected_receipt_live.py qualify", text)
        self.assertIn("--authorization-comment-id 5349149366", text)
        self.assertIn("Publish durable remediation result", text)
        self.assertNotIn("prepare_administrative_candidate", text)
        self.assertNotIn("administrative_autonomy_runtime.py execute", text)
        self.assertNotIn("update-branch", text)
        self.assertNotIn("merge_pull_request", text)
        self.assertNotIn("administrative_autonomy_0813_closure_preflight.py", text)
        self.assertLess(text.index("Referee exact-head admission and Candidate expected-head merge"), text.index("Reconcile exact PR-only Administration actor"))
        self.assertLess(text.index("Reconcile exact PR-only Administration actor"), text.index("Execute canonical read-only qualification"))
        self.assertLess(text.index("Execute canonical read-only qualification"), text.index("Publish durable remediation result"))
        self.assertLess(text.index("Publish durable remediation result"), text.index("Preserve remediation and qualification evidence"))

    def test_qualification_coordinator_declares_complete_non_authority_fields(self):
        text = (ROOT / "ci" / "administrative_protected_receipt_live.py").read_text(encoding="utf-8")
        for required in (
            "protected_head_start", "protected_head_end", "protected_integration_is_ancestor",
            "OBSERVATION_ONLY__NO_MUTATION", "authoritative_frontier", "mirror_results",
            "suspension_guard_trace", "idempotency", "LIVE_QUALIFICATION_GREEN__REACTIVATION_NOT_AUTHORIZED",
            "reactivation_authorized", "human_steward_identity_asserted", "ruleset_mutation_performed",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
