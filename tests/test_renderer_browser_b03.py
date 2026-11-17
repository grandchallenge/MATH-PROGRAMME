import unittest
from ci.renderer_browser_b03 import ROUTES,VIEWS,new_severe
class AccessibilityContract(unittest.TestCase):
 def test_templates(self):
  self.assertEqual(len(ROUTES),8)
  self.assertTrue('oai26/catalogue/index.html' in ROUTES)
  self.assertEqual(set(VIEWS),{'mobile','desktop','reflow200'})
 def test_baseline_severe_not_misreported(self):
  old=[{'id':'color-contrast','impact':'serious'}]
  self.assertEqual(new_severe(old,old),[])
 def test_new_serious_fails(self):
  v=[{'id':'button-name','impact':'serious','nodes':2}]
  self.assertEqual(new_severe([],v)[0]['rule'],'button-name')
 def test_new_minor_is_diagnostic(self):
  self.assertEqual(new_severe([],[{'id':'region','impact':'moderate','nodes':1}]),[])
 def test_different_severity_requires_independent_review(self):
  self.assertEqual(new_severe([{'id':'label','impact':'minor'}],[{'id':'label','impact':'critical','nodes':3}])[0]['impact'],'critical')
if __name__=='__main__':unittest.main()
