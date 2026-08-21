from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
MODULE_PATH = ROOT / "ci" / "administrative_autonomy_runtime_receipt_behind_resume.py"
SPEC = importlib.util.spec_from_file_location("administrative_autonomy_runtime_receipt_behind_resume", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class FakeCandidate:
    def __init__(self, *, mergeable: bool | None = True, merge_state: str = "blocked", pull_count: int = 1, at_current: bool = False) -> None:
        self.branch = "automation/maintenance/receipt-structural_sweep-20260814T083300Z"
        self.declared_base = "a" * 40
        self.current_base = "b" * 40
        self.old_head = "1" * 40
        self.new_head = "2" * 40
        self.head = self.old_head
        self.mergeable = mergeable
        self.merge_state = merge_state
        self.pull_count = pull_count
        self.at_current = at_current
        self.update_payloads: list[dict[str, str]] = []

    def _pull(self) -> dict:
        return {
            "number": 529,
            "state": "open",
            "draft": False,
            "node_id": "PR_test",
            "mergeable": self.mergeable,
            "mergeable_state": self.merge_state,
            "head": {"ref": self.branch, "sha": self.head, "repo": {"full_name": "grandchallenge/MATH-PROGRAMME"}},
            "base": {"ref": "main"},
        }

    def get(self, path: str):
        prefix = "/repos/grandchallenge/MATH-PROGRAMME/git/ref/heads/"
        if path.startswith(prefix):
            ref = unquote(path[len(prefix):])
            if ref == self.branch:
                return {"object": {"sha": self.head}}
            if ref == "main":
                return {"object": {"sha": self.current_base}}
            raise AssertionError(path)
        if "/pulls?" in path:
            return [self._pull() for _ in range(self.pull_count)]
        if path == "/repos/grandchallenge/MATH-PROGRAMME/pulls/529":
            return self._pull()
        if path == "/repos/grandchallenge/MATH-PROGRAMME/pulls/529/files?per_page=100":
            return [{"filename": module.STATE_PATH, "additions": 14, "deletions": 3}]
        compare = "/repos/grandchallenge/MATH-PROGRAMME/compare/"
        if path.startswith(compare):
            pair = path[len(compare):]
            ancestor, descendant = pair.split("...", 1)
            if ancestor == descendant:
                return {"status": "identical"}
            if ancestor == self.current_base and descendant == self.head:
                return {"status": "ahead" if self.at_current else "diverged"}
            if ancestor == self.declared_base and descendant in {self.head, self.current_base}:
                return {"status": "ahead"}
            return {"status": "diverged"}
        if path.startswith("/repos/grandchallenge/MATH-PROGRAMME/commits/") and path.endswith("/check-runs?per_page=100"):
            return {"check_runs": []}
        raise AssertionError(path)

    def put(self, path: str, payload: dict):
        if path != "/repos/grandchallenge/MATH-PROGRAMME/pulls/529/update-branch":
            raise AssertionError(path)
        self.update_payloads.append(copy.deepcopy(payload))
        self.head = self.new_head
        self.at_current = True
        return {"message": "Updating pull request branch."}


class ReceiptBehindResumeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.control = {
            "control_id": "MP-ADMIN-RECEIPT-BEHIND-RESUME-001",
            "status": "ACTIVE_WHEN_PROTECTED",
            "repository": "grandchallenge/MATH-PROGRAMME",
            "synchronization": {
                "branch_prefix": module.RECEIPT_BRANCH_PREFIX, "base_branch": "main", "state_path": module.STATE_PATH,
                "expected_head_required": True, "single_open_pull_required": True, "same_repository_required": True,
                "exact_payload_required_before_and_after_sync": True, "synchronize_only_when_behind": True,
                "clean_resume_allowed": True, "merge_state_wait_seconds": 1, "head_change_wait_seconds": 1,
                "poll_interval_seconds": 0, "fresh_exact_head_checks_required": True,
                "fresh_referee_disposition_required": True, "ordinary_protected_merge_required": True,
            },
            "authority_boundary": {"human_steward_identity_asserted": False, "bypass_may_be_exercised": False, "direct_protected_push": False},
            "claim_boundaries": {"mathematical_target_proved": False, "campaign_admitted": False, "source_verified": False, "cert_route_registered": False, "adjudication_authorized": False, "certificate_issued": False, "external_claim_authorized": False},
        }
        self.completion = {"schema_version": "1.0.0", "control_id": "MP-ADMIN-MAINT-001", "derived_from_protected_head": "a" * 40, "state": "PROTECTED_RECEIPT_DERIVED", "procedures": {}, "authority_boundary": {}}

    def _loader(self, expected=None):
        value = self.completion if expected is None else expected
        return lambda _client, _repo, _path, _ref: copy.deepcopy(value)

    def test_blocked_advisory_but_typed_behind_uses_expected_head(self) -> None:
        candidate = FakeCandidate(mergeable=True, merge_state="blocked")
        result = module.resume_existing_receipt(candidate, "grandchallenge/MATH-PROGRAMME", candidate.branch, self.completion, self.control, completion_loader=self._loader())
        assert result is not None
        _, head, event = result
        self.assertEqual(candidate.new_head, head)
        self.assertEqual([{"expected_head_sha": candidate.old_head}], candidate.update_payloads)
        self.assertEqual("BEHIND_CURRENT_BASE", event["branch_state"])
        self.assertEqual("blocked", event["raw_advisory"]["mergeable_state"])
        self.assertTrue(event["expected_head_used"])

    def test_at_current_base_resumes_even_when_raw_advisory_blocked(self) -> None:
        candidate = FakeCandidate(at_current=True, merge_state="blocked")
        result = module.resume_existing_receipt(candidate, "grandchallenge/MATH-PROGRAMME", candidate.branch, self.completion, self.control, completion_loader=self._loader())
        assert result is not None
        _, head, event = result
        self.assertEqual(candidate.old_head, head)
        self.assertEqual([], candidate.update_payloads)
        self.assertEqual("AT_CURRENT_BASE", event["branch_state"])

    def test_true_content_conflict_fails_closed(self) -> None:
        candidate = FakeCandidate(mergeable=False)
        with self.assertRaisesRegex(module.AutonomyError, "true content conflict"):
            module.resume_existing_receipt(candidate, "grandchallenge/MATH-PROGRAMME", candidate.branch, self.completion, self.control, completion_loader=self._loader())
        self.assertEqual([], candidate.update_payloads)

    def test_payload_drift_fails_before_update(self) -> None:
        candidate = FakeCandidate()
        drift = copy.deepcopy(self.completion); drift["state"] = "DRIFT"
        with self.assertRaises(module.AutonomyError):
            module.resume_existing_receipt(candidate, "grandchallenge/MATH-PROGRAMME", candidate.branch, self.completion, self.control, completion_loader=self._loader(drift))
        self.assertEqual([], candidate.update_payloads)

    def test_multiple_open_receipt_pulls_fail_closed(self) -> None:
        candidate = FakeCandidate(pull_count=2)
        with self.assertRaises(module.AutonomyError):
            module.resume_existing_receipt(candidate, "grandchallenge/MATH-PROGRAMME", candidate.branch, self.completion, self.control, completion_loader=self._loader())

    def test_runtime_reactivation_preserves_generic_behind_sync(self) -> None:
        text = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(encoding="utf-8")
        executor_import = "import administrative_autonomy_runtime_behind_sync as behind_sync"
        self.assertIn(executor_import, text)
        for suspended in (
            "suspended_pending_closures",
            "suspended_stage_completion_receipt",
            "suspended_eligible_candidates",
        ):
            self.assertNotIn(suspended, text)
        self.assertIn("# administrative_review_0813_receipt_pending_closures", text)
        self.assertNotIn(
            "import administrative_autonomy_runtime_administrative_review_0813_receipt_recovery",
            text,
        )


if __name__ == "__main__":
    unittest.main()
