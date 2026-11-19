#!/usr/bin/env python3
"""Pure integer enumeration of 3×3 pairs not excluded by the degree-core gates."""
from itertools import combinations_with_replacement
from collections import Counter
import json

def weight(n,m):
    return sum(max(n[i]+m[k-i]-1 for i in range(len(n))
                   if 0<=k-i<len(m)) for k in range(len(n)+len(m)-1))
triples=[v[::-1] for v in combinations_with_replacement(range(1,10),3) if v[-1]>=2]
remaining=[]
stats=Counter()
for red in triples:
    for blue in triples:
        D=red[0]+blue[0]-2
        if D>=10:continue
        stats["small_pairs"]+=1
        W=weight(red,blue)
        e=W-1
        threshold=D*(D+1)//2
        if e<threshold:
            stats["edge_budget"]+=1
            continue
        order_r=sum(red)+3
        order_b=sum(blue)+3
        bound=2*e-D*D+1
        if max(order_r,order_b)>bound:
            stats["vertex_budget"]+=1
            continue
        if max(order_r,order_b)==bound and min(order_r,order_b)>D+1 and e-threshold<max(red[0],blue[0]):
            stats["equality_colouring"]+=1
            continue
        remaining.append({"red":red,"blue":blue,"D":D,"W":W,"edge_target":e})
stats["remaining"]=len(remaining)
assert dict(stats)=={"small_pairs":4566,"edge_budget":2725,"vertex_budget":918,"equality_colouring":72,"remaining":851},stats
print(json.dumps({"counts":dict(stats),"remaining":remaining},indent=2))
