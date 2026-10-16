#!/usr/bin/env python3
"""Bounded Council Clerk source-REVISE resolution (3/5); never MathCERT.

Operates only from protected main with existing scoped Council App. Historical
worker custody and review comments are immutable. Dry-run is read-only.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
REPO='grandchallenge/MATH-PROGRAMME'
RESOLUTION='GCL-CRITICAL-SOURCE-RESOLUTION/1'
REVISE='gcl-review:revise'
CORRECTED='gcl-review:source-corrected'
TARGET={2520:11,2521:12,2523:15}
EXCLUDED=(2522,2536)
MERGES={2695:'58c9ca9d68e21bc6c342cb7bef32270e75e32acd',
        2683:'46db216d09fca7e0a90c0333e969f9453c8e572e',
        2681:'1868f750947e48f1d85ae6056e95fe153cca328d'}

class CouncilError(RuntimeError):pass

def execute(*args):
    p=subprocess.run(['gh',*args],capture_output=True,text=True,timeout=50)
    if p.returncode:raise CouncilError('GitHub '+str(args[:3])+': '+p.stderr[:350])
    return p.stdout

def api(path):return json.loads(execute('api',path))

def issue_snapshot(n):
    raw=json.loads(execute('issue','view',str(n),'-R',REPO,'--json','state,labels,projectItems'))
    fields=api(f'repos/{REPO}/issues/{n}/issue-field-values')
    project=[x for x in raw['projectItems'] if x['title']=='GCL Worker Queue']
    states=[(x.get('single_select_option') or {}).get('name') for x in fields
            if x.get('issue_field_name')=='GCL State']
    labels={x['name'] for x in raw['labels']}
    if not (raw['state']=='OPEN' and len(project)==1 and project[0]['status']['name']=='RETURNED'
            and states==['RETURNED']):
        raise CouncilError(f'issue #{n}: historical RETURNED custody or OPEN state drift')
    return {'issue':n,'state':raw['state'],'project':'RETURNED','field':'RETURNED',
            'revise':REVISE in labels,'corrected':CORRECTED in labels}

def comments(n):
    x=api(f'repos/{REPO}/issues/{n}/comments?per_page=100')
    if not isinstance(x,list) or len(x)==100:raise CouncilError('incomplete issue comments')
    return x

def check_evidence():
    import sys
    sys.path.insert(0,str(ROOT/'governance/source_erdos_critical_005'))
    from active_source_lock import LEDGER,ROSTER,verify
    locks=json.loads(LEDGER.read_text());roster=json.loads(ROSTER.read_text())
    accepted=verify(locks,roster)
    if {r['problem_id'] for r in accepted}!={11,12,15}:
        raise CouncilError('source admission scope drift')
    original=json.loads((ROOT/'governance/source_erdos_critical_005/CRITICAL_SOURCE_CORRECTIONS_005.json').read_text())
    byproblem={r['problem_id']:r for r in original['source_corrections']}
    for pr,sha in MERGES.items():
        obj=json.loads(execute('pr','view',str(pr),'-R',REPO,
                               '--json','state,mergeCommit'))
        if obj['state']!='MERGED' or (obj.get('mergeCommit') or {}).get('oid')!=sha:
            raise CouncilError(f'protected source admission #{pr} not exact')
    historical=json.loads((ROOT/'governance/source_erdos_critical_005/PRIMARY_1970_PROPERTY_P_ADJUDICATION.json').read_text())
    if (historical['original_1970_source_semantics_adjudicated'] is not True
            or historical['mathematical_certification_authorized'] is not False):
        raise CouncilError('primary source/adjudication drift')
    results=[]
    for n,problem in TARGET.items():
        expected=byproblem[problem]
        state=issue_snapshot(n)
        cm=comments(n)
        original_review=[x for x in cm if (x.get('body') or '').startswith('GCL-CRITICAL-REVIEW/1\n')]
        fixed_note=[x for x in cm if (x.get('body') or '').startswith('GCL-SOURCE-FIDELITY-RECONCILIATION/1\n')]
        resolutions=[x for x in cm if (x.get('body') or '').startswith(RESOLUTION+'\n')]
        if (len(original_review)!=1 or original_review[0]['id']!=expected['review_comment']
                or 'DISPOSITION: REVISE\n' not in original_review[0]['body']
                or len(fixed_note)!=1 or len(resolutions)>1
                or expected['review_issue']!=n):
            raise CouncilError(f'#{n}: original REVIEW/1 or source repair evidence mismatch')
        if resolutions:
            if (resolutions[0].get('user') or {}).get('login')!='gcl-council-clerk[bot]':
                raise CouncilError(f'#{n}: resolution not made by Council Clerk App')
            if expected['refreshed_blob'] not in resolutions[0]['body']:
                raise CouncilError(f'#{n}: resolution references wrong source byte lock')
        elif not (state['revise'] and not state['corrected']):
            raise CouncilError(f'#{n}: labels changed without signed resolution')
        results.append({'issue':n,'problem':problem,'source_blob':expected['refreshed_blob'],
                        'state':state,'already_resolved':bool(resolutions)})
    for n in EXCLUDED:
        state=issue_snapshot(n)
        if not state['revise'] or state['corrected']:
            raise CouncilError(f'#{n}: unresolved external-proof/historical predicate case changed')
    return results

def verify_installation_scope():
    # GitHub App INSTALLATION access tokens intentionally do not implement
    # GET /user (HTTP 403). The pinned App-token workflow is the authority.
    # Recheck that the minted token is installed for exactly this one repo.
    obj=api('installation/repositories?per_page=100')
    if (not isinstance(obj,dict) or obj.get('total_count')!=1
            or not isinstance(obj.get('repositories'),list)
            or len(obj['repositories'])!=1
            or obj['repositories'][0].get('full_name')!=REPO):
        raise CouncilError('Council Clerk installation token is not restricted to MATH-PROGRAMME')


def verify_bot_resolution(issue,blob):
    notes=[x for x in comments(issue)
           if (x.get('body') or '').startswith(RESOLUTION+'\n')]
    if (len(notes)!=1 or (notes[0].get('user') or {}).get('login')!='gcl-council-clerk[bot]'
            or blob not in notes[0]['body']):
        raise CouncilError(f'#{issue}: authenticated Council Clerk source resolution not verified')


def apply_transitions(rows):
    if (os.environ.get('GITHUB_ACTIONS')!='true'
            or os.environ.get('GITHUB_REF')!='refs/heads/main'
            or os.environ.get('GCL_CONTROLLER_ID')!='erdos-three-source-resolution'
            or not os.environ.get('GH_TOKEN')):
        raise CouncilError('protected main release-trust Council Clerk runtime required')
    verify_installation_scope()
    # Create a narrowly named positive source-correction marker only once.
    try:
        lab=api(f'repos/{REPO}/labels/gcl-review%3Asource-corrected')
        if lab.get('name')!=CORRECTED:raise CouncilError('unexpected source-correction label identity')
    except CouncilError as ex:
        if '404' not in str(ex) and 'Not Found' not in str(ex):raise
        execute('api',f'repos/{REPO}/labels','--method','POST',
                '-f',f'name={CORRECTED}','-f','description=Protected source-fidelity remediation accepted; not mathematical certification',
                '-f','color=637381')
    for row in rows:
        n=row['issue']
        if not row['already_resolved']:
            body=(f'{RESOLUTION}\nERDOS_PROBLEM: {row["problem"]}\n'
                  f'REVIEW_ISSUE: #{n}\n'
                  'DISPOSITION: SOURCE_CORRECTION_ACCEPTED\n'
                  'PROTECTED_SOURCE_LOCK_PR: https://github.com/grandchallenge/MATH-PROGRAMME/pull/2695\n'
                  'SOURCE_FIDELITY_AUDIT_PR: https://github.com/grandchallenge/MATH-PROGRAMME/pull/2681\n'
                  f'NEW_GIT_BLOB_SHA1: {row["source_blob"]}\n'
                  'GOVERNANCE_EFFECT: source statement/interpretation accepted for RESEARCH ONLY, pending no source defects for this issue.\n'
                  'MATHEMATICAL_CERTIFICATION: FALSE\n'
                  'OPEN_PROBLEM_STATUS: UNCHANGED\n'
                  'ORIGINAL_RESULT_AND_CRITICAL_REVIEW: IMMUTABLE\n'
                  'PROJECT_AND_ISSUE_CUSTODY: RETURNED / OPEN (PRESERVED)\n'
                  'EXCEPTIONS: ERDOS 14 external kernel replay and ERDOS 41 imported historical predicate remain REVISE.\n')
            note=ROOT/'artifacts/erdos-three-source-resolution'/f'issue-{n}.md'
            note.parent.mkdir(parents=True,exist_ok=True)
            note.write_text(body)
            execute('issue','comment',str(n),'-R',REPO,'--body-file',str(note))
        # Require an authenticated APP author and exact statement lock before
        # ANY corresponding label mutation; replay-safe after partial writes.
        verify_bot_resolution(n,row['source_blob'])
        execute('issue','edit',str(n),'-R',REPO,'--add-label',CORRECTED,'--remove-label',REVISE)
        state=issue_snapshot(n)
        if state['revise'] or not state['corrected']:
            raise CouncilError(f'#{n}: source correction label readback failed')
    for n in EXCLUDED:
        state=issue_snapshot(n)
        if not state['revise'] or state['corrected']:
            raise CouncilError(f'#{n}: out-of-scope revision disturbed')
    return True

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--receipt',required=True)
    args=parser.parse_args()
    output={'schema':'GCL-ERDOS-THREE-SOURCE-COUNCIL/1',
            'apply_requested':args.apply,'source_provenance':'protected 2681 2683 2695',
            'three_source_remediations':[],'excluded_revision_issues':list(EXCLUDED),
            'mathematical_certification':False,'original_provenance_changed':False,
            'applied':False,'error':None}
    target=ROOT/args.receipt
    target.parent.mkdir(parents=True,exist_ok=True)
    try:
        rows=check_evidence()
        output['three_source_remediations']=rows
        if args.apply:
            apply_transitions(rows)
            output['applied']=True
            output['three_source_remediations']=check_evidence()
            if not all(x['already_resolved'] and not x['state']['revise'] and x['state']['corrected'] for x in output['three_source_remediations']):
                raise CouncilError('postwrite dispositions incomplete')
    except Exception as e:
        output['error']=str(e)
        target.write_text(json.dumps(output,indent=2)+'\n')
        raise
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'applied':output['applied'],'count':len(output['three_source_remediations']),
                      'excluded':output['excluded_revision_issues']},sort_keys=True))

if __name__=='__main__':main()
