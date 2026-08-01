from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CLOSURE_PATH = ROOT / "governance" / "administrative_maintenance_cross_repository_closure.json"
SCHEMA_PATH = ROOT / "schemas" / "administrative_maintenance_cross_repository_closure.schema.json"


class AdministrativeMaintenanceCrossRepositoryClosureTests(unittest.TestCase):
    def load_closure(self) -> dict:
        return json.loads(CLOSURE_PATH.read_text(encoding="utf-8"))

    def errors_for(self, closure: dict) -> list[str]:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        return [error.message for error in validator.iter_errors(closure)]

    def test_closure_is_schema_valid(self) -> None:
        self.assertEqual(self.errors_for(self.load_closure()), [])

    def test_programme_and_intellect_are_exactly_pinned(self) -> None:
        closure = self.load_closure()
        self.assertEqual(
            closure["programme"]["merge_commit"],
            "f3bea6f632a6fc653262c6c6ca0b667d0219d3e6",
        )
        self.assertEqual(
            closure["intellect"]["merge_commit"],
            "d26d673efffbe0874e1440450322869ff70be9d1",
        )
        self.assertEqual(
            closure["intellect"]["adoption"]["blob"],
            "3a82ef0b1a83d6b343da0098cff71bf1748f07a9",
        )
        self.assertEqual(
            closure["intellect"]["adoption"]["phase"],
            "PHASE_B_PROTECTED_ADOPTION_COMPLETE",
        )

    def test_accelerated_schedule_and_pilot_dates_are_exact(self) -> None:
        closure = self.load_closure()
        self.assertEqual(closure["accelerated_schedule"]["factor"], 0.1)
        self.assertEqual(closure["accelerated_schedule"]["pilot"], "P9D")
        self.assertEqual(
            closure["pilot_activation"]["review_due_at"],
            "2026-08-09T18:21:00-07:00",
        )
        self.assertEqual(
            closure["pilot_activation"]["structural_first_due_at"],
            "2026-08-01T11:09:00-07:00",
        )

    def test_all_identity_mismatch_counts_are_zero(self) -> None:
        closure = self.load_closure()
        self.assertTrue(
            all(value == 0 for value in closure["identity_mismatch_counts"].values())
        )

    def test_unchanged_mathematical_providers_are_not_repinned(self) -> None:
        closure = self.load_closure()
        disposition = closure["unchanged_provider_disposition"]
        self.assertFalse(disposition["mathforge_repin_required"])
        self.assertFalse(disposition["mathsolve_repin_required"])
        self.assertFalse(disposition["mathcert_repin_required"])

    def test_external_attestation_remains_post_merge(self) -> None:
        closure = self.load_closure()
        attestation = closure["post_merge_attestation"]
        self.assertIsNone(attestation["final_programme_closure_merge"])
        self.assertTrue(attestation["required_after_merge"])

    def test_claim_boundaries_remain_closed(self) -> None:
        closure = self.load_closure()
        self.assertTrue(all(value is False for value in closure["claim_boundaries"].values()))

    def test_mutation_rejects_stale_intellect_merge(self) -> None:
        closure = self.load_closure()
        closure["intellect"]["merge_commit"] = "0" * 40
        self.assertTrue(self.errors_for(closure))

    def test_mutation_rejects_nonzero_mismatch(self) -> None:
        closure = self.load_closure()
        closure["identity_mismatch_counts"]["intellect_adoption_blob"] = 1
        self.assertTrue(self.errors_for(closure))

    def test_mutation_rejects_unaccelerated_pilot(self) -> None:
        closure = self.load_closure()
        closure["accelerated_schedule"]["pilot"] = "P90D"
        self.assertTrue(self.errors_for(closure))

    def test_mutation_rejects_claim_inflation(self) -> None:
        closure = self.load_closure()
        closure["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(self.errors_for(closure))


if __name__ == "__main__":
    unittest.main()
