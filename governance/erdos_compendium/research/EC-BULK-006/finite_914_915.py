#!/usr/bin/env python3
"""Exact small Hajnal–Szemerédi and Menger interfaces.
No general HS theorem, Mader bound, or 57-vertex Leonard certificate is proved.
"""
import json
from itertools import combinations
from functools import lru_cache
from math import comb

def hs_check(n,mask,edges,r,m):
    # Complement graph H has maximum degree <=m-1; equitable m colors of size r.
    a=[0]*n
    for i,(u,v) in enumerate(edges):
        if mask>>i&1:
            a[u]|=1<<v;a[v]|=1<<u
    if min(z.bit_count() for z in a)<m*(r-1):return False
    opts=[]
    full=(1<<n)-1
    for group in combinations(range(n),r):
        gmask=sum(1<<i for i in group)
        if all(a[u]>>v&1 for u,v in combinations(group,2)):opts.append(gmask)
    @lru_cache(None)
    def partition(rem):
        if rem==0:return True
        u=(rem&-rem).bit_length()-1
        return any((o>>u&1) and (o&rem)==o and partition(rem^o) for o in opts)
    assert partition(full),(n,r,m,mask)
    # Independent exact bijection: disjoint K_r partition gives m color classes
    # of size r in complement, and vice versa.
    return True

def finite_hs():
    rows=[];counts=0
    for n in range(2,7):
        E=list(combinations(range(n),2))
        cases=[(r,n//r) for r in range(2,n+1) if n%r==0]
        per=[]
        for r,m in cases:
            eligible=0
            for mask in range(1<<len(E)):
                if hs_check(n,mask,E,r,m):eligible+=1
            per.append({'r':r,'m':m,'minimum_degree_required':m*(r-1),
                        'graphs_meeting_hypothesis':eligible})
            counts+=eligible
        rows.append({'n':n,'total_labelled_graphs':1<<len(E),'applicable_parameters':per})
    assert sum(x['total_labelled_graphs'] for x in rows)==33866
    # Stronger min-degree threshold is tight: n=6, r=3, m=2,
    # K_{3,3} has delta 3, while hypothesis 4; contains no K3.
    n=6;E=list(combinations(range(n),2))
    bip=sum(1<<i for i,(u,v) in enumerate(E) if (u<3)!=(v<3))
    adj=[0]*n
    for i,(u,v) in enumerate(E):
        if bip>>i&1:adj[u]|=1<<v;adj[v]|=1<<u
    assert min(z.bit_count() for z in adj)==3
    assert not any(all(adj[u]>>v&1 for u,v in combinations(g,2))
                   for g in combinations(range(n),3))
    return dict(rows=rows,qualifying_exact_graph_parameter_pairs=counts,
                sharp_boundary={'graph':'K3,3','n':6,'r':3,'m':2,
                                'degree':3,'required_degree':4,'triangle_count':0})

def reachable(n,edges,s,t,remove):
    a=[[] for _ in range(n)]
    for u,v in edges:
        if u not in remove and v not in remove:
            a[u].append(v);a[v].append(u)
    q=[s];seen={s}
    for u in q:
        if u==t:return True
        for v in a[u]:
            if v not in seen:seen.add(v);q.append(v)
    return False

def internally_disjoint_count(n,edges,s,t):
    # Paths with adjacent endpoints: direct edge is a separate internally
    # disjoint path. Remove that edge; Menger theorem applies to nonadjacent
    # endpoints in the remaining graph, where a finite vertex separator exists.
    direct=(min(s,t),max(s,t)) in set(edges)
    e2=[e for e in edges if e!=(min(s,t),max(s,t))]
    others=[v for v in range(n) if v!=s and v!=t]
    if not reachable(n,e2,s,t,set()):return int(direct)
    for k in range(len(others)+1):
        for U in combinations(others,k):
            if not reachable(n,e2,s,t,set(U)):
                return k+int(direct)
    raise AssertionError('nonadjacent endpoints cannot remain connected after all others removed')

def finite_menger():
    rows=[];tot=0
    # Relevant nontrivial cases for m=2 and m=3; for m=3, n=5, e>=7.
    for n in range(3,7):
        E=list(combinations(range(n),2));satisfy=0;tested=0
        for mask in range(1<<len(E)):
            e=mask.bit_count()
            targets=[]
            for m in (2,3):
                if (n-1)%(m-1)==0:
                    t=(n-1)//(m-1)
                    threshold=1+t*comb(m,2)
                    if threshold<=comb(n,2) and e>=threshold:targets.append((m,threshold))
            if not targets:continue
            edges=[e for i,e in enumerate(E) if mask>>i&1]
            maxconn=max(internally_disjoint_count(n,edges,u,v) for u,v in E)
            for m,threshold in targets:
                assert maxconn>=m,(n,e,m,threshold,edges)
                tested+=1;satisfy+=1
        rows.append(dict(n=n,graph_count=1<<comb(n,2),
            graph_parameter_instances_tested=tested,passed=satisfy))
        tot+=tested
    bouquet=[]
    for m in range(2,9):
        for t in (1,2,3,5):
            n=1+t*(m-1);e=t*comb(m,2)
            assert (1+t*(m-1),1+t*comb(m,2))==(n,e+1)
            # Each block K_m has at most m-1 internally vertex-disjoint
            # paths between its vertices; different blocks connected only
            # through one shared cut vertex. So no pair has m.
            bouquet.append(dict(clique_size=m,blocks=t,vertices=n,edges=e,
                claimed_max_internal_vertex_connectivity=m-1,
                conjectured_edge_threshold=e+1))
    return dict(finite_small_instances=rows,
                relevant_graph_parameter_cases=tot,
                bouquet_examples=bouquet,
                distinction='Internally vertex-disjoint uses vertex separators; edge-disjoint uses edge cuts. Different questions.',
                source_boundary='Leonard m5 57-vertex141-edge counterexample and Mader general results cited, not independently constructed by this finite fixture.')

if __name__=='__main__':
 print(json.dumps(dict(record_type='EC_BULK_006_914_915_FINITE/1',
  authority='Exact finite structural tests only; full 1970, 1973, 2008 published proofs imported',
  p914=finite_hs(),p915=finite_menger()),indent=2,sort_keys=True))
