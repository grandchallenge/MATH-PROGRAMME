#!/usr/bin/env python3
"""Independent Python verification of all degree-two component types.
Unlike the C++ implementation, construct actual target embeddings from
vertex-disjoint edge patterns, then use subset upward closure of edge masks.
"""
from collections import Counter

TARGETS=[((2,1,1),(2,1,1),8),((2,1,1),(2,2,1),10),
         ((2,1,1),(2,2,2),12),((2,2,1),(2,2,1),11),
         ((2,2,1),(2,2,2),13),((2,2,2),(2,2,2),14)]
COUNTS={8:46,10:106,11:156,12:232,13:334,14:482}

def graph_types(e):
    # All multisets of edge-bearing path/cycle components with total e edges.
    kinds=tuple((n,c) for n in range(1,e+1) for c in ((False,True) if n>=3 else (False,)))
    def rec(k,remain,cs):
        if remain==0:
            yield tuple(cs)
            return
        for i in range(k,len(kinds)):
            length,cyclic=kinds[i]
            if length>remain:break
            cs.append((length,cyclic))
            yield from rec(i,remain-length,cs)
            cs.pop()
    yield from rec(0,e,[])

def graph_edges(cs):
    edges=[];offset=0
    for length,cyclic in cs:
        for i in range(length):
            edges.append((offset+i,offset+(i+1)%length if cyclic else offset+i+1))
        offset+=length if cyclic else length+1
    return tuple(edges)

def placement_masks(edges):
    pat1=[(1<<i,(1<<u)|(1<<v)) for i,(u,v) in enumerate(edges)]
    pat2=[]
    for i,(a,b) in enumerate(edges):
        for j in range(i+1,len(edges)):
            c,d=edges[j]
            v={a,b,c,d}
            if len(v)==3:
                vm=0
                for x in v:vm|=1<<x
                pat2.append(((1<<i)|(1<<j),vm))
    return {1:pat1,2:pat2}

def embeddings(placements,target):
    found=set()
    def rec(k,usedv,usededges):
        if k==3:
            found.add(usededges)
            return
        for em,vm in placements[target[k]]:
            if not usedv&vm:
                rec(k+1,usedv|vm,usededges|em)
    rec(0,0,0)
    return found

def contains_table(edgecount,embeds):
    size=1<<edgecount
    contains=bytearray(size)
    for em in embeds:contains[em]=1
    # Standard subset transform, independently implemented.
    for i in range(edgecount):
        bit=1<<i
        for m in range(size):
            if m&bit:
                contains[m] |=contains[m^bit]
    return contains

def check_case(red,blue,e):
    graphcount=0
    for cs in graph_types(e):
        graphcount+=1
        edges=graph_edges(cs)
        assert len(edges)==e
        pat=placement_masks(edges)
        R=contains_table(e,embeddings(pat,red))
        B=contains_table(e,embeddings(pat,blue))
        allmask=(1<<e)-1
        if not any((not R[m] and not B[allmask^m]) for m in range(1<<e)):
            raise AssertionError(('ARROWING_GRAPH',red,blue,cs))
    assert graphcount==COUNTS[e],(e,graphcount)
    print('INDEPENDENT_D2_CASE_PASS',red,blue,'E',e,'graph_types',graphcount,flush=True)

if __name__=='__main__':
    for pair in TARGETS:check_case(*pair)
    print('INDEPENDENT_DEGREE2_FULL_CORPUS_PASS',sum(COUNTS.values()))
