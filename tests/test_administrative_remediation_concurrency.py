from __future__ import annotations

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/administrative-protected-receipt-live-qualification.yml"


class AdministrativeRemediationConcurrencyTests(unittest.TestCase):
    def test_admission_is_nonblocking_while_qualification_stays_global(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(
            "group: administrative-protected-receipt-run-${{ github.run_id }}",
            text,
        )
        self.assertIn(
            "group: administrative-protected-receipt-qualification",
            text,
        )
        self.assertGreaterEqual(text.count("cancel-in-progress: false"), 2)
        self.assertNotIn("format('admission-pr-{0}'", text)
        self.assertNotIn("&& 'qualification' || 'admission' }}", text)

    def test_ineligible_events_do_not_allocate_admission_runner(self) -> None:
        workflow = yaml.load(WORKFLOW.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        expected = '(github.event_name == \'pull_request_target\' && github.event.action != \'closed\' && github.event.pull_request.draft == false && startsWith(github.event.pull_request.head.ref, \'remediation/mp-admin-\')) || (github.event_name == \'issue_comment\' && github.event.issue.pull_request != null && contains(fromJSON(\'["OWNER","MEMBER","COLLABORATOR"]\'), github.event.comment.author_association) && startsWith(github.event.comment.body, \'DELEGATED_REMEDIATION_ADMIT \'))'
        self.assertEqual(" ".join(workflow["jobs"]["admit"]["if"].split()), expected)
        # Preserve the authoritative resolver and qualification route.
        steps = workflow["jobs"]["admit"]["steps"]
        self.assertEqual(steps[0]["id"], "target")
        self.assertIn("re.fullmatch", steps[0]["run"])
        for step in steps[1:]:
            self.assertIn("steps.target.outputs.eligible == 'true'", step["if"])
        self.assertIn("github.event.pull_request.merged == true", workflow["jobs"]["qualify"]["if"])

    def test_secret_free_target_resolution_precedes_app_tokens(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")
        resolver = text.index("- name: Resolve exact admission target")
        admin_token = text.index("- name: Mint read-only Administration ruleset token")
        candidate_token = text.index("- name: Mint bounded Candidate merge-executor token")
        self.assertLess(resolver, admin_token)
        self.assertLess(resolver, candidate_token)
        self.assertIn("eligible={'true' if eligible else 'false'}", text)
        self.assertIn("steps.target.outputs.eligible == 'true'", text)


if __name__ == "__main__":
    unittest.main()
