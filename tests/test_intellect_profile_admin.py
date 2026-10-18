from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
SPEC = importlib.util.spec_from_file_location(
    "intellect_profile_admin", ROOT / "ci" / "intellect_profile_admin.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def contract() -> dict:
    return json.loads(
        (ROOT / "governance" / "intellect_profile_admin_contract.json").read_text(
            encoding="utf-8"
        )
    )


def schema() -> dict:
    return json.loads(
        (ROOT / "schemas" / "intellect_profile_admin_contract.schema.json").read_text(
            encoding="utf-8"
        )
    )


def ruleset_detail(name: str = "Provider profile - main") -> dict:
    return {
        "id": 123,
        "name": name,
        "target": "branch",
        "enforcement": "active",
        "bypass_actors": [],
        "conditions": {
            "ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}
        },
        "rules": [
            {"type": "deletion"},
            {"type": "non_fast_forward"},
            {
                "type": "pull_request",
                "parameters": {
                    "allowed_merge_methods": ["merge", "squash"],
                    "dismiss_stale_reviews_on_push": True,
                    "require_code_owner_review": False,
                    "require_last_push_approval": False,
                    "required_approving_review_count": 1,
                    "required_review_thread_resolution": True,
                    "require_extra_approval_for_unattributed_changes": True,
                    "required_reviewers": [],
                    "dismissal_restriction": {
                        "enabled": False,
                        "allowed_actors": [],
                    },
                },
            },
            {
                "type": "required_status_checks",
                "parameters": {
                    "do_not_enforce_on_create": False,
                    "strict_required_status_checks_policy": False,
                    "required_status_checks": [
                        {"context": "test (3.11.14)"},
                        {"context": "test (3.12.13)"},
                        {"context": "policy / policy"},
                        {"context": "security / action-policy"},
                        {"context": "routing-enforcement"},
                    ],
                },
            },
        ],
        "source": "grandchallenge/INTELLECT",
        "node_id": "RRS_123",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
    }


class IntellectProfileAdminTests(unittest.TestCase):
    def test_contract_and_schema_validate(self) -> None:
        jsonschema.Draft202012Validator.check_schema(schema())
        MODULE.validate_contract(contract(), schema())

    def test_rejects_phase_a_identity_substitution(self) -> None:
        broken = copy.deepcopy(contract())
        broken["authority"]["phase_a_merge"] = "0" * 40
        with self.assertRaises(MODULE.IntellectProfileAdminError):
            MODULE.validate_contract(broken, schema())

    def test_rejects_claim_boundary_inflation(self) -> None:
        broken = copy.deepcopy(contract())
        broken["claim_boundaries"]["organization_wide_conformance"] = True
        with self.assertRaises(MODULE.IntellectProfileAdminError):
            MODULE.validate_contract(broken, schema())

    def test_installation_scope_requires_exact_repositories(self) -> None:
        payload = {
            "total_count": 2,
            "repositories": [
                {"id": 2, "full_name": "grandchallenge/INTELLECT"},
                {"id": 1, "full_name": "grandchallenge/MATH-PROGRAMME"},
            ],
        }
        normalized = MODULE.normalize_installation_scope(payload)
        self.assertEqual(normalized["authentication"], "github_app_installation")
        self.assertEqual(normalized["repository_count"], 2)
        self.assertEqual(
            [row["full_name"] for row in normalized["repositories"]],
            ["grandchallenge/INTELLECT", "grandchallenge/MATH-PROGRAMME"],
        )

    def test_installation_scope_rejects_repository_substitution(self) -> None:
        payload = {
            "total_count": 2,
            "repositories": [
                {"id": 2, "full_name": "grandchallenge/INTELLECT"},
                {"id": 3, "full_name": "grandchallenge/MATHCERT"},
            ],
        }
        with self.assertRaisesRegex(
            MODULE.IntellectProfileAdminError, "exactly MATH-PROGRAMME and INTELLECT"
        ):
            MODULE.normalize_installation_scope(payload)

    def test_property_update_adds_required_value_and_preserves_fields(self) -> None:
        current = {
            "property_name": "constitutional_profile",
            "value_type": "single_select",
            "required": True,
            "default_value": "Provider",
            "description": "Profile class",
            "allowed_values": ["Provider", "Programme"],
            "values_editable_by": "org_actors",
            "require_explicit_values": True,
        }
        payload = MODULE.property_update_payload(current, "Constitutional")
        self.assertEqual(
            payload["allowed_values"], ["Provider", "Programme", "Constitutional"]
        )
        self.assertTrue(payload["required"])
        self.assertEqual(payload["default_value"], "Provider")
        self.assertEqual(payload["description"], "Profile class")
        self.assertEqual(payload["values_editable_by"], "org_actors")
        self.assertTrue(payload["require_explicit_values"])

    def test_property_update_is_idempotent(self) -> None:
        current = {
            "property_name": "authority_scope",
            "value_type": "single_select",
            "required": False,
            "default_value": None,
            "description": "Scope",
            "allowed_values": ["provider", "constitutional"],
            "values_editable_by": "org_actors",
        }
        payload = MODULE.property_update_payload(current, "constitutional")
        self.assertEqual(payload["allowed_values"].count("constitutional"), 1)

    def test_property_update_rejects_wrong_type(self) -> None:
        current = {
            "property_name": "authority_scope",
            "value_type": "string",
            "allowed_values": [],
        }
        with self.assertRaisesRegex(
            MODULE.IntellectProfileAdminError, "single_select"
        ):
            MODULE.property_update_payload(current, "constitutional")

    def test_property_schema_readback_rejects_non_vocabulary_drift(self) -> None:
        before = {
            "property_name": "authority_scope",
            "source_type": "organization",
            "value_type": "single_select",
            "required": False,
            "default_value": None,
            "description": "Scope",
            "allowed_values": ["provider"],
            "values_editable_by": "org_actors",
            "require_explicit_values": False,
        }
        after = copy.deepcopy(before)
        after["allowed_values"].append("constitutional")
        after["description"] = "Changed"
        with self.assertRaisesRegex(
            MODULE.IntellectProfileAdminError, "outside allowed_values"
        ):
            MODULE.verify_property_schema_change(before, after, "constitutional")

    def test_property_value_normalization_rejects_duplicates(self) -> None:
        rows = [
            {"property_name": "risk_tier", "value": "critical"},
            {"property_name": "risk_tier", "value": "high"},
        ]
        with self.assertRaisesRegex(
            MODULE.IntellectProfileAdminError, "duplicate property-value"
        ):
            MODULE.normalize_property_values(rows)

    def test_expected_ruleset_validates(self) -> None:
        normalized = MODULE.normalize_intellect_ruleset(ruleset_detail())
        MODULE.validate_ruleset(normalized, contract())

    def test_ruleset_rejects_bypass_actor(self) -> None:
        detail = ruleset_detail()
        detail["bypass_actors"] = [{"actor_id": 1, "actor_type": "Team"}]
        normalized = MODULE.normalize_intellect_ruleset(detail)
        with self.assertRaisesRegex(MODULE.IntellectProfileAdminError, "bypass"):
            MODULE.validate_ruleset(normalized, contract())

    def test_ruleset_rejects_missing_required_check(self) -> None:
        detail = ruleset_detail()
        detail["rules"][3]["parameters"]["required_status_checks"].pop()
        normalized = MODULE.normalize_intellect_ruleset(detail)
        with self.assertRaisesRegex(
            MODULE.IntellectProfileAdminError, "required_checks"
        ):
            MODULE.validate_ruleset(normalized, contract())

    def test_ruleset_update_changes_only_name_when_current(self) -> None:
        detail = ruleset_detail()
        payload = MODULE.writable_ruleset(detail, "Constitutional profile - main")
        expected = {
            "name": "Constitutional profile - main",
            "target": detail["target"],
            "enforcement": detail["enforcement"],
            "bypass_actors": detail["bypass_actors"],
            "conditions": detail["conditions"],
            "rules": detail["rules"],
        }
        self.assertEqual(payload, expected)

    @staticmethod
    def prestate_detail() -> dict:
        detail = ruleset_detail()
        checks = detail["rules"][3]["parameters"]["required_status_checks"]
        assert checks[-1] == {"context": "routing-enforcement"}
        checks.pop()
        return detail

    @staticmethod
    def rule_state(detail: dict) -> dict:
        return {
            "main_sha": "a" * 40,
            "actor": {"authentication": "github_app_installation"},
            "property_schemas": {
                "constitutional_profile": {
                    "property_name": "constitutional_profile",
                    "source_type": "organization",
                    "value_type": "single_select",
                    "required": False,
                    "default_value": None,
                    "description": "Profile",
                    "allowed_values": ["Provider", "Constitutional"],
                    "values_editable_by": "org_actors",
                    "require_explicit_values": False,
                },
                "authority_scope": {
                    "property_name": "authority_scope",
                    "source_type": "organization",
                    "value_type": "single_select",
                    "required": False,
                    "default_value": None,
                    "description": "Scope",
                    "allowed_values": ["provider", "constitutional"],
                    "values_editable_by": "org_actors",
                    "require_explicit_values": False,
                },
            },
            "property_values": copy.deepcopy(contract()["repository_property_values"]),
            "ruleset_detail": detail,
            "ruleset": MODULE.normalize_intellect_ruleset(detail),
        }

    def test_four_to_five_prestate_only_allowed_in_apply(self) -> None:
        pre = MODULE.normalize_intellect_ruleset(self.prestate_detail())
        with self.assertRaisesRegex(
            MODULE.IntellectProfileAdminError, "required_checks"
        ):
            MODULE.validate_ruleset(pre, contract())
        MODULE.validate_ruleset(pre, contract(), allow_admitted_prestate=True)

    def test_reconcile_four_to_five_preserves_other_fields(self) -> None:
        original = self.prestate_detail()
        frozen = copy.deepcopy(original)
        result = MODULE.target_ruleset_payload(original, contract())
        self.assertEqual(original, frozen, "input detail mutated")
        self.assertEqual(result["rules"][3]["parameters"]["required_status_checks"],
                         ruleset_detail()["rules"][3]["parameters"]["required_status_checks"])
        self.assertEqual(result["rules"][:3], original["rules"][:3])
        self.assertTrue(result["rules"][2]["parameters"][
            "require_extra_approval_for_unattributed_changes"])
        self.assertEqual(result["rules"][2]["parameters"]["required_approving_review_count"], 1)
        self.assertEqual(result["bypass_actors"], [])
        before = self.rule_state(original)
        after = self.rule_state({**copy.deepcopy(original), **result})
        MODULE.verify_after(before, after, contract())

    def test_already_reconciled_idempotent(self) -> None:
        original = ruleset_detail("Constitutional profile - main")
        target = MODULE.target_ruleset_payload(original, contract())
        self.assertEqual(target["rules"], original["rules"])
        before = self.rule_state(original)
        after = self.rule_state({**copy.deepcopy(original), **target})
        MODULE.verify_after(before, after, contract())

    def test_unexpected_check_drift_rejected(self) -> None:
        for kind in ("unknown", "duplicate", "missing_other", "reordered"):
            with self.subTest(kind=kind):
                detail = self.prestate_detail()
                checks = detail["rules"][3]["parameters"]["required_status_checks"]
                if kind == "unknown":
                    checks.append({"context": "unapproved-check"})
                elif kind == "duplicate":
                    checks.append({"context": checks[0]["context"]})
                elif kind == "missing_other":
                    checks.pop(0)
                else:
                    checks[0], checks[1] = checks[1], checks[0]
                with self.assertRaises(MODULE.IntellectProfileAdminError):
                    MODULE.target_ruleset_payload(detail, contract())

    def test_unrelated_policy_change_rejected_after_apply(self) -> None:
        pre = self.prestate_detail()
        before = self.rule_state(pre)
        target = MODULE.target_ruleset_payload(pre, contract())
        for kind in ("review_count", "bypass", "extra_approval", "unknown_rule"):
            with self.subTest(kind=kind):
                edited = copy.deepcopy(target)
                if kind == "review_count":
                    edited["rules"][2]["parameters"]["required_approving_review_count"] = 0
                elif kind == "bypass":
                    edited["bypass_actors"].append({"actor_type": "Team", "actor_id": 4})
                elif kind == "extra_approval":
                    edited["rules"][2]["parameters"]["require_extra_approval_for_unattributed_changes"] = False
                else:
                    edited["rules"].append({"type": "update"})
                after = self.rule_state({**copy.deepcopy(pre), **edited})
                with self.assertRaises(MODULE.IntellectProfileAdminError):
                    MODULE.verify_after(before, after, contract())

    def test_apply_writes_admitted_target_and_is_preflighted(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = []
            def request(self, method, path, payload):
                self.calls.append((method, path, copy.deepcopy(payload)))
        client = FakeClient()
        before = self.rule_state(self.prestate_detail())
        old_pause = MODULE.MUTATION_PAUSE_SECONDS
        MODULE.MUTATION_PAUSE_SECONDS = 0
        try:
            operations = MODULE.apply_contract(client, contract(), before)
        finally:
            MODULE.MUTATION_PAUSE_SECONDS = old_pause
        self.assertEqual([x[0] for x in client.calls], ["PATCH", "PATCH", "PUT"])
        self.assertEqual(operations[-1]["operation"],
                         "reconcile_ruleset_required_checks_and_name")
        put = client.calls[-1][2]
        self.assertEqual(put["rules"][3]["parameters"]["required_status_checks"],
                         ruleset_detail()["rules"][3]["parameters"]["required_status_checks"])
        self.assertEqual(put["rules"][2], self.prestate_detail()["rules"][2])
        self.assertEqual(put["bypass_actors"], [])
        # Unexpected pre-state must fail before any property or ruleset mutation.
        bad = copy.deepcopy(before)
        bad["ruleset_detail"]["rules"][3]["parameters"]["required_status_checks"][0] = {
            "context": "foreign-check"}
        bad["ruleset"] = MODULE.normalize_intellect_ruleset(bad["ruleset_detail"])
        blocked_client = FakeClient()
        with self.assertRaises(MODULE.IntellectProfileAdminError):
            MODULE.apply_contract(blocked_client, contract(), bad)
        self.assertEqual(blocked_client.calls, [])

    def test_verify_post_state_rejects_property_drift(self) -> None:
        current_contract = contract()
        before = {
            "main_sha": "a" * 40,
            "actor": {"authentication": "github_app_installation"},
            "property_schemas": {
                "constitutional_profile": {
                    "allowed_values": ["Provider", "Constitutional"]
                },
                "authority_scope": {
                    "allowed_values": ["provider", "constitutional"]
                },
            },
            "property_values": {},
            "ruleset": MODULE.normalize_intellect_ruleset(ruleset_detail()),
        }
        after = copy.deepcopy(before)
        after["property_values"] = copy.deepcopy(
            current_contract["repository_property_values"]
        )
        after["property_values"]["risk_tier"] = "high"
        after["ruleset"]["name"] = "Constitutional profile - main"
        with self.assertRaisesRegex(
            MODULE.IntellectProfileAdminError, "property readback drift"
        ):
            MODULE.verify_after(before, after, current_contract)

    def test_evidence_digest_is_stable(self) -> None:
        value = {"b": 2, "a": 1}
        self.assertEqual(
            MODULE.canonical_sha256(value),
            MODULE.canonical_sha256({"a": 1, "b": 2}),
        )


if __name__ == "__main__":
    unittest.main()
