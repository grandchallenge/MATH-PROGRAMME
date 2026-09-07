#!/usr/bin/env python3
"""Finite branch/selection compatibility explorer."""
def synchronize(selector,offerer,label):
    if label not in selector: raise ValueError("selector cannot choose label")
    if label not in offerer: raise ValueError("peer does not offer selected label")
    return selector[label],offerer[label]
sel={"ok":"?Nat.end!","cancel":"end!"}; offer={"ok":"!Nat.end?","cancel":"end?","help":"!Bool.end?"}
assert synchronize(sel,offer,"ok")== ("?Nat.end!","!Nat.end?")
assert synchronize(sel,offer,"cancel")== ("end!","end?")
try:
    synchronize(sel,{"cancel":"end?"},"ok"); raise AssertionError("missing-label fixture accepted")
except ValueError: pass
print("PASS lab04_branching: compatible selections accepted; missing-label peer rejected")
