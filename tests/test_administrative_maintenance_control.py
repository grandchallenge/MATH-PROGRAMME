from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_PATH = ROOT / "governance" / "administrative_maintenance_control.json"
SCHEMA_PATH = ROOT / "schemas" / "administrative_maintenance_control.schema.json"
VALIDATOR_PATH = ROOT / "ci" / "validate_administrative_maintenance_control.py"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("administrative_maintenance_validator", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATOR = load_validator_module()


def load_control() -> dict:
    return json.loads(CONTROL_PATH.read_text(encoding="utf-8"))


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def errors_for(control: dict) -> list[str]:
    return VALIDATOR.schema_errors(control, load_schema()) + VALIDATOR.semantic_errors(control)


class AdministrativeMaintenanceControlTests(unittest.TestCase):
    def test_accelerated_control_is_valid(self) -> None:
        self.assertEqual(errors_for(load_control()), [])

    def test_cli_validator_accepts_repository_files(self) -> None:
        self.assertEqual(VALIDATOR.validate(CONTROL_PATH, SCHEMA_PATH), [])

    def test_human_steward_decision_is_resolved(self) -> None:
        control = load_control()
        self.assertEqual(control["status"], "APPROVED_ACCELERATED_PILOT")
        self.assertTrue(control["effective"])
        self.assertEqual(control["activation"], "PROTECTED_MERGE_ONLY")
        self.assertTrue(control["promotion_gate"]["council_decisions_resolved"])
        self.assertTrue(control["promotion_gate"]["human_steward_release_complete"])

    def test_all_durations_are_accelerated(self) -> None:
        control = load_control()
        self.assertEqual(control["acceleration"]["factor"], 0.1)
        self.assertEqual(control["acceleration"]["pilot_duration"], "P9D")
        self.assertEqual(control["control_loops"]["structural_sweep"]["cadence"], "PT16H48M")
        self.assertEqual(control["control_loops"]["administrative_portfolio_review"]["cadence"], "P3D")
        self.assertEqual(control["control_loops"]["deep_conformance_review"]["cadence"], "P9D")
        self.assertEqual(control["control_loops"]["constitutional_review"]["cadence"], "P36DT12H")
        self.assertEqual(control["tracker_hygiene"]["refresh_target"], "PT7H12M")
        self.assertEqual(control["waiver_policy"]["steward_local_administrative_limit"], "P3D")
        self.assertEqual(control["emergency_override_policy"]["maximum_duration"], "PT7H12M")
        self.assertEqual(control["emergency_override_policy"]["steward_review_deadline"], "PT2H24M")
        self.assertEqual(control["emergency_override_policy"]["council_and_referee_retrospective_deadline"], "PT16H48M")

    def test_event_triggered_sync_remains_immediate(self) -> None:
        control = load_control()
        event_loop = control["control_loops"]["event_triggered_synchronization"]
        self.assertTrue(event_loop["binding"])
        self.assertEqual(event_loop["cadence"], "IMMEDIATE_ON_MATERIAL_CHANGE")
        self.assertTrue(control["acceleration"]["event_triggered_obligations_remain_immediate"])

    def test_intellect_buy_in_is_required(self) -> None:
        control = load_control()
        self.assertTrue(control["intellect_buy_in"]["required"])
        self.assertTrue(control["intellect_buy_in"]["exact_protected_pin_required_after_programme_merge"])
        self.assertFalse(control["intellect_buy_in"]["final_closure_allowed_without_intellect_protected_adoption"])

    def test_mutation_rejects_issue_authority_inflation(self) -> None:
        control = load_control()
        control["core_clarity_invariants"]["mutable_issues_are_navigation_only"] = False
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_ceremonial_repin_policy(self) -> None:
        control = load_control()
        control["core_clarity_invariants"]["unchanged_material_artifacts_do_not_require_repin"] = False
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_unaccelerated_pilot(self) -> None:
        control = load_control()
        control["acceleration"]["pilot_duration"] = "P90D"
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_unaccelerated_structural_sweep(self) -> None:
        control = load_control()
        control["control_loops"]["structural_sweep"]["cadence"] = "P7D"
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_delayed_material_sync(self) -> None:
        control = load_control()
        control["control_loops"]["event_triggered_synchronization"]["cadence"] = "P3D"
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_unresolved_council_decision(self) -> None:
        control = load_control()
        control["council_decisions"]["D1"] = "PENDING"
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_missing_repository_role(self) -> None:
        control = load_control()
        del control["repository_roles"]["intellect"]
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_incomplete_workflow_capabilities(self) -> None:
        control = load_control()
        control["workflow_coverage_requirements"]["required_capabilities"].remove("adversarial mutation tests")
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_yaml_only_coverage(self) -> None:
        control = load_control()
        control["workflow_coverage_requirements"]["yaml_presence_alone_is_sufficient"] = True
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_tracker_authority(self) -> None:
        control = load_control()
        control["tracker_hygiene"]["tracker_can_create_authority"] = True
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_unaccelerated_tracker_clock(self) -> None:
        control = load_control()
        control["tracker_hygiene"]["refresh_target"] = "PT72H"
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_uncertain_change_without_fail_closed_escalation(self) -> None:
        control = load_control()
        control["material_change_classification"]["uncertain_classification_disposition"] = "ALLOW"
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_claim_promotion_by_waiver(self) -> None:
        control = load_control()
        control["waiver_policy"]["claim_promotion_by_waiver_allowed"] = True
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_critical_waiver_delegation(self) -> None:
        control = load_control()
        control["waiver_policy"]["council_required_for"].remove("required-check waiver")
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_emergency_claim_promotion(self) -> None:
        control = load_control()
        control["emergency_override_policy"]["prohibited_actions"].remove("claim promotion")
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_unaccelerated_emergency_override(self) -> None:
        control = load_control()
        control["emergency_override_policy"]["maximum_duration"] = "PT72H"
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_binding_gcl_tcs_before_g8_g9(self) -> None:
        control = load_control()
        control["communication_profile"]["gcl_tcs_00_binding"] = True
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_premature_programme_merge_gate(self) -> None:
        control = load_control()
        control["promotion_gate"]["may_merge_programme_control"] = True
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_premature_final_closure(self) -> None:
        control = load_control()
        control["promotion_gate"]["final_cross_repository_closure_complete"] = True
        self.assertTrue(errors_for(control))

    def test_mutation_rejects_mathematical_claim_inflation(self) -> None:
        control = load_control()
        control["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(errors_for(control))


if __name__ == "__main__":
    unittest.main()
