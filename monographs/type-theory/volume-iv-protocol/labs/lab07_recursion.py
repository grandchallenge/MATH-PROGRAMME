#!/usr/bin/env python3
"""Guarded recursive-session checker and bounded unfolding."""
def guarded(expr,var="t",under_prefix=False):
    tag=expr[0]
    if tag=="var": return expr[1]!=var or under_prefix
    if tag in {"send","recv"}: return guarded(expr[2],var,True)
    if tag in {"end!","end?"}: return True
    if tag=="mu": return guarded(expr[2],expr[1],False)
    raise ValueError(tag)
def subst(expr,var,repl):
    tag=expr[0]
    if tag=="var": return repl if expr[1]==var else expr
    if tag in {"send","recv"}: return (tag,expr[1],subst(expr[2],var,repl))
    if tag in {"end!","end?"}: return expr
    if tag=="mu": return expr if expr[1]==var else ("mu",expr[1],subst(expr[2],var,repl))
    raise ValueError(tag)
def unfold(mu): assert mu[0]=="mu"; return subst(mu[2],mu[1],mu)
good=("mu","t",("recv","Nat",("send","Bool",("var","t")))); bad=("mu","t",("var","t"))
assert guarded(good) and not guarded(bad)
u=unfold(good); assert u[0]=="recv" and u[2][0]=="send" and u[2][2]==good
print("PASS lab07_recursion: guardedness and bounded unfolding fixtures")
