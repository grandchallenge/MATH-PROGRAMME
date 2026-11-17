import unittest
from ci.renderer_browser_b02 import CASES,EXPLORATORY,SIZES,check
class BrowserSearchContract(unittest.TestCase):
 def ok(self,href):return {'input_selected':True,'errors':[], 'results':[{'href':href,'text':'Relevant'}]}
 def test_grounded_mathematical_oracle(self):
  self.assertTrue(len(CASES)>=7)
  self.assertTrue(any('erdos/problems/0001/index.html'==x['target'] for x in CASES))
  self.assertTrue(any('oai26/catalogue/index.html'==x['target'] for x in CASES))
  self.assertEqual(set(SIZES),{'desktop','mobile'})
 def test_exact_canonical_target_present(self):
  self.assertFalse(check(self.ok('http://localhost/MATH-PROGRAMME/erdos/problems/0001/'),'erdos/problems/0001/index.html'))
 def test_unrelated_link_is_not_success(self):
  self.assertIn('REQUIRED_TARGET_NOT_FOUND',check(self.ok('http://localhost/MATH-PROGRAMME/erdos/problems/0002/'),'erdos/problems/0001/index.html'))
 def test_missing_input_and_js_error_fail(self):
  x=self.ok('http://localhost/MATH-PROGRAMME/CMDG_CM4/');x['input_selected']=False;x['errors']=['failed'];self.assertEqual(set(check(x,'CMDG_CM4/index.html')),{'NO_USABLE_SEARCH_INPUT','JAVASCRIPT_PAGEERROR'})
 def test_diagnostic_query_is_not_false_acceptance(self):
  self.assertEqual(check({'input_selected':False,'errors':[], 'results':[]},None),[])
  self.assertTrue(any('ζ' in x for x in EXPLORATORY))
if __name__=='__main__':unittest.main()
