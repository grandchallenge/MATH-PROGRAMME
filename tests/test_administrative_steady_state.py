from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance/administrative_maintenance_steady_state_0_1.json"
SCHEMA = ROOT / "schemas/administrative_maintenance_steady_state.schema.json"
REGISTRY = ROOT / "governance/administrative_maintenance_trigger_registry.json"
COMPLETION_STATE = ROOT / "governance/administrative_maintenance_completion_state.json"
DISPATCH = ROOT / ".github/workflows/administrative-maintenance-dispatch.yml"
PREPARE_V4 = ROOT / "ci/prepare_administrative_candidate_v4.py"
DISPATCH_V2 = ROOT / "ci/dispatch_administrative_maintenance_v2.py"

EXPECTED_RECURRENT_CRONS = {
    "9 18 * * 6",
    "57 10 * * 0",
    "45 3 * * 1",
    "33 20 * * 1",
    "21 13 * * 2",
    "9 6 * * 3",
    "57 22 * * 3",
    "45 15 * * 4",
    "33 8 * * 5",
    "21 1 * * *",
}


class AdministrativeSteadyStateTests(unittest.TestCase):
    def load_record(self):
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def test_schema_and_authority_boundary(self):
        record = self.load_record()
        jsonschema.validate(record, json.loads(SCHEMA.read_text(encoding="utf-8")))
        self.assertEqual(record["successor_id"], "MP-ADMIN-STEADY-STATE-0.1-001")
        self.assertEqual(record["acceleration_factor"], 0.1)
        self.assertEqual(record["cadence_anchor_utc"], "2026-08-01T01:21:00Z")
        self.assertTrue(record["authority_boundary"]["successor_requires_human_steward_exact_head_disposition"])
        self.assertFalse(record["authority_boundary"]["candidate_branch_is_authority"])
        self.assertFalse(record["authority_boundary"]["future_control_plane_changes_pre_authorized"])
        self.assertFalse(record["historical_evidence_policy"]["eventual_recovery_rewrites_failure"])
        self.assertTrue(all(value is False for value in record["claim_boundaries"].values()))

    def test_successor_horizon_preserves_static_completion_baselines(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        rows = {row["id"]: row for row in registry["procedures"]}
        horizon = "2026-09-06T13:21:00Z"
        for procedure in ("structural_sweep", "administrative_review", "deep_conformance_review"):
            self.assertEqual(rows[procedure]["active_through_utc"], horizon)
        self.assertEqual(rows["structural_sweep"]["interval_minutes"], 1008)
        self.assertEqual(rows["administrative_review"]["interval_minutes"], 4320)
        self.assertEqual(rows["deep_conformance_review"]["interval_minutes"], 12960)
        # Static trigger baselines remain historical/replay-compatible. Current
        # protected completion is overlaid dynamically by dispatcher v2/v3.
        self.assertEqual(rows["structural_sweep"]["completed_through_utc"], "2026-08-01T18:09:00Z")
        self.assertIsNone(rows["administrative_review"]["completed_through_utc"])
        self.assertIsNone(rows["deep_conformance_review"]["completed_through_utc"])
        self.assertEqual(rows["pilot_review"]["active_through_utc"], "2026-08-10T01:21:00Z")

    def test_protected_completion_state_is_runtime_authority(self):
        state = json.loads(COMPLETION_STATE.read_text(encoding="utf-8"))
        procedures = state["procedures"]
        self.assertEqual(procedures["structural_sweep"]["completed_through_utc"], "2026-08-10T20:33:00Z")
        self.assertEqual(procedures["administrative_review"]["completed_through_utc"], "2026-08-10T01:21:00Z")
        self.assertEqual(procedures["deep_conformance_review"]["completed_through_utc"], "2026-08-10T01:21:00Z")
        source = DISPATCH_V2.read_text(encoding="utf-8")
        self.assertIn("derive_completion_state", source)
        self.assertIn("apply_completion_to_registry", source)

    def test_exact_recurrence_is_bound_in_registry_and_workflow(self):
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        registry_crons = set(registry["schedule"]["exact_pilot_crons_utc"])
        self.assertTrue(EXPECTED_RECURRENT_CRONS <= registry_crons)
        workflow = yaml.safe_load(DISPATCH.read_text(encoding="utf-8"))
        # PyYAML 1.1 parses the key 'on' as boolean True.
        on_block = workflow.get("on", workflow.get(True))
        workflow_crons = {row["cron"] for row in on_block["schedule"]}
        self.assertTrue(EXPECTED_RECURRENT_CRONS <= workflow_crons)
        self.assertIn("47 * * * *", workflow_crons)

    def test_transition_bridge_is_exact_and_bounded(self):
        record = self.load_record()
        bridge = record["transition_bridge"]
        self.assertEqual(bridge["occurrence_key"], "structural_sweep:2026-08-10T03:45:00Z")
        self.assertEqual(bridge["normal_freeze_at_utc"], "2026-08-10T02:15:00Z")
        self.assertEqual(bridge["bounded_mutation_until_utc"], bridge["due_at_utc"])
        self.assertTrue(bridge["one_time_only"])
        self.assertFalse(bridge["deadline_reset"])
        self.assertFalse(bridge["required_checks_weakened"])
        self.assertFalse(bridge["exact_head_gate_weakened"])
        source = PREPARE_V4.read_text(encoding="utf-8")
        self.assertIn('TRANSITION_OCCURRENCE_KEY = "structural_sweep:2026-08-10T03:45:00Z"', source)
        self.assertIn("now >= occurrence.due_at", source)
        self.assertIn("successor_transition_mutation_allowed", source)

    def test_mutations_fail_schema_or_invariants(self):
        record = self.load_record()
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        mutated = copy.deepcopy(record)
        mutated["acceleration_factor"] = 1.0
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(mutated, schema)
        mutated = copy.deepcopy(record)
        mutated["authority_boundary"]["waiver_created"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(mutated, schema)
        mutated = copy.deepcopy(record)
        mutated["claim_boundaries"]["external_claim_authorized"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(mutated, schema)
        mutated = copy.deepcopy(record)
        mutated["transition_bridge"]["deadline_reset"] = True
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(mutated, schema)


if __name__ == "__main__":
    unittest.main()
