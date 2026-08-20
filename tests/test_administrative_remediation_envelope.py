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


class FakeActorClient:
    def __init__(self, ruleset):
        self.ruleset = copy.deepcopy(ruleset)

    def get(self, path):
        if path != "/repos/grandchallenge/MATH-PROGRAMME/rulesets/17137629":
            raise AssertionError(path)
        return copy.deepcopy(self.ruleset)


class FakeRefereeClient:
    def __init__(self, head: str):
        self.head = head

    def get(self, path):
        if path == "/repos/grandchallenge/MATH-PROGRAMME/issues/comments/5349149366":
            return {
                "id": 5349149366,
                "user": {"login": "fyremael"},
                "body": (
                    "HUMAN STEWARD INITIAL APPROVAL — DELEGATED REMEDIATION ENVELOPE\n\n"
                    "Final administrative-review reactivation/incident closure remains reserved to the Human Steward."
                ),
            }
        if path == "/repos/grandchallenge/MATH-PROGRAMME/pulls/616":
            return {
                "number": 616,
                "node_id": "PR_node",
                "state": "open",
                "draft": False,
                "base": {"ref": "main"},
                "head": {
                    "sha": self.head,
                    "ref": "remediation/mp-admin-remediation-envelope-001",
                },
            }
        if path == "/repos/grandchallenge/MATH-PROGRAMME/pulls/616/files?per_page=100":
            return [
                {"filename": ".github/workflows/administrative-protected-receipt-live-qualification.yml"},
                {"filename": "ci/administrative_remediation_envelope.py"},
                {"filename": "governance/administrative_remediation_envelope.json"},
                {"filename": "tests/test_administrative_remediation_envelope.py"},
                {"filename": "ci/validate_workflow_coverage_v2.py"},
                {"filename": "ci/test_workflow_coverage_v2.py"},
            ]
        raise AssertionError(path)


class FakeAdminReadClient:
    def get(self, path):
        if path != "/repos/grandchallenge/MATH-PROGRAMME/rulesets/17137629":
            raise AssertionError(path)
        return {
            "id": 17137629,
            "rules": [
                {
                    "type": "required_status_checks",
                    "parameters": {
                        "required_status_checks": [
                            {"context": "Programme policy checks"},
                            {"context": "GCL conformance"},
                        ]
                    },
                }
            ],
        }


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
        review = value["delegated_review"]
        self.assertEqual("github-actions[bot]", review["referee_login"])
        self.assertFalse(review["github_review_submission_required"])
        self.assertTrue(review["expected_head_auto_merge_required"])

    def test_path_scope_excludes_receipt_and_allows_control_plane(self):
        value = remediation.load_envelope()
        self.assertTrue(
            remediation.path_allowed(
                "ci/administrative_remediation_envelope.py", value
            )
        )
        self.assertTrue(
            remediation.path_allowed("ci/validate_workflow_coverage_v2.py", value)
        )
        self.assertFalse(
            remediation.path_allowed(
                "governance/administrative_maintenance_completion_state.json", value
            )
        )

    def test_referee_admission_binds_live_approval_checks_and_expected_head_auto_merge(self):
        head = "1" * 40
        referee = FakeRefereeClient(head)
        admin = FakeAdminReadClient()
        merged = {
            "merged": True,
            "merge_commit_sha": "2" * 40,
            "head": {"sha": head},
        }
        with tempfile.TemporaryDirectory() as td, mock.patch.object(
            remediation, "Client", side_effect=[referee, admin]
        ), mock.patch.object(
            remediation,
            "wait_checks",
            return_value={"Programme policy checks": "success", "GCL conformance": "success"},
        ) as wait_checks, mock.patch.object(
            remediation, "record_disposition", return_value={"id": 9001}
        ) as disposition, mock.patch.object(
            remediation, "auto_merge"
        ) as auto_merge, mock.patch.object(
            remediation, "wait_merge", return_value=merged
        ) as wait_merge:
            path = Path(td) / "admission.json"
            report = remediation.admit_pull_request(
                "referee-token", "admin-token", 616, head, path
            )
            self.assertEqual("REMEDIATION_PR_PROTECTED_MERGE_COMPLETE", report["state"])
            self.assertEqual(head, report["exact_head"])
            self.assertEqual(9001, report["referee_disposition_comment_id"])
            self.assertFalse(report["github_review_submission_required"])
            self.assertFalse(report["direct_protected_push"])
            self.assertFalse(report["bypass_exercised"])
            self.assertFalse(report["receipt_mutation_performed"])
            wait_checks.assert_called_once()
            disposition.assert_called_once()
            auto_merge.assert_called_once()
            wait_merge.assert_called_once()
            persisted = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(report["merge_commit_sha"], persisted["merge_commit_sha"])

    def test_actor_reconciliation_changes_only_exact_actor(self):
        client = FakeActorClient(self.base_ruleset())

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
        client = FakeActorClient(ruleset)
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
            "pull_request_target:",
            "types:\n      - closed",
            "      - ready_for_review",
            "github.event_name == 'pull_request_target'",
            "github.event.action != 'closed'",
            "github.event.pull_request.draft == false",
            "startsWith(github.event.pull_request.head.ref, 'remediation/mp-admin-')",
            "checks: read",
            "issues: write",
            "pull-requests: write",
            "REFEREE_TOKEN: ${{ github.token }}",
            "Check out trusted protected implementation",
            "ref: refs/heads/main",
            "administrative_remediation_envelope.py admit-pull-request",
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
            "gh pr merge",
            "administrative_autonomy_0813_closure_preflight.py",
            "administrative_maintenance_completion_state.json",
            "receipt-administrative_review",
            "reactivation_authorized: true",
        ):
            self.assertNotIn(forbidden, text)
        self.assertLess(
            text.index("administrative_remediation_envelope.py admit-pull-request"),
            text.index("administrative_remediation_envelope.py reconcile-actor"),
        )
        self.assertLess(
            text.index("administrative_remediation_envelope.py reconcile-actor"),
            text.index("administrative_protected_receipt_live.py qualify"),
        )


if __name__ == "__main__":
    unittest.main()
