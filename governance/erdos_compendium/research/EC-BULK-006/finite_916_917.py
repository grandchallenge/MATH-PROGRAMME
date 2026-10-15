#!/usr/bin/env python3
"""Exact finite regressions for GCL Erdős #916 and #917; no infinite proof."""
from itertools import combinations, permutations
import json

def edge_index(n):
    return {e:i for i,e in enumerate(combinations(range(n),2))}

def adjacency(n,mask,idx):
    a=[0]*n
    for (u,v),i in idx.items():
        if mask>>i&1: a[u]|=1<<v; a[v]|=1<<u
    return a

def cycles(n,idx):
    out=[]
    for size in range(3,n+1):
        for vertices in combinations(range(n),size):
            root=vertices[0]
            for rest in permutations(vertices[1:]):
                if rest[0]>rest[-1]: continue
                seq=(root,)+rest
                edges=[tuple(sorted((seq[j],seq[(j+1)%size]))) for j in range(size)]
                out.append((sum(1<<v for v in vertices),sum(1<<idx[e] for e in edges)))
    return out

def special_cycle(G,n,idx,cyc):
    a=adjacency(n,G,idx)
    for vs,es in cyc:
        if G&es!=es: continue
        for v in range(n):
            if not(vs>>v&1) and (a[v]&vs).bit_count()>=3: return True
    return False

def sharp_916(n):
    idx=edge_index(n)
    es=[(0,1)]+[(v,u) for v in range(2,n) for u in (0,1)]
    mask=sum(1<<idx[tuple(sorted(e))] for e in es)
    assert mask.bit_count()==2*n-3
    assert not special_cycle(mask,n,idx,cycles(n,idx))
    return len(es)

def join_odd_cycles(q):
    l=2*q+1;n=2*l
    edges=set()
    for start in (0,l):
        for i in range(l):
            edges.add(tuple(sorted((start+i,start+(i+1)%l))))
    for u in range(l):
        for v in range(l,2*l):edges.add((u,v))
    return n,sorted(edges)

def cycle_path_coloring(l,start,deleted,colors):
    # Delete one cycle edge; the remaining connected path is bipartite.
    a={v:set() for v in range(start,start+l)}
    for i in range(l):
        u=start+i;v=start+(i+1)%l
        if tuple(sorted((u,v)))==deleted:continue
        a[u].add(v);a[v].add(u)
    col={start:colors[0]};q=[start]
    for u in q:
        for v in sorted(a[u]):
            want=colors[1] if col[u]==colors[0] else colors[0]
            if v not in col:col[v]=want;q.append(v)
            else:assert col[v]==want
    assert len(col)==l
    return col

def cycle_unique_coloring(l,start,special,colors):
    col={special:colors[0]}
    for step in range(1,l):
        v=start+(special-start+step)%l
        col[v]=colors[1] if step%2 else colors[2]
    return col

def verify_join(q):
    n,edges=join_odd_cycles(q);l=n//2;S=set(edges)
    assert len(S)==l*l+2*l
    assert len(S)==4*q*q+8*q+3
    assert n==4*q+2
    # Each factor is an odd cycle, so chi(join)=3+3=6.
    # Exhibit a proper five-colouring after deleting EVERY edge.
    for e in edges:
        u,v=e
        if u<l<=v:
            c=cycle_unique_coloring(l,0,u,(0,1,2))
            c.update(cycle_unique_coloring(l,l,v,(0,3,4)))
        elif v<l:
            c=cycle_path_coloring(l,0,e,(0,1))
            c.update(cycle_unique_coloring(l,l,l,(2,3,4)))
        else:
            c=cycle_unique_coloring(l,0,0,(0,1,2))
            c.update(cycle_path_coloring(l,l,e,(3,4)))
        assert len(c)==n and len(set(c.values()))<=5
        assert all(c[x]!=c[y] for x,y in S if (x,y)!=e),(q,e)
    return {"q":q,"vertices":n,"edges":len(S),"edge_deletion_coloring_certificates":len(S)}

def main():
    stats={"graphs_enumerated":0,"eligible_916":0,"witnesses_916":0,"by_n":{}}
    for n in range(2,7):
        idx=edge_index(n);cyc=cycles(n,idx)
        count=0;eligible=0
        for G in range(1<<len(idx)):
            count+=1
            if G.bit_count()<2*n-2:continue
            eligible+=1
            assert special_cycle(G,n,idx,cyc),(n,G)
        stats["graphs_enumerated"]+=count
        stats["eligible_916"]+=eligible
        stats["witnesses_916"]+=eligible
        stats["by_n"][str(n)]={"graphs":count,"eligible":eligible}
    stats["sharp_916"]={str(n):sharp_916(n) for n in range(4,8)}
    stats["join_917"]=[verify_join(q) for q in range(1,5)]
    assert stats["graphs_enumerated"]==33866
    assert stats["eligible_916"]==5001
    print(json.dumps(stats,indent=2,sort_keys=True))
if __name__=="__main__":main()
