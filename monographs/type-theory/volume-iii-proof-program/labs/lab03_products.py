#!/usr/bin/env python3
from dataclasses import dataclass
import json
@dataclass(frozen=True)
class Pair: left: object; right: object
def fst(p):
    if not isinstance(p,Pair): raise TypeError('projection requires pair')
    return p.left
def snd(p):
    if not isinstance(p,Pair): raise TypeError('projection requires pair')
    return p.right
def run():
    p=Pair('proof-A','proof-B'); negative=False
    try: fst('not-a-pair')
    except TypeError: negative=True
    ok=fst(p)=='proof-A' and snd(p)=='proof-B' and negative
    return {'lab':'03-products','ok':ok,'principal_reductions':['fst(pair(a,b))=a','snd(pair(a,b))=b'],'negative_projection_rejected':negative,'claim_boundary':'Fixture evidence for product construction/projection only.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
