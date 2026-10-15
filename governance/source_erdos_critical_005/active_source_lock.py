#!/usr/bin/env python3
"""Source-selection ledger: immutable original review versus admitted research.

No GitHub changes, no MathCERT, no Solve dispatch. Does not substitute a
source-correction annotation for a proved mathematical theorem.
"""
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LEDGER=Path(__file__).with_name('ACTIVE_SOURCE_LOCKS_005.json')
ROSTER=ROOT/'governance/erdos_catalogue/ROLLING_RESEARCH_024.json'
ALLOWED={11:2520,12:2521,15:2523}
class SourceLockError(ValueError):pass

def verify(registry,roster,root=ROOT):
    if registry.get('record_type')!='GCL_ERDOS_CRITICAL_ACTIVE_SOURCE_LOCKS_005_V1':
        raise SourceLockError('unknown source contract')
    if registry.get('reconciled_cohort')!=roster.get('cohort_id') or len(roster.get('items',[]))!=24:
        raise SourceLockError('not the protected exact-24 cohort')
    if registry.get('authority_effects')!={'mathematical_certification':False,'solve_dispatch':False,'issue_closure':False,'review_label_clearance':False,'source_history_mutation':False}:
        raise SourceLockError('authority escalation')
    byid={r['problem_id']:r for r in roster['items']}
    sources=registry.get('active_sources')
    if not isinstance(sources,list) or len(sources)!=3 or {x['problem_id'] for x in sources}!=set(ALLOWED):
        raise SourceLockError('incorrect admitted source subset')
    for row in sources:
        n=row['problem_id'];old=byid[n]
        if (row['review_issue']!=ALLOWED[n]
                or row['catalogue_issue']!=old['catalogue_issue']
                or row['frozen_historical_blob_sha1']!=old['protected_statement']['git_blob_sha1']
                or row['provider_path']!=old['protected_statement']['path']
                or row['provider_repository']!=old['protected_statement']['provider_repository']
                or row['provider_commit']!='79eac378a26b46d30974cdb33962e0752591b79d'
                or row['source_role']!='ACTIVE_RESEARCH_SOURCE_FIDELITY_REFERENCE'
                or row['historical_roster_not_overwritten'] is not True
                or row['mathcert'] is not False or row['solve_dispatch'] is not False
                or row['research_problem_open'] is not True):
            raise SourceLockError('provider identity, review binding or source scope drift')
        path=root/row['source_snapshot']
        if path.parent!=ROOT/'governance/source_erdos_critical_005' or not path.is_file():
            raise SourceLockError('source outside protected snapshot directory')
        b=path.read_bytes()
        if row['source_sha256']!=hashlib.sha256(b).hexdigest():
            raise SourceLockError('source byte hash changed')
        gitblob=hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
        if gitblob!=row['provider_blob_sha1']:
            raise SourceLockError('provider Git blob changed')
        if gitblob==row['frozen_historical_blob_sha1']:
            raise SourceLockError('not a corrected source')
    if registry.get('excluded_until_replay')!={'14':'EXTERNAL_PROOF_KERNEL_REPLAY_UNVERIFIED','41':'HISTORICAL_AT_MOST_THREE_DISTINCT_PREDICATE_NOT_CURRENT_MULTISET'}:
        raise SourceLockError('pending #14/#41 improperly admitted')
    return sources

def get(problem_id, purpose='research'):
    roster=json.loads(ROSTER.read_text());registry=json.loads(LEDGER.read_text())
    sources=verify(registry,roster)
    if purpose!='research':raise SourceLockError('this source selection may not dispatch or certify')
    return next((x for x in sources if x['problem_id']==problem_id),None)

if __name__=='__main__':
    r=json.loads(ROSTER.read_text());s=json.loads(LEDGER.read_text());rows=verify(s,r)
    print('EXACT_SOURCE_LOCKS_VALID',len(rows),[x['problem_id'] for x in rows])
