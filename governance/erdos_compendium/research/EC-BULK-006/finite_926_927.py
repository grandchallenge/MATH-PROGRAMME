#!/usr/bin/env python3
"""Exactly check H_k source graph, finite projective-plane lower witnesses,
and ALL maximal-clique-size patterns on labelled graphs of orders 1..6.
Published all-order Füredi, AKS, Spencer are imported, NOT derived here.
"""
import json
from itertools import combinations
from collections import Counter
from math import floor,log2

def h(k):
    assert k>=3
    y=list(range(1,k+1)); pairs=list(combinations(y,2))
    edges={(0,i) for i in y}
    for j,(a,b) in enumerate(pairs,start=k+1):
        edges.add(tuple(sorted((a,j))));edges.add(tuple(sorted((b,j))))
    n=1+k+len(pairs)
    A=[0]*n
    for u,v in edges:A[u]|=1<<v;A[v]|=1<<u
    assert len(edges)==k+2*len(pairs)
    assert all(A[0]>>u&1 for u in y)
    assert all(A[j].bit_count()==2 for j in range(k+1,n))
    assert all(A[u].bit_count()==k for u in y)
    assert A[0].bit_count()==k
    assert all((A[i]&A[j])>>0&1 for i,j in pairs)
    assert all((A[i]&A[j]) & ((1<<n)-1) for i,j in pairs)
    # The graph is bipartite between {y_i} and {x,z_ij}
    for u,v in edges:assert (u in y)!=(v in y)
    # C4 witnessed by x-y_i-z_ij-y_j-x.
    assert any((A[0]>>i)&1 and (A[0]>>j)&1
               and (A[k+1+t]>>i)&1 and (A[k+1+t]>>j)&1
               for t,(i,j) in enumerate(pairs))
    # Degeneracy: delete all z (degree 2), then y (degree 1), then x.
    return {'k':k,'vertices':n,'edges':len(edges),'degree_y':k,
      'x_degree':k,'z_degree':2,'bipartite':True,'girth':4,
      'two_degenerate_elimination':'first all z degree2, then y degree1, then x degree0'}

def projective(q):
    assert q in (2,3,5,7)
    vec=set()
    for x in range(q):
        for y in range(q):
            for z in range(q):
                if x==y==z==0:continue
                t=(x,y,z);a=pow(next(v for v in t if v),-1,q)
                vec.add(tuple((v*a)%q for v in t))
    V=sorted(vec);v=q*q+q+1;assert len(V)==v
    lines=[]
    for t in V:
        L={i for i,p in enumerate(V) if sum(a*b for a,b in zip(t,p))%q==0}
        assert len(L)==q+1
        lines.append(L)
    assert all(sum(i in line for line in lines)==q+1 for i in range(v))
    assert all(len(lines[a]&lines[b])==1 for a,b in combinations(range(v),2))
    n=2*v;e=v*(q+1)
    return {'q':q,'vertices':n,'edges':e,'minimum_degree':q+1,'girth':6,
      'no_C4':True,'no_H_k_for_any_k_ge_3':True,
      'edges_div_n_to_three_halves':e/n**1.5}

def max_clique_sizes(n,A):
    full=(1<<n)-1;out=set();witness={}
    for mask in range(1,full+1):
        if any(A[v]&(mask & ~(1<<v)) != mask & ~(1<<v) for v in range(n) if mask>>v&1):
            continue
        if any((A[v]&mask)==mask for v in range(n) if not mask>>v&1):
            continue
        k=mask.bit_count();out.add(k);witness.setdefault(k,mask)
    return out,witness

def maximal_cliques():
    allrows=[];count=0;upper=0
    for n in range(1,7):
        ed=list(combinations(range(n),2));mx=0;sample=None;hist=Counter()
        for graph_bits in range(1<<len(ed)):
            A=[0]*n
            for j,(u,v) in enumerate(ed):
                if graph_bits>>j&1:A[u]|=1<<v;A[v]|=1<<u
            sizes,w=max_clique_sizes(n,A)
            assert sizes,('nonempty maximal clique',n,graph_bits)
            assert all(1<=s<=n for s in sizes)
            # CRITICAL max clique means maximal by inclusion, not arbitrary K_t.
            cnt=len(sizes);hist[cnt]+=1;count+=1
            if n>=4:
                assert cnt<=n-floor(log2(n)),('Moon-Moser upper',n,graph_bits,cnt)
                upper+=1
            if cnt>mx:mx=cnt;sample={'edge_bitmask':graph_bits,'sizes':sorted(sizes),
                                   'one_maximal_vertex_set_per_size':{str(k):[i for i in range(n) if m>>i&1] for k,m in w.items()}}
        allrows.append({'n':n,'all_labelled_graphs':1<<len(ed),
                        'best_g_n':mx,'distribution_sizes_count':dict(sorted(hist.items())),
                        'one_witness':sample,
                        'moon_moser_bound':n-floor(log2(n)) if n>=4 else None})
    assert count==33867
    return {'graphs_checked':count,'moon_moser_upper_graphs_checked':upper,'rows':allrows,
      'maximal_not_maximum':'A clique is maximal if it cannot be extended by a vertex, not merely an arbitrary complete subgraph.',
      'injection_lemma':'Fix a largest clique T. A maximal clique C is uniquely determined by C minus T: its T part is exactly the vertices of T adjacent to every vertex of C minus T. Hence at most 2^(n-|T|) distinct maximal cliques.',
      'source_limitation':'Spencer 1971 all-n lower g(n)>=n-log2(n)-O(1) is imported published proof, not derived by finite search.'}

if __name__=='__main__':
 print(json.dumps({'record_type':'EC_BULK_006_926_927_FINITE/1',
      'p926':{'H_k':[h(k) for k in range(3,9)],
               'finite_projective_plane_incidence':[projective(q) for q in (2,3,5,7)],
               'claim_boundary':'Projective plane incidence C4-free gives omega(n^1.5) edges along q primes; C4 subset Hk. Published all-n extremal bound not proved here.'},
      'p927':maximal_cliques()},sort_keys=True,indent=2))
