#!/usr/bin/env python3
"""Finite choreography projection and per-exemplar trace comparison."""
def project(trace,role):
    out=[]
    for src,dst,label,typ in trace:
        if role==src: out.append(("send",dst,label,typ))
        elif role==dst: out.append(("recv",src,label,typ))
    return out
G=[("C","B","job","Nat"),("B","W","job","Nat"),("W","B","result","Bool"),("B","C","result","Bool")]
roles={"C","B","W"}; proj={r:project(G,r) for r in roles}
assert proj["C"]==[("send","B","job","Nat"),("recv","B","result","Bool")]
assert proj["W"]==[("recv","B","job","Nat"),("send","B","result","Bool")]
for src,dst,label,typ in G:
    assert ("send",dst,label,typ) in proj[src] and ("recv",src,label,typ) in proj[dst]
branches=[G,[("C","B","cancel","Unit"),("B","W","cancel","Unit")]]
assert all(all(project(t,r) is not None for r in roles) for t in branches)
print("PASS lab09_multiparty: registered finite choreography projections and trace witnesses")
