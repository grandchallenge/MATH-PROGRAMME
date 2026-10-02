#!/usr/bin/env python3
from dataclasses import dataclass
import json
@dataclass(frozen=True)
class Proof:
    end:str; cut_formula:str|None=None; left:object=None; right:object=None
def rank(p): return (0,1) if p.cut_formula is None else (len(p.cut_formula),1+(rank(p.left)[1] if p.left else 0)+(rank(p.right)[1] if p.right else 0))
def principal_reduce(p):
    if p.cut_formula!='A->B': raise ValueError('fixture reducer only handles principal implication cut')
    return Proof(end=p.end,cut_formula='B',left=Proof('B'),right=Proof(p.end))
def run():
    p=Proof('Gamma,Delta=>C','A->B',Proof('Gamma=>A->B'),Proof('Delta,A->B=>C'))
    q=principal_reduce(p); decreased=rank(q)<rank(p); preserved=q.end==p.end
    hostile=False
    try: principal_reduce(Proof('X','A+B'))
    except ValueError: hostile=True
    ok=decreased and preserved and hostile
    return {'lab':'07-cut-reducer','ok':ok,'before_rank':rank(p),'after_rank':rank(q),'end_sequent_preserved':preserved,'unsupported_cut_rejected':hostile,'claim_boundary':'One bounded principal-reduction schema; not general cut elimination.'}
if __name__=='__main__':
    r=run(); print(json.dumps(r,indent=2)); raise SystemExit(0 if r['ok'] else 1)
