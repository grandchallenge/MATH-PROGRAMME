#!/usr/bin/env python3
"""Exact integer arithmetic: factor-difference witnesses and square subfamily intervals."""
import json
from math import isqrt

def factor_differences(n):
    assert n>=1
    return {n//a-a for a in range(1,isqrt(n)+1) if n%a==0}

def square_factor_certificate(n,d):
    """Positive factors (a,b) with n=a*b and b-a=d, if one exists."""
    q=d*d+4*n
    s=isqrt(q)
    if s*s!=q or (s-d)%2:return None
    a=(s-d)//2;b=(s+d)//2
    if a<1 or a*b!=n:return None
    return (a,b)

def verify_885():
    Ns=[79200,227205,1258560]
    Ds=[factor_differences(n) for n in Ns]
    common=sorted(set.intersection(*Ds))
    assert common==[36,468,692,1028],common
    cert={str(n):{str(d):square_factor_certificate(n,d) for d in common} for n in Ns}
    assert all(pair and pair[0]*pair[1]==n and pair[1]-pair[0]==d
        for n in Ns for d in common
        for pair in [square_factor_certificate(n,d)])
    # Every D(n) member must have the square-and-parity certificate and vice versa.
    for n in range(1,2001):
        assert factor_differences(n)=={d for d in range(n)
                      if square_factor_certificate(n,d) is not None},n
    offsets=[756000,15971200,45130176]
    anchor=[330,870,2445,4155,10482]
    roots={str(z):[isqrt(z*z+a) for a in offsets] for z in anchor}
    assert all(r*r==z*z+a for z in anchor for a,r in zip(offsets,roots[str(z)]))
    # Corrected 1028, not 1029, from the user's exact finite source note.
    assert 1029 not in common
    return dict(N=Ns,common_differences=common,factor_pairs=cert,
                square_certificate_equivalence_tested_through=2000,
                anchored_offsets=offsets,anchored_z=anchor,anchored_square_roots=roots)

def verify_886():
    # For n=t^2, sqrt(n)=t and n^(1/4)=sqrt(t).
    # For integer C, t<d<t+C*sqrt(t) iff 0<delta=d-t and delta^2<C^2*t.
    max_count={1:0,2:0,3:0}
    argmax={1:[],2:[],3:[]}
    samples={}
    for t in range(2,2001):
        n=t*t
        ds={}
        # Exact strict inequalities, with no floating-point endpoints.
        for C in (1,2,3):
            ds[C]=[t+gap for gap in range(1,3*isqrt(t)+4)
                     if gap*gap<C*C*t and n%(t+gap)==0]
            c=len(ds[C])
            # The 1997 theorem's upper bound 1+C^2 in CLOSED interval is compatible.
            assert c<=1+C*C,(t,C,c)
            if c>max_count[C]:
                max_count[C]=c;argmax[C]=[t]
            elif c==max_count[C] and len(argmax[C])<8:argmax[C].append(t)
        if t in (20,60,120,360,720,1440,2000):
            samples[t]={str(C):ds[C] for C in (1,2,3)}
    return dict(n_family="n=t^2",t_range=[2,2000],epsilon="1/4",
                strict_interval="(t,t+C*sqrt(t))",C_values=[1,2,3],
                maximum_counts={str(C):max_count[C] for C in (1,2,3)},
                first_maximum_t={str(C):argmax[C] for C in (1,2,3)},
                samples=samples,method="exact integer gap^2 < C^2*t")

def main():
    print(json.dumps(dict(record_type="EC_BULK_006_885_886_FINITE/1",
       authority="finite exact integer arithmetic only, not an infinite theorem",
       p885=verify_885(),p886=verify_886()),indent=2))
if __name__=="__main__": main()
