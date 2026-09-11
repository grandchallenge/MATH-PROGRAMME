from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import programme_formal_context_migration as migration  # noqa: E402


OLD = [
    "validate-json",
    "Replay LOG-GCD-001 in Lean",
    "Replay PC-WP04 bounded certificate",
    "Replay pinned Union-Closed MATHCERT evidence",
    "policy / policy",
    "security / action-policy",
]
NEW = [
    "validate-json",
    "formal-validation / formal-validation",
    "policy / policy",
    "security / action-policy",
]


def ruleset(contexts=OLD):
    return {
        "id": 17137629,
        "name": "Programme profile - main",
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [
            {"actor_id": 4423678, "actor_type": "Integration", "bypass_mode": "pull_request"}
        ],
        "conditions": {"ref_name": {"exclude": [], "include": ["~DEFAULT_BRANCH"]}},
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {
                "type": "pull_request",
                "parameters": {
                    "required_approving_review_count": 0,
                    "dismiss_stale_reviews_on_push": True,
                    "required_reviewers": [],
                    "require_code_owner_review": False,
                    "dismissal_restriction": {"enabled": False, "allowed_actors": []},
                    "require_last_push_approval": False,
                    "required_review_thread_resolution": True,
                    "require_extra_approval_for_unattributed_changes": True,
                    "allowed_merge_methods": ["merge", "squash"],
                },
            },
            {
                "type": "required_status_checks",
                "parameters": {
                    "strict_required_status_checks_policy": False,
                    "do_not_enforce_on_create": False,
                    "required_status_checks": [{"context": value} for value in contexts],
                },
            },
        ],
        "_links": {"self": {"href": "https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/rulesets/17137629"}},
    }


class FakeClient:
    def __init__(self, initial):
        self.detail = copy.deepcopy(initial)
        self.puts = []

    def request(self, method, path, data=None):
        if method == "GET" and path.endswith("/rulesets"):
            return [
                {"id": 17137629, "name": "Programme profile - main", "target": "branch", "enforcement": "active"},
                {"id": 21969152, "name": "GH-OS universal execution routing", "target": "branch", "enforcement": "active"},
            ]
        if method == "GET" and path.endswith("/rulesets/17137629"):
            return copy.deepcopy(self.detail)
        if method == "PUT" and path.endswith("/rulesets/17137629"):
            self.puts.append(copy.deepcopy(data))
            next_detail = copy.deepcopy(data)
            next_detail["id"] = 17137629
            next_detail["_links"] = self.detail["_links"]
            self.detail = next_detail
            return copy.deepcopy(self.detail)
        raise AssertionError((method, path, data))


class ProgrammeFormalContextMigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = migration.load_contract()

    def test_contract_is_exact(self):
        self.assertEqual(self.contract["from_required_checks"], OLD)
        self.assertEqual(self.contract["to_required_checks"], NEW)

    def test_apply_changes_only_context_list(self):
        before = ruleset()
        client = FakeClient(before)
        evidence = migration.migrate(client, self.contract, apply=True)
        self.assertEqual(len(client.puts), 1)
        self.assertEqual(migration.required_contexts(client.detail), NEW)
        self.assertEqual(
            migration.preservation_projection(client.detail),
            migration.preservation_projection(before),
        )
        pull = next(rule for rule in client.detail["rules"] if rule["type"] == "pull_request")
        self.assertTrue(pull["parameters"]["require_extra_approval_for_unattributed_changes"])
        self.assertEqual(client.detail["bypass_actors"], before["bypass_actors"])
        self.assertTrue(evidence["preservation_verified"])

    def test_verify_rejects_legacy_contexts(self):
        with self.assertRaises(migration.MigrationError):
            migration.migrate(FakeClient(ruleset()), self.contract, apply=False)

    def test_target_state_is_idempotent(self):
        client = FakeClient(ruleset(NEW))
        evidence = migration.migrate(client, self.contract, apply=False)
        self.assertFalse(evidence["mutation_performed"])
        self.assertEqual(client.puts, [])

    def test_unknown_context_state_fails_closed(self):
        with self.assertRaises(migration.MigrationError):
            migration.migrate(FakeClient(ruleset(["validate-json"])), self.contract, apply=True)

    def test_ruleset_identity_drift_fails_closed(self):
        bad = ruleset()
        bad["id"] = 999
        client = FakeClient(bad)
        with self.assertRaises(migration.MigrationError):
            migration.migrate(client, self.contract, apply=True)


if __name__ == "__main__":
    unittest.main()
