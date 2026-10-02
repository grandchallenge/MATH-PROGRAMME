#!/usr/bin/env python3
from dataclasses import dataclass
import json
@dataclass(frozen=True)
class Inl: value: object
@dataclass(frozen=True)
class Inr: value: object
def case(s,left,right):
    if isinstance(s,Inl): return left(s.value)
    if isinstance(s,Inr): return right(s.value)
    raise TypeError('case requires sum injection')
def run():
    a=case(Inl(3),lambda x:x+1,lambda y:y-1)
    b=case(Inr(3),lambda x:x+1,lambda y:y-1)
    hostile=False
    try: case(3,lambda x:x,lambda x:x)
    except TypeError: hostile=True
    ok=(a,b)==(4,2) and hostile
    return {'lab':'04-sums','ok':ok,'left_result':a,'right_result':b,'non_sum_rejected':hostile,'claim_boundary':'Branch evaluation fixtures; branch typing theorem remains in manuscript.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
