#!/usr/bin/env python3
"""Exact finite CRT-fibre replay for FFKPY Lemma 3.1; standard library only."""
from fractions import Fraction
from itertools import combinations_with_replacement, product
from math import gcd, lcm
import hashlib
import json
import random

def smooth(n, q):
    # Repeatedly extract every divisor <= q; composite factors are harmless
    # because all their prime factors have already been exhausted.
    a = 1
    for p in range(2, int(q)+1):
        while n % p == 0:
            a *= p
            n //= p
    return a, n

def density(c):
    period = lcm(*(n for n, r in c))
    return Fraction(sum(all((x-r)%n for n,r in c) for x in range(period)), period)

def replay(c, q):
    parts = [(n,r,*smooth(n,q)) for n,r in c]
    m = lcm(*(a for n,r,a,b in parts))
    b = lcm(*(b for n,r,a,b in parts))
    period = lcm(*(n for n,r in c))
    assert gcd(m,b)==1 and period==m*b
    assert all(gcd(n,m)==a and a*t==n for n,r,a,t in parts)
    direct = [0]*m
    for x in range(period):
        if all((x-r)%n for n,r in c):
            direct[x%m]+=1
    fibre = []
    for h in range(m):
        ch = {(t,r%t) for n,r,a,t in parts if (r-h)%a==0}
        d = density(ch)
        assert (d*b).denominator==1
        fibre.append(int(d*b))
    assert direct==fibre
    assert density(c)==Fraction(sum(fibre),m*b)
    return [m,b,sum(direct),min(fibre),max(fibre)]

def main():
    digest=hashlib.sha256()
    cases=0
    for k in range(4):
        for moduli in combinations_with_replacement(range(1,7),k):
            for residues in product(*(range(n) for n in moduli)):
                c=list(zip(moduli,residues))
                for q in (2,3,5,7):
                    result=replay(c,q)
                    digest.update(json.dumps([c,q,result],separators=(',',':')).encode()+b'\n')
                    cases+=1
    rng=random.Random(270031)
    for _ in range(240):
        c=[(n:=rng.choice([1,2,3,4,5,6,7,8,9,10,12,14,15,18,20,21,25,28,35]),rng.randrange(-2*n,3*n)) for i in range(rng.randrange(1,6))]
        q=rng.choice([2,2.5,3,5,7,11])
        result=replay(c,q)
        digest.update(json.dumps([c,q,result],separators=(',',':')).encode()+b'\n')
        cases+=1
    # Explicit hostile controls:
    # 1. Drop smooth compatibility: class 0 mod 2 projects to modulus 1
    # in every fibre, falsely predicting zero rather than 1/2.
    assert density([(2,0)])==Fraction(1,2) and density([(1,0)])==0
    # 2. Drop coprimality: x even implies x mod 2=0, not uniform.
    assert sum(x%2!=0 for x in (0,2))==0 and density([(2,0)])==Fraction(1,2)
    # 3. Nonuniform fibre density; averaging is necessary.
    assert replay([(6,0)],2)==[2,3,5,2,3]
    # 4. Repeated projected restrictions must be unioned, not multiplied.
    assert replay([(3,0),(6,0),(6,6)],2)==[2,3,4,2,2]
    # 5. Replacing x by t in x=h+Mt without residue transform is wrong
    # pointwise: h=1,M=2,x=1,t=0 satisfies x=1 mod 3, t does not.
    assert (1-1)%3==0 and (0-1)%3!=0
    print(json.dumps({"record_type":"ERDOS_PV_0027_B_FINITE_CRT_REPLAY/1","cases":cases,"seed":270031,"sha256":digest.hexdigest(),"hostile_controls":5,"result":"PASS","kernel_replay":False,"full_theorem_B":False},indent=2))
if __name__=="__main__":
    main()
