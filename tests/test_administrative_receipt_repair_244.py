from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_automation as aa
import administrative_receipts as receipts

HEAD = "f" * 40
REVIEWED = "3a5977c2d13d8ece9365dcda356d089e7baefd8e"
MERGE = "ba89cf1cc253486a70ea832c2db8fca9e81f4a9f"
BASE = "6dd51c29b8bcbac812bcf7a4e803b693ac8be69c"
BLOB = "51db3bc72c8f371ace530ad5ce11322cd6af326c"
MESSAGE = (
    "Merge pull request #244 from grandchallenge/automation/maintenance/"
    "structural_sweep-20260805T225700Z\n\n"
    "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007: record contemporaneous sweep"
)


def repair_record() -> dict:
    return {
        "schema_version": "1.0.0",
        "repair_id": "MP-ADMIN-RECEIPT-REPAIR-244-001",
        "control_id": "MP-ADMIN-MAINT-001",
        "repository": "grandchallenge/MATH-PROGRAMME",
        "source_issue": 249,
        "tracking_issue": 243,
        "procedure_id": "structural_sweep",
        "occurrence_key": "structural_sweep:2026-08-05T22:57:00Z",
        "scheduled_due_at": "2026-08-05T22:57:00Z",
        "record": {
            "path": "governance/administrative_structural_sweeps/MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007.json",
            "git_blob": BLOB,
            "sweep_id": "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007",
            "status": "COMPLETE_WITH_REPAIRED_P2_AND_NONBLOCKING_OPEN_PR",
        },
        "pull_request": {
            "number": 244,
            "base": BASE,
            "head": REVIEWED,
            "approval": {
                "review_id": 4869603629,
                "reviewer": "jimsteeg",
                "state": "APPROVED",
                "submitted_at": "2026-08-05T23:21:12Z",
                "exact_head": REVIEWED,
            },
            "disposition": {
                "comment_id": 5198515780,
                "actor": "fyremael",
                "posted_at": "2026-08-05T23:23:05Z",
                "exact_head": REVIEWED,
                "token": "HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            },
        },
        "merge": {
            "commit": MERGE,
            "committed_at": "2026-08-05T23:23:25Z",
            "parents": [BASE, REVIEWED],
            "message": MESSAGE,
            "message_receipt_parseable": False,
            "signature_verified": True,
        },
        "failure_evidence": {
            "completion_registry_advanced": False,
            "tracking_issue_closed": False,
        },
        "bootstrap": {
            "record_sha256_mode": "DERIVE_FROM_IMMUTABLE_RECORD",
            "receipt_state": "PROTECTED_COMPLETE",
            "protected_completion_declared_before_repair_merge": False,
        },
        "authority_boundary": {"protected_main_rewritten": False},
        "claim_boundaries": {"mathematical_target_proved": False},
    }


def bootstrap_receipt() -> dict:
    return {
        "repair_id": "MP-ADMIN-RECEIPT-REPAIR-244-001",
        "repair_record_path": "governance/administrative_receipt_repairs/MP-ADMIN-RECEIPT-REPAIR-244-001.json",
        "procedure_id": "structural_sweep",
        "scheduled_due_at": "2026-08-05T22:57:00Z",
        "record_path": "governance/administrative_structural_sweeps/MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007.json",
        "record_sha256": "DERIVE_FROM_IMMUTABLE_RECORD",
        "record_git_blob": BLOB,
        "merge_commit": MERGE,
        "merge_parents": [BASE, REVIEWED],
        "reviewed_head": REVIEWED,
        "pull_request": 244,
        "review_id": 4869603629,
        "review_state": "APPROVED",
        "review_submitted_at": "2026-08-05T23:21:12Z",
        "disposition_comment_id": 5198515780,
        "disposition_posted_at": "2026-08-05T23:23:05Z",
        "merge_committed_at": "2026-08-05T23:23:25Z",
        "disposition": "HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
        "receipt_state": "PROTECTED_COMPLETE",
    }


class ReceiptRepair244Tests(unittest.TestCase):
    def test_repository_repair_record_matches_schema(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "administrative_receipt_repair_244.schema.json").read_text(encoding="utf-8")
        )
        record = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_receipt_repairs"
                / "MP-ADMIN-RECEIPT-REPAIR-244-001.json"
            ).read_text(encoding="utf-8")
        )
        errors = list(
            Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(record)
        )
        self.assertEqual(errors, [])

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        repair_path = (
            self.root
            / "governance"
            / "administrative_receipt_repairs"
            / "MP-ADMIN-RECEIPT-REPAIR-244-001.json"
        )
        repair_path.parent.mkdir(parents=True)
        repair_path.write_text(json.dumps(repair_record()), encoding="utf-8")
        record_path = (
            self.root
            / "governance"
            / "administrative_structural_sweeps"
            / "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007.json"
        )
        record_path.parent.mkdir(parents=True)
        record_path.write_text('{"status":"COMPLETE_WITH_REPAIRED_P2_AND_NONBLOCKING_OPEN_PR"}\n', encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def runner(self, args: list[str]) -> str:
        if args[0] == "log":
            return MERGE
        if "--format=%P" in args:
            return f"{BASE} {REVIEWED}"
        if "--format=%B" in args:
            return MESSAGE
        if "--format=%cI" in args:
            return "2026-08-05T16:23:25-07:00"
        raise AssertionError(args)

    def write_repair(self, value: dict) -> None:
        path = (
            self.root
            / "governance"
            / "administrative_receipt_repairs"
            / "MP-ADMIN-RECEIPT-REPAIR-244-001.json"
        )
        path.write_text(json.dumps(value), encoding="utf-8")

    def normalize(self, receipt: dict | None = None) -> dict:
        with (
            patch("administrative_receipts.git_blob_sha", return_value=BLOB),
            patch("administrative_receipts.protected_ancestor", return_value=True),
        ):
            return receipts.normalize_repaired_bootstrap_receipt(
                self.root,
                receipt or bootstrap_receipt(),
                HEAD,
                self.runner,
            )

    def test_valid_repair_materializes_normal_receipt(self) -> None:
        item = self.normalize()
        self.assertEqual(item["pull_request"], 244)
        self.assertEqual(item["reviewed_head"], REVIEWED)
        self.assertEqual(item["merge_commit"], MERGE)
        self.assertEqual(len(item["record_sha256"]), 64)
        self.assertEqual(item["receipt_state"], "PROTECTED_COMPLETE")

    def test_altered_pr_rejected(self) -> None:
        value = bootstrap_receipt(); value["pull_request"] = 245
        with self.assertRaises(aa.AutomationError): self.normalize(value)

    def test_altered_head_rejected(self) -> None:
        value = bootstrap_receipt(); value["reviewed_head"] = "a" * 40
        with self.assertRaises(aa.AutomationError): self.normalize(value)

    def test_altered_merge_rejected(self) -> None:
        value = bootstrap_receipt(); value["merge_commit"] = "b" * 40
        with self.assertRaises(aa.AutomationError): self.normalize(value)

    def test_parent_order_rejected(self) -> None:
        value = bootstrap_receipt(); value["merge_parents"] = [REVIEWED, BASE]
        with self.assertRaises(aa.AutomationError): self.normalize(value)

    def test_altered_review_rejected(self) -> None:
        value = bootstrap_receipt(); value["review_id"] += 1
        with self.assertRaises(aa.AutomationError): self.normalize(value)

    def test_nonapproved_review_rejected(self) -> None:
        value = repair_record(); value["pull_request"]["approval"]["state"] = "COMMENTED"; self.write_repair(value)
        with self.assertRaises(aa.AutomationError): self.normalize()

    def test_altered_disposition_rejected(self) -> None:
        value = bootstrap_receipt(); value["disposition"] = "RETROSPECTIVE_ONLY"
        with self.assertRaises(aa.AutomationError): self.normalize(value)

    def test_altered_record_blob_rejected(self) -> None:
        value = bootstrap_receipt(); value["record_git_blob"] = "c" * 40
        with self.assertRaises(aa.AutomationError): self.normalize(value)

    def test_post_merge_disposition_timing_rejected(self) -> None:
        value = repair_record(); value["pull_request"]["disposition"]["posted_at"] = "2026-08-05T23:23:26Z"; self.write_repair(value)
        with self.assertRaises(aa.AutomationError): self.normalize()

    def test_parseable_historical_message_rejected(self) -> None:
        value = repair_record()
        value["merge"]["message"] = (
            f"Merge PR #244 at exact head {REVIEWED}\n\n"
            "Disposition: HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE"
        )
        self.write_repair(value)
        with self.assertRaises(aa.AutomationError): self.normalize()

    def test_nonancestral_merge_rejected(self) -> None:
        with (
            patch("administrative_receipts.git_blob_sha", return_value=BLOB),
            patch("administrative_receipts.protected_ancestor", return_value=False),
        ):
            with self.assertRaises(aa.AutomationError):
                receipts.normalize_repaired_bootstrap_receipt(
                    self.root, bootstrap_receipt(), HEAD, self.runner
                )

    def test_bootstrap_coverage_skips_malformed_direct_receipt(self) -> None:
        config = {
            "bootstrap_receipts": [bootstrap_receipt()],
            "procedures": {
                "structural_sweep": {
                    "record_globs": ["governance/administrative_structural_sweeps/*.json"],
                    "due_fields": ["scheduled_due_at"],
                    "receipt_floor_utc": "2026-08-05T00:00:00Z",
                }
            },
        }
        record_path = (
            self.root
            / "governance"
            / "administrative_structural_sweeps"
            / "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007.json"
        )
        record_path.write_text(
            json.dumps({
                "status": "COMPLETE_WITH_REPAIRED_P2_AND_NONBLOCKING_OPEN_PR",
                "scheduled_due_at": "2026-08-05T22:57:00Z",
            }),
            encoding="utf-8",
        )
        with (
            patch("administrative_receipts.git_blob_sha", return_value=BLOB),
            patch("administrative_receipts.protected_ancestor", return_value=True),
        ):
            state = receipts.derive_completion_state(self.root, config, HEAD, self.runner)
        self.assertEqual(
            state["procedures"]["structural_sweep"]["completed_through_utc"],
            "2026-08-05T22:57:00Z",
        )


if __name__ == "__main__":
    unittest.main()
