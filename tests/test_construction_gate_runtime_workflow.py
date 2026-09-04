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

    def test_gcl_tcs_issue_path_is_exactly_pinned(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("github.event.issue.number == 831", text)
        self.assertIn("ISSUE_NUMBER: ${{ github.event.issue.number || 0 }}", text)
        self.assertIn("GCL-TCS-V1-PROMOTION-001)", text)
        self.assertIn("8833253f620c6c05930740bda983d6f43bee6612", text)
        self.assertIn("CREATE_DEVELOPMENT|FREEZE_CANDIDATE", text)
        self.assertIn("issue #831 is not open", text)
        self.assertNotIn("actions: write", text)

        gcl_block = text.split("GCL-TCS-V1-PROMOTION-001)", 1)[1].split(
            '*) echo "unsupported issue-command target"', 1
        )[0]
        self.assertNotIn("UPDATE_DEVELOPMENT", gcl_block)


if __name__ == "__main__":
    unittest.main()
