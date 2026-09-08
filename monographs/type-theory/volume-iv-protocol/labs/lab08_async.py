#!/usr/bin/env python3
"""Bounded typed FIFO simulator for the PROTO-A1 teaching fragment."""

from collections import deque


class Config:
    def __init__(self, protocol=("Nat", "Bool"), limit=4):
        self.protocol = tuple(protocol)
        self.sender_i = 0
        self.receiver_i = 0
        self.q = deque()
        self.limit = limit
        self.peer_alive = True

    def consistent(self):
        if not (0 <= self.receiver_i <= self.sender_i <= len(self.protocol)):
            return False
        pending = self.protocol[self.receiver_i:self.sender_i]
        queued = tuple(kind for kind, _ in self.q)
        return queued == pending

    def send(self, kind, value):
        assert self.consistent()
        if len(self.q) >= self.limit:
            raise OverflowError("queue full")
        if self.sender_i >= len(self.protocol):
            raise ValueError("sender protocol exhausted")
        expected = self.protocol[self.sender_i]
        if kind != expected:
            raise TypeError(f"sender expected {expected}, got {kind}")
        self.q.append((kind, value))
        self.sender_i += 1
        assert self.consistent()

    def recv(self, kind):
        assert self.consistent()
        if not self.q:
            raise IndexError("empty")
        expected = self.protocol[self.receiver_i]
        queued_kind, value = self.q[0]
        if kind != expected or queued_kind != expected:
            raise TypeError(f"receiver expected {expected}, found {queued_kind}")
        self.q.popleft()
        self.receiver_i += 1
        assert self.consistent()
        return value

    def orphaned(self):
        return (not self.peer_alive) and bool(self.q)


c = Config(limit=3)
assert c.consistent()
c.send("Nat", 7)
assert c.consistent() and list(c.q) == [("Nat", 7)]
c.send("Bool", True)
assert c.consistent() and list(c.q) == [("Nat", 7), ("Bool", True)]
assert c.recv("Nat") == 7 and c.consistent()
assert c.recv("Bool") is True and c.consistent() and not c.q

wrong = Config(protocol=("Nat",), limit=2)
wrong.send("Nat", 9)
snapshot = (wrong.sender_i, wrong.receiver_i, tuple(wrong.q))
try:
    wrong.recv("Bool")
    raise AssertionError("wrong-head type accepted")
except TypeError:
    pass
assert snapshot == (wrong.sender_i, wrong.receiver_i, tuple(wrong.q))
assert wrong.consistent()

bounded = Config(protocol=("Nat", "Bool"), limit=1)
bounded.send("Nat", 1)
try:
    bounded.send("Bool", True)
    raise AssertionError("bounded overflow accepted")
except OverflowError:
    pass
assert bounded.consistent() and list(bounded.q) == [("Nat", 1)]

orphan = Config(protocol=("Nat",), limit=1)
orphan.send("Nat", 42)
orphan.peer_alive = False
assert orphan.consistent() and orphan.orphaned()

print("PASS lab08_async: FIFO, typing, queue consistency, bounded growth, and orphan diagnostics")
