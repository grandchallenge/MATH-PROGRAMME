#!/usr/bin/env python3
"""Full core plus degree-one leaves at k=D+2 maximum degree vertices.

A degree-D core vertex is attached to exactly d_M(v)-1 pendant leaves,
where M is the complement of G[C] in K_(D+2), and d_M(v)>=1.

Find degree-(alpha,beta) edge partition iff choose red core edges s.t.
alpha-(d_M(v)-1)<=redcoredegree(v)<=alpha.
"""
import itertools, collections, json

def trial(D, alpha, M, want_witness=False):
    n=D+2
    E=[(u,v) for u in range(n) for v in range(u+1,n) if not (M>> (v*(v-1)//2+u))&1]
    md=[0]*n
    for v in range(1,n):
        for u in range(v):
            if (M>> (v*(v-1)//2+u))&1:
                md[u]+=1;md[v]+=1
    if min(md)<1:return None
    low=[max(0,alpha-(k-1)) for k in md]
    hi=[min(alpha,D+1-k) for k in md]
    if any(a>b for a,b in zip(low,hi)):return False
    deg=[0]*n;rem=[0]*n
    for u,v in E:rem[u]+=1;rem[v]+=1
    # Order scarce high demand first, simple heuristic
    E.sort(key=lambda uv:-(low[uv[0]]+low[uv[1]]))
    def go(i):
        if i==len(E):return all(low[v]<=deg[v]<=hi[v] for v in range(n))
        u,v=E[i];rem[u]-=1;rem[v]-=1
        for c in (1,0):
            deg[u]+=c;deg[v]+=c
            if deg[u]<=hi[u] and deg[v]<=hi[v] and deg[u]+rem[u]>=low[u] and deg[v]+rem[v]>=low[v]:
                if go(i+1):return True
            deg[u]-=c;deg[v]-=c
        rem[u]+=1;rem[v]+=1
        return False
    return go(0)

def core_has_isolated_KD1(D,M):
    n=D+2
    # n=D+2, a K_(D+1) component => one exceptional vertex of n
    # one vertex w has all missing edges to other D+1 (no core edges), and
    # all remaining vertices have missing degree=1
    return any(all((M>>(max(u,v)*(max(u,v)-1)//2+min(u,v)))&1 for v in range(n) if v!=u) for u in range(n))

def full(D):
    n=D+2; E=n*(n-1)//2
    total=0;fails=collections.Counter(); fail_details=[]
    for M in range(1<<E):
        md=[0]*n
        for v in range(1,n):
            for u in range(v):
                if (M>> (v*(v-1)//2+u))&1:md[u]+=1;md[v]+=1
        if min(md)<1: continue
        total+=1
        for a in range(1,D):
            test=trial(D,a,M)
            if test is False:
                special=core_has_isolated_KD1(D,M)
                fails[(a,special)]+=1
                if not special and len(fail_details)<10:fail_details.append((D,a,M,md))
    return {'D':D,'tested_missing_graphs':total,'failures':{str(k):v for k,v in fails.items()},'non_KD1_failures':fail_details}
if __name__=='__main__':
    for d in (2,3,4):
        res=full(d);print(json.dumps(res),flush=True)
