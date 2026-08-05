from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import validate_administrative_automation_v3 as validator


class AdministrativeAutomationRemediationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(validator.ATTESTATION_SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.record = json.loads(validator.ATTESTATION_PATH.read_text(encoding="utf-8"))

    def validate(self, record: dict) -> list[str]:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            schema_path = root / "schema.json"
            record_path = root / "record.json"
            schema_path.write_text(json.dumps(self.schema), encoding="utf-8")
            record_path.write_text(json.dumps(record), encoding="utf-8")
            with patch.object(validator, "ATTESTATION_SCHEMA_PATH", schema_path), patch.object(validator, "ATTESTATION_PATH", record_path):
                return validator.validate_post_merge_attestation()

    def test_current_attestation_valid(self) -> None:
        self.assertEqual(self.validate(copy.deepcopy(self.record)), [])

    def test_premerge_disposition_claim_rejected(self) -> None:
        value = copy.deepcopy(self.record)
        value["disposition_preceded_merge"] = True
        self.assertTrue(self.validate(value))

    def test_reviewed_head_drift_rejected(self) -> None:
        value = copy.deepcopy(self.record)
        value["reviewed_head"] = "0" * 40
        self.assertTrue(self.validate(value))

    def test_merge_receipt_drift_rejected(self) -> None:
        value = copy.deepcopy(self.record)
        value["merge_commit"] = "0" * 40
        self.assertTrue(self.validate(value))

    def test_premature_completion_rejected(self) -> None:
        value = copy.deepcopy(self.record)
        value["protected_completion_declared"] = True
        self.assertTrue(self.validate(value))

    def test_missing_failure_identity_rejected(self) -> None:
        value = copy.deepcopy(self.record)
        value["failure_detail"] = "credential unavailable"
        self.assertTrue(self.validate(value))


if __name__ == "__main__":
    unittest.main()
