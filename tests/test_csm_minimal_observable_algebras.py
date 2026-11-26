import importlib.util
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import unittest

p=Path(__file__).resolve().parents[1]/"research/csm-001/minimal_observable_algebras.py"
spec=importlib.util.spec_from_file_location("observable",p)
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

def ring(n):return [(i,i+1,1) for i in range(n-1)]+[(0,n-1,1)]
def bipart(a,b):return [(min(i,j),max(i,j),1) for i in a for j in b]
def rank(vs,n):
    S=s.Span(n)
    for v in vs:S.add(v)
    return len(S.rows)
def pathlaw(initial,Ms,labels):
    d={}
    for path in product(range(len(initial)),repeat=len(Ms)+1):
        p=initial[path[0]]
        for t,M in enumerate(Ms):p*=M[path[t]][path[t+1]]
        if p:
            key=tuple(labels[i] for i in path);d[key]=d.get(key,0)+p
    return d
def tv(p,q,likelihood=lambda path:1):
    p={x:v*likelihood(x) for x,v in p.items()}
    q={x:v*likelihood(x) for x,v in q.items()}
    a,b=sum(p.values()),sum(q.values())
    return sum(abs(p.get(x,0)/a-q.get(x,0)/b) for x in p.keys()|q.keys())/2

class MinimalTests(unittest.TestCase):
    def test_degree_and_parity(self):
        for n in range(3,8):
            for k in range(1,n):
                xs=s.sector(n,k);d=min(k,n-k)
                self.assertEqual(rank(s.monomials(xs,d),len(xs)),len(xs))
                v=s.monomials(xs,d-1)
                self.assertLess(rank(v,len(xs)),len(xs))
                sub=[x for x in xs if all(x[2*i]+x[2*i+1]==1 for i in range(d)) and all(x[i]==int(i<2*d+k-d) for i in range(2*d,n))]
                self.assertEqual(len(sub),2**d)
                signs=[(-1)**sum(x[2*i] for i in range(d)) for x in sub]
                self.assertTrue(all(sum(a*b for a,b in zip(signs,m))==0 for m in s.monomials(sub,d-1)))
                self.assertNotEqual(sum(a*2**sum(x[2*i] for i in range(d)) for a,x in zip(signs,sub)),0)
    def test_predictive_growth(self):
        xs=s.sector(6,3);P=s.exchange(xs,ring(6));coords=list(zip(*xs))
        _,dims=s.predictive(len(xs),coords,[P])
        self.assertEqual(dims,[6,6])
        I=[[F(i==j) for j in range(len(xs))] for i in range(len(xs))]
        acts=[P]+[s.transfer(I,[1+x for x in c]) for c in coords]
        _,dims=s.predictive(len(xs),[],acts)
        self.assertEqual(dims,[1,6,15,20,20])
        part,_=s.refine(len(xs),coords,[P])
        self.assertEqual(len(part),20)
    def test_coarse_count_lumpability(self):
        a,b=[0,2,4],[1,3,5]
        for k in range(7):
            xs=s.sector(6,k);features=s.count_features(xs,[a,b])
            P=s.exchange(xs,bipart(a,b))
            part,sizes=s.refine(len(xs),features,[P])
            self.assertEqual(sizes[0],sizes[-1])
            B,l,u=s.quotient_ratio(P,part);self.assertEqual((l,u),(1,1))
            for C,row in zip(part,B):
                x=xs[C[0]];ka=sum(x[i] for i in a);kb=k-ka
                for D,v in zip(part,row):
                    ka2=sum(xs[D[0]][i] for i in a)
                    if ka2==ka-1:self.assertEqual(v,F(ka*(3-kb),18))
        xs=s.sector(6,2);features=s.count_features(xs,[a,b]);P=s.exchange(xs,ring(6))
        part,sizes=s.refine(len(xs),features,[P])
        self.assertEqual(sizes,[3,4,4])
        self.assertEqual(len(s.refine(6,s.count_features(s.sector(6,1),[a,b]),[s.exchange(s.sector(6,1),ring(6))])[0]),2)
    def test_approximate_conditioned_paths(self):
        xs=s.sector(4,2);a,b=[0,1],[2,3]
        part=s.group(zip(*s.count_features(xs,[a,b])))
        bonds=bipart(a,b);bonds[0]=(0,2,F(11,10))
        P=s.exchange(xs,bonds)
        labels=[next(i for i,C in enumerate(part) if j in C) for j in range(len(xs))]
        L=[F(2)**sum(x[i] for i in a) for x in xs]
        Ms=[s.transfer(P,L),P]
        Bs=[];ratios=[]
        for M in Ms:
            B,l,u=s.quotient_ratio(M,part);Bs.append(B);ratios.append((l,u))
        bound=s.tv_bound(ratios)
        self.assertLess(bound,F(1,4))
        for j in range(len(xs)):
            initial=[F(i==j) for i in range(len(xs))]
            coarse=s.aggregate(initial,part)
            p=pathlaw(initial,Ms,labels);q=pathlaw(coarse,Bs,list(range(len(part))))
            for f in (lambda path:1,lambda path:100**path[-1],lambda path:10**path[1]):
                self.assertLessEqual(tv(p,q,f),bound)
    def test_minimum_and_interacting_symmetry(self):
        a,b=[0,1],[2,3];xs=s.sector(4,2)
        part=s.group(zip(*s.count_features(xs,[a,b])))
        bonds=bipart(a,b);bonds[0]=(0,2,F(11,10));P=s.exchange(xs,bonds)
        L=[F(2)**sum(x[i] for i in a) for x in xs];actions=[s.transfer(P,L),P]
        for eps,classes,error in [(F(1,8),3,F(11628,104653)),(F(1,10),5,0),(F(1,20),5,0),(F(0),5,0)]:
            q,e,n=s.minimum_certified(part,actions,eps)
            self.assertEqual((len(q),e,n),(classes,error,15))
        with self.assertRaises(ValueError):s.minimum_certified(part,actions,F(1,8),budget=2)
        # Independently reconstruct actual interacting microscopic Gibbs bond heat bath.
        bonds=[(i,j) for i,j,_ in bipart(a,b)]
        weights=[F(1),F(1),F(3,2),F(3,2)]
        factors=[(0,1,F(2)),(2,3,F(3,2))]+[(i,j,F(5,4)) for i,j in bonds]
        def mass(x):
            m=F(1)
            for i in range(4):m*=weights[i]**x[i]
            for i,j,v in factors:m*=v**(x[i]*x[j])
            return m
        P=[[F(0) for _ in xs] for _ in xs]
        for i,x in enumerate(xs):
            for j,k in bonds:
                y=list(x);y[j],y[k]=y[k],y[j];y=tuple(y);l=xs.index(y)
                r=mass(y)/(mass(x)+mass(y))/len(bonds)
                P[i][l]+=r;P[i][i]+=F(1,len(bonds))-r
        q,sizes=s.refine(len(xs),s.count_features(xs,[a,b]),[P])
        self.assertEqual(sizes,[3,3]);B,lo,hi=s.quotient_ratio(P,q)
        self.assertEqual((lo,hi),(1,1))
        for C,row in zip(q,B):
            x=xs[C[0]];ka=sum(x[i] for i in a);kb=2-ka
            for D,r in zip(q,row):
                y=xs[D[0]];ka2=sum(y[i] for i in a)
                if ka2==ka-1:self.assertEqual(r,F(ka*(2-kb),4)*mass(y)/(mass(x)+mass(y)))
    def test_support_and_budget(self):
        with self.assertRaises(ValueError):s.quotient_ratio([[F(1),F(0),F(0)],[F(0),F(0),F(1)],[F(0),F(0),F(1)]],[[0,1],[2]])
        with self.assertRaises(ValueError):s.sector(20,10)
        self.assertEqual(s.tv_bound([(F(1),F(1))]),0)
