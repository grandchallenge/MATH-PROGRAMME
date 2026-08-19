from __future__ import annotations

import base64
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

import administrative_autonomy_runtime_structural_1809_recovery as recovery
from autonomy_github import AutonomyError

CONTROL = ROOT / "governance" / "administrative_structural_1809_late_recovery_control.json"
SCHEMA = ROOT / "schemas" / "administrative_structural_1809_late_recovery_control.schema.json"
RUNTIME_ENTRY = ROOT / "ci" / "administrative_autonomy_runtime.py"
UTC = timezone.utc


class FakeClient:
    def __init__(self):
        self.calls = []
        self.puts = []

    def put(self, path, payload):
        self.puts.append((path, payload))
        return {"commit": {"sha": "8" * 40}}

    def call(self, method, path, payload):
        self.calls.append((method, path, payload))
        return {"commit": {"sha": "9" * 40}}


class AdministrativeStructural1809LateRecoveryTests(unittest.TestCase):
    def load_control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def runtime(self):
        return {
            "scope": {"recovery_window_minutes_after_due": 180},
            "first_production_occurrence": {
                "occurrence_key": "structural_sweep:2026-08-04T23:09:00Z",
                "record_id": "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-001",
            },
            "record_layout": {
                "structural_sweep": {
                    "id_prefix": "MP-ADMIN-STRUCTURAL-SWEEP",
                    "directory": "governance/administrative_structural_sweeps",
                }
            },
        }

    def receipt(self, due, path, pr, merge="1" * 40):
        return {
            "procedure_id": "structural_sweep",
            "scheduled_due_at": due,
            "record_path": path,
            "record_sha256": "0" * 64,
            "merge_commit": merge,
            "reviewed_head": "2" * 40,
            "pull_request": pr,
            "disposition": "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            "receipt_state": "PROTECTED_COMPLETE",
        }

    def ledger(self):
        receipts = [
            self.receipt(
                "2026-08-15T01:21:00Z",
                "governance/administrative_structural_sweeps/MP-ADMIN-STRUCTURAL-SWEEP-2026-08-15-001.json",
                516,
                "a" * 40,
            ),
            self.receipt(
                "2026-08-17T03:45:00Z",
                "governance/administrative_structural_sweeps/MP-ADMIN-STRUCTURAL-SWEEP-2026-08-17-001.json",
                537,
                "b" * 40,
            ),
        ]
        return {
            "schema_version": "1.0.0",
            "control_id": "MP-ADMIN-MAINT-001",
            "derived_from_protected_head": "b" * 40,
            "state": "PROTECTED_RECEIPT_DERIVED",
            "procedures": {
                "structural_sweep": {
                    "completed_through_utc": "2026-08-17T03:45:00Z",
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

    def pair(self, head="f" * 40):
        c = self.load_control()
        return (
            {"number": 521, "head": {"ref": c["occurrence"]["candidate_branch"], "sha": head}},
            {
                "state": "CANDIDATE_PREPARED",
                "procedure_id": "structural_sweep",
                "occurrence_key": c["occurrence"]["occurrence_key"],
                "scheduled_due_at": c["occurrence"]["due_at_utc"],
                "issue_number": 520,
                "pull_request_number": 521,
                "branch": c["occurrence"]["candidate_branch"],
                "manifest_path": c["occurrence"]["manifest_path"],
                "source_protected_head": c["occurrence"]["original_source_protected_head"],
            },
        )

    def stale_record(self):
        c = self.load_control()
        return {
            "record_id": c["collision"]["stale_record_id"],
            "scheduled_due_at": c["occurrence"]["due_at_utc"],
            "source_candidate": {
                "occurrence_key": c["occurrence"]["occurrence_key"],
                "issue_number": 520,
                "pull_request_number": 521,
                "branch": c["occurrence"]["candidate_branch"],
                "manifest_path": c["occurrence"]["manifest_path"],
                "source_protected_head": c["occurrence"]["original_source_protected_head"],
            },
        }

    def target_receipt(self):
        c = self.load_control()
        return self.receipt(
            c["occurrence"]["due_at_utc"], c["collision"]["canonical_record_path"], 521, "c" * 40
        )

    def test_schema_and_boundaries(self):
        control = self.load_control()
        jsonschema.validate(control, json.loads(SCHEMA.read_text(encoding="utf-8")))
        self.assertEqual(control["issue"], 546)
        self.assertEqual(control["occurrence"]["candidate_issue"], 520)
        self.assertEqual(control["collision"]["canonical_record_id"], "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-15-002")
        self.assertFalse(control["authority_boundary"]["general_identity_rewrite_authority_created"])
        self.assertFalse(control["authority_boundary"]["issue_522_or_pr_523_authority_created"])
        self.assertTrue(all(value is False for value in control["claim_boundaries"].values()))

    def test_allocator_derives_002_and_fails_if_002_is_already_occupied(self):
        control = self.load_control()
        _, manifest = self.pair()
        with patch.object(recovery, "list_directory_names", return_value=["MP-ADMIN-STRUCTURAL-SWEEP-2026-08-15-001.json"]):
            record_id, path = recovery._canonical_target_identity(
                object(), "grandchallenge/MATH-PROGRAMME", self.runtime(), manifest, control
            )
        self.assertEqual(record_id, control["collision"]["canonical_record_id"])
        self.assertEqual(path, control["collision"]["canonical_record_path"])
        with patch.object(
            recovery,
            "list_directory_names",
            return_value=[
                "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-15-001.json",
                "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-15-002.json",
            ],
        ):
            with self.assertRaisesRegex(AutonomyError, "allocator drift"):
                recovery._canonical_target_identity(
                    object(), "grandchallenge/MATH-PROGRAMME", self.runtime(), manifest, control
                )

    def test_exact_receipt_hole_and_bounded_window(self):
        control = self.load_control()
        ledger = self.ledger()
        self.assertTrue(recovery.exact_receipt_absent(ledger, control))
        self.assertEqual(recovery.bounded_recovery_minutes(self.runtime(), control), 3024)
        ledger["procedures"]["structural_sweep"]["receipts"].insert(1, self.target_receipt())
        ledger["procedures"]["structural_sweep"]["receipt_count"] = 3
        self.assertFalse(recovery.exact_receipt_absent(ledger, control))

    def test_ordinary_eligibility_precedes_exact_recovery(self):
        sentinel = self.pair()
        result = recovery.eligible_candidates(
            object(), "grandchallenge/MATH-PROGRAMME", self.runtime(),
            datetime(2026, 8, 17, 10, 50, tzinfo=UTC),
            base=lambda candidate, repo, runtime, now: [sentinel],
        )
        self.assertEqual(result, [sentinel])

    def test_widened_replay_filters_520_and_preserves_522_boundary(self):
        expected = self.pair("e" * 40)
        other = (
            {"number": 523, "head": {"sha": "d" * 40}},
            {"occurrence_key": "structural_sweep:2026-08-16T10:57:00Z", "issue_number": 522},
        )
        calls = []
        def base(candidate, repo, runtime, now):
            calls.append(runtime["scope"]["recovery_window_minutes_after_due"])
            return [] if calls[-1] == 180 else [expected, other]
        with patch.object(recovery, "_require_protected_occupant"), patch.object(
            recovery, "_canonical_target_identity", return_value=("x", "y")
        ):
            result = recovery.eligible_candidates(
                object(), "grandchallenge/MATH-PROGRAMME", self.runtime(),
                datetime(2026, 8, 17, 10, 50, tzinfo=UTC), base=base,
                completion_loader=lambda candidate, repo: self.ledger(),
                ancestry_checker=lambda candidate, repo, source: True,
            )
        self.assertEqual(calls, [180, 3024])
        self.assertEqual(result, [expected])
        self.assertEqual(
            recovery.eligible_candidates(
                object(), "grandchallenge/MATH-PROGRAMME", self.runtime(),
                datetime(2026, 8, 17, 20, 33, tzinfo=UTC),
                base=lambda candidate, repo, runtime, now: [],
            ), []
        )

    def test_source_ancestry_fails_closed(self):
        with self.assertRaisesRegex(AutonomyError, "not ancestral"):
            recovery.eligible_candidates(
                object(), "grandchallenge/MATH-PROGRAMME", self.runtime(),
                datetime(2026, 8, 17, 10, 50, tzinfo=UTC),
                base=lambda candidate, repo, runtime, now: [],
                completion_loader=lambda candidate, repo: self.ledger(),
                ancestry_checker=lambda candidate, repo, source: False,
            )

    def test_normalization_preserves_historical_record_body_and_removes_only_stale_blob(self):
        client = FakeClient()
        pull, manifest = self.pair()
        control = self.load_control()
        stale = self.stale_record()
        raw = {
            "sha": control["collision"]["stale_branch_blob_sha"],
            "content": base64.b64encode(json.dumps(stale).encode()).decode(),
        }
        with patch.object(recovery, "_require_protected_occupant"), patch.object(
            recovery, "_canonical_target_identity"
        ), patch.object(recovery, "_branch_record", side_effect=[(raw, stale), None]), patch.object(
            recovery, "validate_record", return_value=[]
        ):
            event = recovery.normalize_target_collision(
                client, "grandchallenge/MATH-PROGRAMME", self.runtime(), pull, manifest
            )
        self.assertTrue(event["historical_record_body_preserved"])
        self.assertEqual(len(client.puts), 1)
        canonical = json.loads(base64.b64decode(client.puts[0][1]["content"]))
        expected = copy.deepcopy(stale)
        expected["record_id"] = control["collision"]["canonical_record_id"]
        self.assertEqual(canonical, expected)
        self.assertEqual(len(client.calls), 1)
        self.assertEqual(client.calls[0][0], "DELETE")
        self.assertEqual(client.calls[0][2]["sha"], control["collision"]["stale_branch_blob_sha"])

    def test_sync_wrapper_normalizes_then_uses_ordinary_behind_sync(self):
        expected = self.pair()
        with patch.object(recovery, "eligible_candidates", return_value=[expected]), patch.object(
            recovery, "normalize_target_collision", return_value={"normalization_commit": "9" * 40}
        ):
            result = recovery.synchronize_eligible_candidate(
                object(), "grandchallenge/MATH-PROGRAMME", self.runtime(), {}, 1,
                base=lambda candidate, repo, runtime, control, attempt: {
                    "trigger": "BEHIND", "synchronized_head": "8" * 40
                },
            )
        self.assertEqual(result["trigger"], "EXACT_1809_IDENTITY_COLLISION_NORMALIZATION_AND_BEHIND")
        self.assertEqual(result["ordinary_behind_sync_event"]["trigger"], "BEHIND")

    def test_backfill_uses_002_and_preserves_current_frontier(self):
        current = self.ledger()
        target = self.target_receipt()
        updated = recovery.advance_completion_state(current, target, "4" * 40)
        procedure = updated["procedures"]["structural_sweep"]
        self.assertEqual(procedure["completed_through_utc"], "2026-08-17T03:45:00Z")
        self.assertEqual(
            [item["scheduled_due_at"] for item in procedure["receipts"]],
            ["2026-08-15T01:21:00Z", "2026-08-15T18:09:00Z", "2026-08-17T03:45:00Z"],
        )
        self.assertEqual(procedure["receipts"][1]["record_path"], self.load_control()["collision"]["canonical_record_path"])
        stale = copy.deepcopy(target)
        stale["record_path"] = self.load_control()["collision"]["stale_record_path"]
        with self.assertRaisesRegex(AutonomyError, "receipt identity drift"):
            recovery.advance_completion_state(current, stale, "4" * 40)

    def test_mirror_readback_uses_preserved_current_frontier(self):
        completion = recovery.advance_completion_state(self.ledger(), self.target_receipt(), "4" * 40)
        observed = {}
        def base(observability, evidence, repo, merge_sha, procedure, due, runtime):
            observed["due"] = due
            return 88
        with patch.object(recovery, "json_content", return_value=completion):
            result = recovery.wait_mirror_sync(
                object(), object(), "grandchallenge/MATH-PROGRAMME", "5" * 40,
                "structural_sweep", "2026-08-15T18:09:00Z", {}, base=base,
            )
        self.assertEqual(result, 88)
        self.assertEqual(observed["due"], "2026-08-17T03:45:00Z")

    def test_runtime_wiring_adds_exact_520_overlay_after_prior_controls(self):
        text = RUNTIME_ENTRY.read_text(encoding="utf-8")
        self.assertIn("structural_0121_recovery_eligible_candidates", text)
        self.assertIn("structural_1809_recovery_eligible_candidates", text)
        self.assertIn("structural_1809_collision_advance_completion_state", text)
        self.assertIn("base=structural_0121_hole_advance_completion_state", text)
        self.assertIn("base=current_frontier_post_receipt_wait_mirror_sync", text)
        self.assertIn("structural_1809_synchronize_eligible_candidate", text)


if __name__ == "__main__":
    unittest.main()
