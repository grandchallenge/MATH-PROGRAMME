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

import administrative_autonomy_runtime_administrative_review_0121_recovery as recovery
from autonomy_github import AutonomyError

CONTROL = ROOT / "governance" / "administrative_review_0121_late_recovery_control.json"
SCHEMA = ROOT / "schemas" / "administrative_review_0121_late_recovery_control.schema.json"
RUNTIME_ENTRY = ROOT / "ci" / "administrative_autonomy_runtime.py"
UTC = timezone.utc


class AdministrativeReview0121LateRecoveryTests(unittest.TestCase):
    def load_control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def runtime(self):
        return {
            "scope": {"recovery_window_minutes_after_due": 180},
            "record_layout": {
                "administrative_review": {
                    "directory": "governance/administrative_reviews"
                }
            },
        }

    def expected_pair(self):
        c = self.load_control()["occurrence"]
        pull = {
            "number": 523,
            "state": "open",
            "head": {"ref": c["candidate_branch"], "sha": c["stale_finalized_head"]},
        }
        manifest = {
            "occurrence_key": c["occurrence_key"],
            "procedure_id": c["procedure_id"],
            "scheduled_due_at": c["due_at_utc"],
            "issue_number": c["candidate_issue"],
            "pull_request_number": c["candidate_pull_request"],
            "branch": c["candidate_branch"],
            "manifest_path": c["manifest_path"],
            "source_protected_head": c["original_source_protected_head"],
        }
        return pull, manifest

    def incomplete_ledger(self):
        return {
            "procedures": {
                "administrative_review": {
                    "completed_through_utc": "2026-08-13T01:21:00Z",
                    "receipts": [],
                }
            }
        }

    def eligible_kwargs(self):
        return {
            "completion_loader": lambda *_: self.incomplete_ledger(),
            "ancestry_checker": lambda *_: True,
            "record_identity_checker": lambda *_: None,
        }

    def test_schema_and_exact_boundary(self):
        control = self.load_control()
        jsonschema.validate(control, json.loads(SCHEMA.read_text(encoding="utf-8")))
        self.assertEqual(control["issue"], 549)
        self.assertEqual(control["occurrence"]["candidate_issue"], 522)
        self.assertEqual(control["occurrence"]["candidate_pull_request"], 523)
        self.assertEqual(
            control["occurrence"]["record_id"],
            "MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-16-001",
        )
        self.assertTrue(
            control["authority_boundary"]["human_steward_exact_head_authorization_required"]
        )
        self.assertFalse(control["authority_boundary"]["stale_referee_approval_is_authority"])
        self.assertFalse(control["authority_boundary"]["general_late_recovery_authority_created"])
        self.assertFalse(control["correction"]["structural_frontier_mutation_authorized"])
        self.assertTrue(all(value is False for value in control["claim_boundaries"].values()))

    def test_bounded_window_is_next_admin_locus(self):
        control = self.load_control()
        runtime = self.runtime()
        self.assertEqual(recovery.bounded_recovery_minutes(runtime, control), 4320)
        self.assertEqual(runtime["scope"]["recovery_window_minutes_after_due"], 180)
        self.assertEqual(
            control["occurrence"]["bounded_recovery_expires_at_utc"],
            "2026-08-19T01:21:00Z",
        )

    def test_existing_chain_wins(self):
        ordinary = ({"number": 999}, {"occurrence_key": "other"})
        result = recovery.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime(),
            datetime(2026, 8, 17, 12, 0, tzinfo=UTC),
            base=lambda *args: [ordinary],
        )
        self.assertEqual(result, [ordinary])

    def test_exact_candidate_only_inside_bounded_window(self):
        pair = self.expected_pair()

        def base(candidate, repo, runtime, now):
            if runtime["scope"]["recovery_window_minutes_after_due"] > 180:
                return [
                    (
                        {"number": 520},
                        {"occurrence_key": "structural_sweep:2026-08-15T18:09:00Z"},
                    ),
                    pair,
                ]
            return []

        kwargs = dict(
            candidate=object(),
            repo="grandchallenge/MATH-PROGRAMME",
            runtime=self.runtime(),
            base=base,
            **self.eligible_kwargs(),
        )
        self.assertEqual(
            recovery.eligible_candidates(
                now=datetime(2026, 8, 16, 4, 20, tzinfo=UTC), **kwargs
            ),
            [],
        )
        self.assertEqual(
            recovery.eligible_candidates(
                now=datetime(2026, 8, 17, 12, 0, tzinfo=UTC), **kwargs
            ),
            [pair],
        )
        self.assertEqual(
            recovery.eligible_candidates(
                now=datetime(2026, 8, 19, 1, 21, tzinfo=UTC), **kwargs
            ),
            [],
        )

    def test_completion_suppresses_recovery_and_duplicate_fails_closed(self):
        pair = self.expected_pair()
        complete = {
            "procedures": {
                "administrative_review": {
                    "completed_through_utc": "2026-08-16T01:21:00Z",
                    "receipts": [{"scheduled_due_at": "2026-08-16T01:21:00Z"}],
                }
            }
        }
        result = recovery.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime(),
            datetime(2026, 8, 17, 12, 0, tzinfo=UTC),
            base=lambda candidate, repo, runtime, now: [pair]
            if runtime["scope"]["recovery_window_minutes_after_due"] > 180
            else [],
            completion_loader=lambda *_: complete,
            ancestry_checker=lambda *_: True,
            record_identity_checker=lambda *_: None,
        )
        self.assertEqual(result, [])

        duplicate = self.incomplete_ledger()
        duplicate["procedures"]["administrative_review"]["receipts"] = [
            {"scheduled_due_at": "2026-08-16T01:21:00Z"},
            {"scheduled_due_at": "2026-08-16T01:21:00Z"},
        ]
        with self.assertRaisesRegex(AutonomyError, "duplicate administrative"):
            recovery.completion_absent(duplicate, self.load_control())

    def test_ancestry_and_identity_drift_fail_closed(self):
        pair = self.expected_pair()
        base = lambda candidate, repo, runtime, now: [pair] if runtime["scope"]["recovery_window_minutes_after_due"] > 180 else []
        with self.assertRaisesRegex(AutonomyError, "not ancestral"):
            recovery.eligible_candidates(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime(),
                datetime(2026, 8, 17, 12, 0, tzinfo=UTC),
                base=base,
                completion_loader=lambda *_: self.incomplete_ledger(),
                ancestry_checker=lambda *_: False,
                record_identity_checker=lambda *_: None,
            )
        pull, manifest = pair
        drifted = copy.deepcopy(manifest)
        drifted["pull_request_number"] = 999
        with self.assertRaisesRegex(AutonomyError, "pull-request identity drift"):
            recovery.eligible_candidates(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime(),
                datetime(2026, 8, 17, 12, 0, tzinfo=UTC),
                base=lambda candidate, repo, runtime, now: [(pull, drifted)]
                if runtime["scope"]["recovery_window_minutes_after_due"] > 180
                else [],
                **self.eligible_kwargs(),
            )

    def test_governed_sync_head_may_advance(self):
        pull, manifest = self.expected_pair()
        advanced = copy.deepcopy(pull)
        advanced["head"]["sha"] = "1" * 40
        result = recovery.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime(),
            datetime(2026, 8, 17, 12, 0, tzinfo=UTC),
            base=lambda candidate, repo, runtime, now: [(advanced, manifest)]
            if runtime["scope"]["recovery_window_minutes_after_due"] > 180
            else [],
            **self.eligible_kwargs(),
        )
        self.assertEqual(result, [(advanced, manifest)])

    def test_allocator_identity_is_exact_and_drift_fails_closed(self):
        control = self.load_control()
        _, manifest = self.expected_pair()
        expected_id = control["occurrence"]["record_id"]
        expected_path = (
            "governance/administrative_reviews/"
            "MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-16-001.json"
        )
        with patch.object(recovery, "list_directory_names", return_value=["older.json"]), patch.object(
            recovery, "record_path_for", return_value=(expected_id, expected_path)
        ):
            recovery.default_record_identity_checker(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime(),
                manifest,
                control,
            )
        with patch.object(recovery, "list_directory_names", return_value=["older.json"]), patch.object(
            recovery,
            "record_path_for",
            return_value=("MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-16-002", expected_path),
        ):
            with self.assertRaisesRegex(AutonomyError, "allocator identity drift"):
                recovery.default_record_identity_checker(
                    object(),
                    "grandchallenge/MATH-PROGRAMME",
                    self.runtime(),
                    manifest,
                    control,
                )

    def test_control_mutations_fail_schema(self):
        control = self.load_control()
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        mutations = (
            ("correction", "global_recovery_window_minutes_unchanged", 4320),
            ("correction", "deadline_reset", True),
            ("correction", "structural_frontier_mutation_authorized", True),
            ("authority_boundary", "human_steward_exact_head_authorization_required", False),
            ("authority_boundary", "stale_referee_approval_is_authority", True),
            ("authority_boundary", "general_late_recovery_authority_created", True),
            ("claim_boundaries", "external_claim_authorized", True),
        )
        for section, field, value in mutations:
            mutated = copy.deepcopy(control)
            mutated[section][field] = value
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(mutated, schema)

    def test_runtime_entrypoint_chains_exact_wrapper_last(self):
        source = RUNTIME_ENTRY.read_text(encoding="utf-8")
        self.assertIn(
            "administrative_autonomy_runtime_administrative_review_0121_recovery",
            source,
        )
        self.assertIn("administrative_review_0121_recovery_eligible_candidates", source)
        self.assertIn(
            "structural_1809_recovery_eligible_candidates,\n    administrative_review_0121_recovery_eligible_candidates,",
            source,
        )


if __name__ == "__main__":
    unittest.main()
