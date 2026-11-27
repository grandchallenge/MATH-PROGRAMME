import importlib.util
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import exp,cos,pi,sqrt
import unittest

p=Path(__file__).resolve().parents[1]/"research/csm-001/homogeneous_memory.py"
spec=importlib.util.spec_from_file_location("memory",p)
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

def evolve(L,f,t):
    # Bounded small-time numerical replay, not a rigorous exponential enclosure.
    a=[float(v) for v in f];z=a[:]
    for k in range(1,100):
        a=[v*t/k for v in s.mv(L,a)]
        z=[x+y for x,y in zip(z,a)]
    return z

def model(n,lam):
    xs=s.sector(n,n//2);bonds=s.ring(n)
    L,p=s.generator(xs,bonds,[1]*n,[(i,j,lam) for i,j in bonds])
    labels=[tuple(sum(x[i:i+2]) for i in range(0,n,2)) for x in xs]
    P=s.projection(labels,p)
    return xs,L,p,labels,P

class MemoryTests(unittest.TestCase):
    def test_exact_projection_and_memory(self):
        xs,L,p,labels,P=model(6,F(17,16))
        A,D,B,Q=s.decomposition(L,P)
        self.assertEqual(s.mm(P,P),P)
        self.assertTrue(all(sum(row)==0 for row in L))
        for i,j in product(range(len(xs)),repeat=2):
            self.assertEqual(p[i]*L[i][j],p[j]*L[j][i])
            self.assertEqual(p[i]*P[i][j],p[j]*P[j][i])
        Bstar=[[p[j]*B[j][i]/p[i] for j in range(len(xs))] for i in range(len(xs))]
        memory=s.mm(Bstar,B)
        self.assertEqual(s.sub(s.mm(s.mm(P,s.mm(L,L)),P),s.mm(A,A)),memory)
        self.assertGreater(s.hs2(B,p),0)
        f=[F(k[0]) for k in labels]
        self.assertEqual(s.dot(f,s.mv(memory,f),p),s.dot(s.mv(B,f),s.mv(B,f),p))
    def test_unscheduled_conditioned_residual(self):
        xs,L,p,labels,P=model(4,F(17,16))
        A,D,B,Q=s.decomposition(L,P)
        # WP21 internal two-site gap: one cross-edge factor 17/16 on each
        # of two boundaries, eta=1/4, random-block selection.
        g=(1-(F(17,16)**2-1))/8
        f=[F(k[0]==2) for k in labels]
        t=F(1,20)
        exact=evolve(L,f,float(t));coarse=evolve(A,f,float(t))
        err=sum(float(w)*(a-b)**2 for w,a,b in zip(p,exact,coarse))
        self.assertLessEqual(err,float(s.residual_bound2(B,p,g,t,f))+1e-12)
        # Two successive physical intervals and positive count likelihoods.
        h=[F(1)+F(k[0],10) for k in labels]
        def transfer(G,v):
            for _ in range(2):v=evolve(G,[a*b for a,b in zip(v,h)],float(t))
            return sum(float(a)*b for a,b in zip(p,v))
        e=transfer(L,f)/transfer(L,[1]*len(xs))
        c=transfer(A,f)/transfer(A,[1]*len(xs))
        eps=sqrt(float(t*s.hs2(B,p)/(2*g)))
        bound=2*float(max(h)/min(h))**2*2*eps
        self.assertLessEqual(abs(e-c),bound+1e-12)
    def test_ring_diffusive_obstruction(self):
        for ell in (2,4,8):
            n=4096
            physical,naive,corrected=s.ring_correlations(n,ell,n*n/20)
            self.assertLess(abs(physical-exp(-pi*pi/10)),1e-5)
            self.assertLess(abs(naive-exp(-ell*pi*pi/10)),1e-5)
            self.assertGreater(physical-naive,0.2)
            self.assertLess(abs(physical-corrected),4*pi*ell/n)
        xs,L,p,labels,P=model(6,F(1))
        A,D,B,Q=s.decomposition(L,P)
        f=[F(k[0])-F(sum(k),3) for k in labels]
        self.assertEqual(s.mv(A,f),[-F(3,4)*v for v in f])
        actual=s.dot(f,evolve(L,f,0.5),p)/s.dot(f,f,p)
        predicted,naive,_=s.ring_correlations(6,2,0.5)
        self.assertAlmostEqual(actual,predicted,places=11)
        self.assertAlmostEqual(s.dot(f,evolve(A,f,0.5),p)/s.dot(f,f,p),naive,places=11)
    def test_soft_phase(self):
        for n in (4,6,8):
            lam=F(1,10000)
            xs,L,p,labels,P=model(n,lam)
            f=[F(1) if x==tuple(i%2==0 for i in range(n)) else F(-1) if x==tuple(i%2==1 for i in range(n)) else F(0) for x in xs]
            self.assertEqual(s.mv(P,f),[0]*len(xs))
            m=s.dot(f,f,p);floor,a=s.phase_certificate(n,lam)
            self.assertGreaterEqual(m,floor)
            self.assertEqual(-s.dot(f,s.mv(L,f),p),a*m)
            stag=[F(sum((-1)**i*(2*v-1) for i,v in enumerate(x)),n) for x in xs]
            residual=[a-b for a,b in zip(stag,s.mv(P,stag))]
            self.assertGreaterEqual(s.dot(residual,residual,p),m)
            corr=s.dot(f,evolve(L,f,0.25),p)
            self.assertGreaterEqual(corr+1e-12,float(m)*exp(-float(a)*0.25))
    def test_reject(self):
        with self.assertRaises(ValueError):s.sector(30,15)
        with self.assertRaises(ValueError):s.phase_certificate(5,F(1,2))
        with self.assertRaises(ValueError):s.ring_correlations(10,3,1)
