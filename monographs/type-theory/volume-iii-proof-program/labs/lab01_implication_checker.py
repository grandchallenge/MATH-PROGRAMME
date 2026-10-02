#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
import json

class Type: pass
@dataclass(frozen=True)
class Atom(Type):
    name: str
    def __str__(self): return self.name
@dataclass(frozen=True)
class Arrow(Type):
    dom: Type; cod: Type
    def __str__(self): return f"({self.dom} -> {self.cod})"
class Term: pass
@dataclass(frozen=True)
class Var(Term):
    name: str
    def __str__(self): return self.name
@dataclass(frozen=True)
class Lam(Term):
    var: str; var_type: Type; body: Term
    def __str__(self): return f"(lam {self.var}:{self.var_type}. {self.body})"
@dataclass(frozen=True)
class App(Term):
    fn: Term; arg: Term
    def __str__(self): return f"({self.fn} {self.arg})"
class ParseError(ValueError): pass
class TypeErrorCH(ValueError): pass

def tokenize(src: str) -> list[str]: return src.replace("("," ( ").replace(")"," ) ").split()
def _sexpr(tokens: list[str], i: int=0):
    if i>=len(tokens): raise ParseError("unexpected end of input")
    tok=tokens[i]
    if tok!="(": return tok,i+1
    out=[]; i+=1
    while True:
        if i>=len(tokens): raise ParseError("missing ')'")
        if tokens[i]==")": return out,i+1
        node,i=_sexpr(tokens,i); out.append(node)
def parse_sexpr(src: str):
    tokens=tokenize(src); node,i=_sexpr(tokens)
    if i!=len(tokens): raise ParseError("trailing tokens")
    return node
def parse_type_node(node) -> Type:
    if isinstance(node,str):
        if node in {"lam","app","->"}: raise ParseError(f"reserved type token {node!r}")
        return Atom(node)
    if len(node)==3 and node[0]=="->": return Arrow(parse_type_node(node[1]),parse_type_node(node[2]))
    raise ParseError(f"bad type expression: {node!r}")
def parse_term_node(node) -> Term:
    if isinstance(node,str): return Var(node)
    if len(node)==4 and node[0]=="lam" and isinstance(node[1],str): return Lam(node[1],parse_type_node(node[2]),parse_term_node(node[3]))
    if len(node)==3 and node[0]=="app": return App(parse_term_node(node[1]),parse_term_node(node[2]))
    raise ParseError(f"bad term expression: {node!r}")
def parse_type(src: str) -> Type: return parse_type_node(parse_sexpr(src))
def parse_term(src: str) -> Term: return parse_term_node(parse_sexpr(src))
def infer(term: Term, ctx: Mapping[str,Type]) -> Type:
    if isinstance(term,Var):
        if term.name not in ctx: raise TypeErrorCH(f"unbound variable {term.name!r}")
        return ctx[term.name]
    if isinstance(term,Lam):
        ext=dict(ctx); ext[term.var]=term.var_type
        return Arrow(term.var_type,infer(term.body,ext))
    if isinstance(term,App):
        fn_ty=infer(term.fn,ctx); arg_ty=infer(term.arg,ctx)
        if not isinstance(fn_ty,Arrow): raise TypeErrorCH(f"application head has non-arrow type {fn_ty}")
        if fn_ty.dom!=arg_ty: raise TypeErrorCH(f"application expected {fn_ty.dom}, got {arg_ty}")
        return fn_ty.cod
    raise AssertionError(term)
def check(term: Term, expected: Type, ctx: Mapping[str,Type]|None=None) -> None:
    actual=infer(term,{} if ctx is None else ctx)
    if actual!=expected: raise TypeErrorCH(f"expected {expected}, inferred {actual}")
def run_fixtures() -> dict:
    fixtures=[
      ("identity","(lam x P x)","(-> P P)",True),
      ("k","(lam x P (lam y Q x))","(-> P (-> Q P))",True),
      ("compose","(lam f (-> Q R) (lam g (-> P Q) (lam x P (app f (app g x)))))","(-> (-> Q R) (-> (-> P Q) (-> P R)))",True),
      ("bad-argument","(app (lam x P x) (lam y Q y))",None,False),
      ("unbound","z",None,False)]
    results=[]
    for name,term_src,expected_src,should_pass in fixtures:
        try:
            term=parse_term(term_src); ty=infer(term,{})
            if expected_src is not None and ty!=parse_type(expected_src): raise TypeErrorCH(f"fixture expected {expected_src}, got {ty}")
            passed=True; detail=str(ty)
        except (ParseError,TypeErrorCH) as exc:
            passed=False; detail=str(exc)
        results.append({"name":name,"expected_accept":should_pass,"accepted":passed,"detail":detail})
    ok=all(r["expected_accept"]==r["accepted"] for r in results)
    return {"calculus":"CH-0 implication fragment","ok":ok,"fixtures":results}
if __name__=="__main__":
    report=run_fixtures(); print(json.dumps(report,indent=2)); raise SystemExit(0 if report["ok"] else 1)
