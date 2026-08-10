from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "governance" / "administrative_transition_recovery_candidate_control.json"
SCHEMA = ROOT / "schemas" / "administrative_transition_recovery_candidate_control.schema.json"
RUNTIME = ROOT / "governance" / "administrative_autonomy_runtime_integration.json"
SOURCE = ROOT / "ci" / "prepare_administrative_candidate_v5.py"


class AdministrativeTransitionRecoveryCandidateTests(unittest.TestCase):
    def load_control(self):
        return json.loads(CONTROL.read_text(encoding="utf-8"))

    def run_dry(self, now: str):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            env = dict(os.environ)
            # Use the checked-out commit, not a stale workflow event SHA, when
            # proving successor ancestry in this subprocess.
            env.pop("GITHUB_SHA", None)
            completed = subprocess.run(
                [
                    sys.executable,
                    "ci/prepare_administrative_candidate_v5.py",
                    "--now",
                    now,
                    "--report",
                    str(report),
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, msg=completed.stdout + completed.stderr)
            return json.loads(report.read_text(encoding="utf-8"))

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

    def test_exact_post_due_occurrence_is_reconstructed_for_dry_run(self):
        report = self.run_dry("2026-08-10T04:30:00Z")
        keys = {item["occurrence_key"] for item in report["results"]}
        self.assertIn("structural_sweep:2026-08-10T03:45:00Z", keys)
        exact = next(item for item in report["results"] if item["occurrence_key"] == "structural_sweep:2026-08-10T03:45:00Z")
        self.assertFalse(exact["mutation_allowed"])
        self.assertEqual(exact["scheduled_due_at"], "2026-08-10T03:45:00Z")
        self.assertEqual(exact["prepare_at"], "2026-08-09T21:45:00Z")
        self.assertEqual(exact["freeze_at"], "2026-08-10T02:15:00Z")

    def test_reconstruction_expires_at_existing_recovery_boundary(self):
        report = self.run_dry("2026-08-10T06:45:00Z")
        keys = {item["occurrence_key"] for item in report["results"]}
        self.assertNotIn("structural_sweep:2026-08-10T03:45:00Z", keys)

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
