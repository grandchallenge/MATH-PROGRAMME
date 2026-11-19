#!/usr/bin/env python3
"""Independent bounded brute-force near-equality cap feasibility + integer Ramsey gates."""
from itertools import combinations, combinations_with_replacement
from collections import Counter
import json

def can_split(D,alpha,missing,pair):
    # Build a degree-D core on D+1 vertices with missing edges replaced by
    # pendant stubs, with one degree-two outsider joining the core pair.
    n=D+1; missing=set(missing)
    stubs=[0]*n
    for u,v in missing:stubs[u]+=1;stubs[v]+=1
    a,b=pair
    if stubs[a]==0 or stubs[b]==0:return None
    remain=[e for e in combinations(range(n),2) if e not in missing]
    low=[max(0,alpha-s) for s in stubs]
    high=[min(alpha,D-s) for s in stubs]
    red=[0]*n; rem=[0]*n
    for u,v in remain:rem[u]+=1;rem[v]+=1
    def dfs(i):
        if i==len(remain):
            if any(red[j]<low[j] or red[j]>high[j] for j in range(n)):return False
            for ru in (0,1):
                if not 0<=alpha-red[a]-ru<=stubs[a]-1:continue
                for rv in (0,1):
                    if not 0<=alpha-red[b]-rv<=stubs[b]-1:continue
                    if ru+rv<=alpha and 2-ru-rv<=D-alpha:return True
            return False
        u,v=remain[i];rem[u]-=1;rem[v]-=1
        for color in (0,1):
            red[u]+=color;red[v]+=color
            if (red[u]<=high[u] and red[v]<=high[v] and
                red[u]+rem[u]>=low[u] and red[v]+rem[v]>=low[v] and dfs(i+1)):
                return True
            red[u]-=color;red[v]-=color
        rem[u]+=1;rem[v]+=1
        return False
    return dfs(0)

def near_tests():
    out=Counter();failures=[]
    for D,maxmissing in ((3,6),(4,10),(5,2),(6,1)):
        E=list(combinations(range(D+1),2))
        if maxmissing==len(E):
            patterns=(tuple(E[i] for i in range(len(E)) if mask>>i&1)
                      for mask in range(1,1<<len(E)))
        else:
            patterns=(sub for k in range(1,maxmissing+1) for sub in combinations(E,k))
        for M in patterns:
            stubs=[0]*(D+1)
            for u,v in M:stubs[u]+=1;stubs[v]+=1
            for p in combinations([i for i,s in enumerate(stubs) if s],2):
                for alpha in range(1,D):
                    okay=can_split(D,alpha,M,p)
                    out['tested']+=1
                    if okay:out['passed']+=1
                    else:failures.append((D,alpha,M,p))
    assert not failures,failures[:10]
    return dict(out)

def weight(n,m):
    return sum(max(n[i]+m[k-i]-1 for i in range(3) if 0<=k-i<3) for k in range(5))

def original_filter():
    ts=[x[::-1] for x in combinations_with_replacement(range(1,10),3) if x[-1]>=2]
    stats=Counter();new=[];survivors=[]
    for n in ts:
        for m in ts:
            D=n[0]+m[0]-2
            if D>=10:continue
            E=weight(n,m)-1;T=D*(D+1)//2
            if E<T:continue
            B=2*E-D*D+1
            R=max(sum(n)+3,sum(m)+3)
            if R>B:continue
            if R==B and min(sum(n)+3,sum(m)+3)>D+1 and E-T<max(n[0],m[0]):continue
            stats['legacy_851']+=1
            if R==B and D%2:stats['odd_degree_excluded']+=1;continue
            if R==B and D%2==0 and E>T:stats['even_degree_equality_excluded']+=1;continue
            if B-R==1 and D>=3 and E>T:
                stats['one_slack_excluded']+=1
                new.append({'red':n,'blue':m,'D':D,'W':E+1,'required_vertices':R,'bound_vertices':B})
                continue
            survivors.append((n,m))
    assert (stats['legacy_851'],stats['odd_degree_excluded'],stats['even_degree_equality_excluded'],stats['one_slack_excluded'],len(survivors))==(851,6,10,80,755),stats
    return {'stats':dict(stats),'survivors':len(survivors),'new_one_slack_cases':new}

if __name__=='__main__':
 print(json.dumps({'independent_near_core_feasibility':near_tests(),'original_parameter_gate':original_filter()},indent=2,default=list))
