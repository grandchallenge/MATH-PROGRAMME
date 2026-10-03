#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

EXPECTED_SOLVE="20fc4eb4cda683bc07992bd27903e926b190b8b4"

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
    if reg.get('campaign_id')!='GCL-ERDOS3' or reg.get('status')!='ACTIVE__E3_B_AP':
        errors.append('GCL-ERDOS3 registration drift')
    if reg.get('origin',{}).get('solve_commit')!=EXPECTED_SOLVE:
        errors.append('GCL-ERDOS3 Solve evidence bind drift')
    if reg.get('mechanism',{}).get('automatic_replay_successors') is not False:
        errors.append('automatic replay successor policy returned')
    if reg.get('mechanism',{}).get('next_residual_is_scheduling_authority') is not False:
        errors.append('Next residual regained scheduling authority')
    if reg.get('current_frontier')!=['E3-B-AP']:
        errors.append('Programme frontier projection drift')
    results=reg.get('results',{})
    if results.get('E3-F01',{}).get('disposition')!='FORMALIZED':
        errors.append('F01 result missing')
    if results.get('E3-B01',{}).get('disposition')!='PROVED__INDEPENDENTLY_VERIFIED':
        errors.append('B01 independent verification missing')
    if results.get('E3-V01',{}).get('disposition')!='VERIFIED__CLOSED':
        errors.append('E3-V01 closure missing')
    verification=reg.get('verification',{})
    if verification.get('issue_number')!=762 or verification.get('state')!='CLOSED_VERIFIED':
        errors.append('B01 verification closure drift')
    if verification.get('result_comment_id')!=5969123988:
        errors.append('B01 verification result bind drift')
    if verification.get('adjudication_commit')!=EXPECTED_SOLVE:
        errors.append('B01 verification adjudication bind drift')
    return errors

if __name__=='__main__':
    e=validate()
    for x in e: print('FAIL:',x)
    if not e: print('PASS: GCL-ERDOS3 B01 independently verified; E3-B-AP is sole active frontier')
    raise SystemExit(bool(e))
