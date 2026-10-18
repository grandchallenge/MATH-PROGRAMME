"""Offline exact-head source mapping and negative controls."""
import hashlib,json,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'governance/assurance/GCL-PAAR-001'
class MapTests(unittest.TestCase):
 def setUp(self):
  self.scope=json.loads((P/'ESTATE_SCOPE_20261017.json').read_text())
  self.m=json.loads((P/'ESTATE_CONTRACT_SOURCES_20261017.json').read_text())
  self.b=json.loads((P/'BRANCH_PROTECTION_EXCEPTIONS_20261017.json').read_text())
  self.r=json.loads((P/'RESEARCH_RUN_WITNESSES_20261017.json').read_text())
 def check(self):
  known={x['repository']:x for x in self.scope['repositories'] if not x['prior_six_repo_control_sample']}
  rows=self.m['entries']
  assert len(rows)==len(known)==14
  assert {x['repository'] for x in rows}==set(known)
  assert self.m['semantic_assurance'] is False
  assert self.m['scope_sha256']==hashlib.sha256((P/'ESTATE_SCOPE_20261017.json').read_bytes()).hexdigest()
  for x in rows:
   assert x['head']==known[x['repository']]['head_sha']
   assert x['status']=='PINNED_SOURCE_ONLY_NOT_ENFORCEMENT'
   if x['private']:assert 'workflows' not in x and 'governance_sources' not in x
  assert len(self.b['exceptions'])==3
  for x in self.b['exceptions']:
   assert x['branch_protected'] is False and x['effective_rules']==[]
   assert x['legacy_protection_endpoint_status']==404
  assert len(self.r['runs'])==3
  for x in self.r['runs']:
   assert x['head']==known[x['repository']]['head_sha']
   assert x['conclusion']=='success' and x['semantic_admission_verified'] is False
 def test_actual(self):self.check()
 def test_missing(self):
  self.m['entries'].pop()
  with self.assertRaises(AssertionError):self.check()
 def test_stale_head(self):
  self.m['entries'][0]['head']='0'*40
  with self.assertRaises(AssertionError):self.check()
 def test_duplicate(self):
  self.m['entries'][1]['repository']=self.m['entries'][0]['repository']
  with self.assertRaises(AssertionError):self.check()
 def test_unjustified_certification(self):
  self.m['semantic_assurance']=True
  with self.assertRaises(AssertionError):self.check()
 def test_incorrect_branch_status(self):
  self.b['exceptions'][0]['branch_protected']=True
  with self.assertRaises(AssertionError):self.check()
 def test_incorrect_run_scope(self):
  self.r['runs'][0]['semantic_admission_verified']=True
  with self.assertRaises(AssertionError):self.check()
 def test_gsd_path_filter(self):
  g=next(x for x in self.m['entries'] if x['repository'].endswith('/GSD'))
  w=g['workflows'][0]
  self.assertEqual(w['path'],'.github/workflows/ci.yml')
  for event in ('pull_request','push'):
   paths=w['events'][event]['paths']
   self.assertIn('.github/workflows/gsd-ci.yml',paths)
   self.assertNotIn('.github/workflows/ci.yml',paths)

if __name__=='__main__':unittest.main()
