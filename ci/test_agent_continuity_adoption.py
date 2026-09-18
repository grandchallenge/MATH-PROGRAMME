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

    def test_repository_candidate_is_valid(self) -> None:
        self.assertEqual([], adoption_errors(self.record, self.agents))

    def test_duplicate_checkpoint_registry_is_forbidden(self) -> None:
        record = copy.deepcopy(self.record)
        record["implementation"]["duplicate_checkpoint_registry_forbidden"] = False
        errors = adoption_errors(record, self.agents)
        self.assertTrue(any("duplicate_checkpoint_registry_forbidden" in error for error in errors))

    def test_existing_checkpoint_registry_is_authoritative(self) -> None:
        record = copy.deepcopy(self.record)
        record["implementation"]["authoritative_checkpoint_registry"] = "governance/second_registry.json"
        errors = adoption_errors(record, self.agents)
        self.assertTrue(any("authoritative_checkpoint_registry" in error for error in errors))

    def test_authority_expansion_is_rejected(self) -> None:
        record = copy.deepcopy(self.record)
        record["authority_preservation"]["mathematical_certification_changed"] = True
        errors = adoption_errors(record, self.agents)
        self.assertTrue(any("mathematical_certification_changed" in error for error in errors))

    def test_routine_work_exclusion_cannot_be_removed(self) -> None:
        record = copy.deepcopy(self.record)
        record["applicability"]["routine_bounded_work_excluded"] = False
        errors = adoption_errors(record, self.agents)
        self.assertTrue(any("routine bounded work" in error for error in errors))

if __name__ == "__main__":
    unittest.main()
