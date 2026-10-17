#!/usr/bin/env python3
"""Read-only actual CI failure and protected-commit Pages deployment binding."""
import datetime,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def gh(path):
 p=subprocess.run(['gh','api',path],capture_output=True,text=True,timeout=30)
 if p.returncode:raise ValueError(path+': '+p.stderr[:180])
 return json.loads(p.stdout)

def main():
 prior=(ROOT/'ESTATE_NEGATIVE_AND_PUBLIC_20261017.json').read_bytes()
 src=json.loads(prior);closed=[]
 for case in src['negative_samples']:
  repo=case['repository'];head=case.get('pr_head_sha')
  if not head:
   closed.append({'repository':repo,'check_status':'PRIVATE_DETAILS_REDACTED' if case.get('private_metadata_redacted') else 'NO_CLOSED_UNMERGED_PR','failed_check_runs':[],'causal_rejection_certified':False});continue
  checks=[]
  for page in range(1,11):
   runs=gh(f'repos/{repo}/commits/{head}/check-runs?per_page=100&page={page}')
   checks.extend(runs['check_runs'])
   if len(checks)>=runs['total_count']:break
  if len(checks)!=runs['total_count']:
   raise ValueError('incomplete paged CI checks '+repo)
  failed=[{'id':r['id'],'name':r['name'],'conclusion':r['conclusion']} for r in checks if r.get('conclusion')=='failure']
  closed.append({'repository':repo,'pr_number':case['sample_pr_number'],
    'pr_head_sha':head,'check_status':'FAILED_HEAD_CHECKS_OBSERVED' if failed else 'NO_FAILED_HEAD_CHECK_IN_SAMPLE',
    'failed_check_runs':failed,'causal_rejection_certified':False})
  print(repo, 'failed',len(failed),flush=True)
 deploy=[]
 for public in src['pages']:
  repo=public['repository']
  items=gh(f'repos/{repo}/deployments?environment=github-pages&per_page=15')
  if not items:raise ValueError('no deployed Pages artifact for '+repo)
  chosen=None
  for item in items:
   statuses=gh(f'repos/{repo}/deployments/{item["id"]}/statuses?per_page=10')
   if statuses and statuses[0]['state']=='success':
    chosen=(item,statuses[0]);break
  if not chosen:raise ValueError('no successfully completed deployment for '+repo)
  item,status=chosen
  branch=gh(f'repos/{repo}/branches/main')
  current=branch['commit']['sha']
  sha=item['sha']
  if sha!=current:
   compare=gh(f'repos/{repo}/compare/{sha}...{current}')
   if not (compare['status']=='ahead' and compare['behind_by']==0
           and compare['merge_base_commit']['sha']==sha):
    raise ValueError('public deployment source not protected ancestor '+repo)
  if not (branch['protected'] is True and public['https_transport_readback']=='PASS'
          and status.get('environment_url')==public['configured_url']):
   raise ValueError('public deployment binding drift '+repo)
  deploy.append({'repository':repo,'deployment_id':item['id'],'protected_source_sha':sha,
    'current_protected_head':current,'source_is_protected_ancestor':True,
    'authenticated_deployment_status':'success','deployment_status_url':status['log_url'],
    'public_url':status['environment_url'],'https_transport':'PASS',
    'rendered_document_equivalent_to_accepted_source':False})
 output={'record_type':'GCL_PAAR_001_FAILED_CHECK_AND_PAGES_DEPLOYMENT/1',
   'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
   'prior_negative_snapshot_sha256':hashlib.sha256(prior).hexdigest(),
   'negative_cases':closed,'pages_deployments':deploy,
   'failed_check_candidate_count':sum(bool(x['failed_check_runs']) for x in closed),
   'successful_source_anchored_page_deployments':len(deploy),
   'rejection_causality_certified':False,'document_parity_certified':False,
   'gcl_wide_assurance_certified':False}
 path=ROOT/'ESTATE_ADVERSE_DEPLOYMENTS_20261017.json'
 path.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'failed_candidate_count':output['failed_check_candidate_count'],
  'source_anchored_successful_public_deployments':len(deploy),'global_certified':False}))
if __name__=='__main__':main()
