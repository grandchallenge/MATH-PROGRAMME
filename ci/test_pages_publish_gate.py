#!/usr/bin/env python3
"""Regression and hostile tests for bounded Pages publication eligibility."""
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

try:
    from ci import pages_publish_gate as gate
except ImportError:
    import pages_publish_gate as gate


class GateTests(unittest.TestCase):
    def test_unrelated_protected_merge_skips_deployment(self):
        paths = ['fixtures/formal/CMDG-FOO.lean', 'ci/policy_impact.py',
                 '.github/workflows/other.yml', 'governance/cmdg/foo.json',
                 'governance/erdos_compendium/batches/EC-BULK-004.json',
                 'governance/erdos_compendium/reviews/EC004-CRIT.md',
                 'governance/oai26_documentary/reviews/F001.md']
        self.assertEqual(gate.decision('a' * 40, 'b' * 40, paths),
                         (False, 'SITE_INPUTS_UNCHANGED'))

    def test_site_inputs_always_publish(self):
        for path in ['docs/index.md', 'overrides/partials/tabs.html', 'mkdocs.yml', 'requirements/docs.txt',
                     'governance/erdos_catalogue/REGISTRY.json',
                     'governance/erdos_compendium/EDITORIAL_ADMISSIONS.json',
                     'governance/oai26_documentary/editorial/001.md',
                     'ci/erdos_compendium_hook.py', 'ci/oai26_compendium.py']:
            with self.subTest(path=path):
                self.assertTrue(gate.decision('a' * 40, 'b' * 40, [path])[0])

    def test_unknown_or_missing_evidence_publishes(self):
        self.assertTrue(gate.decision(None, 'b' * 40, [])[0])
        self.assertTrue(gate.decision('a' * 40, 'b' * 40, None)[0])
        self.assertTrue(gate.site_source('../unknown'))

    def test_exact_same_head_skips_compare(self):
        with patch.object(gate, 'latest_deployed', return_value='a' * 40), \
             patch.object(gate, 'compared_paths', return_value=[]) as compare:
            publish, reason = gate.run('grandchallenge/MATH-PROGRAMME', 'a' * 40, 'token')
            self.assertFalse(publish)
            compare.assert_called_once()

    def test_rest_failure_fail_open(self):
        with patch.object(gate, 'latest_deployed', side_effect=HTTPError('x', 403, 'denied', {}, None)):
            self.assertTrue(gate.run('grandchallenge/MATH-PROGRAMME', 'a' * 40, 'token')[0])

    def test_pagination_cap_and_divergence_publish(self):
        with patch('urllib.request.urlopen') as urlopen:
            response = urlopen.return_value.__enter__.return_value
            for record in [{'status': 'ahead', 'files': [{'filename': 'README.md'}] * 300},
                           {'status': 'diverged', 'files': []}]:
                response.read.return_value = json.dumps(record).encode()
                with self.subTest(status=record['status']):
                    self.assertIsNone(gate.compared_paths('o/r', 'token', 'a' * 40, 'b' * 40))

    def test_rename_includes_previous_path(self):
        with patch('urllib.request.urlopen') as urlopen:
            resp = urlopen.return_value.__enter__.return_value
            resp.read.return_value = json.dumps({'status': 'ahead', 'files': [
                {'filename': 'moved.md', 'previous_filename': 'docs/old.md'}]}).encode()
            self.assertEqual(gate.compared_paths('o/r', 'token', 'a' * 40, 'b' * 40),
                             ['moved.md', 'docs/old.md'])


if __name__ == '__main__':
    unittest.main()
