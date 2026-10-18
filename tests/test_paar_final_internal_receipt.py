"""Bounded internal receipt fidelity; no publication certification from this test."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'governance/assurance/GCL-PAAR-001'
RECEIPT=ROOT/'FINAL_INTERNAL_ASSURANCE_RECEIPT.json'
SHA=re.compile('[0-9a-f]{40}\\Z')
def check(x):
 assert x['record_type']=='GCL_PAAR_001_PROTECTED_INTERNAL_ASSURANCE_RECEIPT/1'
 assert x['decision']=='OPERATIONAL_AUDIT_COMPLETED_WITH_EXPLICIT_LIMITS'
 assert x['authority']=='GCL_ACCOUNTABLE_INTERNAL_ASSURANCE'
 assert x['protected_source_pr']==2735
 assert SHA.fullmatch(x['source_pr_head_sha']) and SHA.fullmatch(x['protected_source_merge_sha'])
 assert x['source_record']['path'].endswith('/INTERNAL_ASSURANCE_DECISION.json')
 assert x['source_record']['git_blob_sha']=='3442a89e997ceeda68209fac3dacab7983015096'
 assert x['human_readable_report']['git_blob_sha']=='7e4da3d22e22e85cbd3f5a3f5afe8fcb55292727'
 assert len(x['source_record']['sha256'])==64
 assert x['audit_population_count']==20 and x['branch_gaps_fixed_count']==3
 assert x['actual_validator_test_count']==243 and x['additional_audit_test_count']==43
 assert x['genuine_private_authenticated_control_readback'] is True
 assert x['parent_issue']=='grandchallenge/MATH-PROGRAMME#2705'
 assert x['standing_publication_certification_controls_unchanged'] is True
 for f in ('extra_external_assurance_review_required','mathematical_or_publication_certification',
 'historical_original_chad_execution_attested','every_rejection_causal_explanation_verified',
 'all_public_rendered_pages_exact_parity_verified'):
  assert x[f] is False
class FinalReceiptTests(unittest.TestCase):
 def setUp(self):self.x=json.loads(RECEIPT.read_text())
 def reject(self):
  with self.assertRaises((AssertionError,KeyError)):check(self.x)
 def test_original(self):check(self.x)
 def test_wrong_source_blob(self):
  self.x['source_record']['git_blob_sha']='0'*40;self.reject()
 def test_made_up_review_body(self):
  self.x['extra_external_assurance_review_required']=True;self.reject()
 def test_forged_scientific_certification(self):
  self.x['mathematical_or_publication_certification']=True;self.reject()
 def test_inflated_scope(self):
  self.x['audit_population_count']=22;self.reject()
 def test_forged_closed_exception(self):
  self.x['historical_original_chad_execution_attested']=True;self.reject()
if __name__=='__main__':unittest.main()
