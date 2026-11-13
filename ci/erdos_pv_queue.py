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

def permitted(row,phase):
    s=row['stage_work_items'];target=s[phase]
    if target['work_status'] not in ('UNEXECUTED','EVIDENCE_BLOCKED'):return False
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
            selected.append({'task_id':t['task_id'],'problem_id':n,'phase':stage,'queue_issue':t['issue_number'],'source_issue':row['source_audit_issue'],'source_issue_body_sha256':row['source_issue_body_sha256'],'historical_catalogue_status':row['catalogue_status_at_lock'],'formal_provider_hint':row['formal_provider_hint_at_lock'],'triage_decision':row['triage_decision'],'cohort':name,'source_commit':reg['source_lock']['source_commit'],'requires_atomic_claim_and_live_readback':True})
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
    print(json.dumps(out,ensure_ascii=False,sort_keys=True))

if __name__=='__main__':main()
