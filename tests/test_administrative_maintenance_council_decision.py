from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DECISION_PATH = ROOT / "governance" / "administrative_maintenance_council_decision.json"
SCHEMA_PATH = ROOT / "schemas" / "administrative_maintenance_council_decision.schema.json"


class AdministrativeMaintenanceCouncilDecisionTests(unittest.TestCase):
    def load_decision(self) -> dict:
        return json.loads(DECISION_PATH.read_text(encoding="utf-8"))

    def errors_for(self, decision: dict) -> list[str]:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        return [error.message for error in validator.iter_errors(decision)]

    def test_binding_decision_is_schema_valid(self) -> None:
        self.assertEqual(self.errors_for(self.load_decision()), [])

    def test_acceleration_factor_is_exact(self) -> None:
        decision = self.load_decision()
        self.assertEqual(decision["acceleration"]["factor"], 0.1)
        self.assertTrue(decision["acceleration"]["event_triggered_obligations_remain_immediate"])
        self.assertEqual(decision["pilot"]["duration"], "P9D")

    def test_all_decisions_are_resolved(self) -> None:
        decision = self.load_decision()
        self.assertEqual(set(decision["decisions"]), {f"D{i}" for i in range(1, 9)})
        self.assertNotIn("PENDING", {item["disposition"] for item in decision["decisions"].values()})

    def test_intellect_buy_in_is_mandatory(self) -> None:
        decision = self.load_decision()
        self.assertTrue(decision["intellect_requirement"]["buy_in_required"])
        self.assertTrue(decision["intellect_requirement"]["required_before_final_closure"])

    def test_mutation_rejects_ninety_day_pilot(self) -> None:
        decision = self.load_decision()
        decision["pilot"]["duration"] = "P90D"
        self.assertTrue(self.errors_for(decision))

    def test_mutation_rejects_unaccelerated_factor(self) -> None:
        decision = self.load_decision()
        decision["acceleration"]["factor"] = 1.0
        self.assertTrue(self.errors_for(decision))

    def test_mutation_rejects_pending_decision(self) -> None:
        decision = self.load_decision()
        decision["decisions"]["D1"]["disposition"] = "PENDING"
        self.assertTrue(self.errors_for(decision))

    def test_mutation_rejects_claim_inflation(self) -> None:
        decision = self.load_decision()
        decision["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(self.errors_for(decision))


if __name__ == "__main__":
    unittest.main()
