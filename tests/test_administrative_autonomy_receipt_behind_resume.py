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
SPEC = importlib.util.spec_from_file_location(
    "administrative_autonomy_runtime_receipt_behind_resume", MODULE_PATH
)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class FakeCandidate:
    def __init__(self, *, merge_state: str = "behind", pull_count: int = 1) -> None:
        self.branch = "automation/maintenance/receipt-structural_sweep-20260814T083300Z"
        self.old_head = "1" * 40
        self.new_head = "2" * 40
        self.head = self.old_head
        self.merge_state = merge_state
        self.pull_count = pull_count
        self.update_payloads: list[dict[str, str]] = []

    def _pull(self) -> dict:
        return {
            "number": 529,
            "state": "open",
            "draft": False,
            "node_id": "PR_test",
            "mergeable_state": self.merge_state,
            "head": {
                "ref": self.branch,
                "sha": self.head,
                "repo": {"full_name": "grandchallenge/MATH-PROGRAMME"},
            },
            "base": {"ref": "main"},
        }

    def get(self, path: str):
        if path.startswith("/repos/grandchallenge/MATH-PROGRAMME/git/ref/heads/"):
            encoded = path.rsplit("/heads/", 1)[1]
            if unquote(encoded) != self.branch:
                raise AssertionError(path)
            return {"object": {"sha": self.old_head}}
        if "/pulls?" in path:
            return [self._pull() for _ in range(self.pull_count)]
        if path == "/repos/grandchallenge/MATH-PROGRAMME/pulls/529":
            return self._pull()
        if path == "/repos/grandchallenge/MATH-PROGRAMME/pulls/529/files?per_page=100":
            return [
                {
                    "filename": module.STATE_PATH,
                    "additions": 14,
                    "deletions": 3,
                }
            ]
        raise AssertionError(path)

    def put(self, path: str, payload: dict):
        if path != "/repos/grandchallenge/MATH-PROGRAMME/pulls/529/update-branch":
            raise AssertionError(path)
        self.update_payloads.append(copy.deepcopy(payload))
        self.head = self.new_head
        self.merge_state = "clean"
        return {"message": "Updating pull request branch."}


class ReceiptBehindResumeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.control = {
            "control_id": "MP-ADMIN-RECEIPT-BEHIND-RESUME-001",
            "status": "ACTIVE_WHEN_PROTECTED",
            "repository": "grandchallenge/MATH-PROGRAMME",
            "synchronization": {
                "branch_prefix": module.RECEIPT_BRANCH_PREFIX,
                "base_branch": "main",
                "state_path": module.STATE_PATH,
                "expected_head_required": True,
                "single_open_pull_required": True,
                "same_repository_required": True,
                "exact_payload_required_before_and_after_sync": True,
                "synchronize_only_when_behind": True,
                "clean_resume_allowed": True,
                "merge_state_wait_seconds": 10,
                "head_change_wait_seconds": 30,
                "poll_interval_seconds": 2,
                "fresh_exact_head_checks_required": True,
                "fresh_referee_disposition_required": True,
                "ordinary_protected_merge_required": True,
            },
            "authority_boundary": {
                "human_steward_identity_asserted": False,
                "bypass_may_be_exercised": False,
                "direct_protected_push": False,
            },
            "claim_boundaries": {
                "mathematical_target_proved": False,
                "campaign_admitted": False,
                "source_verified": False,
                "cert_route_registered": False,
                "adjudication_authorized": False,
                "certificate_issued": False,
                "external_claim_authorized": False,
            },
        }
        self.completion = {
            "schema_version": "1.0.0",
            "control_id": "MP-ADMIN-MAINT-001",
            "derived_from_protected_head": "a" * 40,
            "state": "PROTECTED_RECEIPT_DERIVED",
            "procedures": {},
            "authority_boundary": {},
        }

    def _loader(self, expected=None):
        value = self.completion if expected is None else expected
        return lambda _client, _repo, _path, _ref: copy.deepcopy(value)

    def test_control_file_preserves_non_authority_boundary(self) -> None:
        control = module.load_control()
        module.validate_control(control)
        self.assertEqual(531, control["issue"])
        self.assertFalse(
            control["authority_boundary"]["general_branch_update_authority_created"]
        )
        self.assertTrue(
            all(value is False for value in control["claim_boundaries"].values())
        )

    def test_behind_receipt_uses_expected_head_and_preserves_payload(self) -> None:
        candidate = FakeCandidate()
        result = module.resume_existing_receipt(
            candidate,
            "grandchallenge/MATH-PROGRAMME",
            candidate.branch,
            self.completion,
            self.control,
            completion_loader=self._loader(),
        )
        self.assertIsNotNone(result)
        assert result is not None
        pull, head, event = result
        self.assertEqual(529, pull["number"])
        self.assertEqual(candidate.new_head, head)
        self.assertEqual(
            [{"expected_head_sha": candidate.old_head}], candidate.update_payloads
        )
        self.assertTrue(event["expected_head_used"])
        self.assertEqual(candidate.old_head, event["previous_head"])
        self.assertEqual(candidate.new_head, event["synchronized_head"])

    def test_clean_exact_receipt_resumes_without_branch_update(self) -> None:
        candidate = FakeCandidate(merge_state="clean")
        result = module.resume_existing_receipt(
            candidate,
            "grandchallenge/MATH-PROGRAMME",
            candidate.branch,
            self.completion,
            self.control,
            completion_loader=self._loader(),
        )
        assert result is not None
        _, head, event = result
        self.assertEqual(candidate.old_head, head)
        self.assertEqual([], candidate.update_payloads)
        self.assertFalse(event["expected_head_used"])

    def test_payload_drift_fails_before_update_branch(self) -> None:
        candidate = FakeCandidate()
        drift = copy.deepcopy(self.completion)
        drift["state"] = "DRIFT"
        with self.assertRaises(module.AutonomyError):
            module.resume_existing_receipt(
                candidate,
                "grandchallenge/MATH-PROGRAMME",
                candidate.branch,
                self.completion,
                self.control,
                completion_loader=self._loader(drift),
            )
        self.assertEqual([], candidate.update_payloads)

    def test_multiple_open_receipt_pulls_fail_closed(self) -> None:
        candidate = FakeCandidate(pull_count=2)
        with self.assertRaises(module.AutonomyError):
            module.resume_existing_receipt(
                candidate,
                "grandchallenge/MATH-PROGRAMME",
                candidate.branch,
                self.completion,
                self.control,
                completion_loader=self._loader(),
            )
        self.assertEqual([], candidate.update_payloads)

    def test_non_behind_dirty_state_fails_closed(self) -> None:
        candidate = FakeCandidate(merge_state="blocked")
        with self.assertRaises(module.AutonomyError):
            module.resume_existing_receipt(
                candidate,
                "grandchallenge/MATH-PROGRAMME",
                candidate.branch,
                self.completion,
                self.control,
                completion_loader=self._loader(),
            )
        self.assertEqual([], candidate.update_payloads)

    def test_runtime_wires_resumable_receipt_stage_before_executor_import(self) -> None:
        text = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(
            encoding="utf-8"
        )
        wire = "receipt_stage.stage_completion_receipt = resumable_stage_completion_receipt"
        executor_import = "from administrative_autonomy_runtime_behind_sync import ("
        self.assertIn(wire, text)
        self.assertIn(executor_import, text)
        self.assertLess(text.index(wire), text.index(executor_import))


if __name__ == "__main__":
    unittest.main()
