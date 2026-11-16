import json
import tempfile
import unittest
from pathlib import Path
from ci.zensical_semantic_parity import governed_asset_census,search_parity,canonical_search_route

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
 def test_mkdocs_and_zensical_distinct_index_formats_preserve_page_locations(self):
  baseline={'docs':[{'location':'erdos/index.html#section','title':'Erdos','text':'text'},
                    {'location':'oai26/','title':'OAI'}]}
  candidate={'config':{'lang':['en']},'items':[
    {'location':'erdos/#section','level':1,'title':'Erdos','text':'text','path':[],'tags':[]},
    {'location':'oai26/','level':0,'title':'OAI','text':'text','path':[],'tags':[]}]}
  self.put(self.a,'search/search_index.json',json.dumps(baseline))
  self.put(self.b,'search.json',json.dumps(candidate))
  result=search_parity(self.a,self.b,{'erdos/index.html','oai26/index.html'})
  self.assertTrue(result['search_parity_proven'])
  self.assertTrue(result['cross_engine_index_schema_different'])
  self.assertEqual(result['baseline_indexed_page_routes'],2)
 def test_missing_candidate_search_index_or_canonical_page_not_certified(self):
  self.put(self.a,'search/search_index.json',json.dumps({'docs':[{'location':'oai26/','title':'OAI'}]}))
  self.assertFalse(search_parity(self.a,self.b)['search_parity_proven'])
  self.put(self.b,'search.json',json.dumps({'items':[{'location':'index.html','title':'Home'}]}))
  self.assertEqual(search_parity(self.a,self.b)['missing_indexed_locations_count'],1)
 def test_unknown_search_schema_is_inconclusive(self):
  self.put(self.a,'search/search_index.json','{}')
  self.put(self.b,'search.json','{}')
  self.assertFalse(search_parity(self.a,self.b)['search_parity_proven'])
 def test_page_route_normalization(self):
  self.assertEqual(canonical_search_route('https://grandchallenge.ai/MATH-PROGRAMME/erdos/'), 'erdos/index.html')
  self.assertEqual(canonical_search_route('erdos/#heading'), 'erdos/index.html')
  self.assertEqual(canonical_search_route(''), 'index.html')
  self.assertEqual(canonical_search_route('docs/logo.svg'), None)
if __name__=='__main__':unittest.main()
