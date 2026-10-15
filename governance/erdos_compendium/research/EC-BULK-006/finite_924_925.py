#!/usr/bin/env python3
"""Exact small Ramsey/edge-Folkman tests; finite fixtures only."""
import itertools,json
from collections import Counter

def edges(n):return list(itertools.combinations(range(n),2))
def triangles(n):
    e=edges(n); index={p:i for i,p in enumerate(e)}
    return [tuple(index[p] for p in itertools.combinations(t,2)) for t in itertools.combinations(range(n),3)]
def cliques(n):
    e=edges(n); index={p:i for i,p in enumerate(e)}
    return {m:[tuple(index[p] for p in itertools.combinations(s,2)) for s in itertools.combinations(range(n),m)] for m in range(2,n+1)}
def avoid(c,tri,colors=(0,1)):
    return all(not (c[a]==c[b]==c[d] and c[a] in colors) for a,b,d in tri)
def alpha_of_red_blue(c,cls):
    # Independent sets in G=(red+blue edges) are exactly green cliques.
    return max((m for m,sets in cls.items() if any(all(c[i]==2 for i in s) for s in sets)),default=1)
def check():
    rows=[];total=0;exact=0
    for n in range(1,6):
        E=edges(n);T=triangles(n);C=cliques(n)
        row={'n':n,'all_3_colorings':3**len(E),'red_blue_triangle_free':0,
             'green_clique_distribution':{},'conversion_checks':0,
             'two_color_avoiding':0}
        hist=Counter()
        for c in itertools.product(range(3),repeat=len(E)):
            if not avoid(c,T):continue
            row['red_blue_triangle_free']+=1
            alpha=alpha_of_red_blue(c,C)
            # Independently enumerate independent vertex sets in the graph
            # whose edges are the non-green pairs.
            graph_edges={E[i] for i,x in enumerate(c) if x!=2}
            brute=max((len(s) for m in range(1,n+1)
                       for s in itertools.combinations(range(n),m)
                       if all(p not in graph_edges for p in itertools.combinations(s,2))),default=0)
            assert alpha==brute,(n,c,alpha,brute)
            hist[alpha]+=1;row['conversion_checks']+=1;total+=1
            if all(x!=2 for x in c):row['two_color_avoiding']+=1
        row['green_clique_distribution']={str(k):v for k,v in sorted(hist.items())}
        rows.append(row)
    n=6;T=triangles(n);avoid6=0;count6=0
    for c in itertools.product((0,1),repeat=15):
        count6+=1
        if avoid(c,T):avoid6+=1
    assert avoid6==0
    assert rows[-1]['two_color_avoiding']>0
    assert sum(r['all_3_colorings'] for r in rows)==1+3+27+729+59049
    # A K5 2-colouring avoiding triangles extends by restriction to every graph
    # with <=5 vertices. Every 2-colouring of K6 contains a monochromatic K3.
    result={'fixture':'finite_924_925','scope':'all 3-edge-colorings of K_n for 1<=n<=5; all 2-edge-colorings of K6',
            'rows':rows,'conversion_checks':total,'two_color_K6':{'colorings':count6,'avoiding':avoid6},
            'logic':'G uses non-green edges; alpha(G) equals largest green clique exactly'}
    return result
if __name__=='__main__':
    from pathlib import Path
    r=check()
    p=Path(__file__).with_suffix('.json')
    p.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'conversion_checks':r['conversion_checks'],'K6':r['two_color_K6'],'rows':r['rows']},sort_keys=True))
