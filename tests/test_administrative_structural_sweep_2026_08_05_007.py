from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = (
    ROOT
    / "governance"
    / "administrative_structural_sweeps"
    / "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-05-007.json"
)
VALIDATOR_PATH = ROOT / "ci" / "validate_administrative_structural_sweep.py"

spec = importlib.util.spec_from_file_location("sweep_validator_007", VALIDATOR_PATH)
assert spec and spec.loader
sweep_validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sweep_validator)


class AdministrativeStructuralSweep007Tests(unittest.TestCase):
    def load_record(self) -> dict:
        return json.loads(RECORD_PATH.read_text(encoding="utf-8"))

    def errors_for(self, record: dict) -> list[str]:
        return sweep_validator.validate_record(record)

    def assert_rejected(self, record: dict) -> None:
        self.assertTrue(self.errors_for(record))

    def repository(self, record: dict, name: str) -> dict:
        return next(
            item for item in record["scope"]["repositories"]
            if item["repository"] == name
        )

    def open_pr(self, record: dict, number: int) -> dict:
        return next(
            item for item in record["scope"]["open_pull_requests"]
            if item["pull_request"] == number
        )

    def test_successor_record_is_valid(self) -> None:
        self.assertEqual(self.errors_for(self.load_record()), [])

    def test_preceding_record_remains_valid(self) -> None:
        path = (
            ROOT
            / "governance"
            / "administrative_structural_sweeps"
            / "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-04-006.json"
        )
        record = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(self.errors_for(record), [])

    def test_mutation_rejects_candidate_source_head_as_final_programme_head(self) -> None:
        record = self.load_record()
        item = self.repository(record, "grandchallenge/MATH-PROGRAMME")
        item["protected_head"] = "183ff2a0adfbe5bd0ffd5f2e638089b94b868c54"
        self.assert_rejected(record)

    def test_mutation_rejects_omitted_book_vii_forge_transition(self) -> None:
        record = self.load_record()
        item = self.repository(record, "grandchallenge/MATHFORGE")
        item["protected_head"] = "af5398a05f17789a061ab0d23c2b47f0cc952fff"
        item["merge_commit"] = item["protected_head"]
        item["latest_transition_pr"] = 66
        self.assert_rejected(record)

    def test_mutation_rejects_dependabot_policy_run_substitution(self) -> None:
        record = self.load_record()
        self.open_pr(record, 247)["core_run_id"] += 1
        self.assert_rejected(record)

    def test_mutation_rejects_open_pr_merge_authority(self) -> None:
        record = self.load_record()
        self.open_pr(record, 244)["merge_authorized"] = True
        self.assert_rejected(record)

    def test_mutation_rejects_after_locus_evidence_close(self) -> None:
        record = self.load_record()
        record["evidence_closed_at"] = "2026-08-05T15:57:01-07:00"
        self.assert_rejected(record)

    def test_mutation_rejects_next_locus_drift(self) -> None:
        record = self.load_record()
        record["next_structural_due_at"] = "2026-08-06T08:46:00-07:00"
        self.assert_rejected(record)

    def test_mutation_rejects_stale_transition_review(self) -> None:
        record = self.load_record()
        item = self.repository(record, "grandchallenge/MATHCERT")
        item["review"]["review_id"] = 4868582252
        self.assert_rejected(record)

    def test_mutation_rejects_p2_erasure(self) -> None:
        record = self.load_record()
        record["findings"]["P2"] = record["findings"]["P2"][:1]
        self.assert_rejected(record)

    def test_mutation_rejects_tracker_repair_inflation(self) -> None:
        record = self.load_record()
        record["tracker_mirrors"][2]["repair_required"] = True
        record["tracker_mirrors"][2]["repair_completed"] = True
        self.assert_rejected(record)

    def test_mutation_rejects_removed_human_steward_gate(self) -> None:
        record = self.load_record()
        record["review_readiness"]["human_steward_exact_head_disposition_required"] = False
        self.assert_rejected(record)

    def test_mutation_rejects_claim_inflation(self) -> None:
        record = self.load_record()
        record["claim_boundaries"]["publication_claim_authorized"] = True
        self.assert_rejected(record)

    def test_mutation_rejects_unknown_successor_identity(self) -> None:
        record = self.load_record()
        record["sweep_id"] = "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-06-008"
        self.assert_rejected(record)

    def test_mutation_rejects_repository_duplication(self) -> None:
        record = self.load_record()
        record["scope"]["repositories"][4] = copy.deepcopy(record["scope"]["repositories"][0])
        self.assert_rejected(record)


if __name__ == "__main__":
    unittest.main()
