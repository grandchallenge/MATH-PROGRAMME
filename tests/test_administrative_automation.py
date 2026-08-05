from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_automation as aa
import synchronize_administrative_completion as sync
import validate_administrative_automation as validator

UTC = timezone.utc
HEAD = "a" * 40
MERGE = "b" * 40
REVIEWED = "c" * 40
NAMES = ("structural_sweep", "administrative_review", "deep_conformance_review", "pilot_review", "constitutional_review")


def config_fixture() -> dict:
    return {
        "schema_version": "1.0.0",
        "control_id": "MP-ADMIN-MAINT-001",
        "repository": "grandchallenge/MATH-PROGRAMME",
        "evidence_repositories": ["grandchallenge/MATH-PROGRAMME", "grandchallenge/MATHFORGE", "grandchallenge/MATHSOLVE", "grandchallenge/MATHCERT", "grandchallenge/INTELLECT"],
        "procedures": {
            name: {
                "lead_minutes": 360 if name == "structural_sweep" else 720,
                "freeze_minutes": 90,
                "record_globs": [f"governance/{name}/*.json"],
                "due_fields": ["scheduled_due_at"],
                "receipt_floor_utc": "2026-08-01T00:00:00Z",
            }
            for name in NAMES
        },
        "authority_boundary": {
            "automated_approval": False,
            "automated_human_steward_disposition": False,
            "automated_merge": False,
            "automated_auto_merge": False,
            "branch_protection_bypass": False,
        },
    }


def registry_fixture() -> dict:
    return {
        "procedures": [
            {
                "id": name,
                "first_due_utc": "2026-08-05T22:57:00Z" if name == "structural_sweep" else "2026-08-10T01:21:00Z",
                "active_through_utc": "2026-09-10T01:21:00Z",
                "interval_minutes": 1008 if name == "structural_sweep" else None,
                "completed_through_utc": None,
                "required_output": "protected record",
                "issue_class": "P2_IF_LATE",
            }
            for name in NAMES
        ]
    }


def empty_completion() -> dict:
    return {
        "schema_version": "1.0.0",
        "control_id": "MP-ADMIN-MAINT-001",
        "derived_from_protected_head": HEAD,
        "state": "PROTECTED_RECEIPT_DERIVED",
        "procedures": {name: {"completed_through_utc": None, "receipt_count": 0, "receipts": []} for name in NAMES},
        "authority_boundary": {
            "issues_are_authority": False,
            "workflow_artifacts_are_authority": False,
            "draft_pull_requests_are_authority": False,
            "unmerged_branches_are_authority": False,
            "protected_merge_receipts_required": True,
        },
    }


def repo_state() -> list[dict]:
    return [
        {"repository": repository, "default_branch": "main", "protected_head": str(index) * 40, "open_pull_requests": []}
        for index, repository in enumerate(config_fixture()["evidence_repositories"], start=1)
    ]


def receipt() -> dict:
    return {
        "procedure_id": "structural_sweep",
        "scheduled_due_at": "2026-08-05T22:57:00Z",
        "record_path": "governance/record.json",
        "record_sha256": "e" * 64,
        "merge_commit": MERGE,
        "reviewed_head": REVIEWED,
        "pull_request": 230,
        "disposition": "HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
        "receipt_state": "PROTECTED_COMPLETE",
    }


