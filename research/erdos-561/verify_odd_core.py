#!/usr/bin/env python3
"""Independent exact finite odd-core gate for Erdős #561 3x3 pairs. No third-party dependencies."""
from itertools import combinations_with_replacement
from collections import Counter
import json

def weights(n,m):
    return [max(n[i]+m[j]-1 for i in range(3) for j in range(3) if i+j==k)
            for k in range(5)]

T=[tuple(reversed(x)) for x in combinations_with_replacement(range(1,10),3) if x[-1]>=2]
counts=Counter()
new=[]
for n in T:
    for m in T:
        D=n[0]+m[0]-2
        if D>=10: continue
        counts["small_pairs"]+=1
        W=sum(weights(n,m))
        E=W-1
        M=D*(D+1)//2
        if E<M:
            counts["edge_budget"]+=1
            continue
        V=max(sum(n)+3,sum(m)+3)
        B=2*E-D*D+1
        if V>B:
            counts["vertex_budget"]+=1
            continue
        if V==B and min(sum(n)+3,sum(m)+3)>D+1 and E-M<max(n[0],m[0]):
            counts["previous_equality_gate"]+=1
            continue
        counts["old_survivors"]+=1
        if D%2 and V==B:
            new.append({"n":n,"m":m,"W":W,"D":D,"vplus_bound":B})
        else:
            counts["new_survivors"]+=1

counts["newly_resolved"]=len(new)
assert counts==Counter(small_pairs=4566,edge_budget=2725,vertex_budget=918,
                      previous_equality_gate=72,old_survivors=851,
                      newly_resolved=6,new_survivors=845),counts

# Independently check an explicit 1-factorization of K_{D+1}, D odd.
for D in (3,5,7,9):
    color={}
    for t in range(D):
        color[tuple(sorted((D,t)))]=t
        for i in range(1,(D+1)//2):
            color[tuple(sorted(((t+i)%D,(t-i)%D)))]=t
    assert len(color)==D*(D+1)//2
    for v in range(D+1):
        incident=[c for (u,w),c in color.items() if v in (u,w)]
        assert len(incident)==D and len(set(incident))==D




# Independent 1..10 parameter enumeration for the strengthened core-threshold corollary.
def general_weights(a,b):
    return [max(a[i]+b[j]-1 for i in range(len(a)) for j in range(len(b)) if i+j==k)
            for k in range(len(a)+len(b)-1)]

T10=[tuple(reversed(x)) for x in combinations_with_replacement(range(1,11),3) if x[-1]>=2]
bounded=Counter()
for n in T10:
    for m in T10:
        w=general_weights(n,m)
        W=sum(w)
        sigma=W-w[0]-max(sum(general_weights(n[1:],m)),sum(general_weights(n,m[1:])))
        assert sigma>=0
        bounded["all_pairs"]+=1
        if sigma==0: bounded["zero_switch"]+=1
        if W<=(n[0]+m[0]-2)*(n[0]+m[0]-1)//2:
            bounded["core_threshold"]+=1
            if sigma==0: bounded["core_threshold_zero_switch"]+=1
            else: bounded["core_threshold_positive_switch"]+=1
assert bounded==Counter(all_pairs=47961,zero_switch=44893,core_threshold=46120,
                        core_threshold_zero_switch=43066,core_threshold_positive_switch=3054),bounded
print(json.dumps({"counts":dict(counts),"newly_resolved":new,"bounded_1_to_10":dict(bounded)},indent=2))
