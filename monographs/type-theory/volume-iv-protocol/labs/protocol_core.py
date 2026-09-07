#!/usr/bin/env python3
"""Finite session-type parser and trace checker for Type Theory Volume IV Gate 1.

This module implements only the bounded PROTO-0 teaching syntax used in Chapters 1-2.
It is executable evidence, not a proof of the volume's metatheory.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple

class ParseError(ValueError):
    pass

@dataclass(frozen=True)
class Session:
    pass

@dataclass(frozen=True)
class Send(Session):
    payload: str
    cont: Session

@dataclass(frozen=True)
class Recv(Session):
    payload: str
    cont: Session

@dataclass(frozen=True)
class Select(Session):
    branches: Tuple[Tuple[str, Session], ...]

@dataclass(frozen=True)
class Branch(Session):
    branches: Tuple[Tuple[str, Session], ...]

@dataclass(frozen=True)
class Close(Session):
    pass

@dataclass(frozen=True)
class Wait(Session):
    pass


def _canonical_branches(items: Iterable[tuple[str, Session]]) -> Tuple[Tuple[str, Session], ...]:
    items = tuple(sorted(items, key=lambda kv: kv[0]))
    labels = [k for k, _ in items]
    if len(labels) != len(set(labels)):
        raise ParseError("duplicate branch label")
    if not items:
        raise ParseError("empty branch set")
    return items


class Parser:
    def __init__(self, text: str):
        self.text = "".join(text.split())
        self.i = 0

    def peek(self) -> str:
        return self.text[self.i:self.i+1]

    def consume(self, token: str) -> None:
        if not self.text.startswith(token, self.i):
            got = self.text[self.i:self.i+max(1,len(token))]
            raise ParseError(f"expected {token!r} at offset {self.i}, got {got!r}")
        self.i += len(token)

    def ident(self) -> str:
        start = self.i
        if self.i >= len(self.text) or not (self.text[self.i].isalpha() or self.text[self.i] == '_'):
            raise ParseError(f"expected identifier at offset {self.i}")
        self.i += 1
        while self.i < len(self.text) and (self.text[self.i].isalnum() or self.text[self.i] in "_-'" ):
            self.i += 1
        return self.text[start:self.i]

    def session(self) -> Session:
        if self.text.startswith("send(", self.i):
            self.consume("send(")
            p = self.ident()
            self.consume(").")
            return Send(p, self.session())
        if self.text.startswith("recv(", self.i):
            self.consume("recv(")
            p = self.ident()
            self.consume(").")
            return Recv(p, self.session())
        if self.text.startswith("select{", self.i):
            self.consume("select{")
            return Select(self.branch_items())
        if self.text.startswith("branch{", self.i):
            self.consume("branch{")
            return Branch(self.branch_items())
        if self.text.startswith("close", self.i):
            self.consume("close")
            return Close()
        if self.text.startswith("wait", self.i):
            self.consume("wait")
            return Wait()
        raise ParseError(f"unknown session constructor at offset {self.i}: {self.text[self.i:self.i+20]!r}")

    def branch_items(self) -> Tuple[Tuple[str, Session], ...]:
        out: list[tuple[str, Session]] = []
        while True:
            label = self.ident()
            self.consume(":")
            out.append((label, self.session()))
            if self.peek() == ",":
                self.consume(",")
                continue
            self.consume("}")
            return _canonical_branches(out)


def parse_session(text: str) -> Session:
    p = Parser(text)
    s = p.session()
    if p.i != len(p.text):
        raise ParseError(f"trailing input at offset {p.i}: {p.text[p.i:]!r}")
    return s


def dual(s: Session) -> Session:
    if isinstance(s, Send):
        return Recv(s.payload, dual(s.cont))
    if isinstance(s, Recv):
        return Send(s.payload, dual(s.cont))
    if isinstance(s, Select):
        return Branch(_canonical_branches((l, dual(t)) for l, t in s.branches))
    if isinstance(s, Branch):
        return Select(_canonical_branches((l, dual(t)) for l, t in s.branches))
    if isinstance(s, Close):
        return Wait()
    if isinstance(s, Wait):
        return Close()
    raise TypeError(s)


def pretty(s: Session) -> str:
    if isinstance(s, Send):
        return f"send({s.payload}).{pretty(s.cont)}"
    if isinstance(s, Recv):
        return f"recv({s.payload}).{pretty(s.cont)}"
    if isinstance(s, Select):
        return "select{" + ",".join(f"{l}:{pretty(t)}" for l,t in s.branches) + "}"
    if isinstance(s, Branch):
        return "branch{" + ",".join(f"{l}:{pretty(t)}" for l,t in s.branches) + "}"
    if isinstance(s, Close):
        return "close"
    if isinstance(s, Wait):
        return "wait"
    raise TypeError(s)


def compatible(a: Session, b: Session) -> bool:
    return dual(a) == b


def advance(s: Session, event: str) -> Session | None:
    """Consume one local trace event. Return continuation, or None after terminal event."""
    if isinstance(s, Send):
        if event != f"send:{s.payload}":
            raise ValueError(f"expected send:{s.payload}, got {event}")
        return s.cont
    if isinstance(s, Recv):
        if event != f"recv:{s.payload}":
            raise ValueError(f"expected recv:{s.payload}, got {event}")
        return s.cont
    if isinstance(s, Select):
        prefix = "select:"
        if not event.startswith(prefix):
            raise ValueError(f"expected selection, got {event}")
        label = event[len(prefix):]
        table = dict(s.branches)
        if label not in table:
            raise ValueError(f"unknown selection label {label!r}")
        return table[label]
    if isinstance(s, Branch):
        prefix = "branch:"
        if not event.startswith(prefix):
            raise ValueError(f"expected offered branch, got {event}")
        label = event[len(prefix):]
        table = dict(s.branches)
        if label not in table:
            raise ValueError(f"unknown branch label {label!r}")
        return table[label]
    if isinstance(s, Close):
        if event != "close":
            raise ValueError(f"expected close, got {event}")
        return None
    if isinstance(s, Wait):
        if event != "wait":
            raise ValueError(f"expected wait, got {event}")
        return None
    raise TypeError(s)


def validate_trace(s: Session, events: Iterable[str]) -> tuple[bool, str]:
    state: Session | None = s
    try:
        for i, event in enumerate(events, start=1):
            if state is None:
                return False, f"event {i}: trailing event after protocol termination: {event}"
            state = advance(state, event)
        if state is None:
            return True, "accepted"
        return False, f"trace ended before protocol termination; residual={pretty(state)}"
    except ValueError as exc:
        return False, str(exc)
