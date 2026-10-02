#!/usr/bin/env python3
import json
WORLDS=('w0','w1'); LEQ={('w0','w0'),('w0','w1'),('w1','w1')}; ATOM_P={'w1'}
def extensions(w): return [v for v in WORLDS if (w,v) in LEQ]
def forces_p(w): return w in ATOM_P
def forces_false(w): return False
def forces_not_p(w): return all((not forces_p(v)) or forces_false(v) for v in extensions(w))
def forces_em(w): return forces_p(w) or forces_not_p(w)
def run():
    persistence=all(not forces_p(w) or all(forces_p(v) for v in extensions(w)) for w in WORLDS)
    root={'P':forces_p('w0'),'not_P':forces_not_p('w0'),'EM':forces_em('w0')}
    ok=persistence and root=={'P':False,'not_P':False,'EM':False} and forces_em('w1')
    return {'lab':'08-kripke','ok':ok,'persistence':persistence,'root':root,'w1_EM':forces_em('w1'),'claim_boundary':'Finite countermodel under implemented intuitionistic forcing clauses.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
