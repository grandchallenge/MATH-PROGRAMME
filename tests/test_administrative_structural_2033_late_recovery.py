from __future__ import annotations

import copy
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_runtime_structural_2033_recovery as recovery
from autonomy_github import AutonomyError

CONTROL = ROOT / "governance" / "administrative_structural_2033_late_recovery_control.json"
SCHEMA = ROOT / "schemas" / "administrative_structural_2033_late_recovery_control.schema.json"
RUNTIME_ENTRY = ROOT / "ci" / "administrative_autonomy_runtime.py"
UTC = timezone.utc


class AdministrativeStructural2033LateRecoveryTests(unittest.TestCase):
    def load_control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def runtime(self):
        return {"scope": {"recovery_window_minutes_after_due": 180}}

    def expected_pair(self):
        control = self.load_control()
        pull = {
            "number": 401,
            "state": "open",
            "head": {"ref": control["occurrence"]["candidate_branch"]},
        }
        manifest = {
            "occurrence_key": control["occurrence"]["occurrence_key"],
            "issue_number": 400,
            "pull_request_number": 401,
            "branch": control["occurrence"]["candidate_branch"],
            "source_protected_head": control["occurrence"]["original_source_protected_head"],
        }
        return pull, manifest

    def incomplete_ledger(self):
        return {
            "procedures": {
                "structural_sweep": {
                    "completed_through_utc": "2026-08-10T03:45:00Z",
                    "receipts": [],
                }
            }
        }

    def test_schema_and_exact_authority_boundary(self):
        control = self.load_control()
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        jsonschema.validate(control, schema)
        self.assertEqual(control["issue"], 404)
        self.assertEqual(control["occurrence"]["candidate_issue"], 400)
        self.assertEqual(control["occurrence"]["candidate_pull_request"], 401)
        self.assertEqual(control["correction"]["global_recovery_window_minutes_unchanged"], 180)
        self.assertFalse(control["correction"]["deadline_reset"])
        self.assertFalse(control["correction"]["cadence_anchor_reset"])
        self.assertFalse(control["correction"]["eventual_recovery_relabels_on_time"])
        self.assertTrue(control["authority_boundary"]["human_steward_exact_head_authorization_required"])
        self.assertFalse(control["authority_boundary"]["general_late_recovery_authority_created"])
        self.assertTrue(all(value is False for value in control["claim_boundaries"].values()))

    def test_bounded_window_is_exactly_next_structural_locus(self):
        control = self.load_control()
        self.assertEqual(recovery.bounded_recovery_minutes(self.runtime(), control), 1008)
        self.assertEqual(control["occurrence"]["bounded_recovery_expires_at_utc"], "2026-08-11T13:21:00Z")

    def test_ordinary_runtime_always_wins(self):
        ordinary = ({"number": 999}, {"occurrence_key": "other"})

        def base(candidate, repo, runtime, now):
            return [ordinary]

        result = recovery.eligible_candidates(
            object(), "grandchallenge/MATH-PROGRAMME", self.runtime(),
            datetime(2026, 8, 11, 1, 0, tzinfo=UTC), base=base,
        )
        self.assertEqual(result, [ordinary])

    def test_exact_candidate_is_admitted_only_after_ordinary_expiry(self):
        pair = self.expected_pair()

        def base(candidate, repo, runtime, now):
            if runtime["scope"]["recovery_window_minutes_after_due"] > 180:
                return [pair]
            return []

        kwargs = {
            "candidate": object(),
            "repo": "grandchallenge/MATH-PROGRAMME",
            "runtime": self.runtime(),
            "base": base,
            "completion_loader": lambda candidate, repo: self.incomplete_ledger(),
            "ancestry_checker": lambda candidate, repo, source: True,
        }
        before = recovery.eligible_candidates(
            now=datetime(2026, 8, 10, 23, 30, tzinfo=UTC), **kwargs
        )
        inside = recovery.eligible_candidates(
            now=datetime(2026, 8, 11, 1, 0, tzinfo=UTC), **kwargs
        )
        expired = recovery.eligible_candidates(
            now=datetime(2026, 8, 11, 13, 21, tzinfo=UTC), **kwargs
        )
        self.assertEqual(before, [])
        self.assertEqual(inside, [pair])
        self.assertEqual(expired, [])

    def test_protected_completion_suppresses_continuation(self):
        pair = self.expected_pair()

        def base(candidate, repo, runtime, now):
            return [pair] if runtime["scope"]["recovery_window_minutes_after_due"] > 180 else []

        complete = {
            "procedures": {
                "structural_sweep": {
                    "completed_through_utc": "2026-08-10T20:33:00Z",
                    "receipts": [{"scheduled_due_at": "2026-08-10T20:33:00Z"}],
                }
            }
        }
        result = recovery.eligible_candidates(
            object(), "grandchallenge/MATH-PROGRAMME", self.runtime(),
            datetime(2026, 8, 11, 1, 0, tzinfo=UTC), base=base,
            completion_loader=lambda candidate, repo: complete,
            ancestry_checker=lambda candidate, repo, source: True,
        )
        self.assertEqual(result, [])

    def test_ancestry_failure_and_identity_drift_fail_closed(self):
        pair = self.expected_pair()

        def base(candidate, repo, runtime, now):
            return [pair] if runtime["scope"]["recovery_window_minutes_after_due"] > 180 else []

        with self.assertRaises(AutonomyError):
            recovery.eligible_candidates(
                object(), "grandchallenge/MATH-PROGRAMME", self.runtime(),
                datetime(2026, 8, 11, 1, 0, tzinfo=UTC), base=base,
                completion_loader=lambda candidate, repo: self.incomplete_ledger(),
                ancestry_checker=lambda candidate, repo, source: False,
            )

        pull, manifest = self.expected_pair()
        drifted = copy.deepcopy(manifest)
        drifted["pull_request_number"] = 999

        def drift_base(candidate, repo, runtime, now):
            return [(pull, drifted)] if runtime["scope"]["recovery_window_minutes_after_due"] > 180 else []

        with self.assertRaises(AutonomyError):
            recovery.eligible_candidates(
                object(), "grandchallenge/MATH-PROGRAMME", self.runtime(),
                datetime(2026, 8, 11, 1, 0, tzinfo=UTC), base=drift_base,
                completion_loader=lambda candidate, repo: self.incomplete_ledger(),
                ancestry_checker=lambda candidate, repo, source: True,
            )

    def test_control_mutations_fail_schema(self):
        control = self.load_control()
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        mutations = (
            ("correction", "global_recovery_window_minutes_unchanged", 1008),
            ("correction", "deadline_reset", True),
            ("correction", "cadence_anchor_reset", True),
            ("authority_boundary", "human_steward_exact_head_authorization_required", False),
            ("authority_boundary", "general_late_recovery_authority_created", True),
            ("claim_boundaries", "external_claim_authorized", True),
        )
        for section, field, value in mutations:
            mutated = copy.deepcopy(control)
            mutated[section][field] = value
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(mutated, schema)

    def test_runtime_entrypoint_uses_exact_wrapper(self):
        source = RUNTIME_ENTRY.read_text(encoding="utf-8")
        self.assertIn("administrative_autonomy_runtime_structural_2033_recovery", source)
        self.assertIn("structural_2033_recovery_eligible_candidates", source)


if __name__ == "__main__":
    unittest.main()
