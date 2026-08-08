#!/usr/bin/env python3
"""Adversarial mutations for CMDG-VERTICAL-SPINE-V0-001."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_cmdg_vertical_spine_v0 import V0Error, validate_payload  # noqa: E402

RECORD = ROOT / "governance" / "cmdg_vertical_spine_v0_001.json"
NODES = ROOT / "fixtures" / "cmdg" / "vertical_spine_v0_001" / "nodes.json"
EDGES = ROOT / "fixtures" / "cmdg" / "vertical_spine_v0_001" / "edges.json"
LEAN = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "CMDGVerticalSpineV0.lean"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

class CMDGVerticalSpineV0Tests(unittest.TestCase):
    def setUp(self):
        self.record = load(RECORD)
        self.nodes = load(NODES)
        self.edges = load(EDGES)
        self.lean = LEAN.read_text(encoding="utf-8")

    def validate(self, record=None, nodes=None, edges=None, lean=None):
        validate_payload(
            self.record if record is None else record,
            self.nodes if nodes is None else nodes,
            self.edges if edges is None else edges,
            self.lean if lean is None else lean,
        )

    def rejected(self, needle, **kwargs):
        with self.assertRaises(V0Error) as caught:
            self.validate(**kwargs)
        self.assertIn(needle, str(caught.exception))

    def test_canonical_candidate(self):
        self.validate()

    def test_broken_endpoint_route_rejected(self):
        r = copy.deepcopy(self.record); r["route"]["ordered_nodes"].pop()
        self.rejected("BROKEN_V0_ROUTE", record=r)

    def test_proof_import_promoted_to_semantic_rejected(self):
        e = copy.deepcopy(self.edges)
        x = next(x for x in e if x["layer"] == "G_implementation")
        x["layer"] = "G_semantic"; x["relation"] = "REQUIRES_DEFINITION"
        self.rejected("EDGE_SCHEMA_VIOLATION", edges=e)

    def test_unclassified_reuse_rejected(self):
        n = copy.deepcopy(self.nodes); n[0]["engagement_mode"] = "UNKNOWN"
        self.rejected("NODE_SCHEMA_VIOLATION", nodes=n)

    def test_stale_mathlib_pin_rejected(self):
        r = copy.deepcopy(self.record); r["environment"]["mathlib_commit"] = "0" * 40
        self.rejected("PROOF_ENVIRONMENT_DRIFT", record=r)

    def test_semantic_edge_without_proposal_gate_rejected(self):
        e = copy.deepcopy(self.edges); e[0]["authority_state"] = "REVIEWED_DIRECT"; e[0]["evidence_refs"]=["x"]; e[0]["review"]={"reviewer":"x","disposition":"x","artifact_ref":"x"}
        self.rejected("UNREVIEWED_SEMANTIC_AUTHORITY", edges=e)

    def test_tool_origin_semantic_authority_rejected(self):
        e = copy.deepcopy(self.edges); e[0]["proposal_origin"]={"origin":"SEMANTIC_GRAPH_RECONCILER","tool":"reconciler","artifact_ref":"x"}
        self.rejected("TOOL_ORIGIN_SEMANTIC_AUTHORITY", edges=e)

    def test_uncertified_equivalence_rejected(self):
        e = copy.deepcopy(self.edges); e[0]["relation"]="EQUIVALENT_TO"; e[0]["equivalence"]={"quotient_admissibility":"NOT_ADMISSIBLE"}
        self.rejected("UNCERTIFIED_EQUIVALENCE_IN_V0", edges=e)

    def test_weakened_nat_anchor_rejected(self):
        r = copy.deepcopy(self.record); r["protected_reuse"][0]["artifact_blob_sha1"] = "0" * 40
        self.rejected("NAT_REUSE_IDENTITY_DRIFT", record=r)

    def test_weakened_euclid_anchor_rejected(self):
        r = copy.deepcopy(self.record); r["protected_reuse"][1]["authority"] = "RECONSTRUCTED"
        self.rejected("PROTECTED_AUTHORITY_REDEFINITION", record=r)

    def test_condensed_cardinality_boundary_rejected(self):
        r = copy.deepcopy(self.record); r["condensed_target_profile"]["formal_cardinality_policy"] = "CARDINAL_BOUNDED"
        self.rejected("CONDENSED_CARDINALITY_PROFILE_MISSING", record=r)

    def test_pyknotic_boundary_rejected(self):
        r = copy.deepcopy(self.record); r["condensed_target_profile"]["formal_source_characterization"] = "FULLY_CLAUSEN_SCHOLZE_CONCORDANT"
        self.rejected("PYKNOTIC_BOUNDARY_MISSING", record=r)

    def test_cm2_promotion_rejected(self):
        r = copy.deepcopy(self.record); r["condensed_target_profile"]["cm_scope"] = "CM0_CM2"
        self.rejected("CONDENSED_CM_SCOPE_OVERCLAIM", record=r)

    def test_graph_certified_promotion_rejected(self):
        r = copy.deepcopy(self.record); r["claim_boundary"]["graph_certified_conferred"] = True
        self.rejected("PROHIBITED_AUTHORITY_PROMOTION", record=r)

    def test_minimality_promotion_rejected(self):
        r = copy.deepcopy(self.record); r["claim_boundary"]["v0_unique_or_minimal"] = True
        self.rejected("PROHIBITED_AUTHORITY_PROMOTION", record=r)

    def test_missing_formal_interface_check_rejected(self):
        lean = self.lean.replace("#check Condensed.discreteUnderlyingAdj", "")
        self.rejected("FORMAL_INTERFACE_CHECK_MISSING", lean=lean)

    def test_local_axiom_rejected(self):
        self.rejected("FORMAL_INTERFACE_PLACEHOLDER_OR_AXIOM", lean=self.lean + "\naxiom bad : True\n")

if __name__ == "__main__":
    unittest.main()
