#!/usr/bin/env python3
"""Independent finite parameter certificate for the Erdős #561 joint 3×3 theorem.
Pure Python. General unbounded reduction is in JOINT_3x3_AND_DEGREE_CORE_PROOF.md.
"""
from itertools import combinations_with_replacement
import json

def diagonals(n,m):
    return [max(n[i]+m[k-i]-1 for i in range(len(n))
                if 0 <= k-i < len(m))
            for k in range(len(n)+len(m)-1)]

triples=[x[::-1] for x in combinations_with_replacement(range(1,8),3)]
assert len(triples)==84
stats={"positive_switch_degree_le7":0,"excluded_by_edges":0,"excluded_by_vertices":0}
exceptions=[]
for red in triples:
    for blue in triples:
        w=diagonals(red,blue)
        J=sum(w[1:])
        separate=max(sum(diagonals(red[1:],blue)),sum(diagonals(red,blue[1:])))
        sigma=J-separate
        assert sigma>=0
        if not sigma:continue
        d=w[1]-1
        assert max(red[0],blue[0])<=d
        if d>7:continue
        stats["positive_switch_degree_le7"]+=1
        tail=sum(w[2:])
        assert tail==max(sum(diagonals(red[2:],blue)),
                         sum(diagonals(red[1:],blue[1:])),
                         sum(diagonals(red,blue[2:])))
        assert J-1==d+tail
        e=J-1
        if e<d*(d+1)//2:
            stats["excluded_by_edges"]+=1
            continue
        required=max(sum(red)+3,sum(blue)+3)
        bound=2*e-d*d+1
        assert required>bound,(red,blue,e,d,required,bound)
        stats["excluded_by_vertices"]+=1
        exceptions.append({"red":red,"blue":blue,"edges":e,"D":d,
                           "required_order":required,"allowed_order":bound})
assert stats=={"positive_switch_degree_le7":82,"excluded_by_edges":74,"excluded_by_vertices":8}
print(json.dumps({"stats":stats,"exceptions":exceptions},indent=2))
