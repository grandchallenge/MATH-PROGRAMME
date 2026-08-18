from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))


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

    def test_executor_captures_exact_closure_overlay(self):
        import administrative_autonomy_runtime  # noqa: F401
        import administrative_autonomy_receipt_stage as receipt_stage
        import administrative_autonomy_runtime_execute as runtime_execute

        self.assertIs(runtime_execute.pending_closures, receipt_stage.pending_closures)


if __name__ == "__main__":
    unittest.main()
