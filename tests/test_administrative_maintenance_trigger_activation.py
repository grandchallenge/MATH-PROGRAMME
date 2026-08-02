from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "administrative_maintenance_trigger_registry.json"
SCHEMA_PATH = ROOT / "schemas" / "administrative_maintenance_trigger_registry.schema.json"


class AdministrativeMaintenanceTriggerActivationTests(unittest.TestCase):
    def load_registry(self) -> dict:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def errors_for(self, registry: dict) -> list[str]:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        return [error.message for error in validator.iter_errors(registry)]

    def test_activation_record_is_schema_valid(self) -> None:
        self.assertEqual(self.errors_for(self.load_registry()), [])

    def test_trigger_control_is_protected_and_operational(self) -> None:
        registry = self.load_registry()
        self.assertEqual(registry["status"], "PROTECTED_TRIGGER_CONTROL")
        self.assertTrue(registry["activation"]["operational_on_default_branch"])

    def test_activation_pins_exact_review_and_merge(self) -> None:
        activation = self.load_registry()["activation"]
        self.assertEqual(activation["pull_request"], 203)
        self.assertEqual(
            activation["reviewed_head"],
            "70f8ef8600a4b219ea3915d333105f0c48233e7d",
        )
        self.assertEqual(
            activation["merge_commit"],
            "e941b28dbd2daa8063fcb936dca8a525d1d8d219",
        )
        self.assertEqual(
            activation["workflow_blob"],
            "786a90b4242d43947fbf8fb153f5cc384e77c07d",
        )

    def test_activation_pins_exact_green_runs(self) -> None:
        activation = self.load_registry()["activation"]
        self.assertEqual(activation["dispatcher_run"], 30733399827)
        self.assertEqual(activation["programme_policy_run"], 30733399846)
        self.assertEqual(activation["gcl_conformance_run"], 30733400069)
        self.assertEqual(activation["delegated_review_id"], 4837277963)

    def test_intellect_repin_is_not_inflated(self) -> None:
        activation = self.load_registry()["activation"]
        self.assertFalse(activation["intellect_repin_required"])
        self.assertIn("without changing", activation["intellect_repin_reason"])

    def test_mutation_rejects_candidate_status(self) -> None:
        registry = self.load_registry()
        registry["status"] = "PROPOSED_PROTECTED_TRIGGER_CONTROL"
        self.assertTrue(self.errors_for(registry))

    def test_mutation_rejects_merge_drift(self) -> None:
        registry = self.load_registry()
        registry["activation"]["merge_commit"] = "0" * 40
        self.assertTrue(self.errors_for(registry))

    def test_mutation_rejects_workflow_blob_drift(self) -> None:
        registry = self.load_registry()
        registry["activation"]["workflow_blob"] = "0" * 40
        self.assertTrue(self.errors_for(registry))

    def test_mutation_rejects_false_nonoperational_state(self) -> None:
        registry = self.load_registry()
        registry["activation"]["operational_on_default_branch"] = False
        self.assertTrue(self.errors_for(registry))

    def test_mutation_rejects_unnecessary_intellect_repin(self) -> None:
        registry = copy.deepcopy(self.load_registry())
        registry["activation"]["intellect_repin_required"] = True
        self.assertTrue(self.errors_for(registry))


if __name__ == "__main__":
    unittest.main()
