from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
from agent_routine_review import (  # noqa: E402
    APP_REVIEWER, REMOVE_EXACTLY, REQUIRED_HEAD_CONTEXTS, REPOSITORY,
    RoutineReviewError, candidate_number, eligible_image_removal,
    removed_patch_text, required_contexts_green,
)


class RoutineAgentReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.head = "a" * 40
        self.pr = {
            "state": "open", "draft": False, "changed_files": 1,
            "head": {"sha": self.head, "repo": {"full_name": REPOSITORY}},
            "base": {"ref": "main"},
            "user": {"login": "fyremael"},
        }
        self.files = [{
            "filename": "docs/index.md", "status": "modified",
            "additions": 0, "deletions": 6,
            "patch": "@@ -1,10 +1,4 @@ context\n"
                + "".join("-" + line for line in REMOVE_EXACTLY.splitlines(keepends=True))
                + " context unchanged\n",
        }]

    def test_exact_image_removal_is_routine(self) -> None:
        eligible_image_removal(self.pr, self.files, self.head)
        self.assertEqual(removed_patch_text(self.files[0]["patch"]), REMOVE_EXACTLY)

    def test_adversarial_claim_deletion_is_rejected(self) -> None:
        files = copy.deepcopy(self.files)
        files[0]["patch"] = files[0]["patch"].replace(
            "-## The GCL continuity fabric", "-## Proof of the Riemann hypothesis"
        )
        with self.assertRaisesRegex(RoutineReviewError, "deletion content"):
            eligible_image_removal(self.pr, files, self.head)

    def test_adversarial_added_claim_is_rejected(self) -> None:
        files = copy.deepcopy(self.files)
        files[0]["patch"] += "+Theorem CM4 proved by this edit.\n"
        with self.assertRaisesRegex(RoutineReviewError, "unexpected added"):
            eligible_image_removal(self.pr, files, self.head)

    def test_unknown_file_fails_closed(self) -> None:
        files = copy.deepcopy(self.files)
        files[0]["filename"] = "fixtures/formal/CMDG-NAT-CONCORDANCE-001/test.lean"
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(self.pr, files, self.head)

    def test_unsafe_multi_file_scope_fails_closed(self) -> None:
        pr = copy.deepcopy(self.pr)
        pr["changed_files"] = 2
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(pr, self.files, self.head)

    def test_reviewer_does_not_review_own_work(self) -> None:
        pr = copy.deepcopy(self.pr)
        pr["user"]["login"] = APP_REVIEWER
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(pr, self.files, self.head)

    def test_stale_head_fails_closed(self) -> None:
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(self.pr, self.files, "b" * 40)

    def test_external_fork_fails_closed(self) -> None:
        pr = copy.deepcopy(self.pr)
        pr["head"]["repo"]["full_name"] = "random/MATH-PROGRAMME"
        with self.assertRaises(RoutineReviewError):
            eligible_image_removal(pr, self.files, self.head)

    def test_missing_context_fails_closed(self) -> None:
        checks = [
            {"name": name, "status": "completed", "conclusion": "success"}
            for name in REQUIRED_HEAD_CONTEXTS if name != "routing-enforcement"
        ]
        with self.assertRaisesRegex(RoutineReviewError, "missing"):
            required_contexts_green(checks, [])

    def test_pending_context_fails_closed(self) -> None:
        checks = [
            {"name": name, "status": "completed", "conclusion": "success"}
            for name in REQUIRED_HEAD_CONTEXTS if name != "validate-json"
        ]
        checks.append({"name": "validate-json", "status": "in_progress"})
        with self.assertRaisesRegex(RoutineReviewError, "failed_or_pending"):
            required_contexts_green(checks, [])

    def test_all_checks_and_routing_green(self) -> None:
        checks = [
            {"name": name, "status": "completed", "conclusion": "success"}
            for name in REQUIRED_HEAD_CONTEXTS if name != "routing-enforcement"
        ]
        required_contexts_green(
            checks, [{"context": "routing-enforcement", "state": "success"}]
        )

    def test_workflow_event_must_bind_one_sha_and_one_pr(self) -> None:
        self.assertEqual(
            candidate_number({
                "workflow_run": {
                    "event": "pull_request", "conclusion": "success",
                    "head_sha": self.head,
                    "repository": {"full_name": REPOSITORY},
                    "pull_requests": [{"number": 1246}],
                },
            }, "workflow_run"), (1246, self.head),
        )
        self.assertIsNone(candidate_number({
            "workflow_run": {"event": "pull_request", "conclusion": "success",
                             "head_sha": self.head,
                             "repository": {"full_name": REPOSITORY},
                             "pull_requests": []},
        }, "workflow_run"))


if __name__ == "__main__":
    unittest.main()
