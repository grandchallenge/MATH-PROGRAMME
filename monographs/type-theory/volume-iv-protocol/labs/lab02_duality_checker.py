#!/usr/bin/env python3
"""Gate-1 Lab 02: finite session duality and peer compatibility."""
from protocol_core import parse_session, dual, pretty, compatible


def main():
    fixtures = [
        "send(Nat).recv(Bool).close",
        "recv(Nat).send(Bool).wait",
        "select{ok:send(Nat).close,err:close}",
        "branch{ok:recv(Nat).wait,err:wait}",
        "send(Unit).close",
        "recv(Unit).wait",
    ]
    for src in fixtures:
        s = parse_session(src)
        d = dual(s)
        dd = dual(d)
        print(f"involution {src} -> {pretty(d)} -> {pretty(dd)}")
        assert dd == s
        assert compatible(s, d)

    client = parse_session("send(Nat).recv(Bool).close")
    exact_peer = parse_session("recv(Nat).send(Bool).wait")
    same_direction = parse_session("send(Nat).recv(Bool).close")
    wrong_payload = parse_session("recv(Bool).send(Bool).wait")
    assert compatible(client, exact_peer)
    assert not compatible(client, same_direction)
    assert not compatible(client, wrong_payload)

    chooser = parse_session("select{ok:send(Nat).close,err:close}")
    offer = parse_session("branch{ok:recv(Nat).wait,err:wait}")
    missing_label = parse_session("branch{ok:recv(Nat).wait}")
    wrong_direction = parse_session("select{ok:recv(Nat).wait,err:wait}")
    assert compatible(chooser, offer)
    assert not compatible(chooser, missing_label)
    assert not compatible(chooser, wrong_direction)

    print("LAB02_RESULT=PASS involution_fixtures=6 hostile_peer_fixtures=5")


if __name__ == "__main__":
    main()
