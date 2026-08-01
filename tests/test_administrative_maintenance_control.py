from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

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


def test_candidate_control_is_valid() -> None:
    assert errors_for(load_control()) == []


def test_cli_validator_accepts_repository_files() -> None:
    assert VALIDATOR.validate(CONTROL_PATH, SCHEMA_PATH) == []


def test_mutation_rejects_issue_authority_inflation() -> None:
    control = load_control()
    control["core_clarity_invariants"]["mutable_issues_are_navigation_only"] = False
    assert errors_for(control)


def test_mutation_rejects_ceremonial_repin_policy() -> None:
    control = load_control()
    control["core_clarity_invariants"]["unchanged_material_artifacts_do_not_require_repin"] = False
    assert errors_for(control)


def test_mutation_rejects_candidate_activation() -> None:
    control = load_control()
    control["effective"] = True
    assert errors_for(control)


def test_mutation_rejects_premature_council_resolution() -> None:
    control = load_control()
    control["council_decisions"]["D1"] = "APPROVE"
    assert errors_for(control)


def test_mutation_rejects_premature_promotion() -> None:
    control = load_control()
    control["promotion_gate"]["may_promote_now"] = True
    assert errors_for(control)


def test_mutation_rejects_missing_repository_role() -> None:
    control = load_control()
    del control["repository_roles"]["mathcert"]
    assert errors_for(control)


def test_mutation_rejects_incomplete_workflow_capabilities() -> None:
    control = load_control()
    control["workflow_coverage_requirements"]["required_capabilities"].remove("adversarial mutation tests")
    assert errors_for(control)


def test_mutation_rejects_yaml_only_coverage() -> None:
    control = load_control()
    control["workflow_coverage_requirements"]["yaml_presence_alone_is_sufficient"] = True
    assert errors_for(control)


def test_mutation_rejects_tracker_authority() -> None:
    control = load_control()
    control["tracker_hygiene"]["tracker_can_create_authority"] = True
    assert errors_for(control)


def test_mutation_rejects_stale_tracker_override() -> None:
    control = load_control()
    control["tracker_hygiene"]["stale_tracker_overrides_protected_state"] = True
    assert errors_for(control)


def test_mutation_rejects_uncertain_change_without_fail_closed_escalation() -> None:
    control = load_control()
    control["material_change_classification"]["uncertain_classification_disposition"] = "ALLOW"
    assert errors_for(control)


def test_mutation_rejects_claim_promotion_by_waiver() -> None:
    control = load_control()
    control["waiver_policy"]["claim_promotion_by_waiver_allowed"] = True
    assert errors_for(control)


def test_mutation_rejects_binding_undecided_waiver_policy() -> None:
    control = load_control()
    control["waiver_policy"]["binding"] = True
    assert errors_for(control)


def test_mutation_rejects_emergency_claim_promotion() -> None:
    control = load_control()
    control["emergency_override_policy"]["prohibited_actions"].remove("claim promotion")
    assert errors_for(control)


def test_mutation_rejects_nonexpiring_emergency_override() -> None:
    control = load_control()
    control["emergency_override_policy"]["automatic_expiry_required"] = False
    assert errors_for(control)


def test_mutation_rejects_binding_gcl_tcs_before_g8_g9() -> None:
    control = load_control()
    control["communication_profile"]["gcl_tcs_00_binding"] = True
    assert errors_for(control)


def test_mutation_rejects_mathematical_claim_inflation() -> None:
    control = load_control()
    control["claim_boundaries"]["mathematical_target_proved"] = True
    assert errors_for(control)


@pytest.mark.parametrize("decision", [f"D{i}" for i in range(1, 9)])
def test_all_council_decisions_are_explicit_and_pending(decision: str) -> None:
    control = load_control()
    assert control["council_decisions"][decision] == "PENDING"
