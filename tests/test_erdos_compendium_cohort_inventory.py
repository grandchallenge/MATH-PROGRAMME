"""Live inventory must recognize authenticated returns after AVAILABLE is removed."""
import hashlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
import erdos_compendium_cohort_inventory as inventory


class CohortCustodyTests(unittest.TestCase):
    def setUp(self):
        body = "ERDOS-CATALOGUE-0447-S01\nhttps://www.erdosproblems.com/447\nsourcecommit"
        self.item = {
            "problem_id": 447, "audit_issue": 1717,
            "assignment_id": "ERDOS-CATALOGUE-0447-S01",
            "registry_issue_body_sha256": hashlib.sha256(body.encode()).hexdigest(),
            "source_return": "https://github.com/grandchallenge/MATH-PROGRAMME/issues/1717#issuecomment-123",
        }
        self.manifest = {
            "cohort_id": "EC-BULK-004", "source_registry_blob": "registry",
            "source": {"source_commit": "sourcecommit"},
            "items": [self.item] + [
                dict(self.item, problem_id=i, audit_issue=1717+i-447)
                for i in range(448, 647)
            ],
        }
        self.issue = {
            "number": 1717, "state": "open", "title": "ERDOS-CATALOGUE-0447-S01",
            "body": body, "html_url": "https://github.com/grandchallenge/MATH-PROGRAMME/issues/1717",
            "labels": [{"name": name} for name in inventory.LABELS],
        }
        self.comment = {
            "html_url": self.item["source_return"], "user": {"login": "fyremael"},
            "body": (
                "RESULT/1\nASSIGNMENT_ID: ERDOS-CATALOGUE-0447-S01\n"
                "PROBLEM_ID: 447\nDISPOSITION: PARTIAL\n"
                + "\n".join(inventory.valid_return.__globals__["REQUIRED_SECTIONS"])
            ),
        }

    def check(self, comments):
        with patch.object(inventory, "read_issue", return_value=self.issue):
            with patch.object(inventory, "get_comments", return_value=comments):
                return inventory.audit(self.manifest, "fake", 1)["records"][0]

    def test_verified_return_replaces_available(self):
        r = self.check([self.comment])
        self.assertEqual(r["exceptions"], [])
        self.assertEqual(r["queue_custody"], "AUTHENTICATED_RETURN_POSTED")

    def test_missing_available_without_verified_return_fails(self):
        self.assertIn("QUEUE_AVAILABLE_MISSING_WITHOUT_VERIFIED_RETURN", self.check([])["exceptions"])

    def test_available_label_needs_no_return(self):
        self.issue["labels"].append({"name": "gcl-state:available"})
        self.assertEqual(self.check([])["queue_custody"], "AVAILABLE")

    def test_wrong_return_identity_fails(self):
        bad = dict(self.comment, body=self.comment["body"].replace("PROBLEM_ID: 447", "PROBLEM_ID: 448"))
        self.assertIn("QUEUE_AVAILABLE_MISSING_WITHOUT_VERIFIED_RETURN", self.check([bad])["exceptions"])
