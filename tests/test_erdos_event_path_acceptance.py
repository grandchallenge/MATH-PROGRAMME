"""Bounded positive, duplicate, malformed, and edited-result event acceptance.

Hermetic: creates no issue comments and grants no mathematical authority.
Production issue-comment runs are checked separately through their run artifacts.
"""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ci import erdos_catalogue_programme_intake as intake
from ci import erdos_catalogue_queue_projection as projection
from tests.test_administrative_erdos_catalogue_intake import CatalogueIntakeTests


class EventPathAcceptance(unittest.TestCase):
    def setUp(self):
        fixture = CatalogueIntakeTests()
        fixture.setUp()
        self.registry = fixture.registry
        self.event = fixture.event
        self.issue = fixture.row["issue_number"]

    def _report(self, events):
        with tempfile.TemporaryDirectory() as directory:
            report = intake.build_report(self.registry, events, Path(directory))
            raw_count = len(list((Path(directory) / "returns").rglob("*.md")))
            return report, raw_count

    def test_fresh_positive_and_duplicate_are_single_current_return(self):
        report, count = self._report([self.event, copy.deepcopy(self.event)])
        self.assertEqual(1, count)
        self.assertEqual(1, report["summary"]["structurally_valid_current_returns"])
        receipt = projection.validate_receipt(report, self.issue)
        self.assertEqual("STRUCTURALLY_VALID_UNADJUDICATED", receipt["validation"])
        self.assertFalse(any(receipt["authority_effects"].values()))

    def test_malformed_and_edited_remain_rejected_and_versioned(self):
        bad = copy.deepcopy(self.event)
        bad["comment"]["id"] = 902
        bad["comment"]["body"] = "RESULT/1\nCANARY: MALFORMED"
        edited = copy.deepcopy(bad)
        edited["action"] = "edited"
        edited["comment"]["updated_at"] = "2026-10-10T00:01:00Z"
        edited["comment"]["body"] = "RESULT/1\nCANARY: ALTERED"
        report, count = self._report([self.event, bad, edited, copy.deepcopy(edited)])
        self.assertEqual(3, count)
        self.assertEqual(1, report["summary"]["structurally_valid_current_returns"])
        self.assertEqual(2, len([r for r in report["receipts"] if r["validation"] == "REJECTED"]))
        self.assertEqual(self.event["comment"]["id"], projection.validate_receipt(report, self.issue)["comment_id"])

    def test_mutated_valid_comment_requires_recapture_before_project_write(self):
        report, _ = self._report([self.event])
        changed = copy.deepcopy(self.event)
        changed["action"] = "edited"
        changed["comment"]["body"] += "\nUnreviewed change"
        changed["comment"]["updated_at"] = "2026-10-10T00:02:00Z"
        with patch.object(projection, "gh") as gh, patch.object(projection, "project_metadata") as metadata:
            gh.side_effect = [
                {"state": "open", "labels": [
                    {"name": x} for x in ("gcl-job","gcl-pickup:direct-editorial","gcl-role:source-audit")
                ]},
                {"issue_url": f"https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/issues/{self.issue}",
                 "body": changed["comment"]["body"]},
            ]
            with self.assertRaisesRegex(ValueError, "comment changed since capture"):
                projection.reconcile(report, self.issue, False)
            metadata.assert_not_called()

    def test_edited_away_valid_return_not_projectable(self):
        invalid = copy.deepcopy(self.event)
        invalid["action"] = "edited"
        invalid["comment"]["updated_at"] = "2026-10-10T00:03:00Z"
        invalid["comment"]["body"] = "Withdrawn"
        report, count = self._report([self.event, invalid])
        self.assertEqual(2, count)
        with self.assertRaisesRegex(ValueError, "exactly one current"):
            projection.validate_receipt(report, self.issue)


if __name__ == "__main__":
    unittest.main()
