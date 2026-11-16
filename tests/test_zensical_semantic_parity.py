import tempfile
import unittest
from pathlib import Path
from ci.zensical_semantic_parity import audit

class RendererAuditTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
  self.before=self.root/'mkdocs';self.after=self.root/'zensical'
  for p in (self.before,self.after):p.mkdir()
 def tearDown(self):self.tmp.cleanup()
 def put(self,root,body):
  (root/'index.html').write_text(body,encoding='utf-8')
 def test_equivalent_content_not_confused_with_html_bytes(self):
  for root in (self.before,self.after):
   self.put(root,'<html><h1>Mathematics</h1><p>Protected source</p></html>')
  x=audit(self.before,self.after,{'index.html'})
  self.assertEqual(x['critical_issue_count'],0)
  self.assertEqual(x['heading_drift_count'],0)
  self.assertFalse(x['semantics_proven_equivalent'])
 def test_missing_local_asset_is_critical(self):
  self.put(self.before,'<h1>Math</h1>')
  self.put(self.after,'<h1>Math</h1><script src="missing.js"></script>')
  self.assertEqual(audit(self.before,self.after,{'index.html'})['critical_issues'][0]['code'],'BROKEN_LOCAL_ASSETS')
 def test_directory_style_internal_html_link_resolves_to_index(self):
  for root in (self.before,self.after):
   (root/'chapter').mkdir()
   (root/'chapter/index.html').write_text('<h1>Chapter</h1>',encoding='utf-8')
  self.put(self.before,'<h1>Math</h1>')
  self.put(self.after,'<h1>Math</h1><link href="chapter/">')
  self.assertEqual(audit(self.before,self.after,{'index.html'})['critical_issue_count'],0)
 def test_unexpanded_status_is_critical(self):
  self.put(self.before,'<h1>Math</h1>')
  self.put(self.after,'<h1>Math</h1><!-- GCL_ERDOS_HOME_STATUS -->')
  self.assertEqual(audit(self.before,self.after,{'index.html'})['critical_issue_count'],1)
 def test_math_loss_reported_without_false_certification(self):
  self.put(self.before,'<h1>Math</h1><span class="arithmatex">x</span>')
  self.put(self.after,'<h1>Math</h1><p>x</p>')
  self.assertEqual(audit(self.before,self.after,{'index.html'})['math_marker_loss_count'],1)
 def test_asset_path_escape_cannot_be_accepted(self):
  self.put(self.before,'<h1>Math</h1>')
  self.put(self.after,'<h1>Math</h1><link href="../../../secret.css">')
  self.assertEqual(audit(self.before,self.after,{'index.html'})['critical_issue_count'],1)
if __name__=='__main__':unittest.main()
