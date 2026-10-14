#!/usr/bin/env python3
"""Exact finite coprime-graph and reciprocal divisor-gap tests for #883–884."""
import json
from fractions import Fraction
from math import gcd,isqrt

def threshold(n):
    return n//2+n//3-n//6

def adjacencies(n):
    return [sum(1<<(v-1) for v in range(1,n+1) if v!=u and gcd(u,v)==1) for u in range(1,n+1)]

def triangle(vertices,adj):
    mask=sum(1<<v for v in vertices)
    for i in vertices:
        nbr=adj[i]&mask
        while nbr:
            bit=nbr&-nbr;nbr-=bit
            j=bit.bit_length()-1
            if adj[i]&adj[j]&mask:return True
    return False

def triangle_independent(vertices):
    for i,a in enumerate(vertices):
        for j in range(i+1,len(vertices)):
            b=vertices[j]
            if gcd(a+1,b+1)>1:continue
            for c in vertices[j+1:]:
                if gcd(a+1,c+1)==gcd(b+1,c+1)==1:return True
    return False

def cycle(vertices,adj,length):
    if length==3:return triangle(vertices,adj)
    def seek(start,current,seen):
        if len(seen)==length:return bool(adj[current]&(1<<start))
        for nxt in vertices:
            if nxt<=start or nxt in seen or not (adj[current]&(1<<nxt)):continue
            if seek(start,nxt,seen|{nxt}):return True
        return False
    return any(seek(start,start,{start}) for start in vertices)

def finite_883():
    out=[]
    for n in range(3,13):
        B=[i for i in range(1,n+1) if i%2==0 or i%3==0]
        assert len(B)==threshold(n)
        adj=adjacencies(n)
        assert not triangle([x-1 for x in B],adj)
        lengths=list(range(3,min(n,int(n/3+1))+1,2))
        counts={str(L):0 for L in lengths}
        first={str(L):None for L in lengths}
        total=0
        for mask in range(1<<n):
            if mask.bit_count()<=threshold(n):continue
            V=[i for i in range(n) if mask>>i&1]
            total+=1
            assert triangle(V,adj)==triangle_independent(V)
            for L in lengths:
                ok=cycle(V,adj,L)
                counts[str(L)]+=int(ok)
                if not ok and first[str(L)] is None:first[str(L)]=[x+1 for x in V]
        out.append(dict(N=n,threshold=threshold(n),extremal_mod_2_or_3=B,
                        subsets_strictly_above_threshold=total,cycle_lengths_tested=lengths,
                        cycle_present_counts=counts,first_counterexamples=first))
    return out

def divisors(n):
    lo=[];hi=[]
    for d in range(1,isqrt(n)+1):
        if n%d==0:
            lo.append(d)
            if d*d!=n:hi.append(n//d)
    return lo+hi[::-1]

def energy(n):
    d=divisors(n);t=len(d)
    S=sum((Fraction(1,d[i+1]-d[i]) for i in range(t-1)),Fraction())
    T=sum((Fraction(1,d[j]-d[i]) for i in range(t) for j in range(i+1,t)),Fraction())
    H=sum((Fraction(1,j) for j in range(1,t)),Fraction())
    assert T<=H*S
    return d,S,T,T/(1+S),H

def finite_884():
    samples=[];best=(Fraction(-1),0,[])
    for n in range(2,1201):
        d,S,T,R,H=energy(n)
        assert all(d[i]<d[i+1] and n%d[i]==0 for i in range(len(d)-1))
        if R>best[0]:best=(R,n,d)
        if n<=24 or n%50==0 or R==best[0]:
            samples.append(dict(n=n,tau=len(d),S=str(S),T=str(T),
                                ratio_T_over_1_plus_S=str(R),harmonic_upper_H_tau_minus_1=str(H)))
    return dict(n_range=[2,1200],largest_ratio_n=best[1],
                largest_ratio=str(best[0]),largest_ratio_divisors=best[2],samples=samples)

def main():
    out=dict(record_type='EC_BULK_006_883_884_FINITE/1',
             scope='finite exact enumeration only; no infinite theorem inferred',
             p883=finite_883(),p884=finite_884())
    print(json.dumps(out,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
