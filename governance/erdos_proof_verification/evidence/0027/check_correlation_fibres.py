"""Exact pair-correlation replay for the first reduction in FFKPY Lemma 3.2."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd,lcm,prod
import json,hashlib,random

def split(n,Q):
    a=1
    for p in range(2,int(Q)+1):
        while n%p==0:
            a*=p
            n//=p
    return a,n

def beta(C):
    return sum((F(1,n*m) for (n,r),(m,t) in combinations(sorted(set(C)),2)
                if gcd(n,m)>1),F(0))

def check(C,Q):
    assert len(C)==len(set(C)) and all(n>0 for n,r in C)
    A=[(*split(n,Q),r) for n,r in C]
    M=lcm(*(a for a,b,r in A))
    direct=sum((beta([(b,r) for a,b,r in A if (h-r)%a==0])
                for h in range(M)),F(0))/M
    compatible=F(0); coarse=F(0)
    for (a,b,r),(c,d,t) in combinations(A,2):
        if gcd(b,d)>1:
            w=F(1,lcm(a,c)*b*d)
            coarse+=w
            if (r-t)%gcd(a,c)==0:
                compatible+=w
    assert direct<=compatible<=coarse
    injective=all(len(active)==len(set(active)) for h in range(M)
        for active in [[(b,r) for a,b,r in A if (h-r)%a==0]])
    if injective: assert direct==compatible
    div=[m for m in range(1,M+1) if M%m==0]
    D=sum((F(1,lcm(a,c)) for a in div for c in div),F(0))
    factors=[]; t=M
    for p in range(2,M+1):
        if p*p>t: break
        e=0
        while t%p==0:
            e+=1; t//=p
        if e: factors.append((p,e))
    if t>1: factors.append((t,1))
    E=prod(sum((F(2*j+1,p**j) for j in range(e+1)),F(0)) for p,e in factors)
    assert D==E
    return [str(direct),str(compatible),str(coarse),injective,str(D)]

def main():
    digest=hashlib.sha256(); total=strict=compat_loss=0
    def run(C,Q):
        nonlocal total,strict,compat_loss
        out=check(C,Q)
        total+=1
        strict+=F(out[0])<F(out[1])
        compat_loss+=F(out[1])<F(out[2])
        digest.update((json.dumps([C,Q,out],separators=(',',':'))+'\n').encode())
    universe=[(n,r) for n in range(1,7) for r in range(n)]
    for k in range(4):
        for C in combinations(universe,k):
            for Q in (2,3,5,7): run(C,Q)
    rng=random.Random(270032)
    universe=[(n,r) for n in (2,3,4,5,6,7,8,9,10,12,14,15,18,21,25,28,35) for r in range(-n,2*n)]
    for i in range(200):
        run(rng.sample(universe,rng.randrange(1,6)),rng.choice([2,2.5,3,5,7]))
    assert check([(3,0),(6,0)],2)[:3]==['0','1/18','1/18']
    assert check([(6,0),(6,1)],2)[:3]==['0','0','1/18']
    assert check([(6,0),(9,0)],2)[:3]==['1/54','1/54','1/54']
    assert strict>0 and compat_loss>0
    print(json.dumps(dict(record_type='ERDOS_PV_0027_CORRELATION_FIBRE_REPLAY/1',
      cases=total,projection_strict_cases=strict,compatibility_strict_cases=compat_loss,
      digest_sha256=digest.hexdigest(),seed=270032,hostile_controls=3,
      divisor_euler_identity_checked=True,result='PASS',full_analytic_replay=False),indent=2))
if __name__=='__main__': main()
