#!/usr/bin/env python3
"""Adversarial mutations for CMDG-CONDENSED-CM3-001."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_cmdg_condensed_cm3 import CM3Error, validate_payload  # noqa: E402

RECORD = ROOT / "governance" / "cmdg_condensed_cm3_001.json"
NODES = ROOT / "fixtures" / "cmdg" / "condensed_cm3_001" / "nodes.json"
EDGES = ROOT / "fixtures" / "cmdg" / "condensed_cm3_001" / "edges.json"
LEAN = ROOT / "fixtures" / "formal" / "CMDG-NAT-CONCORDANCE-001" / "CMDGCondensedCM3.lean"
EXTRACTOR = ROOT / "fixtures" / "cmdg" / "extractor_001" / "condensed_cm3.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


class CMDGCondensedCM3Tests(unittest.TestCase):
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
        with self.assertRaises(CM3Error):
            self.validate(**kwargs)

    def claim_overclaim(self, key):
        r = copy.deepcopy(self.record)
        r["claim_boundary"][key] = True
        self.rejected(record=r)

    def test_canonical_candidate(self): self.validate()

    def test_repository_baseline_drift_rejected(self):
        r = copy.deepcopy(self.record); r["repository_baseline"] = "0" * 40
        self.rejected(record=r)

    def test_cm2_identity_drift_rejected(self):
        r = copy.deepcopy(self.record); r["protected_cm2"]["merge_commit"] = "0" * 40
        self.rejected(record=r)

    def test_cm2_authority_redefinition_rejected(self):
        r = copy.deepcopy(self.record); r["protected_cm2"]["authority"] = "RECONSTRUCTED"
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

    def test_premature_semantic_promotion_rejected(self):
        e = copy.deepcopy(self.edges); x = next(x for x in e if x["layer"] == "G_semantic")
        x["authority_state"] = "REVIEWED_DIRECT"
        x["evidence_refs"] = ["x"]
        x["review"] = {"reviewer": "x", "disposition": "x", "artifact_ref": "x", "independent_of_proposal_origin": True}
        x.pop("proposal_origin", None)
        self.rejected(edges=e)

    def test_missing_abelian_witness_rejected(self):
        self.rejected(lean=self.lean.replace("noncomputable def cm3Abelian", "noncomputable def removedAbelian", 1))

    def test_missing_ab5_witness_rejected(self):
        self.rejected(lean=self.lean.replace("noncomputable def cm3AB5", "noncomputable def removedAB5", 1))

    def test_missing_ab4_witness_rejected(self):
        self.rejected(lean=self.lean.replace("noncomputable def cm3AB4", "noncomputable def removedAB4", 1))

    def test_missing_ab4star_witness_rejected(self):
        self.rejected(lean=self.lean.replace("noncomputable def cm3AB4Star", "noncomputable def removedAB4Star", 1))

    def test_local_axiom_rejected(self):
        self.rejected(lean=self.lean + "\naxiom bad : True\n")

    def test_grothendieck_overclaim_rejected(self): self.claim_overclaim("is_grothendieck_abelian_conferred")
    def test_separator_overclaim_rejected(self): self.claim_overclaim("separator_or_generator_conferred")
    def test_derived_overclaim_rejected(self): self.claim_overclaim("derived_category_or_ext_or_cohomology_conferred")
    def test_enough_injectives_overclaim_rejected(self): self.claim_overclaim("enough_injectives_or_projectives_conferred")
    def test_full_concordance_overclaim_rejected(self): self.claim_overclaim("full_clausen_scholze_concordance_conferred")
    def test_solid_liquid_overclaim_rejected(self): self.claim_overclaim("solid_or_liquid_conferred")
    def test_c04_beyond_cm3_rejected(self): self.claim_overclaim("c04_discharged_beyond_cm3")
    def test_c05_rejected(self): self.claim_overclaim("c05_discharged")
    def test_c06_rejected(self): self.claim_overclaim("c06_discharged")
    def test_graph_certified_rejected(self): self.claim_overclaim("graph_certified_conferred")

    def test_extractor_root_drift_rejected(self):
        e = copy.deepcopy(self.extractor); e["roots"] = ["CMDG.CondensedCM3.cm3AB5"]
        self.rejected(extractor=e)

    def test_extractor_authority_overclaim_rejected(self):
        e = copy.deepcopy(self.extractor); e["claim_boundary"]["semantic_authority_conferred"] = True
        self.rejected(extractor=e)


if __name__ == "__main__":
    unittest.main()
