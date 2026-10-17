"""Protect the finite post-audit remit from duplicate programmes or fake passes."""
import json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'governance/assurance/GCL-PAAR-001/POST_AUDIT_CORRECTIVE_ACTIONS.json'
def verify(x):
 assert x['record_type']=='GCL_PAAR_001_BOUNDED_POST_AUDIT_ACTIONS/1'
 assert x['audit_state']=='CLOSED' and x['new_umbrella_programme'] is False
 assert len(x['actions'])==2 and len({a['id'] for a in x['actions']})==2
 assert [a['owner_issue'] for a in x['actions']]==['grandchallenge/CONTROL#5','grandchallenge/MATH-PROGRAMME#2552']
 assert all(a['state']=='PREPARED_NOT_IMPLEMENTED' and len(a['acceptance'])>=4 for a in x['actions'])
 assert x['historical_exception']=='CHAD_ORIGINAL_EXECUTION_UNATTESTED'
 assert x['additional_external_integrity_review_required'] is False
 assert x['mathematical_certification_claimed'] is False
class RemedialTests(unittest.TestCase):
 def setUp(self):self.x=json.loads(P.read_text())
 def reject(self):
  with self.assertRaises((AssertionError,KeyError)):verify(self.x)
 def test_baseline(self):verify(self.x)
 def test_added_umbrella(self):self.x['new_umbrella_programme']=True;self.reject()
 def test_duplicate(self):self.x['actions'][1]['id']=self.x['actions'][0]['id'];self.reject()
 def test_fake_implementation(self):self.x['actions'][0]['state']='DONE';self.reject()
 def test_retrospective_origin_upgrade(self):self.x['historical_exception']='CERTIFIED';self.reject()
 def test_external_review_bottleneck(self):self.x['additional_external_integrity_review_required']=True;self.reject()
 def test_false_science_certification(self):self.x['mathematical_certification_claimed']=True;self.reject()
if __name__=='__main__':unittest.main()
