#!/usr/bin/env python3
"""Independent complete Python search for the forced 14-edge equality
class n=321,m=4111. No imports from the C++ oracle; generates graph
attachments by combinations rather than bitmask subset iteration;
checks B necessary 2-vertex deletion by explicit F321 embeddings;
constructs A bad colorings either red star or red matching.
"""
from itertools import combinations
from collections import Counter
from functools import lru_cache
import sys,json,hashlib

base=((0,1),(0,2),(0,3),(4,5),(4,6),(7,8))


def build(A,B,h):
    G=list(base)
    G.extend((9,u) for u in A)
    G.extend((10,u) for u in B)
    v=11
    for _ in range(h):G.append((9,v));G.append((10,v));v+=1
    for _ in range(4-len(A)-h):G.append((9,v));v+=1
    for _ in range(4-len(B)-h):G.append((10,v));v+=1
    assert len(G)==14 and len({frozenset(x) for x in G})==14
    return G


def star_options(G,size):
    adj={}
    for idx,(u,v) in enumerate(G):
        adj.setdefault(u,[]).append((v,idx))
        adj.setdefault(v,[]).append((u,idx))
    ans=[]
    for c,neighbors in adj.items():
        for arm in combinations(neighbors,size):
            V=(1<<c);E=0
            for v,i in arm:V|=1<<v;E|=1<<i
            ans.append((V,E))
    return ans


def embeddings(G,target):
    choices=[star_options(G,s) for s in target]
    found=set()
    def dfs(i,V,E):
        if i==len(choices):found.add((V,E));return
        for v,e in choices[i]:
            if not V&v:dfs(i+1,V|v,E|e)
    dfs(0,0,0)
    return found


def two_hub_deletion_must_fail(G):
    patterns={v for v,e in embeddings(G,(3,2,1))}
    if not patterns:return True
    active={v for edge in G for v in edge}
    for u in active:
        survivors=(vs for vs in patterns if not vs&(1<<u))
        commons=None
        for vs in survivors:
            commons=vs if commons is None else commons&vs
            if commons==0:break
        if commons is None or commons:return True
    return False


def avoids_full_blue_with_red_matching(G,blue_masks):
    # matching red automatically avoids any red F(2,1), because a
    # matching contains no two edges incident to the same centre.
    # For every blue target copy require at least one of its edges red.
    @lru_cache(None)
    def dfs(i,used,red):
        if i==14:return red if all(p&red for p in blue_masks) else None
        res=dfs(i+1,used,red)
        if res is not None:return res
        a,b=G[i]
        if not used&((1<<a)|(1<<b)):
            return dfs(i+1,used|(1<<a)|(1<<b),red|(1<<i))
        return None
    return dfs(0,0,0)


def check(A,B,h,G):
    if two_hub_deletion_must_fail(G):return 'B_failed_vertex_pair',None
    blue=embeddings(G,(4,1,1,1))
    if not blue:return 'A_failed_no_blue_forest',0
    common=(1<<25)-1
    for v,e in blue:common &=v
    if common:
        v=(common&-common).bit_length()-1
        mask=sum(1<<i for i,(a,b) in enumerate(G) if a==v or b==v)
        assert all(e&mask for v2,e in blue)
        return 'A_failed_red_star',mask
    hit=avoids_full_blue_with_red_matching(G,[e for v,e in blue])
    if hit is not None:
        assert all(e&hit for v,e in blue)
        return 'A_failed_red_matching',hit
    raise AssertionError(('UNCLASSIFIED',A,B,h,G))

if __name__=='__main__':
 subsets=[tuple(c) for k in range(5) for c in combinations(range(9),k)]
 lo=int(sys.argv[1]) if len(sys.argv)>1 else 0
 hi=int(sys.argv[2]) if len(sys.argv)>2 else len(subsets)
 totals=Counter();proofs=[];checksum=hashlib.sha256()
 for A in subsets[lo:hi]:
    for B in subsets:
        if 0 in A and 0 in B:continue
        for h in range(min(4-len(A),4-len(B))+1):
            G=build(A,B,h)
            totals['generated']+=1
            verdict,mask=check(A,B,h,G)
            totals[verdict]+=1
            if verdict=='A_failed_red_matching':
                proofs.append({'A':list(A),'B':list(B),'h':h,'red_matching_edges':[G[i] for i in range(14) if mask&(1<<i)]})
            checksum.update(bytes([len(A),len(B),h])+bytes(A)+b'|'+bytes(B)+b'\n')
 if lo==0 and hi==256:
    expected={'generated':74553,'B_failed_vertex_pair':72512,
              'A_failed_red_star':1914,'A_failed_red_matching':127}
    assert totals==expected,(totals,expected)
    assert len(proofs)==127
    record={'record_type':'ERDOS561_JOINT_RIGID14_FINITE_CERTIFICATE/1',
       'red_target_original':[3,2,1],'blue_target_original':[4,1,1,1],
       'first_residual_red':[2,1],'first_residual_blue':[4,1,1,1],
       'second_residual_red':[3,2,1],'second_residual_blue':[1,1,1],
       'J':15,'ruled_out_edge_budget':14,'classification':dict(totals),
       'generation_order_sha256':checksum.hexdigest(),
       'red_matching_witnesses':proofs,
       'counterexamples':0,'independent_implementations':['verify_rigid14_exact.cpp','verify_rigid14_independent.py'],
       'mathematical_scope':'exact 3x4 joint residual case; not full conjecture'}
    from pathlib import Path
    Path(__file__).with_name('RIGID_14EDGE_CERTIFICATE.json').write_text(json.dumps(record,indent=2)+'\n')
 print('RIGID14_INDEPENDENT_PYTHON_PASS',json.dumps({'start':lo,'stop':hi,'counts':dict(totals),'generation_sha256':checksum.hexdigest(),'red_matching_witness_count':len(proofs)}),flush=True)
