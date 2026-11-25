"""Exact finite replay of geometric-mean and correlation synthesis inequalities."""
from fractions import Fraction as F
from itertools import combinations
from math import gcd,lcm,prod
import hashlib,json,random
def split(n,Q):
    a=1
    for p in range(2,Q+1):
        while n%p==0: a*=p;n//=p
    return a,n
def alpha(C): return prod((1-F(1,n) for n,r in C),start=F(1))
def beta(C):
    return sum((F(1,n*m) for (n,r),(m,t) in combinations(sorted(C),2) if gcd(n,m)>1),F(0))
def density(C):
    T=lcm(*(n for n,r in C))
    return F(sum(all((x-r)%n!=0 for n,r in C) for x in range(T)),T)
def check(C,Q):
    A=[(*split(n,Q),r) for n,r in C]
    M=lcm(*(a for a,b,r in A))
    fibres=[{(b,r) for a,b,r in A if (h-r)%a==0} for h in range(M)]
    good=[D for D in fibres if all(b>1 for b,r in D)]
    g=len(good);d=F(g,M);s=sum((F(1,n) for n,r in C),F(0))
    assert d==density([(n,r) for n,r in C if split(n,Q)[1]==1])
    mean=sum(map(alpha,fibres),F(0))/M
    assert sum((density(D) for D in fibres),F(0))/M==density(C)
    assert density(C)>=mean-sum(map(beta,fibres),F(0))/M
    weights=lambda D:sum((F(1,b) for b,r in D),F(0))
    assert sum(map(weights,fibres),F(0))<=M*s
    assert sum(map(weights,good),F(0))<=M*s-(M-g)
    if not g:
        assert mean==0
        return [str(d),str(mean),'ZERO_GOOD']
    assert all(alpha(D)>0 for D in good)
    assert (mean/d)**g>=prod(map(alpha,good),start=F(1))
    e=F(Q+1,Q)/d
    assert mean**e.denominator>=alpha(C)**e.numerator
    return [str(d),str(mean),'PASS']
def main():
    digest=hashlib.sha256();counts={'PASS':0,'ZERO_GOOD':0}
    def run(C,Q):
        out=check(C,Q);counts[out[-1]]+=1
        digest.update((json.dumps([C,Q,out],separators=(',',':'))+'\n').encode())
    pool=[(n,r) for n in range(1,7) for r in range(n)]
    for k in range(4):
        for C in combinations(pool,k):
            for Q in (2,3,5,7):run(C,Q)
    rng=random.Random(270033)
    pool=[(n,r) for n in (2,3,4,5,6,7,8,9,10,12,14,15) for r in range(-n,2*n)]
    for _ in range(200):run(rng.sample(pool,rng.randrange(1,5)),rng.choice((2,3,5)))
    assert check([(2,0),(2,1)],2)[-1]=='ZERO_GOOD'
    assert check([(2,0),(3,0)],2)[0]=='1/2'
    assert check([],2)==['1','1','PASS']
    print(json.dumps({'record_type':'ERDOS_PV_0027_GEOMETRIC_MEAN_REPLAY/1','cases':sum(counts.values()),'positive_good_cases':counts['PASS'],'zero_good_cases':counts['ZERO_GOOD'],'hostile_and_boundary_controls':3,'digest_sha256':digest.hexdigest(),'arithmetic':'exact rational; exponent cleared by positive integer powers','result':'PASS','analytic_proof_is_not_finite_test':True},indent=2))
if __name__=='__main__':main()
