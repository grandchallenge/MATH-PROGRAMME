#!/usr/bin/env python3
"""Exact finite, source-scoped cases for Erdős #903 and #904.
Neither arbitrary projective-plane parameter nor full Bollobás–Nikiforov theorem is proved here.
"""
import json
from itertools import combinations
from math import comb
from functools import lru_cache

def validate_design(v,blocks):
    seen={}
    for i,b in enumerate(blocks):
        assert len(b)>=2 and len(set(b))==len(b),(i,b)
        for a,c in combinations(sorted(b),2):
            assert (a,c) not in seen,(a,c,seen.get((a,c)),i)
            seen[(a,c)]=i
    assert len(seen)==comb(v,2)
    return True

def projective_plane(p):
    assert p in (2,3,5,7)
    vectors=[]
    for x in range(p):
        for y in range(p):
            for z in range(p):
                if (x,y,z)==(0,0,0):continue
                trip=(x,y,z)
                first=next(t for t in trip if t)
                inv=pow(first,-1,p)
                norm=tuple(t*inv%p for t in trip)
                if norm not in vectors:vectors.append(norm)
    assert len(vectors)==p*p+p+1
    blocks=[]
    for a,b,c in vectors:
        line=tuple(i for i,(x,y,z) in enumerate(vectors) if (a*x+b*y+c*z)%p==0)
        assert len(line)==p+1
        blocks.append(line)
    assert len(set(blocks))==len(vectors)
    validate_design(len(vectors),blocks)
    return vectors,blocks

def near_pencil_split(blocks):
    line=blocks[0];x=line[0]
    new=[tuple(line[1:])]+[tuple(sorted((x,y))) for y in line[1:]]
    assert len(new)==len(line) # old 1 replaced by p+1 => increases p
    result=blocks[1:]+new
    return result

def nontrivial_7_design_search():
    # Exact cover of 21 edges of K7 by blocks on >=2 vertices.
    # For a fixed earliest uncovered pair, enumerate blocks containing it,
    # and only allow blocks whose constituent pair edges are all uncovered.
    v=7
    edges=list(combinations(range(v),2))
    index={e:i for i,e in enumerate(edges)}
    full=(1<<len(edges))-1
    choices=[[] for _ in edges]
    for length in range(2,v+1):
        for block in combinations(range(v),length):
            mask=sum(1<<index[e] for e in combinations(block,2))
            for e in combinations(block,2):choices[index[e]].append((mask,block))
    # Counting isomorphism classes not required: every labelled exact cover checked.
    @lru_cache(None)
    def possible(mask,left):
        if mask==full:return left==0
        if left<=0:return False
        gap=full^mask
        if gap.bit_count()<left:return False
        if gap.bit_count()>left*comb(v,2):return False
        bit=gap&-gap
        i=bit.bit_length()-1
        for m,_ in choices[i]:
            if mask&m==0 and possible(mask|m,left-1):return True
        return False
    assert possible(0,7)
    assert not possible(0,8)
    assert possible(0,9)
    return dict(v=7,exact_cover_7_lines=True,exact_cover_8_lines=False,
       exact_cover_9_lines=True,cache_states=possible.cache_info().currsize)

def design_examples():
    examples=[]
    for p in (2,3,5):
        vectors,lines=projective_plane(p)
        broken=near_pencil_split(lines)
        validate_design(len(vectors),broken)
        assert len(broken)==len(vectors)+p
        examples.append(dict(p=p,v=len(vectors),projective_lines=len(lines),
           broken_lines=len(broken),all_pairs_exactly_once=True,
           first_old_line=lines[0],
           first_replacement_lines=broken[-(p+1):],
           line_size_distribution={str(k):sum(len(x)==k for x in broken) for k in range(2,p+2)}))
    return dict(examples=examples,exact_seven_point_exhaustion=nontrivial_7_design_search(),
       theorem_boundary='Erdos-Fowler-Sos-Wilson 1985 proves general excluded interval; finite fixtures verify p2 and constructions p2,p3,p5')

def turan_edges(n,r):
    q,k=divmod(n,r)
    classes=[q+1]*k+[q]*(r-k)
    return (n*n-sum(s*s for s in classes))//2

def verify_graph(n,mask,edges,edgeindex):
    adj=[0]*n
    m=mask.bit_count()
    for i,(a,b) in enumerate(edges):
        if mask>>i&1:adj[a]|=1<<b;adj[b]|=1<<a
    deg=[a.bit_count() for a in adj]
    assert sum(deg)==2*m
    record=[]
    for r in range(2,n+1):
        tr=turan_edges(n,r)
        if m<tr:continue
        maximum=0
        witness=None
        for S in combinations(range(n),r):
            if all(adj[a]>>b&1 for a,b in combinations(S,2)):
                score=sum(deg[a] for a in S)
                if score>maximum:maximum=score;witness=S
        assert witness is not None
        assert n*maximum>=2*r*m,(n,m,r,maximum,2*r*m)
        if n*maximum==2*r*m:record.append(r)
    return record

def balanced_cliques():
    cases=[]
    for n in range(2,7):
        edges=list(combinations(range(n),2))
        meets=0
        equal=0
        for mask in range(1<<len(edges)):
            observed=verify_graph(n,mask,edges,{v:i for i,v in enumerate(edges)})
            meets+=len(observed)
            equal+=int(bool(observed))
        cases.append(dict(n=n,graph_count=1<<comb(n,2),
           total_threshold_equalities_counted_by_r=meets,
           graphs_with_some_threshold_equality=equal,
           turan_values={str(r):turan_edges(n,r) for r in range(2,n+1)}))
    assert sum(x['graph_count'] for x in cases)==33866
    # Sharp example: balanced bipartite K3,3 (r=2,n=6) 9 edges;
    # every crossing edge has degree sum 6 == 4m/n.
    n=6;L=set(range(3));R=set(range(3,6))
    pair=list(combinations(range(n),2))
    mask=sum(1<<i for i,(a,b) in enumerate(pair) if (a in L)!=(b in L))
    assert mask.bit_count()==turan_edges(6,2)==9
    assert 2*2*9==6*(3+3)
    return dict(cases=cases,total_graphs=33866,
      exact_integer_inequality='n * max_{K_r} sum_deg >= 2*r*m',
      sharp_bipartite_case={'n':6,'r':2,'m':9,'clique_degree_sum':6,
                            'mean_scaled':6,'graph':'K3,3'},
      theorem_boundary='Exhaustive graph orders 2..6 only, not general Bollobas-Nikiforov')

if __name__=='__main__':
    print(json.dumps({'record_type':'EC_BULK_006_903_904_FINITE/1',
        'authority':'exact finite only, published 1985 and 2005 general proofs imported',
        'p903':design_examples(),'p904':balanced_cliques()},indent=2))
