#!/usr/bin/env python3
"""Exact bounded arithmetic for four original #561 odd-leading families.
No claim to computationally prove arbitrary-host Ramsey arrowing.
"""
def diagonal(n,m):
    return tuple(max(n[i]+m[j]-1 for i in range(len(n)) for j in range(len(m)) if i+j==k)
                 for k in range(len(n)+len(m)-1))

def diagonal_independent(n,m):
    return tuple(max(n[i-1]+m[k-i-1]-1 for i in range(1,len(n)+1)
                     if 1<=k-i<=len(m))
                 for k in range(2,len(n)+len(m)+1))

def audit(n,m,predicted_joint,predicted_original):
    w=diagonal(n,m)
    assert w==diagonal_independent(n,m)
    assert w[0]==n[0]+m[0]-1
    assert sum(w[1:])==predicted_joint,(n,m,w,predicted_joint)
    assert sum(w)==predicted_original,(n,m,w,predicted_original)
    assert predicted_joint+predicted_original-predicted_joint==predicted_original
    assert all(x>0 for x in n+m) and n[0]%2==1 and m[0]%2==1
    return 1

counts={"B1":0,"B2":0,"B3":0,"B4":0}
for t in range(4,9):
    for a in range(3,14,2):
        for c in range(1,a+1):
            for b in range(3,23,2):
                if b<a+c-1:continue
                n=(a,1,1);m=(b,c)+(1,)*(t-2)
                counts["B1"]+=audit(n,m,2*b+(t-3)*a+2,3*b+(t-2)*a+1)
for s in range(3,10):
    for t in range(3,10):
        for a in range(3,16,2):
            n=(a,)+(1,)*(s-1);m=(a,)+(1,)*(t-1)
            counts["B2"]+=audit(n,m,(max(s,t)-1)*a+min(s,t)-1,(max(s,t)+1)*a+min(s,t)-2)
for a in range(5,30,2):
    counts["B3"]+=audit((a,2,1),(a,1,1,1),3*a+4,5*a+3)
for a in range(3,16,2):
    for b in range(3,37,2):
        if b<2*a-2:continue
        counts["B4"]+=audit((a,1,1),(b,a-1,2,1),2*b+a+3,3*b+2*a+2)
assert all(v>0 for v in counts.values())
print("ERDOS561_EVEN_CAP_ORIGINAL_TRANSFER_FAMILIES_PASS",counts,"total",sum(counts.values()))
