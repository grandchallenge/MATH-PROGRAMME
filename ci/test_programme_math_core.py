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
        certificate = next(e for e in trace["events"] if e["event_type"] == "CERTIFICATE")
        certificate["producer"]["class"] = "MATHSOLVE"
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_forward_dependency_is_rejected(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["events"][0]["dependencies"] = ["MCORE-C-9999"]
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_learned_constraint_cannot_escape_search_scope(self) -> None:
        trace = copy.deepcopy(self.trace)
        learned = next(e for e in trace["events"] if e["event_type"] == "LEARN")
        learned["payload"]["effect"] = "THEOREM"
        with self.assertRaises(core.ProtocolError):
            core.validate_trace(trace, self.registry)

    def test_stale_theory_response_is_rejected(self) -> None:
        exchange = copy.deepcopy(self.exchange)
        response = next(m for m in exchange["messages"] if m["message_type"] == "RESPONSE")
        response["base_checkpoint"]["revision"] = "stale-reference"
        with self.assertRaises(core.ProtocolError):
            core.validate_exchange(exchange, self.trace, self.registry)

    def test_unprivileged_producer_cannot_submit_theory_proposal(self) -> None:
        exchange = copy.deepcopy(self.exchange)
        response = next(m for m in exchange["messages"] if m["message_type"] == "RESPONSE")
        response["producer"]["class"] = "INTELLECT"
        with self.assertRaises(core.ProtocolError):
            core.validate_exchange(exchange, self.trace, self.registry)

    def test_materialization_ignores_provenance_timestamps(self) -> None:
        trace = copy.deepcopy(self.trace)
        before = core.materialize(trace["events"])
        for event in trace["events"]:
            event["created_at"] = "2030-01-01T00:00:00Z"
        after = core.materialize(trace["events"])
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
