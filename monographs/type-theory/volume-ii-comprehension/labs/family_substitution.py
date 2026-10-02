#!/usr/bin/env python3
"""COMP-0 family/context substitution laboratory for Volume II.

This is executable regression evidence for the first two chapters. It is not a
mechanized proof of the metatheory.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse
import json

# ---------- syntax ----------
class Term: pass

@dataclass(frozen=True)
class Var(Term):
    name: str

@dataclass(frozen=True)
class Zero(Term):
    pass

@dataclass(frozen=True)
class Succ(Term):
    term: Term

@dataclass(frozen=True)
class TrueTerm(Term):
    pass

@dataclass(frozen=True)
class FalseTerm(Term):
    pass

class Ty: pass

@dataclass(frozen=True)
class NatTy(Ty):
    pass

@dataclass(frozen=True)
class BoolTy(Ty):
    pass

@dataclass(frozen=True)
class FinTy(Ty):
    index: Term

Context = list[tuple[str, Ty]]
NAT = NatTy()
BOOL = BoolTy()

# ---------- display ----------
def show_term(t: Term) -> str:
    if isinstance(t, Var): return t.name
    if isinstance(t, Zero): return "0"
    if isinstance(t, Succ): return f"succ({show_term(t.term)})"
    if isinstance(t, TrueTerm): return "true"
    if isinstance(t, FalseTerm): return "false"
    raise TypeError(t)

def show_ty(A: Ty) -> str:
    if isinstance(A, NatTy): return "Nat"
    if isinstance(A, BoolTy): return "Bool"
    if isinstance(A, FinTy): return f"Fin({show_term(A.index)})"
    raise TypeError(A)

def show_ctx(ctx: Context) -> list[str]:
    return [f"{x}:{show_ty(A)}" for x, A in ctx]

# ---------- free variables and substitution ----------
def fv_term(t: Term) -> set[str]:
    if isinstance(t, Var): return {t.name}
    if isinstance(t, Succ): return fv_term(t.term)
    return set()

def subst_term(t: Term, a: Term, x: str) -> Term:
    if isinstance(t, Var): return a if t.name == x else t
    if isinstance(t, Succ): return Succ(subst_term(t.term, a, x))
    return t

def subst_ty(A: Ty, a: Term, x: str) -> Ty:
    if isinstance(A, FinTy): return FinTy(subst_term(A.index, a, x))
    return A

def subst_trailing_context(delta: Context, a: Term, x: str) -> Context:
    return [(name, subst_ty(A, a, x)) for name, A in delta]

# ---------- typing / formation ----------
def lookup(ctx: Context, name: str) -> Ty:
    for y, A in reversed(ctx):
        if y == name:
            return A
    raise TypeError(f"unbound variable {name}")

def infer(ctx: Context, t: Term) -> Ty:
    if isinstance(t, Var): return lookup(ctx, t.name)
    if isinstance(t, Zero): return NAT
    if isinstance(t, Succ):
        if infer(ctx, t.term) != NAT:
            raise TypeError("succ expects Nat")
        return NAT
    if isinstance(t, (TrueTerm, FalseTerm)): return BOOL
    raise TypeError(t)

def wf_type(ctx: Context, A: Ty) -> bool:
    try:
        if isinstance(A, (NatTy, BoolTy)):
            return True
        if isinstance(A, FinTy):
            return infer(ctx, A.index) == NAT
        return False
    except TypeError:
        return False

def wf_ctx(ctx: Context) -> bool:
    prefix: Context = []
    seen: set[str] = set()
    for x, A in ctx:
        if x in seen or not wf_type(prefix, A):
            return False
        prefix.append((x, A))
        seen.add(x)
    return True

# ---------- deterministic regression suite ----------
def numeral(n: int) -> Term:
    t: Term = Zero()
    for _ in range(n): t = Succ(t)
    return t

def composition_term(E: Term, a: Term, x: str, b: Term, y: str) -> tuple[Term, Term]:
    lhs = subst_term(subst_term(E, a, x), b, y)
    rhs = subst_term(subst_term(E, b, y), subst_term(a, b, y), x)
    return lhs, rhs

def composition_type(E: Ty, a: Term, x: str, b: Term, y: str) -> tuple[Ty, Ty]:
    lhs = subst_ty(subst_ty(E, a, x), b, y)
    rhs = subst_ty(subst_ty(E, b, y), subst_term(a, b, y), x)
    return lhs, rhs

def run_cases() -> dict:
    n = Var("n")
    dependent = [("n", NAT), ("i", FinTy(n)), ("j", FinTy(Succ(n)))]
    reversed_bad = [("i", FinTy(n)), ("n", NAT)]
    delta = [("i", FinTy(n)), ("j", FinTy(Succ(n)))]
    three = numeral(3)
    specialized = subst_trailing_context(delta, three, "n")

    E_term = Succ(Var("x"))
    a = Var("y")
    b = numeral(2)  # x is not free in b, satisfying the lemma's side condition.
    lhs_t, rhs_t = composition_term(E_term, a, "x", b, "y")

    E_ty = FinTy(Succ(Var("x")))
    lhs_A, rhs_A = composition_type(E_ty, a, "x", b, "y")

    cases = [
        {"name": "dependent_context_well_formed", "pass": wf_ctx(dependent), "actual": show_ctx(dependent)},
        {"name": "reversed_dependency_rejected", "pass": not wf_ctx(reversed_bad), "actual": show_ctx(reversed_bad)},
        {"name": "trailing_context_specializes", "pass": show_ctx(specialized) == ["i:Fin(succ(succ(succ(0))))", "j:Fin(succ(succ(succ(succ(0)))))"], "actual": show_ctx(specialized)},
        {"name": "specialized_context_well_formed", "pass": wf_ctx(specialized), "actual": show_ctx(specialized)},
        {"name": "family_formation_preserved", "pass": wf_type([], subst_ty(FinTy(Succ(n)), numeral(2), "n")), "actual": show_ty(subst_ty(FinTy(Succ(n)), numeral(2), "n"))},
        {"name": "substitution_composition_term", "pass": lhs_t == rhs_t, "lhs": show_term(lhs_t), "rhs": show_term(rhs_t)},
        {"name": "substitution_composition_type", "pass": lhs_A == rhs_A, "lhs": show_ty(lhs_A), "rhs": show_ty(rhs_A)},
    ]
    return {
        "calculus": "COMP-0",
        "purpose": "finite regression evidence for dependent family/context substitution",
        "claim_boundary": "passing cases are not a mechanized proof of generalized substitution",
        "cases": cases,
        "all_pass": all(c["pass"] for c in cases),
    }

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--evidence", default="evidence/family_substitution.json")
    args = ap.parse_args()
    result = run_cases()
    out = Path(args.evidence)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["all_pass"] else 1)

if __name__ == "__main__":
    main()
