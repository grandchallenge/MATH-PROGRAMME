from fractions import Fraction as F
from itertools import product
from math import log
from pathlib import Path
import importlib.util
import unittest

root=Path(__file__).resolve().parents[1]/"research/csm-001"
def load(name):
    spec=importlib.util.spec_from_file_location(name,root/(name+".py"))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
s=load("certified_transport_correctors")
h=load("homogeneous_memory")

def model(n,lam):
    xs=h.sector(n,n//2); bonds=h.ring(n)
    L,p=h.generator(xs,bonds,[1]*n,[(i,j,lam) for i,j in bonds])
    labels=[tuple(sum(x[i:i+2]) for i in range(0,n,2)) for x in xs]
    P=h.projection(labels,p); A,D,B,Q=h.decomposition(L,P)
    return xs,p,labels,L,A,D,B,Q

class CorrectorTests(unittest.TestCase):
    def test_krylov_interacting(self):
        for lam in (F(3,2),F(2,3)):
            xs,p,labels,L,A,D,B,Q=model(6,lam);z=F(1,36)
            f=[F(k[0]-1) for k in labels]; b=s.mv(B,f)
            H=s.shifted(D,z);truth=s.dot(b,s.solve(H,b),p)
            self.assertGreater(truth,0)
            lower=F(0);upper=None;trial=[]
            # projected local site differences, followed by Krylov directions
            local=[s.mv(Q,[F(x[i]) for x in xs]) for i in range(2)]
            v=b
            for w in local+[b]:
                trial.append(w);out=s.galerkin(H,b,p,trial,z)
                self.assertLessEqual(out["lower"],truth)
                self.assertGreaterEqual(out["upper"],truth)
                self.assertGreaterEqual(out["lower"],lower);lower=out["lower"]
            for _ in range(len(xs)):
                trial.append(v);out=s.galerkin(H,b,p,trial,z)
                self.assertLessEqual(out["lower"],truth)
                self.assertGreaterEqual(out["upper"],truth)
                self.assertGreaterEqual(out["lower"],lower)
                lower=out["lower"];upper=out["upper"]
                if lower==upper:break
                v=s.mv(H,v)
            self.assertEqual(lower,truth);self.assertEqual(upper,truth)
    def test_all_retained_schur(self):
        xs,p,labels,L,A,D,B,Q=model(6,F(3,2));z=F(1,36)
        retained=[[F(k==a) for k in labels] for a in sorted(set(labels))]
        bs=[s.mv(B,v) for v in retained];H=s.shifted(D,z)
        trial=[];current=bs
        for _ in range(len(xs)):
            trial=s.orthogonal(trial+current,p)
            eta,C,R=s.relative_trace(L,D,B,p,retained,trial,z)
            self.assertGreaterEqual(eta,0)
            if eta<F(1,100):break
            current=[s.mv(H,v) for v in current]
        self.assertLess(eta,F(1,100))
        V=s.orthogonal(retained,p)
        for coeff in ([F(i==0) for i in range(len(V))],[F(i-2) for i in range(len(V))]):
            f=[sum(c*v[j] for c,v in zip(coeff,V)) for j in range(len(xs))]
            b=[s.dot(u,f,p) for u in V]
            approx=sum(a*b for a,b in zip(b,s.solve(C,b)))
            exact=s.dot(f,s.solve(s.shifted(L,z),f),p)
            self.assertLessEqual(approx,exact)
            self.assertLessEqual(exact,approx/(1-eta))
    def test_phase_exact_small(self):
        n=8;xs=h.sector(n,n//2);bonds=h.ring(n)
        edges=[(i,j,F(4)**((-1)**(i+j))) for i in range(n) for j in range(i+1,n)]
        L,p=h.generator(xs,bonds,[1]*n,edges)
        stag=[F(sum((-1)**i*(2*v-1) for i,v in enumerate(x)),n) for x in xs]
        f=[F((v>0)-(v<0)) for v in stag]
        labels=[tuple(sum(x[i:i+2]) for i in range(0,n,2)) for x in xs]
        P=h.projection(labels,p)
        self.assertEqual(s.mv(P,f),[0]*len(xs))
        self.assertEqual(s.mv(P,stag),[0]*len(xs))
        mass=[F(2)**int(2*n*v*v) for v in stag];Z=sum(mass)
        self.assertEqual(p,[v/Z for v in mass])
        band=sum(w for w,v in zip(p,stag) if abs(v)<=F(4,n))
        E=-s.dot(f,s.mv(L,f),p);norm=s.dot(f,f,p)
        self.assertLessEqual(E,2*n*band)
        b,g,c=s.phase_bounds(n)
        self.assertLessEqual(band,b);self.assertLessEqual(E/norm,g)
        self.assertLessEqual(sum(w for w,v in zip(p,stag) if abs(v)<=F(1,2)),c)
        num=s.phase_mass(n,log(4))
        self.assertAlmostEqual(num["band"],float(band),places=14)
    def test_phase_large(self):
        for n in (16,64,256,1024):
            b,g,c=s.phase_bounds(n);num=s.phase_mass(n,log(4))
            self.assertLessEqual(num["band"],float(b))
            self.assertLessEqual(num["central_half"],float(c))
            self.assertGreater(num["second_moment"],0.9)
            self.assertGreater(num["sign_variance"],0.99)
    def test_reject(self):
        with self.assertRaises(ValueError):s.phase_bounds(6)
        with self.assertRaises(ValueError):s.galerkin([[F(1)]],[F(1)],[F(1)],[],0)
        with self.assertRaises(ValueError):s.solve([[0]],[1])
