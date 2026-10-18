"""Mutational tests for the bounded 20-repository live evidence contract."""
from __future__ import annotations
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'governance'/'assurance'/'GCL-PAAR-001'
sys.path.insert(0,str(ROOT))
from verify_estate_lifecycle import verify_report
class WorkflowEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.scope=(ROOT/'ESTATE_SCOPE_20261017.json').read_bytes()
        self.positive=json.loads((ROOT/'ESTATE_LIFECYCLE_READBACK_20261017.json').read_text())
        self.negative=json.loads((ROOT/'ESTATE_NEGATIVE_AND_PUBLIC_20261017.json').read_text())
        mapping=json.loads((ROOT/'ESTATE_CONTROL_MAPPING_14_20261017.json').read_text())
        self.classes={r['repository']:r['assertion_class'] for r in mapping['entries']}
        self.classes.update({
          'grandchallenge/CONTROL':'GCL_CONTROL_AND_PROJECT_ADMISSION',
          'grandchallenge/MATH-PROGRAMME':'SOURCE_PROOF_AND_PUBLICATION',
          'grandchallenge/MATHSOLVE':'MATHEMATICAL_SOLUTION_CLAIM',
          'grandchallenge/MATHCERT':'PROOF_CERTIFICATION_AND_REVIEW',
          'grandchallenge/INTELLECT':'SPECIALIST_REVIEW_AND_INDEPENDENT_ADMISSION',
          'grandchallenge/MATHFORGE':'MATHEMATICAL_PRODUCTION_EXECUTION'})
    def verify(self):
        result=verify_report(self.positive,self.scope,self.classes)
        a=self.negative
        assert a['record_type']=='GCL_PAAR_001_REJECTED_STATE_AND_PUBLIC_HTTPS/1'
        assert a['source_lifecycle_sha256']==hashlib.sha256(
            (ROOT/'ESTATE_LIFECYCLE_READBACK_20261017.json').read_bytes()).hexdigest()
        assert len(a['negative_samples'])==20
        assert len({v['repository'] for v in a['negative_samples']})==20
        assert a['closed_unmerged_samples']==17
        assert a['successful_https_pages']==2
        assert a['actual_negative_transition_causality_proven'] is False
        assert a['published_semantic_equivalence_proven'] is False
        assert a['global_assurance_certified'] is False
        assert all(p['published_document_semantically_matches_source']=='NOT_VERIFIED'
                   for p in a['pages'])
        assert not result['semantic_enforcement_certified']
    def test_bounded_live_readback(self):self.verify()
    def test_missing_repo_rejected(self):
        self.positive['repositories'].pop()
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_duplicate_repo_rejected(self):
        self.positive['repositories'][1]['repository']=self.positive['repositories'][0]['repository']
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_forged_merged_pr_rejected(self):
        self.positive['repositories'][0]['recent_protected_candidate']['authenticated_merged_pr']=False
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_forged_protected_branch_rejected(self):
        self.positive['repositories'][0]['current_default_branch']['protected']=False
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_wrong_source_sha_rejected(self):
        self.positive['repositories'][1]['recent_protected_candidate']['head_sha']='0'*39
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_forged_scientific_certification_rejected(self):
        self.positive['repositories'][0]['semantic_assertion_certified']=True
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_forged_public_mirror_claim_rejected(self):
        self.positive['repositories'][0]['publication']['source_to_mirror_equivalence']='PASS'
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_forged_negative_gate_certification_rejected(self):
        self.negative['actual_negative_transition_causality_proven']=True
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_forged_public_semantics_rejected(self):
        self.negative['pages'][0]['published_document_semantically_matches_source']='PASS'
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_negative_scope_incomplete_rejected(self):
        self.negative['negative_samples'].pop()
        with self.assertRaises((ValueError,AssertionError)):self.verify()
    def test_global_claim_rejected(self):
        self.positive['estate_wide_integrity_certified']=True
        with self.assertRaises((ValueError,AssertionError)):self.verify()
if __name__=='__main__':unittest.main()
