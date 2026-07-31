from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_mathforge_provider_imports import (  # noqa: E402
    EXPECTED_CAMPAIGN_ARTIFACT_IDS,
    EXPECTED_EXPANDED_EVIDENCE,
    EXPECTED_PROVIDER_COMMIT,
    REGISTRY_PATH,
    active_domain_campaign_ids,
    mathforge_provider_import_errors,
    provider_gate_errors,
)


class MathforgeProviderImportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def campaign(self, campaign_id: str, registry: dict | None = None) -> dict:
        source = registry if registry is not None else self.registry
        return next(item for item in source["campaigns"] if item["campaign_id"] == campaign_id)

    def test_current_registry_passes(self) -> None:
        self.assertEqual(mathforge_provider_import_errors(self.registry), [])

    def test_exact_merged_provider_and_replay_are_pinned(self) -> None:
        self.assertEqual(self.registry["provider_commit"], EXPECTED_PROVIDER_COMMIT)
        self.assertEqual(self.registry["expanded_evidence"], EXPECTED_EXPANDED_EVIDENCE)
        self.assertEqual(
            self.registry["expanded_evidence"]["replay"]["archive_sha256"],
            "1c74747519c17f873f323198a92104538667092f3274a667a09e1a6b219a7bcb",
        )
        self.assertEqual(self.registry["expanded_evidence"]["snapshot"]["statement_count"], 43)
        self.assertEqual(self.registry["expanded_evidence"]["inventory"]["problem_count"], 3232)

    def test_all_active_domains_are_covered(self) -> None:
        imported = {item["campaign_id"] for item in self.registry["campaigns"]}
        self.assertTrue(active_domain_campaign_ids().issubset(imported))

    def test_coverage_modes_are_not_upgraded_by_supplements(self) -> None:
        observed = {item["campaign_id"]: item["coverage_mode"] for item in self.registry["campaigns"]}
        self.assertEqual(observed["UC-001"], "native")
        self.assertEqual(observed["HC-001"], "native")
        for campaign_id in ("BSD-001", "PNP-001", "RH-001", "YM-001", "OZ-001"):
            self.assertEqual(observed[campaign_id], "retrospective")

    def test_omitted_campaign_fails_closed(self) -> None:
        altered = copy.deepcopy(self.registry)
        altered["campaigns"] = [item for item in altered["campaigns"] if item["campaign_id"] != "RH-001"]
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("registered campaign is uncovered: RH-001" in error for error in errors))
        self.assertTrue(provider_gate_errors("RH-001", "WP01", altered))

    def test_new_active_domain_fails_closed(self) -> None:
        errors = mathforge_provider_import_errors(self.registry, active_campaigns=active_domain_campaign_ids() | {"NEW-001"})
        self.assertTrue(any("ACTIVE domain campaign is uncovered: NEW-001" in error for error in errors))

    def test_provider_commit_drift_is_rejected(self) -> None:
        altered = copy.deepcopy(self.registry)
        altered["provider_commit"] = "0" * 40
        self.assertTrue(any("provider commit drift" in error for error in mathforge_provider_import_errors(altered)))

    def test_expanded_replay_identity_drift_is_rejected(self) -> None:
        altered = copy.deepcopy(self.registry)
        altered["expanded_evidence"]["snapshot"]["sha256"] = "0" * 64
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("expanded replay evidence identity drift" in error for error in errors))
        self.assertTrue(provider_gate_errors("OZ-001", "WP01", altered))

    def test_manifest_identity_drift_is_rejected(self) -> None:
        altered = copy.deepcopy(self.registry)
        altered["campaigns"][0]["manifest_git_blob_sha1"] = "1" * 40
        self.assertTrue(any("manifest identity drift" in error for error in mathforge_provider_import_errors(altered)))

    def test_supplemental_identity_drift_is_rejected(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = self.campaign("UC-001", altered)
        entry["supplemental_artifacts"][-1]["git_blob_sha1"] = "2" * 40
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("FC-GDM-002-UC-CONCORDANCE identity drift" in error for error in errors))
        self.assertTrue(provider_gate_errors("UC-001", "WP01", altered))

    def test_missing_common_expansion_artifact_fails_closed(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = self.campaign("PNP-001", altered)
        entry["supplemental_artifacts"] = [item for item in entry["supplemental_artifacts"] if item["artifact_id"] != "FC-GDM-002-LOCK"]
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("FC-GDM-002-LOCK" in error and "missing" in error for error in errors))
        self.assertTrue(provider_gate_errors("PNP-001", "WP00", altered))

    def test_partial_odd_zeta_lattice_fails_closed(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = self.campaign("OZ-001", altered)
        entry["supplemental_artifacts"] = [item for item in entry["supplemental_artifacts"] if item["artifact_id"] != "FC-GDM-002-OZ-ODD-INFINITUDE-CONCORDANCE"]
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("OZ-ODD-INFINITUDE" in error and "missing" in error for error in errors))
        self.assertTrue(provider_gate_errors("OZ-001", "WP01", altered))

    def test_all_expanded_campaigns_have_exact_expected_artifacts(self) -> None:
        for campaign_id in ("UC-001", "PNP-001", "OZ-001", "BSD-001", "HC-001", "YM-001"):
            actual = {item["artifact_id"] for item in self.campaign(campaign_id)["supplemental_artifacts"]}
            self.assertEqual(actual, set(EXPECTED_CAMPAIGN_ARTIFACT_IDS[campaign_id]), campaign_id)

    def test_unregistered_supplement_fails(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = self.campaign("HC-001", altered)
        extra = copy.deepcopy(entry["supplemental_artifacts"][-1])
        extra["artifact_id"] = "FC-GDM-002-UNREGISTERED"
        entry["supplemental_artifacts"].append(extra)
        self.assertTrue(any("unregistered supplemental artifact" in error for error in mathforge_provider_import_errors(altered)))

    def test_incomplete_waiver_fails_closed(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = altered["campaigns"][0]
        entry.clear()
        entry.update({"campaign_id":"UC-001","title":"Union-Closed waiver","disposition":"waiver","waiver":{"approved_by":"Council","reason":"Temporary provider exception","scope":"WP00","review_on":""}})
        self.assertTrue(mathforge_provider_import_errors(altered))
        self.assertTrue(provider_gate_errors("UC-001", "WP00", altered))

    def test_non_provider_gated_stage_is_unaffected(self) -> None:
        self.assertEqual(provider_gate_errors("UNKNOWN", "DOCUMENTARY", self.registry), [])


if __name__ == "__main__":
    unittest.main()
