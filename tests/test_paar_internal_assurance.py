"""GCL internal audit claim-boundary and source-pinning hostile controls."""
from pathlib import Path
import copy
import json
import re
import unittest

P=Path(__file__).resolve().parents[1]/'governance/assurance/GCL-PAAR-001/INTERNAL_ASSURANCE_DECISION.json'
SHA=re.compile('[0-9a-f]{40}\\Z')

def check(x):
    assert x['record_type']=='GCL_PAAR_001_INTERNAL_INTEGRITY_ASSURANCE_DECISION/1'
    assert x['operational_audit']=='COMPLETE_WITH_RECORDED_LIMITS'
    assert x['bounded_20_repo_scope'] is True
    assert x['authority']=='GCL_ACCOUNTABLE_INTERNAL_AUDIT'
    assert SHA.fullmatch(x['protected_source_head_sha'])
    assert len(x['evidence_source_blobs'])==7
    assert len({e['path'] for e in x['evidence_source_blobs']})==7
    assert all(SHA.fullmatch(e['git_blob_sha']) and e['bytes']>0 for e in x['evidence_source_blobs'])
    assert x['actual_live_evidence']['merged_pr_with_successful_ci_samples']==20
    assert x['actual_live_evidence']['closed_unmerged_pr_samples']==17
    assert x['actual_live_evidence']['closed_unmerged_pr_samples_with_failed_check_runs']==10
    assert x['actual_live_evidence']['private_executive_required_ci_checked']==3
    assert x['regression']['actual_validator_tests_passed']==243
    assert x['regression']['additional_assurance_evidence_tests_passed']==43
    assert x['final_receipt_protected'] is False
    assert x['status']=='INTERNAL_AUDIT_FINAL_SOURCE_PENDING_PROTECTED_ADMISSION'
    assert x['not_a_publication_certification'] is True
    assert all(val is False for val in x['limits'].values())
    assert {e['id'] for e in x['exceptions']}=={
        'HISTORICAL_CHAD_ORIGIN','COMPLETE_PUBLICATION_CONTENT_PARITY',
        'UNIVERSAL_CAUSAL_REJECTION','PRIVATE_CONTENT'}
    return True

class InternalAssuranceTests(unittest.TestCase):
    def setUp(self): self.x=json.loads(P.read_text(encoding='utf-8'))
    def test_original_source_and_scope(self):check(self.x)
    def reject(self):
        with self.assertRaises((AssertionError,KeyError,TypeError)):check(self.x)
    def test_missing_source_rejected(self):
        self.x['evidence_source_blobs'].pop();self.reject()
    def test_duplicate_source_rejected(self):
        self.x['evidence_source_blobs'][1]['path']=self.x['evidence_source_blobs'][0]['path'];self.reject()
    def test_forged_sha_rejected(self):
        self.x['evidence_source_blobs'][0]['git_blob_sha']='0'*39;self.reject()
    def test_inflated_coverage_rejected(self):
        self.x['actual_live_evidence']['merged_pr_with_successful_ci_samples']=21;self.reject()
    def test_false_certification_rejected(self):
        self.x['limits']['mathematical_theorem_certification']=True;self.reject()
    def test_hidden_historical_exception_rejected(self):
        self.x['exceptions'][0]['id']='ASSUMED_PROVEN';self.reject()
    def test_unprotected_receipt_claim_rejected(self):
        self.x['final_receipt_protected']=True;self.reject()

if __name__=='__main__':unittest.main()
