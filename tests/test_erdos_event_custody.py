"""Hermetic acceptance of durable operational event custody and canary isolation."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from ci import erdos_event_custody as custody


class CustodyTests(unittest.TestCase):
    def setUp(self):
        self.event = {
            "repository": {"full_name": "grandchallenge/MATH-PROGRAMME"},
            "action": "created",
            "issue": {"number": 2491,
                      "title": "[GCL-ERDOS] ERDOS-CATALOGUE-1220-S01 — Problem 1220: audit"},
            "comment": {"id": 881, "body": "RESULT/1\nfixture",
                        "updated_at": "2026-10-10T00:00:00Z",
                        "user": {"id": 123, "login": "worker"}},
        }

    def test_event_identity_is_repeatable(self):
        a = custody.record(self.event)
        b = custody.record(copy.deepcopy(self.event))
        self.assertEqual(a, b)
        self.assertEqual(hashlib.sha256(__import__("base64").b64decode(a["raw"])).hexdigest(),
                         a["digest"])

    def test_edited_revision_has_distinct_event_key(self):
        edited = copy.deepcopy(self.event)
        edited["action"] = "edited"
        edited["comment"]["body"] = "Withdrawn"
        edited["comment"]["updated_at"] = "2026-10-10T00:01:00Z"
        self.assertNotEqual(custody.record(self.event)["key"], custody.record(edited)["key"])

    def test_non_catalogue_and_non_result_creation_are_rejected(self):
        other = copy.deepcopy(self.event)
        other["issue"]["number"] = custody.LEDGER
        with self.assertRaises(ValueError):
            custody.record(other)
        other = copy.deepcopy(self.event)
        other["comment"]["body"] = "ordinary text"
        with self.assertRaises(ValueError):
            custody.record(other)

    @patch.object(custody, "gh")
    def test_duplicate_delivery_does_not_append(self, gh):
        evidence = custody.record(self.event)
        marker = f"{custody.PREFIX}\nKEY: {evidence['key']}\n"
        gh.return_value = [[{"id": 3001, "body": marker +
                            f"PAYLOAD_SHA256: {evidence['digest']}\n"}]]
        result = custody.append(self.event)
        self.assertEqual(result["status"], "EXISTS")
        gh.assert_called_once()

    @patch.object(custody, "gh")
    def test_first_delivery_append_is_verified(self, gh):
        evidence = custody.record(self.event)
        def fake(*args, **kwargs):
            if "--paginate" in args:
                return [[]]
            if "-X" in args:
                self.assertIn("AUTHORITY: OPERATIONAL_EVENT_CUSTODY_ONLY", kwargs["payload"]["body"])
                self.body = kwargs["payload"]["body"]
                return {"id": 3002}
            return {"id": 3002, "body": self.body}
        gh.side_effect = fake
        self.assertEqual(custody.append(self.event)["status"], "APPENDED")
        self.assertEqual(gh.call_count, 3)


if __name__ == "__main__":
    unittest.main()
