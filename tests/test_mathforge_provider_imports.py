from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from validate_mathforge_provider_imports import (  # noqa: E402
    REGISTRY_PATH,
    active_domain_campaign_ids,
    mathforge_provider_import_errors,
    provider_gate_errors,
)


class MathforgeProviderImportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_current_registry_passes(self) -> None:
        self.assertEqual(mathforge_provider_import_errors(self.registry), [])

    def test_all_active_domains_are_covered(self) -> None:
        imported = {item["campaign_id"] for item in self.registry["campaigns"]}
        self.assertTrue(active_domain_campaign_ids().issubset(imported))

    def test_omitted_campaign_fails_closed(self) -> None:
        altered = copy.deepcopy(self.registry)
        altered["campaigns"] = [
            item for item in altered["campaigns"] if item["campaign_id"] != "RH-001"
        ]
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(
            any("registered campaign is uncovered: RH-001" in error for error in errors)
        )
        self.assertTrue(provider_gate_errors("RH-001", "WP01", altered))

    def test_new_active_domain_fails_closed(self) -> None:
        errors = mathforge_provider_import_errors(
            self.registry,
            active_campaigns=active_domain_campaign_ids() | {"NEW-001"},
        )
        self.assertTrue(
            any("ACTIVE domain campaign is uncovered: NEW-001" in error for error in errors)
        )

    def test_provider_commit_drift_is_rejected(self) -> None:
        altered = copy.deepcopy(self.registry)
        altered["provider_commit"] = "0" * 40
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("provider commit drift" in error for error in errors))

    def test_manifest_identity_drift_is_rejected(self) -> None:
        altered = copy.deepcopy(self.registry)
        altered["campaigns"][0]["manifest_git_blob_sha1"] = "1" * 40
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("manifest identity drift" in error for error in errors))

    def test_supplemental_identity_drift_is_rejected(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = next(item for item in altered["campaigns"] if item["campaign_id"] == "RH-001")
        entry["supplemental_artifacts"][-1]["git_blob_sha1"] = "2" * 40
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("FC-GDM-001-RH-CONCORDANCE identity drift" in error for error in errors))
        self.assertTrue(provider_gate_errors("RH-001", "WP01", altered))

    def test_missing_supplemental_artifact_fails_closed(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = next(item for item in altered["campaigns"] if item["campaign_id"] == "NS-CI-001")
        entry["supplemental_artifacts"] = entry["supplemental_artifacts"][:-1]
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("supplemental artifact is missing" in error for error in errors))
        self.assertTrue(provider_gate_errors("NS-CI-001", "WP01", altered))

    def test_unregistered_supplement_on_other_campaign_fails(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = next(item for item in altered["campaigns"] if item["campaign_id"] == "HC-001")
        entry["supplemental_artifacts"] = copy.deepcopy(
            next(item for item in altered["campaigns"] if item["campaign_id"] == "RH-001")["supplemental_artifacts"]
        )
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("HC-001 has unregistered supplemental artifacts" in error for error in errors))

    def test_incomplete_waiver_fails_closed(self) -> None:
        altered = copy.deepcopy(self.registry)
        entry = altered["campaigns"][0]
        entry.clear()
        entry.update(
            {
                "campaign_id": "UC-001",
                "title": "Union-Closed waiver",
                "disposition": "waiver",
                "waiver": {
                    "approved_by": "Council",
                    "reason": "Temporary provider exception",
                    "scope": "WP00",
                    "review_on": "",
                },
            }
        )
        self.assertTrue(mathforge_provider_import_errors(altered))
        self.assertTrue(provider_gate_errors("UC-001", "WP00", altered))

    def test_non_provider_gated_stage_is_unaffected(self) -> None:
        self.assertEqual(
            provider_gate_errors("UNKNOWN", "DOCUMENTARY", self.registry), []
        )


if __name__ == "__main__":
    unittest.main()
