from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import validate_administrative_automation_v3 as validator

HISTORICAL_OBSERVED = "9d42a0d5b5dee624389eaddb63805dd585745bba"
CURRENT_DERIVATION = "a7ccabd94c7bf6197a35a2ca75257fb17a864042"
VALIDATION_HEAD = "f" * 40


class CompletionStateProgressionTests(unittest.TestCase):
    def evidence(self) -> dict:
        return {"observed_protected_head": HISTORICAL_OBSERVED}

    def completion(self) -> dict:
        return {"derived_from_protected_head": CURRENT_DERIVATION}

    def test_forward_progression_is_accepted(self) -> None:
        allowed = {
            (HISTORICAL_OBSERVED, CURRENT_DERIVATION),
            (CURRENT_DERIVATION, VALIDATION_HEAD),
        }
        errors = validator.completion_progression_errors(
            self.evidence(),
            self.completion(),
            VALIDATION_HEAD,
            lambda ancestor, descendant: (ancestor, descendant) in allowed,
        )
        self.assertEqual(errors, [])

    def test_current_derivation_may_equal_historical_terminal_head(self) -> None:
        completion = {"derived_from_protected_head": HISTORICAL_OBSERVED}
        allowed = {
            (HISTORICAL_OBSERVED, HISTORICAL_OBSERVED),
            (HISTORICAL_OBSERVED, VALIDATION_HEAD),
        }
        errors = validator.completion_progression_errors(
            self.evidence(),
            completion,
            VALIDATION_HEAD,
            lambda ancestor, descendant: (ancestor, descendant) in allowed,
        )
        self.assertEqual(errors, [])

    def test_malformed_current_derivation_is_rejected_before_ancestry(self) -> None:
        calls: list[tuple[str, str]] = []
        errors = validator.completion_progression_errors(
            self.evidence(),
            {"derived_from_protected_head": "not-a-sha"},
            VALIDATION_HEAD,
            lambda ancestor, descendant: calls.append((ancestor, descendant)) or True,
        )
        self.assertEqual(
            errors,
            ["terminal_closure: current completion derivation head is invalid"],
        )
        self.assertEqual(calls, [])

    def test_non_descendant_current_derivation_is_rejected(self) -> None:
        errors = validator.completion_progression_errors(
            self.evidence(),
            self.completion(),
            VALIDATION_HEAD,
            lambda ancestor, descendant: (ancestor, descendant)
            == (CURRENT_DERIVATION, VALIDATION_HEAD),
        )
        self.assertIn(
            "terminal_closure: current completion derivation head does not descend from the historical terminal head",
            errors,
        )

    def test_derivation_not_ancestral_to_validation_head_is_rejected(self) -> None:
        errors = validator.completion_progression_errors(
            self.evidence(),
            self.completion(),
            VALIDATION_HEAD,
            lambda ancestor, descendant: (ancestor, descendant)
            == (HISTORICAL_OBSERVED, CURRENT_DERIVATION),
        )
        self.assertIn(
            "terminal_closure: current completion derivation head is not ancestral to validation head",
            errors,
        )

    def test_historical_terminal_record_remains_immutable(self) -> None:
        record = validator.json.loads(
            validator.TERMINAL_CLOSURE_PATH.read_text(encoding="utf-8")
        )
        evidence = record["post_merge_evidence"]
        self.assertEqual(
            evidence["completion_derivation_head"],
            "18b2020685f11e886eec2cc87aa05d5f4a1367de",
        )
        self.assertEqual(evidence["observed_protected_head"], HISTORICAL_OBSERVED)
        self.assertFalse(evidence["completion_semantics_changed"])
        self.assertIsNone(evidence["completion_state_pull_request"])


if __name__ == "__main__":
    unittest.main()
