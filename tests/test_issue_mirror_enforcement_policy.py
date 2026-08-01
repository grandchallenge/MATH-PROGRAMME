from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "governance" / "issue_mirror_enforcement_policy.json"
SCHEMA_PATH = ROOT / "schemas" / "issue_mirror_enforcement_policy.schema.json"


class IssueMirrorEnforcementPolicyTests(unittest.TestCase):
    def load_policy(self) -> dict:
        return json.loads(POLICY_PATH.read_text(encoding="utf-8"))

    def load_schema(self) -> dict:
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def errors_for(self, policy: dict) -> list[str]:
        validator = Draft202012Validator(self.load_schema())
        return [error.message for error in validator.iter_errors(policy)]

    def test_candidate_policy_is_valid(self) -> None:
        self.assertEqual(self.errors_for(self.load_policy()), [])

    def test_candidate_is_nonbinding_and_nonpromotable(self) -> None:
        policy = self.load_policy()
        self.assertFalse(policy["effective"])
        self.assertEqual(policy["council_state"], "PENDING")
        self.assertFalse(policy["may_promote_now"])

    def test_issue_edit_cannot_create_authority(self) -> None:
        policy = self.load_policy()
        self.assertFalse(
            policy["authority_model"][
                "issue_edit_can_change_lifecycle_route_certification_or_claim_state"
            ]
        )

    def test_stale_issue_cannot_override_protected_state(self) -> None:
        policy = self.load_policy()
        self.assertFalse(policy["authority_model"]["stale_issue_can_override_protected_state"])

    def test_mutation_rejects_issue_authority_inflation(self) -> None:
        policy = self.load_policy()
        policy["authority_model"][
            "issue_edit_can_change_lifecycle_route_certification_or_claim_state"
        ] = True
        self.assertTrue(self.errors_for(policy))

    def test_mutation_rejects_stale_issue_override(self) -> None:
        policy = self.load_policy()
        policy["authority_model"]["stale_issue_can_override_protected_state"] = True
        self.assertTrue(self.errors_for(policy))

    def test_mutation_rejects_contradictory_tracker_closure(self) -> None:
        policy = self.load_policy()
        policy["proposed_enforcement"][
            "contradictory_canonical_tracker_blocks_reconciliation_closure"
        ] = False
        self.assertTrue(self.errors_for(policy))

    def test_mutation_rejects_premature_binding(self) -> None:
        policy = self.load_policy()
        policy["effective"] = True
        self.assertTrue(self.errors_for(policy))

    def test_mutation_rejects_premature_promotion(self) -> None:
        policy = self.load_policy()
        policy["may_promote_now"] = True
        self.assertTrue(self.errors_for(policy))

    def test_mutation_rejects_claim_inflation(self) -> None:
        policy = self.load_policy()
        policy["claim_boundaries"]["mathematical_claim_promoted"] = True
        self.assertTrue(self.errors_for(policy))


if __name__ == "__main__":
    unittest.main()
