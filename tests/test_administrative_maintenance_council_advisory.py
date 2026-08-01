from __future__ import annotations

import json
import unittest
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ADVISORY_PATH = ROOT / "council" / "advisories" / "MP-ADMIN-MAINT-001.agent_review.yaml"
REFEREE_PATH = ROOT / "reviews" / "governance" / "MP-ADMIN-MAINT-001.referee_review.yaml"
SCHEMA_PATH = ROOT / "schemas" / "agent_review.schema.json"


class AdministrativeMaintenanceCouncilAdvisoryTests(unittest.TestCase):
    def load_yaml(self, path: Path) -> dict:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertIsInstance(value, dict)
        return value

    def validate_review(self, review: dict) -> list[str]:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        return [error.message for error in validator.iter_errors(review)]

    def test_advisory_conforms_to_agent_review_schema(self) -> None:
        self.assertEqual(self.validate_review(self.load_yaml(ADVISORY_PATH)), [])

    def test_separate_referee_review_conforms_to_agent_review_schema(self) -> None:
        self.assertEqual(self.validate_review(self.load_yaml(REFEREE_PATH)), [])

    def test_human_steward_release_is_recorded(self) -> None:
        advisory = self.load_yaml(ADVISORY_PATH)
        steward = advisory["council_review"]["Steward"]
        self.assertEqual(steward["status"], "reviewed")
        self.assertEqual(steward["reviewed_by"], "Human Steward fyremael")

    def test_non_author_referee_review_is_complete_and_scoped(self) -> None:
        advisory = self.load_yaml(ADVISORY_PATH)
        referee = advisory["council_review"]["Referee"]
        self.assertEqual(referee["status"], "reviewed")
        self.assertIn("no independent human identity asserted", referee["reviewed_by"])
        referee_record = self.load_yaml(REFEREE_PATH)
        self.assertTrue(referee_record["promotion"]["ready_for_next_stage"])
        self.assertEqual(referee_record["promotion"]["blockers"], [])

    def test_advisory_is_ready_for_programme_merge(self) -> None:
        advisory = self.load_yaml(ADVISORY_PATH)
        self.assertEqual(advisory["artifact"]["status"], "ready_for_next_stage")
        self.assertTrue(advisory["promotion"]["ready_for_next_stage"])
        self.assertEqual(advisory["promotion"]["blockers"], [])
        self.assertFalse(any(item["blocking"] for item in advisory["unresolved_obligations"]))

    def test_intellect_phase_b_remains_final_closure_obligation(self) -> None:
        advisory = self.load_yaml(ADVISORY_PATH)
        obligations = advisory["unresolved_obligations"]
        self.assertTrue(any("INTELLECT Phase B" in item["description"] for item in obligations))
        self.assertTrue(all(item["blocking"] is False for item in obligations))

    def test_accelerated_timing_and_terminology_are_recorded(self) -> None:
        advisory = self.load_yaml(ADVISORY_PATH)
        self.assertIn(
            "Accelerated maintenance time scale",
            advisory["amanuensis_control"]["terminology_registry"]["terms_introduced_or_changed"],
        )
        findings = advisory["council_review"]["Formalist"]["findings"]
        self.assertTrue(any("0.1" in finding for finding in findings))


if __name__ == "__main__":
    unittest.main()
