"""Protect the finite post-audit remit from duplicate programmes or fake passes."""
import json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'governance/assurance/GCL-PAAR-001/POST_AUDIT_CORRECTIVE_ACTIONS.json'
def verify(x):
 assert x['record_type']=='GCL_PAAR_001_BOUNDED_POST_AUDIT_ACTIONS/1'
 assert x['audit_state']=='CLOSED' and x['new_umbrella_programme'] is False
 assert len(x['actions'])==2 and len({a['id'] for a in x['actions']})==2
 assert [a['owner_issue'] for a in x['actions']]==['grandchallenge/CONTROL#5','grandchallenge/MATH-PROGRAMME#2552']
 assert [a['state'] for a in x['actions']]==['IMPLEMENTED_BOUNDED_FAIL_CLOSED','IMPLEMENTED_HOSTED_VERIFIED']
 assert all(len(a['acceptance'])>=4 and a['proof'].endswith('/POST_AUDIT_REMEDIATION_IMPLEMENTATION_20261017.json') for a in x['actions'])
 assert x['historical_exception']=='CHAD_ORIGINAL_EXECUTION_UNATTESTED'
 assert x['additional_external_integrity_review_required'] is False
 assert x['mathematical_certification_claimed'] is False
E=P.with_name('POST_AUDIT_REMEDIATION_IMPLEMENTATION_20261017.json')
def verify_evidence(e):
 assert e['record_type']=='GCL_PAAR_001_FINITE_CORRECTIVE_IMPLEMENTATION_READBACK/1'
 assert e['R1']['pr']==32 and e['R1']['protected_merge_sha']==e['R1']['active_release_commit_sha']
 assert e['R1']['local_capture_authority']=='OS_ACCOUNT_ONLY'
 assert e['R1']['local_capture_original_execution_attested'] is False
 assert e['R1']['control_unit_regression_count']==342
 assert e['R1']['material_acceptance_rule']=='LOCAL_CAPTURE_MAY_NOT_CERTIFY_ORIGINAL_EXECUTION_USE_VERIFIED_HOSTED_RUN'
 assert e['R2']['pr']==2741 and e['R2']['protected_merge_sha']==e['R2']['deployed_source_sha']
 assert e['R2']['hosted_workflow_run']==39076844379 and e['R2']['hosted_conclusion']=='success'
 assert e['R2']['verified_problem_id']==99
 assert (e['R2']['verified_editorial_sections'],e['R2']['verified_equations'],e['R2']['verified_real_browser_equations'])==(6,10,10)
 assert e['R2']['existing_protocol_reused'] is True
 assert all(v is False for v in e['limits'].values())
class RemedialTests(unittest.TestCase):
 def setUp(self):self.x=json.loads(P.read_text())
 def reject(self):
  with self.assertRaises((AssertionError,KeyError)):verify(self.x)
 def test_baseline(self):verify(self.x);verify_evidence(json.loads(E.read_text()))
 def test_added_umbrella(self):self.x['new_umbrella_programme']=True;self.reject()
 def test_duplicate(self):self.x['actions'][1]['id']=self.x['actions'][0]['id'];self.reject()
 def test_fake_implementation(self):self.x['actions'][0]['state']='DONE';self.reject()
 def test_retrospective_origin_upgrade(self):self.x['historical_exception']='CERTIFIED';self.reject()
 def test_external_review_bottleneck(self):self.x['additional_external_integrity_review_required']=True;self.reject()
 def test_false_science_certification(self):self.x['mathematical_certification_claimed']=True;self.reject()
 def test_no_forged_independent_chad_provenance(self):
  e=json.loads(E.read_text());e['R1']['local_capture_original_execution_attested']=True
  with self.assertRaises(AssertionError):verify_evidence(e)
 def test_no_forged_global_publication_parity(self):
  e=json.loads(E.read_text());e['limits']['all_1221_articles_rechecked']=True
  with self.assertRaises(AssertionError):verify_evidence(e)
 def test_hosted_publication_evidence_not_inflated(self):
  e=json.loads(E.read_text());e['R2']['verified_real_browser_equations']=0
  with self.assertRaises(AssertionError):verify_evidence(e)
if __name__=='__main__':unittest.main()
