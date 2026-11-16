import unittest
from ci.renderer_browser_b01 import ROUTES,SIZES,compare
class B01Contract(unittest.TestCase):
 def page(self,**kwargs):
  v=dict(status=200,main=True,chars=500,h1='Mathematics',broken_images=[],overflow=0,clipped_math=[],rendered_math=12)
  v.update(kwargs);return v
 def test_covers_all_documentary_and_core_surfaces(self):
  self.assertEqual(len(ROUTES),16)
  self.assertEqual(len([x for x in ROUTES if x.startswith('documentaries/')]),8)
  self.assertEqual(set(SIZES),{'desktop','mobile'})
 def test_identical_math_is_not_defect(self):
  self.assertEqual(compare(self.page(),self.page(),'CMDG_CM4/index.html','mobile','default'),[])
 def test_missing_math_is_critical_when_baseline_rendered(self):
  r=compare(self.page(),self.page(rendered_math=0),'CMDG_CM4/index.html','desktop','default')
  self.assertIn('MATHJAX_RENDERING_LOST',[x['code'] for x in r])
 def test_candidate_only_clipping_or_images_is_defect(self):
  r=compare(self.page(),self.page(clipped_math=[[0,1200]],broken_images=['lost.svg']),'documentaries/bsd/index.html','mobile','default')
  self.assertEqual({x['code'] for x in r},{'CANDIDATE_CLIPPED_MATH','CANDIDATE_BROKEN_IMAGES'})
 def test_inherited_overflow_is_not_diagnosed_as_candidate_only(self):
  r=compare(self.page(overflow=55),self.page(overflow=57),'erdos/problems/0001/index.html','mobile','default')
  self.assertFalse(r)
 def test_lost_main_and_h1_reported(self):
  r=compare(self.page(),self.page(chars=5,h1='Other'),'index.html','desktop','default')
  self.assertEqual({x['code'] for x in r},{'CANDIDATE_PAGE_UNREADABLE','HEADING_CHANGED'})
if __name__=='__main__':unittest.main()
