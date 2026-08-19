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

import administrative_autonomy_runtime_post_receipt_current_frontier as recovery
from autonomy_github import AutonomyError

CONTROL = ROOT / "governance" / "administrative_post_receipt_current_frontier_control.json"
SCHEMA = ROOT / "schemas" / "administrative_post_receipt_current_frontier_control.schema.json"
RUNTIME_ENTRY = ROOT / "ci" / "administrative_autonomy_runtime.py"


class AdministrativePostReceiptCurrentFrontierTests(unittest.TestCase):
    def control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def predecessor_control(self):
        return recovery.predecessor.load_control()

    def target_receipt(self):
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

    def latest_receipt(self, due="2026-08-17T03:45:00Z", merge="f" * 40):
        return {
            "procedure_id": "structural_sweep",
            "scheduled_due_at": due,
            "record_path": "governance/administrative_structural_sweeps/LATEST.json",
            "record_sha256": "1" * 64,
            "merge_commit": merge,
            "reviewed_head": "e" * 40,
            "pull_request": 999,
            "disposition": "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            "receipt_state": "PROTECTED_COMPLETE",
        }

    def ledger(self, due="2026-08-17T03:45:00Z", merge="f" * 40):
        receipts = [self.target_receipt(), self.latest_receipt(due, merge)]
        return {
            "schema_version": "1.0.0",
            "control_id": "MP-ADMIN-MAINT-001",
            "derived_from_protected_head": merge,
            "state": "PROTECTED_RECEIPT_DERIVED",
            "procedures": {
                "structural_sweep": {
                    "completed_through_utc": due,
                    "receipt_count": 2,
                    "receipts": receipts,
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
            "receipt": self.target_receipt(),
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

    def test_schema_and_scope(self):
        control = self.control()
        jsonschema.validate(control, json.loads(SCHEMA.read_text(encoding="utf-8")))
        self.assertEqual(control["issue"], 544)
        self.assertEqual(control["target"]["candidate_issue"], 515)
        self.assertTrue(control["predecessor_control"]["mutation_prohibited"])
        self.assertFalse(control["authority_boundary"]["candidate_520_authorized"])
        self.assertFalse(control["authority_boundary"]["candidate_522_authorized"])
        self.assertTrue(all(value is False for value in control["claim_boundaries"].values()))

    def test_validated_current_frontier_accepts_protected_advance(self):
        frontier, receipt = recovery._validated_current_frontier(
            self.ledger(), self.control(), self.predecessor_control()
        )
        self.assertEqual(frontier, "2026-08-17T03:45:00Z")
        self.assertEqual(receipt["scheduled_due_at"], "2026-08-15T01:21:00Z")

    def test_validated_current_frontier_accepts_later_protected_advance(self):
        frontier, _ = recovery._validated_current_frontier(
            self.ledger("2026-08-17T20:33:00Z", "d" * 40),
            self.control(),
            self.predecessor_control(),
        )
        self.assertEqual(frontier, "2026-08-17T20:33:00Z")

    def test_frontier_regression_and_derivation_mismatch_fail_closed(self):
        ledger = self.ledger("2026-08-16T10:57:00Z", "f" * 40)
        with self.assertRaisesRegex(AutonomyError, "regressed below protected discovery"):
            recovery._validated_current_frontier(
                ledger, self.control(), self.predecessor_control()
            )

        ledger = self.ledger()
        ledger["derived_from_protected_head"] = "a" * 40
        with self.assertRaisesRegex(AutonomyError, "derivation head"):
            recovery._validated_current_frontier(
                ledger, self.control(), self.predecessor_control()
            )

    def test_duplicate_exact_historical_receipt_fails_closed(self):
        ledger = self.ledger()
        conflict = copy.deepcopy(self.target_receipt())
        conflict["record_path"] = "conflict.json"
        ledger["procedures"]["structural_sweep"]["receipts"].insert(1, conflict)
        ledger["procedures"]["structural_sweep"]["receipt_count"] = 3
        with self.assertRaisesRegex(AutonomyError, "duplicate or unordered"):
            recovery._validated_current_frontier(
                ledger, self.control(), self.predecessor_control()
            )

    def test_exact_receipt_complete_target_is_readmitted_at_current_frontier(self):
        item = self.closure()
        with patch.object(recovery, "json_content", return_value=self.ledger()), patch.object(
            recovery, "_require_predecessor_merge_ancestry", return_value="d" * 40
        ), patch.object(
            recovery.predecessor, "_require_receipt_introduction"
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

    def test_target_stage_reuses_receipt_without_ledger_mutation(self):
        target = self.control()["target"]
        delegate = Mock(side_effect=AssertionError("delegate must not run for exact target"))
        with patch.object(recovery, "json_content", return_value=self.ledger()), patch.object(
            recovery, "_require_predecessor_merge_ancestry", return_value="d" * 40
        ), patch.object(recovery.predecessor, "_require_receipt_introduction"):
            result = recovery.stage_completion_receipt(
                object(), object(), object(), "grandchallenge/MATH-PROGRAMME", {},
                target["record_id"], target["procedure_id"], target["scheduled_due_at"],
                target["record_path"], {"record_id": target["record_id"]},
                target["candidate_pull_request"], target["reviewed_head"],
                target["record_merge_commit"], "github-actions[bot]",
                "gcl-release-trust[bot]", base=delegate,
            )
        self.assertTrue(result["receipt_recovered"])
        self.assertEqual(result["receipt_pull_request"], 540)
        self.assertEqual(result["protected_current_frontier"], "2026-08-17T03:45:00Z")
        self.assertEqual(result["completion"], self.ledger())
        delegate.assert_not_called()

    def test_mirror_wait_uses_validated_current_frontier(self):
        target = self.control()["target"]
        observed = []

        def mirrors(evidence, runtime, head, frontier):
            observed.append(frontier)
            return True

        with patch.object(recovery, "json_content", return_value=self.ledger()), patch.object(
            recovery, "_require_predecessor_merge_ancestry", return_value="d" * 40
        ), patch.object(recovery.predecessor, "_current_main", return_value="d" * 40), patch.object(
            recovery.predecessor, "_is_ancestor", return_value=True
        ), patch.object(recovery.predecessor, "_successful_sync_run", return_value=77), patch.object(
            recovery.predecessor, "_mirrors_current", side_effect=mirrors
        ), patch.object(recovery.time, "sleep", return_value=None), patch.object(
            recovery.time, "monotonic", side_effect=[0.0, 0.0, 0.0]
        ):
            run = recovery.wait_mirror_sync(
                object(), object(), "grandchallenge/MATH-PROGRAMME",
                target["receipt_introduction_commit"], target["procedure_id"],
                target["scheduled_due_at"], self.runtime(),
            )
        self.assertEqual(run, 77)
        self.assertEqual(observed, ["2026-08-17T03:45:00Z", "2026-08-17T03:45:00Z"])

    def test_runtime_successor_wiring_is_last_before_executor(self):
        text = RUNTIME_ENTRY.read_text(encoding="utf-8")
        predecessor_line = "runtime_github.wait_mirror_sync = descendant_post_receipt_wait_mirror_sync"
        successor_pending = "receipt_stage.pending_closures = current_frontier_post_receipt_pending_closures"
        successor_stage = "receipt_stage.stage_completion_receipt = current_frontier_post_receipt_stage_completion_receipt"
        successor_mirror = "runtime_github.wait_mirror_sync = current_frontier_post_receipt_wait_mirror_sync"
        executor = "from administrative_autonomy_runtime_behind_sync import"
        for line in (predecessor_line, successor_pending, successor_stage, successor_mirror, executor):
            self.assertIn(line, text)
        self.assertLess(text.index(predecessor_line), text.index(successor_pending))
        self.assertLess(text.index(successor_pending), text.index(executor))
        self.assertLess(text.index(successor_stage), text.index(executor))
        self.assertLess(text.index(successor_mirror), text.index(executor))


if __name__ == "__main__":
    unittest.main()
