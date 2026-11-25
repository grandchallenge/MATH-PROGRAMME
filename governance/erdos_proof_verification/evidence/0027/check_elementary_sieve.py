"""Exact finite checks of elementary Selberg weights used in Lemma 3.2."""
from fractions import Fraction as F
from math import gcd,lcm
import hashlib,json

def mobius_phi(n):
    m=n; mu=1; phi=n; p=2
    while p*p<=m:
        if m%p==0:
            m//=p; mu=-mu; phi=phi//p*(p-1)
            if m%p==0:
                mu=0
                while m%p==0: m//=p
        p+=1
    if m>1: mu=-mu; phi=phi//m*(m-1)
    return mu,phi

def main():
    digest=hashlib.sha256(); domains=0; counting_cases=0
    for D in range(1,65):
        mp=[(0,0)]+[mobius_phi(n) for n in range(1,D+1)]
        G=sum((F(mu*mu,ph) for mu,ph in mp[1:]),F(0))
        y=[F(0)]+[F(mu,ph)/G for mu,ph in mp[1:]]
        lam=[F(0)]+[d*sum((mp[k//d][0]*y[k] for k in range(d,D+1,d)),F(0)) for d in range(1,D+1)]
        assert lam[1]==1 and all(abs(w)<=1 for w in lam)
        for d in range(1,D+1):
            assert y[d]==sum((lam[k]/k for k in range(d,D+1,d)),F(0))
            mu,ph=mp[d]
            Gd=sum((F(mp[m][0]**2,mp[m][1]) for m in range(1,D//d+1) if gcd(m,d)==1),F(0))
            assert lam[d]==F(mu*d,ph)*Gd/G
        q=sum((lam[d]*lam[e]/lcm(d,e) for d in range(1,D+1) for e in range(1,D+1)),F(0))
        assert q==1/G
        assert G>=sum((F(1,k) for k in range(1,D+1)),F(0))/2
        # Compare exact summation over n with the quadratic lcm expansion and bound.
        for x in [1,2,3,7,D,D*D,2*D*D+3]:
            s=sum((lam[d]*lam[e]*(x//lcm(d,e)) for d in range(1,D+1) for e in range(1,D+1)),F(0))
            assert 0<=s<=F(x)/G+D*D
            # Independently count n without nontrivial divisors <=D.
            rough=sum(all(n%d for d in range(2,D+1)) for n in range(1,x+1))
            assert rough<=s
            if D<=12:
                assert s==sum((sum((lam[d] for d in range(1,D+1) if n%d==0),F(0))**2 for n in range(1,x+1)),F(0))
            digest.update((json.dumps([D,x,str(G),str(q),str(s),rough],separators=(',',':'))+'\n').encode())
            counting_cases+=1
        domains+=1
    print(json.dumps(dict(record_type='ERDOS_PV_0027_ELEMENTARY_SIEVE_REPLAY/1',
        weight_domains=domains,counting_cases=counting_cases,sha256=digest.hexdigest(),
        quadratic_identity=True,weight_bounds=True,result='PASS',kernel_replay=False),indent=2))
if __name__=='__main__': main()
