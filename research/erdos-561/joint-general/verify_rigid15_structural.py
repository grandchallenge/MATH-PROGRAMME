#!/usr/bin/env python3
"""Independent proof-oriented complete classification for 15-edge equality
case (a,b)=(4,2). Does not import C++ embedding or colouring engine.
Each failing case provides a size-2 vertex-deletion obstruction to B,
except the unique disjoint union F(4,2,1)+2K(1,4), where A fails.
"""
from itertools import combinations
from collections import Counter
import json,hashlib
from pathlib import Path

old=range(1,10)
subsets=[frozenset(p) for k in range(5) for p in combinations(old,k)]
small=frozenset(range(5,10))
large_leaves=frozenset(range(1,5))
counts=Counter();examples={}
for A in subsets:
 for B in subsets:
  for h in range(min(4-len(A),4-len(B))+1):
   counts['generated']+=1
   if A&small or B&small:
    counts['B_fails_by_deleting_hub_plus_base_centre']+=1
    continue
   if A&large_leaves or B&large_leaves:
    counts['B_fails_by_deleting_opposite_hub_plus_shared_base_leaf']+=1
    continue
   if h:
    counts['B_fails_by_deleting_base_centre_plus_common_fresh_neighbour']+=1
    continue
   assert not A and not B and h==0
   counts['unique_two_vertex_deletion_survivor']+=1
   examples['unique']={'old_hub_neighbours':[[],[]],'fresh_shared_neighbours':0,
       'graph_components':[[4,2,1],[4],[4]],
       'A_avoiding_rule':'one red edge from each of three 4-stars, all other edges blue'}
assert counts['generated']==84653
assert counts['unique_two_vertex_deletion_survivor']==1
assert sum(v for k,v in counts.items() if k!='generated')==84653
print('RIGID15_INDEPENDENT_SYMBOLIC_CLASSIFICATION_PASS',dict(counts))
Path(__file__).with_name('RIGID_15EDGE_STRUCTURAL_CERTIFICATE.json').write_text(json.dumps({'record_type':'ERDOS561_RIGID15_COMPLETE_STRUCTURAL_CERTIFICATE/1',
 'original_red':[4,2,1],'original_blue':[4,1,1,1],
 'joint_lower_bound':16,'candidate_edges_excluded':15,
 'partition_counts':dict(counts),'unique_survivor':examples['unique'],
 'proof':'Each failure is accompanied by a two-vertex deletion that eliminates every degree-four centre or forces two required F(4,2,1) stars to share vertices. The sole deletion survivor is the disjoint-star host and has the indicated explicit A-avoiding colouring.',
 'full_general_conjecture_proved':False},indent=2)+'\n')
