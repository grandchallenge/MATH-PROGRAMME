#!/usr/bin/env python3
"""Post-deploy accepted-article verification and protected-receipt PR handoff.

The CHECK step is read-only; the PUBLISH step opens a normal protected PR.
No temporary Actions artifact, proposed branch or pending PR counts as covered.
"""
from __future__ import annotations
import argparse
import base64
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

from erdos_parity_coverage import plan,apply_receipt,verify_ledger
from erdos_accepted_publication_parity import compare_accepted_article,assert_rendered_math
from erdos_compendium import load_batch_admissions,manuscript

REPO='grandchallenge/MATH-PROGRAMME'
COVERAGE='governance/erdos_compendium/publication_parity/COVERAGE.json'
RECEIPT_DIR='governance/erdos_compendium/publication_parity/receipts/'
DOC='ERDOS_ACCEPTED_PARITY_BATCH_EVIDENCE/1'
SHA=re.compile(r'^[0-9a-f]{40}$')

def refuse(reason):raise ValueError('AUTO_ACCEPTED_PARITY_'+reason)

def cli(*args):
    completed=subprocess.run(args,capture_output=True,text=True,timeout=35)
    if completed.returncode:refuse('COMMAND_FAILED_'+args[0])
    return completed.stdout.strip()

def api(path,data=None,method='POST'):
    command=['gh','api','repos/'+REPO+'/'+path]
    if data is not None:
        import tempfile
        with tempfile.NamedTemporaryFile('w',suffix='.json',delete=False) as fd:
            json.dump(data,fd);filename=fd.name
        command += ['--method',method,'--input',filename]
    try:
        r=subprocess.run(command,capture_output=True,text=True,timeout=40)
        if r.returncode:refuse('GITHUB_API_'+path.split('/')[0]+'_'+r.stderr[:100].replace(' ','_'))
        return json.loads(r.stdout)
    finally:
        if data is not None:os.unlink(filename)

def context(root:Path):
    root=root.resolve()
    deployed=cli('git','-C',str(root),'rev-parse','HEAD')
    if not SHA.fullmatch(deployed):refuse('CHECKOUT_SHA')
    head=api('branches/main')
    if head.get('protected') is not True or head['commit']['sha']!=deployed:refuse('STALE_PROTECTED_HEAD')
    event_sha=os.environ.get('DEPLOYED_SHA')
    if event_sha and event_sha!=deployed:refuse('EVENT_SOURCE_MISMATCH')
    deployments=api('deployments?environment=github-pages&per_page=10')
    if not deployments or deployments[0].get('sha')!=deployed:refuse('STALE_PAGES_DEPLOYMENT')
    sts=api('deployments/'+str(deployments[0]['id'])+'/statuses?per_page=2')
    if not sts or sts[0]['state']!='success':refuse('PAGES_NOT_SUCCESSFUL')
    return deployed,deployments[0]['id']

def check(root:Path,output:Path,run_id:int):
    if type(run_id) is not int or run_id<=0:refuse('RUN_ID')
    root=root.resolve();sha,deployment=context(root)
    ledger=verify_ledger(json.loads((root/COVERAGE).read_text()))
    current=load_batch_admissions()
    candidates,remaining=plan(ledger,current)
    report={'record_type':DOC,'run_id':run_id,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'deployed_source_sha':sha,'pages_deployment_id':deployment,
        'baseline_source_sha':ledger['baseline_protected_sha'],
        'historical_baseline_accepted_unverified':len(ledger['baseline_accepted']),
        'selected_article_ids':candidates,'remaining_after_this_batch':remaining,
        'articles':[], 'mathematical_certification':False,'coverage_until_protected_receipt_merged':False}
    if candidates:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            try:
                for n in candidates:
                    source=manuscript(n)
                    admission=current[n]
                    if source is None:refuse('MISSING_MANUSCRIPT_'+str(n))
                    url=f'https://grandchallenge.github.io/MATH-PROGRAMME/erdos/problems/{n:04d}/'
                    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'GCL-automatic-accepted-parity/1'}),timeout=35) as resp:
                        if resp.status!=200 or resp.geturl()!=url:refuse('PAGE_URL_'+str(n))
                        body=resp.read(2_500_001)
                    if len(body)>2_500_000:refuse('PAGE_TOO_LARGE_'+str(n))
                    item=compare_accepted_article(problem_id=n,source=source,admission=admission,
                        public_html=body,public_url=url,source_commit=sha,deploy_commit=sha)
                    item.update(assert_rendered_math(browser,url,item['verified_math_expressions']))
                    item['pages_deployment_id']=deployment
                    item['theorem_certified']=False
                    report['articles'].append(item)
                    print('PASS_ACCEPTED_SOURCE_AND_MATH',n,item['verified_math_expressions'],flush=True)
            finally:browser.close()
        updated=apply_receipt(ledger,report)
    else:updated=ledger
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    (output.parent/'proposed-coverage.json').write_text(json.dumps(updated,indent=2,sort_keys=True)+'\n')
    print('AUTO_PARITY_VERIFIED_NOT_YET_PROTECTED',len(candidates),'REMAINING',remaining,flush=True)
    return report

