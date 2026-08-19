from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from administrative_protected_receipt_adapters import ConfigurationAdapter, DesiredConfiguration, RulesetActor
from administrative_protected_receipt_engine import AuthoritativeFrontier, DerivedFrontier, MirrorAdapter
from administrative_protected_receipt_live import (
    ADMINISTRATIVE_REVIEW_PROCEDURE,
    LiveClientProvider,
    SuspendedReceiptLaneError,
    classify_receipt_pull_for_sync,
    read_only_configuration_preflight,
    runtime_capability_sets,
    suspended_eligible_candidates,
    suspended_pending_closures,
    suspended_stage_completion_receipt,
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

    def test_true_content_conflict_is_typed_conflict(self):
        client = FakeClient(); client.mergeable = False
        facts = classify_receipt_pull_for_sync(client, "grandchallenge/MATH-PROGRAMME", 10, client.declared, update_control_permitted=True)
        self.assertEqual(ConflictState.CONFLICTED, facts.conflict_state)

    def test_unknown_ancestry_fails_closed_as_unknown(self):
        client = FakeClient(); client.declared = "c" * 40
        facts = classify_receipt_pull_for_sync(client, "grandchallenge/MATH-PROGRAMME", 10, client.declared, update_control_permitted=True)
        self.assertEqual(BranchState.UNKNOWN, facts.branch_state)

    def test_live_provider_is_read_only(self):
        client = FakeClient()
        provider = LiveClientProvider(client)
        with self.assertRaises(Exception):
            provider.update_branch("grandchallenge/MATH-PROGRAMME", 10, client.head)
        self.assertEqual([], client.puts)

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

    def test_generic_production_runtime_has_no_aug13_literal_dependencies(self):
        text = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(encoding="utf-8")
        for literal in ("#475", "#476", "#596", "2026-08-13", "import administrative_autonomy_runtime_administrative_review_0813_receipt_recovery"):
            self.assertNotIn(literal, text)

    def test_workflow_admin_token_preserves_protected_credential_contract(self):
        text = (ROOT / ".github" / "workflows" / "administrative-maintenance-candidate.yml").read_text(encoding="utf-8")
        self.assertIn("permission-administration: write", text)


if __name__ == "__main__":
    unittest.main()
