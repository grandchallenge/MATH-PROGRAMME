#!/usr/bin/env python3
"""Adversarial mutation tests for CMDG C03 foundational profiles."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_cmdg_nat_foundations_profile import (  # noqa: E402
    FoundationProfileError,
    validate_profile,
)

PROFILE = ROOT / "governance" / "cmdg_nat_concordance_foundations_profile_001.json"


def load_profile():
    return json.loads(PROFILE.read_text(encoding="utf-8"))


class CMDGNatFoundationsProfileTests(unittest.TestCase):
    def assert_rejected(self, artifact, needle: str | None = None):
        with self.assertRaises(FoundationProfileError) as caught:
            validate_profile(artifact, validate_local_environment=False)
        if needle:
            self.assertIn(needle, str(caught.exception))

    def test_canonical_profile(self):
        validate_profile(load_profile())

    def test_missing_theory_identity(self):
        artifact = load_profile()
        artifact["syntactic_zfc_profile"].pop("zfc_theory_id")
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_missing_language_identity(self):
        artifact = load_profile()
        artifact["syntactic_zfc_profile"].pop("language")
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_incomplete_zf_inventory(self):
        artifact = load_profile()
        artifact["syntactic_zfc_profile"]["zf_axiom_inventory"].pop()
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_substituted_zf_axiom_rejected(self):
        artifact = load_profile()
        artifact["syntactic_zfc_profile"]["zf_axiom_inventory"][0]["axiom_id"] = "CHOICE"
        self.assert_rejected(artifact, "INCOMPLETE_ZF_AXIOM_INVENTORY")

    def test_separation_cannot_be_single_axiom(self):
        artifact = load_profile()
        entry = artifact["syntactic_zfc_profile"]["zf_axiom_inventory"][-2]
        entry["kind"] = "SINGLE_AXIOM"
        entry.pop("schema_parameterization")
        self.assert_rejected(artifact, "INCOMPLETE_ZF_AXIOM_INVENTORY")

    def test_replacement_schema_requires_parameterization(self):
        artifact = load_profile()
        artifact["syntactic_zfc_profile"]["zf_axiom_inventory"][-1].pop("schema_parameterization")
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_hidden_classicality_rejected(self):
        artifact = load_profile()
        artifact["syntactic_zfc_profile"]["logic"]["classicality_explicit"] = False
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_substrate_object_theory_conflation_rejected(self):
        artifact = load_profile()
        artifact["syntactic_zfc_profile"]["substrate_separation"]["conflation_prohibited"] = False
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_semantic_realizes_as_overclaim_rejected(self):
        artifact = load_profile()
        artifact["semantic_set_realization_profile"]["programme_realizes_as_status"] = "ADMITTED"
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_standard_model_overclaim_rejected(self):
        artifact = load_profile()
        artifact["semantic_set_realization_profile"]["nonclaims"]["standard_model"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_unreviewed_formula_crosswalk_promotion_rejected(self):
        artifact = load_profile()
        artifact["semantic_set_realization_profile"]["object_theory_obligation_status"][0][
            "programme_formula_crosswalk"
        ] = "DIRECT_DECLARATION_IDENTIFIED"
        self.assert_rejected(artifact, "UNREVIEWED_SET_THEORY_CROSSWALK_PROMOTION")

    def test_omitted_set_universe_profile_rejected(self):
        artifact = load_profile()
        artifact["semantic_set_realization_profile"].pop("universe_size_profile")
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_omitted_nno_universe_profile_rejected(self):
        artifact = load_profile()
        artifact["categorical_nno_profile"].pop("universe_size_profile")
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_malformed_nno_universal_property_rejected(self):
        artifact = load_profile()
        artifact["categorical_nno_profile"]["universal_property"]["equations"][1] = "succ ≫ h = s ≫ h"
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_nno_definitional_identity_overclaim_rejected(self):
        artifact = load_profile()
        artifact["categorical_nno_profile"]["uniqueness_status"]["definitional_identity"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_nno_coproduct_assumption_scope_drift_rejected(self):
        artifact = load_profile()
        artifact["categorical_nno_profile"]["ambient_category"]["binary_coproducts_required"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_dtt_nat_identity_drift_rejected(self):
        artifact = load_profile()
        artifact["dtt_nat_profile"]["declaration"] = "Natural"
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_dtt_set_definitional_identity_overclaim_rejected(self):
        artifact = load_profile()
        artifact["dtt_nat_profile"]["nonclaims"]["definitional_identity"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_realizes_as_edge_promotion_rejected(self):
        artifact = load_profile()
        artifact["cross_foundational_relation_policy"]["current_promoted_edges"] = [
            "CMDG:E:N_DTT_REALIZES_N_ZFC"
        ]
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_foundational_concordance_promotion_rejected(self):
        artifact = load_profile()
        artifact["cross_foundational_relation_policy"]["foundational_concordance_status"] = "ESTABLISHED"
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_graph_certified_promotion_rejected(self):
        artifact = load_profile()
        artifact["claim_boundary"]["graph_certified_conferred"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_artifact_alone_cannot_discharge_c03(self):
        artifact = load_profile()
        artifact["claim_boundary"]["profile_prerequisite_satisfied_by_artifact_alone"] = True
        self.assert_rejected(artifact, "SCHEMA_VIOLATION")

    def test_missing_future_relation_directionality_rejected(self):
        artifact = load_profile()
        artifact["cross_foundational_relation_policy"]["evidence_requirements"].remove(
            "EXPLICIT_DIRECTION"
        )
        self.assert_rejected(artifact, "FOUNDATIONAL_RELATION_EVIDENCE_INCOMPLETE")

    def test_choice_is_the_only_directly_identified_programme_crosswalk(self):
        artifact = load_profile()
        choice = next(
            item
            for item in artifact["semantic_set_realization_profile"]["object_theory_obligation_status"]
            if item["object_theory_item"] == "CHOICE"
        )
        choice["programme_formula_crosswalk"] = "NOT_YET_ADMITTED"
        self.assert_rejected(artifact, "CHOICE_DECLARATION_NOT_IDENTIFIED")


if __name__ == "__main__":
    unittest.main()
