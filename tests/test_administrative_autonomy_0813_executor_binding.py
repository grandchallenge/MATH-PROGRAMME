from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AdministrativeReview0813ExecutorBindingTests(unittest.TestCase):
    def test_exact_closure_overlay_precedes_executor_import(self):
        source = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(
            encoding="utf-8"
        )
        overlay = source.index(
            "receipt_stage.pending_closures = partial(\n"
            "    administrative_review_0813_receipt_pending_closures,"
        )
        executor_import = source.index(
            "import administrative_autonomy_runtime_behind_sync as behind_sync"
        )
        self.assertLess(overlay, executor_import)

    def test_fresh_runtime_process_binds_exact_closure_overlay_into_executor(self):
        probe = """
import sys
from pathlib import Path
root = Path.cwd()
sys.path.insert(0, str(root / 'ci'))
import administrative_autonomy_runtime  # noqa: F401
import administrative_autonomy_receipt_stage as receipt_stage
import administrative_autonomy_runtime_execute as runtime_execute
raise SystemExit(0 if runtime_execute.pending_closures is receipt_stage.pending_closures else 1)
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
                "fresh runtime process did not bind exact Aug13 closure overlay "
                f"into executor\nstdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            ),
        )


if __name__ == "__main__":
    unittest.main()
