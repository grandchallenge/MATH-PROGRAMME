#!/usr/bin/env python3
"""Adversarial tests for MCORE-DOMAIN-SHADOW-001."""

from __future__ import annotations

import copy
import unittest

from validate_math_core_domain_shadow import ARTIFACT, load_json, validate_document


class DomainShadowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = load_json(ARTIFACT)

    def assert_rejected(self, mutate) -> None:
        doc = copy.deepcopy(self.base)
        mutate(doc)
        with self.assertRaises(Exception):
            validate_document(doc)

    def test_reference_shadow_validates(self) -> None:
        validate_document(copy.deepcopy(self.base))

    def test_reject_retroactive_live_history(self) -> None:
        self.assert_rejected(lambda d: d["invariants"].__setitem__("retroactive_live_event_history", True))

    def test_reject_autonomous_pruning(self) -> None:
        self.assert_rejected(lambda d: d["invariants"].__setitem__("autonomous_pruning", True))

    def test_reject_cm4_certification_laundering(self) -> None:
        self.assert_rejected(lambda d: d["current_frontier"].__setitem__("cm4_theorem_certified", True))

    def test_reject_p2_reintroduced_as_blocker(self) -> None:
        def mutate(doc):
            for node in doc["nodes"]:
                if node["node_id"] == "MCORE:CONDENSED:CM4:P2":
                    node["current_status"] = "BLOCKING"
                    node["blocker_classes"] = ["MATHEMATICAL"]
        self.assert_rejected(mutate)

    def test_reject_p3_false_closure(self) -> None:
        def mutate(doc):
            for node in doc["nodes"]:
                if node["node_id"] == "MCORE:CONDENSED:CM4:P3":
                    node["current_status"] = "PROTECTED_CLOSED"
                    node["blocker_classes"] = []
        self.assert_rejected(mutate)

    def test_reject_source_blob_drift(self) -> None:
        self.assert_rejected(lambda d: d["source_records"][0].__setitem__("git_blob_sha1", "0" * 40))

    def test_reject_canonical_promotion_effect(self) -> None:
        self.assert_rejected(lambda d: d["nodes"][0].__setitem__("canonical_claim_effect", "PROMOTE"))

    def test_reject_spurious_execution_blocker(self) -> None:
        def mutate(doc):
            doc["current_frontier"]["blockers"][0]["blocker_classes"].append("EXECUTION_INFRASTRUCTURE")
        self.assert_rejected(mutate)

    def test_reject_c06_discharge(self) -> None:
        self.assert_rejected(lambda d: d["current_frontier"].__setitem__("c06_discharged", True))


if __name__ == "__main__":
    unittest.main()
