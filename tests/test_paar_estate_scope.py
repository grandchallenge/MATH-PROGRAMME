"""Bounded estate enumeration integrity, not semantic assertion certification."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]/'governance/assurance/GCL-PAAR-001'

class EstateScopeTests(unittest.TestCase):
    def setUp(self):
        self.raw=(HERE/'ESTATE_SCOPE_20261017.json').read_bytes()
        self.scope=json.loads(self.raw)
        self.surfaces=json.loads((HERE/'ESTATE_SURFACES_20261017.json').read_text())
    def verify(self):
        a=self.scope['repositories']; b=self.surfaces['sources']
        assert self.scope['record_type']=='GCL_PAAR_001_ESTATE_SCOPE_SNAPSHOT/1'
        assert len(a)==len(b)==20
        assert len(set(x['repository'] for x in a))==len(a)
        assert len(set(x['repository'] for x in b))==len(b)
        assert set(x['repository'] for x in a)==set(x['repository'] for x in b)
        assert self.surfaces['scope_file_sha256']==hashlib.sha256(self.raw).hexdigest()
        assert all(x['tree_status']=='COMPLETE' for x in b)
        assert all(x['head_sha']==next(y['head'] for y in b if y['repository']==x['repository']) for x in a)
        assert self.scope['active_count']==20 and self.scope['original_sample_count']==6
        assert self.scope['unverified_mapping_count']==14
        assert self.scope['global_integrity_certified'] is False
        assert self.surfaces['semantic_assurance_certified'] is False
    def test_actual_complete_pins(self):self.verify()
    def test_missing_repo_rejected(self):
        self.scope['repositories'].pop()
        with self.assertRaises(AssertionError):self.verify()
    def test_duplicate_repo_rejected(self):
        self.scope['repositories'][1]['repository']=self.scope['repositories'][0]['repository']
        with self.assertRaises(AssertionError):self.verify()
    def test_head_changed_rejected(self):
        self.scope['repositories'][0]['head_sha']='0'*40
        with self.assertRaises(AssertionError):self.verify()
    def test_truncated_tree_rejected(self):
        self.surfaces['sources'][0]['tree_status']='TRUNCATED'
        with self.assertRaises(AssertionError):self.verify()
    def test_forged_complete_certification_rejected(self):
        self.scope['global_integrity_certified']=True
        with self.assertRaises(AssertionError):self.verify()
    def test_retyped_unverified_is_not_pass(self):
        self.scope['unverified_mapping_count']=0
        with self.assertRaises(AssertionError):self.verify()

if __name__=='__main__':unittest.main()
