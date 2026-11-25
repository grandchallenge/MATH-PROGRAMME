"""Exact support-aware network regression. Joint materialization is oracle only."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from support_aware_interacting import (
    SupportedNetwork, contextual_quotient, discover_partition,
    verify_stochastic_interface, rectangular_domains, packets, site_rows,
    certify, reduce_and_certify, replay_reduced, revealed_ring, partly_revealed_ring,
    symmetric_response, spatial_column_margin, column_events, insertion_bounds,
)
from interacting_small_gain import LocalNetwork
from observable_polytope_certificate import row_mul,solve_square


def materialize(net):
    states=tuple(product(*(range(s) for s in net.sizes)))
    labels=tuple(product(*(range(s) for s in net.labels)))
    T=tuple(tuple(tuple(prod(net.factor(i,z[i],tuple(x[j] for j in net.parents[i]),y[i])
                             for i in range(net.n)) for y in states) for x in states)
            for z in labels)
    return states,labels,T


def posterior(T,word,prior):
    p=prior
    for a in word:p=row_mul(p,T[a])
    return tuple(x/sum(p) for x in p)


def one_hot(n,i):
    return tuple(F(j==i) for j in range(n))


def clamp_matrix(net,states,pattern):
    return tuple(tuple(prod(net.factor(i,net.labels[i] if z is None else z,
                                       tuple(x[j] for j in net.parents[i]),y[i])
                             for i,z in enumerate(pattern)) for y in states) for x in states)


def strip_marginal(net,patterns,boundary,t):
    """Exact two-sided smoothing on a small slab, oracle only."""
    states=tuple(product(*(range(s) for s in net.sizes)))
    p=one_hot(len(states),states.index(boundary))
    mats=tuple(clamp_matrix(net,states,z) for z in patterns)
    for A in mats[:t]:p=row_mul(p,A)
    b=(F(1),)*len(states)
    for A in reversed(mats[t:]):b=tuple(sum(a*v for a,v in zip(row,b)) for row in A)
    m=tuple(x*y for x,y in zip(p,b));s=sum(m)
    return tuple(x/s for x in m),states


def port_distribution(net,patterns,boundary,t,i):
    """Output distribution at a wildcard port, with past/future clamps."""
    nums=[]
    for a in range(net.labels[i]):
        p=list(patterns);row=list(p[t-1]);row[i]=a;p[t-1]=tuple(row)
        states=tuple(product(*(range(s) for s in net.sizes)))
        x=one_hot(len(states),states.index(boundary))
        for z in p:x=row_mul(x,clamp_matrix(net,states,z))
        nums.append(sum(x))
    return tuple(v/sum(nums) for v in nums)


class TestSupportAwareInteracting(unittest.TestCase):
    def test_contextual_partition_and_conserved_hidden_colors(self):
        net=partly_revealed_ring(2,nuisance=2)
        P,Q,stats=discover_partition(net)
        self.assertEqual(P,((0,0,1,1),)*2)
        self.assertEqual(Q.sizes,(2,2))
        self.assertEqual(stats["rounds"],1)
        self.assertEqual(contextual_quotient(net,P).tables,Q.tables)
        self.assertEqual(certify(net)["outcome"],"undecided")
        # Conservation is present in the microscopic table; reduced labels
        # still have hard zeros (not an epsilon-regularization).
        for x in net.lookup[0]:
            for y in range(4):
                if x[0]%2!=y%2:self.assertEqual(net.factor(0,3,x,y),0)
        self.assertEqual(rectangular_domains(Q)[0],((0,),(1,),(0,1),(0,1)))
        with self.assertRaisesRegex(ValueError,"strictly positive"):
            LocalNetwork(Q.sizes,Q.parents,tuple(T[:-1] for T in Q.tables))
        with self.assertRaisesRegex(ValueError,"lumpability"):
            contextual_quotient(net,((0,)*4,)*2)
        # Exact labelled tensor intertwining on every microscopic row.
        X,Z,A=materialize(net);Y,Z2,B=materialize(Q)
        self.assertEqual(Z,Z2)
        projection=tuple(Y.index(tuple(P[i][v] for i,v in enumerate(x))) for x in X)
        for C,D in zip(A,B):
            for x,row in enumerate(C):
                got=tuple(sum(v for y,v in enumerate(row) if projection[y]==j)
                          for j in range(len(Y)))
                self.assertEqual(got,D[projection[x]])
        # Arbitrary correlated initial states, not just a stationary product.
        p=tuple(F(i+1,sum(range(1,len(X)+1))) for i in range(len(X)))
        q=tuple(sum(v for x,v in enumerate(p) if projection[x]==j) for j in range(len(Y)))
        for w in product(range(len(Z)),repeat=2):
            x,y=p,q
            for a in w:x,y=row_mul(x,A[a]),row_mul(y,B[a])
            self.assertEqual(sum(x),sum(y))

    def test_partition_refinement_propagates_downstream(self):
        net=SupportedNetwork((2,2,1),((0,),(0,),(1,)),
             ((((1,0),(0,1)),),(((1,0),(0,1)),),(((1,),(0,)),((0,),(1,)))))
        P,Q,stats=discover_partition(net)
        self.assertEqual(P,((0,1),(0,1),(0,)))
        self.assertEqual(stats["rounds"],2)
        self.assertEqual(certify(Q)["boundary"],"nonrectangular label support")
        with self.assertRaisesRegex(ValueError,"lumpability"):
            contextual_quotient(net,((0,0),(0,1),(0,)))

    def test_stochastic_interface_shared_parent_guard(self):
        # A fair random encoded parent drives two deterministic labels;
        # separate child marginal identities hold but the joint law differs.
        net=SupportedNetwork((1,1,1),((),(0,),(0,)),
                ((((1,),),),(((F(1,2),),),((F(1,2),),)),
                 (((F(1,2),),),((F(1,2),),))))
        parent=(((F(1,2),F(1,2)),),)
        active=(((1,),(0,)),((0,),(1,)))
        inert=(((F(1,2),),(F(1,2),)),)*2
        E=(((F(1,2),F(1,2)),),((1,),),((1,),))
        Q=SupportedNetwork((2,1,1),net.parents,(parent,active,active))
        with self.assertRaisesRegex(ValueError,"shared randomized"):
            verify_stochastic_interface(net,Q,E)
        Q=SupportedNetwork((2,1,1),net.parents,(parent,active,inert))
        self.assertTrue(verify_stochastic_interface(net,Q,E))
        with self.assertRaisesRegex(ValueError,"intertwiner"):
            verify_stochastic_interface(net,Q,(((F(1,3),F(2,3)),),((1,),),((1,),)))
        m=partly_revealed_ring(2,nuisance=2);P,Q,_=discover_partition(m)
        E=tuple(tuple(one_hot(Q.sizes[i],v) for v in row) for i,row in enumerate(P))
        self.assertTrue(verify_stochastic_interface(m,Q,E))

    def test_hard_support_temporal_and_partial_clamp_oracle(self):
        net=partly_revealed_ring(2,nuisance=2);P,Q,_=discover_partition(net)
        D=reduce_and_certify(net,max_dense=0)
        self.assertEqual(D["outcome"],"certified")
        self.assertEqual(D["rho"],F(13,32))
        self.assertEqual(D["port_nonnull"],(F(11,64),)*2)
        self.assertEqual(D["port_constants"],(F(10,11),)*2)
        self.assertEqual(replay_reduced(net,D)["gain"],D["gain"])
        X,Z,A=materialize(Q)
        # Every joint observed suffix through length two, all boundaries,
        # and every current partial clamp. Includes zero-supported states.
        for n in range(3):
            for w in product(range(len(Z)),repeat=n):
                posts=tuple(posterior(A,w,one_hot(len(X),i)) for i in range(len(X)))
                for i in range(Q.n):
                    for pre in product(*(range(k) for k in Q.labels[:i])):
                        idx=tuple(j for j,z in enumerate(Z) if z[:i]==pre)
                        for a in range(Q.labels[i]):
                            values=[]
                            for p in posts:
                                weights={j:sum(row_mul(p,A[j])) for j in idx}
                                values.append(sum(v for j,v in weights.items() if Z[j][i]==a)/sum(weights.values()))
                            self.assertGreaterEqual(min(values),D["port_nonnull"][i])
                            self.assertLessEqual(max(values)/min(values)-1,D["port_constants"][i]*D["rho"]**n)
        # Actual interaction, not merely observation coupling.
        self.assertNotEqual(Q.likelihood(0,1,(0,0)),Q.likelihood(0,1,(0,1)))

    def test_two_sided_support_clamp_comparison_and_insertion(self):
        Q=partly_revealed_ring(2);D=certify(Q,max_dense=0)
        self.assertEqual(D["spatial_method"],"site")
        self.assertLess(D["spatial_gain"],F(67,100))
        self.assertEqual(D["insertion_nonnull"],(F(1331,262144),)*2)
        # Common past and future clamps near target; a remote exact label
        # changes from zero to one, hence changes an allowed state domain.
        pats=[(None,None)]*10;pats[8]=(0,2)
        alt=list(pats);alt[8]=(1,2)
        p,X=strip_marginal(Q,pats,(0,0),3)
        q,_=strip_marginal(Q,alt,(0,0),3)
        for i in range(Q.n):
            tv=abs(sum(x for x,s in zip(p,X) if s[i])-sum(x for x,s in zip(q,X) if s[i]))
            # Changed factor at time 9 involves times 8,9; target time 3
            # is at graph distance at least 5 (each edge spans <=1 time).
            self.assertLessEqual(tv,D["spatial_prefactor"]*D["spatial_rate"]**5)
        # Exact insertion probabilities with both neighboring times clamped.
        for left,right in product(range(3),repeat=2):
            p=port_distribution(Q,[(left,2),(None,1),(right,0)],(1,0),2,0)
            self.assertGreaterEqual(min(p),D["insertion_nonnull"][0])

    def test_symmetric_column_strong_memory_and_large_network(self):
        k,r=F(1,3),F(3,4)
        for lo,hi in ((-1,-1),(-1,0),(0,1),(-1,1),(0,0)):
            v=symmetric_response(k,r,lo,hi)
            p=sum(k**max(0,-(h+hi),h+lo)/r**abs(h) for h in range(-40,41))
            self.assertLess(p,v);self.assertLess(v-p,F(1,10**10))
        small=partly_revealed_ring(3,nuisance=2,self_gain=F(7,16),neighbor_gain=F(1,4096))
        D=reduce_and_certify(small,method="column",max_dense=0)
        self.assertEqual((D["outcome"],D["spatial_outcome"],D["spatial_method"]),
                         ("certified","certified","column"))
        self.assertEqual((D["rho"],D["spatial_rate"]),(F(29,32),F(29,32)))
        self.assertLess(D["gain"],F(27,100));self.assertLess(D["spatial_gain"],F(52,100))
        self.assertEqual(replay_reduced(small,D)["spatial_gain"],D["spatial_gain"])
        self.assertGreater(D["spatial_prefactor"],1)
        self.assertEqual(certify(contextual_quotient(small,D["partition"]),max_dense=0)["outcome"],"undecided")
        with self.assertRaisesRegex(ValueError,"below internal"):
            replay_reduced(small,dict(D,spatial_rate=F(1,2)))
        large=partly_revealed_ring(128,nuisance=2,self_gain=F(7,16),neighbor_gain=F(1,4096))
        L=reduce_and_certify(large,method="column",max_dense=0)
        for key in ("rho","gain","spatial_rate","spatial_gain","spatial_prefactor"):
            self.assertEqual(L[key],D[key])
        self.assertEqual(L["quotient_sizes"],(2,)*128)
        self.assertEqual(L["work"],1);self.assertFalse(L["joint_state_constructed"])

    def test_controls_and_refinement_initial_classes(self):
        # Parent-dependent supports cannot be silently treated as product domains.
        net=SupportedNetwork((2,),((0,),),((((1,0),(0,1)),),))
        self.assertEqual(certify(net)["boundary"],"nonrectangular label support")
        P,Q,_=discover_partition(net)
        self.assertEqual(P,((0,0),))
        self.assertEqual(certify(Q)["outcome"],"certified")
        net=partly_revealed_ring(2,nuisance=2)
        P,Q,_=discover_partition(net,((0,1,0,1),)*2)
        self.assertEqual(Q.sizes,(4,4))
        self.assertNotEqual(P,((0,0,1,1),)*2)
        self.assertEqual(certify(Q)["outcome"],"undecided")
        with self.assertRaisesRegex(ValueError,"noncanonical"):
            contextual_quotient(net,((1,1,0,0),)*2)


if __name__=="__main__":unittest.main()
