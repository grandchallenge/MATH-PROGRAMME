#!/usr/bin/env python3
"""Closed-world, fail-closed 1,221-problem proof-work queue inventory validator.

Queue creation never certifies mathematics. Full closure demands separate receipts.
"""
from __future__ import annotations
import collections
import hashlib
import json
from pathlib import Path
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
REG='governance/erdos_proof_verification/coverage/REGISTRY.json'
SRC='governance/erdos_catalogue/REGISTRY.json'
PHASES='ABCD'
PILOT={246:3202,247:3203,248:3204,249:3205,250:3206}
VALID_STATUS={'UNEXECUTED','PILOT_REUSE_PENDING_EVIDENCE','IN_PROGRESS','EVIDENCE_BLOCKED','VERIFIED_BOUNDED','NOT_APPLICABLE_REVIEWED','PROTECTED_ADMITTED','REUSED_SCOPE_VERIFIED'}

def ensure(ok,msg):
    if not ok:raise ValueError(msg)

def read(path,root=ROOT):
    p=(root/path).resolve()
    ensure(p.is_relative_to(root.resolve()) and p.is_file(),'unsafe or missing file '+str(path))
    return json.loads(p.read_text())

TRIAGE_FIVE_PATH = 'governance/erdos_proof_verification/triage/0560-0564.json'


def validate_five_source_scope(row, root=ROOT):
    n=row['problem_id']
    if n not in (560,561,562,563,564):
        return
    doc=read(TRIAGE_FIVE_PATH,root)
    ensure(doc['record_type']=='GCL-ERDOS-560-564-PHASE-A-SCOPE-TRIAGE/1'
           and doc['source_commit']=='536408716724a2402bdfa7c1d764bf83d64a8c89'
           and doc['source_file_blob_sha1']=='4e60263a80af6207aca494d2e1388e44fa372889'
           and doc['cohort_issue']==3217 and doc['phase_B_issue']==3230
           and doc['source_only_verified_count']==3 and doc['source_blocked_count']==2
           and doc['selection_policy']=='SOURCE_SCOPE_BEFORE_PROOF__NO_DUPLICATE_QUEUE__NO_AUTO_CERTIFICATION',
           '560-564 protected triage identity or claim scope drift')
    records=doc['records']
    ensure(len(records)==5 and [r['problem_id'] for r in records]==[560,561,562,563,564],
           '560-564 triage record census drift')
    r=records[n-560]
    expected_selected=n in (560,561,562)
    expected='SELECTED_WITH_MANIFEST' if expected_selected else 'PENDING'
    stage=row['stage_work_items']['A']
    ensure(r['source_audit_issue']==row['source_audit_issue']
           and r['source_issue_body_sha256']==row['source_issue_body_sha256']
           and re.fullmatch('[a-f0-9]{64}',r['source_comment_sha256']) is not None
           and isinstance(r['source_comment_id'],int) and r['source_comment_id']>0
           and r['source_issue_live_custody']=='OPEN__PROJECT_RETURNED__ISSUE_FIELD_RETURNED'
           and r['source_role_return_disposition']=='BOUNDED_TASK_DESIGNED'
           and r['triage_decision']==expected
           and row['source_issue_live_state']=='OPEN_RETURNED'
           and row['triage_decision']==expected
           and row['literature_status_current']=='SOURCE_AUDIT_RETURNED__RESEARCH_STATUS_UNCERTIFIED'
           and row['mathcert_status']=='NOT_SUBMITTED'
           and row['scope']=='OPEN_BOUNDED_LEMMA_ONLY'
           and r['critical_role_pass']['scope']=='STATEMENT_AND_QUEUE_SCOPE_ONLY__NO_PROOF'
           and r['critical_role_pass']['separate_human_identity_claim'] is False
           and r['critical_role_pass']['role']=='LOGICAL_ADVERSARY'
           and r['critical_role_pass']['actor']=='fyremael'
           and all(v is False for v in r['prohibitions'].values()),
           f'problem {n}: source critical-scope or return identity drift')
    comment=f"https://github.com/grandchallenge/MATH-PROGRAMME/issues/{row['source_audit_issue']}#issuecomment-{r['source_comment_id']}"
    ensure(stage['source_lock_receipt']==TRIAGE_FIVE_PATH
           and stage['evidence_refs']==[TRIAGE_FIVE_PATH,comment]
           and stage['work_status']==('VERIFIED_BOUNDED' if expected_selected else 'EVIDENCE_BLOCKED')
           and stage['review_status']==('ROLE_SCOPED_CRITICAL_PASS' if expected_selected else 'BLOCKER_CONFIRMED')
           and stage['blocker']==(None if expected_selected else r['critical_role_pass']['finding'])
           and row['closure_status']==('IN_PROGRESS' if expected_selected else 'BLOCKED_WITH_EVIDENCE')
           and r['selected_phase_B_queue_issue']==(3230 if expected_selected else None)
           and r['scope_review']==('SOURCE_READY_FOR_BOUNDED_VERIFICATION' if expected_selected
                                    else ('SOURCE_CONFLICT_REPAIR_REQUIRED' if n==563 else 'EVIDENCE_BLOCKED')),
           f'problem {n}: invalid Phase A triage, evidence or blocker')
    # Phase A was an immutable prerequisite, not a permanent B/C/D freeze.
    # A future stage may advance only if source-selected, previous evidence
    # is reviewed, and its own stage-specific receipts exist. This preserves
    # the original no-promotion gate without deadlocking legitimate Phase B.
    admitted={'VERIFIED_BOUNDED','PROTECTED_ADMITTED','REUSED_SCOPE_VERIFIED',
              'NOT_APPLICABLE_REVIEWED'}
    for later, predecessor in (('B','A'),('C','B'),('D','C')):
        v=row['stage_work_items'][later]
        if v['work_status']=='UNEXECUTED':
            ensure(not v['evidence_refs'] and v['formal_replay_receipt'] is None
                   and v['protected_admission_ref'] is None,
                   f'problem {n}: unexecuted stage contains false completion evidence')
            continue
        prior=row['stage_work_items'][predecessor]
        ensure(expected_selected and prior['work_status'] in admitted,
               f'problem {n}: downstream phase not source-selected/reviewed')
        if later in ('C','D'):
            ensure(prior['work_status']=='PROTECTED_ADMITTED',
                   f'problem {n}: {later} requires previous protected admission')
        evidence=v['evidence_refs']
        ensure(isinstance(evidence,list) and bool(evidence)
               and all(isinstance(x,str) and x.startswith(
                   f'governance/erdos_proof_verification/evidence/{n:04}/') for x in evidence)
               and v['source_lock_receipt']==TRIAGE_FIVE_PATH,
               f'problem {n}: downstream evidence/source lock not scoped')
        # The named evidence files must exist in this exact checked-out
        # candidate, not merely be strings that resemble paths.
        ensure(all((root / ref).resolve().is_relative_to(root.resolve())
                   and (root / ref).is_file() for ref in evidence),
               f'problem {n}: downstream proof evidence file missing')
        if v['work_status'] in admitted:
            ensure(v['review_status'] not in ('NOT_REVIEWED','PENDING','')
                   and v['adversarial_review_receipt'] in evidence
                   and v['semantic_equivalence_receipt'] in evidence,
                   f'problem {n}: bounded result lacks semantic/adversarial review')
        if v['work_status']=='PROTECTED_ADMITTED':
            ensure(bool(v['protected_admission_ref']),
                   f'problem {n}: unbound protected admission')
        else:
            ensure(v['protected_admission_ref'] is None,
                   f'problem {n}: protected admission claimed before merge')

