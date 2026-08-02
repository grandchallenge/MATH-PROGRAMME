from __future__ import annotations

import copy
import json
import unittest
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SWEEP_PATH = (
    ROOT
    / "governance"
    / "administrative_structural_sweeps"
    / "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-01-001.json"
)
SCHEMA_PATH = ROOT / "schemas" / "administrative_structural_sweep.schema.json"

EXPECTED_HEADS = {
    "grandchallenge/MATH-PROGRAMME": "fb8e215d56714f595f328cb22b2b3f5e9410cc7b",
    "grandchallenge/MATHFORGE": "0ea98866de3066e6a44ea1ca2cf93ade8a9e1c15",
    "grandchallenge/MATHSOLVE": "443daf537dc7e4ee34ab43aeb01508d9177816ab",
    "grandchallenge/MATHCERT": "e8d1e34509e640d82902ad0195560740b52bec0e",
    "grandchallenge/INTELLECT": "d26d673efffbe0874e1440450322869ff70be9d1",
}


class AdministrativeStructuralSweepTests(unittest.TestCase):
    def load_sweep(self) -> dict:
        return json.loads(SWEEP_PATH.read_text(encoding="utf-8"))

    def errors_for(self, sweep: dict) -> list[str]:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        return [error.message for error in validator.iter_errors(sweep)]

    def test_sweep_is_schema_valid(self) -> None:
        self.assertEqual(self.errors_for(self.load_sweep()), [])

    def test_lateness_is_exact_and_does_not_reset_cadence(self) -> None:
        sweep = self.load_sweep()
        due = datetime.fromisoformat(sweep["scheduled_due_at"])
        started = datetime.fromisoformat(sweep["execution_started_at"])
        next_due = datetime.fromisoformat(sweep["next_structural_due_at"])
        self.assertEqual(int((started - due).total_seconds() // 60), 622)
        self.assertEqual(sweep["lateness_minutes_at_start"], 622)
        self.assertEqual(int((next_due - due).total_seconds() // 60), 1008)

    def test_exact_five_repository_heads_are_recorded_once(self) -> None:
        sweep = self.load_sweep()
        observed = {
            item["repository"]: item["protected_head"]
            for item in sweep["scope"]["repositories"]
        }
        self.assertEqual(observed, EXPECTED_HEADS)
        self.assertEqual(len(observed), 5)

    def test_every_repository_has_successful_core_and_gcl_evidence(self) -> None:
        sweep = self.load_sweep()
        for item in sweep["scope"]["repositories"]:
            self.assertEqual(item["core_workflow"]["conclusion"], "success")
            self.assertEqual(item["gcl_workflow"]["conclusion"], "success")
            self.assertGreater(item["core_workflow"]["run_id"], 0)
            self.assertGreater(item["gcl_workflow"]["run_id"], 0)

    def test_open_pr_is_non_authoritative_and_non_interfering(self) -> None:
        sweep = self.load_sweep()
        open_pr = sweep["scope"]["open_pull_requests"][0]
        self.assertEqual(open_pr["repository"], "grandchallenge/INTELLECT")
        self.assertEqual(open_pr["pull_request"], 24)
        self.assertTrue(open_pr["draft"])
        self.assertFalse(open_pr["merge_authorized"])
        self.assertEqual(open_pr["base"], EXPECTED_HEADS["grandchallenge/INTELLECT"])
        self.assertEqual(
            open_pr["interference_disposition"],
            "NO_PROTECTED_AUTHORITY_INTERFERENCE",
        )

    def test_no_p0_or_p1_and_all_p2_findings_are_repaired(self) -> None:
        sweep = self.load_sweep()
        self.assertEqual(sweep["findings"]["P0"], [])
        self.assertEqual(sweep["findings"]["P1"], [])
        self.assertEqual(len(sweep["findings"]["P2"]), 2)
        self.assertTrue(
            all("REPAIRED" in item["disposition"] for item in sweep["findings"]["P2"])
        )

    def test_august_3_administrative_review_remains_clear(self) -> None:
        sweep = self.load_sweep()
        readiness = sweep["review_readiness"]
        self.assertTrue(readiness["administrative_review_clear_to_proceed"])
        self.assertFalse(readiness["circuit_breaker_triggered"])
        self.assertFalse(readiness["waiver_used"])
        self.assertFalse(readiness["emergency_authority_used"])
        self.assertEqual(
            sweep["administrative_review_due_at"],
            "2026-08-03T18:21:00-07:00",
        )

    def test_claim_boundaries_remain_closed(self) -> None:
        sweep = self.load_sweep()
        self.assertTrue(all(value is False for value in sweep["claim_boundaries"].values()))

    def test_mutation_rejects_protected_schedule_rewrite(self) -> None:
        sweep = self.load_sweep()
        sweep["scheduled_due_at"] = sweep["execution_started_at"]
        self.assertTrue(self.errors_for(sweep))

    def test_mutation_rejects_false_on_time_claim(self) -> None:
        sweep = self.load_sweep()
        sweep["lateness_minutes_at_start"] = 0
        self.assertTrue(self.errors_for(sweep))

    def test_mutation_rejects_open_pr_authority_inflation(self) -> None:
        sweep = self.load_sweep()
        sweep["scope"]["open_pull_requests"][0]["merge_authorized"] = True
        self.assertTrue(self.errors_for(sweep))

    def test_mutation_rejects_unrepaired_p1(self) -> None:
        sweep = self.load_sweep()
        sweep["findings"]["P1"] = [
            {
                "finding_id": "MP-ADMIN-P1-2026-08-01-999",
                "title": "Injected authority mismatch",
                "disposition": "OPEN",
            }
        ]
        self.assertTrue(self.errors_for(sweep))

    def test_mutation_rejects_claim_inflation(self) -> None:
        sweep = self.load_sweep()
        sweep["claim_boundaries"]["cert_output_issued"] = True
        self.assertTrue(self.errors_for(sweep))

    def test_mutation_rejects_head_drift(self) -> None:
        sweep = self.load_sweep()
        mutated = copy.deepcopy(sweep)
        mutated["scope"]["repositories"][0]["protected_head"] = "0" * 40
        self.assertNotEqual(
            {
                item["repository"]: item["protected_head"]
                for item in mutated["scope"]["repositories"]
            },
            EXPECTED_HEADS,
        )


if __name__ == "__main__":
    unittest.main()
