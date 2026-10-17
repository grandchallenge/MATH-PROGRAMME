#!/usr/bin/env python3
"""Authenticated, fail-closed positive live verification of one accepted Erdős article.

Run only from checked-out, current protected main after a successful Pages build.
This does not accept an article, change the ledger, or certify mathematics.
"""
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,sys,urllib.request
from pathlib import Path
from erdos_accepted_publication_parity import compare_accepted_article,assert_rendered_math

REPOSITORY='grandchallenge/MATH-PROGRAMME'
def _cmd(*parts):
 p=subprocess.run(parts,capture_output=True,text=True,timeout=30)
 if p.returncode:raise RuntimeError('AUTHENTICATED_SOURCE_UNAVAILABLE')
 return p.stdout.strip()
def _api(url):return json.loads(_cmd('gh','api',url))
def verify_live(problem_id: int,root:Path)->dict:
 root=Path(root).resolve();source_commit=_cmd('git','-C',str(root),'rev-parse','HEAD')
 if not re.fullmatch('[0-9a-f]{40}',source_commit):raise ValueError('SOURCE_SHA_INVALID')
 branch=_api('repos/'+REPOSITORY+'/branches/main')
 if branch['protected'] is not True or branch['commit']['sha']!=source_commit:
  raise ValueError('PROTECTED_MAIN_NOT_CURRENT')
 deps=_api('repos/'+REPOSITORY+'/deployments?environment=github-pages&per_page=10')
 if not deps or deps[0]['sha']!=source_commit:raise ValueError('PAGES_DEPLOYMENT_STALE')
 statuses=_api('repos/'+REPOSITORY+'/deployments/'+str(deps[0]['id'])+'/statuses?per_page=2')
 if not statuses or statuses[0]['state']!='success':raise ValueError('PAGES_DEPLOYMENT_NOT_SUCCESSFUL')
 sys.path.insert(0,str(root/'ci'))
 from erdos_compendium import load_batch_admissions,manuscript
 admission=load_batch_admissions().get(problem_id)
 source=manuscript(problem_id)
 if admission is None or source is None:raise ValueError('ARTICLE_NOT_ACCEPTED')
 url=f'https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/{problem_id:04d}/'
 req=urllib.request.Request(url,headers={'User-Agent':'GCL-PAAR-001-accepted-parity/1'})
 with urllib.request.urlopen(req,timeout=25) as resp:
  if resp.status!=200 or resp.geturl()!=url:raise ValueError('PUBLIC_URL_REDIRECT_OR_ERROR')
  page=resp.read(2_500_001)
 if len(page)>2_500_000:raise ValueError('PUBLIC_HTML_TOO_LARGE')
 record=compare_accepted_article(problem_id=problem_id,source=source,admission=admission,
     public_html=page,public_url=url,source_commit=source_commit,deploy_commit=deps[0]['sha'])
 from playwright.sync_api import sync_playwright
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True)
  try:render=assert_rendered_math(browser,url,record['verified_math_expressions'])
  finally:browser.close()
 record.update(render)
 record['verified_pages_deployment_id']=deps[0]['id']
 record['record_authority']='AUTHENTICATED_GITHUB_PROTECTED_MAIN_PAGES_AND_LIVE_BROWSER'
 record['theorem_certified']=False
 return record

def main():
 a=argparse.ArgumentParser()
 a.add_argument('--problem-id',type=int,required=True)
 a.add_argument('--repository-root',type=Path,required=True)
 a.add_argument('--output',type=Path,required=True)
 args=a.parse_args();result=verify_live(args.problem_id,args.repository_root)
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
 print(result['status'],result['problem_id'],result['verified_math_expressions'])
if __name__=='__main__':main()
