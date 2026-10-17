#!/usr/bin/env python3
"""Read-only authenticated enumeration of current GCL organization repo scope.

No inference from branch protection to semantic assertion integrity.
"""
import argparse
import datetime
import hashlib
import json
import subprocess
from pathlib import Path

ORG='grandchallenge'
ORIGINAL={'CONTROL','MATH-PROGRAMME','MATHSOLVE','MATHCERT','INTELLECT','MATHFORGE'}

def api(path):
    p=subprocess.run(['gh','api',path],capture_output=True,text=True,check=True,timeout=30)
    return json.loads(p.stdout)

def capture():
    pages=[]
    index=1
    while True:
        items=api(f'orgs/{ORG}/repos?per_page=100&type=all&page={index}')
        if not isinstance(items,list):raise ValueError('not a GitHub repo collection')
        pages.extend(items)
        if len(items)<100:break
        index+=1
        if index>20:raise ValueError('unexpectedly large org; enumerate explicitly')
    found=[]
    seen=set()
    for row in sorted(pages,key=lambda x:x['name'].casefold()):
        name=row['name'];branch=row['default_branch']
        if name in seen:raise ValueError('duplicate org repository')
        seen.add(name)
        if row['archived'] or row['disabled']:
            status='EXCLUDED_INACTIVE'
        else:
            status='IN_SCOPE'
        b=api(f'repos/{ORG}/{name}/branches/{branch}')
        sha=(b.get('commit') or {}).get('sha')
        if not isinstance(sha,str) or len(sha)!=40:
            raise ValueError('cannot establish immutable head for '+name)
        found.append({'repository':f'{ORG}/{name}', 'default_branch':branch,
          'protected':b.get('protected') is True,'head_sha':sha,
          'visibility':row['visibility'], 'archived':bool(row['archived']),
          'disabled':bool(row['disabled']),'scope':status,
          'prior_six_repo_control_sample':name in ORIGINAL,
          'assurance_control_mapping':'PARTIAL_SAMPLED' if name in ORIGINAL else 'NOT_YET_VERIFIED',
          'cross_repository_lifecycle_replay':'NOT_YET_VERIFIED',
          'scientific_claim_certification':'NOT_ASSESSED_BY_THIS_SNAPSHOT'})
    return {'record_type':'GCL_PAAR_001_ESTATE_SCOPE_SNAPSHOT/1',
      'captured_utc':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
      'source':'AUTHENTICATED_GITHUB_ORG_REPOSITORY_LIST_AND_BRANCH_API',
      'scope':'GITHUB_REPOSITORY_BOUNDARY_ONLY_NOT_EXTERNAL_RUNTIME_OR_PUBLIC_SITE_INVENTORY',
      'repositories':found,
      'active_count':sum(x['scope']=='IN_SCOPE' for x in found),
      'original_sample_count':sum(x['prior_six_repo_control_sample'] for x in found),
      'unverified_mapping_count':sum(x['assurance_control_mapping']=='NOT_YET_VERIFIED' for x in found),
      'global_integrity_certified':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path)
    args=p.parse_args();v=capture()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(v,indent=2,sort_keys=True)+'\n').encode()
    args.output.write_bytes(raw)
    print(json.dumps({'output':str(args.output),'active_count':v['active_count'],
      'sampled':v['original_sample_count'],'unverified':v['unverified_mapping_count'],
      'sha256':hashlib.sha256(raw).hexdigest(),
      'unprotected_default_branches':[i['repository'] for i in v['repositories']
        if i['scope']=='IN_SCOPE' and not i['protected']]},sort_keys=True))

if __name__=='__main__':main()
