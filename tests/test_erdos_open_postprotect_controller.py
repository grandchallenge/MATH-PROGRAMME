import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ci.erdos_open_postprotect_controller import (
    _advanced_state,
    _approval_exists,
    _merge,
    branch_name,
    closure_path,
)


class FakeGithub:
    def __init__(self):
        self.calls = []
        self.reviews = []

    def request(self, method, path, payload=None):
        self.calls.append((method, path, payload))
        if path.endswith("/reviews?per_page=100"):
            return self.reviews
        if method == "PUT" and path.endswith("/pulls/77/merge"):
            return {"merged": True, "sha": "f" * 40}
        raise AssertionError((method, path, payload))


class ErdosPostprotectControllerTests(unittest.TestCase):
    def test_controller_cli_imports_in_production_shape(self):
        root = Path(__file__).resolve().parents[1]
        proc = subprocess.run(
            [sys.executable, str(root / "ci" / "erdos_open_postprotect_controller.py"), "--help"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("--solve-root", proc.stdout)

    def test_direct_cli_help_smoke(self):
        proc = subprocess.run(
            [sys.executable, "ci/erdos_open_postprotect_controller.py", "--help"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_registered_branch_and_closure_paths_are_exact(self):
        self.assertEqual(
            branch_name("241"),
            "lifecycle/erdos-241-cohort-closure-001",
        )
        self.assertEqual(
            closure_path("241"),
            "contributions/ERDOS-OPEN-001/RECON_TRANCHE_001/"
            "closures/ERDOS-241-BLIND-COHORT-001.json",
        )

    def test_unregistered_problem_stops_at_synthesis_ready(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(
                _advanced_state(Path(td), "593")["state"],
                "SYNTHESIS_READY_NEEDS_REGISTERED_PLUGIN",
            )

    def test_registered_validator_can_recognize_advanced_bundle(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            script = root / "ci" / "validate_erdos_241_synthesis.py"
            script.parent.mkdir(parents=True)
            script.write_text(
                "print('PASS: protected 241 bundle')\n",
                encoding="utf-8",
            )
            state = _advanced_state(root, "241")
            self.assertEqual(state["state"], "ADVANCED")
            self.assertIn("PASS", state["validator_output"])

    def test_registered_validator_failure_does_not_advance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            script = root / "ci" / "validate_erdos_241_synthesis.py"
            script.parent.mkdir(parents=True)
            script.write_text(
                "raise SystemExit(1)\n",
                encoding="utf-8",
            )
            self.assertEqual(
                _advanced_state(root, "241")["state"],
                "REGISTERED_PLUGIN_NOT_SATISFIED",
            )

    def test_clerk_review_must_match_exact_head(self):
        gh = FakeGithub()
        gh.reviews = [
            {
                "state": "APPROVED",
                "commit_id": "a" * 40,
                "user": {"login": "gcl-council-clerk[bot]"},
            }
        ]
        self.assertTrue(_approval_exists(gh, 77, "a" * 40))
        self.assertFalse(_approval_exists(gh, 77, "b" * 40))

    def test_merge_is_exact_head_squash_without_bypass(self):
        gh = FakeGithub()
        out = _merge(gh, 77, "c" * 40, "241")
        self.assertTrue(out["merged"])
        method, path, payload = gh.calls[-1]
        self.assertEqual(method, "PUT")
        self.assertEqual(path, "/repos/grandchallenge/MATHSOLVE/pulls/77/merge")
        self.assertEqual(payload["sha"], "c" * 40)
        self.assertEqual(payload["merge_method"], "squash")
        self.assertNotIn("admin", str(payload).lower())


if __name__ == "__main__":
    unittest.main()
