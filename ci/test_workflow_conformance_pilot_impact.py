#!/usr/bin/env python3
"""Positive and hostile impact-routing checks for nonrequired GCL pilots."""
import unittest
from unittest.mock import patch
try:
    from ci import workflow_conformance_pilot_impact as gate
except ImportError:
    import workflow_conformance_pilot_impact as gate

A = 'a' * 40
B = 'b' * 40

class PilotImpactTests(unittest.TestCase):
    def test_workflow_preserves_unconditional_required_jobs_and_fails_open(self):
        from pathlib import Path
        import yaml
        workflow = yaml.safe_load((Path(__file__).resolve().parents[1] /
                                   '.github/workflows/gcl-conformance.yml').read_text())
        jobs = workflow['jobs']
        self.assertNotIn('if', jobs['policy'])
        self.assertNotIn('if', jobs['security'])
        for name, output in [('assurance-pilot', 'assurance'), ('disclosure-pilot', 'disclosure')]:
            self.assertEqual(jobs[name]['needs'], 'pilot-impact')
            cond = jobs[name]['if']
            self.assertIn('always()', cond)
            self.assertIn("needs.pilot-impact.result != 'success'", cond)
            self.assertIn(f"needs.pilot-impact.outputs.{output} != 'false'", cond)
        self.assertIn('workflow_dispatch', workflow.get('on', workflow.get(True, {})))

    def test_unrelated_pr_skips_only_optional_pilots(self):
        self.assertEqual(gate.classify(['fixtures/formal/CMDG-foo.lean', 'ci/validate_workflow_coverage.py']),
                         (False, False, 'EXACT_PATH_IMPACT'))

    def test_own_sources_dispatch_correct_pilot(self):
        for path in ('assurance/output/dossier.json','ci/assure_pr.py','tests/test_assurance_product.py'):
            with self.subTest(path=path):
                self.assertEqual(gate.classify([path])[:2], (True, False))
        for path in ('disclosure/measurement_ledger.json','ci/disclose_pr.py','tests/test_disclosure_gate.py'):
            with self.subTest(path=path):
                self.assertEqual(gate.classify([path])[:2], (False, True))

    def test_shared_dependencies_dispatch_both(self):
        for path in gate.SHARED:
            with self.subTest(path=path):
                self.assertEqual(gate.classify([path])[:2], (True, True))

    def test_missing_and_unsafe_fail_open(self):
        self.assertEqual(gate.classify(None)[:2], (True, True))
        self.assertEqual(gate.classify(['../wrong'])[:2], (True, True))
        self.assertEqual(gate.plan('pull_request', {'pull_request': {'base': {'sha': 'bad'}}})[:2], (True, True))
        self.assertEqual(gate.plan('push', {'before':'0'*40,'after':B})[:2], (True, True))

    def test_schedule_and_manual_always_run(self):
        for event in ('schedule','workflow_dispatch'):
            self.assertEqual(gate.plan(event,{})[:2], (True, True))

    def test_exact_event_diff(self):
        data={'pull_request': {'base':{'sha':A},'head':{'sha':B}}}
        with patch.object(gate,'diff_paths',return_value=['README.md']) as diff:
            self.assertEqual(gate.plan('pull_request', data)[:2], (False, False))
            diff.assert_called_once_with(A,B)

    def test_merge_group_conservative(self):
        event={'merge_group':{'base_sha':A,'head_sha':B}}
        with patch.object(gate,'diff_paths',return_value=None):
            self.assertEqual(gate.plan('merge_group',event)[:2], (True, True))

    def test_diff_error_fails_open(self):
        with patch.object(gate.subprocess,'run',side_effect=OSError('git unavailable')):
            with self.assertRaises(OSError):gate.diff_paths(A,B)

if __name__ == '__main__':
    unittest.main()
