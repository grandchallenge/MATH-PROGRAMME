from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_runtime_post_receipt_closure_resume as recovery
from autonomy_github import AutonomyError

CONTROL = (
    ROOT
    / "governance"
    / "administrative_post_receipt_closure_resume_control.json"
)
SCHEMA = (
    ROOT
    / "schemas"
    / "administrative_post_receipt_closure_resume_control.schema.json"
)
RUNTIME_ENTRY = ROOT / "ci" / "administrative_autonomy_runtime.py"


class AdministrativePostReceiptClosureResumeTests(unittest.TestCase):
    def control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def receipt(self):
        target = self.control()["target"]
        return {
            "procedure_id": target["procedure_id"],
            "scheduled_due_at": target["scheduled_due_at"],
            "record_path": target["record_path"],
            "record_sha256": "0" * 64,
            "merge_commit": target["record_merge_commit"],
            "reviewed_head": target["reviewed_head"],
            "pull_request": target["candidate_pull_request"],
            "disposition": "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            "receipt_state": "PROTECTED_COMPLETE",
        }

    def ledger(self):
        target = self.control()["target"]
        receipt = self.receipt()
        return {
            "schema_version": "1.0.0",
            "control_id": "MP-ADMIN-MAINT-001",
            "derived_from_protected_head": target["record_merge_commit"],
            "state": "PROTECTED_RECEIPT_DERIVED",
            "procedures": {
                "structural_sweep": {
                    "completed_through_utc": target[
                        "preserved_completed_through_utc"
                    ],
                    "receipt_count": 1,
                    "receipts": [receipt],
                }
            },
            "authority_boundary": {
                "issues_are_authority": False,
                "workflow_artifacts_are_authority": False,
                "draft_pull_requests_are_authority": False,
                "unmerged_branches_are_authority": False,
                "protected_merge_receipts_required": True,
            },
        }

    def closure(self):
        target = self.control()["target"]
        return {
            "manifest": {
                "occurrence_key": target["occurrence_key"],
                "procedure_id": target["procedure_id"],
                "scheduled_due_at": target["scheduled_due_at"],
                "issue_number": target["candidate_issue"],
                "pull_request_number": target["candidate_pull_request"],
                "branch": target["candidate_branch"],
            },
            "record": {"record_id": target["record_id"]},
            "record_id": target["record_id"],
            "record_path": target["record_path"],
            "issue_number": target["candidate_issue"],
            "pull_request": target["candidate_pull_request"],
            "exact_head": target["reviewed_head"],
            "record_merge_commit": target["record_merge_commit"],
            "record_disposition_comment_id": 123,
            "receipt_present": True,
            "receipt": self.receipt(),
        }

    def runtime(self):
        return {
            "merge_control": {
                "maximum_protected_readback_wait_seconds": 1,
                "poll_interval_seconds": 0,
            },
            "mirrors": [
                {"repository": "grandchallenge/MATH-PROGRAMME", "issue": 182},
                {"repository": "grandchallenge/MATH-PROGRAMME", "issue": 183},
                {"repository": "grandchallenge/INTELLECT", "issue": 21},
            ],
        }

    def test_schema_and_authority_boundary(self):
        control = self.control()
        jsonschema.validate(
            control, json.loads(SCHEMA.read_text(encoding="utf-8"))
        )
        self.assertEqual(control["issue"], 541)
        self.assertEqual(control["target"]["candidate_issue"], 515)
        self.assertEqual(control["target"]["candidate_pull_request"], 516)
        self.assertEqual(control["target"]["receipt_pull_request"], 540)
        self.assertTrue(control["authority_boundary"]["control_plane_change"])
        self.assertTrue(
            control["authority_boundary"][
                "human_steward_exact_head_authorization_required"
            ]
        )
        self.assertFalse(
            control["authority_boundary"]["general_descendant_head_authority_created"]
        )
        self.assertFalse(control["authority_boundary"]["candidate_520_authorized"])
        self.assertTrue(all(value is False for value in control["claim_boundaries"].values()))

    def test_ordinary_receipt_missing_closure_has_precedence(self):
        sentinel = {"ordinary": True}
        result = recovery.pending_closures(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            {},
            "github-actions[bot]",
            base=lambda candidate, repo, runtime, referee: [sentinel],
            all_base=lambda candidate, repo, runtime, referee: self.fail(
                "receipt-complete scan must not run while ordinary closure blocks"
            ),
        )
        self.assertEqual(result, [sentinel])

    def test_exact_receipt_complete_target_is_readmitted(self):
        item = self.closure()
        with patch.object(recovery, "json_content", return_value=self.ledger()), patch.object(
            recovery, "_require_receipt_introduction"
        ) as introduction:
            result = recovery.pending_closures(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                {},
                "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: [],
                all_base=lambda candidate, repo, runtime, referee: [item],
            )
        self.assertEqual(result, [item])
        introduction.assert_called_once()

    def test_non_target_and_duplicate_target_fail_closed(self):
        non_target = copy.deepcopy(self.closure())
        non_target["issue_number"] = 520
        result = recovery.pending_closures(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            {},
            "github-actions[bot]",
            base=lambda candidate, repo, runtime, referee: [],
            all_base=lambda candidate, repo, runtime, referee: [non_target],
        )
        self.assertEqual(result, [])

        item = self.closure()
        with self.assertRaisesRegex(AutonomyError, "duplicate exact"):
            recovery.pending_closures(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                {},
                "github-actions[bot]",
                base=lambda candidate, repo, runtime, referee: [],
                all_base=lambda candidate, repo, runtime, referee: [item, item],
            )

    def test_target_stage_reuses_exact_protected_receipt_without_delegate(self):
        target = self.control()["target"]
        delegate = Mock(side_effect=AssertionError("delegate must not run for target"))
        with patch.object(recovery, "json_content", return_value=self.ledger()), patch.object(
            recovery, "_require_receipt_introduction"
        ):
            result = recovery.stage_completion_receipt(
                object(),
                object(),
                object(),
                "grandchallenge/MATH-PROGRAMME",
                {},
                target["record_id"],
                target["procedure_id"],
                target["scheduled_due_at"],
                target["record_path"],
                {"record_id": target["record_id"]},
                target["candidate_pull_request"],
                target["reviewed_head"],
                target["record_merge_commit"],
                "github-actions[bot]",
                "gcl-release-trust[bot]",
                base=delegate,
            )
        self.assertEqual(result["receipt_pull_request"], 540)
        self.assertEqual(result["receipt_head"], target["receipt_head"])
        self.assertEqual(
            result["receipt_merge_commit"], target["receipt_introduction_commit"]
        )
        self.assertTrue(result["receipt_recovered"])
        delegate.assert_not_called()

    def test_non_target_stage_delegates(self):
        sentinel = {"delegated": True}
        delegate = Mock(return_value=sentinel)
        result = recovery.stage_completion_receipt(
            object(), object(), object(), "grandchallenge/MATH-PROGRAMME", {},
            "OTHER", "structural_sweep", "2026-08-17T03:45:00Z", "other.json",
            {}, 999, "f" * 40, "e" * 40, "github-actions[bot]",
            "gcl-release-trust[bot]", base=delegate,
        )
        self.assertIs(result, sentinel)
        delegate.assert_called_once()

    def test_frontier_and_same_due_receipt_drift_fail_closed(self):
        ledger = self.ledger()
        ledger["procedures"]["structural_sweep"]["completed_through_utc"] = (
            "2026-08-15T01:21:00Z"
        )
        with self.assertRaisesRegex(AutonomyError, "frontier drift"):
            recovery._require_target_receipt_in_completion(ledger, self.control())

        ledger = self.ledger()
        conflict = copy.deepcopy(self.receipt())
        conflict["record_path"] = "conflict.json"
        ledger["procedures"]["structural_sweep"]["receipts"].append(conflict)
        ledger["procedures"]["structural_sweep"]["receipt_count"] = 2
        with self.assertRaisesRegex(AutonomyError, "absent, conflicting, or ambiguous"):
            recovery._require_target_receipt_in_completion(ledger, self.control())

    def test_descendant_synchronized_mirror_head_closes_target(self):
        target = self.control()["target"]
        descendant = "d" * 40
        with patch.object(recovery, "json_content", return_value=self.ledger()), patch.object(
            recovery, "_current_main", return_value=descendant
        ), patch.object(recovery, "_is_ancestor", return_value=True), patch.object(
            recovery, "_successful_sync_run", return_value=77
        ), patch.object(recovery, "_mirrors_current", return_value=True), patch.object(
            recovery.time, "sleep", return_value=None
        ):
            run = recovery.wait_mirror_sync(
                object(),
                object(),
                "grandchallenge/MATH-PROGRAMME",
                target["receipt_introduction_commit"],
                target["procedure_id"],
                target["scheduled_due_at"],
                self.runtime(),
            )
        self.assertEqual(run, 77)

    def test_stale_or_unsynchronized_mirrors_do_not_close_target(self):
        target = self.control()["target"]
        with patch.object(recovery, "json_content", return_value=self.ledger()), patch.object(
            recovery, "_current_main", return_value="d" * 40
        ), patch.object(recovery, "_is_ancestor", return_value=True), patch.object(
            recovery, "_successful_sync_run", return_value=77
        ), patch.object(recovery, "_mirrors_current", return_value=False), patch.object(
            recovery.time, "sleep", return_value=None
        ), patch.object(recovery.time, "monotonic", side_effect=[0.0, 0.0, 2.0]):
            with self.assertRaisesRegex(AutonomyError, "descendant protected mirror"):
                recovery.wait_mirror_sync(
                    object(),
                    object(),
                    "grandchallenge/MATH-PROGRAMME",
                    target["receipt_introduction_commit"],
                    target["procedure_id"],
                    target["scheduled_due_at"],
                    self.runtime(),
                )

    def test_runtime_wiring_is_after_compatibility_and_before_executor(self):
        text = RUNTIME_ENTRY.read_text(encoding="utf-8")
        compatibility = (
            "runtime_github.wait_mirror_sync = structural_0121_hole_wait_mirror_sync"
        )
        pending_overlay = (
            "receipt_stage.pending_closures = resumable_post_receipt_pending_closures"
        )
        receipt_overlay = (
            "receipt_stage.stage_completion_receipt = "
            "stable_post_receipt_stage_completion_receipt"
        )
        mirror_overlay = (
            "runtime_github.wait_mirror_sync = descendant_post_receipt_wait_mirror_sync"
        )
        executor = "from administrative_autonomy_runtime_behind_sync import"
        for line in (compatibility, pending_overlay, receipt_overlay, mirror_overlay, executor):
            self.assertIn(line, text)
        self.assertLess(text.index(compatibility), text.index(pending_overlay))
        self.assertLess(text.index(pending_overlay), text.index(executor))
        self.assertLess(text.index(receipt_overlay), text.index(executor))
        self.assertLess(text.index(mirror_overlay), text.index(executor))


if __name__ == "__main__":
    unittest.main()
