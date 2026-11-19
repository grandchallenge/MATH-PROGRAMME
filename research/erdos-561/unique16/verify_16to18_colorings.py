#!/usr/bin/env python3
"""Independent exhaustive simple-graph check of 16-edge motif with <=2 extra
edges wholly outside its two saturated five-vertex blocks.
Every graph with e<=18 failing (1,2) caps must have this form by the
paper theorem and separate exact cut-profile audit. The extra edges can
meet center vertex x=10, or up to four otherwise isolated new vertices.
Check both monochrome choices for the extra edges against the exact
three-star target vertex-count obstruction, for EVERY permitted outside
graph of size r=1 or 2. Two cap failure types are not conflated with
target avoidance.
"""
import json,os
from itertools import combinations
from pathlib import Path

src=Path(os.environ.get('UPSTREAM_561_LOWDEGREE_LEDGER',Path(__file__).resolve().parent.parent/'lowdegree'/'LOWDEGREE_75_CASE_LEDGER.json'))
assert src.is_file(),src
data=json.loads(src.read_text())
base16=json.loads(Path(__file__).with_name('CANONICAL_MOTIF_CLOSURES.json').read_text())
prior_closed={(tuple(a),tuple(b)) for a,b in base16['closed_ordered_pairs']}

missing=[x for x in data['remaining'] if (tuple(x['red']),tuple(x['blue'])) not in prior_closed]
d3=[x for x in missing if x['D']==3]
assert len(d3)==10,d3
assert sorted([x['E'] for x in d3])==[17]*6+[18]*4

# Canonical 16-edge motif uses original vertices 0..10.
removed={(0,1),(0,2),(3,4)}
base_red=[(i,j) for i,j in combinations(range(5),2) if (i,j) not in removed]+[(0,10)]
base_blue=[(i+5,j+5) for i,j in combinations(range(5),2) if (i,j) not in removed]+[(5,10)]
assert len(base_red)==len(base_blue)==8
base_edges=base_red+base_blue

def used_vertices(edges):
    return {v for e in edges for v in e}

def target_vertices(t):return sum(t)+3

# Edges outside both 5-blocks can use the central vertex x and 4 new
# vertices 11..14. Every pair of new exterior edges can be relabelled
# into this five-vertex exterior host (at most 4 new endpoints).
outsiders=range(10,15)
pool=list(combinations(outsiders,2))
checked=0;approved=[]
for item in d3:
    red_target=tuple(item['red']);blue_target=tuple(item['blue']);e=item['E']
    r=e-16
    configurations=0
    for extra in combinations(pool,r):
        edges=base_edges+list(extra)
        assert len(set(edges))==len(edges)==e
        deg={v:0 for v in range(15)}
        for u,v in edges:
            deg[u]+=1;deg[v]+=1
        if max(deg.values())>3:continue
        configurations+=1;checked+=1
        valid=False
        # All extra edges sent to ONE color, choosing whichever forest
        # has adequate vertex-size lower bound.
        for red_extra in (True,False):
            red=list(base_red)+list(extra if red_extra else [])
            blue=list(base_blue)+list([] if red_extra else extra)
            if len(used_vertices(red))<target_vertices(red_target) and \
               len(used_vertices(blue))<target_vertices(blue_target):
                valid=True;break
        if not valid:
            raise AssertionError(('UNCOVERED_OUTSIDE_GRAPH',item,extra))
    assert configurations==(10 if r==1 else 39),(item,configurations)
    approved.append([list(red_target),list(blue_target),e,configurations])

assert checked==6*10+4*39,checked
assert len(approved)==10
allclosed={*prior_closed,*((tuple(a),tuple(b)) for a,b,*_ in approved)}
left=[x for x in data['remaining'] if (tuple(x['red']),tuple(x['blue'])) not in allclosed]
assert len(allclosed)==14 and len(left)==25,(len(allclosed),len(left))
assert all(x['D']==4 for x in left)
unordered_left={tuple(sorted((tuple(x['red']),tuple(x['blue'])))) for x in left}
assert len(unordered_left)==13,len(unordered_left)
result={'previous_ordered_method_survivors':39,'initial_16edge_exclusions':4,
        'new_17_18edge_exclusions':10,'total_excluded':14,
        'remaining_ordered':25,'remaining_unordered':13,
        'max_degree_of_all_remaining':4,
        'exterior_graph_colorings_checked':checked,
        'added_17_18_cases':approved,
        'remaining_25':left}
Path(__file__).with_name('SIXTEEN_TO_EIGHTEEN_PARAMETER_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print('SIXTEEN_TO_EIGHTEEN_EXACT_COLORING_PASS',
      {'17edge_target_cases':6,'18edge_target_cases':4,'outside_graph_configs_checked':checked,
       'newly_excluded':10,'total_excluded':14,'remaining_ordered':25,'remaining_unordered':13})
