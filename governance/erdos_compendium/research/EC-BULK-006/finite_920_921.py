#!/usr/bin/env python3
"""Exact small-graph interfaces for EC-BULK-006 920/921.
Does NOT reprove Bradač's 2026 off-diagonal Ramsey theorem, nor KST84.
"""
import json
from itertools import combinations
from math import ceil

def graph(n, mask, edges):
    a=[0]*n
    for i,(u,v) in enumerate(edges):
        if mask>>i&1:
            a[u]|=1<<v;a[v]|=1<<u
    return a

def is_independent(a, vs):
    return all((a[u]>>v&1)==0 for u,v in combinations(vs,2))

def has_clique(a, k):
    return any(all(a[u]>>v&1 for u,v in combinations(vs,2)) for vs in combinations(range(len(a)),k))

def alpha(a):
    n=len(a)
    for t in range(n,0,-1):
        if any(is_independent(a,vs) for vs in combinations(range(n),t)):return t
    return 0

def chi(a):
    n=len(a);order=sorted(range(n),key=lambda i:-a[i].bit_count())
    color=[-1]*n
    def dfs(pos,k):
        if pos==n:return True
        v=order[pos]
        for c in range(k):
            if all(color[u]!=c for u in range(n) if (a[v]>>u)&1):
                color[v]=c
                if dfs(pos+1,k):return True
                color[v]=-1
        return False
    for k in range(1,n+1):
        if dfs(0,k):return k
    raise AssertionError('no coloring')

def small_graphs():
    rows=[]; total=0; total_transfer=0; total_4chromatic=0
    for n in range(2,7):
        E=list(combinations(range(n),2))
        counts={'k3free':0,'k4free':0,'chi_ge4':0,'chi_ge4_triangles':0}
        min_independence={'3':n+1,'4':n+1}
        max_chi={'3':0,'4':0}
        for mask in range(1<<len(E)):
            a=graph(n,mask,E)
            al=alpha(a);c=chi(a)
            assert n<=al*c
            total_transfer+=1
            if c>=4:
                counts['chi_ge4']+=1
                assert has_clique(a,3),('triangle-free four-chromatic small',n,mask)
                counts['chi_ge4_triangles']+=1
            for k in (3,4):
                if not has_clique(a,k):
                    counts[f'k{k}free']+=1
                    min_independence[str(k)]=min(min_independence[str(k)],al)
                    max_chi[str(k)]=max(max_chi[str(k)],c)
                    assert c>=ceil(n/al)
        rows.append(dict(n=n,total_graphs=1<<len(E),counts=counts,
            min_alpha_by_clique_free=min_independence,
            f_k_n_by_exhaustive_chromatic=max_chi))
        total+=1<<len(E);total_4chromatic+=counts['chi_ge4']
    assert total==33866
    # On five vertices C5 avoids triangles and independent triples, so
    # r(3,3)>5; on six vertices any graph has a triangle or independent triple.
    n=5;E=list(combinations(range(n),2))
    cyc={(min(i,(i+1)%n),max(i,(i+1)%n)) for i in range(n)}
    cmask=sum(1<<i for i,e in enumerate(E) if e in cyc)
    a=graph(n,cmask,E)
    assert not has_clique(a,3) and alpha(a)==2 and chi(a)==3
    n=6;E=list(combinations(range(n),2))
    assert all(has_clique(graph(n,m,E),3) or alpha(graph(n,m,E))>=3
               for m in range(1<<len(E)))
    return dict(all_labelled_graphs=total,all_graph_chi_alpha_bounds=total_transfer,
      graph_rows=rows,chi_at_least_four_graphs=total_4chromatic,
      exact_r33=6,
      ramsey_transfer='If n<r(s,t), some n-vertex Ks-free G has alpha(G)<t, so chi(G)>=ceil(n/(t-1)).',
      source_boundary='Finite Ramsey transfer and odd-cycle small examples only. Not Bradač v3 or Kierstead–Szemerédi–Trotter full theorem.')

if __name__=='__main__':
 print(json.dumps(dict(record_type='EC_BULK_006_920_921_FINITE/1',
       p920_p921=small_graphs(),
       symbolic={
          '920':'Bradač v3 r(k,t)>=a*t^(k-1)/(log t)^(2k-4) implies f_k(n)>=b*n^((k-2)/(k-1))/(log n)^((2k-4)/(k-1)). Positive log exponent is in DENOMINATOR.',
          '921':'Set l=k-2 in KST84: no short odd cycles at length C_l*n^(1/l) implies chromatic number at most l+1=k-1, so a k-chromatic graph has some odd cycle at most C_l*n^(1/(k-2)).',
          '921_lower':'Lovasz/Schrijver examples credited by KST84 give matching exponent. Not reconstructed by finite enumeration.',
          'source_versions':'Bradac arXiv 2605.28793 v1 exponent s-2; v3 Jun 16 2026 exponent s-1; KST84 original Combinatorica 4 pp183-185.'
        }),indent=2,sort_keys=True))
