#!/usr/bin/env python3
"""Bounded, authenticated live workflow audit for frozen GCL-PAAR-001 estate.

Distinguishes real GitHub PR/check/review events from scientific correctness,
public-page equivalence, and tests that merely exist in the source tree.
"""
from __future__ import annotations
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SHA40=re.compile(r'[a-f0-9]{40}\Z')
SCHEMA='GCL_PAAR_001_ESTATE_LIFECYCLE_READBACK/1'

def need(ok,reason):
    if not ok:raise ValueError(reason)

def gh(url):
    proc=subprocess.run(['gh','api',url],capture_output=True,text=True,timeout=35)
    if proc.returncode:
        raise ValueError(f'authenticated GitHub API failed ({url}): {proc.stderr[:180]}')
    return json.loads(proc.stdout)

def gh_optional(url):
    proc=subprocess.run(['gh','api',url],capture_output=True,text=True,timeout=35)
    return json.loads(proc.stdout) if proc.returncode==0 else None

def effective_rules(repo,branch):
    rules=gh(f'repos/{repo}/rules/branches/{branch}')
    need(isinstance(rules,list),'missing effective branch rules')
    base=gh(f'repos/{repo}/branches/{branch}')
    need(base.get('protected') is True,'effective branch not protected: '+repo)
    approvals=0
    required=[]
    types={x['type'] for x in rules}
    if not rules:
        legacy=gh(f'repos/{repo}/branches/{branch}/protection')
        need(isinstance(legacy,dict),'no legacy protection')
        rr=legacy.get('required_pull_request_reviews')
        if isinstance(rr,dict):
            approvals=rr.get('required_approving_review_count',0)
            types.add('pull_request')
        sc=legacy.get('required_status_checks')
        if isinstance(sc,dict):
            required=sc.get('contexts',[]) or []
            types.add('required_status_checks')
    else:
        for item in rules:
            prm=item.get('parameters') or {}
            if item['type']=='pull_request':
                approvals=max(approvals,prm.get('required_approving_review_count',0))
            if item['type']=='required_status_checks':
                required += [x['context'] for x in prm.get('required_status_checks',[])]
    need('pull_request' in types,'no protected PR workflow: '+repo)
    need(type(approvals) is int and approvals>=0,'invalid reviewer requirement')
    return {'protected':True,'types':sorted(types),
            'required_approving_review_count':approvals,
            'required_status_contexts':sorted(set(required)),
            'head_sha':base['commit']['sha']}

def resolve_recent_merged_pr(repo,branch):
    events=gh(f'repos/{repo}/pulls?state=closed&per_page=100&sort=updated&direction=desc')
    need(isinstance(events,list),'invalid GitHub pull request collection')
    merged=[x for x in events if x.get('merged_at') and (x.get('base') or {}).get('ref')==branch]
    need(bool(merged),'no merged PR in latest 100 closed events: '+repo)
    return max(merged,key=lambda x:x['merged_at'])

def selected_review(reviews,subject):
    author=(subject.get('user') or {}).get('login')
    head=(subject.get('head') or {}).get('sha')
    need(bool(author) and bool(SHA40.fullmatch(head or '')),'PR actor/head unavailable')
    latest={}
    for rev in sorted(reviews,key=lambda r:(r.get('submitted_at') or '',r.get('id') or 0)):
        user=(rev.get('user') or {}).get('login')
        if user and user!=author:latest[user]=rev
    matching=[r for r in latest.values()
              if r.get('state')=='APPROVED' and r.get('commit_id')==head]
    return sorted([{'login':r['user']['login'],'id':r['id'],'commit_id':r['commit_id']}
                   for r in matching],key=lambda r:r['login'])

def get_run(repo,sha):
    obj=gh(f'repos/{repo}/commits/{sha}/check-runs?per_page=100')
    need(isinstance(obj,dict) and isinstance(obj.get('check_runs'),list),
         'invalid checks response')
    need(obj.get('total_count',101)<=100,
         'check enumeration truncated; cannot assert completeness')
    return [{'id':x['id'],'name':x['name'],
             'conclusion':x.get('conclusion'),'status':x.get('status'),
             'app':(x.get('app') or {}).get('slug')}
            for x in obj['check_runs']]

