import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import ci.erdos_open_postprotect_controller as controller
from ci.erdos_open_postprotect_controller import (
    CANARY2_ADVANCE_BRANCH,
    CANARY2_CLOSURE_BRANCH,
    CANARY2_SUCCESSOR_PATH,
    CANARY3_ADVANCE_BRANCH,
    CANARY3_CLOSURE_BRANCH,
    CANARY3_SUCCESSOR_PATH,
    _advanced_state,
    _approval_exists,
    _merge,
    _report_exit_code,
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

    def test_canary2_lifecycle_identities_are_disjoint_and_exact(self):
        self.assertEqual(
            CANARY2_CLOSURE_BRANCH,
            "lifecycle/gcl-e2e-canary-002-cohort-closure",
        )
        self.assertEqual(
            CANARY2_ADVANCE_BRANCH,
            "lifecycle/gcl-e2e-canary-002-advance",
        )
        self.assertEqual(
            CANARY2_SUCCESSOR_PATH,
            "work_packages/GCL_E2E_CANARY/GCL_E2E_CANARY_003.md",
        )

    def test_canary3_lifecycle_identities_are_disjoint_and_exact(self):
        self.assertEqual(
            CANARY3_CLOSURE_BRANCH,
            "lifecycle/gcl-e2e-canary-003-cohort-closure",
        )
        self.assertEqual(
            CANARY3_ADVANCE_BRANCH,
            "lifecycle/gcl-e2e-canary-003-advance",
        )
        self.assertEqual(
            CANARY3_SUCCESSOR_PATH,
            "work_packages/GCL_E2E_CANARY/GCL_E2E_CANARY_004.md",
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


    def test_existing_erdos_closure_pr_reuses_exact_head_without_rewrite(self):
        fake_gh = MagicMock()
        fake_gh.request.return_value = {"head": {"sha": "a" * 40}}

        class ClosureModule:
            @staticmethod
            def build_closure(problem, main_sha, date):
                return {"problem": problem, "source_commit": main_sha}

            @staticmethod
            def validate_closure(problem, closure):
                return []

        existing_pr = {"number": 77}
        candidate = {
            "problem": "593",
            "branch": branch_name("593"),
            "path": closure_path("593"),
            "head_sha": "a" * 40,
            "closure": {"problem": "593"},
        }
        with (
            patch.dict("os.environ", {"MATHSOLVE_ERDOS_LIFECYCLE_TOKEN": "test-token"}),
            patch.object(controller, "Github", return_value=fake_gh),
            patch.object(controller, "PROBLEMS", ("593",)),
            patch.object(controller, "_main_sha", return_value="b" * 40),
            patch.object(controller, "_local_sha", return_value="b" * 40),
            patch.object(controller, "_load_closure_module", return_value=ClosureModule),
            patch.object(controller, "_content", return_value=None),
            patch.object(controller, "_find_pr", return_value=existing_pr),
            patch.object(controller, "validate_candidate", return_value=candidate),
            patch.object(controller, "_approval_exists", return_value=False),
            patch.object(controller, "_create_branch") as create_branch,
            patch.object(controller, "_put_closure") as put_closure,
            patch.object(controller, "_run_canary", return_value={"canary": "1", "state": "ADVANCED"}),
            patch.object(controller, "_run_canary2", return_value={"canary": "2", "state": "ADVANCED"}),
            patch.object(controller, "_run_canary3", return_value={"canary": "3", "state": "WAITING"}),
        ):
            report = controller.run(Path("."), apply=True)

        create_branch.assert_not_called()
        put_closure.assert_not_called()
        self.assertEqual(report["errors"], [])
        erdos_state = next(x for x in report["states"] if x.get("problem") == "593")
        self.assertEqual(erdos_state["state"], "AWAITING_COUNCIL_CLERK_DOCUMENTARY_REVIEW")
        self.assertEqual(erdos_state["head_sha"], "a" * 40)

    def test_report_errors_make_controller_run_fail(self):
        self.assertEqual(_report_exit_code({"errors": []}), 0)
        self.assertEqual(
            _report_exit_code({"errors": [{"problem": "593", "error": "head drift"}]}),
            1,
        )


if __name__ == "__main__":
    unittest.main()
