#!/usr/bin/env python3
import json
def kernel_check(cert):
    term=cert['term']; claimed=cert['claimed_type']
    if term=='lam x:P. x': inferred='P->P'
    elif term=='lam x:Q. x': inferred='Q->Q'
    else: raise ValueError('kernel parser rejects unsupported certificate')
    if inferred!=claimed: raise ValueError(f'type mismatch: inferred {inferred}, claimed {claimed}')
    return inferred
def run():
    good=kernel_check({'term':'lam x:P. x','claimed_type':'P->P'})
    hostile=[]
    for cert in [{'term':'lam x:P. x','claimed_type':'Q->Q'},{'term':'magic','claimed_type':'P'}]:
        try: kernel_check(cert); hostile.append(False)
        except ValueError: hostile.append(True)
    ok=good=='P->P' and all(hostile)
    return {'lab':'13-kernel-boundary','ok':ok,'positive':good,'hostile_rejections':hostile,'claim_boundary':'Toy independent checker; does not certify informal-statement translation or implementation correctness.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
