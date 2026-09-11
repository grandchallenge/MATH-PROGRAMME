#!/usr/bin/env python3
"""Adversarial mutations for CMDG-EUCLID-BRIDGE-001."""
from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
import validate_cmdg_euclid_bridge as validator  # noqa: E402
from validate_cmdg_euclid_bridge import BridgeError, validate_record  # noqa: E402

RECORD = ROOT / "governance" / "cmdg_euclid_bridge_001.json"
EDGES = ROOT / "fixtures" / "cmdg" / "euclid_bridge_001" / "edges.json"


def load_record():
    return json.loads(RECORD.read_text(encoding="utf-8"))


def load_edges():
    return json.loads(EDGES.read_text(encoding="utf-8"))


class CMDGEuclidBridgeTests(unittest.TestCase):
    def assert_rejected(self, artifact, needle=None):
        with self.assertRaises(BridgeError) as caught:
            validate_record(artifact)
        if needle:
            self.assertIn(needle, str(caught.exception))

    def test_canonical_record(self):
        validate_record(load_record())

    def test_stale_euclid_source_rejected(self):
        a = load_record()
        a["euclid_authority"]["mathcert_source_blob_sha1"] = "0" * 40
        self.assert_rejected(a, "MATHCERT_SOURCE_IDENTITY_DRIFT")

    def test_wrong_theorem_root_rejected(self):
        a = load_record()
        a["euclid_authority"]["roots"][-1] = "MathCert.NumberTheory.fake"
        self.assert_rejected(a, "EUCLID_THEOREM_ROOT_DRIFT")

    def test_original_environment_drift_rejected(self):
        a = load_record()
        a["original_proof_environment"]["lean_toolchain"] = "leanprover/lean4:latest"
        self.assert_rejected(a, "ORIGINAL_ENVIRONMENT_DRIFT")

    def test_transport_direction_reversal_rejected(self):
        a = load_record()
        a["semantic_scope"]["transport_route"] = ["N_ZFC", "N_NNO", "N_DTT"]
        self.assert_rejected(a, "TRANSPORT_DIRECTION_DRIFT")

    def test_omitted_divisibility_rejected(self):
        a = load_record()
        a["semantic_scope"]["admitted_operation_dependencies"].remove("DIVISIBILITY")
        self.assert_rejected(a, "NAT_OPERATION_SCOPE_DRIFT")

    def test_out_of_scope_operation_rejected(self):
        a = load_record()
        a["semantic_scope"]["admitted_operation_dependencies"].append("GCD_FUNCTION")
        self.assert_rejected(a, "NAT_OPERATION_SCOPE_DRIFT")

    def test_gcd_function_transport_overclaim_rejected(self):
        a = load_record()
        a["semantic_scope"]["gcd_function_transport"] = "ADMITTED"
        self.assert_rejected(a, "GCD_FUNCTION_TRANSPORT_OVERCLAIM")

    def test_integer_bezout_transport_overclaim_rejected(self):
        a = load_record()
        a["semantic_scope"]["bezout_integer_transport"] = "ADMITTED"
        self.assert_rejected(a, "INTEGER_BEZOUT_TRANSPORT_OVERCLAIM")

    def test_syntactic_zfc_overclaim_rejected(self):
        a = load_record()
        a["semantic_scope"]["zfc_scope"] = "FULL_SYNTACTIC_ZFC"
        self.assert_rejected(a, "SYNTACTIC_ZFC_OVERCLAIM")

    def test_graph_certified_overclaim_rejected(self):
        a = load_record()
        a["claim_boundary"]["graph_certified_conferred"] = True
        self.assert_rejected(a, "PROHIBITED_AUTHORITY_PROMOTION")

    def test_foundational_equivalence_overclaim_rejected(self):
        a = load_record()
        a["claim_boundary"]["foundational_equivalence_conferred"] = True
        self.assert_rejected(a, "PROHIBITED_AUTHORITY_PROMOTION")

    def test_review_gate_removal_rejected(self):
        a = load_record()
        a["claim_boundary"]["independent_review_required"] = False
        self.assert_rejected(a, "ADMISSION_GATE_BYPASS")

    def test_semantic_edge_promotion_rejected(self):
        edges = load_edges()
        edges[0]["authority_state"] = "REVIEWED_DIRECT"
        edges[0]["review"] = {"reviewer": "x", "disposition": "x", "artifact_ref": "x"}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "edges.json"
            path.write_text(json.dumps(edges), encoding="utf-8")
            with patch.object(validator, "EDGES", path):
                self.assert_rejected(load_record(), "UNREVIEWED_SEMANTIC_AUTHORITY")

    def test_proof_to_semantic_laundering_rejected(self):
        edges = load_edges()
        edge = next(e for e in edges if e["layer"] == "G_proof")
        edge["layer"] = "G_semantic"
        edge["relation"] = "USES_THEOREM"
        edge["authority_state"] = "OBSERVED"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "edges.json"
            path.write_text(json.dumps(edges), encoding="utf-8")
            with patch.object(validator, "EDGES", path):
                self.assert_rejected(load_record(), "EDGE_SCHEMA_VIOLATION")

    def test_realization_automatic_claim_rejected(self):
        edges = load_edges()
        edge = next(e for e in edges if e["relation"] == "REALIZES_AS")
        edge["realization"]["automatic_claims"]["mathematical_equivalence"] = True
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "edges.json"
            path.write_text(json.dumps(edges), encoding="utf-8")
            with patch.object(validator, "EDGES", path):
                self.assert_rejected(load_record(), "EDGE_SCHEMA_VIOLATION")

    def test_formal_lane_identity_drift_rejected(self):
        registry = json.loads(validator.FORMAL_REGISTRY.read_text(encoding="utf-8"))
        lane = next(item for item in registry["lanes"] if item["id"] == "cmdg-euclid-bridge")
        lane["development_targets"] = ["WrongEuclid.lean"]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "formal_validation_registry.json"
            path.write_text(json.dumps(registry), encoding="utf-8")
            with patch.object(validator, "FORMAL_REGISTRY", path):
                self.assert_rejected(load_record(), "FORMAL_LANE_BINDING_DRIFT")

    def test_promotion_wrapper_lane_drift_rejected(self):
        workflow = validator.WF.read_text(encoding="utf-8").replace(
            "lane: cmdg-euclid-bridge", "lane: cmdg-nat"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cmdg-euclid-bridge.yml"
            path.write_text(workflow, encoding="utf-8")
            with patch.object(validator, "WF", path):
                self.assert_rejected(load_record(), "WORKFLOW_EXECUTION_BINDING_MISSING")

    def test_promotion_wrapper_pr_trigger_rejected(self):
        workflow = validator.WF.read_text(encoding="utf-8") + "\n# pull_request:\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cmdg-euclid-bridge.yml"
            path.write_text(workflow, encoding="utf-8")
            with patch.object(validator, "WF", path):
                self.assert_rejected(load_record(), "WORKFLOW_EXECUTION_SCOPE_DRIFT")


if __name__ == "__main__":
    unittest.main()
