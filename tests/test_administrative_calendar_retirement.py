import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
import prepare_administrative_candidate_v5 as preparation


class CalendarRetirementTests(unittest.TestCase):
    def test_scheduled_apply_never_reaches_candidate_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / "report.json"
            with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "schedule"}), \
                 patch.object(preparation.implementation, "main") as legacy, \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(preparation.main(["--apply", "--report", str(report)]), 0)
            legacy.assert_not_called()
            data = json.loads(report.read_text())
            self.assertEqual(data["state"], "CALENDAR_ONLY_CANDIDATE_CREATION_RETIRED")
            self.assertEqual(data["occurrence_count"], 0)
            self.assertFalse(data["authority_created"])

    def test_explicit_dispatch_preserves_existing_controls(self):
        with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "workflow_dispatch"}), \
             patch.object(preparation.implementation, "main", return_value=0) as legacy:
            self.assertEqual(preparation.main(["--apply"]), 0)
            legacy.assert_called_once_with(["--apply"])

    def test_read_only_schedule_evaluation_remains_available(self):
        with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "schedule"}), \
             patch.object(preparation.implementation, "main", return_value=0) as legacy:
            self.assertEqual(preparation.main([]), 0)
            legacy.assert_called_once_with([])


if __name__ == "__main__":
    unittest.main()
