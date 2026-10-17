"""Structural, bounded regression of PAAR-001 mapped sources and branch receipts."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/'governance/assurance/GCL-PAAR-001'

class FourteenControlMappingTests(unittest.TestCase):
    def setUp(self):
        self.scope_raw=(ROOT/'ESTATE_SCOPE_20261017.json').read_bytes()
        self.source_raw=(ROOT/'ESTATE_CONTRACT_SOURCES_20261017.json').read_bytes()
        self.mapping=json.loads((ROOT/'ESTATE_CONTROL_MAPPING_14_20261017.json').read_text())
        self.repairs=json.loads((ROOT/'BRANCH_PROTECTION_REPAIRS_20261017.json').read_text())
        self.scope=json.loads(self.scope_raw)
        self.source=json.loads(self.source_raw)
    def verify(self):
        m=self.mapping;r=self.repairs
        expected={x['repository']:x for x in self.scope['repositories']
                  if not x['prior_six_repo_control_sample']}
        source={x['repository']:x for x in self.source['entries']}
        rows=m['entries']
        assert m['record_type']=='GCL_PAAR_001_FOURTEEN_REPOSITORY_CONTROL_MAPPING/1'
        assert len(expected)==len(source)==len(rows)==14
        assert len(set(x['repository'] for x in rows))==14
        assert set(expected)==set(source)=={x['repository'] for x in rows}
        assert m['pinned_scope_sha256']==hashlib.sha256(self.scope_raw).hexdigest()
        assert m['source_map_sha256']==hashlib.sha256(self.source_raw).hexdigest()
        assert m['known_workflow_routes']==44
        assert m['semantic_enforcement_established'] is False
        assert m['scientific_or_gcl_wide_assurance_certified'] is False
        for row in rows:
            name=row['repository']
            assert row['scope_pinned_main_sha']==expected[name]['head_sha']==source[name]['head']
            assert row['source_map_state']=='PINNED_PRODUCER_AND_WORKFLOW_CONSUMER_IDENTIFIED'
            assert row['independent_specialist_semantic_review']=='NOT_VERIFIED_IN_THIS_MAP'
            assert row['public_mirror_accuracy']=='NOT_VERIFIED_IN_THIS_MAP'
            assert row['branch_enforcement']['protected'] is True
            assert row['branch_enforcement']['observed_class']=='PROTECTED_WITH_PR_AND_REQUIRED_CI'
            assert row['branch_enforcement']['required_status_contexts']
            assert len(row['controller_consumer_routes'])==len(source[name].get('workflows',[]))
        assert r['record_type']=='GCL_PAAR_001_BRANCH_CONTROL_REMEDIATION/1'
        assert r['frozen_scope_sha256']==hashlib.sha256(self.scope_raw).hexdigest()
        assert r['original_exceptions']==r['resolved']==3 and r['unresolved']==0
        assert {x['repository'] for x in r['repositories']}=={
            'grandchallenge/ADAPTIVE-INTELLIGENCE-ATLAS',
            'grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS','grandchallenge/GSD'}
        assert r['full_20_repositories_semantic_assurance'] is False
        contexts={'grandchallenge/ADAPTIVE-INTELLIGENCE-ATLAS':['validate'],
          'grandchallenge/COMPUTATIONAL-DIFFICULTY-ATLAS':['direct-return-contract'],
          'grandchallenge/GSD':['unit']}
        for x in r['repositories']:
            assert x['enforcement']=='active' and x['bypass_actors']==[]
            assert x['blanket_approving_review_count']==0
            assert x['required_status_checks']==contexts[x['repository']]
            assert {'pull_request','deletion','non_fast_forward','required_status_checks'} <= set(x['effective_rule_types'])
            assert x['verification']=='PASS_EFFECTIVE_GITHUB_RULE_READBACK'
            assert x['scientific_certification'] is False
    def test_protected_snapshot_consistency(self):self.verify()
    def test_missing_repo_fails(self):
        self.mapping['entries'].pop()
        with self.assertRaises(AssertionError):self.verify()
    def test_duplicate_repo_fails(self):
        self.mapping['entries'][1]['repository']=self.mapping['entries'][0]['repository']
        with self.assertRaises(AssertionError):self.verify()
    def test_wrong_source_git_head_fails(self):
        self.mapping['entries'][0]['scope_pinned_main_sha']='0'*40
        with self.assertRaises(AssertionError):self.verify()
    def test_missing_required_ci_fails(self):
        self.mapping['entries'][0]['branch_enforcement']['required_status_contexts']=[]
        with self.assertRaises(AssertionError):self.verify()
    def test_claim_upgrade_fails(self):
        self.mapping['semantic_enforcement_established']=True
        with self.assertRaises(AssertionError):self.verify()
    def test_no_protection_fails(self):
        self.repairs['repositories'][0]['effective_rule_types'].remove('pull_request')
        with self.assertRaises(AssertionError):self.verify()
    def test_false_reviewer_count_fails(self):
        self.repairs['repositories'][1]['blanket_approving_review_count']=1
        with self.assertRaises(AssertionError):self.verify()
    def test_false_chad_or_science_claim_fails(self):
        self.repairs['repositories'][0]['scientific_certification']=True
        with self.assertRaises(AssertionError):self.verify()
    def test_legacy_branch_protection_is_recorded(self):
        rows={e['repository']:e for e in self.mapping['entries']}
        self.assertEqual(rows['grandchallenge/TROVE-CURATA']['branch_enforcement']['mechanism'],'LEGACY_BRANCH_PROTECTION')
        self.assertIn('replay',rows['grandchallenge/TROVE-CURATA']['branch_enforcement']['required_status_contexts'])

if __name__=='__main__': unittest.main()
