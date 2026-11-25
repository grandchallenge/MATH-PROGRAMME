"""Independent trial-division and divisor enumeration for the smooth/rough split."""
from fractions import Fraction
from math import gcd, lcm, isqrt
from pathlib import Path
import hashlib
import json
import random

def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p)+1))

def split(n,q):
    a,b=1,n
    for p in range(2,q+1):
        if prime(p):
            while b%p==0:
                a*=p
                b//=p
    return a,b

def run():
    digest=hashlib.sha256()
    pairs=0
    powers=0
    for n in range(1,1001):
        pp=[p for p in range(2,n+1) if n%p==0 and prime(p)]
        for q in range(32):
            a,b=split(n,q)
            assert a*b==n and gcd(a,b)==1
            # Independent divisor definition: largest divisor with no prime above q.
            smooth_divisors=[d for d in range(1,n+1) if n%d==0
                             and all(d%p for p in pp if p>q)]
            assert a==max(smooth_divisors)
            for p in pp:
                power=p
                while n%power==0:
                    assert (a%power==0)==(p<=q)
                    assert (b%power==0)==(p>q)
                    power*=p
                    powers+=1
            digest.update(f'{n},{q},{a},{b}\n'.encode())
            pairs+=1
    rng=random.Random(270031)
    families=0
    for t in (1,60,120,210,360,420):
        divs=[n for n in range(1,t+1) if t%n==0]
        for _ in range(80):
            ns=[rng.choice(divs) for _ in range(rng.randrange(0,8))]
            rs=[rng.randrange(-2*t,2*t+1) for _ in ns]
            q=rng.randrange(0,17)
            ab=[split(n,q) for n in ns]
            M=lcm(*(a for a,b in ab));B=lcm(*(b for a,b in ab))
            T=lcm(*ns)
            assert M*B==T and gcd(M,B)==1
            direct=sum(all(x%n!=r%n for n,r in zip(ns,rs)) for x in range(T))
            fibres=sum(sum(all(h%a!=r%a or y%b!=r%b
                               for (a,b),r in zip(ab,rs))
                           for y in range(B)) for h in range(M))
            assert Fraction(direct,T)==Fraction(fibres,M*B)
            digest.update(repr((q,ns,rs,M,B,direct,fibres)).encode()+b'\n')
            families+=1
    # Hostile examples: splitting one occurrence of a small prime is not enough;
    # treating non-coprime factors as independent CRT coordinates is not valid.
    assert split(72,2)==(8,9) and gcd(2,36)>1
    assert len({(x%4,x%6) for x in range(12)})<4*6
    return dict(result="PASS",modulus_cutoff_pairs=pairs,prime_power_checks=powers,
                fibre_families=families,hostile_controls=2,digest=digest.hexdigest())

if __name__=='__main__':
    result=run()
    receipt=Path(__file__).with_name('SPLIT_REGRESSION_001.json')
    if receipt.exists() and receipt.stat().st_size:
        assert result==json.loads(receipt.read_text())
    print(json.dumps(result,sort_keys=True))
