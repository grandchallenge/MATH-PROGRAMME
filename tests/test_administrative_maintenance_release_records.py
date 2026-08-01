from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]


class AdministrativeMaintenanceReleaseRecordTests(unittest.TestCase):
    def validate(self, document_name: str, schema_name: str) -> tuple[dict, list[str]]:
        document = json.loads((ROOT / "governance" / document_name).read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        return document, [error.message for error in validator.iter_errors(document)]

    def test_artifact_ledger_is_valid_and_ready_for_programme_merge(self) -> None:
        ledger, errors = self.validate(
            "administrative_maintenance_artifact_ledger.json",
            "administrative_maintenance_artifact_ledger.schema.json",
        )
        self.assertEqual(errors, [])
        self.assertEqual(ledger["status"], "READY_FOR_PROTECTED_PROGRAMME_MERGE")
        records = {item["artifact_id"]: item for item in ledger["artifacts"]}
        self.assertEqual(records["MP-ADMIN-REFEREE-001"]["status"], "APPROVED_FOR_PROGRAMME_MERGE")
        self.assertEqual(
            records["GI-ADMIN-MAINT-001"]["status"],
            "PHASE_A_COMMITTED_PENDING_PROTECTED_PIN",
        )

    def test_human_steward_release_is_valid_and_accelerated(self) -> None:
        release, errors = self.validate(
            "administrative_maintenance_steward_release.json",
            "administrative_maintenance_steward_release.schema.json",
        )
        self.assertEqual(errors, [])
        self.assertEqual(release["human_steward"], "fyremael")
        self.assertEqual(release["timing_correction"]["factor"], 0.1)
        self.assertEqual(release["timing_correction"]["pilot_duration"], "P9D")
        self.assertTrue(
            release["timing_correction"]["event_triggered_obligations_remain_immediate"]
        )

    def test_release_records_preserve_claim_boundaries(self) -> None:
        ledger, _ = self.validate(
            "administrative_maintenance_artifact_ledger.json",
            "administrative_maintenance_artifact_ledger.schema.json",
        )
        release, _ = self.validate(
            "administrative_maintenance_steward_release.json",
            "administrative_maintenance_steward_release.schema.json",
        )
        self.assertTrue(all(value is False for value in ledger["claim_boundaries"].values()))
        self.assertTrue(all(value is False for value in release["claim_boundaries"].values()))


if __name__ == "__main__":
    unittest.main()
