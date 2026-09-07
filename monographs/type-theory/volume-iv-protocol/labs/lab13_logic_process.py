#!/usr/bin/env python3
"""Claim-discipline table for proof/process correspondences."""
rows=[("linear resource","single-use session obligation","structural-analogy"),("cut/composition","private channel connection","exact-in-cited-calculi"),("linear negation","session duality","not-established-for-PROTO-0")]
allowed={"structural-analogy","exact-in-cited-calculi","not-established-for-PROTO-0"}
assert all(status in allowed for _,_,status in rows)
assert not any(a=="linear negation" and status=="exact-in-cited-calculi" for a,_,status in rows)
print("PASS lab13_logic_process: correspondence claims carry explicit authority tags")
