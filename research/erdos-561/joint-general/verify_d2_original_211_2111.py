#!/usr/bin/env python3
"""Complete degree-two 10-edge class check for original (211,2111).

All original hosts with <=10 edges have max degree <=2 by a separate,
source-proved sharp J=8 joint-residual theorem and vertex deletion.
Up to isolates, every such host after padding to 10 edges is a disjoint
union of paths/cycles; the 106 canonical component multisets are exhaustive.

Two independent ordinary non-induced disjoint-star embedding oracles compare
all 108544 red/blue allocations. This is a finite proof over the forced
degree-two equality class, not full all-host graph enumeration.
"""
from itertools import combinations
from collections import Counter
import hashlib
import json

RED=(2,1,1)
BLUE=(2,1,1,1)
E=10

def partitions(n,least=1):
    if n==0:
        yield ()
    else:
        for k in range(least,n+1):
            for rest in partitions(n-k,k):
                yield (k,)+rest

def typed(parts):
    if not parts:
        yield ()
        return
    k,*tail=parts
    for kind in (('P','C') if k>=3 else ('P',)):
        for rest in typed(tail):
            yield ((kind,k),)+rest

def classes():
    unique=set()
    for part in partitions(E):
        for seq in typed(part):
            unique.add(tuple(sorted(seq,key=lambda x:(x[1],x[0]))))
    return sorted(unique)

def edges_of(types):
    edges=[];first=0
    for kind,k in types:
        if kind=='P':
            edges.extend((first+j,first+j+1) for j in range(k))
            first+=k+1
        else:
            edges.extend((first+j,first+(j+1)%k) for j in range(k))
            first+=k
    assert len(edges)==E and len(set(tuple(sorted(e)) for e in edges))==E
    return edges

# Oracle 1: direct two-edge star + disjoint matching extraction
def contains_direct(edges,colour,tail_count):
    for i,(u,v) in enumerate(edges):
        if not colour>>i&1:continue
        for j in range(i+1,E):
            if not colour>>j&1:continue
            a,b=edges[j]
            used={u,v,a,b}
            if len(used)!=3:continue
            pool=[(x,y) for k,(x,y) in enumerate(edges) if colour>>k&1 and x not in used and y not in used]
            if tail_count==2:
                for p,(x,y) in enumerate(pool):
                    if any(len({x,y,z,w})==4 for z,w in pool[p+1:]):return True
            elif tail_count==3:
                for p,(x,y) in enumerate(pool):
                    for q in range(p+1,len(pool)):
                        z,w=pool[q]
                        if len({x,y,z,w})!=4:continue
                        if any(len({x,y,z,w,z1,w1})==6 for z1,w1 in pool[q+1:]):return True
            else:
                raise ValueError("tail_count")
    return False

# Oracle 2: independent general forest embedding construction + upward DP
def all_embeddings(edges,target):
    vs=sorted({x for e in edges for x in e})
    inds={v:i for i,v in enumerate(vs)}
    adj={v:[] for v in vs}
    for i,(u,v) in enumerate(edges):
        adj[u].append((v,i))
        adj[v].append((u,i))
    choices={}
    for k in set(target):
        current=[]
        for centre,neighbours in adj.items():
            for pick in combinations(neighbours,k):
                vb=1<<inds[centre];eb=0
                for leaf,i in pick:
                    vb|=1<<inds[leaf]
                    eb|=1<<i
                current.append((vb,eb))
        choices[k]=current
    patterns=set()
    def rec(pos,vertices,mask):
        if pos==len(target):
            patterns.add(mask)
            return
        for vb,eb in choices[target[pos]]:
            if not vb&vertices:
                rec(pos+1,vertices|vb,mask|eb)
    rec(0,0,0)
    return patterns

def upward(patterns):
    table=bytearray(1<<E)
    for m in patterns:table[m]=1
    for i in range(E):
        bit=1<<i
        for x in range(1<<E):
            if x&bit:table[x]|=table[x^bit]
    return table

def run():
    graph_types=classes()
    assert len(graph_types)==106,len(graph_types)
    counts=Counter()
    witnesses=[]
    checked=0
    for types in graph_types:
        edges=edges_of(types)
        counts[sum(kind=='C' for kind,k in types)]+=1
        R=upward(all_embeddings(edges,RED))
        B=upward(all_embeddings(edges,BLUE))
        best=None
        for red in range(1<<E):
            blue=((1<<E)-1)^red
            direct=(not contains_direct(edges,red,2) and not contains_direct(edges,blue,3))
            general=(not R[red] and not B[blue])
            assert direct==general,(types,red,direct,general)
            if direct and best is None:best=red
            checked+=1
        assert best is not None,('ARROWING_TEN_EDGE_GRAPH',types)
        witnesses.append({'types':types,'red_edge_mask':best})
    assert counts==Counter({0:42,1:45,2:17,3:2}),counts
    assert checked==106*1024
    body=json.dumps(witnesses,sort_keys=True,separators=(',',':'))
    digest=hashlib.sha256(body.encode()).hexdigest()
    assert digest=='2840d4d0a16690272b3052a33e21d8b487ce717e982879899735af3577680aaf',digest
    print("ERDOS561_D2_106_CANONICAL_CLASSES_PASS",dict(counts))
    print("ERDOS561_D2_TWO_ORACLES_108544_COLOURINGS_PASS")
    print("ERDOS561_D2_106_WITNESS_DIGEST_PASS",digest)
    return witnesses

if __name__=='__main__':
    run()
