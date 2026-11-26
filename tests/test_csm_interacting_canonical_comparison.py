import importlib.util
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import unittest
p=Path(__file__).resolve().parents[1]/"research/csm-001/interacting_canonical_comparison.py"
spec=importlib.util.spec_from_file_location("canonical",p)
s=importlib.util.module_from_spec(spec); spec.loader.exec_module(s)

def states(n,k): return [frozenset(x) for x in combinations(range(n),k)]

def law(w,edges,k):
    d={}
    for x in states(len(w),k):
        v=F(1)
        for i in x: v*=w[i]
        for i,j,a in edges:
            if i in x and j in x: v*=a
        d[x]=v
    z=sum(d.values()); return {x:v/z for x,v in d.items()}

def swap_p(x,i,j,w,edges):
    if (i in x)==(j in x): return F(0)
    y=x^{i,j}
    def weight(z):
        a=F(1)
        for h in z:a*=w[h]
        for h,l,v in edges:
            if h in z and l in z:a*=v
        return a
    a,b=weight(x),weight(y)
    return b/(a+b)

def ring(n,v):
    return [(i,i+1,v) for i in range(n-1)]+[(0,n-1,v)]

class InteractingTests(unittest.TestCase):
    def test_local_and_global_oracle(self):
        for n in range(4,9):
            for v in (F(17,16),F(16,17)):
                edges=ring(n,v); w=[F(1)]*n; u=w[:];u[0]=F(9,8)
                b=s.bounds(w,u,edges)
                for k in range(n+1):
                    p,q=law(w,edges,k),law(u,edges,k)
                    errors=[abs(sum(z for x,z in p.items() if i in x)-sum(z for x,z in q.items() if i in x)) for i in range(n)]
                    for i,e in enumerate(errors):self.assertLessEqual(e,b["local"][i])
                    self.assertLessEqual(sum(errors)/2,b["D"])
    def test_adjacent_coupling_exact(self):
        n=5; w=[F(1+i%2,1) for i in range(n)]
        edges=ring(n,F(17,16)); adj,L,eta,A0,A=s.certificate(n,edges,2)
        M=F(n*(n-1)//2)
        for k in range(1,n):
            for x in states(n,k):
                for i in x:
                    for j in set(range(n))-x:
                        y=x^{i,j}; e=[F(0)]*n
                        perm=lambda z:j if z==i else i if z==j else z
                        for a,b in combinations(range(n),2):
                            c,d=perm(a),perm(b)
                            if {a,b}=={i,j}:continue
                            p,q=swap_p(x,a,b,w,edges),swap_p(y,c,d,w,edges)
                            cuts=sorted({F(0),p,q,F(1)})
                            for lo,hi in zip(cuts,cuts[1:]):
                                xx=x^{a,b} if lo<p else x
                                yy=y^{c,d} if lo<q else y
                                for h in xx^yy:e[h]+=(hi-lo)/M
                        self.assertLessEqual(sum(e)/2,1-A/M)
                        for h in range(n):
                            b=1-A0/M if h in (i,j) else (1+2*L+(n-3)*(adj[h].get(i,0)+adj[h].get(j,0)))/M
                            self.assertLessEqual(e[h],b)
    def test_large_sparse(self):
        for n in (128,1024):
            w=[F(1)]*n;u=w[:];u[0]=F(9,8)
            b=s.bounds(w,u,ring(n,F(17,16)))
            self.assertLess(b["q"],F(1,2))
            self.assertLess(b["local"][n//2],F(1,10))
            self.assertLess(b["base"]*n,2)
    def test_temporal_oracle(self):
        n=5; bonds=[(i,i+1) for i in range(n-1)]+[(0,n-1)]
        h=F(3,2)
        for k in range(n+1):
            p=law([1]*n,[],k); q={x:v*(h if 0 in x else 1) for x,v in p.items()}
            z=sum(q.values()); q={x:v/z for x,v in q.items()}
            for t in range(5):
                expected=[sum(v for x,v in q.items() if i in x)-F(k,n) for i in range(n)]
                self.assertEqual(expected,s.temporal_response(n,bonds,k,0,t,h))
                r={x:F(0) for x in q}
                for x,v in q.items():
                    for a,b in bonds:
                        if (a in x)==(b in x):r[x]+=v/len(bonds)
                        else:
                            r[x]+=v/(2*len(bonds));r[x^{a,b}]+=v/(2*len(bonds))
                q=r
    def test_fail_closed(self):
        with self.assertRaises(ValueError):s.certificate(10,ring(10,4),1)
        with self.assertRaises(ValueError):s.certificate(4,[(0,1,1),(0,1,2)],1)
        b=s.bounds([1]*5,[1]*5,ring(5,F(17,16)))
        self.assertEqual(b["local"],[0]*5)
