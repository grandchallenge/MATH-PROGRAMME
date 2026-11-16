import json
import tempfile
import unittest
from pathlib import Path
from ci.zensical_semantic_parity import governed_asset_census,search_parity

class SearchAssetAuditTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.a=Path(self.tmp.name)/'a';self.b=Path(self.tmp.name)/'b'
  self.a.mkdir();self.b.mkdir()
 def tearDown(self):self.tmp.cleanup()
 def put(self,root,rel,content):
  p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
 def test_identical_governed_source_assets(self):
  for root in (self.a,self.b):self.put(root,'assets/documentaries/bsd/cover.svg','<svg/>')
  self.assertTrue(governed_asset_census(self.a,self.b)['byte_identical_on_shared_source_assets'])
 def test_missing_or_mutated_governed_assets_rejected(self):
  self.put(self.a,'javascripts/documentary.js','correct')
  self.assertEqual(governed_asset_census(self.a,self.b)['missing_governed_asset_count'],1)
  self.put(self.b,'javascripts/documentary.js','wrong')
  self.assertEqual(governed_asset_census(self.a,self.b)['changed_governed_asset_count'],1)
 def test_search_index_location_set_proven(self):
  index=json.dumps({'docs':[{'location':'erdos/index.html','title':'Erdos','text':'text'}]})
  for root in (self.a,self.b):self.put(root,'search/search_index.json',index)
  self.assertTrue(search_parity(self.a,self.b)['search_parity_proven'])
 def test_missing_search_index_and_location_not_certified(self):
  self.put(self.a,'search/search_index.json',json.dumps({'docs':[{'location':'oai26/','title':'OAI'}]}))
  self.assertEqual(len(search_parity(self.a,self.b)['missing_baseline_search_files']),1)
  self.put(self.b,'search/search_index.json',json.dumps({'docs':[{'location':'index.html'}]}))
  self.assertEqual(search_parity(self.a,self.b)['missing_indexed_locations_count'],1)
 def test_unknown_search_schema_is_inconclusive(self):
  for root in (self.a,self.b):self.put(root,'search/search_index.json','{}')
  self.assertFalse(search_parity(self.a,self.b)['search_parity_proven'])
if __name__=='__main__':unittest.main()
