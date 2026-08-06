from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
ATTESTATION = ROOT / "governance" / "administrative_autonomy_first_live_run.json"
SCHEMA = ROOT / "schemas" / "administrative_autonomy_first_live_run.schema.json"
COMPLETION = ROOT / "governance" / "administrative_maintenance_completion_state.json"


class AdministrativeAutonomyFirstLiveRunTests(unittest.TestCase):
    def setUp(self) -> None:
        self.attestation = json.loads(ATTESTATION.read_text(encoding="utf-8"))
        self.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.completion = json.loads(COMPLETION.read_text(encoding="utf-8"))

    def test_attestation_schema_is_closed(self) -> None:
        validator = Draft202012Validator(
            self.schema, format_checker=FormatChecker()
        )
        self.assertEqual([], list(validator.iter_errors(self.attestation)))

    def test_first_live_receipt_is_exact(self) -> None:
        receipts = self.completion["procedures"]["structural_sweep"]["receipts"]
        target = [item for item in receipts if item["pull_request"] == 263]
        self.assertEqual(1, len(target))
        receipt = target[0]
        protected = self.attestation["protected_receipts"]
        self.assertEqual(protected["protected_merge_commit"], receipt["merge_commit"])
        self.assertEqual(protected["exact_finalized_head"], receipt["reviewed_head"])
        self.assertEqual(
            "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            receipt["disposition"],
        )

    def test_historical_failures_are_preserved(self) -> None:
        evidence = self.attestation["runtime_evidence"]
        self.assertFalse(evidence["original_terminal_readback_complete"])
        self.assertTrue(evidence["successful_record_merge_preserved"])
        self.assertEqual([5206932513, 5207148968], evidence["preserved_failure_comments"])

    def test_claim_inflation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.attestation)
        mutated["claim_boundaries"]["mathematical_target_proved"] = True
        validator = Draft202012Validator(
            self.schema, format_checker=FormatChecker()
        )
        self.assertTrue(list(validator.iter_errors(mutated)))


if __name__ == "__main__":
    unittest.main()

# Exact-head CI exercises this file through repository unit-test discovery.
