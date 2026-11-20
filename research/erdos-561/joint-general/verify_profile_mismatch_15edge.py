#!/usr/bin/env python3
"""Independent COMPLETE finite graph checker for the 15-edge equality
case n=(3,1,1),m=(5,2,2,1). Every candidate admits a fixed explicit
A-avoiding colouring: colour every edge touching first hub 8 red.
Verify the blue graph cannot have the complete F(5,2,2,1) edge forest.
"""
from collections import Counter
from itertools import combinations
import json,hashlib
from pathlib import Path

base=((0,1),(0,2),(0,3),(4,5),(6,7))
subsets=[tuple(s) for k in range(6) for s in combinations(range(8),k)]

def make(A,B,h):
    edges=list(base)
    edges.extend((8,v) for v in A)
    edges.extend((9,v) for v in B)
    next_vertex=10
    for i in range(h):
        edges.extend(((8,next_vertex),(9,next_vertex)))
        next_vertex+=1
    for i in range(5-len(A)-h):
        edges.append((8,next_vertex));next_vertex+=1
    for i in range(5-len(B)-h):
        edges.append((9,next_vertex));next_vertex+=1
    assert len(edges)==15 and len({frozenset(e) for e in edges})==15
    assert sum(8 in e for e in edges)==5 and sum(9 in e for e in edges)==5
    assert (8,9) not in edges
    return edges

def component_star_sizes(edges):
    graph={}
    for x,y in edges:
        graph.setdefault(x,set()).add(y)
        graph.setdefault(y,set()).add(x)
    leftover=set(graph)
    sizes=[]
    while leftover:
        vertex=next(iter(leftover))
        connected={vertex};frontier=[vertex]
        for v in frontier:
            for w in graph[v]:
                if w not in connected:
                    connected.add(w);frontier.append(w)
        leftover-=connected
        number_edges=sum(len(graph[v]) for v in connected)//2
        if number_edges<1 or number_edges!=len(connected)-1 or max(len(graph[v]) for v in connected)!=number_edges:
            return None
        sizes.append(number_edges)
    return sorted(sizes,reverse=True)

count=Counter();red_degree_failures=0;digest=hashlib.sha256()
for A in subsets:
    for B in subsets:
        for h in range(min(5-len(A),5-len(B))+1):
            edges=make(A,B,h)
            count['all_equality_descriptions']+=1
            blue=[e for e in edges if 8 not in e]
            red=[e for e in edges if 8 in e]
            assert len(blue)==10 and len(red)==5
            assert len({x for e in red for x in e})==6
            profile=component_star_sizes(blue)
            if profile==[5,2,2,1]:
                raise AssertionError(('UNEXPECTED_FULL_BLUE_F5221',A,B,h,edges))
            if profile is None:count['blue_not_star_forest']+=1
            else:count['blue_wrong_star_partition']+=1
            digest.update(bytes([len(A),len(B),h])+bytes(A)+b'|'+bytes(B)+b'\n')
assert count['all_equality_descriptions']==84630,count
assert count['blue_not_star_forest']+count['blue_wrong_star_partition']==84630
print('RIGID15_PROFILE_MISMATCH_PYTHON_COMPLETE_PASS',dict(count))
Path(__file__).with_name('RIGID_15EDGE_MISMATCH_CERTIFICATE.json').write_text(json.dumps({
    'record_type':'ERDOS561_RIGID15_PROFILE_MISMATCH_EXACT_CERTIFICATE/1',
    'original_red':[3,1,1],'original_blue':[5,2,2,1],
    'forced_edge_budget':15,'all_possible_attachment_descriptions':84630,
    'classification':dict(count),
    'generation_order_sha256':digest.hexdigest(),
    'explicit_coloring':'Every edge at hub vertex 8 is red; all other edges blue. Red is K1,5; blue has ten edges but is never exactly F(5,2,2,1).',
    'all_full_equality_hosts_A_avoided':True,
    'full_general_joint_residual_hypothesis_proved':False},indent=2)+'\n')