def one(repo,branch,source):
    branch_data=effective_rules(repo,branch)
    pr=resolve_recent_merged_pr(repo,branch)
    head=pr['head']['sha']
    merge_sha=pr.get('merge_commit_sha')
    need(bool(SHA40.fullmatch(head or '')) and
         bool(SHA40.fullmatch(merge_sha or '')) and
         bool(pr.get('merged_at')),'merged PR missing original identity')
    reviews=gh(f'repos/{repo}/pulls/{pr["number"]}/reviews?per_page=100')
    need(isinstance(reviews,list) and len(reviews)<100,
         'review enumeration truncated')
    native=selected_review(reviews,pr)
    checks=get_run(repo,head)
    successful={x['name'] for x in checks if x['conclusion']=='success'}
    required=branch_data['required_status_contexts']
    review_status=('EXACT_HEAD_NONAUTHOR_APPROVED' if native else
                   'NO_EXACT_HEAD_NONAUTHOR_APPROVAL')
    required_review=('NO_NATIVE_APPROVAL_REQUIRED_BY_CURRENT_RULE' if branch_data['required_approving_review_count']==0 else
                    'PASS_EXACT_HEAD_NONAUTHOR_APPROVAL' if len(native)>=branch_data['required_approving_review_count']
                    else 'UNVERIFIED_HISTORIC_PR_UNDER_CURRENT_RULES')
    req_success=sorted(set(required) & successful)
    missing=sorted(set(required)-successful)
    checks_status=('CHECK_RUN_SUCCESS_OBSERVED' if successful
                   else 'NO_SUCCESSFUL_PR_HEAD_CHECK_OBSERVED')
    pages=gh_optional(f'repos/{repo}/pages')
    publication={'category':'GITHUB_PAGES_CONFIGURED' if isinstance(pages,dict) else
                          'GITHUB_PAGES_NOT_CONFIGURED',
                 'url':pages.get('html_url') if isinstance(pages,dict) else None,
                 'https_enforced':pages.get('https_enforced') if isinstance(pages,dict) else None,
                 'live_document_content_verified':False,
                 'source_to_mirror_equivalence':'NOT_VERIFIED'}
    record={
      'repository':repo,'assertion_class':source,
      'current_default_branch':branch_data,
      'recent_protected_candidate':{
         'pr_number':pr['number'],'pr_url':pr['html_url'],
         'head_sha':head,'merge_commit_sha':merge_sha,
         'merged_at':pr['merged_at'],'base_branch':pr['base']['ref'],
         'author':pr['user']['login'],'authenticated_merged_pr':True},
      'authentic_native_reviews':native,
      'nonauthor_exact_head_review_status':review_status,
      'current_review_requirement_assessment':required_review,
      'observed_github_check_runs':checks,
      'check_summary':{'positive_count':len(successful),
                       'status':checks_status,
                       'required_contexts_matching_successful_pr_head':req_success,
                       'current_required_contexts_absent_from_old_pr_head':missing,
                       'required_checks_passed_at_admission':'NOT_DETERMINED_FOR_HISTORICAL_PR'},
      'publication':publication,
      'admission_state':'AUTHENTICATED_MERGED_PR_OBSERVED',
      'failure_lifecycle_state':'NOT_OBSERVED_IN_THIS_MERGED_PR_SAMPLE',
      'semantic_assertion_certified':False}
    if repo=='grandchallenge/GCT-EXECUTIVE':
        record['private_metadata_redacted']=True
        record['recent_protected_candidate']['pr_url']=None
        record['recent_protected_candidate']['author']=None
        record['observed_github_check_runs']=[]
        record['authentic_native_reviews']=[]
        record['sensitive_raw_check_evidence']='PRIVATE_REPOSITORY_AUTHENTICATED_READBACK_NOT_PUBLISHED'
    return record

