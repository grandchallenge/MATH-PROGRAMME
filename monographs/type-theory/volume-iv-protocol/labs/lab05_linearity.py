#!/usr/bin/env python3
"""Finite linear-environment split checker."""
def check_split(delta,left,right):
    D=set(delta); L=set(left); R=set(right)
    if L & R: return False,"duplicated"
    if (L|R)!=D:
        if (L|R)<D: return False,"dropped"
        return False,"invented"
    return True,"ok"
D={"x":"S","y":"T","z":"U"}
assert check_split(D,{"x":"S"},{"y":"T","z":"U"})==(True,"ok")
assert check_split(D,{"x":"S","y":"T"},{"y":"T","z":"U"})==(False,"duplicated")
assert check_split(D,{"x":"S"},{"y":"T"})==(False,"dropped")
assert check_split(D,{"x":"S"},{"y":"T","z":"U","w":"V"})==(False,"invented")
print("PASS lab05_linearity: exact split, duplicate, drop, and invention fixtures")