def validate_row(row,source,phase_issues,root=ROOT):
    n=source['problem_id'];tag=f'problem {n}'
    ensure(row['problem_id']==n,tag+': wrong ID')
    ensure(row['source_audit_issue']==source['issue_number'],tag+': wrong source issue')
    ensure(re.fullmatch('[0-9a-f]{64}',row['source_issue_body_sha256']) is not None and row['source_issue_body_sha256']==source['issue_body_sha256'],tag+': source body hash mismatch')
    ensure(row['catalogue_status_at_lock']==source['catalogue_status'] and row['catalogue_triage_class_at_lock']==source['triage_class'],tag+': status/triage lock mismatch')
    ensure(row['formal_provider_hint_at_lock'] is source['protected_fc_present'],tag+': formal hint mismatch')
    ensure(row['topics']==source['topics'],tag+': source topics changed')
    ensure(n not in PILOT or row['existing_proof_issue']==PILOT[n],tag+': pilot dedup boundary drift')
    ensure(row['existing_proof_issue'] is None or (isinstance(row['existing_proof_issue'],int) and row['existing_proof_issue']>0),tag+': invalid prior proof issue')
    ensure(row['mathcert_status'] in ('NOT_SUBMITTED','SUBMITTED','CERTIFIED','DECLINED'),tag+': certification status invalid')
    if row['mathcert_status']!='NOT_SUBMITTED':
        ensure(bool(row['certification_ref']) and 'MATHCERT' in row['certification_ref'] and bool(row['closure_evidence_refs']),tag+': certification without MathCERT evidence')
    ensure(row['triage_decision'] in ('PENDING','SELECTED_WITH_MANIFEST','REUSED_EXISTING_VERIFICATION','DECLINED_WITH_REASON'),tag+': unknown triage decision')
    if row['triage_decision']=='DECLINED_WITH_REASON':
        ensure(row.get('triage_reason') and bool(row['closure_evidence_refs']),tag+': silent decline')
    if row['triage_decision']=='REUSED_EXISTING_VERIFICATION':
        ensure(row.get('prior_work_to_reconcile') and row['closure_evidence_refs'],tag+': unevidenced reuse')
    if row['source_issue_live_state']=='NOT_RECONCILED':
        ensure(row['triage_decision'] in ('PENDING','SELECTED_WITH_MANIFEST'),tag+': no current source readback')
    if row['catalogue_status_at_lock']=='open':
        ensure(row['scope']!='FULL_ORIGINAL_CONJECTURE_SOLVED',tag+': open conjecture promoted')
    stages=row['stage_work_items'];ensure(set(stages)==set(PHASES),tag+': missing work stages')
    for stage,rec in stages.items():
        issue=row['existing_proof_issue'] if row['existing_proof_issue'] is not None and stage!='A' else phase_issues[stage]
        ensure(rec['issue_number']==issue and rec['cohort_issue_number']==phase_issues[stage],tag+': incorrect project queue linkage at '+stage)
        ensure(rec['task_id']==f'ERDOS-PV-{n:04}-{stage}',tag+': task ID mismatch')
        ensure(rec['work_status'] in VALID_STATUS,tag+': unknown stage work status')
        ensure(rec['work_status']!='PILOT_REUSE_PENDING_EVIDENCE' or (n in PILOT and stage!='A'),tag+': ungrounded pilot reuse')
        if rec['work_status'] in ('VERIFIED_BOUNDED','PROTECTED_ADMITTED','REUSED_SCOPE_VERIFIED','NOT_APPLICABLE_REVIEWED'):
            ensure(rec['evidence_refs'] and rec['review_status'] not in ('NOT_REVIEWED','PENDING'),tag+': green work without evidence/adversarial review')
        if rec['work_status']=='PROTECTED_ADMITTED':
            ensure(bool(rec['protected_admission_ref']),tag+': admitted without protected readback')
        if rec['formal_replay_receipt'] is not None:
            ensure(stage=='C' and bool(rec['axiom_report_receipt']) and bool(rec['semantic_equivalence_receipt']),tag+': kernel replay missing axiom/type receipts')
        if rec['work_status']=='EVIDENCE_BLOCKED':
            ensure(rec['blocker'] and rec['evidence_refs'],tag+': blocker without evidence')
    if row['closure_status']=='ADMITTED_BOUNDED_COMPLETE':
        ensure(stages['D']['work_status']=='PROTECTED_ADMITTED' and bool(row['closure_evidence_refs']),tag+': false terminal closure')
        ensure(row['source_issue_live_state']!='NOT_RECONCILED' and row['triage_decision']!='PENDING',tag+': closed without source/triage')
        admitted={'VERIFIED_BOUNDED','PROTECTED_ADMITTED','REUSED_SCOPE_VERIFIED','NOT_APPLICABLE_REVIEWED'}
        ensure(all(stages[p]['work_status'] in admitted for p in PHASES),tag+': terminal stages not actually reviewed')
    else:ensure(row['closure_status'] in ('NOT_STARTED','IN_PROGRESS','BLOCKED_WITH_EVIDENCE'),tag+': invalid closure status')
    validate_five_source_scope(row,root)

