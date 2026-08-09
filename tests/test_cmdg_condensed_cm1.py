#!/usr/bin/env python3
"""Adversarial mutations for CMDG-CONDENSED-CM1-001."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_cmdg_condensed_cm1 import CM1Error, validate_payload  # noqa: E402

RECORD = ROOT / "governance" / "cmdg_condensed_cm1_001.json"
NODES = ROOT / "fixtures" / "cmdg" / "condensed_cm1_001" / "nodes.json"
EDGES = ROOT / "fixtures" / "cmdg" / "condensed_cm1_001" / "edges.json"
LEAN = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "CMDGCondensedCM1.lean"
EXTRACTOR = ROOT / "fixtures" / "cmdg" / "extractor_001" / "condensed_cm1.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class CMDGCondensedCM1Tests(unittest.TestCase):
    def setUp(self):
        self.record = load(RECORD)
        self.nodes = load(NODES)
        self.edges = load(EDGES)
        self.lean = LEAN.read_text(encoding="utf-8")
        self.extractor = load(EXTRACTOR)

    def validate(self, record=None, nodes=None, edges=None, lean=None, extractor=None):
        validate_payload(
            self.record if record is None else record,
            self.nodes if nodes is None else nodes,
            self.edges if edges is None else edges,
            self.lean if lean is None else lean,
            self.extractor if extractor is None else extractor,
        )

    def rejected(self, **kwargs):
        with self.assertRaises(CM1Error):
            self.validate(**kwargs)

    def test_canonical_candidate(self):
        self.validate()

    def test_stale_baseline_rejected(self):
        r = copy.deepcopy(self.record); r["protected_baseline"] = "0" * 40
        self.rejected(record=r)

    def test_stale_v0_blob_rejected(self):
        r = copy.deepcopy(self.record); r["protected_v0"]["record_blob_sha1"] = "0" * 40
        self.rejected(record=r)

    def test_v0_redefinition_rejected(self):
        r = copy.deepcopy(self.record); r["protected_v0"]["authority"] = "RECONSTRUCTED"
        self.rejected(record=r)

    def test_mathlib_pin_drift_rejected(self):
        r = copy.deepcopy(self.record); r["environment"]["mathlib_commit"] = "0" * 40
        self.rejected(record=r)

    def test_source_lineage_drift_rejected(self):
        r = copy.deepcopy(self.record); r["source_lineage"][0]["git_blob_sha1"] = "0" * 40
        self.rejected(record=r)

    def test_missing_node_rejected(self):
        n = copy.deepcopy(self.nodes); n.pop()
        self.rejected(nodes=n)

    def test_unclassified_node_rejected(self):
        n = copy.deepcopy(self.nodes); n[0]["engagement_mode"] = "REUSED"
        self.rejected(nodes=n)

    def test_premature_semantic_promotion_rejected(self):
        e = copy.deepcopy(self.edges); x = next(x for x in e if x["layer"] == "G_semantic")
        x["authority_state"] = "REVIEWED_DIRECT"; x["evidence_refs"] = ["x"]
        x["review"] = {"reviewer": "x", "disposition": "x", "artifact_ref": "x", "independent_of_proposal_origin": True}
        x.pop("proposal_origin", None)
        self.rejected(edges=e)

    def test_import_recast_as_semantic_rejected(self):
        e = copy.deepcopy(self.edges); x = next(x for x in e if x["layer"] == "G_implementation")
        x["layer"] = "G_semantic"; x["relation"] = "REQUIRES_DEFINITION"; x["authority_state"] = "PROPOSED"
        x["proposal_origin"] = {"origin": "HUMAN", "artifact_ref": "governance/cmdg_condensed_cm1_001.json"}
        self.rejected(edges=e)

    def test_missing_hom_equiv_rejected(self):
        self.rejected(lean=self.lean.replace("noncomputable def cm1HomEquiv", "noncomputable def removedHomEquiv"))

    def test_missing_unit_rejected(self):
        self.rejected(lean=self.lean.replace("noncomputable def cm1Unit", "noncomputable def removedUnit"))

    def test_missing_counit_rejected(self):
        self.rejected(lean=self.lean.replace("noncomputable def cm1Counit", "noncomputable def removedCounit"))

    def test_local_axiom_rejected(self):
        self.rejected(lean=self.lean + "\naxiom bad : True\n")

    def test_full_concordance_overclaim_rejected(self):
        r = copy.deepcopy(self.record); r["claim_boundary"]["full_clausen_scholze_concordance_conferred"] = True
        self.rejected(record=r)

    def test_discrete_fully_faithful_overclaim_rejected(self):
        r = copy.deepcopy(self.record); r["claim_boundary"]["discrete_fully_faithful_conferred"] = True
        self.rejected(record=r)

    def test_every_object_discrete_overclaim_rejected(self):
        r = copy.deepcopy(self.record); r["claim_boundary"]["every_condensed_object_discrete_claim"] = True
        self.rejected(record=r)

    def test_cm2_overclaim_rejected(self):
        r = copy.deepcopy(self.record); r["claim_boundary"]["cm2_or_stronger_conferred"] = True
        self.rejected(record=r)

    def test_graph_certified_overclaim_rejected(self):
        r = copy.deepcopy(self.record); r["claim_boundary"]["graph_certified_conferred"] = True
        self.rejected(record=r)

    def test_c04_beyond_cm1_rejected(self):
        r = copy.deepcopy(self.record); r["claim_boundary"]["c04_discharged_beyond_cm1"] = True
        self.rejected(record=r)

    def test_extractor_root_drift_rejected(self):
        e = copy.deepcopy(self.extractor); e["roots"] = ["CMDG.CondensedCM1.cm1HomEquiv"]
        self.rejected(extractor=e)

    def test_extractor_semantic_authority_overclaim_rejected(self):
        e = copy.deepcopy(self.extractor); e["claim_boundary"]["semantic_authority_conferred"] = True
        self.rejected(extractor=e)


if __name__ == "__main__":
    unittest.main()