def verify_report(report,scope,classes):
    need(report.get('record_type')==SCHEMA,'report schema changed')
    need(report.get('scope_sha256')==hashlib.sha256(scope).hexdigest(),
         'frozen population digest drift')
    pinned=json.loads(scope)
    universe={r['repository'] for r in pinned['repositories']}
    entries=report.get('repositories')
    need(isinstance(entries,list) and len(entries)==len(universe)==20,
         'missing estate repository')
    need({e['repository'] for e in entries}==universe,'repo population drift')
    need(len({e['repository'] for e in entries})==20,'duplicate repository')
    for item in entries:
        branch=item['current_default_branch']
        need(branch['protected'] is True and 'pull_request' in branch['types'],
             'missing protected PR control')
        pr=item['recent_protected_candidate']
        need(pr.get('authenticated_merged_pr') is True
             and pr['base_branch']=='main'
             and SHA40.fullmatch(pr['head_sha'])
             and SHA40.fullmatch(pr['merge_commit_sha'])
             and bool(pr.get('merged_at')),'unverified lifecycle success')
        need(item['semantic_assertion_certified'] is False,
             'unsupported semantic certification')
        need(item['admission_state']=='AUTHENTICATED_MERGED_PR_OBSERVED',
             'unsupported authority promotion')
        need(item['publication']['source_to_mirror_equivalence']=='NOT_VERIFIED',
             'unsupported mirror claim')
        need(item['assertion_class']==classes[item['repository']],
             'scope classification drift')
        need(item['failure_lifecycle_state']=='NOT_OBSERVED_IN_THIS_MERGED_PR_SAMPLE',
             'unsupported failure path claim')
    need(report.get('estate_wide_integrity_certified') is False,
         'unauthorized global certification')
    return {'positive_merged_pr_samples':len(entries),
            'semantic_enforcement_certified':False,
            'mirror_equivalence_verified':False}

def main():
    scope_file=ROOT/'ESTATE_SCOPE_20261017.json'
    scope=scope_file.read_bytes()
    mapping=json.loads((ROOT/'ESTATE_CONTROL_MAPPING_14_20261017.json').read_text())
    source={r['repository']:r['assertion_class'] for r in mapping['entries']}
    source.update({
      'grandchallenge/CONTROL':'GCL_CONTROL_AND_PROJECT_ADMISSION',
      'grandchallenge/MATH-PROGRAMME':'SOURCE_PROOF_AND_PUBLICATION',
      'grandchallenge/MATHSOLVE':'MATHEMATICAL_SOLUTION_CLAIM',
      'grandchallenge/MATHCERT':'PROOF_CERTIFICATION_AND_REVIEW',
      'grandchallenge/INTELLECT':'SPECIALIST_REVIEW_AND_INDEPENDENT_ADMISSION',
      'grandchallenge/MATHFORGE':'MATHEMATICAL_PRODUCTION_EXECUTION'})
    pinned=json.loads(scope)
    rows=[]
    for item in pinned['repositories']:
        repo=item['repository']
        row=one(repo,item['default_branch'],source[repo])
        rows.append(row)
        print(f'{repo}: PR #{row["recent_protected_candidate"]["pr_number"]}, '
              f'green={row["check_summary"]["positive_count"]}, '
              f'approval={row["nonauthor_exact_head_review_status"]}',flush=True)
    result={'record_type':SCHEMA,
      'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'scope_sha256':hashlib.sha256(scope).hexdigest(),
      'repo_count':20,'repositories':rows,
      'observed_protected_merge_samples':len(rows),
      'observed_pr_head_successful_ci':sum(
          r['check_summary']['positive_count']>0 for r in rows),
      'native_nonauthor_exact_head_approved_samples':sum(
          bool(r['authentic_native_reviews']) for r in rows),
      'pages_configured':sum(
          r['publication']['category']=='GITHUB_PAGES_CONFIGURED' for r in rows),
      'failure_path_end_to_end_verified':False,
      'public_mirror_semantics_verified':False,
      'estate_wide_integrity_certified':False,
      'limitation':'Historical PR samples prove bounded protected merges; current gate settings may postdate those merges. No negative-path or live document mirror identity is inferred.'}
    verify_report(result,scope,source)
    out=ROOT/'ESTATE_LIFECYCLE_READBACK_20261017.json'
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':'PASS_TWENTY_AUTHENTIC_MERGED_PR_SAMPLES',
                      'positive_ci':result['observed_pr_head_successful_ci'],
                      'nonauthor_reviews':result['native_nonauthor_exact_head_approved_samples'],
                      'pages_configured':result['pages_configured'],
                      'source_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
                      'estate_wide_certified':False},sort_keys=True))

if __name__=='__main__':main()
