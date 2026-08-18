from __future__ import annotations

import copy
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_runtime_structural_0121_recovery as recovery
from autonomy_github import AutonomyError

CONTROL = ROOT / "governance" / "administrative_structural_0121_late_recovery_control.json"
SCHEMA = ROOT / "schemas" / "administrative_structural_0121_late_recovery_control.schema.json"
RUNTIME_ENTRY = ROOT / "ci" / "administrative_autonomy_runtime.py"
UTC = timezone.utc


class AdministrativeStructural0121LateRecoveryTests(unittest.TestCase):
    def load_control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def runtime(self):
        return {"scope": {"recovery_window_minutes_after_due": 180}}

    def receipt(self, due: str, path: str, pr: int):
        return {
            "procedure_id": "structural_sweep",
            "scheduled_due_at": due,
            "record_path": path,
            "record_sha256": "0" * 64,
            "merge_commit": "1" * 40,
            "reviewed_head": "2" * 40,
            "pull_request": pr,
            "disposition": "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            "receipt_state": "PROTECTED_COMPLETE",
        }

    def later_frontier_ledger(self):
        receipts = [
            self.receipt(
                "2026-08-14T08:33:00Z",
                "governance/administrative_structural_sweeps/MP-ADMIN-STRUCTURAL-SWEEP-2026-08-14-001.json",
                514,
            ),
            self.receipt(
                "2026-08-16T10:57:00Z",
                "governance/administrative_structural_sweeps/MP-ADMIN-STRUCTURAL-SWEEP-2026-08-16-001.json",
                526,
            ),
        ]
        return {
            "schema_version": "1.0.0",
            "control_id": "MP-ADMIN-MAINT-001",
            "derived_from_protected_head": "3" * 40,
            "state": "PROTECTED_RECEIPT_DERIVED",
            "procedures": {
                "structural_sweep": {
                    "completed_through_utc": "2026-08-16T10:57:00Z",
                    "receipt_count": len(receipts),
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

    def target_receipt(self):
        control = self.load_control()
        return self.receipt(
            control["occurrence"]["due_at_utc"],
            control["occurrence"]["record_path"],
            516,
        )

    def expected_pair(self, head: str = "f" * 40):
        control = self.load_control()
        pull = {
            "number": 516,
            "head": {
                "ref": control["occurrence"]["candidate_branch"],
                "sha": head,
            },
        }
        manifest = {
            "occurrence_key": control["occurrence"]["occurrence_key"],
            "issue_number": 515,
            "pull_request_number": 516,
            "branch": control["occurrence"]["candidate_branch"],
            "source_protected_head": control["occurrence"]["original_source_protected_head"],
        }
        return pull, manifest

    def test_schema_and_authority_boundary(self):
        control = self.load_control()
        jsonschema.validate(control, json.loads(SCHEMA.read_text(encoding="utf-8")))
        self.assertEqual(control["issue"], 534)
        self.assertEqual(control["occurrence"]["candidate_issue"], 515)
        self.assertEqual(control["occurrence"]["candidate_pull_request"], 516)
        self.assertEqual(control["occurrence"]["bounded_recovery_expires_at_utc"], "2026-08-17T03:45:00Z")
        self.assertTrue(control["correction"]["later_completion_frontier_preserved"])
        self.assertTrue(control["correction"]["mirror_current_frontier_preserved"])
        self.assertTrue(control["authority_boundary"]["human_steward_exact_head_authorization_required"])
        self.assertFalse(control["authority_boundary"]["general_late_recovery_authority_created"])
        self.assertTrue(all(value is False for value in control["claim_boundaries"].values()))

    def test_exact_hole_is_absent_despite_later_frontier(self):
        control = self.load_control()
        ledger = self.later_frontier_ledger()
        self.assertTrue(recovery.exact_receipt_absent(ledger, control))
        ledger["procedures"]["structural_sweep"]["receipts"].insert(1, self.target_receipt())
        ledger["procedures"]["structural_sweep"]["receipt_count"] = 3
        self.assertFalse(recovery.exact_receipt_absent(ledger, control))

    def test_hole_detection_requires_later_frontier(self):
        ledger = self.later_frontier_ledger()
        ledger["procedures"]["structural_sweep"]["completed_through_utc"] = "2026-08-15T01:21:00Z"
        with self.assertRaisesRegex(AutonomyError, "later than the hole"):
            recovery.exact_receipt_absent(ledger, self.load_control())

    def test_bounded_window_is_3024_and_global_window_unchanged(self):
        runtime = self.runtime()
        self.assertEqual(recovery.bounded_recovery_minutes(runtime, self.load_control()), 3024)
        self.assertEqual(runtime["scope"]["recovery_window_minutes_after_due"], 180)

    def test_ordinary_eligibility_precedes_hole_recovery(self):
        sentinel = self.expected_pair()
        result = recovery.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime(),
            datetime(2026, 8, 16, 21, 40, tzinfo=UTC),
            base=lambda candidate, repo, runtime, now: [sentinel],
        )
        self.assertEqual(result, [sentinel])

    def test_widened_replay_filters_exact_515_and_allows_post_sync_head(self):
        expected = self.expected_pair("e" * 40)
        other = (
            {"number": 521, "head": {"sha": "d" * 40}},
            {
                "occurrence_key": "structural_sweep:2026-08-15T18:09:00Z",
                "issue_number": 520,
                "pull_request_number": 521,
                "branch": "automation/maintenance/structural_sweep-20260815T180900Z",
                "source_protected_head": "d0daf58cfcc5ca738d9b5c4f4bf712ba4a37b27c",
            },
        )
        calls = []

        def base(candidate, repo, runtime, now):
            window = runtime["scope"]["recovery_window_minutes_after_due"]
            calls.append(window)
            return [] if window == 180 else [expected, other]

        result = recovery.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime(),
            datetime(2026, 8, 16, 21, 40, tzinfo=UTC),
            base=base,
            completion_loader=lambda candidate, repo: self.later_frontier_ledger(),
            ancestry_checker=lambda candidate, repo, source: True,
        )
        self.assertEqual(calls, [180, 3024])
        self.assertEqual(result, [expected])
        self.assertNotEqual(expected[0]["head"]["sha"], self.load_control()["occurrence"]["stale_finalized_head"])

    def test_bounded_expiry_and_source_ancestry_fail_closed(self):
        result = recovery.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime(),
            datetime(2026, 8, 17, 3, 45, tzinfo=UTC),
            base=lambda candidate, repo, runtime, now: [],
        )
        self.assertEqual(result, [])
        with self.assertRaisesRegex(AutonomyError, "not ancestral"):
            recovery.eligible_candidates(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime(),
                datetime(2026, 8, 16, 21, 40, tzinfo=UTC),
                base=lambda candidate, repo, runtime, now: [],
                completion_loader=lambda candidate, repo: self.later_frontier_ledger(),
                ancestry_checker=lambda candidate, repo, source: False,
            )

    def test_backfill_inserts_sorted_receipt_without_lowering_frontier(self):
        current = self.later_frontier_ledger()
        target = self.target_receipt()
        updated = recovery.advance_completion_state(current, target, "4" * 40)
        procedure = updated["procedures"]["structural_sweep"]
        self.assertEqual(procedure["receipt_count"], 3)
        self.assertEqual(procedure["completed_through_utc"], "2026-08-16T10:57:00Z")
        self.assertEqual(
            [item["scheduled_due_at"] for item in procedure["receipts"]],
            ["2026-08-14T08:33:00Z", "2026-08-15T01:21:00Z", "2026-08-16T10:57:00Z"],
        )
        self.assertEqual(updated["derived_from_protected_head"], "4" * 40)
        self.assertEqual(recovery.advance_completion_state(updated, target, "5" * 40), updated)

    def test_backfill_rejects_conflict_and_non_target_delegates(self):
        current = self.later_frontier_ledger()
        conflict = copy.deepcopy(self.target_receipt())
        conflict["record_path"] = "governance/administrative_structural_sweeps/conflict.json"
        current["procedures"]["structural_sweep"]["receipts"].insert(1, conflict)
        current["procedures"]["structural_sweep"]["receipt_count"] = 3
        with self.assertRaisesRegex(AutonomyError, "conflicting exact"):
            recovery.advance_completion_state(current, self.target_receipt(), "4" * 40)

        sentinel = {"delegated": True}
        delegated = recovery.advance_completion_state(
            self.later_frontier_ledger(),
            self.receipt("2026-08-17T03:45:00Z", "governance/administrative_structural_sweeps/later.json", 999),
            "4" * 40,
            base=lambda current, receipt, merge: sentinel,
        )
        self.assertIs(delegated, sentinel)

    def test_mirror_readback_uses_preserved_frontier_after_exact_receipt(self):
        completion = recovery.advance_completion_state(
            self.later_frontier_ledger(), self.target_receipt(), "4" * 40
        )
        observed = {}

        def base(observability, evidence, repo, merge_sha, procedure, due, runtime):
            observed["due"] = due
            observed["merge"] = merge_sha
            return 77

        with patch.object(recovery, "json_content", return_value=completion):
            result = recovery.wait_mirror_sync(
                object(), object(), "grandchallenge/MATH-PROGRAMME", "5" * 40,
                "structural_sweep", "2026-08-15T01:21:00Z", {}, base=base,
            )
        self.assertEqual(result, 77)
        self.assertEqual(observed["due"], "2026-08-16T10:57:00Z")
        self.assertEqual(observed["merge"], "5" * 40)

    def test_runtime_wiring_covers_selection_receipt_and_mirror_paths(self):
        text = RUNTIME_ENTRY.read_text(encoding="utf-8")
        self.assertIn("structural_0121_recovery_eligible_candidates", text)
        self.assertIn("receipt_stage.advance_completion_state = structural_0121_hole_advance_completion_state", text)
        self.assertIn("receipt_resume.advance_completion_state = structural_0121_hole_advance_completion_state", text)
        self.assertIn("runtime_github.wait_mirror_sync = structural_0121_hole_wait_mirror_sync", text)


if __name__ == "__main__":
    unittest.main()
