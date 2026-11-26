import importlib.util
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/"research/csm-001/conservation_sector_comparison.py"
spec=importlib.util.spec_from_file_location("sector",p)
s=importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)

def oracle(w,k):
    d={}
    for sub in combinations(range(len(w)),k):
        mass=F(1)
        for i in sub: mass*=w[i]
        d[frozenset(sub)]=mass
    z=sum(d.values())
    return {a:v/z for a,v in d.items()}

def marg(d,inds):
    out={}
    for a,v in d.items():
        key=tuple(i in a for i in inds)
        out[key]=out.get(key,F(0))+v
    return out

class SectorTests(unittest.TestCase):
    def test_covariance_oracle(self):
        for n in range(2,6):
            for w in product((F(1),F(2)),repeat=n):
                for k in range(n+1):
                    d=oracle(w,k); row=F(0)
                    for j in range(1,n):
                        pi,pj,pij,c=s.moments(w,k,0,j)
                        self.assertEqual(pi,sum(v for a,v in d.items() if 0 in a))
                        self.assertEqual(pj,sum(v for a,v in d.items() if j in a))
                        self.assertEqual(pij,sum(v for a,v in d.items() if 0 in a and j in a))
                        self.assertLessEqual(c,(max(w)/min(w))**3/F(4*(n-1)))
                        self.assertGreaterEqual(c,0); row+=c
                    self.assertEqual(row,pi*(1-pi))
    def test_finite_reweight_and_marginal(self):
        n=8; w=[F(1)]*n; u=w[:]; u[6]=F(3,2); u[7]=F(4,3)
        for k in range(n+1):
            p,q=marg(oracle(w,k),(0,1)),marg(oracle(u,k),(0,1))
            tv=sum(abs(p.get(a,0)-q.get(a,0)) for a in p.keys()|q.keys())/2
            self.assertLessEqual(tv,s.comparison_bound(n,2,2,F(3,2)))
            pi,pj,_,c=s.moments(w,k,0,6)
            v=w[:]; v[6]=F(3,2)
            self.assertEqual(s.moments(v,k,0,6)[0]-pi,-F(1,2)*c/(1+pj/2))
    def test_extensive_clamp(self):
        for n in (10,40,100):
            for r in (F(2),F(1,2)):
                self.assertEqual(s.moments([1]+[r]*(n-1),n//2,0,1)[0],1/(1+r))
        n=100
        self.assertEqual(s.moments([1]*n,n//2,0,1)[3],F(1,4*(n-1)))
    def test_exchange_coupling(self):
        for n in range(2,7):
            for k in range(1,n):
                x=set(range(k)); y=(x-{0})|{k}; i,j=0,k
                w=[F(1+h%3,1) for h in range(n)]
                total=F(0)
                for a,b in combinations(range(n),2):
                    perm=lambda z:j if z==i else i if z==j else z
                    c,d=perm(a),perm(b)
                    if {a,b}=={i,j}: continue
                    def swprob(state,a,b):
                        if (a in state)==(b in state): return F(0)
                        return (w[b] if a in state else w[a])/(w[a]+w[b])
                    p,q=swprob(x,a,b),swprob(y,c,d)
                    cuts=sorted({F(0),p,q,F(1)})
                    for lo,hi in zip(cuts,cuts[1:]):
                        xx=x^{a,b} if lo<p else x
                        yy=y^{c,d} if lo<q else y
                        total+=(hi-lo)*F(len(xx^yy),2)
                self.assertLessEqual(total/F(n*(n-1)//2),1-s.exchange_alpha(n,max(w)/min(w)))
    def test_invalid(self):
        for w,k in (([1,0],1),([1,2],3)):
            with self.assertRaises(ValueError): s.moments(w,k,0,1)
        with self.assertRaises(ValueError): s.comparison_bound(4,3,2,1)
