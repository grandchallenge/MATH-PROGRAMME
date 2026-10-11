"""Fail-closed, isolated source-critic queue contract tests."""
import copy
import json
import unittest
from pathlib import Path

from ci.erdos_rolling_review_queue import candidates, LABELS, FIELD_EXPECTED, TEXT_FIELDS

ROOT = Path(__file__).resolve().parents[1]


class ReviewQueueContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT/"governance/erdos_catalogue/ROLLING_RESEARCH_024.json").read_text())

    def test_exact_review_bindings(self):
        tasks = candidates(self.data)
        self.assertEqual(len(tasks), 16)
        self.assertEqual(len({x["issue"] for x in tasks}), 16)
        self.assertEqual({x["problem"] for x in tasks},
                         {99,101,138,241,470,593,595,1052,9,10,11,12,14,15,18,25})

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

    def test_deploy_only_existing_direct_editorial_labels(self):
        self.assertTrue({"gcl-job", "gcl-pickup:direct-editorial", "gcl-state:available"} <= LABELS)
        self.assertEqual(FIELD_EXPECTED["GCL State"], "AVAILABLE")
        self.assertEqual(TEXT_FIELDS["GCL Campaign"], "ERDOS-ROLLING-024-001")


if __name__ == "__main__":
    unittest.main()
