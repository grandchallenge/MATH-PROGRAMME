from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
REPAIR_PATH = (
    ROOT
    / "governance"
    / "administrative_receipt_repairs"
    / "MP-ADMIN-RECEIPT-REPAIR-434-001.json"
)
SCHEMA_PATH = ROOT / "schemas" / "administrative_receipt_repair_434.schema.json"
COMPLETION_PATH = ROOT / "governance" / "administrative_maintenance_completion_state.json"
REQUIRED_RECEIPT_MESSAGE = re.compile(
    r"Merge PR #(\d+).*exact head ([0-9a-f]{40}).*Disposition:\s*([A-Z0-9_]+)",
    re.DOTALL,
)


class AdministrativeReceiptRepair434Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repair = json.loads(REPAIR_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.completion = json.loads(COMPLETION_PATH.read_text(encoding="utf-8"))

    def test_repair_record_matches_closed_schema(self) -> None:
        errors = list(
            Draft202012Validator(
                self.schema,
                format_checker=FormatChecker(),
            ).iter_errors(self.repair)
        )
        self.assertEqual([], errors)

    def test_pr_434_message_is_preserved_as_malformed(self) -> None:
        malformed = self.repair["malformed_receipt"]
        self.assertIsNone(REQUIRED_RECEIPT_MESSAGE.fullmatch(malformed["merge_message"]))
        self.assertEqual([], malformed["independent_non_author_reviews"])
        self.assertIsNone(malformed["exact_head_disposition_comment_id"])
        self.assertIsNone(malformed["receipt_parser_fields"]["exact_head"])
        self.assertIsNone(malformed["receipt_parser_fields"]["disposition"])

    def test_underlying_protected_record_is_not_rewritten_or_invalidated(self) -> None:
        record = self.repair["underlying_record"]
        authority = self.repair["authority_boundary"]
        self.assertTrue(record["protected_record_preserved"])
        self.assertFalse(record["underlying_record_invalidated"])
        self.assertFalse(authority["protected_main_rewritten"])
        self.assertFalse(authority["retrospective_authority_created"])

    def test_repair_binds_exact_current_completion_entry(self) -> None:
        structural = self.completion["procedures"]["structural_sweep"]
        binding = self.repair["completion_ledger_binding"]
        matching = [
            item
            for item in structural["receipts"]
            if item["scheduled_due_at"] == self.repair["scheduled_due_at"]
        ]
        self.assertEqual(1, len(matching))
        receipt = matching[0]
        self.assertEqual(binding["completed_through_utc"], structural["completed_through_utc"])
        self.assertEqual(binding["receipt_count"], structural["receipt_count"])
        self.assertEqual(binding["record_path"], receipt["record_path"])
        self.assertEqual(binding["record_sha256"], receipt["record_sha256"])
        self.assertEqual(binding["record_merge_commit"], receipt["merge_commit"])
        self.assertEqual(binding["record_exact_head"], receipt["reviewed_head"])
        self.assertEqual(binding["record_pull_request"], receipt["pull_request"])
        self.assertEqual(binding["receipt_state"], receipt["receipt_state"])

    def test_repair_remains_fail_closed_until_fresh_human_gates(self) -> None:
        contract = self.repair["repair_contract"]
        authority = self.repair["authority_boundary"]
        for gate in (
            "effective_only_after_protected_repair_merge",
            "independent_non_author_exact_head_approval_required",
            "human_steward_exact_head_disposition_required",
            "required_checks_at_unchanged_head_required",
            "expected_head_protected_merge_required",
            "protected_main_readback_required",
            "head_mutation_invalidates_prior_review",
        ):
            self.assertTrue(contract[gate], gate)
        self.assertTrue(all(value is False for value in authority.values()))
        self.assertTrue(
            all(value is False for value in self.repair["claim_boundaries"].values())
        )


if __name__ == "__main__":
    unittest.main()
