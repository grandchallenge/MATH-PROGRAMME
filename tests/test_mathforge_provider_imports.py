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
    mathforge_provider_import_errors,
    provider_gate_errors,
)


class MathforgeProviderImportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_current_registry_passes(self) -> None:
        self.assertEqual(mathforge_provider_import_errors(self.registry), [])

    def test_omitted_campaign_fails_closed(self) -> None:
        altered = copy.deepcopy(self.registry)
        altered["campaigns"] = [
            item for item in altered["campaigns"] if item["campaign_id"] != "RH-001"
        ]
        errors = mathforge_provider_import_errors(altered)
        self.assertTrue(any("active campaign is uncovered: RH-001" in error for error in errors))
        self.assertTrue(provider_gate_errors("RH-001", "WP01", altered))

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
        self.assertEqual(provider_gate_errors("UNKNOWN", "DOCUMENTARY", self.registry), [])


if __name__ == "__main__":
    unittest.main()
