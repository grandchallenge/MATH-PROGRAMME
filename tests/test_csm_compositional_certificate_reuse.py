"""Exact WP13 composition and packing regression; materialize only test oracles."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from math import prod
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from compositional_certificate_reuse import (
    strict_box_interface,verify_interface,positive_margins,revealed_product_margin,
    finite_range_transducer,serial_transducer,parallel_transducer,identity_transducer,
    transducer_support,synchronization,certify_transducer,replay_network,compose_positive,
    joint_product,coupled_kernel4,packing_bound,packing_cover,discover_packing,
    verify_packing_cover,guaranteed_packing_budget,packing_budget_from_conditionals,
)
from observable_polytope_certificate import PredictiveQuotient,balanced_overlap
from adaptive_graph_certificate import discover,Chart,centered_basis,verify_cover
from effective_polytope_synthesis import three_state_overlap,observable_entry_bound
from finite_range_block_certificate import finite_range_lift,iid_binary,rare_non_iid_source,parity_kernel
from marked_reset_spectral import identity,multiply


class TestCompositionalReuse(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models=(balanced_overlap(),three_state_overlap()[2])
        cls.witnesses=tuple(discover(m,max_block=1,max_bits=2,modes=("weighted",)) for m in cls.models)
        cls.compiled=tuple(strict_box_interface(m,w) for m,w in zip(cls.models,cls.witnesses))
        cls.interfaces=tuple(r[0] for r in cls.compiled)

    def test_compile_and_exact_intertwining(self):
        self.assertEqual(tuple(m.dimension for m in self.interfaces),(2,4))
        for m,w,(interface,data) in zip(self.models,self.witnesses,self.compiled):
            self.assertEqual(w["outcome"],"certified")
            chart=Chart(PredictiveQuotient(m),data["basis"])
            self.assertEqual(verify_interface(chart,interface,data["vertices"]),positive_margins(interface))
            for n in range(6):
                for u in product((0,1),repeat=n):
                    self.assertEqual(interface.word_probability(u),m.word_probability(u))
            bad=list(data["vertices"]);bad[0]=(F(1),)+(F(0),)*(chart.dimension-1)
            with self.assertRaisesRegex(ValueError,"interface"):
                verify_interface(chart,interface,bad)

    def test_revealed_product_and_coupled_certificate(self):
        p=revealed_product_margin(self.models,self.witnesses)
        self.assertEqual(p["factor_cells"],(3,3))
        self.assertLess(p["theta"],1)
        T=finite_range_transducer(4,1,coupled_kernel4())
        r=replay_network(self.interfaces,T)
        self.assertEqual(r,compose_positive(self.interfaces,1,coupled_kernel4()))
        self.assertEqual((r["outcome"],r["block"],r["nodes"],r["history_states"]),("certified",2,8,4))
        self.assertEqual(r["nonnull"],F(14897,73728))
        self.assertGreater(r["delta"],20*r["baseline_delta"])
        self.assertEqual(r["b"],r["delta"])
        self.assertFalse(r["joint_lift_constructed"])
        baseline=replay_network(self.interfaces,T,max_weighted_words=0)
        self.assertEqual(baseline["delta"],r["baseline_delta"])
        self.assertIsNone(baseline["weighted_delta"])
        # Reference uses the original factor laws and the compiled laws separately.
        lifted,_=finite_range_lift(joint_product(self.interfaces),1,coupled_kernel4())
        original,_=finite_range_lift(joint_product(self.models),1,coupled_kernel4())
        self.assertNotEqual(lifted.word_probability((0,0)),lifted.word_probability((0,))**2)
        for n in range(4):
            for u in product((0,1),repeat=n):
                self.assertEqual(lifted.word_probability(u),original.word_probability(u))
                for a in (0,1):
                    self.assertGreaterEqual(lifted.word_probability(u+(a,)),r["nonnull"]*lifted.word_probability(u))
                for v in ((0,),(1,0),(0,1,1)):
                    self.assertGreaterEqual(lifted.word_probability(u+v),
                        r["b"]*lifted.word_probability(u)*lifted.word_probability(v))
        for a,b in product((0,1),repeat=2):
            A=multiply(lifted.matrices[a],lifted.matrices[b])
            for col in zip(*A):
                if max(col):self.assertGreaterEqual(min(col),r["delta"]*max(col))

    def test_serial_and_parallel_exact_composition(self):
        T=finite_range_transducer(4,1,coupled_kernel4())
        H=((F(3,4),F(1,4)),(F(1,4),F(3,4)),(F(1,2),F(1,2)),(F(1,4),F(3,4)))
        U=finite_range_transducer(2,1,H)
        S=serial_transducer(T,U)
        self.assertEqual(serial_transducer(identity_transducer(4),T),T)
        self.assertEqual(serial_transducer(T,identity_transducer(2)),T)
        self.assertEqual(parallel_transducer(identity_transducer(2),identity_transducer(2)),identity_transducer(4))
        V=finite_range_transducer(2,0,((F(2,3),F(1,3)),(F(1,5),F(4,5))))
        self.assertEqual(serial_transducer(S,V),serial_transducer(T,serial_transducer(U,V)))
        margins=tuple(positive_margins(m) for m in self.interfaces)
        r=certify_transducer(margins,S)
        self.assertEqual(r,replay_network(self.interfaces,S))
        self.assertEqual((r["outcome"],r["history_states"],r["block"],r["nodes"]),("certified",8,2,31))
        self.assertEqual(r["nonnull"],F(57247,294912))
        self.assertGreater(r["delta"],100*r["baseline_delta"])
        # Exact transition identity against two successive history lifts, after
        # reindexing (previous first output, previous joint input, micro).
        source=joint_product(self.interfaces)
        first,states1=finite_range_lift(source,1,coupled_kernel4())
        second,states2=finite_range_lift(first,1,H)
        keys=[]
        for b,j in states2:
            h,i=states1[j];keys.append((h[0]*2+b[0],i))
        self.assertEqual(len(set(keys)),S["states"]*source.dimension)
        for z in (0,1):
            for i,(h,x) in enumerate(keys):
                row=[F(0)]*len(keys)
                dest_index={key:j for j,key in enumerate(keys)}
                for a in range(source.alphabet):
                    for v,t,p in S["rows"][h*source.alphabet+a]:
                        if v==z:
                            for y,prob in enumerate(source.matrices[a][x]):
                                row[dest_index[t,y]]+=p*prob
                self.assertEqual(tuple(row),second.matrices[z][i])
        for u in product((0,1),repeat=3):
            self.assertGreaterEqual(second.word_probability(u+(0,)),r["nonnull"]*second.word_probability(u))
            self.assertGreaterEqual(second.word_probability(u+(1,0)),r["b"]*second.word_probability(u)*second.word_probability((1,0)))

    def test_support_automaton_exact_exhaustive_oracle(self):
        # All 81 two-state two-label nonempty-row Boolean automata.
        for entries in product((1,2,3),repeat=4):
            masks=(entries[:2],entries[2:])
            r=synchronization(masks)
            relations={ (1,2) };seen=set();s=0
            while True:
                key=frozenset(relations)
                if key in seen:
                    self.assertEqual(r["outcome"],"support_obstruction")
                    break
                seen.add(key);s+=1
                relations={tuple(self._oracle_step(row,masks,z) for row in rel)
                           for rel in relations for z in range(2)}
                if all(a==b for a,b in relations):
                    self.assertEqual((r["outcome"],r["block"]),("synchronized",s))
                    break
        xor=tuple((F((h+a)%2==0),F((h+a)%2==1)) for h,a in product((0,1),repeat=2))
        r=compose_positive((iid_binary(F(3,4)),),1,xor)
        self.assertEqual(r["outcome"],"support_obstruction")
        # Fair XOR is regular, so rejection is not a non-Gibbs decision.
        self.assertEqual(compose_positive((iid_binary(F(1,2)),),1,xor)["outcome"],"support_obstruction")
        self.assertEqual(synchronization(((1,3),(3,2)),max_nodes=1)["outcome"],"undecided")

    @staticmethod
    def _oracle_step(row,masks,z):
        out=0
        for i,r in enumerate(masks):
            if row&(1<<i):out|=r[z]
        return out

    def test_single_seed_packing_and_factorized_verifier(self):
        models=self.models+(finite_range_lift(rare_non_iid_source(),2,parity_kernel(2))[0],)
        for m,count in zip(models,(23,5,5)):
            q=PredictiveQuotient(m);chart=Chart(q,centered_basis(m,q,"weighted"))
            D=discover_packing(chart,max_block=3,max_bits=8,max_cells=128,max_primitives=8)
            self.assertEqual((D["outcome"],D["block"],D["cells"]),("certified",2,count))
            self.assertEqual((D["enclosure_edges"],D["pair_edges"]),(4*count,0))
            self.assertEqual(verify_packing_cover(chart,2,D["boxes"],D["edges"])["eta"],D["eta"])
            sep=F(1,2**(D["bits"]+1))
            centers=D["centers"]
            for i,x in enumerate(centers):
                for y in centers[:i]:
                    self.assertGreater(max(abs(a-b) for a,b in zip(x[1:],y[1:])),sep)
            bad=[list(r) for r in D["edges"]]
            bad[0][0]=(bad[0][0]+1)%count
            with self.assertRaisesRegex(ValueError,"packing enclosure"):
                verify_packing_cover(chart,2,D["boxes"],bad)
            # The graph union need not contain every short-prefix state, yet
            # stationary convexification gives the all-history rate.
            for n in range(4):
                for w in product((0,1),repeat=n):
                    x,y=chart.state((0,)+w),chart.state((1,)+w)
                    self.assertLessEqual(max(abs(a-b) for a,b in zip(x[1:],y[1:])),
                                         D["diameter"]*D["eta"]**(n//2))

    def test_guaranteed_packing_budget_on_markov_and_iid(self):
        # A fully revealed Markov chain has rank-one labelled transfers, H=0.
        from observable_polytope_certificate import balanced_source
        m=balanced_source();q=PredictiveQuotient(m);J=observable_entry_bound(m,q)
        B=guaranteed_packing_budget(q.dimension,q.alphabet,F(1,2),J,0,F(1,2))
        self.assertEqual(B["block"],1)
        boxes,edges,centers=packing_cover(q,B["block"],B["radius"],B["rate"],B["cell_bound"],B["primitive_bound"])
        D=verify_packing_cover(q,1,boxes,edges)
        self.assertEqual(D["eta"],0)
        self.assertLessEqual(len(centers),B["cell_bound"])
        self.assertEqual(packing_bound(2,F(1,4),F(1,2)),81)
        m=iid_binary(F(1,2));q=PredictiveQuotient(m)
        B=packing_budget_from_conditionals(m,1,0,1,0)
        self.assertEqual((B["block"],B["cell_bound"],B["H"]),(1,1,0))
        self.assertEqual(verify_packing_cover(q,1,*packing_cover(q,1,F(1,4),F(1,2))[:2])["eta"],0)

    def test_budget_and_malformed_controls(self):
        T=finite_range_transducer(4,1,coupled_kernel4())
        self.assertEqual(replay_network(self.interfaces,T,max_nodes=1)["outcome"],"undecided")
        with self.assertRaisesRegex(ValueError,"strictly positive"):
            replay_network(self.models,T)
        q=PredictiveQuotient(self.models[0])
        with self.assertRaisesRegex(ValueError,"primitive budget"):
            packing_cover(q,4,F(1,4),F(1,2),max_primitives=1)
        with self.assertRaisesRegex(ValueError,"stochasticity"):
            transducer_support({"states":1,"inputs":1,"outputs":1,"rows":(((0,0,1.0),),)})


if __name__=="__main__":unittest.main()
