import importlib.util
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import unittest

p=Path(__file__).resolve().parents[1]/"research/csm-001/projected_response_calculus.py"
spec=importlib.util.spec_from_file_location("response",p)
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)

def ring(n):
    return [(i,i+1) for i in range(n-1)]+[(0,n-1)]

def setup(n,k,interact):
    xs=s.states(n,k); bonds=ring(n)
    Q,pi=s.kernel(xs,bonds,[F(1+i%2) if interact else F(1) for i in range(n)],[(i,j,F(17,16)) for i,j in bonds] if interact else [])
    return xs,Q,pi

def oracle(xs,Q,pi,ls):
    d={}
    for path in product(range(len(xs)),repeat=len(ls)):
        v=pi[path[0]]*ls[0][path[0]]
        for t in range(1,len(path)):v*=Q[path[t-1]][path[t]]*ls[t][path[t]]
        if v:d[path]=v
    z=sum(d.values());return {x:v/z for x,v in d.items()}

class ResponseTests(unittest.TestCase):
    def test_interacting_multiclamp(self):
        xs,Q,pi=setup(4,2,True)
        ls=[[F(3,2)**x[0]*F(2)**x[2] for x in xs],
            [F(4,3)**x[1] for x in xs],[F(2)**x[3] for x in xs]]
        p=s.Posterior(xs,pi,[Q,Q],ls);d=oracle(xs,Q,pi,ls)
        for t in range(3):
            for u in range(3):
                R=p.response(t,u)
                self.assertTrue(all(sum(row)==0 for row in R))
                self.assertTrue(all(sum(col)==0 for col in zip(*R)))
                for i,j in product(range(4),repeat=2):
                    a=sum(v*xs[path[t]][i] for path,v in d.items())
                    b=sum(v*xs[path[u]][j] for path,v in d.items())
                    c=sum(v*xs[path[t]][i]*xs[path[u]][j] for path,v in d.items())
                    self.assertEqual(R[i][j],c-a*b)
        # Exact finite reweighting, charge-gauge invariance and Hessian positivity.
        gauge=[[v*F(5,3)**sum(x) for x,v in zip(xs,l)] for l in ls]
        q=s.Posterior(xs,pi,[Q,Q],gauge)
        self.assertEqual(p.response(2,0),q.response(2,0))
        self.assertEqual(p.marg,q.marg)
        ls2=[l[:] for l in ls]
        ls2[0]=[l*F(7,5)**x[1] for x,l in zip(xs,ls2[0])]
        q=s.Posterior(xs,pi,[Q,Q],ls2)
        for i in range(4):
            self.assertEqual(q.means(2)[i]-p.means(2)[i],F(2,5)*p.response(2,0)[i][1]/(1+F(2,5)*p.means(0)[1]))
        a=[[F((i+2*t)%3-1) for i in range(4)] for t in range(3)]
        self.assertGreaterEqual(sum(a[t][i]*p.response(t,u)[i][j]*a[u][j] for t,u in product(range(3),repeat=2) for i,j in product(range(4),repeat=2)),0)
    def test_block_certificate(self):
        xs,Q,pi=setup(4,2,True)
        ls=[[F(2)**x[t%4] for x in xs] for t in range(9)]
        B=s.transfer([Q]*8,ls,0,6)
        eta=F(1,1)/(1+2*F(17,16)**4)
        delta=s.coarse_delta(4,4,eta,[2]*5)
        self.assertGreaterEqual(s.column_delta(B),delta)
        self.assertEqual(s.column_delta(B),F(1298683449634385525,5608074338365162367))
        for b in ([F(1)]*len(xs),[F(10)**i for i in range(len(xs))]):
            M=[[v*z for v,z in zip(row,b)] for row in B]
            M=[[v/sum(row) for v in row] for row in M]
            for row,u in product(M,repeat=2):
                self.assertLessEqual(sum(abs(a-b) for a,b in zip(row,u))/2,1-s.column_delta(B))
        p=s.Posterior(xs,pi,[Q]*8,ls)
        for row in p.response(6,0):
            for c in row:self.assertLessEqual(abs(c),(1-s.column_delta(B))/4)
    def test_closure_defect(self):
        xs,Q,pi=setup(4,2,False)
        ones=[F(1)]*len(xs);clamp=[F(2)**x[0] for x in xs]
        p=s.Posterior(xs,pi,[Q,Q],[clamp,ones,clamp])
        d=s.closure_defect(p,2,1,0,0,0)
        self.assertEqual(d,F(512,1058501))
        g=[sum(Q[k][l]*clamp[l]*x[0] for l,x in enumerate(xs))/sum(v*z for v,z in zip(Q[k],clamp)) for k in range(len(xs))]
        coef=s.solve(p.response(1,1),p.response(0,1)[0])
        m=p.means(1); avg=p.means(0)[0]
        var=sum(w*(v-avg-sum(a*(b-c) for a,b,c in zip(coef,x,m)))**2 for w,v,x in zip(p.marg[1],g,xs))
        self.assertEqual(d,var)
        q=s.Posterior(xs,pi,[Q,Q],[ones]*3)
        self.assertEqual(s.closure_defect(q,2,1,0,0,0),0)
    def test_hard_phase(self):
        for n in (4,6,8):
            xs=[x for x in s.states(n,n//2) if all(not(x[i] and x[j]) for i,j in ring(n))]
            self.assertEqual(len(xs),2)
            Q=[[F(1),F(0)],[F(0),F(1)]]
            p=s.Posterior(xs,[F(1,2)]*2,[Q],[[1,1],[1,1]])
            R=p.response(1,0)
            self.assertEqual([sum(row[j]*(-1)**j for j in range(n)) for row in R],[F(n,4)*(-1)**i for i in range(n)])
    def test_budget(self):
        with self.assertRaises(ValueError):s.states(20,10)
        with self.assertRaises(ValueError):s.coarse_delta(4,4,F(1,2),[1])
        self.assertEqual(s.column_delta([[F(1),F(0)],[F(0),F(1)]]),0)
