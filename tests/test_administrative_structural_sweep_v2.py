from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "governance" / "administrative_structural_sweeps" / "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-006.json"
VALIDATOR_PATH = ROOT / "ci" / "validate_administrative_structural_sweep.py"

spec = importlib.util.spec_from_file_location("sweep_validator", VALIDATOR_PATH)
assert spec and spec.loader
sweep_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sweep_validator)


class AdministrativeStructuralSweepV2Tests(unittest.TestCase):
    def load_record(self) -> dict:
        return json.loads(RECORD_PATH.read_text(encoding="utf-8"))

    def errors_for(self, record: dict) -> list[str]:
        return sweep_validator.validate_record(record)

    def assert_rejected(self, record: dict) -> None:
        self.assertTrue(self.errors_for(record))

    def test_governed_record_is_valid(self) -> None:
        self.assertEqual(self.errors_for(self.load_record()), [])

    def test_mutation_rejects_deadline_drift(self) -> None:
        record = self.load_record()
        record["scheduled_due_at"] = "2026-08-05T00:00:00-07:00"
        self.assert_rejected(record)

    def test_mutation_rejects_retrospective_evidence_label(self) -> None:
        record = self.load_record()
        record["evidence_mode"] = "RETROSPECTIVE_RECONSTRUCTION"
        self.assert_rejected(record)

    def test_mutation_rejects_after_deadline_evidence_close(self) -> None:
        record = self.load_record()
        record["evidence_closed_at"] = "2026-08-04T23:10:00-07:00"
        self.assert_rejected(record)

    def test_mutation_rejects_cadence_reset(self) -> None:
        record = self.load_record()
        record["baseline_reset"]["cadence_anchor_reset"] = True
        self.assert_rejected(record)

    def test_mutation_rejects_discarded_implementation_commit(self) -> None:
        record = self.load_record()
        record["baseline_reset"]["implementation_commits_discarded"] = 1
        self.assert_rejected(record)

    def test_mutation_rejects_protected_head_drift(self) -> None:
        record = self.load_record()
        record["scope"]["repositories"][0]["protected_head"] = "0" * 40
        self.assert_rejected(record)

    def test_mutation_rejects_duplicate_repository(self) -> None:
        record = self.load_record()
        record["scope"]["repositories"][4] = copy.deepcopy(record["scope"]["repositories"][0])
        self.assert_rejected(record)

    def test_mutation_rejects_stale_review_identity(self) -> None:
        record = self.load_record()
        record["scope"]["repositories"][2]["review"]["review_id"] += 1
        self.assert_rejected(record)

    def test_mutation_rejects_non_exact_review(self) -> None:
        record = self.load_record()
        record["scope"]["repositories"][3]["review"]["exact_head"] = False
        self.assert_rejected(record)

    def test_mutation_rejects_missing_required_disposition(self) -> None:
        record = self.load_record()
        record["scope"]["repositories"][0]["disposition"]["comment_id"] = None
        self.assert_rejected(record)

    def test_mutation_rejects_failed_workflow(self) -> None:
        record = self.load_record()
        record["scope"]["repositories"][1]["core_workflow"]["conclusion"] = "failure"
        self.assert_rejected(record)

    def test_mutation_rejects_omitted_open_pr(self) -> None:
        record = self.load_record()
        record["scope"]["open_pull_requests"] = []
        self.assert_rejected(record)

    def test_mutation_rejects_open_pr_authority_inflation(self) -> None:
        record = self.load_record()
        record["scope"]["open_pull_requests"][0]["merge_authorized"] = True
        self.assert_rejected(record)

    def test_mutation_rejects_omitted_tracker_repair(self) -> None:
        record = self.load_record()
        record["tracker_mirrors"][2]["repair_required"] = False
        self.assert_rejected(record)

    def test_mutation_rejects_unrepaired_p2(self) -> None:
        record = self.load_record()
        record["findings"]["P2"][0]["disposition"] = "OPEN"
        self.assert_rejected(record)

    def test_mutation_rejects_injected_p1(self) -> None:
        record = self.load_record()
        record["findings"]["P1"] = [{
            "finding_id": "MP-ADMIN-P1-2026-08-04-006-999",
            "title": "Injected authority defect",
            "observed_at": "2026-08-04T19:46:00-07:00",
            "disposition": "OPEN"
        }]
        self.assert_rejected(record)

    def test_mutation_rejects_manual_process_pending(self) -> None:
        record = self.load_record()
        record["review_readiness"]["pending_manual_processes_at_evidence_freeze"] = 1
        self.assert_rejected(record)

    def test_mutation_rejects_removed_review_gate(self) -> None:
        record = self.load_record()
        record["review_readiness"]["independent_exact_head_review_required"] = False
        self.assert_rejected(record)

    def test_mutation_rejects_claim_inflation(self) -> None:
        record = self.load_record()
        record["claim_boundaries"]["certificate_issued"] = True
        self.assert_rejected(record)


if __name__ == "__main__":
    unittest.main()
