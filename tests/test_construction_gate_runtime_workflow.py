from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "construction-gate-runtime.yml"


class ConstructionGateRuntimeWorkflowTests(unittest.TestCase):
    def test_exact_head_evidence_is_scoped_to_development_branch(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertNotIn("      checks: read\n", text)
        self.assertNotIn("      statuses: read\n", text)
        self.assertIn('"https://api.github.com/repos/$REPO/commits/$current_head/check-suites"', text)
        self.assertIn("exact_head_evidence=true", text)
        self.assertIn("select(.head_branch == $branch)", text)
        self.assertIn("select(any(.branches[]?; .name == $branch))", text)
        self.assertNotIn('"repos/$REPO/commits/$current_head/check-runs"', text)


if __name__ == "__main__":
    unittest.main()
