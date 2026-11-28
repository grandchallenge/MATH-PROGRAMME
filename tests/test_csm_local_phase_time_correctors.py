from fractions import Fraction as F
from itertools import product
from pathlib import Path
import importlib.util
import unittest

root=Path(__file__).resolve().parents[1]/"research/csm-001"
def load(name):
    spec=importlib.util.spec_from_file_location(name,root/(name+".py"))
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m
s=load("local_phase_time_correctors")
h=load("homogeneous_memory")
c=load("certified_transport_correctors")

class WP24Tests(unittest.TestCase):
    def test_exact_ring_local_forms(self):
        N=6;K=3;w=[F(1)+F(i%2,3) for i in range(N)]
        lam=[F(3,2) if i%2 else F(2,3) for i in range(N)]
        R=s.Ring(w,lam,K)
        xs=h.sector(N,K);edges=[(min(i,(i+1)%N),max(i,(i+1)%N),a) for i,a in enumerate(lam)]
        G,p=h.generator(xs,h.ring(N),w,edges)
        self.assertEqual(R.prob({0:1,5:0}),sum(q for q,x in zip(p,xs) if x[0] and not x[5]))
        fs=[R.cylinder([0],lambda a:a[0]),R.cylinder([1,2],lambda a:a[1]*a[2])]
        def evalf(f,x):return f[1][tuple(x[i] for i in f[0])]
        V=[[evalf(f,x) for x in xs] for f in fs]
        GV=[h.mv(G,v) for v in V]
        for f,gv in zip(fs,GV):
            self.assertEqual([sum(evalf(g,x) for g in R.action(f)) for x in xs],gv)
        gram,stiff,leak=R.forms([[f] for f in fs])
        self.assertEqual(gram,[[h.dot(a,b,p) for b in V] for a in V])
        self.assertEqual(stiff,[[h.dot(a,b,p) for b in GV] for a in V])
        coeff=[s.solve(gram,[row[j] for row in stiff]) for j in range(2)]
        res=[[g-sum(v[i]*a for v,a in zip(V,co)) for i,g in enumerate(gv)] for gv,co in zip(GV,coeff)]
        self.assertEqual(leak,[[h.dot(a,b,p) for b in res] for a in res])
        _,base,err=s.time_certificate(gram,stiff,leak,[1,0],F(1,10),8)
        self.assertGreater(base,0);self.assertGreater(err,0)
    def test_time_residual_diffusive(self):
        N=6;xs=h.sector(N,3);bonds=h.ring(N)
        G,p=h.generator(xs,bonds,[1]*N,[(i,j,F(3,2)) for i,j in bonds])
        f=[F(x[0]+x[1]-1) for x in xs]
        V=c.orthogonal([f],p)
        while True:
            W=c.orthogonal(V+[h.mv(G,v) for v in V],p)
            if len(W)==len(V):break
            V=W
        self.assertEqual(len(V),3)
        GV=[h.mv(G,v) for v in V]
        gram=[[h.dot(a,b,p) for b in V] for a in V]
        stiff=[[h.dot(a,b,p) for b in GV] for a in V]
        coeff=[s.solve(gram,[row[j] for row in stiff]) for j in range(len(V))]
        for gv,co in zip(GV,coeff):
            self.assertEqual(gv,[sum(v[i]*a for v,a in zip(V,co)) for i in range(len(xs))])
        zero=[[F(0)]*len(V) for _ in V]
        v,base,err=s.time_certificate(gram,stiff,zero,[1]+[0]*(len(V)-1),N*N,64)
        self.assertEqual(err,0);self.assertLess(base,F(1,32))
        # Direct rational implicit Euler oracle on full microscopic generator.
        H=[[F(i==j)-F(N*N,64)*a for j,a in enumerate(row)] for i,row in enumerate(G)]
        invcols=[s.solve(H,[F(i==j) for i in range(len(xs))]) for j in range(len(xs))]
        full=f
        for _ in range(64):full=h.mv(list(zip(*invcols)),full)
        self.assertEqual(full,[sum(a*b[i] for a,b in zip(v,V)) for i in range(len(xs))])
    def test_large_ring_transfer(self):
        N=64;K=32;R=s.Ring([1]*N,[F(3,2)]*N,K)
        self.assertEqual(R.prob({0:1}),F(1,2))
        self.assertEqual(sum(R.prob({0:a,1:b}) for a,b in product((0,1),repeat=2)),1)
        self.assertEqual(R.prob({0:1,1:0}),R.prob({0:0,1:1}))
    def test_ising_collision_exact(self):
        L=4;m=L*L;z=s.ising_torus_counts(L)
        self.assertEqual(z,z[::-1])
        # Independent single-layer enumeration, never enumerate two-layer sector.
        edges=[(i*L+j,i*L+(j+1)%L) for i in range(L) for j in range(L)]+[(i*L+j,((i+1)%L)*L+j) for i in range(L) for j in range(L)]
        oracle=[0]*(m+1)
        for x in range(1<<m):
            a=sum(((x>>i)&1)==((x>>j)&1) for i,j in edges)
            oracle[x.bit_count()]+=16**a
        self.assertEqual(z,oracle)
        p=[F(a,sum(z)) for a in z];C,q=s.collision(p)
        self.assertGreaterEqual(C,F(1,m+1));self.assertEqual(q,q[::-1])
        b=sum(q[k] for k in range(m+1) if abs(2*k-m)<=2)
        self.assertLessEqual(b,(m+1)*sum(p[k] for k in range(m+1) if abs(2*k-m)<=2))
    def test_connected_bilayer_symmetry(self):
        m=4;xs=h.sector(2*m,m); layer=h.ring(m)
        bonds=layer+[(i+m,j+m) for i,j in layer]+[(i,i+m) for i in range(m)]
        # Ising exp(beta spin spin) gives pair factor exp(4 beta)
        G,p=h.generator(xs,bonds,[F(1,16)]*(2*m),[(i,j,F(16)) for i,j in bonds[:2*len(layer)]])
        M=[sum(2*a-1 for a in x[:m]) for x in xs]
        f=[F((a>0)-(a<0)) for a in M]
        labels=[tuple(x[i]+x[i+m] for i in range(m)) for x in xs]
        P=h.projection(labels,p)
        self.assertEqual(h.mv(P,f),[0]*len(xs))
        self.assertEqual(h.mv(P,M),[0]*len(xs))
        band=sum(w for a,w in zip(M,p) if abs(a)<=2)
        self.assertLessEqual(-h.dot(f,h.mv(G,f),p),2*m*band)
        self.assertTrue(any(G[i][j]>0 and M[i]!=M[j] for i,j in product(range(len(xs)),repeat=2)))
        self.assertTrue(any(G[i][j]>0 and labels[i]!=labels[j] for i,j in product(range(len(xs)),repeat=2)))
    def test_rejections(self):
        self.assertEqual(s.sqrt_up(F(4,9))**2>=F(4,9),True)
        with self.assertRaises(ValueError):s.ising_torus_counts(8)
        with self.assertRaises(ValueError):s.ring_partition([1]*4,[1]*4,5)
        with self.assertRaises(ValueError):s.time_certificate([[1]],[[0]],[[0]],[1],1,1)
