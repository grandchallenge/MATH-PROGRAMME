#!/usr/bin/env python3
import json
def predicate(n): return n*n==4
def check_package(pkg): return isinstance(pkg.get('witness'),int) and pkg.get('certificate')==predicate(pkg['witness']) and pkg['certificate'] is True
def extract(pkg):
    if not check_package(pkg): raise ValueError('invalid witness/certificate package')
    return pkg['witness']
def run():
    good={'witness':2,'certificate':True}; witness=extract(good); replay=predicate(witness)
    hostile=False
    try: extract({'witness':3,'certificate':True})
    except ValueError: hostile=True
    ok=witness==2 and replay and hostile
    return {'lab':'11-extractor','ok':ok,'extracted_witness':witness,'replay':replay,'corrupt_certificate_rejected':hostile,'claim_boundary':'Selected finite existential extraction architecture only.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
