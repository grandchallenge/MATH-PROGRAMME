#!/usr/bin/env python3
"""Bounded typed FIFO simulator for PROTO-A1 teaching fragment."""
from collections import deque
class Queue:
    def __init__(self,limit=4): self.q=deque(); self.limit=limit
    def send(self,kind,value):
        if len(self.q)>=self.limit: raise OverflowError("queue full")
        self.q.append((kind,value))
    def recv(self,kind):
        if not self.q: raise IndexError("empty")
        k,v=self.q[0]
        if k!=kind: raise TypeError(f"expected {kind}, found {k}")
        self.q.popleft(); return v
q=Queue(3); q.send("Nat",7); q.send("Bool",True)
assert list(q.q)==[("Nat",7),("Bool",True)] and q.recv("Nat")==7 and q.recv("Bool") is True and not q.q
q.send("Nat",9)
try: q.recv("Bool"); raise AssertionError("wrong-head type accepted")
except TypeError: pass
assert list(q.q)==[("Nat",9)]
print("PASS lab08_async: FIFO, typing, mismatch, and orphan-state diagnostics")
