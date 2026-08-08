#!/usr/bin/env python3
"""Adversarial mutation tests for CMDG-NAT-CONCORDANCE-001."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import validate_cmdg_nat_concordance as validator  # noqa: E402
from validate_cmdg_nat_concordance import ConcordanceError, validate_record  # noqa: E402

RECORD = ROOT / "governance" / "cmdg_nat_concordance_001.json"
EDGES = ROOT / "fixtures" / "cmdg" / "nat_concordance_001" / "edges.json"


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def load_edges():
    return json.loads(EDGES.read_text(encoding="utf-8"))


class CMDGNatConcordanceTests(unittest.TestCase):
    def assert_rejected(self, artifact, needle: str | None = None):
        with self.assertRaises(ConcordanceError) as caught:
            validate_record(artifact)
        if needle:
            self.assertIn(needle, str(caught.exception))

    def test_canonical_record(self):
        validate_record(load_record())

    def test_profile_version_drift_rejected(self):
        artifact = load_record()
        artifact["foundational_profile"]["schema_version"] = "2.0.0"
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_protected_profile_merge_drift_rejected(self):
        artifact = load_record()
        artifact["foundational_profile"]["protected_merge"] = "0" * 40
        self.assert_rejected(artifact, "FOUNDATIONAL_PROFILE_BINDING_DRIFT")

    def test_mathlib_pin_drift_rejected(self):
        artifact = load_record()
        artifact["proof_environment"]["mathlib_commit"] = "0" * 40
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_dtt_identity_drift_rejected(self):
        artifact = load_record()
        artifact["realizations"]["N_DTT"]["formal_locator"] = "Natural"
        self.assert_rejected(artifact, "DTT_IDENTITY_DRIFT")

    def test_zfc_identity_drift_rejected(self):
        artifact = load_record()
        artifact["realizations"]["N_ZFC"]["formal_locator"] = "ZFSet"
        self.assert_rejected(artifact, "ZFC_NAT_IDENTITY_DRIFT")

    def test_nno_identity_drift_rejected(self):
        artifact = load_record()
        artifact["realizations"]["N_NNO"]["formal_locator"] = "Nat"
        self.assert_rejected(artifact, "NNO_IDENTITY_DRIFT")

    def test_transport_direction_reversal_rejected(self):
        artifact = load_record()
        artifact["transport_maps"][0]["source"] = "N_ZFC"
        artifact["transport_maps"][0]["target"] = "N_DTT"
        self.assert_rejected(artifact, "TRANSPORT_DIRECTION_DRIFT")

    def test_missing_operation_rejected(self):
        artifact = load_record()
        artifact["operation_matrix"].pop()
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_duplicate_operation_rejected(self):
        artifact = load_record()
        artifact["operation_matrix"][-1] = dict(artifact["operation_matrix"][0])
        self.assert_rejected(artifact, "DUPLICATE_OPERATION_EVIDENCE")

    def test_order_theorem_substitution_rejected(self):
        artifact = load_record()
        row = next(x for x in artifact["operation_matrix"] if x["map_id"].endswith("DTT_TO_ZFC") and x["operation"] == "ORDER")
        row["theorem"] = "CMDG.NatConcordance.zNat_mem_iff"
        self.assert_rejected(artifact, "OPERATION_THEOREM_DRIFT")

    def test_divisibility_theorem_substitution_rejected(self):
        artifact = load_record()
        row = next(x for x in artifact["operation_matrix"] if x["map_id"].endswith("NNO_TO_ZFC") and x["operation"] == "DIVISIBILITY")
        row["theorem"] = "CMDG.NatConcordance.nnoToZfc_mul"
        self.assert_rejected(artifact, "OPERATION_THEOREM_DRIFT")

    def test_unproved_operation_promotion_rejected(self):
        artifact = load_record()
        artifact["operation_matrix"][0]["status"] = "ADMITTED"
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_definitional_identity_overclaim_rejected(self):
        artifact = load_record()
        artifact["realizations"]["N_ZFC"]["definitional_identity_to_other_foundations"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_foundational_equivalence_overclaim_rejected(self):
        artifact = load_record()
        artifact["claim_boundary"]["foundational_equivalence_conferred"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_graph_certified_overclaim_rejected(self):
        artifact = load_record()
        artifact["claim_boundary"]["graph_certified_conferred"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_global_completeness_overclaim_rejected(self):
        artifact = load_record()
        artifact["claim_boundary"]["global_dependency_completeness_claim"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_artifact_alone_cannot_confer_concordance(self):
        artifact = load_record()
        artifact["claim_boundary"]["conferred_by_artifact_alone"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_review_gate_cannot_be_removed(self):
        artifact = load_record()
        artifact["claim_boundary"]["independent_review_required"] = False
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_unreviewed_direct_graph_authority_rejected(self):
        edges = load_edges()
        edges[0]["authority_state"] = "REVIEWED_DIRECT"
        edges[0]["evidence_refs"] = ["fake-import-only-evidence"]
        edges[0]["review"] = {
            "reviewer": "fake",
            "disposition": "fake",
            "artifact_ref": "fake"
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "edges.json"
            path.write_text(json.dumps(edges), encoding="utf-8")
            with patch.object(validator, "EDGES", path):
                self.assert_rejected(load_record(), "UNREVIEWED_DIRECT_AUTHORITY")

    def test_realizes_as_automatic_claim_rejected(self):
        edges = load_edges()
        edge = next(x for x in edges if x["relation"] == "REALIZES_AS")
        edge["realization"]["automatic_claims"]["foundational_concordance"] = True
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "edges.json"
            path.write_text(json.dumps(edges), encoding="utf-8")
            with patch.object(validator, "EDGES", path):
                self.assert_rejected(load_record(), "EDGE_SCHEMA_VIOLATION")


if __name__ == "__main__":
    unittest.main()
