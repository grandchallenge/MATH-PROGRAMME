#!/usr/bin/env python3
"""Wait-for graph witness for locally compatible multi-session deadlock."""
def dual_action(a): return {"send":"recv","recv":"send","close":"wait","wait":"close"}[a]
session_a={"P":"send","Q":"recv"}; session_b={"P":"recv","Q":"send"}
assert session_a["Q"]==dual_action(session_a["P"]); assert session_b["Q"]==dual_action(session_b["P"])
front={"P":("recv","b","Q"),"Q":("recv","a","P")}; wait_for={p:{peer} for p,(_,_,peer) in front.items()}
def has_cycle(graph):
    visiting=set(); done=set()
    def dfs(v):
        if v in visiting: return True
        if v in done: return False
        visiting.add(v)
        for w in graph.get(v,()):
            if dfs(w): return True
        visiting.remove(v); done.add(v); return False
    return any(dfs(v) for v in graph)
assert has_cycle(wait_for); assert not any(front[p][0]=="send" for p in front)
print("PASS lab06_deadlock: local duality holds; wait-for cycle detected; no exposed send")
