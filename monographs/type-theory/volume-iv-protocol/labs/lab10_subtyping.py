#!/usr/bin/env python3
"""Finite synchronous session subtyping with invariant payloads."""
def leq(s,t):
    if s[0]!=t[0]: return False
    tag=s[0]
    if tag in {"end!","end?"}: return True
    if tag in {"send","recv"}: return s[1]==t[1] and leq(s[2],t[2])
    if tag=="select":
        S,T=s[1],t[1]; return set(S)<=set(T) and all(leq(S[k],T[k]) for k in S)
    if tag=="branch":
        S,T=s[1],t[1]; return set(T)<=set(S) and all(leq(S[k],T[k]) for k in T)
    raise ValueError(tag)
E=("end!",)
assert leq(("select",{"a":E}),("select",{"a":E,"b":E}))
assert not leq(("select",{"a":E,"b":E}),("select",{"a":E}))
assert leq(("branch",{"a":E,"b":E}),("branch",{"a":E}))
assert not leq(("branch",{"a":E}),("branch",{"a":E,"b":E}))
assert leq(("send","Nat",E),("send","Nat",E)) and not leq(("send","Bool",E),("send","Nat",E))
print("PASS lab10_subtyping: select-less/offer-more width and invariant payload fixtures")
