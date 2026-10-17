"""Read-only authenticated Git tree inventory; paths are not enforcement proof."""
import json,subprocess,sys,hashlib,datetime
from pathlib import Path
root=Path(__file__).parent
scope=json.loads((root/'ESTATE_SCOPE_20261017.json').read_text())
records=[]
for item in scope['repositories']:
 repo=item['repository']; head=item['head_sha']
 response=subprocess.run(['gh','api',f'repos/{repo}/git/trees/{head}?recursive=1'],capture_output=True,text=True,timeout=45)
 if response.returncode:
  records.append({'repository':repo,'head':head,'tree_status':'UNAVAILABLE','reason':response.stderr[:250]})
  continue
 data=json.loads(response.stdout)
 blobs=[v for v in data.get('tree',[]) if v.get('type')=='blob']
 paths=sorted(v['path'] for v in blobs)
 categories={key:sum(p.startswith(prefix) for p in paths) for key,prefix in {
  'ci':'ci/','governance':'governance/','workflows':'.github/workflows/',
  'tests':'tests/','public_docs':'docs/','research':'mathematics/'}.items()}
 records.append({'repository':repo,'head':head,'tree_status':'TRUNCATED' if data.get('truncated') else 'COMPLETE',
  'file_count':len(paths),'paths_sha256':hashlib.sha256(json.dumps(paths).encode()).hexdigest(),
  'categories':categories,'semantic_enforcement':'UNVERIFIED'})
result={'record_type':'GCL_PAAR_ESTATE_CONTROL_SURFACES/1',
 'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope_file_sha256':hashlib.sha256((root/'ESTATE_SCOPE_20261017.json').read_bytes()).hexdigest(),
 'sources':records,'semantic_assurance_certified':False}
(root/'ESTATE_SURFACES_20261017.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'repos':len(records),'complete':sum(x['tree_status']=='COMPLETE' for x in records),
 'exceptions':[x['repository'] for x in records if x['tree_status']!='COMPLETE'],
 'no_governance':[x['repository'] for x in records if x.get('categories',{}).get('governance')==0]},sort_keys=True))
