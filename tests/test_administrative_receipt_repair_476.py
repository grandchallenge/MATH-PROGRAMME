from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_receipts as receipts


CONFIG_PATH = ROOT / "governance" / "administrative_maintenance_automation.json"
REPAIR_PATH = (
    ROOT
    / "governance"
    / "administrative_receipt_repairs"
    / "MP-ADMIN-RECEIPT-REPAIR-476-001.json"
)
SCHEMA_PATH = ROOT / "schemas" / "administrative_receipt_repair_476.schema.json"
RECORD_PATH = (
    ROOT
    / "governance"
    / "administrative_reviews"
    / "MP-ADMIN-ADMINISTRATIVE-REVIEW-2026-08-13-001.json"
)


class AdministrativeReceiptRepair476Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        cls.repair = json.loads(REPAIR_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        protected = subprocess.run(
            ["git", "rev-parse", "origin/main"],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        if protected.returncode != 0:
            protected = subprocess.run(
                ["git", "rev-parse", "HEAD^1"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
        cls.head = protected.stdout.strip()

    def test_repair_record_matches_closed_schema(self) -> None:
        errors = list(
            Draft202012Validator(
                self.schema,
                format_checker=FormatChecker(),
            ).iter_errors(self.repair)
        )
        self.assertEqual([], errors)

    def test_immutable_record_identities_match(self) -> None:
        payload = RECORD_PATH.read_bytes().replace(b"\r\n", b"\n")
        blob = hashlib.sha1(
            f"blob {len(payload)}\0".encode("ascii") + payload
        ).hexdigest()
        self.assertEqual(self.repair["record"]["git_blob"], blob)
        self.assertEqual(
            self.repair["record"]["canonical_sha256"],
            hashlib.sha256(payload).hexdigest(),
        )

    def test_observed_message_remains_classified_malformed(self) -> None:
        message = self.repair["merge"]["message"]
        self.assertIn("Candidate head:", message)
        self.assertIn("Human Steward disposition:", message)
        self.assertNotRegex(message, r"exact head [0-9a-f]{40}")
        self.assertNotRegex(message, r"Disposition:\s*[A-Z0-9_]+")
        self.assertFalse(self.repair["merge"]["message_receipt_parseable"])

    def test_bootstrap_derivation_recovers_only_the_exact_receipt(self) -> None:
        with patch.object(receipts, "git_blob_sha", side_effect=self.index_blob):
            state = receipts.derive_completion_state(ROOT, self.config, self.head)
        administrative = state["procedures"]["administrative_review"]
        matching = [
            item
            for item in administrative["receipts"]
            if item["scheduled_due_at"] == "2026-08-13T01:21:00Z"
        ]
        self.assertEqual(1, len(matching))
        self.assertEqual(476, matching[0]["pull_request"])
        self.assertEqual(
            "7c84b9bf19a1f3e2407860d82965e98fc49512db",
            matching[0]["merge_commit"],
        )
        self.assertEqual(
            "HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            matching[0]["disposition"],
        )

    def test_evidence_mutation_fails_closed(self) -> None:
        mutated = copy.deepcopy(self.config)
        repaired = next(
            item
            for item in mutated["bootstrap_receipts"]
            if item.get("repair_id") == "MP-ADMIN-RECEIPT-REPAIR-476-001"
        )
        repaired["review_id"] = 1
        with patch.object(receipts, "git_blob_sha", side_effect=self.index_blob):
            with self.assertRaises(receipts.aa.AutomationError):
                receipts.derive_completion_state(ROOT, mutated, self.head)

    def test_repair_does_not_create_authority(self) -> None:
        self.assertTrue(
            all(value is False for value in self.repair["authority_boundary"].values())
        )
        self.assertTrue(
            all(value is False for value in self.repair["claim_boundaries"].values())
        )

    @staticmethod
    def index_blob(path: Path) -> str:
        relative = path.relative_to(ROOT).as_posix()
        output = subprocess.run(
            ["git", "ls-files", "--stage", "--", relative],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        return output.split()[1]


if __name__ == "__main__":
    unittest.main()
