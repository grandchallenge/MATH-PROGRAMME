"""Read-only effective rules and protection observations for three research repos."""
import datetime,hashlib,json,subprocess
from pathlib import Path
P=Path(__file__).parent
scope=json.loads((P/'ESTATE_SCOPE_20261017.json').read_text())
subjects={'ADAPTIVE-INTELLIGENCE-ATLAS','COMPUTATIONAL-DIFFICULTY-ATLAS','GSD'}
def api(endpoint):
 p=subprocess.run(['gh','api',endpoint],capture_output=True,text=True,timeout=25)
 return {'exit_code':p.returncode,'response':json.loads(p.stdout) if p.stdout.strip().startswith(('[','{')) else {},'stderr_class':'NOT_FOUND' if '404' in p.stderr else 'OK' if p.returncode==0 else 'ERROR'}
rows=[]
for e in scope['repositories']:
 if e['repository'].split('/')[-1] not in subjects:continue
 repo=e['repository'];b=e['default_branch']
 branch=api(f'repos/{repo}/branches/{b}')
 rules=api(f'repos/{repo}/rules/branches/{b}')
 protection=api(f'repos/{repo}/branches/{b}/protection')
 assert branch['exit_code']==rules['exit_code']==0
 assert branch['response']['commit']['sha']==e['head_sha']
 assert branch['response']['protected'] is False
 assert rules['response']==[]
 assert protection['response'].get('status')=='404'
 rows.append({'repository':repo,'pinned_head':e['head_sha'],'branch':b,
   'branch_protected':False,'effective_rules':[],
   'legacy_protection_endpoint_status':404,
   'finding':'NO_EFFECTIVE_GITHUB_DEFAULT_BRANCH_PROTECTION_AT_OBSERVED_HEAD',
   'impact':'GITHUB_DOES_NOT_REQUIRE_PR_REVIEW_OR_STATUS_CHECKS_FOR_DEFAULT_BRANCH_WRITES',
   'scientific_false_admission_observed':False,
   'policy_disposition':'REQUIRES_GOVERNED_REVIEW_NO_UNILATERAL_MUTATION'})
assert len(rows)==3
r={'record_type':'GCL_PAAR_BRANCH_PROTECTION_NEGATIVE_READBACK/1','observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'scope_sha256':hashlib.sha256((P/'ESTATE_SCOPE_20261017.json').read_bytes()).hexdigest(),
   'exceptions':rows,'branch_settings_mutated':False}
(P/'BRANCH_PROTECTION_EXCEPTIONS_20261017.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
print('REPRODUCED_UNPROTECTED_DEFAULT_BRANCHES',len(rows))
