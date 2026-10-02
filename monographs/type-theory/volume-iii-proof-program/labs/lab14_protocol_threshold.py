#!/usr/bin/env python3
import json
def closed_handler(x): return x+1
TRANSITIONS={('start','hello'):'await_ack',('await_ack','ack'):'start'}
def check_trace(messages):
    state='start'
    for m in messages:
        key=(state,m)
        if key not in TRANSITIONS: return False,state,m
        state=TRANSITIONS[key]
    return True,state,None
def run():
    closed=closed_handler(4)==5
    legal=check_trace(['hello','ack','hello','ack'])[0]
    hostile=not check_trace(['ack'])[0]
    ok=closed and legal and hostile
    return {'lab':'14-protocol-threshold','ok':ok,'closed_handler_terminates':closed,'legal_trace_accepted':legal,'hostile_ordering_rejected':hostile,'claim_boundary':'Trace conformance example only; no session fidelity, deadlock-freedom, fairness, or liveness theorem.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
