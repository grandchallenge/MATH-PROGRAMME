from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_0813_closure_preflight as preflight

CANDIDATE_WORKFLOW = (
    ROOT / ".github" / "workflows" / "administrative-maintenance-candidate.yml"
)
FAILOVER_WORKFLOW = (
    ROOT
    / ".github"
    / "workflows"
    / "administrative-maintenance-0813-recovery-failover.yml"
)
VALIDATION_WORKFLOW = (
    ROOT
    / ".github"
    / "workflows"
    / "administrative-maintenance-automation-validation.yml"
)
MANDATORY_BINDING = ROOT / "tests" / "test_administrative_autonomy_0813_executor_binding.py"


class AdministrativeAutonomy0813ClosurePreflightTests(unittest.TestCase):
    def target(self):
        return {
            "manifest": {
                "occurrence_key": preflight.TARGET["occurrence_key"],
                "procedure_id": preflight.TARGET["procedure_id"],
                "scheduled_due_at": preflight.TARGET["scheduled_due_at"],
                "branch": preflight.TARGET["candidate_branch"],
            },
            "record": {"record_id": preflight.TARGET["record_id"]},
            "record_id": preflight.TARGET["record_id"],
            "record_path": preflight.TARGET["record_path"],
            "issue_number": preflight.TARGET["issue_number"],
            "pull_request": preflight.TARGET["pull_request"],
            "exact_head": preflight.TARGET["exact_head"],
            "record_merge_commit": preflight.TARGET["record_merge_commit"],
            "record_disposition_comment_id": preflight.TARGET[
                "record_disposition_comment_id"
            ],
        }

    def env(self):
        return {
            "GITHUB_REPOSITORY": "grandchallenge/MATH-PROGRAMME",
            "GITHUB_REF": "refs/heads/main",
            "CANDIDATE_TOKEN": "candidate",
            "REFEREE_TOKEN": "referee",
            "ADMIN_TOKEN": "admin",
            "EVIDENCE_TOKEN": "evidence",
            "OBSERVABILITY_TOKEN": "observability",
        }

    def identities(self):
        return (
            SimpleNamespace(login="gcl-release-trust[bot]"),
            SimpleNamespace(login="gcl-release-trust[bot]"),
            SimpleNamespace(login="github-actions[bot]"),
        )

    def test_exact_target_predicate_rejects_any_identity_drift(self):
        item = self.target()
        self.assertTrue(preflight.is_exact_target(item))
        for field in ("issue_number", "pull_request", "record_disposition_comment_id"):
            mutated = self.target()
            mutated[field] = int(mutated[field]) + 1
            self.assertFalse(preflight.is_exact_target(mutated), field)
        for field in ("record_id", "record_path", "exact_head", "record_merge_commit"):
            mutated = self.target()
            mutated[field] = "drift"
            self.assertFalse(preflight.is_exact_target(mutated), field)
        for field in ("occurrence_key", "procedure_id", "scheduled_due_at", "branch"):
            mutated = self.target()
            mutated["manifest"][field] = "drift"
            self.assertFalse(preflight.is_exact_target(mutated), field)

    def test_review_field_diagnostic_reports_only_exact_review_fields(self):
        candidate = Mock()
        candidate.get.return_value = [
            {
                "id": preflight.TARGET["independent_review"],
                "state": "APPROVED",
                "commit_id": preflight.TARGET["exact_head"],
                "user": {"login": "jimsteeg"},
                "author_association": "COLLABORATOR",
            }
        ]
        error = "Aug13 administrative independent review drift"
        detail = preflight.review_field_diagnostic(
            candidate, "grandchallenge/MATH-PROGRAMME", error
        )
        self.assertIn("state='APPROVED'", detail)
        self.assertIn(f"commit_id='{preflight.TARGET['exact_head']}'", detail)
        self.assertIn("login='jimsteeg'", detail)
        self.assertIn("author_association='COLLABORATOR'", detail)
        candidate.get.assert_called_once_with(
            "/repos/grandchallenge/MATH-PROGRAMME/pulls/476/reviews?per_page=100"
        )

    def test_review_field_diagnostic_is_inert_for_other_failures(self):
        candidate = Mock()
        self.assertEqual(
            preflight.review_field_diagnostic(candidate, "repo", "classifier boom"),
            "classifier boom",
        )
        candidate.get.assert_not_called()

    def test_steward_field_diagnostic_reports_only_exact_predicate_fields(self):
        candidate = Mock()
        body = "\n".join(
            (
                "AUTHORIZE_EXACT_HEAD_PROTECTED_MERGE__NO_OTHER_AUTHORITY",
                preflight.TARGET["occurrence_key"],
                f"PR: #{preflight.TARGET['pull_request']}",
                preflight.TARGET["exact_head"],
                "cd0d91b4c1b9e3c3ff2eced0c79c104d97af66e2",
                str(preflight.TARGET["independent_review"]),
            )
        )
        candidate.get.return_value = [
            {
                "id": preflight.TARGET["record_disposition_comment_id"],
                "user": {"login": "fyremael"},
                "author_association": "CONTRIBUTOR",
                "body": body,
            }
        ]
        error = "Aug13 administrative Human Steward disposition drift"
        detail = preflight.steward_field_diagnostic(
            candidate, "grandchallenge/MATH-PROGRAMME", error
        )
        self.assertIn("login='fyremael'", detail)
        self.assertIn("author_association='CONTRIBUTOR'", detail)
        for marker in (
            "authorize_marker=True",
            "occurrence_marker=True",
            "pr_marker=True",
            "head_marker=True",
            "base_marker=True",
            "review_marker=True",
        ):
            self.assertIn(marker, detail)
        candidate.get.assert_called_once_with(
            "/repos/grandchallenge/MATH-PROGRAMME/issues/475/comments?per_page=100"
        )

    def test_steward_field_diagnostic_is_inert_for_other_failures(self):
        candidate = Mock()
        self.assertEqual(
            preflight.steward_field_diagnostic(candidate, "repo", "classifier boom"),
            "classifier boom",
        )
        candidate.get.assert_not_called()

    def test_no_target_is_noop_and_never_finishes_other_closure(self):
        other = self.target()
        other["issue_number"] = 999
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            with (
                patch.dict(os.environ, self.env(), clear=False),
                patch.object(preflight, "runtime_identities", return_value=self.identities()),
                patch.object(preflight, "Client", return_value=Mock()),
                patch.object(preflight.runtime_execute, "pending_closures", return_value=[other]),
                patch.object(preflight, "ruleset_actors") as actors,
                patch.object(preflight, "finish_closure") as finish,
            ):
                self.assertEqual(preflight.recover_exact_aug13(report), 0)
            value = json.loads(report.read_text(encoding="utf-8"))
        self.assertEqual(value["state"], "AUG13_CLOSURE_PREFLIGHT_NO_TARGET")
        self.assertFalse(value["recovered"])
        self.assertFalse(value["authority_created"])
        actors.assert_not_called()
        finish.assert_not_called()

    def test_classifier_failure_is_reported_on_bound_target_issue(self):
        candidate = Mock()
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            with (
                patch.dict(os.environ, self.env(), clear=False),
                patch.object(preflight, "runtime_identities", return_value=self.identities()),
                patch.object(preflight, "Client", return_value=candidate),
                patch.object(
                    preflight.runtime_execute,
                    "pending_closures",
                    side_effect=preflight.AutonomyError("classifier boom"),
                ),
                patch.object(preflight, "ruleset_actors") as actors,
                patch.object(preflight, "finish_closure") as finish,
            ):
                with self.assertRaises(preflight.AutonomyError):
                    preflight.recover_exact_aug13(report)
            value = json.loads(report.read_text(encoding="utf-8"))
        self.assertEqual(value["state"], "AUG13_CLOSURE_PREFLIGHT_FAILED_CLOSED")
        self.assertEqual(value["error"], "classifier boom")
        self.assertFalse(value["recovered"])
        self.assertFalse(value["authority_created"])
        candidate.post.assert_called_once()
        path, payload = candidate.post.call_args.args
        self.assertEqual(path, "/repos/grandchallenge/MATH-PROGRAMME/issues/475/comments")
        self.assertIn("AUG13_CLOSURE_PREFLIGHT_FAILED_CLOSED", payload["body"])
        self.assertIn("classifier boom", payload["body"])
        actors.assert_not_called()
        finish.assert_not_called()

    def test_exact_target_uses_existing_finish_closure_once(self):
        target = self.target()
        closure = {
            "receipt": {"scheduled_due_at": preflight.TARGET["scheduled_due_at"]},
            "receipt_pull_request": 563,
            "receipt_head": "a" * 40,
            "receipt_disposition_comment_id": 123,
            "receipt_merge_commit": "b" * 40,
            "protected_readback_comment_id": 456,
            "mirror_synchronization_run": 789,
            "ruleset_bypass_actors": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "report.json"
            with (
                patch.dict(os.environ, self.env(), clear=False),
                patch.object(preflight, "runtime_identities", return_value=self.identities()),
                patch.object(preflight, "Client", return_value=Mock()),
                patch.object(preflight.runtime_execute, "pending_closures", return_value=[target]),
                patch.object(preflight, "ruleset_actors", return_value=[]) as actors,
                patch.object(preflight, "finish_closure", return_value=closure) as finish,
            ):
                self.assertEqual(preflight.recover_exact_aug13(report), 0)
            value = json.loads(report.read_text(encoding="utf-8"))
        self.assertEqual(value["state"], "AUG13_CLOSURE_PREFLIGHT_PROTECTED_COMPLETE")
        self.assertTrue(value["recovered"])
        self.assertTrue(value["authority_created"])
        self.assertFalse(value["human_steward_identity_asserted"])
        self.assertFalse(value["bypass_used"])
        actors.assert_called_once()
        finish.assert_called_once()

    def test_runtime_overlay_is_installed_before_executor_import(self):
        text = (
            ROOT / "ci" / "administrative_autonomy_0813_closure_preflight.py"
        ).read_text(encoding="utf-8")
        runtime_import = text.index("import administrative_autonomy_runtime  # noqa: F401")
        executor_import = text.index(
            "import administrative_autonomy_runtime_execute as runtime_execute"
        )
        self.assertLess(runtime_import, executor_import)

    def test_candidate_workflow_runs_exact_preflight_before_full_runtime(self):
        text = CANDIDATE_WORKFLOW.read_text(encoding="utf-8")
        preparation = text.index("Prepare idempotent non-authoritative candidates")
        preflight_index = text.index(
            "python ci/administrative_autonomy_0813_closure_preflight.py"
        )
        execute_index = text.index(
            "python ci/administrative_autonomy_runtime.py execute --report"
        )
        self.assertLess(preparation, preflight_index)
        self.assertLess(preflight_index, execute_index)
        self.assertEqual(text.count("${{ github.token }}"), 1)
        self.assertIn('if [[ "$recovered" == "true" ]]; then', text)
        self.assertIn("administrative-autonomy-0813-closure-preflight.json", text)

    def test_merged_control_pr_failover_runs_exact_preflight_only(self):
        text = FAILOVER_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("types:\n      - closed", text)
        self.assertIn("github.event.pull_request.merged == true", text)
        self.assertIn(
            "startsWith(github.event.pull_request.head.ref, 'control/mp-admin-0813-')",
            text,
        )
        self.assertIn("environment: release-trust", text)
        self.assertIn("ref: refs/heads/main", text)
        self.assertIn(
            "python ci/administrative_autonomy_0813_closure_preflight.py", text
        )
        self.assertIn("--apply", text)
        self.assertIn("administrative-autonomy-0813-pr-close-recovery.json", text)
        self.assertEqual(text.count("${{ github.token }}"), 1)
        self.assertNotIn("administrative_autonomy_runtime.py execute", text)
        self.assertNotIn("administrative_maintenance_completion_state.json", text)
        self.assertNotIn("workflow_dispatch:", text)
        self.assertNotIn("schedule:", text)
        self.assertNotIn("push:", text)

    def test_existing_validation_lane_mandatorily_reaches_preflight_regression(self):
        workflow = VALIDATION_WORKFLOW.read_text(encoding="utf-8")
        binding = MANDATORY_BINDING.read_text(encoding="utf-8")
        self.assertIn("tests.test_administrative_autonomy_0813_executor_binding", workflow)
        self.assertIn("AdministrativeAutonomy0813ClosurePreflightTests", binding)


if __name__ == "__main__":
    unittest.main()
