#!/usr/bin/env python3
"""Exact finite interfaces only. Cannot construct Rudin's CH-dependent planar set
or settle Erdős #911 uniform size-Ramsey conjecture.
"""
import json
from itertools import combinations
from math import comb

def topological_cardinality_proxy():
    out=[]
    for n in range(2,13):
        mask=(1<<n)-1
        counts={}
        for d in range(0, min(n,3)+1):
            subsets=[mask^sum(1<<i for i in I) for I in combinations(range(n),d)]
            assert len(subsets)==comb(n,d)
            assert all((mask^x).bit_count()==d for x in subsets)
            counts[str(d)]=len(subsets)
        assert sum(counts.values())==sum(comb(n,d) for d in range(min(n,3)+1))
        out.append({'points':n,'complement_size_to_subset_count':counts})
    return {
       'finite_proxy':out,
       'exact_infinite_lemma':'If |M|=continuum, the family of all subsets M\\D with D countable has cardinal at most continuum, since |[M]^{<=aleph0}| <= |M|^aleph0=(2^aleph0)^aleph0=2^aleph0.',
       'logical_boundary':'Rudin constructs M under CH with every nondegenerate connected N co-countable. This bound applies to connected N AFTER construction; it does not show their homeomorphism types.',
       'CH_boundary':'CH is used in the original Rudin construction, not in continuum^aleph0=continuum arithmetic itself.',
       'no_fake_topology':'Finite-set subset counting cannot reproduce a connected, noncompact, pathological subset of the Euclidean plane.'
    }

def max_cut_edges(n,mask,edges):
    best=0
    for A in range(1<<(n-1)):
        # Fix vertex 0 in side zero to avoid complementary duplicates.
        cut=0
        for i,(u,v) in enumerate(edges):
            if (mask>>i)&1 and ((A>>(u-1)&1 if u else 0)!=(A>>(v-1)&1 if v else 0)):
                cut+=1
        if cut>best:best=cut
    return best

def finite_core_check():
    rows=[]
    total=0
    for n in range(2,7):
        pairs=list(combinations(range(n),2))
        tests=0
        for mask in range(1,1<<len(pairs)):
            e=mask.bit_count()
            cut=max_cut_edges(n,mask,pairs)
            assert 2*cut>=e
            # Create an actual maximum-cut bipartite graph, with deterministic ties.
            bests=[]
            for A in range(1<<(n-1)):
                cutedges=[(u,v) for i,(u,v) in enumerate(pairs)
                    if mask>>i&1 and ((A>>(u-1)&1 if u else 0)!=(A>>(v-1)&1 if v else 0))]
                if len(cutedges)==cut:
                    bests=cutedges;break
            keep=set(range(n)); Ed=set(bests)
            # Remove vertices of degree < C/4 = e/(4n) in original graph.
            while True:
                candidates=[v for v in sorted(keep)
                    if 4*n*sum(v in edge for edge in Ed)<e]
                if not candidates:break
                v=candidates[0]
                keep.remove(v)
                Ed={edge for edge in Ed if v not in edge}
            assert len(Ed)*4>e,(n,mask,e,cut,Ed)
            assert all(4*n*sum(v in edge for edge in Ed)>=e for v in keep)
            tests+=1
        total+=tests
        rows.append(dict(n=n,edge_positions=len(pairs),tested_nonempty_graphs=tests,
                         expected=(1<<comb(n,2))-1))
    assert total==33861
    return dict(rows=rows,all_nonempty_labelled_graphs=total,
      graph_lemma='Every n-vertex G with e>0 edges has a bipartite subgraph F with e(F)>e/4 and min_degree(F)>=e/(4n).',
      proof='A maximum cut keeps >=e/2 edges; remove a vertex of current degree <e/(4n) iteratively. At most n deletions remove <e/4 edges in total.',
      finite_boundary='This only proves structural extraction, not size-Ramsey beta(d)=omega(d).')

def projective_plane(q):
    assert q in (2,3,5,7,11)
    vec=set()
    for a in range(q):
        for b in range(q):
            for c in range(q):
                w=(a,b,c)
                if not any(w):continue
                inverse=pow(next(x for x in w if x),-1,q)
                vec.add(tuple(inverse*x%q for x in w))
    V=sorted(vec)
    k=q*q+q+1
    assert len(V)==k
    line_neigh=[]
    for a,b,c in V:
        ne={j for j,(x,y,z) in enumerate(V) if (a*x+b*y+c*z)%q==0}
        assert len(ne)==q+1
        line_neigh.append(ne)
    degree=[0]*k
    for ne in line_neigh:
        for point in ne:degree[point]+=1
    assert all(d==q+1 for d in degree)
    common_hist={}
    for i,j in combinations(range(k),2):
        intersect=len(line_neigh[i]&line_neigh[j])
        common_hist[intersect]=common_hist.get(intersect,0)+1
        assert intersect==1
    assert sum(common_hist.values())==comb(k,2)
    return dict(q=q,points_per_part=k,total_vertices=2*k,
       min_degree=q+1,edges=k*(q+1),edges_per_vertex=(q+1)/2,
       same_part_pair_common_neighbor_histogram=common_hist,
       square_free=True,
       reason='Any C4 would produce two distinct lines through the same pair of points.')

if __name__=='__main__':
 print(json.dumps(dict(record_type='EC_BULK_006_910_911_FINITE/1',
    source_boundary='Rudin 1958 CH construction and size-Ramsey uniform beta conjecture are NOT established by finite checks.',
    p910=topological_cardinality_proxy(),
    p911={'structural_extraction':finite_core_check(),
           'projective_plane_incidence':[projective_plane(q) for q in (2,3,5,7,11)],
           'universal_two_pile':'Any target F with m>=1 edges has size-Ramsey number >=2m-1; every host with <=2m-2 edges splits into two color piles <=m-1.',
           'reduction':'Uniform beta(d)/d->infinity for bipartite minimum-degree-d targets is equivalent to #911 up to constants via maximum cut and pruning.',
           'remaining_unproved':'Prove beta(d)=omega(d), including high-girth C4-free regular bipartite targets.'}),
   indent=2,sort_keys=True))
