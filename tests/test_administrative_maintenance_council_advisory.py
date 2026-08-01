from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ADVISORY_PATH = ROOT / "council" / "advisories" / "MP-ADMIN-MAINT-001.agent_review.yaml"
SCHEMA_PATH = ROOT / "schemas" / "agent_review.schema.json"


class AdministrativeMaintenanceCouncilAdvisoryTests(unittest.TestCase):
    def load_advisory(self) -> dict:
        value = yaml.safe_load(ADVISORY_PATH.read_text(encoding="utf-8"))
        self.assertIsInstance(value, dict)
        return value

    def test_advisory_conforms_to_agent_review_schema(self) -> None:
        advisory = self.load_advisory()
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        errors = [error.message for error in validator.iter_errors(advisory)]
        self.assertEqual(errors, [])

    def test_advisory_does_not_claim_independent_referee_review(self) -> None:
        advisory = self.load_advisory()
        self.assertEqual(advisory["council_review"]["Referee"]["status"], "pending")
        self.assertIn("non-author Referee review is pending", advisory["promotion"]["blockers"])

    def test_advisory_does_not_claim_human_steward_release(self) -> None:
        advisory = self.load_advisory()
        self.assertEqual(advisory["council_review"]["Steward"]["status"], "pending")
        self.assertIn("Human Steward release is pending", advisory["promotion"]["blockers"])

    def test_advisory_remains_blocked(self) -> None:
        advisory = self.load_advisory()
        self.assertEqual(advisory["artifact"]["status"], "blocked")
        self.assertFalse(advisory["promotion"]["ready_for_next_stage"])
        self.assertTrue(any(item["blocking"] for item in advisory["unresolved_obligations"]))

    def test_issue_mirror_correction_is_recorded(self) -> None:
        advisory = self.load_advisory()
        findings = advisory["council_review"]["Cartographer"]["findings"]
        self.assertTrue(any("MP-ADMIN-MIRROR-001" in finding for finding in findings))


if __name__ == "__main__":
    unittest.main()
