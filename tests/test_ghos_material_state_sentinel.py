from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ghos_material_state_sentinel",
    ROOT / "ci" / "ghos_material_state_sentinel.py",
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class EstateMembershipSentinelTests(unittest.TestCase):
    def campaign(self) -> dict:
        return {
            "campaign_id": "GHOS-ESTATE-ROLLOUT-001",
            "estate": [
                {"repository": "grandchallenge/A", "repository_id": 1},
                {"repository": "grandchallenge/B", "repository_id": 2},
            ],
        }

    def live(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "repositories": [
                {"repository": "grandchallenge/A", "repository_id": 1, "archived": False},
                {"repository": "grandchallenge/B", "repository_id": 2, "archived": False},
            ],
        }

    def test_matching_membership_is_unchanged(self):
        report = MODULE.classify_estate_membership(self.campaign(), self.live())
        self.assertEqual(report["result"], MODULE.UNCHANGED)
        self.assertEqual(report["route"], MODULE.ROUTES[MODULE.UNCHANGED])
        self.assertEqual(report["findings"]["errors"], [])

    def test_new_repository_routes_successor_admission_without_auto_admission(self):
        live = self.live()
        live["repositories"].append(
            {
                "repository": "grandchallenge/GCT-EXECUTIVE",
                "repository_id": 1355707445,
                "archived": False,
            }
        )
        report = MODULE.classify_estate_membership(self.campaign(), live)
        self.assertEqual(report["result"], MODULE.NEW_ESTATE_MEMBER)
        self.assertEqual(
            report["findings"]["new_repositories"],
            [
                {
                    "repository": "grandchallenge/GCT-EXECUTIVE",
                    "repository_id": 1355707445,
                    "archived": False,
                }
            ],
        )
        self.assertFalse(report["authority_boundary"]["may_admit_repository"])
        self.assertFalse(report["historical_terminal_rewrite_permitted"])

    def test_archived_baseline_repository_routes_successor_disposition(self):
        live = self.live()
        live["repositories"][1]["archived"] = True
        report = MODULE.classify_estate_membership(self.campaign(), live)
        self.assertEqual(report["result"], MODULE.ESTATE_MEMBER_REMOVED_OR_ARCHIVED)
        self.assertEqual(
            report["findings"]["archived_baseline_repositories"],
            [{"repository": "grandchallenge/B", "repository_id": 2}],
        )

    def test_missing_baseline_repository_routes_successor_disposition(self):
        live = self.live()
        live["repositories"].pop()
        report = MODULE.classify_estate_membership(self.campaign(), live)
        self.assertEqual(report["result"], MODULE.ESTATE_MEMBER_REMOVED_OR_ARCHIVED)
        self.assertEqual(
            report["findings"]["missing_baseline_repositories"],
            [{"repository": "grandchallenge/B", "repository_id": 2}],
        )

    def test_identity_replacement_fails_closed(self):
        live = self.live()
        live["repositories"][0]["repository_id"] = 99
        report = MODULE.classify_estate_membership(self.campaign(), live)
        self.assertEqual(report["result"], MODULE.UNKNOWN_FAIL_CLOSED)
        self.assertTrue(
            any("identity mismatch" in error for error in report["findings"]["errors"])
        )

    def test_duplicate_live_identity_fails_closed(self):
        live = self.live()
        live["repositories"].append(
            {"repository": "grandchallenge/C", "repository_id": 2, "archived": False}
        )
        report = MODULE.classify_estate_membership(self.campaign(), live)
        self.assertEqual(report["result"], MODULE.UNKNOWN_FAIL_CLOSED)
        self.assertTrue(
            any("duplicate repository_id" in error for error in report["findings"]["errors"])
        )

    def test_mixed_addition_and_removal_fails_closed(self):
        live = self.live()
        live["repositories"].pop()
        live["repositories"].append(
            {"repository": "grandchallenge/C", "repository_id": 3, "archived": False}
        )
        report = MODULE.classify_estate_membership(self.campaign(), live)
        self.assertEqual(report["result"], MODULE.UNKNOWN_FAIL_CLOSED)
        self.assertTrue(
            any(
                "simultaneous new and removed/archived" in error
                for error in report["findings"]["errors"]
            )
        )

    def test_protected_campaign_population_parses_as_fourteen(self):
        campaign = json.loads(
            (ROOT / "governance" / "ghos_estate_rollout_campaign.json").read_text(
                encoding="utf-8"
            )
        )
        live = {
            "schema_version": "1.0.0",
            "repositories": [
                {
                    "repository": item["repository"],
                    "repository_id": item["repository_id"],
                    "archived": False,
                }
                for item in campaign["estate"]
            ],
        }
        report = MODULE.classify_estate_membership(campaign, live)
        self.assertEqual(report["result"], MODULE.UNCHANGED)
        self.assertEqual(report["baseline"]["repository_count"], 14)
        self.assertEqual(report["observed"]["repository_count"], 14)


if __name__ == "__main__":
    unittest.main()
