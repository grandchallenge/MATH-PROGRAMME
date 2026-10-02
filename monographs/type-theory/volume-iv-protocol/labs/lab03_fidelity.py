#!/usr/bin/env python3
"""Finite principal-step fidelity checker for Volume IV."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Step:
    left: tuple
    right: tuple
    action: str

def dual(s):
    tag=s[0]
    if tag=="send": return ("recv",s[1],dual(s[2]))
    if tag=="recv": return ("send",s[1],dual(s[2]))
    if tag=="end!": return ("end?",)
    if tag=="end?": return ("end!",)
    raise ValueError(tag)

def advance_pair(a,b,action,payload=None):
    if b != dual(a): raise ValueError("nondual peers")
    if a[0]=="send" and action=="send/recv":
        if payload != a[1]: raise ValueError("payload mismatch")
        return a[2], b[2]
    if a[0]=="recv" and action=="recv/send":
        if payload != a[1]: raise ValueError("payload mismatch")
        return a[2], b[2]
    if a[0]=="end!" and action=="close/wait": return ("done",), ("done",)
    raise ValueError("action mismatch")

S=("send","Nat",("recv","Bool",("end!",)))
assert dual(dual(S)) == S
a,b=S,dual(S); a,b=advance_pair(a,b,"send/recv","Nat")
assert a==("recv","Bool",("end!",)) and b==("send","Bool",("end?",))
a,b=advance_pair(a,b,"recv/send","Bool"); a,b=advance_pair(a,b,"close/wait")
assert a==b==("done",)
hostile=0
for bad in [("send/recv","Bool"),("recv/send","Nat")]:
    try: advance_pair(S,dual(S),bad[0],bad[1])
    except ValueError: hostile+=1
assert hostile==2
print("PASS lab03_fidelity: principal evolution and hostile payload/action fixtures")
