from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "construction-gate-runtime.yml"
GCL_TCS_BRIDGE = ROOT / ".github" / "workflows" / "gcl-tcs-v1-construction-gate-bridge.yml"


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

    def test_gcl_tcs_issue_bridge_is_exactly_pinned(self) -> None:
        text = GCL_TCS_BRIDGE.read_text(encoding="utf-8")

        self.assertIn("github.event.issue.number == 831", text)
        self.assertIn("github.event.comment.user.login == 'fyremael'", text)
        self.assertIn('GCL-TCS-V1-PROMOTION-001', text)
        self.assertIn("8833253f620c6c05930740bda983d6f43bee6612", text)
        self.assertIn("CREATE_DEVELOPMENT|FREEZE_CANDIDATE", text)
        self.assertIn("construction-gate-runtime.yml/dispatches", text)
        self.assertNotIn("UPDATE_DEVELOPMENT|", text)
        self.assertNotIn("git push", text)


if __name__ == "__main__":
    unittest.main()
