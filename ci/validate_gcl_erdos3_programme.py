#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

EXPECTED_SOLVE="6c39975864788f27aea1f0da50fa409625bd5bd6"

def validate(root=ROOT):
    errors=[]
    state=json.loads((root/'governance/openmath_2026_campaign_state.json').read_text())
    reg=json.loads((root/'governance/gcl_erdos3_campaign.json').read_text())
    if state.get('event_window',{}).get('state')!='TERMINAL':
        errors.append('OPENMATH event window not terminal')
    if state.get('event_window',{}).get('official_submissions')!=0:
        errors.append('OPENMATH submission count drift')
    if state.get('event_window',{}).get('official_acceptances')!=0:
        errors.append('OPENMATH acceptance count drift')
    if state.get('summary',{}).get('external_agents',{}).get('leased_not_launched')!=0:
        errors.append('OPENMATH still exposes leased replay work')
    if state.get('next_action',{}).get('currently_selected')!=[]:
        errors.append('OPENMATH still selects active hills')
    if reg.get('campaign_id')!='GCL-ERDOS3' or reg.get('status')!='ACTIVE__E3_TRANCHE_01':
        errors.append('GCL-ERDOS3 registration drift')
    if reg.get('origin',{}).get('solve_commit')!=EXPECTED_SOLVE:
        errors.append('GCL-ERDOS3 Solve evidence bind drift')
    if reg.get('mechanism',{}).get('automatic_replay_successors') is not False:
        errors.append('automatic replay successor policy returned')
    if reg.get('mechanism',{}).get('next_residual_is_scheduling_authority') is not False:
        errors.append('Next residual regained scheduling authority')
    if reg.get('current_frontier')!=['E3-V-B01','E3-B-AP']:
        errors.append('Programme frontier projection drift')
    results=reg.get('results',{})
    if results.get('E3-F01',{}).get('disposition')!='FORMALIZED':
        errors.append('F01 result missing')
    if results.get('E3-B01',{}).get('disposition')!='PROVED_NATIVE_PENDING_INDEPENDENT_VERIFY':
        errors.append('B01 result missing')
    if results.get('E3-A01',{}).get('disposition')!='BOUNDARY_SHARPENED':
        errors.append('A01 result missing')
    if results.get('E3-S01',{}).get('disposition')!='SOURCE_INTERFACE_FOUND':
        errors.append('S01 result missing')
    verification=reg.get('verification',{})
    if verification.get('issue_number')!=762 or verification.get('state')!='DISPATCHED__AWAITING_RETURN':
        errors.append('B01 verification dispatch drift')
    if verification.get('task_commit')!=EXPECTED_SOLVE:
        errors.append('B01 verification task bind drift')
    return errors

if __name__=='__main__':
    e=validate()
    for x in e: print('FAIL:',x)
    if not e: print('PASS: GCL-ERDOS3 tranche E3-01 projected; F01 closed, B01 proved, one independent verification dispatched, k>=4 frontier open')
    raise SystemExit(bool(e))
