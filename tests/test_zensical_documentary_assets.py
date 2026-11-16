import tempfile
import unittest
from pathlib import Path
from ci.zensical_documentary_assets import DOCUMENTARIES,rewrite_temporary_docs

class DocumentaryRebaseTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.docs=Path(self.t.name)
  (self.docs/'documentaries').mkdir()
  (self.docs/'stylesheets').mkdir()
  (self.docs/'stylesheets'/'documentary.css').write_text('body{}')
  for slug in DOCUMENTARIES:
   (self.docs/'documentaries'/f'{slug}.md').write_text('<link href="../../stylesheets/documentary.css"><p>Unchanged text</p>')
 def tearDown(self):self.t.cleanup()
 def test_rewrite_exactly_eight_manuscripts_and_preserve_prose(self):
  p=self.docs/'documentaries'/'bsd.md';original=p.read_text()
  result=rewrite_temporary_docs(self.docs)
  self.assertEqual(len(result),8)
  self.assertTrue(all(x['asset_references_rebased']==1 for x in result))
  self.assertEqual(p.read_text(),original.replace('../../stylesheets','../stylesheets'))
  self.assertIn('<p>Unchanged text</p>',p.read_text())
 def test_missing_asset_fails_closed(self):
  (self.docs/'stylesheets/documentary.css').unlink()
  with self.assertRaisesRegex(ValueError,'unknown copied documentary asset'):
   rewrite_temporary_docs(self.docs)
 def test_missing_manuscript_fails_closed(self):
  (self.docs/'documentaries/bsd.md').unlink()
  with self.assertRaisesRegex(ValueError,'missing documentary source'):
   rewrite_temporary_docs(self.docs)
 def test_duplicate_asset_reference_fails_closed(self):
  p=self.docs/'documentaries/bsd.md';p.write_text(p.read_text()*2)
  with self.assertRaisesRegex(ValueError,'ambiguous documentary asset'):
   rewrite_temporary_docs(self.docs)
if __name__=='__main__':unittest.main()
