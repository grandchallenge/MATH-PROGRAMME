#!/usr/bin/env python3
"""Exact finite graph fixtures for Erdős #900 and #902.
No finite test supplies the 1981 random-graph theorem or optimal tournament asymptotics.
"""
import json
from itertools import combinations
from math import comb

def path_vertices(n,mask,edges):
    adj=[0]*n
    for i,(a,b) in enumerate(edges):
        if mask>>i&1:
            adj[a]|=1<<b
            adj[b]|=1<<a
    reachable=[0]*(1<<n)
    for i in range(n):reachable[1<<i]|=1<<i
    longest=1
    for s in range(1,1<<n):
        ends=reachable[s]
        if ends==0:continue
        longest=max(longest,s.bit_count())
        while ends:
            bit=ends&-ends
            u=bit.bit_length()-1
            ends-=bit
            nxt=adj[u]&~s
            while nxt:
                vbit=nxt&-nxt
                nxt-=vbit
                reachable[s|vbit]|=vbit
    return longest

def graph_exhaustive():
    rows=[]
    for n in (3,4,5):
        edges=list(combinations(range(n),2))
        totals={}
        values={}
        for mask in range(1<<len(edges)):
            m=mask.bit_count()
            p=path_vertices(n,mask,edges)
            totals[m]=totals.get(m,0)+1
            d=values.setdefault(m,[])
            d.append(p)
            for i in range(len(edges)):
                if not mask>>i&1:
                    assert path_vertices(n,mask|(1<<i),edges)>=p
        assert all(totals[m]==comb(len(edges),m) for m in totals)
        rows.append(dict(n=n,edge_positions=len(edges),graphs=1<<len(edges),
            sampled_c_vs_longest=[dict(m=m,count=totals[m],min_vertices=min(values[m]),
                max_vertices=max(values[m]),
                mean_vertices_numerator=sum(values[m]),
                mean_vertices_denominator=totals[m])
                for m in sorted(totals)]))
    # A tree on n vertices has n-1 edges yet may have longest path 2:
    # random graph theorem is WHP, not all graphs.
    for n in (5,8):
        e=list(combinations(range(n),2))
        mask=sum(1<<i for i,ab in enumerate(e) if 0 in ab)
        assert path_vertices(n,mask,e)==3
    return dict(exhaustive_n=[3,4,5],total_exact_graphs=sum(1<<comb(n,2) for n in (3,4,5)),
        monotonicity='adding one edge cannot reduce longest simple path',tables=rows,
        star_counterexample='a star with n-1 edges has max simple path 3 vertices, so no deterministic linear path theorem for all graphs')

def tournament_property(n,orientation,k):
    # bit 1 for a->b for a<b, else b->a
    edges=list(combinations(range(n),2))
    adj=[0]*n
    for idx,(a,b) in enumerate(edges):
        if orientation>>idx&1:adj[a]|=1<<b
        else:adj[b]|=1<<a
    for S in combinations(range(n),k):
        Sbits=sum(1<<v for v in S)
        if not any((adj[y]&Sbits)==Sbits for y in range(n) if y not in S):
            return False
    return True

def paley67_certificate():
    p=67
    residues={x*x%p for x in range(1,p)}
    assert len(residues)==33 and all((p-r)%p not in residues for r in residues)
    # Common external dominators for set S: vertices y with y->x for each x in S.
    # Orient y->x exactly when y-x modulo 67 lies among quadratic residues.
    incoming=[0]*p
    for x in range(p):
        incoming[x]=sum(1<<y for y in range(p) if y!=x and (y-x)%p in residues)
    hist={}
    total=0
    for a,b,c,d in combinations(range(p),4):
        v=(incoming[a]&incoming[b]&incoming[c]&incoming[d]).bit_count()
        hist[v]=hist.get(v,0)+1
        total+=1
        assert v>=1,(a,b,c,d)
    assert total==comb(67,4)==766480
    assert sum(k*v for k,v in hist.items())==67*comb(33,4)
    return dict(vertices=67,foursets=total,common_dominator_distribution=hist,
        minimum_common_dominators=min(hist),maximum_common_dominators=max(hist),
        independent_checksum=67*comb(33,4),
        strength='EXACT finite certificate f(4)<=67, not a best-possible f(4) claim')

def tournament_exhaustive():
    counts={}
    for n in range(2,7):
        c1=c2=0
        for mask in range(1<<comb(n,2)):
            if tournament_property(n,mask,1):c1+=1
            if n>=3 and tournament_property(n,mask,2):c2+=1
        counts[str(n)]=dict(tournaments=1<<comb(n,2),property_S1=c1,
                           property_S2=c2 if n>=3 else None)
    assert counts['2']['property_S1']==0
    assert counts['3']['property_S1']>0
    assert all(counts[str(n)]['property_S2']==0 for n in range(3,7))
    # The Paley tournament on F_7, edges x->y if y-x mod 7 is a quadratic residue.
    residues={1,2,4};n=7
    E=list(combinations(range(n),2))
    mask=sum(1<<i for i,(a,b) in enumerate(E) if (b-a)%7 in residues)
    assert tournament_property(n,mask,1) and tournament_property(n,mask,2)
    out=[[(b-a)%7 in residues for a,b in E]]
    # Exact elementary union bound: for random tournament, a fixed k-set has no
    # common external dominator with probability (1-2^-k)^(N-k).
    thresholds={}
    for k in (1,2,3):
        for N in range(k+1,1001):
            q=2**k
            if comb(N,k)*(q-1)**(N-k)<q**(N-k):
                thresholds[str(k)]=dict(N=N,union_bound_numerator=comb(N,k)*(q-1)**(N-k),
                    union_bound_denominator=q**(N-k))
                break
        assert str(k) in thresholds
    return dict(exhaustive_tournaments=counts,paley7=dict(vertices=7,
                quadratic_residues=sorted(residues),directed_edge_mask=mask,
                property_S2_verified=True),
                paley67=paley67_certificate(),
                prob_method='union bound: binomial(N,k)(1-2^-k)^(N-k)<1',
                sufficient_N=thresholds,
                claim_boundary='f(2)=7 additionally requires impossibility for N=6, checked exhaustively')

def main():
    j=dict(record_type='EC_BULK_006_900_902_FINITE/1',
      authority='EXACT_FINITE_ONLY; random graph full theorem and tournament asymptotics IMPORTED',
      p900=graph_exhaustive(),p902=tournament_exhaustive())
    print(json.dumps(j,indent=2,sort_keys=True))
if __name__=='__main__':main()
