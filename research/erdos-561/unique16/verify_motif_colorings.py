#!/usr/bin/env python3
"""Sharp 16-edge obstruction's canonical two-block colouring.
Every colour meets exactly six vertices, so neither contains any
three-star forest whose minimum possible vertex count is seven.
"""
from itertools import combinations
from collections import Counter
import json,os
from pathlib import Path

removed={(0,1),(0,2),(3,4)}
red=[];blue=[]
for i,j in combinations(range(5),2):
    if (i,j) not in removed:
        red.append((i,j))
        blue.append((i+5,j+5))
red.append((0,10))
blue.append((5,10))
assert len(red)==len(blue)==8
all_edges=red+blue
assert len(all_edges)==16 and len(set(tuple(sorted(x)) for x in all_edges))==16
D=Counter(v for e in all_edges for v in e)
assert sorted(D.values())==[2]+[3]*10
red_used={u for edge in red for u in edge}
blue_used={u for edge in blue for u in edge}
assert len(red_used)==len(blue_used)==6

inp=Path(os.environ.get('UPSTREAM_561_LOWDEGREE_LEDGER',Path(__file__).resolve().parent.parent/'lowdegree'/'LOWDEGREE_75_CASE_LEDGER.json'))
assert inp.is_file()
data=json.loads(inp.read_text())
closed=[]
for entry in data['remaining']:
    if entry['D']!=3 or entry['E']!=16:continue
    a,b=entry['red'],entry['blue']
    assert len(a)==len(b)==3 and a[0]>=2 and b[0]>=2
    assert sum(a)+3>=7 and sum(b)+3>=7
    assert len(red_used)<sum(a)+3 and len(blue_used)<sum(b)+3
    closed.append([a,b])
assert len(closed)==4
print('CANONICAL_16_EDGE_COLOURING_PASS',{'edges':16,'red_support':6,'blue_support':6,'closed_ordered':len(closed),'closed_pairs':closed})
Path(__file__).with_name('CANONICAL_MOTIF_CLOSURES.json').write_text(json.dumps({'closed_ordered_pairs':closed,'remaining_prior_39':39-4,'unordered_prior_20':20-2},indent=2)+'\n')
