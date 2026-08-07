from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
MODULE_PATH = ROOT / "ci" / "administrative_autonomy_runtime_behind_sync.py"
SPEC = importlib.util.spec_from_file_location(
    "administrative_autonomy_runtime_behind_sync",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class FakeClient:
    def __init__(self, pulls: list[dict]):
        self.pulls = pulls
        self.index = 0
        self.puts: list[tuple[str, dict]] = []

    def get(self, path: str):
        value = self.pulls[min(self.index, len(self.pulls) - 1)]
        if self.index < len(self.pulls) - 1:
            self.index += 1
        return copy.deepcopy(value)

    def put(self, path: str, payload: dict):
        self.puts.append((path, copy.deepcopy(payload)))
        return {"message": "Updating pull request branch."}


class BehindSynchronizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.control = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_behind_sync_control.json"
            ).read_text(encoding="utf-8")
        )
        self.control["synchronization"]["poll_interval_seconds"] = 0
        self.manifest = {
            "pull_request_number": 265,
            "branch": "automation/maintenance/administrative_review-20260807T012100Z",
        }
        self.old_head = "a" * 40
        self.new_head = "b" * 40

    def pull(
        self,
        *,
        mergeable_state: str,
        head: str | None = None,
        branch: str | None = None,
        base: str = "main",
    ) -> dict:
        return {
            "number": 265,
            "state": "open",
            "mergeable_state": mergeable_state,
            "head": {
                "sha": head or self.old_head,
                "ref": branch or self.manifest["branch"],
                "repo": {"full_name": "grandchallenge/MATH-PROGRAMME"},
            },
            "base": {"ref": base},
        }

    def test_control_is_valid(self) -> None:
        original = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_behind_sync_control.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual([], module.validate_behind_sync_control(original))

    def test_clean_candidate_is_not_mutated(self) -> None:
        client = FakeClient([self.pull(mergeable_state="clean")])
        result = module.synchronize_pull_if_behind(
            client,
            "grandchallenge/MATH-PROGRAMME",
            client.get("pull"),
            self.manifest,
            self.control,
            1,
        )
        self.assertIsNone(result)
        self.assertEqual([], client.puts)

    def test_behind_candidate_uses_expected_head_and_reads_new_head(self) -> None:
        client = FakeClient(
            [
                self.pull(mergeable_state="behind"),
                self.pull(mergeable_state="clean", head=self.new_head),
            ]
        )
        result = module.synchronize_pull_if_behind(
            client,
            "grandchallenge/MATH-PROGRAMME",
            client.get("pull"),
            self.manifest,
            self.control,
            1,
        )
        self.assertEqual(self.new_head, result["synchronized_head"])
        self.assertEqual(self.old_head, result["previous_head"])
        self.assertEqual(
            [("/repos/grandchallenge/MATH-PROGRAMME/pulls/265/update-branch", {"expected_head_sha": self.old_head})],
            client.puts,
        )

    def test_wrong_base_is_rejected(self) -> None:
        client = FakeClient(
            [self.pull(mergeable_state="behind", base="release")]
        )
        with self.assertRaisesRegex(module.AutonomyError, "base is not main"):
            module.synchronize_pull_if_behind(
                client,
                "grandchallenge/MATH-PROGRAMME",
                client.get("pull"),
                self.manifest,
                self.control,
                1,
            )

    def test_wrong_branch_is_rejected(self) -> None:
        client = FakeClient(
            [
                self.pull(
                    mergeable_state="behind",
                    branch="feature/outside-maintenance-scope",
                )
            ]
        )
        with self.assertRaisesRegex(module.AutonomyError, "does not match manifest"):
            module.synchronize_pull_if_behind(
                client,
                "grandchallenge/MATH-PROGRAMME",
                client.get("pull"),
                self.manifest,
                self.control,
                1,
            )

    def test_no_head_change_fails_closed(self) -> None:
        control = copy.deepcopy(self.control)
        control["synchronization"]["head_change_wait_seconds"] = 0
        client = FakeClient([self.pull(mergeable_state="behind")])
        with self.assertRaisesRegex(module.AutonomyError, "head-change readback timed out"):
            module.synchronize_pull_if_behind(
                client,
                "grandchallenge/MATH-PROGRAMME",
                client.get("pull"),
                self.manifest,
                control,
                1,
            )
        self.assertEqual(1, len(client.puts))

    def test_only_precise_behind_timeout_is_retryable(self) -> None:
        retryable = module.AutonomyError(
            "post-disposition stabilization timed out: "
            "{'merge_state': 'BEHIND', 'checks': {'policy': 'success'}}"
        )
        other = module.AutonomyError(
            "post-disposition stabilization timed out: "
            "{'merge_state': 'DIRTY', 'checks': {'policy': 'success'}}"
        )
        self.assertTrue(module.is_behind_stabilization_failure(retryable))
        self.assertFalse(module.is_behind_stabilization_failure(other))


if __name__ == "__main__":
    unittest.main()
