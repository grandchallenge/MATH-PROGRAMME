#!/usr/bin/env python3
"""Gate-1 Lab 01: finite protocol trace validation with hostile fixtures."""
from protocol_core import parse_session, validate_trace


def expect(name, protocol, trace, accepted):
    s = parse_session(protocol)
    ok, reason = validate_trace(s, trace)
    print(f"{name}: {'PASS' if ok == accepted else 'FAIL'} | observed={ok} expected={accepted} | {reason}")
    assert ok == accepted, (name, reason)


def main():
    proto = "send(Nat).recv(Bool).close"
    expect("nominal", proto, ["send:Nat", "recv:Bool", "close"], True)
    expect("wrong_order", proto, ["recv:Bool", "send:Nat", "close"], False)
    expect("wrong_payload", proto, ["send:Bool", "recv:Bool", "close"], False)
    expect("premature_end", proto, ["send:Nat"], False)
    expect("trailing_event", proto, ["send:Nat", "recv:Bool", "close", "send:Nat"], False)

    branch_proto = "select{ok:send(Nat).close,err:close}"
    expect("branch_nominal", branch_proto, ["select:ok", "send:Nat", "close"], True)
    expect("branch_unknown_label", branch_proto, ["select:retry", "close"], False)
    expect("branch_wrong_continuation", branch_proto, ["select:err", "send:Nat", "close"], False)
    print("LAB01_RESULT=PASS fixtures=8")


if __name__ == "__main__":
    main()
