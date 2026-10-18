"""Read-only exact-commit source mapping for remaining PAAR repositories."""
import base64,hashlib,json,subprocess,datetime,sys
from pathlib import Path
import yaml
P=Path(__file__).parent
S=P/'ESTATE_SCOPE_20261017.json'
def api(p):
 r=subprocess.run(['gh','api',p],capture_output=True,text=True,timeout=35,check=True)
 return json.loads(r.stdout)
def blob(repo,sha):
 x=api(f'repos/{repo}/git/blobs/{sha}')
 b=base64.b64decode(x['content'])
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==sha
 return b
out=[]
all_items=[e for e in json.loads(S.read_text())['repositories'] if not e['prior_six_repo_control_sample']]
start=int(sys.argv[1]) if len(sys.argv)>1 else 0
end=int(sys.argv[2]) if len(sys.argv)>2 else 14
for e in all_items[start:end]:
 repo=e['repository'];head=e['head_sha']
 t=api(f'repos/{repo}/git/trees/{head}?recursive=1')
 assert not t['truncated']
 f={v['path']:v['sha'] for v in t['tree'] if v['type']=='blob'}
 w=sorted((p for p in f if p.startswith('.github/workflows/') and p.endswith(('.yml','.yaml'))),key=lambda p:(0 if any(k in p for k in ('validate','ops-check','ci.yml','conformance','review-tests')) else 1 if any(k in p for k in ('review-admission','direct-editorial','return-replay','routing-enforcement')) else 2,p))
 g=sorted(p for p in f if p.startswith('governance/'))
 tests=sorted(p for p in f if p.startswith('tests/'))
 private=e['visibility']=='private'
 item={'repository':repo,'head':head,'private':private,'counts':{'workflows':len(w),'governance':len(g),'tests':len(tests)},'status':'PINNED_SOURCE_ONLY_NOT_ENFORCEMENT'}
 if not private:
  item['governance_sources']=[{'path':p,'blob':f[p]} for p in g[:8]]
  item['test_sources']=[{'path':p,'blob':f[p]} for p in tests[:5]]
  wf=[]
  for p in w[:4]:
   b=blob(repo,f[p]);d=yaml.load(b.decode(),Loader=yaml.BaseLoader) or {}
   jobs=d.get('jobs') or {}
   commands=[{'job':jid,'command':str(s['run'])[:350]} for jid,j in jobs.items() if isinstance(j,dict) for s in j.get('steps',[]) if isinstance(s,dict) and 'run' in s]
   wf.append({'path':p,'blob':f[p],'events':d.get('on'),'job_ids':list(jobs),'commands':commands[:12],'command_count':len(commands)})
  item['workflows']=wf
 out.append(item)
assert len(out)==end-start
r={'record_type':'GCL_PAAR_PINNED_SOURCE_MAP/1','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'entries':out,'source_count':len(out),'semantic_assurance':False}
(P/f'ESTATE_CONTRACT_SOURCES_{start}_{end}.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
print(json.dumps({'mapped':len(out),'private':sum(e['private'] for e in out),'workflow_samples':sum(len(e.get('workflows',[])) for e in out)}))
