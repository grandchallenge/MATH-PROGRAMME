from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_remediation_envelope as remediation


class FakeClient:
    def __init__(self, ruleset):
        self.ruleset = copy.deepcopy(ruleset)

    def get(self, path):
        if path != "/repos/grandchallenge/MATH-PROGRAMME/rulesets/17137629":
            raise AssertionError(path)
        return copy.deepcopy(self.ruleset)


class RemediationEnvelopeTests(unittest.TestCase):
    def base_ruleset(self):
        return {
            "name": "main",
            "target": "branch",
            "enforcement": "active",
            "conditions": {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
            "rules": [{"type": "pull_request"}],
            "bypass_actors": [
                {"actor_id": 123, "actor_type": "Team", "bypass_mode": "pull_request"}
            ],
        }

    def test_envelope_uses_initial_and_final_human_steward_only(self):
        value = remediation.load_envelope()
        self.assertEqual("OPEN", value["state"])
        steward = value["human_steward"]
        self.assertEqual(5349149366, steward["initial_approval_comment_id"])
        self.assertFalse(steward["intermediate_approval_required"])
        self.assertTrue(steward["final_closure_or_reactivation_approval_required"])
        self.assertTrue(value["delegated_authority"]["repeat_until_green_or_scope_expansion"])

    def test_actor_reconciliation_changes_only_exact_actor(self):
        client = FakeClient(self.base_ruleset())

        def install(fake_client, repository, ruleset_id, administrator):
            self.assertIs(fake_client, client)
            self.assertEqual("grandchallenge/MATH-PROGRAMME", repository)
            self.assertEqual(17137629, ruleset_id)
            self.assertEqual(4423678, administrator.app_id)
            before = copy.deepcopy(client.ruleset)
            after = copy.deepcopy(before)
            after["bypass_actors"].append(
                {"actor_id": 4423678, "actor_type": "Integration", "bypass_mode": "pull_request"}
            )
            client.ruleset = copy.deepcopy(after)
            return before, after

        with tempfile.TemporaryDirectory() as td, mock.patch.object(
            remediation, "Client", return_value=client
        ), mock.patch.object(remediation, "install_bypass", side_effect=install):
            path = Path(td) / "report.json"
            report = remediation.reconcile_actor("token", path)
            self.assertTrue(report["mutation_performed"])
            self.assertTrue(report["actor_present_after"])
            self.assertTrue(report["existing_bypass_actors_preserved"])
            self.assertTrue(report["non_actor_fields_preserved"])
            self.assertFalse(report["direct_protected_push"])
            self.assertFalse(report["bypass_exercised"])
            self.assertFalse(report["receipt_mutation_performed"])
            persisted = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(report["terminal_state"], persisted["terminal_state"])
            self.assertEqual(report["after_ruleset_digest"], persisted["after_ruleset_digest"])

    def test_actor_already_present_is_noop(self):
        ruleset = self.base_ruleset()
        ruleset["bypass_actors"].append(
            {"actor_id": 4423678, "actor_type": "Integration", "bypass_mode": "pull_request"}
        )
        client = FakeClient(ruleset)
        with tempfile.TemporaryDirectory() as td, mock.patch.object(
            remediation, "Client", return_value=client
        ), mock.patch.object(remediation, "install_bypass") as install:
            report = remediation.reconcile_actor("token", Path(td) / "report.json")
            self.assertFalse(report["mutation_performed"])
            self.assertEqual("RULESET_ACTOR_ALREADY_PRESENT__NO_MUTATION", report["terminal_state"])
            install.assert_not_called()

    def test_workflow_is_audited_bounded_resume_loop(self):
        text = (
            ROOT / ".github/workflows/administrative-protected-receipt-live-qualification.yml"
        ).read_text(encoding="utf-8")
        for required in (
            "workflow_dispatch:",
            "pull_request:",
            "types:\n      - closed",
            "startsWith(github.event.pull_request.head.ref, 'remediation/mp-admin-')",
            "environment: release-trust",
            "runs-on: ubuntu-24.04",
            "python-version: '3.12'",
            "permission-administration: write",
            "permission-administration: read",
            "permission-contents: read",
            "permission-pull-requests: read",
            "Reconcile exact PR-only Administration actor",
            "administrative_remediation_envelope.py reconcile-actor",
            "administrative_protected_receipt_live.py qualify",
            "--control-id MP-ADMIN-REMEDIATION-ENVELOPE-001",
            "--control-issue 615",
            "--authorization-comment-id 5349149366",
            "retention-days: 90",
        ):
            self.assertIn(required, text)
        for forbidden in (
            "permission-contents: write",
            "permission-issues: write",
            "permission-pull-requests: write",
            "git push origin main",
            "administrative_autonomy_0813_closure_preflight.py",
            "administrative_maintenance_completion_state.json",
            "receipt-administrative_review",
            "reactivation_authorized: true",
        ):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
