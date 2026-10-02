#!/usr/bin/env python3
import json,itertools
A=(0,1); B=('x','y')
RELATIONS=[set(),{(0,'x')},{(1,'y')},{(0,'x'),(1,'y')},set(itertools.product(A,B))]
def identity_a(x): return x
def identity_b(x): return x
def related_preserved(fa,fb,R): return all((fa(a),fb(b)) in R for a,b in R)
def hostile_a(x): return 1-x
def hostile_b(x): return x
def run():
    identity=all(related_preserved(identity_a,identity_b,R) for R in RELATIONS)
    hostile_fail=any(not related_preserved(hostile_a,hostile_b,R) for R in RELATIONS)
    ok=identity and hostile_fail
    return {'lab':'12-parametricity','ok':ok,'relations_checked':len(RELATIONS),'identity_preserves_all':identity,'hostile_nonuniform_function_detected':hostile_fail,'claim_boundary':'Finite relation fixtures only; not the abstraction theorem.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
