"""Fail closed on inadvertent removal of automatic post-deploy parity evidence."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
FLOW=ROOT/'.github/workflows/erdos-compendium-public-html-readback.yml'
PROTO=ROOT/'governance/erdos_compendium/EDITORIAL_PROTOCOL.md'
class IntegrationTests(unittest.TestCase):
 def setUp(self):self.s=FLOW.read_text();self.p=PROTO.read_text()
 def test_deploy_event_causes_automatic_job(self):
  self.assertIn('  workflow_run:',self.s);self.assertIn('    workflows: ["Deploy documentation site"]',self.s)
  self.assertIn('  accepted-parity-auto:',self.s)
  self.assertIn("github.event.workflow_run.conclusion == 'success'",self.s)
 def test_exact_source_and_real_browser(self):
  self.assertIn('ref: ${{ github.event.workflow_run.head_sha }}',self.s)
  self.assertIn('python ci/erdos_parity_auto.py --mode check',self.s)
  self.assertIn('python ci/test_erdos_parity_coverage.py',self.s)
 def test_protected_receipt(self):
  self.assertIn('permission-contents: write',self.s)
  self.assertIn('permission-pull-requests: write',self.s)
  self.assertIn('python ci/erdos_parity_auto.py --mode publish',self.s)
  self.assertIn("if: steps.parity-check.outputs.has_articles == 'true'",self.s)
 def test_no_automatic_direct_push_or_certification(self):
  self.assertIn('only after the corresponding normal PR has merged',self.p)
  self.assertIn('does *not* certify those 650',self.p)
  self.assertIn('not a new admission/review body',self.p)
if __name__=='__main__':unittest.main()
