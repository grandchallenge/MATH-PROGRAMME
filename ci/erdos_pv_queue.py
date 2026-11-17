#!/usr/bin/env python3
"""Read-only source-locked pickup selector for the 1,221-item Erdős verification queue.

A returned candidate is NOT a lease. Acquire the existing authorized atomic
claim and reconcile GitHub comments/status before execution or any mutation.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from validate_erdos_pv_full_coverage import ROOT,REG,read,validate,ensure

READY={'VERIFIED_BOUNDED','PROTECTED_ADMITTED','NOT_APPLICABLE_REVIEWED','REUSED_SCOPE_VERIFIED'}
RAMSEY_SOURCE_FILE = 'governance/source_erdos_566_567/FORMAL_SOURCE_RECONCILIATION.json'
RAMSEY_SOURCE_COMMIT = '6751c0f043985ac6647db28a45a63afdf21acffe'
RAMSEY_SOURCE_BLOBS = {
    566: '554166014f8b0f596c59b02bd5d5a7796c0383c9',
    567: 'f7159b8864d80b72ea44c16a78a93a871763291f',
}
RAMSEY_DEFINITION_BLOB = '9ad9e73d898e9b0cca1db96f1c537466bc07f385'


def checked_formal_source_override(problem, root=ROOT):
    # These two original 1993 vertex-Ramsey statements were erroneously
    # imported as edge-minimal size Ramsey statements in FC-GDM-85F86371.
    # Scope the correction to these two problem identities only.
    if problem not in RAMSEY_SOURCE_BLOBS:
        return None
    doc = read(RAMSEY_SOURCE_FILE, root)
    ensure(doc['record_type'] == 'GCL-ERDOS-566-567-FORMAL-SOURCE-RECONCILIATION/1'
           and doc['corrected_source_commit'] == RAMSEY_SOURCE_COMMIT
           and doc['corrected_source_repository'] == 'google-deepmind/formal-conjectures'
           and doc['legacy_provider_commit'] == '85f863718beeec7b58a3a1926ee92e3472bc2020'
           and doc['corrected_definition']['git_blob_sha1'] == RAMSEY_DEFINITION_BLOB
           and doc['corrected_definition']['target_invariant'] == 'SimpleGraph.graphRamsey'
           and doc['legacy_wrong_definition']['target_invariant'] == 'SimpleGraph.sizeRamsey'
           and doc['claim_boundary']['theorems_proved'] is False
           and doc['claim_boundary']['global_provider_snapshot_replaced'] is False,
           'Ramsey 566/567 source correction drift; no formal-work permission')
    row = doc['problems'][str(problem)]
    ensure(row['corrected_formal_path'] == f'FormalConjectures/ErdosProblems/{problem}.lean'
           and row['corrected_formal_blob_sha1'] == RAMSEY_SOURCE_BLOBS[problem]
           and row['legacy_formal_blob_sha1'] != RAMSEY_SOURCE_BLOBS[problem],
           'Ramsey 566/567 theorem source blob mismatch')
    return {
        'repository': doc['corrected_source_repository'],
        'commit': RAMSEY_SOURCE_COMMIT,
        'path': row['corrected_formal_path'],
        'git_blob_sha1': RAMSEY_SOURCE_BLOBS[problem],
        'definition_git_blob_sha1': RAMSEY_DEFINITION_BLOB,
        'legacy_invariant_disallowed': 'SimpleGraph.sizeRamsey',
        'original_invariant': 'SimpleGraph.graphRamsey',
        'source_admission_scope': 'FORMAL_STATEMENT_ONLY__NO_PROOF_CLAIM',
    }

def permitted(row,phase):
    s=row['stage_work_items'];target=s[phase]
    if target['work_status'] not in ('UNEXECUTED','EVIDENCE_BLOCKED'):return False
    if phase in ('B', 'C', 'D') and row['problem_id'] in RAMSEY_SOURCE_BLOBS:
        checked_formal_source_override(row['problem_id'])
    if phase=='A':return True
    if row['existing_proof_issue'] is not None:return False # independent pilot issue already owns B/C/D
    prev={'B':'A','C':'B','D':'C'}[phase]
    if s[prev]['work_status'] not in READY:return False
    if phase in ('C','D') and row['triage_decision']=='PENDING':return False
    return True

def candidates(stage='A',after=0,cohort=None,limit=1,root=ROOT):
    reg=read(REG,root);selected=[]
    for c in reg['cohorts']:
        name=c['packet'].rsplit('/',1)[-1].removesuffix('.json')
        if cohort and name!=cohort:continue
        for row in read(c['packet'],root)['items']:
            n=row['problem_id']
            if n<=after or not permitted(row,stage):continue
            t=row['stage_work_items'][stage]
            candidate={'task_id':t['task_id'],'problem_id':n,'phase':stage,'queue_issue':t['issue_number'],'source_issue':row['source_audit_issue'],'source_issue_body_sha256':row['source_issue_body_sha256'],'historical_catalogue_status':row['catalogue_status_at_lock'],'formal_provider_hint':row['formal_provider_hint_at_lock'],'triage_decision':row['triage_decision'],'cohort':name,'source_commit':reg['source_lock']['source_commit'],'requires_atomic_claim_and_live_readback':True}
            if stage != 'A' and n in RAMSEY_SOURCE_BLOBS:
                candidate['formal_source_override']=checked_formal_source_override(n,root)
                candidate['pinned_provider_hint_superseded_for_this_problem']=True
            selected.append(candidate)
            if len(selected)>=limit:return selected
    return selected

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['summary','next','get','validate'])
    p.add_argument('--stage',choices=list('ABCD'),default='A')
    p.add_argument('--cohort',help='e.g. 0001-0100')
    p.add_argument('--after',type=int,default=0)
    p.add_argument('--limit',type=int,default=1)
    p.add_argument('--problem',type=int)
    a=p.parse_args();ensure(a.limit>=1 and 0<=a.after<=1221,'invalid cursor/limit')
    if a.mode=='validate':out=validate()
    elif a.mode=='summary':
        out=validate();out['next_source_scope']=candidates('A',limit=1)
        out['next_math']=candidates('B',limit=1)
    elif a.mode=='next':out={'phase':a.stage,'candidates':candidates(a.stage,a.after,a.cohort,a.limit)}
    else:
        ensure(a.problem is not None and 1<=a.problem<=1221,'--problem required, 1..1221')
        reg=read(REG)
        c=reg['cohorts'][(a.problem-1)//100]
        row=read(c['packet'])['items'][(a.problem-1)%100]
        ensure(row['problem_id']==a.problem,'item index drift')
        out={'problem_id':a.problem,'queue_task':row['stage_work_items'][a.stage],'source_audit_issue':row['source_audit_issue'],'literature_status_at_lock':row['catalogue_status_at_lock'],'phase_can_run':permitted(row,a.stage),'warning':'Read-only selection, not a claim or proof acceptance'}
        if a.stage != 'A' and a.problem in RAMSEY_SOURCE_BLOBS:
            out['formal_source_override']=checked_formal_source_override(a.problem)
            out['legacy_provider_invariant_rejected']=True
    print(json.dumps(out,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
