#!/usr/bin/env python3
"""Adversarial tests for MCORE-DOMAIN-DIAG-001."""

from __future__ import annotations

import copy
import unittest

from validate_math_core_domain_diag import ARTIFACT, load_json, validate_document


class DomainDiagnosticTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = load_json(ARTIFACT)

    def assert_rejected(self, mutate) -> None:
        doc = copy.deepcopy(self.base)
        mutate(doc)
        with self.assertRaises(Exception):
            validate_document(doc)

    def test_reference_diagnostic_validates(self) -> None:
        validate_document(copy.deepcopy(self.base))

    def test_reject_source_checkpoint_drift(self) -> None:
        self.assert_rejected(lambda d: d["source_checkpoint"].__setitem__("revision", "0" * 40))

    def test_reject_shadow_blob_drift(self) -> None:
        self.assert_rejected(lambda d: d["source_shadow"].__setitem__("git_blob_sha1", "0" * 40))

    def test_reject_p2_reintroduced_as_blocker(self) -> None:
        def mutate(doc):
            row = next(row for row in doc["frontier_view"] if row["id"] == "CM4-P2")
            row["frontier_role"] = "BLOCKING"
            row["blocker_classes"] = ["MATHEMATICAL"]
        self.assert_rejected(mutate)

    def test_reject_p3_false_close(self) -> None:
        def mutate(doc):
            row = next(row for row in doc["frontier_view"] if row["id"] == "CM4-P3")
            row["current_status"] = "PROTECTED_CLOSED"
        self.assert_rejected(mutate)

    def test_reject_spurious_execution_blocker(self) -> None:
        def mutate(doc):
            row = next(row for row in doc["frontier_view"] if row["id"] == "CM4-P3")
            row["blocker_classes"].append("EXECUTION_INFRASTRUCTURE")
        self.assert_rejected(mutate)

    def test_reject_p4_dependency_drift(self) -> None:
        def mutate(doc):
            row = next(row for row in doc["frontier_view"] if row["id"] == "CM4-P4")
            row["depends_on"] = []
        self.assert_rejected(mutate)

    def test_reject_lineage_status_drift(self) -> None:
        self.assert_rejected(lambda d: d["lineage_view"][0].__setitem__("current_status", "OPEN"))

    def test_reject_live_coordinator_authority(self) -> None:
        self.assert_rejected(lambda d: d["invariants"].__setitem__("live_coordinator", True))

    def test_reject_promotion_effect(self) -> None:
        self.assert_rejected(lambda d: d["claim_boundary"].__setitem__("promotes_claim", True))

    def test_reject_persistent_coordinator_authority(self) -> None:
        self.assert_rejected(lambda d: d["claim_boundary"].__setitem__("authorizes_persistent_coordinator", True))


if __name__ == "__main__":
    unittest.main()
