#!/usr/bin/env python3
"""Finite sanity regressions for infinite graph problems 918/919.
No finite test can decide any uncountable-existence conjecture.
"""
import json
from itertools import combinations,product

def chromatic(adj):
    n=len(adj)
    order=sorted(range(n),key=lambda v:-adj[v].bit_count())
    col=[-1]*n
    def try_k(k,i):
        if i==n:return True
        v=order[i]
        for c in range(k):
            if all(col[u]!=c for u in range(n) if adj[v]>>u&1):
                col[v]=c
                if try_k(k,i+1):return True
                col[v]=-1
        return False
    for k in range(1,n+1):
        if try_k(k,0):return k
    return 0

def adj_of(n,mask):
    e=list(combinations(range(n),2));a=[0]*n
    for i,(u,v) in enumerate(e):
        if mask>>i&1:a[u]|=1<<v;a[v]|=1<<u
    return a

def induce(adj,verts):
    return [sum(1<<j for j,w in enumerate(verts) if (adj[v]>>w)&1) for v in verts]

def semantic_918():
    # Every arbitrary subgraph H (not necessarily induced) is a subgraph
    # of G.induce(W). Check exact chromatic monotonicity under all edge deletions
    # for all labelled graphs n<=5, all W, all subgraphs of G.induce(W).
    cases=0;deletions=0;witness_lower=0
    for n in range(1,6):
        edges=list(combinations(range(n),2))
        for mask in range(1<<len(edges)):
            a=adj_of(n,mask)
            for wmask in range(1,1<<n):
                W=[i for i in range(n) if wmask>>i&1]
                ia=induce(a,W)
                chi=chromatic(ia)
                cases+=1
                ie=list(combinations(range(len(W)),2))
                idx=[j for j,(u,v) in enumerate(ie) if ia[u]>>v&1]
                for sub in range(1<<len(idx)):
                    reduced=0
                    for i,j in enumerate(idx):
                        if sub>>i&1:reduced|=1<<j
                    assert chromatic(adj_of(len(W),reduced))<=chi
                    deletions+=1
                if chi>1:witness_lower+=1
    # "all subgraphs have χ=aleph0" (rather than <=aleph0) is
    # impossible for any nonempty vertex set: edgeless spanning H has χ=1.
    return {'all_graph_vertex_subset_instances':cases,
      'all_induced_edge_subgraphs_tested':deletions,
      'induced_with_nontrivial_chromatic':witness_lower,
      'lemma':'For each vertex subset W, any subgraph on W has χ <= χ(G[W]); equivalence of <= bounds on induced versus all subgraphs.',
      'equality_warning':'For ANY nonempty W, edgeless spanning H on W has chromatic number 1, not countably infinite. The exact-equality variant is not equivalent.',
      'cardinal_padding':'If |V|>=lambda and |W|<=lambda, extend W to size exactly lambda (choice). Monotonicity transfers <=aleph0 from all lambda-sized induced subgraphs to smaller subsets.',
      'pinned_source':'google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020 918.lean blob d3d9b34b11e0903ca735b8e95190de565ba883fe',
      'pinned_ordinal_issue':'Part ii binds forall omega:Ordinal; printed Erdős asks fixed omega0 only. GCH omitted in pinned 1968 finite-k cited theorem.',
      'scope':'Purely finite monotonicity; no statement about existence of uncountable chromatic graphs.'}

def ordinal_grid_919():
    rows=[]
    for a,b in product(range(1,8),repeat=2):
        V=list(product(range(a),range(b)))
        E=[(i,j) for i,(x,y) in enumerate(V) for j,(u,v) in enumerate(V)
           if i<j and x<u and y<v]
        expect=(a*(a-1)//2)*(b*(b-1)//2)
        assert len(E)==expect
        # Coloring by smaller axis index: proper for both-coordinate increases.
        use_x=a<=b
        col=[x if use_x else y for x,y in V]
        assert all(col[i]!=col[j] for i,j in E)
        # A diagonal strictly-increasing clique of size min(a,b) certifies χ>=min(a,b).
        k=min(a,b)
        clique=[V.index((i,i)) for i in range(k)]
        eset=set(E)
        assert all((i,j) in eset for i,j in combinations(clique,2))
        rows.append({'rows':a,'columns':b,'vertices':a*b,'edges':len(E),
          'chromatic_number':k,'explicit_color_count':len(set(col)),
          'explicit_clique_size':k})
    return {'finite_lex_grid_cases':rows,
       'edge_rule':'Distinct pairs (alpha,beta),(alpha2,beta2) joined iff alpha<alpha2 and beta<beta2, unordered.',
       'exact_finite_chromatic':'On rectangular a×b finite grid, chi=min(a,b), by row/column coloring and diagonal clique.',
       'ordinal_cofinal_warning':'For infinite κ=ω₂, S={κ·ξ: ξ<κ} is cofinal in κ·κ but has order type κ, strictly less than κ². Thus lesser ordinal type does NOT imply a bounded initial segment nor lesser cardinality.',
       'counterfactual':'Finite grids do not reproduce infinite ordinal exponentiation or stationary-set/reflection mechanisms.',
       'scope':'Original #919 remains OPEN for χ=aleph2 or aleph1 with all smaller-order-type subsets countably chromatic.'}

if __name__=='__main__':
 print(json.dumps({'record_type':'EC_BULK_006_918_919_FINITE/1',
 'p918':semantic_918(),'p919':ordinal_grid_919()},indent=2,sort_keys=True))
