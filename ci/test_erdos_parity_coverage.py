"""Safeguards for autonomous, exact-hash accepted parity coverage."""
import copy,hashlib,json,unittest
from unittest.mock import patch
from erdos_parity_auto import verified_browser_render
from erdos_parity_coverage import RECORD,verify_ledger,plan,apply_receipt
SHA='a'*40;SHA2='b'*40;H1='1'*64;H2='2'*64

def base():return {'record_type':RECORD,'baseline_protected_sha':SHA,'baseline_accepted':{'99':H1,'100':H1},'covered':{},'bootstrap_ids':[99]}
def article(n,sha=H1):return {'problem_id':n,'source_sha256':sha,'source_commit':SHA,'deployed_source_commit':SHA,'public_html_sha256':H2,'status':'PASS_SOURCE_AND_RENDERED_HTML_PARITY','visible_math_count':10,'verified_math_expressions':10,'verified_editorial_sections':6,'mathjax_startup_complete':True}
def report(*articles):return {'record_type':'ERDOS_ACCEPTED_PARITY_BATCH_EVIDENCE/1','run_id':123,'deployed_source_sha':SHA,'articles':list(articles)}
class CoverageTests(unittest.TestCase):
 def test_initial_canary_only(self):self.assertEqual(plan(base(),{99:{'source_sha256':H1},100:{'source_sha256':H1}}),([99],0))
 def test_new_acceptance(self):self.assertEqual(plan(base(),{99:{'source_sha256':H1},100:{'source_sha256':H1},101:{'source_sha256':H2}}),([99,101],0))
 def test_changed_accepted(self):self.assertEqual(plan(base(),{99:{'source_sha256':H1},100:{'source_sha256':H2}}),([99,100],0))
 def test_protected_receipt_clears_only_exact_source(self):
  ledger=apply_receipt(base(),report(article(99))); self.assertEqual(plan(ledger,{99:{'source_sha256':H1},100:{'source_sha256':H1}}),([],0))
  self.assertEqual(plan(ledger,{99:{'source_sha256':H2},100:{'source_sha256':H1}}),([99],0))
 def test_pending_artifact_not_coverage(self):self.assertEqual(plan(base(),{99:{'source_sha256':H1}}),([99],0))
 def test_batch_is_bounded(self):
  current={n:{'source_sha256':H2} for n in range(99,170)};a,remaining=plan(base(),current);self.assertEqual((len(a),remaining),(25,46))
 def test_missing_receipt_rejected(self):
  with self.assertRaises(ValueError):apply_receipt(base(),{'record_type':'ERDOS_ACCEPTED_PARITY_BATCH_EVIDENCE/1','run_id':123,'deployed_source_sha':SHA,'articles':[]})
 def test_malformed_head_rejected(self):
  l=base();l['baseline_protected_sha']='short'
  with self.assertRaises(ValueError):verify_ledger(l)
 def test_forged_pass_rejected(self):
  a=article(99);a['status']='FAIL'
  with self.assertRaises(ValueError):apply_receipt(base(),report(a))
 def test_wrong_deployed_sha_rejected(self):
  a=article(99);a['deployed_source_commit']=SHA2
  with self.assertRaises(ValueError):apply_receipt(base(),report(a))
 def test_missing_mathjax_rejected(self):
  a=article(99);a['visible_math_count']=0
  with self.assertRaises(ValueError):apply_receipt(base(),report(a))
 def test_duplicate_article_rejected(self):
  with self.assertRaises(ValueError):apply_receipt(base(),report(article(99),article(99)))
 def test_mutated_coverage_refuses_silent_success(self):
  l=apply_receipt(base(),report(article(99)));l['covered']['99']['receipt_sha256']='fake'
  with self.assertRaises(ValueError):verify_ledger(l)
 def test_invalid_added_seed_rejected(self):
  l=base();l['bootstrap_ids']=[101]
  with self.assertRaises(ValueError):verify_ledger(l)
class BrowserRetryTests(unittest.TestCase):
 def test_transient_cdn_timeout_recovers_without_count_change(self):
  proof={'visible_math_count':10,'mathjax_startup_complete':True}
  with patch('erdos_parity_auto.assert_rendered_math',side_effect=[ValueError('cdn'),proof]) as v,patch('erdos_parity_auto.time.sleep') as pause:
   self.assertEqual(verified_browser_render(object(),'https://example.test/',10),proof)
   self.assertEqual(v.call_count,2)
   self.assertEqual(v.call_args.args[-1],10)
 def test_persistent_wrong_math_must_fail(self):
  with patch('erdos_parity_auto.assert_rendered_math',side_effect=ValueError('missing_math')) as v,patch('erdos_parity_auto.time.sleep'):
   with self.assertRaisesRegex(ValueError,'missing_math'):
    verified_browser_render(object(),'https://example.test/',10)
   self.assertEqual(v.call_count,3)
 def test_unbounded_retry_is_rejected(self):
  with self.assertRaises(ValueError):verified_browser_render(None,'https://example.test/',10,attempts=99)
if __name__=='__main__':unittest.main()
