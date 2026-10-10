"""Fail-closed tests for the direct-editorial queue projector."""
import unittest
from unittest.mock import patch
from ci import erdos_catalogue_queue_projection as mod


class QueueProjectionTests(unittest.TestCase):
    def setUp(self):
        self.issue = 2491
        self.body = "RESULT/1\nASSIGNMENT_ID: ERDOS-CATALOGUE-1220-S01\n"
        import hashlib
        self.receipt = {"issue_number": self.issue, "problem_id": 1220,
                        "validation": "STRUCTURALLY_VALID_UNADJUDICATED",
                        "event_action": "created", "task_id": "ERDOS-CATALOGUE-1220-S01",
                        "comment_id": 77, "comment_body_sha256": hashlib.sha256(self.body.encode()).hexdigest()}
        self.report = {"tasks": [{"issue_number": self.issue, "task_id": self.receipt["task_id"]}],
                       "receipts": [self.receipt]}

    def test_registry_bound_valid_receipt(self):
        self.assertEqual(mod.validate_receipt(self.report, self.issue)["comment_id"], 77)

    def test_duplicate_fail_closed(self):
        with self.assertRaises(ValueError):
            mod.validate_receipt({**self.report, "receipts": [self.receipt, self.receipt]}, self.issue)

    def test_no_registry_binding_fail_closed(self):
        with self.assertRaises(ValueError):
            mod.validate_receipt({**self.report, "tasks": []}, self.issue)

    def test_invalid_result_fail_closed(self):
        bad = {**self.receipt, "validation": "REJECTED"}
        with self.assertRaises(ValueError):
            mod.validate_receipt({**self.report, "receipts": [bad]}, self.issue)

    @patch.object(mod, "gh")
    def test_missing_project_state_no_mutation(self, api):
        api.side_effect = [
            {"state": "open", "labels": [{"name": n} for n in ("gcl-job", "gcl-pickup:direct-editorial", "gcl-role:source-audit")]},
            {"issue_url": f"https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/issues/{self.issue}", "body": self.body},
            {"fields": [{"name": "Status", "id": "F", "options": [{"name": "Todo", "id": "T"}]}]},
            {"id": "PROJECT"},
            {"items": [{"id": "I", "content": {"url": f"https://github.com/grandchallenge/MATH-PROGRAMME/issues/{self.issue}"}}]},
        ]
        with self.assertRaisesRegex(ValueError, "no unique RETURNED state"):
            mod.reconcile(self.report, self.issue, False)
        self.assertEqual(api.call_count, 5)


if __name__ == "__main__":
    unittest.main()
