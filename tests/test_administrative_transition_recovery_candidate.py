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

import prepare_administrative_candidate_v5 as recovery

CONTROL = ROOT / "governance" / "administrative_transition_recovery_candidate_control.json"
SCHEMA = ROOT / "schemas" / "administrative_transition_recovery_candidate_control.schema.json"
RUNTIME = ROOT / "governance" / "administrative_autonomy_runtime_integration.json"
AUTOMATION = ROOT / "governance" / "administrative_maintenance_automation.json"
REGISTRY = ROOT / "governance" / "administrative_maintenance_trigger_registry.json"
COMPLETION = ROOT / "governance" / "administrative_maintenance_completion_state.json"
SOURCE = ROOT / "ci" / "prepare_administrative_candidate_v5.py"
UTC = timezone.utc


class AdministrativeTransitionRecoveryCandidateTests(unittest.TestCase):
    def load_control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def load_runtime_inputs(self):
        return (
            json.loads(AUTOMATION.read_text(encoding="utf-8")),
            json.loads(REGISTRY.read_text(encoding="utf-8")),
            json.loads(COMPLETION.read_text(encoding="utf-8")),
        )

    def test_schema_and_exact_bounds(self):
        control = self.load_control()
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        jsonschema.validate(control, schema)
        self.assertEqual(control["occurrence"]["occurrence_key"], "structural_sweep:2026-08-10T03:45:00Z")
        self.assertEqual(control["occurrence"]["reconstruction_expires_at_utc"], "2026-08-10T06:45:00Z")
        self.assertEqual(control["occurrence"]["recovery_window_minutes_after_due"], 180)
        self.assertFalse(control["timing_policy"]["cadence_anchor_reset"])
        self.assertFalse(control["timing_policy"]["eventual_recovery_relabels_on_time"])

    def test_recovery_window_matches_protected_runtime(self):
        control = self.load_control()
        runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
        self.assertEqual(
            control["occurrence"]["recovery_window_minutes_after_due"],
            runtime["scope"]["recovery_window_minutes_after_due"],
        )

    def test_exact_post_due_occurrence_is_reconstructed_without_git_history_dependency(self):
        config, registry, completion = self.load_runtime_inputs()
        now = datetime(2026, 8, 10, 4, 30, tzinfo=UTC)
        with patch.object(recovery, "transition_reconstruction_allowed", return_value=True):
            occurrence = recovery.transition_reconstruction_occurrence(
                config,
                registry,
                completion,
                now,
            )
        self.assertIsNotNone(occurrence)
        self.assertEqual(occurrence.occurrence_key, "structural_sweep:2026-08-10T03:45:00Z")
        self.assertEqual(recovery.automation.iso_z(occurrence.due_at), "2026-08-10T03:45:00Z")
        self.assertEqual(recovery.automation.iso_z(occurrence.prepare_at), "2026-08-09T21:45:00Z")
        self.assertEqual(recovery.automation.iso_z(occurrence.freeze_at), "2026-08-10T02:15:00Z")

    def test_reconstruction_gate_accepts_only_inside_existing_recovery_window(self):
        control = self.load_control()
        completion = json.loads(COMPLETION.read_text(encoding="utf-8"))
        with (
            patch.object(recovery, "successor_record_active", return_value=True),
            patch.object(recovery, "successor_merge_ancestral", return_value=True),
            patch.object(recovery, "completion_absent", return_value=True),
            patch.object(recovery, "protected_record_exists_for_occurrence", return_value=False),
        ):
            self.assertTrue(
                recovery.transition_reconstruction_allowed(
                    datetime(2026, 8, 10, 4, 30, tzinfo=UTC),
                    completion,
                    control,
                )
            )
            self.assertFalse(
                recovery.transition_reconstruction_allowed(
                    datetime(2026, 8, 10, 3, 45, tzinfo=UTC),
                    completion,
                    control,
                )
            )
            self.assertFalse(
                recovery.transition_reconstruction_allowed(
                    datetime(2026, 8, 10, 6, 45, tzinfo=UTC),
                    completion,
                    control,
                )
            )

    def test_authority_and_claim_mutations_fail_schema(self):
        control = self.load_control()
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        for section, field, value in (
            ("authority_boundary", "bypass_created", True),
            ("authority_boundary", "required_checks_weakened", True),
            ("timing_policy", "cadence_anchor_reset", True),
            ("timing_policy", "eventual_recovery_relabels_on_time", True),
            ("claim_boundaries", "certificate_issued", True),
        ):
            mutated = copy.deepcopy(control)
            mutated[section][field] = value
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(mutated, schema)

    def test_source_binds_fail_closed_reconstruction_invariants(self):
        source = SOURCE.read_text(encoding="utf-8")
        for marker in (
            "transition_reconstruction_allowed",
            "completion_absent",
            "protected_record_exists_for_occurrence",
            "successor_merge_ancestral",
            "partial transition-recovery candidate artifacts",
            "transition-recovery occurrence is not on the protected cadence",
            "original_deadline_preserved",
            "lateness_preserved",
        ):
            self.assertIn(marker, source)


if __name__ == "__main__":
    unittest.main()
