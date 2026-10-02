#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

from validate_agent_continuity_adoption import ROOT, adoption_errors, load_json


class AgentContinuityAdoptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = load_json(ROOT / ".gcl/agent-continuity.json")
        cls.agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    def errors(self, mutate) -> list[str]:
        record = copy.deepcopy(self.record)
        mutate(record)
        return adoption_errors(record, self.agents)

    def test_repository_candidate_is_valid(self) -> None:
        self.assertEqual([], adoption_errors(self.record, self.agents))

    def test_common_policy_drift_is_rejected(self) -> None:
        errors = self.errors(lambda r: r.update({"policy_id": "OTHER"}))
        self.assertTrue(any("common schema" in error for error in errors))

    def test_local_validator_identity_is_required(self) -> None:
        errors = self.errors(lambda r: r.pop("local_validator"))
        self.assertTrue(any("local_validator" in error for error in errors))

    def test_schema_binding_cannot_drift(self) -> None:
        errors = self.errors(
            lambda r: r["specialization_data"]["schema_binding"].update(
                {"schema_blob_sha": "0" * 40}
            )
        )
        self.assertTrue(any("schema_blob_sha" in error for error in errors))

    def test_duplicate_checkpoint_registry_is_forbidden(self) -> None:
        errors = self.errors(
            lambda r: r["specialization_data"]["implementation"].update(
                {"duplicate_checkpoint_registry_forbidden": False}
            )
        )
        self.assertTrue(any("duplicate_checkpoint_registry_forbidden" in error for error in errors))

    def test_existing_checkpoint_registry_is_authoritative(self) -> None:
        errors = self.errors(
            lambda r: r["specialization_data"]["implementation"].update(
                {"authoritative_checkpoint_registry": "governance/second_registry.json"}
            )
        )
        self.assertTrue(any("authoritative_checkpoint_registry" in error for error in errors))

    def test_authority_expansion_is_rejected(self) -> None:
        errors = self.errors(
            lambda r: r["authority_preservation"].update(
                {"mathematical_certification_changed": True}
            )
        )
        self.assertTrue(any("mathematical_certification_changed" in error for error in errors))

    def test_routine_work_exclusion_cannot_be_removed(self) -> None:
        errors = self.errors(
            lambda r: r["specialization_data"]["applicability"].update(
                {"routine_bounded_work_excluded": False}
            )
        )
        self.assertTrue(any("routine bounded work" in error for error in errors))

    def test_common_schema_cannot_become_remote_mutable_dependency(self) -> None:
        errors = self.errors(
            lambda r: r["specialization_data"]["schema_binding"].update(
                {"mutable_remote_fetch_allowed": True}
            )
        )
        self.assertTrue(any("mutable_remote_fetch_allowed" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
