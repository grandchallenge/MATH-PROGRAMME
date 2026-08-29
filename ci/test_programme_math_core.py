#!/usr/bin/env python3
from __future__ import annotations

import copy
import unittest

import validate_programme_math_core as core


class MathCoreProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.registry = core.load_json(core.CAPABILITY_REGISTRY)
        cls.trace = core.load_json(core.REFERENCE_TRACE)
        cls.exchange = core.load_json(core.REFERENCE_EXCHANGE)

    @staticmethod
    def event(trace: dict, event_type: str) -> dict:
        return next(e for e in trace["events"] if e["event_type"] == event_type)

    def test_reference_semantics(self) -> None:
        core.validate_capabilities(self.registry)
        core.validate_trace(self.trace, self.registry)
        core.validate_exchange(self.exchange, self.trace, self.registry)

    def test_direct_canonical_promotion_is_forbidden(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["producer_classes"]["MATHCERT"]["canonical_claim_promotion"] = True
        with self.assertRaises(core.ProtocolError):
            core.validate_capabilities(registry)

    def test_human_authority_may_not_be_inferred(self) -> None:
        registry = copy.deepcopy(self.registry)
        registry["authority_invariants"]["human_steward_authority_may_be_inferred"] = True
        with self.assertRaises(core.ProtocolError):
            core.validate_capabilities(registry)

    def test_unauthorized_certificate_is_rejected(self) -> None:
        trace = copy.deepcopy(self.trace)
        certificate = self.event(trace, "CERTIFICATE")
        certificate["producer"]["class"] = "MATHSOLVE"
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_certificate_requires_matching_content_digest(self) -> None:
        trace = copy.deepcopy(self.trace)
        certificate = self.event(trace, "CERTIFICATE")
        certificate["payload"]["artifact_sha256"] = "0" * 64
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_forward_dependency_is_rejected(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["events"][0]["dependencies"] = ["MCORE-C-9999"]
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_learned_constraint_cannot_escape_search_scope(self) -> None:
        trace = copy.deepcopy(self.trace)
        learned = self.event(trace, "LEARN")
        learned["payload"]["effect"] = "THEOREM"
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_heuristic_conflict_cannot_local_prune(self) -> None:
        trace = copy.deepcopy(self.trace)
        conflict = self.event(trace, "CONFLICT")
        learned = self.event(trace, "LEARN")
        conflict["payload"]["assurance"] = "HEURISTIC"
        learned["payload"]["enforcement"] = "LOCAL_PRUNE"
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_heuristic_conflict_cannot_hard_prune(self) -> None:
        trace = copy.deepcopy(self.trace)
        conflict = self.event(trace, "CONFLICT")
        learned = self.event(trace, "LEARN")
        conflict["payload"]["assurance"] = "HEURISTIC"
        learned["payload"]["enforcement"] = "HARD_PRUNE"
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_replayable_conflict_cannot_hard_prune(self) -> None:
        trace = copy.deepcopy(self.trace)
        learned = self.event(trace, "LEARN")
        learned["payload"]["enforcement"] = "HARD_PRUNE"
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_checked_conflict_requires_certifying_producer(self) -> None:
        trace = copy.deepcopy(self.trace)
        conflict = self.event(trace, "CONFLICT")
        conflict["payload"]["assurance"] = "CHECKED"
        conflict["producer"]["class"] = "MATHSOLVE"
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_checked_conflict_can_hard_prune_without_becoming_theorem(self) -> None:
        trace = copy.deepcopy(self.trace)
        conflict = self.event(trace, "CONFLICT")
        learned = self.event(trace, "LEARN")
        conflict["payload"]["assurance"] = "CHECKED"
        conflict["producer"]["class"] = "MATHCERT"
        learned["payload"]["enforcement"] = "HARD_PRUNE"
        self.assertEqual(learned["payload"]["effect"], "SEARCH_ONLY")
        core.validate_trace(trace, self.registry)

    def test_stale_theory_response_is_rejected(self) -> None:
        exchange = copy.deepcopy(self.exchange)
        response = next(m for m in exchange["messages"] if m["message_type"] == "RESPONSE")
        response["base_checkpoint"]["revision"] = "sha256:" + "f" * 64
        with self.assertRaises(core.ProtocolError):
            core.validate_exchange(exchange, self.trace, self.registry)

    def test_unprivileged_producer_cannot_submit_theory_proposal(self) -> None:
        exchange = copy.deepcopy(self.exchange)
        response = next(m for m in exchange["messages"] if m["message_type"] == "RESPONSE")
        response["producer"]["class"] = "INTELLECT"
        with self.assertRaises(core.ProtocolError):
            core.validate_exchange(exchange, self.trace, self.registry)

    def test_missing_repository_evidence_is_rejected(self) -> None:
        trace = copy.deepcopy(self.trace)
        conflict = self.event(trace, "CONFLICT")
        conflict["evidence_refs"] = ["repo:governance/math_core_01/artifacts/does_not_exist.json"]
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_materialization_ignores_provenance_timestamps(self) -> None:
        trace = copy.deepcopy(self.trace)
        before = core.materialize(trace["events"])
        for event in trace["events"]:
            event["created_at"] = "2030-01-01T00:00:00Z"
        after = core.materialize(trace["events"])
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
