#!/usr/bin/env python3
import json
def direct_identity(x): return x
def cps_identity(x,k): return k(x)
def direct_compose(f,g,x): return f(g(x))
def cps_compose(f,g,x,k): return k(f(g(x)))
def run():
    fixtures=[0,1,7,'proof']
    identity=all(cps_identity(x,lambda y:y)==direct_identity(x) for x in fixtures)
    f=lambda x:x+1; g=lambda x:x*2
    composition=all(cps_compose(f,g,x,lambda y:y)==direct_compose(f,g,x) for x in [0,1,5])
    ok=identity and composition
    return {'lab':'09-cps','ok':ok,'identity_fixtures':identity,'composition_fixtures':composition,'answer_type_model':'host result of continuation','claim_boundary':'Closed fixture equivalence for a restricted CPS model; not a control-calculus metatheorem.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
