from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_low_friction as low

runtime = sys.modules.get("__main__")
if runtime is None or not hasattr(runtime, "_base_aware_low_friction_current_pull"):
    import administrative_autonomy_runtime as runtime


class BaseAwareClient:
    def __init__(
        self,
        *,
        pull: dict,
        base_shas: list[str],
        behind_by: int,
        compare_status: str = "diverged",
    ) -> None:
        self.pull = copy.deepcopy(pull)
        self.base_shas = list(base_shas)
        self.behind_by = behind_by
        self.compare_status = compare_status
        self.paths: list[str] = []

    def get(self, path: str):
        self.paths.append(path)
        if path == f"/repos/{low.EXPECTED_REPOSITORY}/pulls/7":
            return copy.deepcopy(self.pull)
        branch_path = (
            f"/repos/{low.EXPECTED_REPOSITORY}/branches/{low.EXPECTED_BASE}"
        )
        if path == branch_path:
            if not self.base_shas:
                raise AssertionError("unexpected protected-base reread")
            sha = self.base_shas.pop(0)
            return {"name": low.EXPECTED_BASE, "commit": {"sha": sha}}
        prefix = f"/repos/{low.EXPECTED_REPOSITORY}/compare/"
        if path.startswith(prefix):
            pair = path[len(prefix):]
            base_sha, head_sha = pair.split("...", 1)
            return {
                "status": self.compare_status,
                "ahead_by": 1,
                "behind_by": self.behind_by,
                "base_commit": {"sha": base_sha},
                "merge_base_commit": {"sha": "d" * 40},
                "head_commit": {"sha": head_sha},
            }
        raise AssertionError(f"unexpected GET {path}")


def candidate_pull(*, merged: bool = False) -> dict:
    return {
        "number": 7,
        "state": "closed" if merged else "open",
        "merged": merged,
        "draft": True,
        "mergeable_state": "clean",
        "base": {"ref": low.EXPECTED_BASE},
        "head": {
            "ref": "routine/low-friction/qualification-regression",
            "sha": "a" * 40,
            "repo": {"full_name": low.EXPECTED_REPOSITORY},
        },
    }


class LowFrictionBaseDriftTests(unittest.TestCase):
    def test_qualification_regression_clean_mergeability_but_behind_base(self):
        base_sha = "b" * 40
        client = BaseAwareClient(
            pull=candidate_pull(),
            base_shas=[base_sha, base_sha],
            behind_by=48,
        )
        observed = runtime._base_aware_low_friction_current_pull(client, 7)
        self.assertEqual(observed["mergeable_state"], "behind")
        evidence = observed["_low_friction_base_drift"]
        self.assertEqual(evidence["behind_by"], 48)
        self.assertEqual(evidence["protected_base_sha"], base_sha)
        self.assertFalse(evidence["base_moved_during_compare"])

    def test_wait_mergeable_state_consumes_ancestry_overlay(self):
        base_sha = "b" * 40
        client = BaseAwareClient(
            pull=candidate_pull(),
            base_shas=[base_sha, base_sha],
            behind_by=3,
        )
        state, observed = low.wait_mergeable_state(
            client, 7, "a" * 40, low.load_json(low.CONTROL_PATH)
        )
        self.assertEqual(state, "behind")
        self.assertEqual(observed["mergeable_state"], "behind")

    def test_current_base_preserves_github_mergeable_state(self):
        base_sha = "b" * 40
        client = BaseAwareClient(
            pull=candidate_pull(),
            base_shas=[base_sha, base_sha],
            behind_by=0,
            compare_status="ahead",
        )
        observed = runtime._base_aware_low_friction_current_pull(client, 7)
        self.assertEqual(observed["mergeable_state"], "clean")
        self.assertNotIn("_low_friction_base_drift", observed)

    def test_protected_base_move_during_compare_fails_to_behind(self):
        client = BaseAwareClient(
            pull=candidate_pull(),
            base_shas=["b" * 40, "c" * 40],
            behind_by=0,
            compare_status="ahead",
        )
        observed = runtime._base_aware_low_friction_current_pull(client, 7)
        self.assertEqual(observed["mergeable_state"], "behind")
        self.assertTrue(
            observed["_low_friction_base_drift"]["base_moved_during_compare"]
        )

    def test_merged_pull_skips_base_comparison(self):
        client = BaseAwareClient(
            pull=candidate_pull(merged=True),
            base_shas=[],
            behind_by=0,
        )
        observed = runtime._base_aware_low_friction_current_pull(client, 7)
        self.assertTrue(observed["merged"])
        self.assertEqual(
            client.paths,
            [f"/repos/{low.EXPECTED_REPOSITORY}/pulls/7"],
        )


if __name__ == "__main__":
    unittest.main()
