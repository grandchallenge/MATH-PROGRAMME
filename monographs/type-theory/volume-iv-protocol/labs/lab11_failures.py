#!/usr/bin/env python3
"""Classify deployment faults as changes to the core communication model."""
VALID=[("send","Nat"),("recv","Bool"),("close",None)]
def inject(trace,kind):
    t=list(trace)
    if kind=="loss": return t[1:]
    if kind=="duplication": return [t[0],t[0]]+t[1:]
    if kind=="reordering": return [t[1],t[0],*t[2:]]
    if kind=="crash": return t[:1]+[("crash",None)]
    if kind=="timeout": return [("timeout",None)]+t
    raise ValueError(kind)
classes={"loss":"reliable-delivery assumption","duplication":"exactly-once/FIFO message assumption","reordering":"FIFO/order assumption","crash":"peer-presence transition system","timeout":"untimed semantics"}
for k in classes: assert inject(VALID,k)!=VALID
print("PASS lab11_failures:",", ".join(f"{k}->{v}" for k,v in classes.items()))
