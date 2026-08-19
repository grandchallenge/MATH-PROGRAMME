from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import pr_visual_status_workflow_operator_surface as operator  # noqa: E402

TIP = "a" * 40


class ExactRefClient:
    def __init__(self) -> None:
        self.paths: list[str] = []

    def get(self, path: str):
        self.paths.append(path)
        if "/branches/" in path:
            raise AssertionError("branch metadata endpoint is not exact ref readback")
        if path.endswith("/git/ref/heads/prvsr-operator-index"):
            return {"object": {"sha": TIP}}
        raise AssertionError(f"unexpected GET {path}")


class PRVisualStatusOperatorRefReadbackTests(unittest.TestCase):
    def test_branch_tip_uses_exact_git_ref_endpoint(self) -> None:
        client = ExactRefClient()
        result = operator._branch_tip(
            client, operator.ALLOWED_REPOSITORY, operator.INDEX_BRANCH
        )
        self.assertEqual(TIP, result)
        self.assertEqual(
            [
                "/repos/grandchallenge/MATH-PROGRAMME/git/ref/heads/"
                "prvsr-operator-index"
            ],
            client.paths,
        )


if __name__ == "__main__":
    unittest.main()
