import importlib.util
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import unittest

p=Path(__file__).resolve().parents[1]/"research/csm-001/local_equilibration.py"
spec=importlib.util.spec_from_file_location("local",p)
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

def matmul(A,B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def mpow(A,t):
    B=eye(len(A))
    while t:
        if t&1:B=matmul(B,A)
        t//=2
        if t:A=matmul(A,A)
    return B
def kernel(xs,bonds,w,edges):
    ids={x:i for i,x in enumerate(xs)}
    P=[[F(0) for _ in xs] for _ in xs]
    for a,x in enumerate(xs):
        for i,j in bonds:
            y=s.swap(x,i,j); b=ids[y];p=s.placement(x,i,j,w,edges)/len(bonds)
            P[a][b]+=p;P[a][a]+=F(1,len(bonds))-p
    return P
def tv(p,q):
    a,b=sum(p),sum(q)
    return sum(abs(x/a-y/b) for x,y in zip(p,q))/2
def specimen(b):
    blocks=[(2*i,2*i+1) for i in range(b)]
    w=[F(1)]*(2*b)
    edges=[(2*i,2*i+1,F(3,2)) for i in range(b)]+[(2*i+1,2*i+2,F(17,16)) for i in range(b-1)]
    return blocks,w,edges

class EquilibrationTests(unittest.TestCase):
    def test_physical_fast_relative_bound(self):
        B,w,E=specimen(2);k=[1,1];xs=s.fiber(B,k)
        C,q=s.influence(B,E);self.assertEqual(q,F(1,16))
        g=s.fast_gap([2,2],[1,1],[F(1,4)]*2,q)
        self.assertEqual(g,F(15,128))
        mass=[s.weight(x,w,E) for x in xs];pi=[a/sum(mass) for a in mass]
        floor=s.pi_floor(B,k,w,E);self.assertLessEqual(floor,min(pi))
        P=kernel(xs,B,w,E)
        self.assertEqual([sum(pi[i]*P[i][j] for i in range(len(xs))) for j in range(len(xs))],pi)
        T=mpow(P,32); e=s.relative_error(g,floor,32);self.assertLess(e,1)
        for row in T:
            for a,b in zip(row,pi):self.assertLessEqual(abs(a/b-1),e)
        avg=s.averaged_outcomes(xs,1,2,w,E)
        for row in T:
            outcomes=[sum(a*b for a,b in zip(row,col)) for col in zip(*(s.outcome(x,1,2,w,E) for x in xs))]
            for a,b in zip(outcomes,avg):self.assertLessEqual(abs(a/b-1),e)
    def test_local_window_against_global(self):
        B,w,E=specimen(5); k=[1]*5;xs=s.fiber(B,k)
        _,q=s.influence(B,E);self.assertEqual(q,F(1,8))
        # slow bond 1,2 depends on blocks 0,1 (and their internal partners)
        exact=s.averaged_outcomes(xs,1,2,w,E)
        for r in range(3):
            U=range(2+r)
            for exterior in product((0,1),repeat=2*(5-len(U))):
                approx=s.local_outcomes(B,k,U,(0,)*(2*len(U))+exterior,1,2,w,E)
                self.assertEqual(sum(approx),1)
                for a,b in zip(exact,approx):self.assertLessEqual(abs(a-b),2*q**(r+1))
        for k in ([0,1,1,1,1],[2,1,1,1,1]):
            exact=s.averaged_outcomes(s.fiber(B,k),1,2,w,E)
            approx=s.local_outcomes(B,k,[0,1],[0]*10,1,2,w,E)
            self.assertEqual([a==0 for a in exact],[b==0 for b in approx])
    def test_conditioned_two_step_coarse_path(self):
        B,w,E=specimen(2); ks=[(0,2),(1,1),(2,0)]
        xs=[x for k in ks for x in s.fiber(B,k)]
        labels=[sum(x[:2]) for x in xs];pi=[];P=kernel(xs,B,w,E);S=kernel(xs,[(1,2)],w,E)
        T=mpow(P,24); M=matmul(T,S)
        avg=[[F(0)]*3 for _ in ks]
        for k in range(3):
            xk=[x for x in xs if sum(x[:2])==k]
            avg[k][k-1 if k else k]=0
            a,b,c=s.averaged_outcomes(xk,1,2,w,E)
            avg[k][k]=c
            if k:avg[k][k-1]=a
            if k<2:avg[k][k+1]=b
        # Averaged count detailed balance under the microscopic Gibbs law.
        kmass=[sum(s.weight(x,w,E) for x in xs if sum(x[:2])==k) for k in range(3)]
        for a,b in product(range(3),repeat=2):self.assertEqual(kmass[a]*avg[a][b],kmass[b]*avg[b][a])
        # Compare exact row envelope, all initial states, strong observations.
        e=max(abs(sum(row[j] for j in range(len(xs)) if labels[j]==l)/avg[labels[i]][l]-1)
            for i,row in enumerate(M) for l in range(3) if avg[labels[i]][l])
        self.assertLess(e,F(1,1000))
        for i in range(len(xs)):
            p=[sum(M[i][j]*M[j][h] for j in range(len(xs)) for h in range(len(xs)) if labels[j]==a and labels[h]==b) for a,b in product(range(3),repeat=2)]
            q=[avg[labels[i]][a]*avg[a][b] for a,b in product(range(3),repeat=2)]
            for base in (1,10,100):
                L=[F(base)**(a+2*b) for a,b in product(range(3),repeat=2)]
                self.assertLessEqual(tv([x*l for x,l in zip(p,L)],[x*l for x,l in zip(q,L)]),e)
        # Exact posterior closure at intermediate time; microscopic past test.
        initial=[s.weight(x,w,E) for x in xs]
        past=[F(3)**labels[i] for i in range(len(xs))]
        future=[F(10)**labels[i] for i in range(len(xs))]
        J=[[[initial[i]*past[i]*M[i][j]*M[j][h]*future[h] for h in range(len(xs))] for j in range(len(xs))] for i in range(len(xs))]
        z=sum(v for A in J for row in A for v in row)
        mass=[sum(J[i][j][h] for i,h in product(range(len(xs)),repeat=2)) for j in range(len(xs))]
        f=[sum(J[i][j][h]*int(labels[h]==2) for i,h in product(range(len(xs)),repeat=2))/mass[j] for j in range(len(xs))]
        g=[sum(J[i][j][h]*xs[i][0] for i,h in product(range(len(xs)),repeat=2))/mass[j] for j in range(len(xs))]
        def project(v):
            return [sum(mass[i]*v[i] for i in range(len(xs)) if labels[i]==k)/sum(mass[i] for i in range(len(xs)) if labels[i]==k) for k in labels]
        Fp,Gp=project(f),project(g)
        defect=sum(m*(a-b)*(c-d)/z for m,a,b,c,d in zip(mass,f,Fp,g,Gp))
        self.assertLessEqual(abs(defect),e/2)
        self.assertGreater(e,0)
        self.assertGreater(abs(defect),0)
    def test_sharp_range_and_radius(self):
        # Gamma=9, two-point extremizer: normalized density 1/3,3 on masses 3/4,1/4.
        self.assertEqual(tv([F(1,4),F(3,4)],[F(3,4),F(1,4)]),F(1,2))
        for H in (16,256,4096):
            r,a=s.window_radius(F(1,8),2,F(1,100),H,F(1,100))
            self.assertLessEqual(a,F(1,200*H))
            if r:self.assertGreater(a*8,F(1,200*H))
    def test_large_sparse_certificate(self):
        B,w,E=specimen(8192)
        C,q=s.influence(B,E)
        self.assertEqual(q,F(1,8))
        self.assertEqual(sum(map(len,C)),2*(len(B)-1))
        for H,r in [(16,6),(256,7),(4096,9)]:
            got,a=s.window_radius(q,2,F(1,100),H,F(1,100))
            self.assertEqual(got,r)
    def test_rejections(self):
        with self.assertRaises(ValueError):s.influence([(0,),(1,)],[(0,1,F(3))])
        with self.assertRaises(ValueError):s.fiber([(0,1)]*2,[1,1])
        with self.assertRaises(ValueError):s.window_radius(F(1,2),2,F(1,100),10,F(1,100),budget=1)
