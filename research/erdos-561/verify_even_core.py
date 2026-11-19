#!/usr/bin/env python3
"""Exact constructive parity/core-partition verifier, no external packages."""
from itertools import combinations, combinations_with_replacement
from collections import Counter
import json

def canon(u,v):return (u,v) if u<v else (v,u)

def hamilton(n):
    assert n%2==1 and n>=3
    D=n-1;k=D//2;cycles=[]
    for s in range(k):
        ring=[n-1,s]
        for i in range(1,k):ring.extend([(s-i)%D,(s+i)%D])
        ring.append((s-k)%D)
        assert len(ring)==n and len(set(ring))==n
        cycles.append([canon(ring[i],ring[(i+1)%n]) for i in range(n)])
    assert sorted(e for c in cycles for e in c)==list(combinations(range(n),2))
    return cycles

def one_factors(n):
    assert n%2==0 and n>=4
    P=n-1;fs=[]
    for s in range(P):
        edges=[canon(n-1,s)]
        for i in range(1,n//2):edges.append(canon((s+i)%P,(s-i)%P))
        assert len({v for e in edges for v in e})==n
        fs.append(edges)
    assert sorted(e for f in fs for e in f)==list(combinations(range(n),2))
    return fs

def split_core(D,alpha,missing):
    assert D>=2 and 1<=alpha<D
    beta=D-alpha; n=D+1
    missing=set(missing)
    every=set(combinations(range(n),2))
    assert missing<=every
    # Assign red/blue to all complete-core edges except, in the odd/odd case,
    # a distinguished deleted edge, which receives one red and one blue stub.
    coloring={}; special=None; first=None; last=None
    if D%2:
        for col,factor in enumerate(one_factors(n)):
            for e in factor:coloring[e]=int(col<alpha)
    else:
        cycles=hamilton(n)
        if alpha%2==0:
            for ci,cycle in enumerate(cycles):
                for e in cycle:coloring[e]=int(ci<alpha//2)
        else:
            if not missing:return None
            special=min(missing)
            special_cycle=next(i for i,cy in enumerate(cycles) if special in cy)
            other=[i for i in range(len(cycles)) if i!=special_cycle]
            for j,i in enumerate(other):
                for e in cycles[i]:coloring[e]=int(j<(alpha-1)//2)
            cyc=cycles[special_cycle]
            # Recover cycle vertex order by walking an n-cycle edge set.
            adj={i:[] for i in range(n)}
            for u,v in cyc:adj[u].append(v);adj[v].append(u)
            a,b=special
            path=[a,b];prev=a;cur=b
            # Walk the long path from a to b with special edge removed:
            path=[a];prev=b;cur=a
            while cur!=b:
                nxt=next(v for v in adj[cur] if v!=prev)
                path.append(nxt);prev,cur=cur,nxt
            assert len(path)==n
            # D=n-1 is even, so first and last path edges have different colours.
            for i in range(n-1):coloring[canon(path[i],path[i+1])]=int(i%2==0)
            first,last=path[0],path[-1]
            assert canon(first,last)==special
    red=[0]*n;blue=[0]*n
    assignments=[]
    for e in every:
        if e==special:continue
        c=coloring[e]
        if e in missing:
            assignments.extend([(e[0],c),(e[1],c)])
        else:
            (red if c else blue)[e[0]]+=1
            (red if c else blue)[e[1]]+=1
    if special is not None:
        # Alternating path starts red; at the first endpoint blue is deficient,
        # and at the last endpoint red is deficient.
        assignments.extend([(first,0),(last,1)])
    for u,c in assignments:(red if c else blue)[u]+=1
    assert red==[alpha]*n,(D,alpha,missing,red)
    assert blue==[beta]*n,(D,alpha,missing,blue)
    return len(assignments)

def check_construction():
    stats=Counter()
    for D in (2,3,4,5,6,7,8):
        n=D+1;edges=list(combinations(range(n),2))
        if D<=4:
            masks=range(1<<len(edges))
            patterns=([edges[i] for i in range(len(edges)) if (mask>>i)&1] for mask in masks)
        else:
            limit=2 if D>=7 else 3
            patterns=(list(combo) for size in range(limit+1) for combo in combinations(edges,size))
        for missing in patterns:
            for alpha in range(1,D):
                got=split_core(D,alpha,missing)
                assert (got is None)==(D%2==0 and alpha%2==1 and not missing)
                if got is not None:assert got==2*len(missing)
                stats['valid_parameter_graph_cases']+=1
                if got is None:stats['odd_odd_complete_core_obstructions']+=1
    return dict(stats)

def diagonals(n,m):
    return sum(max(n[i]+m[k-i]-1 for i in range(3) if 0<=k-i<3) for k in range(5))

def filter_three_star():
    ts=[v[::-1] for v in combinations_with_replacement(range(1,10),3) if v[-1]>=2]
    retained=[];new=[];odd=[];stats=Counter()
    for n in ts:
        for m in ts:
            D=n[0]+m[0]-2
            if D>=10:continue
            E=diagonals(n,m)-1;T=D*(D+1)//2
            if E<T:continue
            R=max(sum(n)+3,sum(m)+3);B=2*E-D*D+1
            if R>B:continue
            if R==B and min(sum(n)+3,sum(m)+3)>D+1 and E-T<max(n[0],m[0]):continue
            stats['old_851']+=1
            if R==B and D%2:stats['old_odd_six']+=1;odd.append((n,m))
            elif R==B and D%2==0 and E>T:
                stats['new_even_exclusions']+=1;new.append({'red':n,'blue':m,'W':E+1,'D':D,'edges':E,'core_T':T})
            else:retained.append((n,m))
    assert (stats['old_851'],stats['old_odd_six'],stats['new_even_exclusions'],len(retained))==(851,6,10,835),stats
    return dict(stats),new,len(retained)

if __name__=='__main__':
 c=check_construction();s,x,n=filter_three_star()
 print(json.dumps({'core_exact_tests':c,'parameter_filter':s,'new_exclusions':x,'remaining_after_both_parity_gates':n},indent=2,default=list))
