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

    def test_duplicate_delivery_is_idempotent(self):
        receipt = mod.validate_receipt({**self.report, "receipts": [self.receipt, self.receipt]}, self.issue)
        self.assertEqual(self.receipt["comment_id"], receipt["comment_id"])

    def test_no_registry_binding_fail_closed(self):
        with self.assertRaises(ValueError):
            mod.validate_receipt({**self.report, "tasks": []}, self.issue)

    def test_invalid_result_fail_closed(self):
        bad = {**self.receipt, "validation": "REJECTED"}
        with self.assertRaises(ValueError):
            mod.validate_receipt({**self.report, "receipts": [bad]}, self.issue)

    @patch.object(mod, "graph")
    def test_missing_project_state_no_mutation(self, graphql):
        graphql.return_value = {"organization": {"projectV2": {
            "id": "PROJECT", "fields": {"pageInfo": {"hasNextPage": False},
            "nodes": [{"name": "Status", "id": "F", "options": [{"name": "Todo", "id": "T"}]}]}
        }}}
        with self.assertRaisesRegex(ValueError, "one RETURNED option"):
            mod.project_metadata()
        graphql.assert_called_once()

    @patch.object(mod, "graph")
    def test_targeted_project_membership_and_status(self, graphql):
        graphql.return_value = {"repository": {"issue": {
            "projectItems": {"pageInfo": {"hasNextPage": False}, "nodes": [
                {"id": "ITEM", "project": {"id": "PROJECT", "number": 2},
                 "fieldValueByName": {"name": "RETURNED"}}
            ]}
        }}}
        self.assertEqual(mod.issue_project_item(self.issue, "PROJECT"),
                         {"id": "ITEM", "status": "RETURNED"})
        self.assertEqual(graphql.call_count, 1)

    @patch.object(mod, "graph")
    def test_targeted_project_membership_ambiguity_fails_closed(self, graphql):
        graphql.return_value = {"repository": {"issue": {
            "projectItems": {"pageInfo": {"hasNextPage": True}, "nodes": []}
        }}}
        with self.assertRaisesRegex(ValueError, "paginated"):
            mod.issue_project_item(self.issue, "PROJECT")


if __name__ == "__main__":
    unittest.main()
