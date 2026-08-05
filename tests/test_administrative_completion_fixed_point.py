from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_automation as aa
import synchronize_administrative_completion as sync
import validate_administrative_automation as validator

OLD_HEAD = "1" * 40
EVALUATED_HEAD = "2" * 40


def completion(head: str = OLD_HEAD) -> dict:
    return {
        "schema_version": "1.0.0",
        "control_id": "MP-ADMIN-MAINT-001",
        "derived_from_protected_head": head,
        "state": "PROTECTED_RECEIPT_DERIVED",
        "procedures": {
            "structural_sweep": {
                "completed_through_utc": "2026-08-05T06:09:00Z",
                "receipt_count": 1,
                "receipts": [{"receipt_state": "PROTECTED_COMPLETE", "merge_commit": "3" * 40}],
            }
        },
        "authority_boundary": {
            "issues_are_authority": False,
            "workflow_artifacts_are_authority": False,
            "draft_pull_requests_are_authority": False,
            "unmerged_branches_are_authority": False,
            "protected_merge_receipts_required": True,
        },
    }


class AdministrativeCompletionFixedPointTests(unittest.TestCase):
    def test_head_only_mutation_retains_derivation_head(self) -> None:
        previous = completion()
        derived = completion(EVALUATED_HEAD)
        stabilized = sync.stabilize_completion_derivation(
            ROOT,
            derived,
            previous,
            EVALUATED_HEAD,
            ancestry_check=lambda root, ancestor, descendant: (ancestor, descendant) == (OLD_HEAD, EVALUATED_HEAD),
        )
        self.assertEqual(stabilized, previous)

    def test_receipt_mutation_advances_derivation_head(self) -> None:
        previous = completion()
        derived = completion(EVALUATED_HEAD)
        derived["procedures"]["structural_sweep"]["receipt_count"] = 2
        derived["procedures"]["structural_sweep"]["receipts"].append(
            {"receipt_state": "PROTECTED_COMPLETE", "merge_commit": "4" * 40}
        )
        stabilized = sync.stabilize_completion_derivation(
            ROOT,
            derived,
            previous,
            EVALUATED_HEAD,
            ancestry_check=lambda *args: (_ for _ in ()).throw(AssertionError("ancestry check must not run for semantic change")),
        )
        self.assertEqual(stabilized["derived_from_protected_head"], EVALUATED_HEAD)
        self.assertNotEqual(sync.completion_semantics(stabilized), sync.completion_semantics(previous))

    def test_authority_mutation_is_substantive(self) -> None:
        previous = completion()
        derived = completion(EVALUATED_HEAD)
        derived["authority_boundary"]["issues_are_authority"] = True
        stabilized = sync.stabilize_completion_derivation(
            ROOT,
            derived,
            previous,
            EVALUATED_HEAD,
            ancestry_check=lambda *args: False,
        )
        self.assertEqual(stabilized["derived_from_protected_head"], EVALUATED_HEAD)

    def test_nonancestral_retained_head_fails_closed(self) -> None:
        with self.assertRaisesRegex(aa.AutomationError, "not ancestral"):
            sync.stabilize_completion_derivation(
                ROOT,
                completion(EVALUATED_HEAD),
                completion(),
                EVALUATED_HEAD,
                ancestry_check=lambda *args: False,
            )

    def test_post_merge_fixed_point_opens_no_successor_pr(self) -> None:
        previous = completion()
        stabilized = sync.stabilize_completion_derivation(
            ROOT,
            completion(EVALUATED_HEAD),
            previous,
            EVALUATED_HEAD,
            ancestry_check=lambda *args: True,
        )
        with tempfile.TemporaryDirectory() as temp:
            state_path = Path(temp) / "completion.json"
            state_path.write_text(json.dumps(previous), encoding="utf-8")
            with patch.object(sync, "STATE_PATH", state_path):
                result = sync.create_completion_sync_pr(
                    object(),
                    "grandchallenge/MATH-PROGRAMME",
                    stabilized,
                    EVALUATED_HEAD,
                )
        self.assertIsNone(result)

    def assert_contract_mutation_rejected(self, marker: str) -> None:
        source = validator.SYNC_SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn(marker, source)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "synchronize.py"
            path.write_text(source.replace(marker, "", 1), encoding="utf-8")
            with patch.object(validator, "SYNC_SCRIPT_PATH", path):
                self.assertTrue(validator.validate_fixed_point_contract())

    def test_mutation_removing_semantic_gate_rejected(self) -> None:
        self.assert_contract_mutation_rejected(
            "if previous is None or completion_semantics(previous) != completion_semantics(completion):"
        )

    def test_mutation_removing_ancestry_gate_rejected(self) -> None:
        self.assert_contract_mutation_rejected(
            "if not ancestry_check(root, retained_head, evaluated_head):"
        )

    def test_mutation_removing_no_successor_gate_rejected(self) -> None:
        self.assert_contract_mutation_rejected("if current == completion:\n        return None")


if __name__ == "__main__":
    unittest.main()
