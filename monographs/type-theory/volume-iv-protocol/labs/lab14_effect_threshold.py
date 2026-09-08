#!/usr/bin/env python3
"""Show that protocol projection can erase materially different world effects."""
def protocol_projection(events): return [e for e in events if e[0] in {"send","recv","close","wait"}]
good=[("send",("Nat",42)),("effect",("debit",42)),("recv",("Bool",True)),("close",None)]
bug=[("send",("Nat",42)),("effect",("debit",84)),("recv",("Bool",True)),("close",None)]
assert protocol_projection(good)==protocol_projection(bug) and good!=bug
print("PASS lab14_effect_threshold: identical protocol projection, distinct external effect trace")
