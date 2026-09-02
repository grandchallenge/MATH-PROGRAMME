#!/usr/bin/env python3
"""Adversarial tests for durable bounded-operation continuity."""

from __future__ import annotations

import copy
import unittest

from validate_bounded_operation_continuity import (
    CHECKPOINT_SCHEMA_REL,
    REGISTRY_REL,
    ROOT,
    checkpoint_semantic_errors,
    instruction_binding_errors,
    load_json,
    registry_errors,
    schema_errors,
)


class BoundedOperationContinuityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = load_json(ROOT / REGISTRY_REL)
        cls.checkpoint_path = ROOT / registry["checkpoints"][0]
        cls.base = load_json(cls.checkpoint_path)

    def errors(self, mutate) -> list[str]:
        checkpoint = copy.deepcopy(self.base)
        mutate(checkpoint)
        return checkpoint_semantic_errors(checkpoint, "fixture")

    def test_repository_candidate_is_valid(self) -> None:
        self.assertEqual([], instruction_binding_errors())
        self.assertEqual([], registry_errors())
        self.assertEqual([], schema_errors(self.base, ROOT / CHECKPOINT_SCHEMA_REL))

    def test_next_action_must_be_permitted(self) -> None:
        errors = self.errors(lambda value: value["next_action"].update({"id": "invented_action"}))
        self.assertTrue(any("next_action must be one of" in error for error in errors))

    def test_vague_wait_is_rejected(self) -> None:
        def mutate(value):
            value["permitted_next_actions"] = [{"id": "wait", "description": "wait"}]
            value["next_action"] = {"id": "wait", "description": "wait", "evidence_targets": ["ci"]}

        errors = self.errors(mutate)
        self.assertTrue(any("vague wait" in error for error in errors))

    def test_awaiting_external_evidence_requires_exact_objects(self) -> None:
        def mutate(value):
            value["state"] = "AWAITING_EXTERNAL_EVIDENCE"
            value["external_evidence"] = {"waiting": False, "objects": []}

        errors = self.errors(mutate)
        self.assertTrue(any("waiting=true" in error for error in errors))
        self.assertTrue(any("requires exact external evidence objects" in error for error in errors))

    def test_blocked_state_requires_named_boundary(self) -> None:
        errors = self.errors(lambda value: value.update({"state": "BLOCKED_GENUINE_BOUNDARY", "blocking_boundary": None}))
        self.assertTrue(any("requires a named blocking_boundary" in error for error in errors))

    def test_nonblocked_state_cannot_carry_synthetic_boundary(self) -> None:
        def mutate(value):
            value["state"] = "IN_PROGRESS"
            value["blocking_boundary"] = {
                "category": "recovery-exhaustion",
                "reason": "claimed without blocked state",
                "evidence_refs": ["fixture"],
            }

        errors = self.errors(mutate)
        self.assertTrue(any("only valid for BLOCKED_GENUINE_BOUNDARY" in error for error in errors))

    def test_terminal_state_requires_terminal_evidence_and_no_next_action(self) -> None:
        errors = self.errors(lambda value: value.update({"state": "TERMINAL"}))
        self.assertTrue(any("must not have next_action" in error for error in errors))
        self.assertTrue(any("must not have permitted_next_actions" in error for error in errors))
        self.assertTrue(any("requires terminal_evidence" in error for error in errors))

    def test_chat_dependent_resume_is_rejected(self) -> None:
        def mutate(value):
            value["resume"]["requires_chat_history"] = True
            value["resume"]["fresh_session_safe"] = False

        errors = self.errors(mutate)
        self.assertTrue(any("cannot require chat history" in error for error in errors))
        self.assertTrue(any("must be fresh-session safe" in error for error in errors))

    def test_checkpoint_cannot_grant_authority(self) -> None:
        errors = self.errors(lambda value: value["claim_boundaries"].update({"merge_authorized": True}))
        self.assertTrue(any("cannot authorize claims or protected actions" in error for error in errors))

    def test_pr_bound_checkpoint_requires_exact_candidate_head(self) -> None:
        errors = self.errors(lambda value: value["identities"].update({"candidate_head_sha": None}))
        self.assertTrue(any("PR-bound checkpoint requires candidate_head_sha" in error for error in errors))
        self.assertTrue(any("workflow-bound checkpoint requires candidate_head_sha" in error for error in errors))

    def test_routine_work_cannot_be_admitted_through_checkpoint(self) -> None:
        errors = self.errors(lambda value: value["admission"].update({"routine_work_excluded": False}))
        self.assertTrue(any("routine bounded work must remain outside" in error for error in errors))

    def test_transition_cannot_disable_live_freshness(self) -> None:
        errors = self.errors(lambda value: value["freshness"].update({"required_before_transition": False}))
        self.assertTrue(any("live freshness verification is required" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
