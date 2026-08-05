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
        cls.terminal_schema = json.loads(validator.TERMINAL_CLOSURE_SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.terminal_record = json.loads(validator.TERMINAL_CLOSURE_PATH.read_text(encoding="utf-8"))
        cls.completion_state = json.loads(validator.COMPLETION_STATE_PATH.read_text(encoding="utf-8"))

    def validate(self, record: dict) -> list[str]:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            schema_path = root / "schema.json"
            record_path = root / "record.json"
            schema_path.write_text(json.dumps(self.schema), encoding="utf-8")
            record_path.write_text(json.dumps(record), encoding="utf-8")
            with patch.object(validator, "ATTESTATION_SCHEMA_PATH", schema_path), patch.object(validator, "ATTESTATION_PATH", record_path):
                return validator.validate_post_merge_attestation()

    def validate_terminal(
        self,
        record: dict,
        completion_state: dict | None = None,
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            terminal_schema_path = root / "terminal-schema.json"
            terminal_record_path = root / "terminal-record.json"
            completion_path = root / "completion.json"
            terminal_schema_path.write_text(json.dumps(self.terminal_schema), encoding="utf-8")
            terminal_record_path.write_text(json.dumps(record), encoding="utf-8")
            completion_path.write_text(json.dumps(self.completion_state if completion_state is None else completion_state), encoding="utf-8")
            with (
                patch.object(validator, "TERMINAL_CLOSURE_SCHEMA_PATH", terminal_schema_path),
                patch.object(validator, "TERMINAL_CLOSURE_PATH", terminal_record_path),
                patch.object(validator, "COMPLETION_STATE_PATH", completion_path),
            ):
                return validator.validate_terminal_closure()

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

    def test_terminal_closure_valid(self) -> None:
        self.assertEqual(self.validate_terminal(copy.deepcopy(self.terminal_record)), [])

    def test_terminal_completion_must_be_true(self) -> None:
        value = copy.deepcopy(self.terminal_record)
        value["protected_completion_declared"] = False
        self.assertTrue(self.validate_terminal(value))

    def test_terminal_successor_pr_rejected(self) -> None:
        value = copy.deepcopy(self.terminal_record)
        value["post_merge_evidence"]["completion_state_pull_request"] = 236
        value["post_merge_evidence"]["open_successor_completion_state_prs"] = 1
        self.assertTrue(self.validate_terminal(value))

    def test_terminal_mirror_drift_rejected(self) -> None:
        value = copy.deepcopy(self.terminal_record)
        value["post_merge_evidence"]["mirrors_current"] = False
        self.assertTrue(self.validate_terminal(value))

    def test_terminal_artifact_identity_drift_rejected(self) -> None:
        value = copy.deepcopy(self.terminal_record)
        value["post_merge_evidence"]["synchronization_artifact_digest"] = "sha256:" + "0" * 64
        self.assertTrue(self.validate_terminal(value))

    def test_terminal_historical_blob_drift_rejected(self) -> None:
        value = copy.deepcopy(self.terminal_record)
        value["historical_attestation"]["blob_sha"] = "0" * 40
        self.assertTrue(self.validate_terminal(value))

    def test_terminal_completion_derivation_drift_rejected(self) -> None:
        completion = copy.deepcopy(self.completion_state)
        completion["derived_from_protected_head"] = "0" * 40
        self.assertTrue(self.validate_terminal(copy.deepcopy(self.terminal_record), completion_state=completion))


if __name__ == "__main__":
    unittest.main()