def publish(root:Path,output:Path,run_id:int):
    # This function runs only in the trusted, successful check job, using an
    # existing installation token. It does not push or merge protected main.
    root=root.resolve()
    report=json.loads(output.read_text())
    if report.get('run_id')!=run_id or report.get('record_type')!=DOC:refuse('PUBLISH_REPORT_ID')
    if not report.get('articles'):
        print('NO_NEW_OR_AMENDED_ACCEPTED_ARTICLES; NO_RECEIPT_NEEDED',flush=True)
        return
    sha,deployment=context(root)
    if report['deployed_source_sha']!=sha or report['pages_deployment_id']!=deployment:refuse('PUBLISH_STALE_SOURCE')
    ledger=verify_ledger(json.loads((root/COVERAGE).read_text()))
    current=load_batch_admissions()
    selected,_=plan(ledger,current)
    if selected!=report['selected_article_ids'] or selected!=[x['problem_id'] for x in report['articles']]:refuse('PUBLISH_SCOPE_DRIFT')
    for item in report['articles']:
        num=item['problem_id']
        if current[num]['source_sha256']!=item['source_sha256']:refuse('PUBLISH_ACCEPTANCE_DRIFT')
    updated=apply_receipt(ledger,report)
    actual=json.loads((output.parent/'proposed-coverage.json').read_text())
    if updated!=actual:refuse('PUBLISH_LEDGER_TAMPERED')
    prefix=f'editorial/erdos-parity-{sha[:12]}-{run_id}'
    # A GitHub-hosted run creates its own receipt PR, never a protected-main
    # direct push. The PR must pass the ordinary policy and protected queue.
    protected=api('branches/main')
    if not protected.get('protected') or protected['commit']['sha']!=sha:refuse('PUBLISH_HEAD_ADVANCED')
    parent=api('git/commits/'+sha)
    receipt_path=f'{RECEIPT_DIR}{sha[:12]}-{run_id}.json'
    files={COVERAGE:(json.dumps(updated,sort_keys=True,indent=2)+'\n').encode(),
           receipt_path:(json.dumps(report,sort_keys=True,indent=2)+'\n').encode()}
    entries=[]
    for path,data in files.items():
        blob=api('git/blobs',{'content':base64.b64encode(data).decode(),'encoding':'base64'})
        entries.append({'path':path,'mode':'100644','type':'blob','sha':blob['sha']})
    tree=api('git/trees',{'base_tree':parent['tree']['sha'],'tree':entries})['sha']
    commit=api('git/commits',{'message':f'Erdős: protected accepted parity receipt run {run_id} ({len(selected)} articles)',
        'tree':tree,'parents':[sha]})['sha']
    ref=api('git/refs',{'ref':'refs/heads/'+prefix,'sha':commit})
    if ref['object']['sha']!=commit:refuse('PUBLISH_REF_MISMATCH')
    numbers=', '.join('#'+str(n) for n in selected)
    body=(f'Automated GCL post-deployment editorial source-to-HTML verification for {numbers}. '
        f'Source and successful Pages deployment SHA `{sha}`; GitHub-hosted run #{run_id}; '
        f'authenticated deployment {deployment}. All source digests, full section text, TeX and live MathJax nodes passed. '
        f'Protected receipt: `{receipt_path}`. Only the protected merge of this PR will count these articles as covered. '
        'This checks publication fidelity, not mathematical theorem certification. '
        f'{report["remaining_after_this_batch"]} additional changed articles remain for subsequent protected batches.')
    pr=api('pulls',{'title':f'Erdős accepted parity: {len(selected)} deployed articles (run {run_id})',
        'head':prefix,'base':'main','body':body})
    if not pr.get('number') or pr['head']['sha']!=commit:refuse('PUBLISH_PR_MISMATCH')
    print('PROTECTED_RECEIPT_PR_SUBMITTED_NOT_YET_MERGED',pr['html_url'],flush=True)
    # Merge queue submission can be delayed by unrelated checks or rules.
    # Failure to enqueue leaves a visible pending protected PR, NOT coverage.
    merge=subprocess.run(['gh','pr','merge',str(pr['number']),'--repo',REPO,'--merge'],capture_output=True,text=True,timeout=35)
    if merge.returncode:
        print('RECEIPT_PR_REQUIRES_NORMAL_QUEUE_ADMISSION',pr['html_url'],merge.stderr[:250],flush=True)
    else:
        print('PROTECTED_RECEIPT_ENTERED_NORMAL_MERGE_QUEUE',pr['html_url'],flush=True)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--mode',choices=['check','publish'],required=True)
    p.add_argument('--repository-root',type=Path,default=Path('.'))
    p.add_argument('--output',type=Path,default=Path('readback/accepted-parity-batch.json'))
    p.add_argument('--run-id',type=int,required=True)
    args=p.parse_args()
    if args.mode=='check':check(args.repository_root,args.output,args.run_id)
    else:publish(args.repository_root,args.output,args.run_id)
if __name__=='__main__':main()
