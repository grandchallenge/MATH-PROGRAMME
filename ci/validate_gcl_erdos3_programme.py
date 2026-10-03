#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

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
    if reg.get('campaign_id')!='GCL-ERDOS3' or reg.get('status')!='ACTIVE':
        errors.append('GCL-ERDOS3 registration drift')
    if reg.get('mechanism',{}).get('automatic_replay_successors') is not False:
        errors.append('automatic replay successor policy returned')
    if reg.get('mechanism',{}).get('next_residual_is_scheduling_authority') is not False:
        errors.append('Next residual regained scheduling authority')
    return errors

if __name__=='__main__':
    e=validate()
    for x in e: print('FAIL:',x)
    if not e: print('PASS: OPENMATH terminal state and GCL-ERDOS3 promotion agree')
    raise SystemExit(bool(e))
