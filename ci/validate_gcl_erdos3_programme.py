#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

EXPECTED_SOLVE="a8abc98d7bd7017202fcb40ee3d5c04ad20769d6"

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
    if reg.get('campaign_id')!='GCL-ERDOS3' or reg.get('status')!='ACTIVE__E3_TRANCHE_02':
        errors.append('GCL-ERDOS3 registration drift')
    if reg.get('origin',{}).get('solve_commit')!=EXPECTED_SOLVE:
        errors.append('GCL-ERDOS3 Solve evidence bind drift')
    if reg.get('mechanism',{}).get('automatic_replay_successors') is not False:
        errors.append('automatic replay successor policy returned')
    if reg.get('mechanism',{}).get('next_residual_is_scheduling_authority') is not False:
        errors.append('Next residual regained scheduling authority')
    if reg.get('current_frontier')!=['E3-V-B02','E3-Q4-SERIES']:
        errors.append('Programme frontier projection drift')
    results=reg.get('results',{})
    if results.get('E3-F01',{}).get('disposition')!='FORMALIZED':
        errors.append('F01 result missing')
    if results.get('E3-B01',{}).get('disposition')!='PROVED__INDEPENDENTLY_VERIFIED':
        errors.append('B01 independent verification missing')
    if results.get('E3-B02',{}).get('disposition')!='PROVED_NATIVE_SOURCE_CONFIRMED':
        errors.append('B02 exact equivalence missing')
    if results.get('E3-V01',{}).get('disposition')!='VERIFIED__CLOSED':
        errors.append('E3-V01 closure missing')
    verification=reg.get('verification',{})
    if verification.get('issue_number')!=776 or verification.get('state')!='DISPATCHED__AWAITING_RETURN':
        errors.append('B02 verification dispatch drift')
    if verification.get('task_commit')!='bf9bc7f448f92d71afeae937fda133b0e1d4de80':
        errors.append('B02 verification task bind drift')
    dispatches=reg.get('active_dispatches',{})
    for key,issue in [('E3-Q01',772),('E3-X01',773),('E3-A02',774),('E3-S03',775),('E3-V02',776)]:
        if dispatches.get(key,{}).get('issue_number')!=issue:
            errors.append(f'{key} dispatch projection drift')
    return errors

if __name__=='__main__':
    e=validate()
    for x in e: print('FAIL:',x)
    if not e: print('PASS: GCL-ERDOS3 B01 independently verified; E3-B-AP is sole active frontier')
    raise SystemExit(bool(e))
