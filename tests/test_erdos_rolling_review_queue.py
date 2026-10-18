"""Fail-closed, isolated source-critic queue contract tests."""
import copy
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from ci.erdos_rolling_review_queue import (
    candidates, LABELS, FIELD_EXPECTED, TEXT_FIELDS,
    review_already_recorded, project_fields, ISSUE_FIELD_IDS,
    PROJECT_STATUS_FIELD_ID, project_status
)

ROOT = Path(__file__).resolve().parents[1]


class ReviewQueueContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT/"governance/erdos_catalogue/ROLLING_RESEARCH_024.json").read_text())

    def test_exact_review_bindings(self):
        tasks = candidates(self.data)
        self.assertEqual(len(tasks), 24)
        self.assertEqual(len({x["issue"] for x in tasks}), 24)
        self.assertEqual({x["problem"] for x in tasks},
                         {99,101,138,241,470,593,595,1052,9,10,11,12,14,15,18,25,17,30,32,33,36,39,40,41})

    def test_cannot_expand_scope(self):
        changed = copy.deepcopy(self.data)
        changed["items"].append(copy.deepcopy(changed["items"][0]))
        with self.assertRaises(ValueError):
            candidates(changed)

    def test_must_bind_prior_result(self):
        changed = copy.deepcopy(self.data)
        row = next(x for x in changed["items"] if x["problem_id"] == 11)
        row["worker_result_comment_id"] = None
        with self.assertRaises(ValueError):
            candidates(changed)

    def test_no_implicit_solve_authority(self):
        changed = copy.deepcopy(self.data)
        changed["items"][0]["claimable"] = True
        with self.assertRaises(ValueError):
            candidates(changed)

    def test_no_duplicate_critical_issue(self):
        changed = copy.deepcopy(self.data)
        first = next(x for x in changed["items"] if x["problem_id"] == 99)
        second = next(x for x in changed["items"] if x["problem_id"] == 101)
        second["source_critical_review_issue"] = first["source_critical_review_issue"]
        with self.assertRaises(ValueError):
            candidates(changed)

    def test_recorded_revise_is_not_reoffered(self):
        review = {"body": "GCL-CRITICAL-REVIEW/1\nDATE: 2026-10-10\nDISPOSITION: REVISE\n"}
        with patch("ci.erdos_rolling_review_queue.gh", return_value=[review]):
            self.assertEqual(review_already_recorded(2506), "REVISE")

    def test_recorded_blocked_is_not_reoffered(self):
        review = {"body": "GCL-CRITICAL-REVIEW/1\nDISPOSITION: BLOCKED\n"}
        with patch("ci.erdos_rolling_review_queue.gh", return_value=[review]):
            self.assertEqual(review_already_recorded(2520), "BLOCKED")

    def test_ambiguous_reviewer_dispositions_fail_closed(self):
        return_body = "GCL-CRITICAL-REVIEW/1\nDISPOSITION: REVISE\n"
        with patch("ci.erdos_rolling_review_queue.gh",
                   return_value=[{"body": return_body}, {"body": return_body}]):
            with self.assertRaises(ValueError):
                review_already_recorded(2506)

    def test_project_status_not_org_issue_fields(self):
        fields = {"fields": [
            {"name": "Status", "id": PROJECT_STATUS_FIELD_ID,
             "options": [{"name": "Todo", "id": "aa440011"}]}
        ]}
        with patch("ci.erdos_rolling_review_queue.gh", return_value=fields):
            self.assertEqual(project_fields()["Status"]["id"], PROJECT_STATUS_FIELD_ID)
        self.assertEqual(ISSUE_FIELD_IDS["GCL State"], 47953501)
        self.assertEqual(ISSUE_FIELD_IDS["GCL Cohort"], 47953514)

    def test_drifted_live_todo_id_is_rebound_and_not_trusted_blindly(self):
        fields = {"fields": [
            {"name": "Status", "id": PROJECT_STATUS_FIELD_ID,
             "options": [{"name": "Todo", "id": "bc123def"},
                         {"name": "Done", "id": "ff112233"}]}
        ]}
        with patch("ci.erdos_rolling_review_queue.gh", return_value=fields):
            self.assertEqual(project_fields()["Status"]["validated_todo_option_id"], "bc123def")

    def test_missing_or_ambiguous_live_todo_fails_closed(self):
        for options in ([], [{"name":"Todo","id":"garbage!"}],
                        [{"name":"Todo","id":"aaaa0000"}, {"name":"Todo","id":"bbbb1111"}]):
            fields = {"fields": [{"name":"Status","id":PROJECT_STATUS_FIELD_ID,
                                  "options": options}]}
            with patch("ci.erdos_rolling_review_queue.gh", return_value=fields):
                with self.assertRaises(ValueError):
                    project_fields()

    def test_graphql_status_readback_uses_gh_api(self):
        result = {"data": {"node": {"fieldValueByName": {
            "name": "Todo", "optionId": "bc123def"}}}}
        with patch("ci.erdos_rolling_review_queue.gh", return_value=result) as fn:
            self.assertEqual(project_status("PVTI_example"),
                             {"name":"Todo","optionId":"bc123def"})
        self.assertEqual(fn.call_args.args[:2], ("api", "graphql"))
        with patch("ci.erdos_rolling_review_queue.gh", return_value={"data":{}}):
            with self.assertRaises(ValueError):
                project_status("PVTI_example")

    def test_project_field_mismatch_blocks(self):
        fields = {"fields": [
            {"name": "Status", "id": "wrong",
             "options": [{"name": "Todo", "id": "aa440011"}]}
        ]}
        with patch("ci.erdos_rolling_review_queue.gh", return_value=fields):
            with self.assertRaises(ValueError):
                project_fields()

    def test_deploy_only_existing_direct_editorial_labels(self):
        self.assertTrue({"gcl-job", "gcl-pickup:direct-editorial", "gcl-state:available"} <= LABELS)
        self.assertEqual(FIELD_EXPECTED["GCL State"], "AVAILABLE")
        self.assertEqual(TEXT_FIELDS["GCL Campaign"], "ERDOS-ROLLING-024-001")


if __name__ == "__main__":
    unittest.main()
