"""WP16 local certificate tests with independent small exact strip oracles."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import prod
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from constrained_block_comparison import (
    BlockNetwork,certify,replay,rectangular_rows,exact_rows,blanket_row,
    pair_ring,exclusion_ring,phase_ring,phase_channel,chain_mass,phase_witness,
    discover_spatial_blocks,finest_product_scope,verify_spatial,
)
from support_aware_interacting import discover_partition
from observable_polytope_certificate import row_mul


def strip(net,patterns,x,t):
    states=tuple(product(*(range(s) for s in net.sizes)))
    A=tuple(tuple(tuple(prod(net.factor(i,net.labels[i] if a is None else a,
                                     tuple(u[j] for j in net.parents[i]),v[i])
                           for i,a in enumerate(z)) for v in states) for u in states)
            for z in patterns)
    p=tuple(F(u==x) for u in states)
    for M in A[:t]:p=row_mul(p,M)
    b=(F(1),)*len(states)
    for M in reversed(A[t:]):b=tuple(sum(a*v for a,v in zip(row,b)) for row in M)
    p=tuple(a*v for a,v in zip(p,b))
    return sum(p),tuple(v/sum(p) for v in p),states


def block_tv(p,q,states,sites):
    a={};b={}
    for u,x,y in zip(states,p,q):
        k=tuple(u[i] for i in sites);a[k]=a.get(k,0)+x;b[k]=b.get(k,0)+y
    return sum(abs(x-b[k]) for k,x in a.items())/2


class TestConstrainedBlockComparison(unittest.TestCase):
    def test_discover_finest_support_blocks_and_surviving_quotient(self):
        net=pair_ring(3);P,Q,_=discover_partition(net)
        self.assertEqual(P,((0,1),)*6)
        W=discover_spatial_blocks(Q)
        self.assertEqual(W["blocks"],((0,1),(2,3),(4,5)))
        self.assertEqual(certify(Q,tuple((i,) for i in range(6)))["boundary"],"safe block reset failed")
        D=certify(Q,W["blocks"])
        self.assertEqual(D["outcome"],"certified")
        self.assertLess(D["spatial_gain"],F(64,1000))
        self.assertTrue(D["positive_wildcard"])
        self.assertEqual(replay(Q,D)["spatial_gain"],D["spatial_gain"])
        self.assertFalse(D["joint_state_constructed"])
        self.assertEqual(discover_spatial_blocks(Q,max_splits=0)["boundary"],"support split budget")
        self.assertEqual(discover_spatial_blocks(Q,max_block_states=2)["boundary"],"block state budget")
        large=pair_ring(64);L=discover_spatial_blocks(large)
        self.assertEqual(len(L["blocks"]),64)
        E=certify(large,L["blocks"])
        self.assertEqual(E["spatial_gain"],D["spatial_gain"])
        self.assertEqual(E["insertion_nonnull"][0],D["insertion_nonnull"][0])

    def test_finest_product_decomposition_exhaustive_ternary_arity(self):
        X=tuple(product((0,1),repeat=3))
        for mask in range(1,256):
            R={x for k,x in enumerate(X) if mask&(1<<k)}
            P=finest_product_scope(R,3,[100])
            self.assertEqual(sorted(i for b in P for i in b),[0,1,2])
            self.assertEqual(len(R),prod(len({tuple(x[i] for i in b) for x in R}) for b in P))
            for i in range(3):
                A={x[i] for x in R};B={x[:i]+x[i+1:] for x in R}
                if len(R)==len(A)*len(B):self.assertIn((i,),P)

    def test_exact_cross_block_support_and_budgets(self):
        net=exclusion_ring(3);blocks=((0,),(1,),(2,))
        self.assertEqual(discover_spatial_blocks(net)["outcome"],"cross_time_support")
        self.assertEqual(certify(net,blocks)["boundary"],"cross-block support")
        D=certify(net,blocks,method="exact")
        self.assertEqual(D["outcome"],"certified")
        self.assertLess(D["spatial_gain"],F(79,100))
        self.assertGreater(D["spatial_gain"],F(78,100))
        self.assertEqual(D["work"],10416)
        self.assertEqual(replay(net,D)["spatial_gain"],D["spatial_gain"])
        L=certify(exclusion_ring(8),tuple((i,) for i in range(8)),method="exact")
        self.assertEqual((L["work"],L["spatial_gain"]),(D["work"],D["spatial_gain"]))
        self.assertEqual(certify(net,blocks,method="exact",max_contexts=1)["boundary"],"local blanket budget")
        with self.assertRaisesRegex(ValueError,"block state budget"):
            BlockNetwork(net,((0,1,2),),max_block_states=4)
        with self.assertRaisesRegex(ValueError,"spatial gain failed"):
            verify_spatial(({(0,0):F(1,2)},),(1,),({(0,0):F(1)},))

    def test_safe_extension_for_incompatible_exterior(self):
        B=BlockNetwork(pair_ring(2),((0,1),(2,3)))
        f=0;_,nodes,_,vals,sf,T=B.factors[f]
        u=nodes.index((0,0));v=nodes.index((-1,0))
        x=list(sf);x[v]=(0,1)
        self.assertTrue(all(T[1][tuple(x[:u]+[a]+x[u+1:])]==0 for a in vals[u]))
        D=B.restriction(f,u,1,tuple(x))
        self.assertGreater(D[sf[u]],0)
        with self.assertRaisesRegex(ValueError,"safe block reset"):
            BlockNetwork(pair_ring(2),((0,),(1,),(2,),(3,)))
        with self.assertRaisesRegex(ValueError,"all-safe"):
            BlockNetwork(pair_ring(2),((0,1),(2,3)),safe=(0,1,0,1))

    def test_exact_smoothing_and_insertion_on_two_models(self):
        for net,blocks,method,N in ((pair_ring(2),((0,1),(2,3)),"rectangular",7),
                                    (exclusion_ring(3),((0,),(1,),(2,)),"exact",16)):
            D=certify(net,blocks,method=method)
            # Clamp a remote output with a parent-dependent hard support.
            # Include common nearby clamp to test actual conditioned model.
            pats=[(None,)*net.n for _ in range(N)]
            pats[2]=tuple(0 if i==0 else None for i in range(net.n))
            pats[-1]=tuple(0 if i==0 else None for i in range(net.n))
            alt=list(pats);alt[-1]=tuple(1 if i==0 else None for i in range(net.n))
            _,p,X=strip(net,pats,(0,)*net.n,2)
            _,q,_=strip(net,alt,(0,)*net.n,2)
            # Last factor at N has scope N-1,N; every block edge spans <=1.
            bound=D["spatial_prefactor"]*D["spatial_rate"]**(N-3)
            self.assertLess(bound,1)
            for b in blocks:self.assertLessEqual(block_tv(p,q,X,b),bound)
            # Target port at time 3: insertion under both past/future clamps.
            pats[2]=(None,)*net.n
            total,_,_=strip(net,pats,(0,)*net.n,2)
            for a in range(net.labels[0]):
                alt=list(pats);alt[2]=tuple(a if i==0 else None for i in range(net.n))
                mass,_,_=strip(net,alt,(0,)*net.n,2)
                self.assertGreaterEqual(mass/total,D["insertion_nonnull"][0])

    def test_full_support_phase_obstruction_and_bounded_blocks(self):
        for n in (1,2,4,16,64):
            self.assertEqual(phase_witness(n,1),(F(17,64),F(9,64),F(7,64),F(31,64)))
            self.assertEqual(phase_witness(n,2),(F(17,64),F(7,64),F(9,64),F(31,64)))
        c=F(1,1+12**2);lo=c*c/2
        # Every finite word full support, including clamping target.
        for w in product(range(4),repeat=4):
            self.assertGreater(chain_mass(w),0)
        # Finite-clamp uniform insertion bound, exact small cases.
        for exterior in product((None,0,1,2,3),repeat=4):
            v=exterior[:2]+(None,)+exterior[2:]
            mass=chain_mass(v)
            for a in range(4):
                self.assertGreaterEqual(chain_mass(v[:2]+(a,)+v[3:])/mass,lo)
        net=phase_ring(8)
        self.assertEqual(discover_spatial_blocks(net,max_block_states=128)["boundary"],"block state budget")
        self.assertEqual(discover_spatial_blocks(net)["blocks"],(tuple(range(8)),))
        self.assertEqual(certify(net,((0,1),(2,3),(4,5),(6,7)))["boundary"],"safe block reset failed")


if __name__=="__main__":unittest.main()
