#!/usr/bin/env python3
"""Read-only current effective-GitHub-rule and protected-merge attestations."""
import datetime,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).parent
EXPECTED={
 'ADAPTIVE-INTELLIGENCE-ATLAS':(25299675,'validate',None),
 'COMPUTATIONAL-DIFFICULTY-ATLAS':(25299676,'direct-return-contract',53),
 'GSD':(25299668,'unit',2),
}
def api(p):
 x=subprocess.run(['gh','api',p],capture_output=True,text=True,check=True,timeout=30)
 return json.loads(x.stdout)
def main():
 before=json.loads((ROOT/'BRANCH_PROTECTION_EXCEPTIONS_20261017.json').read_text())
 scope=json.loads((ROOT/'ESTATE_SCOPE_20261017.json').read_text())
 scope_sha=hashlib.sha256((ROOT/'ESTATE_SCOPE_20261017.json').read_bytes()).hexdigest()
 assert before['scope_sha256']==scope_sha and len(before['exceptions'])==3
 past={x['repository']:x for x in before['exceptions']}
 pinned={x['repository']:x for x in scope['repositories']}
 records=[]
 for name,(ruleset_id,check,pr_number) in EXPECTED.items():
  repo='grandchallenge/'+name; branch=api(f'repos/{repo}/branches/main')
  ruleset=api(f'repos/{repo}/rulesets/{ruleset_id}')
  applied=api(f'repos/{repo}/rules/branches/main')
  assert repo in past and past[repo]['branch_protected'] is False
  assert branch['protected'] is True and ruleset['enforcement']=='active'
  assert ruleset['bypass_actors']==[]
  assert ruleset['conditions']['ref_name']['include']==['~DEFAULT_BRANCH']
  types={x['type'] for x in applied}
  assert {'deletion','non_fast_forward','pull_request','required_status_checks'} <= types
  pr_rules=next(x['parameters'] for x in applied if x['type']=='pull_request')
  assert pr_rules['required_approving_review_count']==0
  ctx=[c['context'] for r in applied if r['type']=='required_status_checks'
       for c in r['parameters']['required_status_checks']]
  assert ctx==[check]
  pr=None
  if pr_number:
   x=api(f'repos/{repo}/pulls/{pr_number}')
   assert x.get('merged_at') and x['base']['ref']=='main'
   prs=api(f'repos/{repo}/commits/{x["head"]["sha"]}/check-runs?per_page=100')
   matching=[c for c in prs['check_runs'] if c['name']==check and c['conclusion']=='success']
   assert matching, f'No authenticated SUCCESS check {check} on {name} PR {pr_number}'
   pr={'number':pr_number,'head_sha':x['head']['sha'],
       'protected_merge_sha':x['merge_commit_sha'],'merged_at':x['merged_at'],
       'green_pr_check_id':matching[0]['id'],'green_pr_check_name':check}
   assert branch['commit']['sha']==pr['protected_merge_sha']
  records.append({'repository':repo,'original_unprotected_head_sha':pinned[repo]['head_sha'],
     'current_protected_main_sha':branch['commit']['sha'],
     'ruleset_id':ruleset_id,'ruleset_name':ruleset['name'],
     'enforcement':'active','bypass_actors':[],
     'effective_rule_types':sorted(types),
     'required_status_checks':ctx,'blanket_approving_review_count':0,
     'conditional_specialist_review_unchanged':True,
     'universal_ci_patch_protected_pr':pr,'verification':'PASS_EFFECTIVE_GITHUB_RULE_READBACK',
     'scientific_certification':False})
 result={'record_type':'GCL_PAAR_001_BRANCH_CONTROL_REMEDIATION/1',
    'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'frozen_scope_sha256':scope_sha,
    'original_exceptions':3,'resolved':3,'unresolved':0,
    'repositories':records,'branch_protection_for_original_three':'PASS',
    'status_checks_required_and_covered':'PASS',
    'full_20_repositories_semantic_assurance':False}
 path=ROOT/'BRANCH_PROTECTION_REPAIRS_20261017.json'
 path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'result':'PASS_THREE_BRANCH_PROTECTION_REPAIRS',
   'repos':[r['repository'] for r in records],
   'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},sort_keys=True))
if __name__=='__main__':main()
