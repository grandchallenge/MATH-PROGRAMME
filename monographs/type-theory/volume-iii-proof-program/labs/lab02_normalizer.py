#!/usr/bin/env python3
from __future__ import annotations
from typing import Mapping
import json
from lab01_implication_checker import Type, Atom, Arrow, Term, Var, Lam, App, parse_term, infer

def free_vars(term: Term) -> set[str]:
    if isinstance(term,Var): return {term.name}
    if isinstance(term,Lam): return free_vars(term.body)-{term.var}
    if isinstance(term,App): return free_vars(term.fn)|free_vars(term.arg)
    raise AssertionError(term)
def fresh(base: str, avoid: set[str]) -> str:
    if base not in avoid: return base
    i=1
    while f"{base}{i}" in avoid: i+=1
    return f"{base}{i}"
def rename_bound(term: Term, old: str, new: str) -> Term:
    if isinstance(term,Var): return Var(new) if term.name==old else term
    if isinstance(term,App): return App(rename_bound(term.fn,old,new),rename_bound(term.arg,old,new))
    if isinstance(term,Lam):
        if term.var==old: return Lam(new,term.var_type,rename_bound(term.body,old,new))
        return Lam(term.var,term.var_type,rename_bound(term.body,old,new))
    raise AssertionError(term)
def subst(term: Term, var: str, replacement: Term) -> Term:
    if isinstance(term,Var): return replacement if term.name==var else term
    if isinstance(term,App): return App(subst(term.fn,var,replacement),subst(term.arg,var,replacement))
    if isinstance(term,Lam):
        if term.var==var: return term
        rf=free_vars(replacement)
        if term.var in rf:
            avoid=free_vars(term.body)|rf|{var}; new=fresh(term.var,avoid)
            return Lam(new,term.var_type,subst(rename_bound(term.body,term.var,new),var,replacement))
        return Lam(term.var,term.var_type,subst(term.body,var,replacement))
    raise AssertionError(term)
def step_normal_order(term: Term) -> Term|None:
    if isinstance(term,App):
        if isinstance(term.fn,Lam): return subst(term.fn.body,term.fn.var,term.arg)
        fn1=step_normal_order(term.fn)
        if fn1 is not None: return App(fn1,term.arg)
        arg1=step_normal_order(term.arg)
        if arg1 is not None: return App(term.fn,arg1)
        return None
    if isinstance(term,Lam):
        body1=step_normal_order(term.body)
        return None if body1 is None else Lam(term.var,term.var_type,body1)
    if isinstance(term,Var): return None
    raise AssertionError(term)
def normalize(term: Term, ctx: Mapping[str,Type]|None=None, max_steps: int=1000):
    ctx={} if ctx is None else dict(ctx); invariant=infer(term,ctx); trace=[term]; current=term
    for _ in range(max_steps):
        nxt=step_normal_order(current)
        if nxt is None: return invariant,trace
        if infer(nxt,ctx)!=invariant: raise AssertionError("type invariant changed during normalization")
        trace.append(nxt); current=nxt
    raise RuntimeError(f"normalization exceeded {max_steps} steps")
def run_fixtures() -> dict:
    cases=[
      ("identity-beta","(app (lam f (-> P P) f) (lam x P x))"),
      ("nested-beta","(app (lam f (-> P P) (lam y P (app f y))) (lam x P x))"),
      ("capture-avoidance","(app (lam x P (lam y Q x)) y)")]
    reports=[]
    for name,src in cases:
        ctx={"y":Atom("P")} if name=="capture-avoidance" else {}
        term=parse_term(src); ty,trace=normalize(term,ctx)
        reports.append({"name":name,"type":str(ty),"steps":len(trace)-1,"trace":[str(t) for t in trace]})
    ok=(reports[0]["trace"][-1]=="(lam x:P. x)" and reports[1]["trace"][-1].startswith("(lam y:P.") and "lam y1:Q" in reports[2]["trace"][-1])
    return {"calculus":"CH-0 implication fragment","strategy":"deterministic normal order","ok":ok,"cases":reports,"claim_boundary":"The traces test this evaluator and type preservation on fixtures; they do not prove strong normalization."}
if __name__=="__main__":
    report=run_fixtures(); print(json.dumps(report,indent=2)); raise SystemExit(0 if report["ok"] else 1)
