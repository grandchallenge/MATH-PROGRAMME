#!/usr/bin/env python3
"""Generate and run a monitor for finite local sessions with choice."""

def monitor(session, trace):
    s = session
    for ev in trace:
        tag = s[0]
        if tag in {"send", "recv"}:
            if ev != (tag, s[1]):
                return "REJECT"
            s = s[2]
        elif tag in {"select", "branch"}:
            if not (isinstance(ev, tuple) and len(ev) == 2 and ev[0] == tag):
                return "REJECT"
            label = ev[1]
            branches = s[1]
            if label not in branches:
                return "REJECT"
            s = branches[label]
        elif tag in {"end!", "end?"}:
            expected = ("close", None) if tag == "end!" else ("wait", None)
            if ev != expected:
                return "REJECT"
            s = ("done",)
        else:
            raise ValueError(tag)
    return "ACCEPT" if s == ("done",) else "INCOMPLETE"


E_OUT = ("end!",)
E_IN = ("end?",)
S = ("send", "Nat", ("recv", "Bool", E_OUT))
assert monitor(S, [("send", "Nat"), ("recv", "Bool"), ("close", None)]) == "ACCEPT"
assert monitor(S, [("recv", "Nat")]) == "REJECT"
assert monitor(S, [("send", "Nat")]) == "INCOMPLETE"

SELECT = ("select", {
    "ok": ("send", "Nat", E_OUT),
    "cancel": E_OUT,
})
assert monitor(SELECT, [("select", "ok"), ("send", "Nat"), ("close", None)]) == "ACCEPT"
assert monitor(SELECT, [("select", "cancel"), ("close", None)]) == "ACCEPT"
assert monitor(SELECT, [("select", "retry"), ("close", None)]) == "REJECT"

BRANCH = ("branch", {
    "ok": ("recv", "Nat", E_IN),
    "cancel": E_IN,
})
assert monitor(BRANCH, [("branch", "ok"), ("recv", "Nat"), ("wait", None)]) == "ACCEPT"
assert monitor(BRANCH, [("branch", "cancel"), ("wait", None)]) == "ACCEPT"

observed = [("send", "Nat"), ("recv", "Bool"), ("close", None)]
execution_with_hidden_failure = [
    ("send", "Nat"),
    ("hidden", "transport-retry"),
    ("recv", "Bool"),
    ("close", None),
]
projection = [e for e in execution_with_hidden_failure if e[0] != "hidden"]
assert projection == observed
assert execution_with_hidden_failure != observed
assert monitor(S, observed) == "ACCEPT"

print(
    "PASS lab12_monitor: accepted, rejected, incomplete, choice, "
    "and unobservable-boundary fixtures"
)
