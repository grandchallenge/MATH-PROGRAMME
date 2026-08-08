#!/usr/bin/env python3
"""Adversarial runtime tests for CMDG-VALIDATOR-001."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_cmdg_graph_package import (  # noqa: E402
    DEFAULT_PACKAGE,
    canonical_bytes,
    git_blob_sha1,
    validate_loaded_package,
    validate_package_path,
)


PACKAGE_PATH = ROOT / "fixtures" / "cmdg" / "validator_001" / "valid_package.json"
MANIFEST_PATH = ROOT / "fixtures" / "cmdg" / "schema_001" / "valid_manifest.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_mutation(package, manifest, *, bind_manifest: bool = True):
    package = copy.deepcopy(package)
    manifest = copy.deepcopy(manifest)
    blob = git_blob_sha1(canonical_bytes(manifest))
    if bind_manifest:
        package["manifest_git_blob_sha1"] = blob
    return validate_loaded_package(package, manifest, blob)


class CMDGGraphValidatorTests(unittest.TestCase):
    def setUp(self):
        self.package = load(PACKAGE_PATH)
        self.manifest = load(MANIFEST_PATH)

    def assert_code(self, report, code):
        self.assertEqual(report["terminal_state"], "VALIDATOR_REJECTED")
        self.assertEqual(report["rejection_codes"], [code])
        self.assertFalse(report["claim_boundary"]["graph_certified_conferred"])
        self.assertFalse(report["claim_boundary"]["global_completeness_claim"])
        self.assertFalse(report["claim_boundary"]["derived_closure_authoritative"])

    def test_valid_package_path_accepts(self):
        self.assertEqual(DEFAULT_PACKAGE, PACKAGE_PATH)
        report = validate_package_path(PACKAGE_PATH)
        self.assertEqual(report["terminal_state"], "VALIDATOR_ACCEPTED_PRECONDITIONS")
        self.assertEqual(report["rejection_codes"], [])
        self.assertEqual(report["pin_checks"], {
            "manifest_identity": "MATCH",
            "proof_environment": "MATCH",
            "replay": "MATCH",
            "implementation_dependencies": "MATCH",
        })

    def test_report_is_deterministic(self):
        first = validate_package_path(PACKAGE_PATH)
        second = validate_package_path(PACKAGE_PATH)
        self.assertEqual(first, second)

    def test_closure_uses_only_manifest_direct_semantic_authority(self):
        report = validate_package_path(PACKAGE_PATH)
        self.assertEqual(report["authoritative_direct_semantic_edge_ids"], [
            "CMDG:E:GCD-REQ-NAT-DIV",
            "CMDG:E:NAT-EQUIV-NNO",
        ])
        self.assertEqual(report["traversed_direct_semantic_edge_ids"], ["CMDG:E:GCD-REQ-NAT-DIV"])
        self.assertEqual(report["derived_reachable_node_ids"], ["CMDG:ARITH.GCD", "CMDG:ARITH.NAT_DIVISIBILITY"])
        self.assertNotIn("CMDG:E:GCD-PROOF-USES-NATGCD", report["traversed_direct_semantic_edge_ids"])
        self.assertNotIn("CMDG:E:GCD-IMPL-MATHLIB", report["traversed_direct_semantic_edge_ids"])

    def test_boundary_exit_is_explicit(self):
        report = validate_package_path(PACKAGE_PATH)
        self.assertEqual(len(report["boundary_exits"]), 1)
        self.assertEqual(report["boundary_exits"][0]["node_id"], "CMDG:ARITH.NAT_DIVISIBILITY")
        self.assertEqual(report["boundary_exits"][0]["trust_class"], "REUSED_LIBRARY")

    def test_duplicate_node_id_rejected(self):
        package = copy.deepcopy(self.package)
        package["nodes"].append(copy.deepcopy(package["nodes"][0]))
        self.assert_code(run_mutation(package, self.manifest), "DUPLICATE_NODE_ID")

    def test_duplicate_edge_id_rejected(self):
        package = copy.deepcopy(self.package)
        package["additional_edges"].append(copy.deepcopy(package["additional_edges"][0]))
        self.assert_code(run_mutation(package, self.manifest), "DUPLICATE_EDGE_ID")

    def test_missing_root_rejected(self):
        package = copy.deepcopy(self.package)
        package["nodes"] = [node for node in package["nodes"] if node["node_id"] != "CMDG:ARITH.GCD"]
        self.assert_code(run_mutation(package, self.manifest), "ROOT_NODE_MISSING")

    def test_dangling_semantic_endpoint_rejected(self):
        package = copy.deepcopy(self.package)
        package["additional_edges"][2]["source"]["identity"] = "CMDG:UNKNOWN"
        self.assert_code(run_mutation(package, self.manifest), "DANGLING_SEMANTIC_ENDPOINT")

    def test_semantic_scope_missing_endpoint_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["semantic_scope"]["included_node_ids"].remove("CMDG:NAT.NNO")
        self.assert_code(run_mutation(self.package, manifest), "SEMANTIC_SCOPE_MISSING_ENDPOINT")

    def test_direct_semantic_without_reviewed_authority_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["direct_semantic_edges"][0]["authority_state"] = "PROPOSED"
        self.assert_code(run_mutation(self.package, manifest), "DIRECT_SEMANTIC_NOT_REVIEWED")

    def test_derived_edge_injected_as_direct_authority_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["direct_semantic_edges"][0]["authority_state"] = "DERIVED"
        self.assert_code(run_mutation(self.package, manifest), "DERIVED_DIRECT_AUTHORITY")

    def test_layer_laundering_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["direct_semantic_edges"][0]["layer"] = "G_implementation"
        self.assert_code(run_mutation(self.package, manifest), "SEMANTIC_LAYER_LAUNDERING")

    def test_proof_import_relation_laundering_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["direct_semantic_edges"][0]["relation"] = "IMPLEMENTATION_IMPORT"
        self.assert_code(run_mutation(self.package, manifest), "SEMANTIC_LAYER_LAUNDERING")

    def test_tool_proposal_cannot_self_promote(self):
        manifest = copy.deepcopy(self.manifest)
        edge = manifest["direct_semantic_edges"][0]
        edge["proposal_origin"] = {
            "origin": "SEMANTIC_GRAPH_RECONCILER",
            "tool": "fixture-reconciler",
            "artifact_ref": "fixture:proposal"
        }
        edge["review"]["independent_of_proposal_origin"] = False
        self.assert_code(run_mutation(self.package, manifest), "TOOL_PROPOSAL_NOT_INDEPENDENT")

    def test_boundary_node_must_be_represented_and_in_scope(self):
        package = copy.deepcopy(self.package)
        package["nodes"] = [node for node in package["nodes"] if node["node_id"] != "CMDG:ARITH.NAT_DIVISIBILITY"]
        manifest = copy.deepcopy(self.manifest)
        manifest["semantic_scope"]["included_node_ids"].remove("CMDG:ARITH.NAT_DIVISIBILITY")
        self.assert_code(run_mutation(package, manifest), "BOUNDARY_NODE_MISSING")

    def test_reached_boundary_must_allow_semantic_purpose(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["boundaries"][0]["allowed_traversal_purposes"] = ["PROOF"]
        self.assert_code(run_mutation(self.package, manifest), "BOUNDARY_PURPOSE_MISMATCH")

    def test_unresolved_in_boundary_obligation_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["unresolved_obligations"].append({
            "obligation_id": "fixture-inside",
            "scope": "INSIDE_BOUNDARY",
            "description": "must reject",
            "status": "OPEN"
        })
        self.assert_code(run_mutation(self.package, manifest), "UNRESOLVED_IN_BOUNDARY")

    def test_realization_missing_evidence_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["realizations"][0]["realization"]["evidence_refs"] = []
        self.assert_code(run_mutation(self.package, manifest), "REALIZATION_EVIDENCE_MISSING")

    def test_realization_overclaim_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["realizations"][0]["realization"]["automatic_claims"]["mathematical_equivalence"] = True
        self.assert_code(run_mutation(self.package, manifest), "REALIZATION_OVERCLAIM")

    def test_realization_environment_drift_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["realizations"][0]["realization"]["proof_environment_ref"] = "stale-env"
        self.assert_code(run_mutation(self.package, manifest), "REALIZATION_ENVIRONMENT_MISMATCH")

    def test_uncertified_quotient_generator_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["direct_semantic_edges"][1]["equivalence"] = {"quotient_admissibility": "NOT_ADMISSIBLE"}
        self.assert_code(run_mutation(self.package, manifest), "MANIFEST_CONTRACT_VIOLATION")

    def test_stale_proof_environment_pin_rejected(self):
        package = copy.deepcopy(self.package)
        package["retained_evidence"]["proof_environment"]["pins"][0] = "lean-toolchain:stale"
        self.assert_code(run_mutation(package, self.manifest), "STALE_PROOF_ENVIRONMENT_PIN")

    def test_replay_identity_mismatch_rejected(self):
        package = copy.deepcopy(self.package)
        package["retained_evidence"]["replay"]["route_id"] = "STALE-REPLAY"
        self.assert_code(run_mutation(package, self.manifest), "REPLAY_EVIDENCE_MISMATCH")

    def test_implementation_pin_mismatch_rejected(self):
        package = copy.deepcopy(self.package)
        package["retained_evidence"]["implementation_pins"]["mathlib"] = "stale-pin"
        self.assert_code(run_mutation(package, self.manifest), "IMPLEMENTATION_PIN_MISMATCH")

    def test_schema_version_drift_rejected(self):
        package = copy.deepcopy(self.package)
        package["required_schema_versions"]["edge"] = "0.9.0"
        self.assert_code(run_mutation(package, self.manifest), "SCHEMA_VERSION_DRIFT")

    def test_graph_certified_terminal_state_rejected(self):
        package = copy.deepcopy(self.package)
        package["requested_terminal_state"] = "GRAPH_CERTIFIED"
        self.assert_code(run_mutation(package, self.manifest), "PROHIBITED_TERMINAL_STATE")

    def test_global_completeness_claim_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["semantic_scope"]["global_completeness_claim"] = True
        self.assert_code(run_mutation(self.package, manifest), "GLOBAL_COMPLETENESS_PROHIBITED")

    def test_manifest_identity_mismatch_rejected(self):
        package = copy.deepcopy(self.package)
        package["manifest_git_blob_sha1"] = "0" * 40
        self.assert_code(run_mutation(package, self.manifest, bind_manifest=False), "MANIFEST_IDENTITY_MISMATCH")

    def test_reviewed_semantic_edge_absent_from_manifest_rejected(self):
        package = copy.deepcopy(self.package)
        edge = copy.deepcopy(self.manifest["direct_semantic_edges"][0])
        edge["edge_id"] = "CMDG:E:UNDECLARED-DIRECT"
        package["additional_edges"].append(edge)
        self.assert_code(run_mutation(package, self.manifest), "UNDECLARED_DIRECT_SEMANTIC_EDGE")

    def test_unknown_boundary_trust_in_footprint_rejected(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["axiom_footprint"]["boundary_trust"].append("CMDG:UNKNOWN.BOUNDARY")
        self.assert_code(run_mutation(self.package, manifest), "FOOTPRINT_BOUNDARY_TRUST_UNKNOWN")

    def test_derived_closure_cannot_be_authoritative(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["closure_policy"]["derived_closure_authoritative"] = True
        self.assert_code(run_mutation(self.package, manifest), "MANIFEST_CONTRACT_VIOLATION")


if __name__ == "__main__":
    unittest.main()