def validate(root=ROOT):
    registry=read(REG,root);source_path=root/SRC;source=read(SRC,root)
    ensure(registry['record_type']=='ERDOS_PV_EXHAUSTIVE_QUEUE_REGISTRY/1','wrong registry identity')
    ensure(registry['source_registry_sha256']==hashlib.sha256(source_path.read_bytes()).hexdigest(),'source registry byte drift')
    ensure(registry['source_lock']==source['source'],'source lock drift')
    src=source['issues'];ensure(len(src)==1221 and [x['problem_id'] for x in src]==list(range(1,1222)),'source missing/duplicate problem')
    ensure(registry['population']['count']==1221 and registry['population']['unique_count']==1221 and not registry['population']['missing_ids'],'population count fiction')
    counts=dict(sorted(collections.Counter(x['catalogue_status'] for x in src).items()))
    ensure(registry['population']['historical_status_counts']==counts,'source status census drift')
    ensure(registry['population']['formal_provider_hints']==sum(x['protected_fc_present'] for x in src),'formal provider census drift')
    ensure(registry['model']['individual_problem_records']==1221 and registry['model']['new_problem_work_records']==1216 and registry['model']['per_problem_stage_slots']==4884,'scope arithmetic drift')
    ensure(registry['model']['cohort_stage_queue_issues']==52 and registry['model']['crosscutting_queue_issues']==6,'queue issue census drift')
    ensure(registry['inventory_complete'] and registry['source_registry_path']==SRC,'inventory state incompatible')
    ensure(registry['project_number']==2 and registry['queue_class']=='Mathematics','wrong queue')
    ensure(len(registry['cohorts'])==13,'missing cohort')
    ensure(registry['pilots']=={str(k):v for k,v in PILOT.items()},'pilot issue identity drift')
    issue_ids=set();project_ids=set();seen=[];pending=0;complete=0
    for i,meta in enumerate(registry['cohorts']):
        start=1+100*i;end=min(start+99,1221);expected={p:3212+13*j+i for j,p in enumerate(PHASES)}
        ensure((meta['first'],meta['last'],meta['count'])==(start,end,end-start+1),'missing/overlapping cohort range')
        ensure(meta['phase_issues']==expected,'cohort phase issue drift')
        ensure(meta['packet']==f'governance/erdos_proof_verification/coverage/cohorts/{start:04}-{end:04}.json','unsafe cohort pathname')
        packet=read(meta['packet'],root)
        ensure(packet['record_type']=='ERDOS_PV_COHORT_WORKSET/1' and packet['source_lock']==source['source'],'invalid packet source lock')
        ensure(packet['phase_issues']==expected and packet['range']=={'first':start,'last':end,'count':end-start+1},'packet range/queue mismatch')
        ensure(len(packet['items'])==end-start+1,'missing cohort items')
        ensure(packet['phase_project_items']==meta['phase_project_items'],'project refs drift')
        for phase,n in expected.items():
            ensure(n not in issue_ids,'duplicate phase issue');issue_ids.add(n)
            pid=packet['phase_project_items'][phase]
            ensure(isinstance(pid,str) and pid.startswith('PVTI_') and pid not in project_ids,'invalid or duplicate project item');project_ids.add(pid)
        for row,source_row in zip(packet['items'],src[start-1:end]):
            validate_row(row,source_row,expected,root);seen.append(row['problem_id']);pending+=(row['triage_decision']=='PENDING');complete+=(row['closure_status']=='ADMITTED_BOUNDED_COMPLETE')
    ensure(seen==list(range(1,1222)),'source population missing or permuted')
    cross=registry['crosscutting_issues'];ensure(len(cross)==6 and sorted(cross.values())==list(range(3264,3270)),'missing closure/dispatch issues')
    for label,n in cross.items():
        ensure(n not in issue_ids,'crosscut issue collision');issue_ids.add(n)
        pid=registry['crosscutting_project_items'][label]
        ensure(pid.startswith('PVTI_') and pid not in project_ids,'bad crosscut project item');project_ids.add(pid)
    ensure(len(issue_ids)==len(project_ids)==58,'queue inventory not 58 unique project tasks')
    if registry['triage_complete']:ensure(pending==0,'triage called complete with PENDING decisions')
    if registry['proof_verification_complete']:ensure(complete==1221,'proof verification called complete without 1221 admitted rows')
    if registry['documentary_closure_complete']:ensure(registry['proof_verification_complete'],'premature documentary closure')
    if registry['mathcert_certification_inferred']:raise ValueError('certification cannot follow from queue existence')
    return {'result':'PASS','individual_problems':len(seen),'distinct_phase_task_ids':len(seen)*4,'cohorts':13,'project_issues':58,'new_proof_problems':1216,'pilots_reused':5,'triage_pending':pending,'substantive_terminal_count':complete,'formal_provider_hints':registry['population']['formal_provider_hints'],'source_historical_status_counts':counts}

if __name__=='__main__':
    try:print(json.dumps(validate(),sort_keys=True))
    except Exception as exc:
        print(f'ERDOS_PV_FULL_COVERAGE_FAIL: {type(exc).__name__}: {exc}',file=sys.stderr)
        sys.exit(1)
