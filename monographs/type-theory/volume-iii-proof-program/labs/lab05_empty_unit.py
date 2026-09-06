#!/usr/bin/env python3
import json
UNIT='star'
VALUE_SHAPES={'arrow':'lambda','product':'pair','sum':'injection','unit':'star','empty':None}
def next_step(term):
    tag=term[0]
    if tag=='id-app': return ('value',term[1])
    if tag=='pair-fst': return ('value',term[1])
    if tag=='sum-case': return ('value',term[2] if term[1]=='left' else term[3])
    if tag=='value': return None
    raise ValueError('ill-formed fixture')
def run():
    fixtures=[('value',UNIT),('id-app',7),('pair-fst','A','B'),('sum-case','left','L','R')]
    progress=all(t[0]=='value' or next_step(t) is not None for t in fixtures)
    ok=progress and VALUE_SHAPES['empty'] is None
    return {'lab':'05-empty-unit','ok':ok,'canonical_shapes':VALUE_SHAPES,'finite_progress_fixture':progress,'claim_boundary':'Finite progress fixture does not prove progress or strong normalization.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
