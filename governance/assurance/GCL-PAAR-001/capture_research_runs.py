"""Exact-head GitHub Actions run readback for three research repositories."""
import json,subprocess,datetime
from pathlib import Path
P=Path(__file__).parent
scope=json.loads((P/'ESTATE_SCOPE_20261017.json').read_text())
ids={'ADAPTIVE-INTELLIGENCE-ATLAS':39008087687,'COMPUTATIONAL-DIFFICULTY-ATLAS':39020937362,'GSD':37856762182}
def api(p):
 return json.loads(subprocess.run(['gh','api',p],capture_output=True,text=True,check=True,timeout=25).stdout)
rows=[]
for e in scope['repositories']:
 n=e['repository'].split('/')[-1]
 if n not in ids:continue
 repo=e['repository'];rid=ids[n]
 run=api(f'repos/{repo}/actions/runs/{rid}')
 jobs=api(f'repos/{repo}/actions/runs/{rid}/jobs?per_page=100')
 assert run['head_sha']==e['head_sha']
 assert run['conclusion']=='success'
 assert jobs['total_count']>0
 rows.append({'repository':repo,'head':e['head_sha'],'run_id':rid,'run_attempt':run['run_attempt'],'name':run['name'],'event':run['event'],'conclusion':run['conclusion'],'created_at':run['created_at'],'jobs':[{'id':j['id'],'name':j['name'],'conclusion':j['conclusion'],'steps':[{'name':s['name'],'conclusion':s['conclusion']} for s in j['steps']]} for j in jobs['jobs']],'semantic_admission_verified':False})
assert len(rows)==3
(P/'RESEARCH_RUN_WITNESSES_20261017.json').write_text(json.dumps({'record_type':'GCL_PAAR_RESEARCH_RUN_WITNESS/1','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':rows,'branch_protection_remediated':False},sort_keys=True,indent=2)+'\n')
print('PINNED_ACTIONS_RUNS',len(rows))
