#!/usr/bin/env python3
"""Finite falsification check for the 1978 triangle/star optimal-host family.

This is NOT a substitute for the published uniform-star lower bound.
No third-party packages or network access.
"""
from itertools import combinations
import json


def components(s, t, c):
    n = s + t - 1
    assert 0 <= c <= n
    comp = []
    v = 0
    for i in range(n):
        if i < c:
            comp.append([(v, v+1), (v+1, v+2), (v, v+2)])
            v += 3
        else:
            comp.append([(v, v+1), (v, v+2), (v, v+3)])
            v += 4
    return comp


def witness(edges, bits, colour):
    chosen = [e for i,e in enumerate(edges) if ((bits>>i)&1)==colour]
    return any(len(set(a)&set(b))==1 for a,b in combinations(chosen,2))


def case(s, t, c):
    parts = components(s,t,c)
    n = len(parts)
    for mask in range(1<<(3*n)):
        red=blue=0
        for j, es in enumerate(parts):
            part=(mask>>(3*j))&7
            red+=witness(es,part,1)
            blue+=witness(es,part,0)
        assert red>=s or blue>=t, (s,t,c,mask)
    # After removing any edge, construct the avoidance colouring explicitly:
    # split two surviving edges red/blue in broken component, and colour
    # s-1 intact components all red, t-1 intact components all blue.
    for deleted in range(3*n):
        broken=deleted//3; red_remaining=s-1
        R=B=0
        for j,es in enumerate(parts):
            if j==broken:
                surv=[x for i,x in enumerate(es) if i!=deleted%3]
                R+=witness(surv,1,1)
                B+=witness(surv,1,0)
            elif red_remaining:
                R+=witness(es,7,1);red_remaining-=1
            else:
                B+=witness(es,0,0)
        assert red_remaining==0 and R<s and B<t,(s,t,c,deleted,R,B)
    return (1<<(3*n),3*n)


def main():
    count=colourings=deleted_witnesses=0
    for s,t in [(2,2),(2,3),(3,2),(3,3)]:
        for c in range(s+t):
            a,b=case(s,t,c)
            colourings+=a;deleted_witnesses+=b;count+=1
    print(json.dumps({'status':'PASS','mixtures':count,
                      'colourings':colourings,
                      'edge_deletion_witnesses':deleted_witnesses},
                      sort_keys=True))


if __name__=='__main__':
    main()
