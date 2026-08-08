#!/usr/bin/env python3
"""Adversarial mutation tests for CMDG-SCHEMA-001."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_cmdg_schema_contracts import (  # noqa: E402
    ContractError,
    validate_edge,
    validate_manifest,
    validate_schema,
)


FIXTURE_DIR = ROOT / "fixtures" / "cmdg" / "schema_001"
SCHEMAS = ROOT / "schemas"


def load(name: str):
    return json.loads((FIXTURE_DIR / name).read_text(encoding="utf-8"))


class CMDGSchemaContractTests(unittest.TestCase):
    def assert_rejected(self, fn, artifact, needle: str | None = None):
        with self.assertRaises(ContractError) as caught:
            fn(artifact)
        if needle:
            self.assertIn(needle, str(caught.exception))

    def test_valid_node_edge_manifest(self):
        node = load("valid_node.json")
        edge = load("valid_edge.json")
        manifest = load("valid_manifest.json")
        validate_schema(node, SCHEMAS / "cmdg_node.schema.json", "node")
        validate_edge(edge)
        validate_manifest(manifest)

    def test_manifest_missing_required_field(self):
        artifact = load("valid_manifest.json")
        artifact.pop("closure_policy")
        self.assert_rejected(validate_manifest, artifact, "schema violation")

    def test_manifest_rejects_unexpected_property(self):
        artifact = load("valid_manifest.json")
        artifact["unexpected"] = True
        self.assert_rejected(validate_manifest, artifact, "schema violation")

    def test_production_intent_rejects_in_boundary_open_obligation(self):
        artifact = load("valid_manifest.json")
        artifact["unresolved_obligations"].append(
            {
                "obligation_id": "open-inside",
                "scope": "INSIDE_BOUNDARY",
                "description": "Must fail closed.",
                "status": "OPEN",
            }
        )
        self.assert_rejected(validate_manifest, artifact, "unresolved in-boundary")

    def test_production_intent_rejects_below_level_five_root(self):
        artifact = load("valid_manifest.json")
        artifact["root"]["programme_level"] = 4
        self.assert_rejected(validate_manifest, artifact, "Level 5")

    def test_replayable_certificate_equivalent_requires_admission_reference(self):
        artifact = load("valid_manifest.json")
        artifact["root"]["programme_level"] = 4
        artifact["root"]["replayable_certificate_equivalent"] = True
        self.assert_rejected(validate_manifest, artifact, "Level 5")

    def test_unpinned_environment_rejected(self):
        artifact = load("valid_manifest.json")
        artifact["proof_environment"]["pins"] = []
        self.assert_rejected(validate_manifest, artifact, "schema violation")

    def test_incomplete_boundary_rejected(self):
        artifact = load("valid_manifest.json")
        artifact["boundaries"][0].pop("authority_refs")
        self.assert_rejected(validate_manifest, artifact, "schema violation")

    def test_unclassified_boundary_rejected(self):
        artifact = load("valid_manifest.json")
        artifact["boundaries"][0]["trust_class"] = "UNCLASSIFIED"
        self.assert_rejected(validate_manifest, artifact, "schema violation")

    def test_direct_semantic_edge_requires_reviewed_authority(self):
        artifact = load("valid_manifest.json")
        artifact["direct_semantic_edges"][0]["authority_state"] = "PROPOSED"
        artifact["direct_semantic_edges"][0]["proposal_origin"] = {"origin": "HUMAN"}
        self.assert_rejected(validate_manifest, artifact, "must be REVIEWED_DIRECT")

    def test_direct_semantic_edge_requires_evidence(self):
        artifact = load("valid_manifest.json")
        artifact["direct_semantic_edges"][0].pop("evidence_refs")
        self.assert_rejected(validate_manifest, artifact, "schema violation")

    def test_derived_edge_cannot_be_direct_semantic_authority(self):
        artifact = load("valid_manifest.json")
        edge = artifact["direct_semantic_edges"][0]
        edge["authority_state"] = "DERIVED"
        edge["derivation"] = {
            "method": "transitive closure",
            "input_edge_ids": ["CMDG:E:OTHER"],
            "non_authoritative": True,
        }
        self.assert_rejected(validate_manifest, artifact, "must be REVIEWED_DIRECT")

    def test_implementation_import_cannot_be_semantic_relation(self):
        edge = load("valid_edge.json")
        edge["relation"] = "IMPLEMENTATION_IMPORT"
        self.assert_rejected(validate_edge, edge, "schema violation")

    def test_proof_dependency_cannot_be_semantic_relation(self):
        edge = load("valid_edge.json")
        edge["relation"] = "PROOF_USES_DECLARATION"
        self.assert_rejected(validate_edge, edge, "schema violation")

    def test_realizes_as_requires_realization_payload(self):
        edge = copy.deepcopy(load("valid_manifest.json")["realizations"][0])
        edge.pop("realization")
        self.assert_rejected(validate_edge, edge, "schema violation")

    def test_realizes_as_rejects_automatic_equivalence_claim(self):
        edge = copy.deepcopy(load("valid_manifest.json")["realizations"][0])
        edge["realization"]["automatic_claims"]["mathematical_equivalence"] = True
        self.assert_rejected(validate_edge, edge, "schema violation")

    def test_reconciler_proposal_cannot_self_promote(self):
        edge = load("valid_edge.json")
        edge["proposal_origin"] = {
            "origin": "SEMANTIC_GRAPH_RECONCILER",
            "tool": "cmdg-reconciler",
            "artifact_ref": "proposal:1",
        }
        self.assert_rejected(validate_edge, edge, "independent review")

    def test_reconciler_proposal_may_be_admitted_by_independent_review(self):
        edge = load("valid_edge.json")
        edge["proposal_origin"] = {
            "origin": "SEMANTIC_GRAPH_RECONCILER",
            "tool": "cmdg-reconciler",
            "artifact_ref": "proposal:1",
        }
        edge["review"]["independent_of_proposal_origin"] = True
        validate_edge(edge)

    def test_uncertified_equivalence_cannot_generate_quotient(self):
        artifact = load("valid_manifest.json")
        artifact["direct_semantic_edges"][1]["equivalence"]["quotient_admissibility"] = "NOT_ADMISSIBLE"
        artifact["direct_semantic_edges"][1]["equivalence"].pop("certification_ref")
        self.assert_rejected(validate_manifest, artifact, "not certified admissible")

    def test_quotient_generator_must_be_traceable_to_direct_edge(self):
        artifact = load("valid_manifest.json")
        artifact["quotient_projection"]["generator_edge_ids"] = ["CMDG:E:MISSING"]
        self.assert_rejected(validate_manifest, artifact, "not a direct semantic edge")

    def test_replay_must_bind_exact_environment(self):
        artifact = load("valid_manifest.json")
        artifact["replay"]["exact_environment_ref"] = "different-env"
        self.assert_rejected(validate_manifest, artifact, "must bind the declared proof environment")

    def test_claim_boundary_cannot_confer_graph_certified(self):
        artifact = load("valid_manifest.json")
        artifact["claim_boundary"]["graph_certified_conferred"] = True
        self.assert_rejected(validate_manifest, artifact, "schema violation")

    def test_global_completeness_claim_rejected(self):
        artifact = load("valid_manifest.json")
        artifact["semantic_scope"]["global_completeness_claim"] = True
        self.assert_rejected(validate_manifest, artifact, "schema violation")


if __name__ == "__main__":
    unittest.main()
