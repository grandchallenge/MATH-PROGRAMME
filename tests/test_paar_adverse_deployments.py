"""Honest fail-closed adversarial/Pages provenance record checks."""
import copy,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'governance'/'assurance'/'GCL-PAAR-001'
class AdverseAndDeploymentTests(unittest.TestCase):
 def setUp(self):
  self.raw=(ROOT/'ESTATE_NEGATIVE_AND_PUBLIC_20261017.json').read_bytes()
  self.x=json.loads((ROOT/'ESTATE_ADVERSE_DEPLOYMENTS_20261017.json').read_text())
 def check(self):
  x=self.x
  assert x['record_type']=='GCL_PAAR_001_FAILED_CHECK_AND_PAGES_DEPLOYMENT/1'
  assert x['prior_negative_snapshot_sha256']==hashlib.sha256(self.raw).hexdigest()
  assert len(x['negative_cases'])==20
  assert len({y['repository'] for y in x['negative_cases']})==20
  assert x['failed_check_candidate_count']==10
  assert len(x['pages_deployments'])==2
  assert x['successful_source_anchored_page_deployments']==2
  assert all(z['authenticated_deployment_status']=='success' and
             z['source_is_protected_ancestor'] is True and
             z['https_transport']=='PASS' and
             z['rendered_document_equivalent_to_accepted_source'] is False
             for z in x['pages_deployments'])
  assert all(z['causal_rejection_certified'] is False for z in x['negative_cases'])
  assert x['rejection_causality_certified'] is False
  assert x['document_parity_certified'] is False
  assert x['gcl_wide_assurance_certified'] is False
 def test_actual_evidence(self):self.check()
 def test_wrong_source_hash(self):
  self.x['prior_negative_snapshot_sha256']='0'*64
  with self.assertRaises(AssertionError):self.check()
 def test_duplicate_repo(self):
  self.x['negative_cases'][1]['repository']=self.x['negative_cases'][0]['repository']
  with self.assertRaises(AssertionError):self.check()
 def test_missing_ci_failure_case(self):
  self.x['failed_check_candidate_count']=9
  with self.assertRaises(AssertionError):self.check()
 def test_forged_source_deployment(self):
  self.x['pages_deployments'][0]['source_is_protected_ancestor']=False
  with self.assertRaises(AssertionError):self.check()
 def test_forged_page_parity(self):
  self.x['pages_deployments'][0]['rendered_document_equivalent_to_accepted_source']=True
  with self.assertRaises(AssertionError):self.check()
 def test_forged_failure_causality(self):
  self.x['negative_cases'][0]['causal_rejection_certified']=True
  with self.assertRaises(AssertionError):self.check()
 def test_fake_estate_certification(self):
  self.x['gcl_wide_assurance_certified']=True
  with self.assertRaises(AssertionError):self.check()
if __name__=='__main__':unittest.main()
