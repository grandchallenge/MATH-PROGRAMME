from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import cos,pi
import importlib.util
import unittest

root=Path(__file__).resolve().parents[1]/"research/csm-001"
def load(name):
    spec=importlib.util.spec_from_file_location(name,root/(name+".py"))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
s=load("gradient_erasure")
h=load("homogeneous_memory")

class WP25Tests(unittest.TestCase):
    def test_gradient_truth_table(self):
        for lam in (F(2,3),F(1),F(3,2),F(7)):
            for a,x,y,b in product((0,1),repeat=4):
                self.assertEqual(s.current(a,x,y,b,lam),s.gradient(a,x,y,b,lam))
    def test_microscopic_generator_gradient(self):
        for N,K in [(5,2),(6,3),(7,2)]:
            xs=h.sector(N,K); bonds=h.ring(N)
            for lam in (F(2,3),F(3,2)):
                G,p=h.generator(xs,bonds,[1]*N,[(i,j,lam) for i,j in bonds])
                c=(1-lam)/(2*(1+lam))
                for i in range(N):
                    def pot(x,j):return F(x[j%N],2)+c*s.psi(x[(j-1)%N],x[j%N],x[(j+1)%N])
                    self.assertEqual(h.mv(G,[F(x[i]) for x in xs]),
                        [pot(x,i-1)+pot(x,i+1)-2*pot(x,i) for x in xs])
    def test_dilute_residual(self):
        for N,K in [(6,2),(8,3),(10,2)]:
            xs=h.sector(N,K);bonds=h.ring(N);lam=F(3,2)
            G,p=h.generator(xs,bonds,[1]*N,[(i,j,lam) for i,j in bonds])
            # Rational coefficient test for the moment bounds uses alternating mode.
            a=[(-1)**i for i in range(N)]
            v=[sum(a[i]*x[i] for i in range(N)) for x in xs]
            z=[sum(a[i]*s.psi(x[(i-1)%N],x[i],x[(i+1)%N]) for i in range(N)) for x in xs]
            R=lam**K
            self.assertEqual(h.dot(v,[1]*len(xs),p),0)
            self.assertGreaterEqual(h.dot(v,v,p),F(K*(N-K),N-1)/R)
            self.assertLessEqual(h.dot(z,z,p),9*R*F(K*K*(K-1),N-1))
            self.assertEqual(h.mv(G,v),[-2*x-4*(1-lam)/(2*(1+lam))*y for x,y in zip(v,z)])
            # First Fourier mode, direct finite oracle (floating evaluation only).
            a=[cos(2*pi*i/N) for i in range(N)]
            v=[sum(a[i]*x[i] for i in range(N)) for x in xs]
            z=[sum(a[i]*s.psi(x[(i-1)%N],x[i],x[(i+1)%N]) for i in range(N)) for x in xs]
            omega=1-cos(2*pi/N)
            for lhs,x,y in zip(h.mv(G,v),v,z):
                self.assertAlmostEqual(lhs,-omega*x-2*omega*float((1-lam)/(2*(1+lam)))*y,places=12)
    def test_uniform_scaling(self):
        for lam in (F(2,3),F(3,2)):
            b=[s.dilute_bound2(N,2,lam) for N in (128,1024,8192,65536)]
            self.assertTrue(all(x>y for x,y in zip(b,b[1:])))
            self.assertLess(b[-1],F(1,1000))
            self.assertEqual(s.dilute_bound2(128,1,lam),0)
            self.assertEqual(s.dilute_bound2(128,2,1),0)
            self.assertGreaterEqual(s.sqrt_up(b[-1])**2,b[-1])
    def test_erasure_cylinder_nonpure_mixture(self):
        # Two overlapping mixtures, neither pure; means separated by a0 on each side.
        r=F(1,2);a0=F(1,4)
        wplus=[F(1,4),F(3,4)];wminus=wplus[::-1]
        means=[F(-1,2),F(1,2)]
        self.assertEqual(sum(w*m for w,m in zip(wplus,means)),a0)
        self.assertEqual(sum(w*m for w,m in zip(wminus,means)),-a0)
        for n in (0,1,10,100):
            p,t,plus=s.mixture_cylinder(wplus,means,r,n)
            q,_,minus=s.mixture_cylinder(wminus,means,r,n)
            self.assertEqual(sum(p),sum(q))
            self.assertEqual(plus-minus,s.erasure_gap(a0,r))
            self.assertGreaterEqual(max(t)-min(t),plus-minus)
    def test_half_density_static(self):
        for a in (F(1,2),F(1),F(2),F(3,2)):
            q,d,D=s.half_density_static(a);lam=a*a;c=(1-lam)/(2*(1+lam))
            self.assertEqual(q*q,lam*(F(1,2)-q)**2)
            self.assertEqual(d,3-8*q+8*q*q)
            self.assertEqual(D,F(1,2)+c*d)
            self.assertGreater(D,0)
        self.assertEqual(s.half_density_static(1)[2],F(1,2))
    def test_rejections(self):
        with self.assertRaises(ValueError):s.dilute_bound2(4,2,1)
        with self.assertRaises(ValueError):s.erasure_gap(1,1)
        with self.assertRaises(ValueError):s.current(0,1,0,0,0)
