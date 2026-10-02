#!/usr/bin/env python3
import json
DOMAIN=(0,1)
def universal_table(f,predicate): return all(predicate(x,f(x)) for x in DOMAIN)
def existential_package(witness,evidence,predicate): return witness in DOMAIN and evidence and predicate(witness)
def run():
    f=lambda x:1-x
    universal=universal_table(f,lambda x,y:y==1-x)
    existential=existential_package(1,True,lambda x:x*x==1)
    hostile=not existential_package(2,True,lambda x:x*x==1)
    ok=universal and existential and hostile
    return {'lab':'06-quantifiers','ok':ok,'domain':list(DOMAIN),'universal_table_checked':universal,'existential_package_checked':existential,'out_of_domain_rejected':hostile,'claim_boundary':'Finite rule-shape model; not a dependent type checker.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
