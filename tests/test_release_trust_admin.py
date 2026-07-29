from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from release_trust_admin import (  # noqa: E402
    ReleaseTrustError,
    normalize_protection,
    protection_errors,
    protection_payload,
    validate_contract,
)


class ReleaseTrustAdminTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            (ROOT / "governance/release_trust_admin_contract.json").read_text(encoding="utf-8")
        )
        cls.schema = json.loads(
            (ROOT / "schemas/release_trust_admin_contract.schema.json").read_text(encoding="utf-8")
        )

    def test_current_contract_passes(self) -> None:
        validate_contract(self.contract, self.schema)

    def test_repository_omission_is_rejected(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["repositories"].pop()
        with self.assertRaises(ReleaseTrustError):
            validate_contract(contract, self.schema)

    def test_required_context_drift_is_rejected(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["repositories"][0]["required_checks"] = ["wrong-check"]
        with self.assertRaises(ReleaseTrustError):
            validate_contract(contract, self.schema)

    def test_payload_is_fail_closed(self) -> None:
        policy = self.contract["branch_policy"]
        payload = protection_payload(policy, ["certify"])
        self.assertTrue(payload["required_status_checks"]["strict"])
        self.assertTrue(payload["enforce_admins"])
        self.assertEqual(
            payload["required_pull_request_reviews"]["required_approving_review_count"], 1
        )
        self.assertTrue(
            payload["required_pull_request_reviews"]["require_last_push_approval"]
        )
        self.assertTrue(payload["required_conversation_resolution"])
        self.assertFalse(payload["allow_force_pushes"])
        self.assertFalse(payload["allow_deletions"])
        self.assertEqual(
            payload["required_pull_request_reviews"]["bypass_pull_request_allowances"],
            {"users": [], "teams": [], "apps": []},
        )

    def test_normalized_matching_protection_passes(self) -> None:
        raw = {
            "url": "https://api.github.com/repos/grandchallenge/MATHCERT/branches/main/protection",
            "required_status_checks": {"strict": True, "contexts": ["certify"]},
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "required_approving_review_count": 1,
                "require_last_push_approval": True,
                "bypass_pull_request_allowances": {"users": [], "teams": [], "apps": []},
            },
            "required_conversation_resolution": {"enabled": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
            "required_linear_history": {"enabled": False},
        }
        normalized = normalize_protection(raw)
        self.assertEqual(
            protection_errors(normalized, self.contract["branch_policy"], ["certify"]), []
        )

    def test_bypass_actor_is_rejected(self) -> None:
        raw = {
            "url": "https://api.github.com/protection",
            "required_status_checks": {"strict": True, "contexts": ["certify"]},
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "required_approving_review_count": 1,
                "require_last_push_approval": True,
                "bypass_pull_request_allowances": {
                    "users": [{"login": "octocat"}],
                    "teams": [],
                    "apps": [],
                },
            },
            "required_conversation_resolution": {"enabled": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
            "required_linear_history": {"enabled": False},
        }
        errors = protection_errors(
            normalize_protection(raw), self.contract["branch_policy"], ["certify"]
        )
        self.assertTrue(any("bypass actors" in error for error in errors))

    def test_relaxed_status_checks_are_rejected(self) -> None:
        raw = {
            "url": "https://api.github.com/protection",
            "required_status_checks": {"strict": False, "contexts": ["certify"]},
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False,
                "required_approving_review_count": 1,
                "require_last_push_approval": True,
                "bypass_pull_request_allowances": {"users": [], "teams": [], "apps": []},
            },
            "required_conversation_resolution": {"enabled": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
            "required_linear_history": {"enabled": False},
        }
        errors = protection_errors(
            normalize_protection(raw), self.contract["branch_policy"], ["certify"]
        )
        self.assertTrue(any("strict_status_checks drift" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
