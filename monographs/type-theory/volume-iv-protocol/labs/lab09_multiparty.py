#!/usr/bin/env python3
"""Finite choreography projection with exhaustive synchronized reconstruction."""

from functools import lru_cache


def project(trace, role):
    out = []
    for src, dst, label, typ in trace:
        if role == src:
            out.append(("send", dst, label, typ))
        elif role == dst:
            out.append(("recv", src, label, typ))
    return tuple(out)


def synchronized_traces(projected):
    roles = tuple(sorted(projected))
    initial = tuple(projected[r] for r in roles)

    @lru_cache(maxsize=None)
    def explore(state):
        if all(not actions for actions in state):
            return {()}

        results = set()
        for i, src in enumerate(roles):
            actions = state[i]
            if not actions:
                continue
            head = actions[0]
            if head[0] != "send":
                continue

            _, dst, label, typ = head
            if dst not in projected:
                continue
            j = roles.index(dst)
            peer_actions = state[j]
            expected = ("recv", src, label, typ)
            if not peer_actions or peer_actions[0] != expected:
                continue

            next_state = list(state)
            next_state[i] = actions[1:]
            next_state[j] = peer_actions[1:]
            event = (src, dst, label, typ)
            for suffix in explore(tuple(next_state)):
                results.add((event,) + suffix)
        return results

    return explore(initial)


REGISTERED = {
    "job": (
        ("C", "B", "job", "Nat"),
        ("B", "W", "job", "Nat"),
        ("W", "B", "result", "Bool"),
        ("B", "C", "result", "Bool"),
    ),
    "cancel": (
        ("C", "B", "cancel", "Unit"),
        ("B", "W", "cancel", "Unit"),
    ),
}

roles = {"C", "B", "W"}
checked = 0
for name, trace in REGISTERED.items():
    projected = {r: project(trace, r) for r in roles}
    reconstructed = synchronized_traces(projected)
    expected = {tuple(trace)}
    assert reconstructed == expected, (name, reconstructed, expected)
    for src, dst, label, typ in trace:
        assert ("send", dst, label, typ) in projected[src]
        assert ("recv", src, label, typ) in projected[dst]
    checked += 1

print(
    f"PASS lab09_multiparty: exhaustive synchronized trace-set equality "
    f"for registered_exemplars={checked}"
)
