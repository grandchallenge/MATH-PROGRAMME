#!/usr/bin/env python3
"""Generate and run a monitor for finite local sessions."""
def monitor(session,trace):
    s=session
    for ev in trace:
        tag=s[0]
        if tag in {"send","recv"}:
            if ev!=(tag,s[1]): return "REJECT"
            s=s[2]
        elif tag in {"end!","end?"}:
            expected=("close",None) if tag=="end!" else ("wait",None)
            if ev!=expected: return "REJECT"
            s=("done",)
        else: raise ValueError(tag)
    return "ACCEPT" if s==("done",) else "INCOMPLETE"
S=("send","Nat",("recv","Bool",("end!",)))
assert monitor(S,[("send","Nat"),("recv","Bool"),("close",None)])=="ACCEPT"
assert monitor(S,[("recv","Nat")])=="REJECT"
assert monitor(S,[("send","Nat")])=="INCOMPLETE"
print("PASS lab12_monitor: accepted, rejected, and incomplete observed traces")
