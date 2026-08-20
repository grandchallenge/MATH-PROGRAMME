from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/administrative-protected-receipt-live-qualification.yml"


class AdministrativeRemediationConcurrencyTests(unittest.TestCase):
    def test_admission_is_serialized_per_pr_while_qualification_stays_global(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        expected_group = (
            "group: administrative-protected-receipt-${{ "
            "(github.event_name == 'workflow_dispatch' || github.event.action == 'closed') "
            "&& 'qualification' || format('admission-pr-{0}', "
            "github.event.pull_request.number || github.event.issue.number) }}"
        )
        self.assertIn(expected_group, text)
        self.assertIn("cancel-in-progress: false", text)
        self.assertNotIn("&& 'qualification' || 'admission' }}", text)
        self.assertEqual(text.count("\nconcurrency:\n"), 1)


if __name__ == "__main__":
    unittest.main()
