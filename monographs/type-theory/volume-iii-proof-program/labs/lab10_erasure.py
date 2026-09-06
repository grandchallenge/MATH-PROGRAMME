#!/usr/bin/env python3
import json
def erase(record):
    if record.get('ghost_controls_output'): raise ValueError('irrelevant field influences retained output')
    return {'value':record['value']}
def run():
    good={'value':9,'ghost':'certificate','ghost_controls_output':False}
    retained=erase(good); hostile=False
    try: erase({'value':1,'ghost':False,'ghost_controls_output':True})
    except ValueError: hostile=True
    ok=retained=={'value':9} and hostile
    return {'lab':'10-erasure','ok':ok,'retained':retained,'hostile_dependency_rejected':hostile,'claim_boundary':'Toy marked erasure policy; no global proof irrelevance claim.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
