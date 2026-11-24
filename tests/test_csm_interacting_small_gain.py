"""Exact small-network oracles and dimension-independent local certification."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from interacting_small_gain import (
    LocalNetwork,ring,binary_network,conditioning_amplification,
    envelope_rows,exact_rows,verify_gain,discover_gain,certify,replay,row_action,
    ratio_tv,factor_envelope,observable_margins,column_events,temporal_response,
    certify_perturbation,replay_perturbation,
)
from observable_polytope_certificate import solve_square,row_mul
from observable_memory_certificate import ObservableFiniteMemory


def reference_joint(net):
    """Oracle only: materialize full labelled matrices on very small networks."""
    states=tuple(product(*(range(s) for s in net.sizes)))
    labels=tuple(product(*(range(s) for s in net.labels)))
    A=tuple(tuple(tuple(prod(net.factor(i,z[i],tuple(x[j] for j in net.parents[i]),y[i])
                             for i in range(net.n)) for y in states) for x in states)
            for z in labels)
    n=len(states)
    Q=tuple(tuple(sum(T[i][j] for T in A) for j in range(n)) for i in range(n))
    eq=tuple(tuple(Q[i][j]-F(i==j) for i in range(n)) for j in range(n-1))+((F(1),)*n,)
    pi=solve_square(eq,(F(0),)*(n-1)+(F(1),))
    return ObservableFiniteMemory(pi,A),states,labels


def normalized(row):
    return tuple(x/sum(row) for x in row)


class TestInteractingSmallGain(unittest.TestCase):
    def test_local_factor_bounds_dominate_exact_blankets(self):
        for net in (ring(2),ring(3),conditioning_amplification()):
            A,B,work=envelope_rows(net)
            X,Y,contexts=exact_rows(net)
            self.assertEqual(work,1)
            self.assertGreater(contexts,0)
            for a,b in zip(A+B,X+Y):
                for node,v in b.items():
                    self.assertLessEqual(v,a.get(node,0))
        self.assertEqual(ratio_tv(1),0)
        self.assertGreaterEqual(ratio_tv(4),F(1,3))
        self.assertLess(ratio_tv(4),F(34,100))
        # Multi-state child and nonbinary observation labels.
        table=(((F(1,9),F(1,9),F(1,9)),)*3,
               ((F(1,12),F(1,12),F(1,6)),)*3,
               ((F(1,6),F(1,12),F(1,12)),)*3)
        net=LocalNetwork((3,),((0,),),(table,))
        self.assertEqual(certify(net)["constant"],0)
        self.assertEqual(factor_envelope(net,0)[0,1],1)

    def test_exact_all_history_port_bounds_against_small_tensor_oracle(self):
        net=ring(2)
        D=certify(net)
        self.assertEqual(D["outcome"],"certified")
        self.assertEqual(D["rho"],F(13,32))
        self.assertEqual(D["port_nonnull"],(F(59,128),)*2)
        self.assertEqual(D["port_constants"],(F(10,59),)*2)
        m,states,labels=reference_joint(net)
        nstates=len(states)
        # Actual interaction is present in the hidden transition and observed law.
        self.assertNotEqual(net.likelihood(0,1,(0,0)),net.likelihood(0,1,(0,1)))
        one=tuple(i for i,z in enumerate(labels) if z[1]==1)
        two=tuple(i for i,z in enumerate(labels) if z[0]==1)
        self.assertNotEqual(sum(m.word_probability((a,b)) for a in one for b in two),
                            sum(m.word_probability((a,)) for a in one)*
                            sum(m.word_probability((b,)) for b in two))
        priors=tuple(tuple(F(i==j) for j in range(nstates)) for i in range(nstates))
        # Every observed suffix through length 3; every initial boundary state.
        for n in range(4):
            for word in product(range(m.alphabet),repeat=n):
                post=[]
                for p in priors:
                    for a in word:p=normalized(row_mul(p,m.matrices[a]))
                    post.append(p)
                # Compare likelihood of each port after clamping any earlier ports.
                for i in range(net.n):
                    for prefix in product(*(range(k) for k in net.labels[:i])):
                        selected=[a for a,z in enumerate(labels) if z[:i]==prefix]
                        for v in range(net.labels[i]):
                            probs=[]
                            for p in post:
                                allp={a:sum(row_mul(p,m.matrices[a])) for a in selected}
                                probs.append(sum(t for a,t in allp.items() if labels[a][i]==v)/sum(allp.values()))
                            self.assertGreaterEqual(min(probs),D["port_nonnull"][i])
                            self.assertLessEqual(max(probs)/min(probs)-1,D["port_constants"][i]*D["rho"]**n)
                for a in range(m.alphabet):
                    p=[sum(row_mul(x,m.matrices[a])) for x in post]
                    self.assertGreaterEqual(min(p),D["nonnull"])
        # Exact stationary concatenation comparisons; not used to infer theorem.
        for u in product(range(m.alphabet),repeat=2):
            for v in product(range(m.alphabet),repeat=2):
                self.assertGreaterEqual(m.word_probability(u+v),D["b"]*m.word_probability(u)*m.word_probability(v))

    def test_size_independent_ring_and_replay(self):
        small=certify(ring(3),max_dense=0)
        large=certify(ring(128),max_dense=0)
        for k in ("rho","gain","cross_budget_fraction"):
            self.assertEqual(small[k],large[k])
        self.assertEqual(large["port_constants"],(F(10,59),)*128)
        self.assertEqual(large["port_nonnull"],(F(59,128),)*128)
        self.assertEqual(large["work"],1)
        self.assertEqual(large["sites"],128)
        self.assertFalse(large["joint_state_constructed"])
        self.assertLess(large["gain"],F(946,1000))
        self.assertLess(large["cross_budget_fraction"],F(81,100))
        self.assertEqual(replay(ring(128),large)["b"],large["b"])
        # A changed local table no longer shares the factor-cache key.
        net=binary_network(tuple(((i,F(1,8)),((i-1)%8,F(1,64) if i==0 else F(1,32))) for i in range(8)))
        self.assertEqual(envelope_rows(net)[2],2)

    def test_weighted_gain_for_asymmetric_interactions(self):
        n=17
        net=binary_network((((0,F(1,16)),(1,F(1,64))),)+
                           tuple(((i,F(1,16)),(0,F(1,16))) for i in range(1,n)))
        A,B,_=envelope_rows(net)
        r=F(3,4)
        self.assertGreater(max(max(row_action(a,(1,)*n,r),row_action(b,(1,)*n,r))
                               for a,b in zip(A,B)),2)
        D=certify(net,rates=(r,),max_dense=0)
        self.assertEqual(D["outcome"],"certified")
        self.assertLess(D["gain"],F(988,1000))
        self.assertGreater(D["weights"][0],D["weights"][1])
        self.assertEqual(replay(net,D)["gain"],D["gain"])
        self.assertTrue(all(d+c<1 for ds,cs in zip(D["self_rows"],D["cross_rows"])
                            for d,c in zip(ds,cs)))
        with self.assertRaisesRegex(ValueError,"small gain"):
            replay(net,dict(D,weights=(1,)*n))

    def test_conditioning_not_unobserved_mixing(self):
        net=conditioning_amplification()
        A,B,_=envelope_rows(net,observed=False)
        self.assertEqual(discover_gain(A,B)["gain"],0)
        self.assertEqual(certify(net,max_dense=0,sparse_steps=0)["outcome"],"undecided")
        self.assertEqual(certify(net,method="exact",max_dense=0,sparse_steps=0)["outcome"],"undecided")
        # Rejection is not non-Gibbs: labels are fair iid in this control.
        m,_,_=reference_joint(net)
        for w in product(range(m.alphabet),repeat=3):
            self.assertEqual(m.word_probability(w),F(1,m.alphabet**3))

    def test_exact_gain_and_hostile_inputs(self):
        net=ring(3)
        D=certify(net,method="exact")
        self.assertEqual(D["outcome"],"certified")
        self.assertEqual(D["rho"],F(3,8))
        self.assertLess(D["gain"],1)
        self.assertEqual(replay(net,D)["gain"],D["gain"])
        with self.assertRaisesRegex(ValueError,"small gain"):
            replay(net,dict(D,rho=F(1,32)))
        self.assertEqual(certify(net,method="exact",max_contexts=1)["boundary"],"local context budget")
        A,B,_=envelope_rows(net)
        G=verify_gain(A,B,(1,)*net.n,1-F(1,2**40))
        compact=observable_margins(net,G,max_tail_steps=0)
        self.assertIsNone(compact["b"])
        self.assertGreater(compact["b_power"]["exponent"],2**40)
        self.assertEqual(compact["b_power"]["base"],compact["nonnull"])
        with self.assertRaisesRegex(ValueError,"strictly positive"):
            LocalNetwork((2,),((0,),),((((1,0),(0,1)),),))
        with self.assertRaisesRegex(ValueError,"normalized"):
            LocalNetwork((2,),((0,),),((((1,1),(1,1)),),))

    def test_temporal_response_exact_geometric_bound(self):
        k,r=F(1,3),F(3,4)
        for lo,hi in ((0,0),(0,1),(-1,-1),(-1,1)):
            W=temporal_response(k,r,lo,hi)
            partial=sum(k**max(0,-(t+hi),t+lo)*r**t for t in range(-40,41))
            self.assertLess(partial,W)
            self.assertLess(W-partial,F(1,10**10))
        with self.assertRaisesRegex(ValueError,"temporal response"):
            temporal_response(F(1,2),F(1,2),0,1)

    def test_strong_internal_memory_column_and_perturbation(self):
        self_c,neighbor_c=F(7,16),F(1,4096)
        n=2
        net=ring(n,self_c,neighbor_c)
        base=binary_network(tuple(((i,self_c),) for i in range(n)))
        self.assertEqual(certify(net,max_dense=0,sparse_steps=0)["outcome"],"undecided")
        D=certify(net,"column",max_dense=0)
        P=certify_perturbation(net,base,max_dense=0)
        self.assertEqual((D["outcome"],P["outcome"]),("certified","certified"))
        self.assertEqual(D["internal_rates"],(F(57345,65537),)*n)
        self.assertEqual(P["baseline_rates"],(F(7,8),)*n)
        self.assertEqual(P["relative_perturbations"],(F(1,256),)*n)
        self.assertEqual(P["internal_rates"],(F(120,137),)*n)
        self.assertEqual((D["rho"],P["rho"]),(F(29,32),F(29,32)))
        self.assertLess(D["gain"],F(27,100))
        self.assertLess(P["gain"],F(55,100))
        self.assertEqual(replay(net,D)["gain"],D["gain"])
        self.assertEqual(replay_perturbation(net,base,P)["gain"],P["gain"])
        with self.assertRaisesRegex(ValueError,"rate below internal"):
            replay(net,dict(D,rho=F(7,8)))
        with self.assertRaisesRegex(ValueError,"isolated factors"):
            certify_perturbation(net,net)
        m,states,labels=reference_joint(net)
        for s in range(4):
            for word in product(range(m.alphabet),repeat=s):
                post=[]
                for i in range(len(states)):
                    p=tuple(F(i==j) for j in range(len(states)))
                    for a in word:p=normalized(row_mul(p,m.matrices[a]))
                    post.append(p)
                for i in range(n):
                    for prefix in product(*(range(k) for k in net.labels[:i])):
                        selected=[a for a,z in enumerate(labels) if z[:i]==prefix]
                        for v in range(net.labels[i]):
                            probs=[]
                            for p in post:
                                allp={a:sum(row_mul(p,m.matrices[a])) for a in selected}
                                probs.append(sum(t for a,t in allp.items() if labels[a][i]==v)/sum(allp.values()))
                            for W in (D,P):
                                self.assertLessEqual(max(probs)/min(probs)-1,
                                                     W["port_constants"][i]*W["rho"]**s)
        # Strong-memory certificate is independent of the size of a ring.
        large=ring(128,self_c,neighbor_c)
        L=certify(large,"column",max_dense=0)
        self.assertEqual((L["rho"],L["gain"],L["port_constants"][0]),
                         (D["rho"],D["gain"],D["port_constants"][0]))
        self.assertEqual(L["work"],1)
        self.assertFalse(L["joint_state_constructed"])
        self.assertIsNotNone(L["b_power"])
        # Near-persistent limit specimen, with weaker but nonzero coupling.
        near=ring(3,F(15,32),F(1,16384))
        W=certify(near,"column",max_dense=0)
        self.assertEqual(W["outcome"],"certified")
        self.assertGreater(W["internal_rates"][0],F(15,16))
        self.assertEqual(W["rho"],F(31,32))

    def test_pure_observation_iid_control_and_mixed_arity(self):
        net=LocalNetwork((1,2),((),(0,)),((((F(1,3),),),((F(2,3),),)),
                          (((F(1,6),F(1,3)),),((F(1,3),F(1,6)),))))
        D=certify(net)
        self.assertEqual((D["gain"],D["constant"],D["b"]),(0,0,1))
        m,_,_=reference_joint(net)
        for a,b in product(range(m.alphabet),repeat=2):
            self.assertEqual(m.word_probability((a,b)),m.word_probability((a,))*m.word_probability((b,)))


if __name__=="__main__":unittest.main()