class AdministrativeAutomationTests(unittest.TestCase):
    def occurrence(self) -> aa.Occurrence:
        return aa.build_occurrence(config_fixture(), "structural_sweep", aa.parse_datetime("2026-08-05T22:57:00Z"))

    def manifest(self) -> dict:
        return aa.build_candidate_manifest(self.occurrence(), aa.parse_datetime("2026-08-05T17:00:00Z"), HEAD, repo_state())

    def test_config_valid(self) -> None:
        self.assertEqual(aa.validate_config(config_fixture()), [])

    def test_duplicate_repository_rejected(self) -> None:
        value = config_fixture(); value["evidence_repositories"][4] = value["evidence_repositories"][0]
        self.assertTrue(aa.validate_config(value))

    def test_freeze_drift_rejected(self) -> None:
        value = config_fixture(); value["procedures"]["structural_sweep"]["freeze_minutes"] = 360
        self.assertTrue(aa.validate_config(value))

    def test_occurrence_key_stable(self) -> None:
        self.assertEqual(aa.occurrence_key("structural_sweep", aa.parse_datetime("2026-08-05T15:57:00-07:00")), "structural_sweep:2026-08-05T22:57:00Z")

    def test_unsafe_procedure_rejected(self) -> None:
        with self.assertRaises(aa.AutomationError): aa.occurrence_key("../merge", datetime.now(UTC))

    def test_preparation_at_lead(self) -> None:
        items = aa.preparation_occurrences(config_fixture(), registry_fixture(), empty_completion(), aa.parse_datetime("2026-08-05T16:57:00Z"))
        self.assertEqual([item.procedure_id for item in items], ["structural_sweep"])

    def test_preparation_too_early(self) -> None:
        self.assertEqual(aa.preparation_occurrences(config_fixture(), registry_fixture(), empty_completion(), aa.parse_datetime("2026-08-05T16:56:59Z")), [])

    def test_completed_occurrence_excluded(self) -> None:
        value = empty_completion(); value["procedures"]["structural_sweep"]["completed_through_utc"] = "2026-08-05T22:57:00Z"
        self.assertEqual(aa.preparation_occurrences(config_fixture(), registry_fixture(), value, aa.parse_datetime("2026-08-05T17:00:00Z")), [])

    def test_mutation_freeze_boundary(self) -> None:
        self.assertTrue(aa.candidate_mutation_allowed(self.occurrence(), aa.parse_datetime("2026-08-05T21:26:59Z")))
        self.assertFalse(aa.candidate_mutation_allowed(self.occurrence(), aa.parse_datetime("2026-08-05T21:27:00Z")))

    def test_candidate_valid(self) -> None:
        self.assertEqual(aa.validate_candidate_manifest(self.manifest(), self.occurrence()), [])

    def test_candidate_occurrence_drift_rejected(self) -> None:
        value = self.manifest(); value["occurrence_key"] += "-drift"
        self.assertTrue(aa.validate_candidate_manifest(value, self.occurrence()))

    def test_candidate_evidence_drift_rejected(self) -> None:
        value = self.manifest(); value["repository_state"][0]["protected_head"] = "f" * 40
        self.assertTrue(aa.validate_candidate_manifest(value, self.occurrence()))

    def test_candidate_authority_inflation_rejected(self) -> None:
        value = self.manifest(); value["authority_boundary"]["merge_authorized"] = True
        self.assertTrue(aa.validate_candidate_manifest(value, self.occurrence()))

    def test_candidate_claim_inflation_rejected(self) -> None:
        value = self.manifest(); value["claim_boundaries"]["certificate_issued"] = True
        self.assertTrue(aa.validate_candidate_manifest(value, self.occurrence()))

    def test_completion_valid(self) -> None:
        self.assertEqual(aa.validate_completion_state(empty_completion()), [])

    def test_nonprotected_receipt_rejected(self) -> None:
        value = empty_completion(); item = receipt(); item["receipt_state"] = "CANDIDATE_PREPARED"
        value["procedures"]["structural_sweep"] = {"completed_through_utc": item["scheduled_due_at"], "receipt_count": 1, "receipts": [item]}
        self.assertTrue(aa.validate_completion_state(value))

    def test_duplicate_receipts_rejected(self) -> None:
        value = empty_completion(); item = receipt()
        value["procedures"]["structural_sweep"] = {"completed_through_utc": item["scheduled_due_at"], "receipt_count": 2, "receipts": [item, copy.deepcopy(item)]}
        self.assertTrue(aa.validate_completion_state(value))

    def test_completed_through_mismatch_rejected(self) -> None:
        value = empty_completion(); item = receipt()
        value["procedures"]["structural_sweep"] = {"completed_through_utc": "2026-08-05T22:58:00Z", "receipt_count": 1, "receipts": [item]}
        self.assertTrue(aa.validate_completion_state(value))

    def test_completion_regression_rejected(self) -> None:
        previous = empty_completion(); previous["procedures"]["structural_sweep"]["completed_through_utc"] = "2026-08-05T22:57:00Z"
        self.assertTrue(aa.validate_completion_state(empty_completion(), previous))

    def test_registry_uses_derived_completion(self) -> None:
        value = empty_completion(); value["procedures"]["structural_sweep"]["completed_through_utc"] = "2026-08-05T22:57:00Z"
        patched = aa.apply_completion_to_registry(registry_fixture(), value)
        structural = next(item for item in patched["procedures"] if item["id"] == "structural_sweep")
        self.assertEqual(structural["completion_source"], "protected_receipt_derivation")

    def test_mirror_update_idempotent(self) -> None:
        section = f"{sync.START}\ncurrent\n{sync.END}"
        first = sync.replace_managed_section("prefix\n", section)
        self.assertEqual(first, sync.replace_managed_section(first, section))

    def test_malformed_mirror_fails_closed(self) -> None:
        with self.assertRaises(aa.AutomationError): sync.replace_managed_section(f"{sync.START}\n", "section")

    def test_workflow_permissions_and_crons(self) -> None:
        config = json.loads((ROOT / "governance" / "administrative_maintenance_automation.json").read_text())
        self.assertEqual(validator.validate_workflows(config), [])

    def test_scripts_have_no_merge_capability(self) -> None:
        self.assertEqual(validator.validate_scripts(), [])

    @patch("administrative_automation.subprocess.run")
    def test_receipt_requires_merge_commit_and_exact_head(self, run_mock) -> None:
        run_mock.return_value.returncode = 0
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); path = root / "governance" / "structural_sweep" / "record.json"; path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"status": "COMPLETE", "scheduled_due_at": "2026-08-05T22:57:00Z"}))
            config = {"procedures": {"structural_sweep": {"record_globs": ["governance/structural_sweep/*.json"], "due_fields": ["scheduled_due_at"], "receipt_floor_utc": "2026-08-05T00:00:00Z"}}, "bootstrap_receipts": []}
            def runner(args: list[str]) -> str:
                if args[0] == "log": return MERGE
                if "--format=%P" in args: return f"{'d' * 40} {REVIEWED}"
                if "--format=%B" in args: return f"Merge PR #230\n\nProtected merge authorized by Human Steward at exact head {REVIEWED}.\n\nDisposition: HUMAN_STEWARD_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE."
                raise AssertionError(args)
            state = aa.derive_completion_state(root, config, HEAD, runner)
            item = state["procedures"]["structural_sweep"]["receipts"][0]
            self.assertEqual((item["merge_commit"], item["reviewed_head"], item["pull_request"]), (MERGE, REVIEWED, 230))


if __name__ == "__main__":
    unittest.main()
