#!/usr/bin/env python3
"""Exact finite Folkman potential and Rödl edge-partition checks.
The checked finite cases do not replace Folkman's arbitrary finite-graph theorem.
"""
import json
from itertools import combinations
from functools import lru_cache

def invariant(a):
    n=len(a); full=(1<<n)-1
    @lru_cache(None)
    def alpha(mask):
        if not mask:return 0
        v=(mask&-mask).bit_length()-1
        return max(alpha(mask&~(1<<v)),1+alpha(mask&~(1<<v)&~a[v]))
    indep=[mask for mask in range(1,full+1)
           if all(not (a[v]&(mask&~(1<<v))) for v in range(n) if mask>>v&1)]
    @lru_cache(None)
    def chi(mask):
        if not mask:return 0
        bit=mask&-mask
        return 1+min(chi(mask^S) for S in indep if S&bit and (S&mask)==S)
    return alpha,chi,indep

def graph(n,mask):
    ed=list(combinations(range(n),2))
    a=[0]*n
    for i,(u,v) in enumerate(ed):
        if mask>>i&1:
            a[u]|=1<<v;a[v]|=1<<u
    return a

def folkman_and_rodl():
    folkrows=[]; rodlrows=[]
    total=0;strict=0;potential_eq=0;exact_pair_tests=0
    rodl_partitioned=0;rodl_high_left=0;rodl_k4free=0
    for n in range(1,7):
        num=1<<(n*(n-1)//2); row={'n':n,'graphs':num,'potential_bound_pass':0,
                 'exact_at_bound':0,'all_k_hypothesis_pairs':0}
        rodl={'n':n,'k4free_graphs':0,'high_chi_left_neighborhood':0,
              'valid_two_layer_partitions':0,'all_partition_trianglefree':True}
        for Gmask in range(num):
            a=graph(n,Gmask); full=(1<<n)-1
            alpha,chi,indep=invariant(a)
            pmax=max((S.bit_count()-2*alpha(S)+2) for S in range(full+1))
            truechi=chi(full)
            assert truechi<=pmax,('folkman',n,Gmask,truechi,pmax)
            if truechi==pmax:row['exact_at_bound']+=1;potential_eq+=1
            row['potential_bound_pass']+=1;total+=1
            # For every k up to n+1 check quantified hypothesis vs the
            # fixed-parameter potential inequality and its chromatic corollary.
            for k in range(n+2):
                hyp=all(2*alpha(S)>=S.bit_count()-k for S in range(full+1))
                assert hyp==(pmax<=k+2)
                if hyp:assert truechi<=k+2
                row['all_k_hypothesis_pairs']+=1;exact_pair_tests+=1
            # Check source mechanism at m=4, target 3, P=F(3,3)-1=2:
            # for every K4-free G, each left neighborhood either has chi>=3,
            # or can be colored using <=P. On low-neighborhood case
            # assign each edge to the local color of its LEFT endpoint in L(v).
            if any(all(a[u]>>v&1 for u,v in combinations(vs,2))
                   for vs in combinations(range(n),4)):
                continue
            rodl['k4free_graphs']+=1; rodl_k4free+=1
            left_colorings={};high=False
            for v in range(n):
                nbrs=[u for u in range(v) if a[v]>>u&1]
                # Explicit exhaustive 2-coloring of induced left-neighborhood.
                colors=None
                for bits in range(1<<len(nbrs)):
                    trial={u:(bits>>i)&1 for i,u in enumerate(nbrs)}
                    if all(trial[u]!=trial[w] for u,w in combinations(nbrs,2)
                           if a[u]>>w&1):
                        colors=trial;break
                if colors is None: high=True;break
                left_colorings[v]=colors
            if high:
                rodl['high_chi_left_neighborhood']+=1;rodl_high_left+=1
                continue
            groups=[[] for i in range(2)]
            for u,v in combinations(range(n),2):
                if a[u]>>v&1:
                    groups[left_colorings[v][u]].append((u,v))
            for edges in groups:
                edge_set=set(edges)
                assert all(not all((u,v) in edge_set for u,v in combinations(vs,2))
                           for vs in combinations(range(n),3)),('triangle layer',n,Gmask)
            rodl['valid_two_layer_partitions']+=1;rodl_partitioned+=1
            assert sum(map(len,groups))==sum(x.bit_count() for x in a)//2
            assert chi(full)<=4,('rodl product-color bound',n,Gmask)
        folkrows.append(row);rodlrows.append(rodl)
    assert total==33867 and rodl_high_left+rodl_partitioned==rodl_k4free
    assert exact_pair_tests==sum(r['graphs']*(r['n']+2) for r in folkrows)
    # Sharpness: C5 gives k=1, chi=3; K_(k+2) for k<=4 gives chi=k+2
    a=graph(5,sum(1<<i for i,e in enumerate(combinations(range(5),2))
                  if e in {(0,1),(1,2),(2,3),(3,4),(0,4)}))
    al,ch,_=invariant(a)
    assert al(31)==2 and ch(31)==3
    for k in range(5):
        m=k+2;a=[((1<<m)-1)^(1<<u) for u in range(m)]
        al,ch,_=invariant(a)
        assert ch((1<<m)-1)==k+2
        assert all(2*al(S)>=S.bit_count()-k for S in range(1<<m))
    def f(m,n):
        if m==2:return 2
        return (n-1)**(f(m-1,n)-1)+1
    recurrence=[{'m':m,'target_chi':n,'bound_F':str(f(m,n))}
                for n in (2,3,4) for m in range(2,6)]
    return {'record_type':'EC_BULK_006_922_923_FINITE/1',
       'p922':{'graphs_checked':total,'k_hypothesis_cases':exact_pair_tests,
         'equality_chi_potential_graphs':potential_eq,'rows':folkrows,
         'potential':'rho(H)=|V(H)|-2*alpha(H)+2; chi(G)<=max_{H induced}rho(H)',
         'small_sharpness':'C5 k=1 chi=3, K_(k+2) k=0..4 attains bound'},
       'p923':{'k4free_graphs_checked':rodl_k4free,
        'left_neighborhood_chi_ge_3':rodl_high_left,
        'exact_two_bucket_trianglefree_partitions':rodl_partitioned,
        'rows':rodlrows,'rodl_recursive_bounds':recurrence,
        'product_coloring_lemma':'If E(G) split into P layers each (n-1)-colorable, chi(G)<=(n-1)^P.',
        'edge_partition_trianglefree':'Color earlier neighbors of each vertex; bucket of an edge uses earlier endpoint color. Every bucket is triangle-free.',
        'source_limit':'Rödl 1977 graph result also needs arbitrarily highly chromatic triangle-free constructions (Mycielski).'},
       'claim_boundary':'All checked examples are finite orders 1..6; exact source proof mechanisms are mathematically explained separately.'}
if __name__=='__main__':
 print(json.dumps(folkman_and_rodl(),sort_keys=True,indent=2))
