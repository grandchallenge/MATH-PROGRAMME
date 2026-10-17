"""Bounded source-to-public parity specimen cannot promote global conclusions."""
import copy,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/'governance'/'assurance'/'GCL-PAAR-001'
class PublicSpecimens(unittest.TestCase):
 def setUp(self):
  self.raw=(ROOT/'ESTATE_ADVERSE_DEPLOYMENTS_20261017.json').read_bytes()
  self.x=json.loads((ROOT/'ESTATE_PUBLIC_CONTENT_SPECIMEN_20261017.json').read_text())
 def check(self):
  x=self.x
  assert x['record_type']=='GCL_PAAR_001_PUBLIC_CONTENT_SPECIMEN/1'
  assert x['source_deployment_evidence_sha256']==hashlib.sha256(self.raw).hexdigest()
  assert x['showcase']['matched']==len(x['showcase']['matching_excerpts'])==5
  assert len(set(x['showcase']['matching_excerpts']))==5
  assert len(x['showcase']['source_commit_sha'])==40
  assert len(x['showcase']['source_git_blob_sha'])==40
  assert x['aether']['source_marker_verified'] is True
  assert x['showcase']['full_document_equivalence_verified'] is False
  assert x['aether']['full_document_equivalence_verified'] is False
  assert x['all_publications_certified'] is False
  assert x['scientific_certification'] is False
  assert x['gcl_wide_assurance_certified'] is False
 def test_actual(self):self.check()
 def test_wrong_source(self):
  self.x['source_deployment_evidence_sha256']='0'*64
  with self.assertRaises(AssertionError):self.check()
 def test_missing_visible_text(self):
  self.x['showcase']['matching_excerpts'].pop()
  with self.assertRaises(AssertionError):self.check()
 def test_forged_version_marker(self):
  self.x['aether']['source_marker_verified']=False
  with self.assertRaises(AssertionError):self.check()
 def test_false_full_parity(self):
  self.x['showcase']['full_document_equivalence_verified']=True
  with self.assertRaises(AssertionError):self.check()
 def test_false_certification(self):
  self.x['gcl_wide_assurance_certified']=True
  with self.assertRaises(AssertionError):self.check()
if __name__=='__main__':unittest.main()
