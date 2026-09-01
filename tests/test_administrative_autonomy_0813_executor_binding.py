from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

from tests.test_administrative_autonomy_0813_closure_preflight import (
    AdministrativeAutonomy0813ClosurePreflightTests,
)

ROOT = Path(__file__).resolve().parents[1]
ACTIVATION_WORKFLOW = ROOT / ".github" / "workflows" / "administrative-autonomy-activation.yml"
FAILOVER_WORKFLOW = ROOT / ".github" / "workflows" / "administrative-maintenance-0813-recovery-failover.yml"


class AdministrativeReview0813ExecutorBindingTests(unittest.TestCase):
    def test_reactivated_generic_runtime_precedes_executor_import(self):
        source = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(encoding="utf-8")
        executor_capture = source.index("import administrative_autonomy_runtime_execute as runtime_execute")
        behind_capture = source.index("import administrative_autonomy_runtime_behind_sync as behind_sync")
        self.assertLess(executor_capture, behind_capture)
        self.assertEqual(
            source.count("runtime_github.eligible_candidates = RECOVERY_ELIGIBILITY_CHAIN[-1]"),
            1,
        )
        self.assertNotIn("runtime_github.eligible_candidates = partial(", source)
        for suspended in (
            "suspended_eligible_candidates",
            "suspended_pending_closures",
            "suspended_stage_completion_receipt",
        ):
            self.assertNotIn(suspended, source)
        self.assertNotIn(
            "import administrative_autonomy_runtime_administrative_review_0813_receipt_recovery",
            source,
        )

    def test_fresh_runtime_process_binds_reactivated_generic_executor(self):
        probe = """
import sys
from pathlib import Path
root = Path.cwd()
sys.path.insert(0, str(root / 'ci'))
import administrative_autonomy_runtime  # noqa: F401
import administrative_autonomy_receipt_stage as receipt_stage
import administrative_autonomy_runtime_execute as runtime_execute
import administrative_autonomy_runtime_github as runtime_github
checks = [
    runtime_execute.pending_closures is receipt_stage.pending_closures,
    runtime_execute.eligible_candidates is runtime_github.eligible_candidates,
]
raise SystemExit(0 if all(checks) else 1)
"""
        completed = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "fresh runtime process did not bind the reactivated generic executor "
                f"path\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            ),
        )

    def test_activation_workflow_self_kicks_exact_aug13_preflight(self):
        text = ACTIVATION_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("branches: [main]", text)
        self.assertIn("- .github/workflows/administrative-autonomy-activation.yml", text)
        self.assertIn("- ci/administrative_autonomy_0813_closure_preflight.py", text)
        self.assertIn("- ci/administrative_autonomy_runtime_administrative_review_0813_receipt_recovery.py", text)
        self.assertIn("id: evidence-token", text)
        self.assertIn("OBSERVABILITY_TOKEN: ${{ steps.evidence-token.outputs.token }}", text)
        preflight = text.index("python ci/administrative_autonomy_0813_closure_preflight.py")
        canary = text.index("python ci/administrative_autonomy_candidate_merge.py")
        self.assertLess(preflight, canary)
        self.assertIn("if: steps.aug13-closure.outputs.recovered != 'true'", text)

    def test_activation_falls_through_when_exact_target_is_absent(self):
        text = ACTIVATION_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("echo \"recovered=${recovered}\" >> \"$GITHUB_OUTPUT\"", text)
        self.assertIn("state': 'AUG13_CLOSURE_RECOVERED__ACTIVATION_CANARY_NOT_REQUIRED'", text)
        self.assertIn("if: steps.aug13-closure.outputs.recovered == 'true'", text)

    def test_pr_close_failover_installs_governed_dependencies_before_preflight(self):
        text = FAILOVER_WORKFLOW.read_text(encoding="utf-8")
        install = text.index("python -m pip install --requirement requirements/policy.txt")
        preflight = text.index("python ci/administrative_autonomy_0813_closure_preflight.py")
        self.assertLess(install, preflight)


if __name__ == "__main__":
    unittest.main()
