from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "administrative_pilot_adjudication_2026_08_10.json"
SCHEMA = ROOT / "schemas" / "administrative_pilot_adjudication.schema.json"
STEADY_STATE = ROOT / "governance" / "administrative_maintenance_steady_state_0_1.json"


class AdministrativePilotAdjudicationTests(unittest.TestCase):
    def load_record(self):
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def load_schema(self):
        return json.loads(SCHEMA.read_text(encoding="utf-8"))

    def validate(self, record):
        jsonschema.Draft202012Validator(self.load_schema()).validate(record)

    def test_record_is_closed_and_selects_council_option_c(self):
        record = self.load_record()
        self.validate(record)
        self.assertEqual(record["docket"], 320)
        self.assertEqual(record["council"]["quorum"], "8/8")
        self.assertEqual(record["council"]["consensus"], "UNANIMOUS")
        self.assertEqual(record["decision"]["selected_option"], "C")
        self.assertEqual(
            record["decision"]["disposition"],
            "RETAIN_ACCELERATION_0_1_WITH_AUTONOMY_HARDENING_CONDITIONS",
        )
        self.assertEqual(record["decision"]["acceleration_factor"], 0.1)
        self.assertEqual(record["decision"]["cadence_anchor_utc"], "2026-08-01T01:21:00Z")

    def test_successor_is_recognized_not_reactivated(self):
        record = self.load_record()
        steady = json.loads(STEADY_STATE.read_text(encoding="utf-8"))
        self.assertEqual(record["decision"]["steady_state_successor"], steady["successor_id"])
        self.assertEqual(steady["status"], "ACTIVE_ON_PROTECTED_MERGE")
        self.assertEqual(steady["acceleration_factor"], record["decision"]["acceleration_factor"])
        self.assertEqual(steady["cadence_anchor_utc"], record["decision"]["cadence_anchor_utc"])
        self.assertTrue(record["decision"]["successor_already_separately_protected"])
        self.assertFalse(record["decision"]["this_adjudication_activates_successor"])
        self.assertEqual(record["decision"]["pilot_historical_status_remains"], "APPROVED_ACCELERATED_PILOT")

    def test_pilot_and_post_pilot_evidence_are_not_conflated(self):
        record = self.load_record()
        self.assertTrue(record["pilot_evidence"]["administrative_review"]["protected_before_due"])
        self.assertTrue(record["pilot_evidence"]["freeze_reconciliation"]["observed_blocker_was_real"])
        self.assertFalse(
            record["pilot_evidence"]["freeze_reconciliation"]["freeze_gate_produced_review_ready_final_record"]
        )
        self.assertTrue(record["pilot_evidence"]["freeze_reconciliation"]["resolved_before_due"])
        self.assertEqual(
            record["post_pilot_corroboration"]["first_transition_occurrence"]["classification"],
            "POST_PILOT",
        )
        self.assertEqual(
            record["post_pilot_corroboration"]["steady_state_2033_occurrence"]["classification"],
            "POST_PILOT",
        )
        self.assertTrue(record["post_pilot_corroboration"]["first_transition_occurrence"]["late"])
        self.assertTrue(record["post_pilot_corroboration"]["steady_state_2033_occurrence"]["late"])
        self.assertFalse(record["historical_evidence_policy"]["post_pilot_events_reclassified_as_pilot_events"])

    def test_hardening_remains_open_and_nonwaived(self):
        record = self.load_record()
        self.assertEqual(record["hardening"]["residual_open_issue"], 407)
        self.assertEqual(
            record["hardening"]["residual_open_issue_state"],
            "OPEN_HARDENING_OBLIGATION__NO_AUTHORITY_CREATED",
        )
        self.assertFalse(record["hardening"]["hardening_complete"])
        self.assertTrue(record["hardening"]["hardening_noncompletion_is_not_waived"])
        self.assertEqual(len(record["hardening"]["required_conditions"]), 8)

    def test_stale_candidate_is_explicitly_non_authoritative(self):
        record = self.load_record()
        stale = record["retired_stale_candidate"]
        self.assertEqual(stale["issue"], 335)
        self.assertEqual(stale["pull_request"], 336)
        self.assertFalse(stale["candidate_is_authority"])
        self.assertFalse(stale["pull_request_merged"])
        self.assertFalse(record["authority_boundary"]["stale_candidate_336_is_authority"])

    def test_authority_and_claim_boundaries_are_closed(self):
        record = self.load_record()
        boundary = record["authority_boundary"]
        self.assertFalse(boundary["council_packet_is_binding_human_steward_authority"])
        self.assertTrue(boundary["human_steward_exact_head_authorization_required"])
        self.assertFalse(boundary["future_control_plane_changes_pre_authorized"])
        self.assertFalse(boundary["hardening_issue_407_is_implementation_authority"])
        self.assertFalse(boundary["waiver_created"])
        self.assertFalse(boundary["emergency_authority_created"])
        self.assertFalse(boundary["direct_protected_push_authorized"])
        self.assertFalse(boundary["required_checks_weakened"])
        self.assertFalse(boundary["referee_separation_weakened"])
        self.assertTrue(all(value is False for value in record["claim_boundaries"].values()))

    def test_critical_mutations_fail_schema(self):
        record = self.load_record()
        mutations = (
            ("decision", "selected_option", "A"),
            ("decision", "selected_option", "B"),
            ("decision", "selected_option", "D"),
            ("decision", "acceleration_factor", 1.0),
            ("decision", "this_adjudication_activates_successor", True),
            ("hardening", "hardening_complete", True),
            ("hardening", "hardening_noncompletion_is_not_waived", False),
            ("retired_stale_candidate", "candidate_is_authority", True),
            ("authority_boundary", "human_steward_exact_head_authorization_required", False),
            ("authority_boundary", "future_control_plane_changes_pre_authorized", True),
            ("authority_boundary", "required_checks_weakened", True),
            ("claim_boundaries", "external_claim_authorized", True),
        )
        for section, field, value in mutations:
            mutated = copy.deepcopy(record)
            mutated[section][field] = value
            with self.subTest(section=section, field=field, value=value):
                with self.assertRaises(jsonschema.ValidationError):
                    self.validate(mutated)

    def test_post_pilot_reclassification_fails_schema(self):
        record = self.load_record()
        for key in ("first_transition_occurrence", "steady_state_2033_occurrence"):
            mutated = copy.deepcopy(record)
            mutated["post_pilot_corroboration"][key]["classification"] = "PILOT"
            with self.subTest(key=key):
                with self.assertRaises(jsonschema.ValidationError):
                    self.validate(mutated)

    def test_historical_rewrite_mutations_fail_schema(self):
        record = self.load_record()
        mutations = (
            ("eventual_recovery_rewrites_failure", True),
            ("post_pilot_events_reclassified_as_pilot_events", True),
            ("preserve_lateness", False),
            ("preserve_freeze_blocker", False),
            ("preserve_mirror_timeouts", False),
        )
        for field, value in mutations:
            mutated = copy.deepcopy(record)
            mutated["historical_evidence_policy"][field] = value
            with self.subTest(field=field):
                with self.assertRaises(jsonschema.ValidationError):
                    self.validate(mutated)


if __name__ == "__main__":
    unittest.main()
