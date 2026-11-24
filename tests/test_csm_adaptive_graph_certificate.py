"""WP12 exact regression: coordinate envelopes, graph margins, hostile controls."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from adaptive_graph_certificate import (
    Chart,centered_basis,linear_min,fractional_max,image_box,corners,image,
    discover,discover_images,verify_cover,replay_witness,uniform_margins,
    graph_horizon,component_bound,component_numerator,row_mul,
)
from observable_polytope_certificate import PredictiveQuotient,balanced_overlap
from effective_polytope_synthesis import three_state_overlap,slow_reset_model
from finite_range_block_certificate import (
    finite_range_lift,rare_non_iid_source,parity_kernel,iid_binary,
    singular_gap_counterexample,
)


class TestAdaptiveGraphCertificate(unittest.TestCase):
    def test_exact_fractional_breakpoint_sweep(self):
        rng=Random(1201)
        for k in range(1,6):
            for _ in range(12):
                box=tuple((F(-rng.randint(0,3),4),F(rng.randint(0,3),4)) for j in range(k))
                den=(F(10*k),)+tuple(F(rng.randint(-4,4),3) for j in range(k))
                cols=[den]+[tuple(F(rng.randint(-8,8),5) for _ in range(k+1)) for j in range(k)]
                A=tuple(zip(*cols))
                low,Y,im=image(A,corners(box))
                self.assertEqual(image_box(A,box),(low,im))
                self.assertEqual(component_numerator(A,im),component_bound(A,F(1),Y))
        # Identical breakpoints, signed/zero coefficients, degenerate sides.
        box=((F(-1),F(2)),(F(0),F(0)),(F(-2),F(1)))
        den=(F(9),F(1),F(-2),F(0))
        num=tuple(3*x for x in den)
        self.assertEqual(fractional_max(box,num,den),3)
        with self.assertRaisesRegex(ValueError,"nonpositive denominator"):
            fractional_max(box,num,(0,1,0,0))
        # 32 free coordinates: linear-fractional sweep is feasible without corners.
        box=((F(0),F(1)),)*32
        den=(F(1),)+(F(1),)*32
        self.assertEqual(fractional_max(box,(F(0),)+(F(1),)*32,den),F(32,33))

    def test_recover_five_dimensional_previous_budget_failure(self):
        model=finite_range_lift(rare_non_iid_source(),2,parity_kernel(2))[0]
        q=PredictiveQuotient(model)
        self.assertEqual(q.dimension,5)
        D=discover(model,max_block=1,max_bits=2,modes=("weighted",))
        self.assertEqual(D["outcome"],"certified")
        self.assertEqual((D["cells"],D["pair_edges"],D["contraction_length"],D["attempts"]),(3,18,1,1))
        self.assertLess(D["eta"],F(805,1000))
        self.assertGreater(D["nonnull"],F(494,1000))
        chart=Chart(q,D["basis"])
        self.assertGreater(max(abs(x) for A in q.matrices for row in A for x in row),1000)
        self.assertLess(max(abs(x) for A in chart.matrices for row in A for x in row),1)
        self.assertEqual(D["weights"],(F(1),F(41,8),F(263,256),F(163,32)))
        for n in range(6):
            for w in product((0,1),repeat=n):
                self.assertEqual(chart.probability(w),model.word_probability(w))
                self.assertEqual(row_mul(chart.state(w),chart.basis),q.state(w))
        r,M=replay_witness(model,D,use_local=False)
        self.assertEqual(r["eta"],D["eta"])
        self.assertEqual(M["b"],F(21,25))
        self.assertLess(M["theta"],1)
        self.assertGreater(M["H"],0)
        local,_=replay_witness(model,D)
        self.assertEqual(local["method"],"local potential")
        self.assertLess(local["eta"],1)

    def test_balanced_expanding_edges_contract_by_graph(self):
        m=balanced_overlap()
        D=discover(m,max_block=1,max_bits=2,modes=("weighted",))
        self.assertEqual(D["outcome"],"certified")
        self.assertEqual(D["horizon"],2)
        self.assertEqual(D["eta"],F(16384,20449))
        self.assertGreater(D["one_step_eta"],1)
        local,_=replay_witness(m,D)
        self.assertEqual(local["contraction_length"],1)
        self.assertGreater(local["potential_ratio"],1)
        q=PredictiveQuotient(m);chart=Chart(q,D["basis"])
        with self.assertRaisesRegex(ValueError,"local potential inequality"):
            verify_cover(chart,1,D["boxes"],D["edges"],1,D["weights"],local=(F(1,2),D["potential"]))
        bad=[list(r) for r in D["edges"]]
        bad[0][0]=0
        with self.assertRaisesRegex(ValueError,"image not enclosed"):
            verify_cover(chart,1,D["boxes"],bad,2)
        # Compare all short actual histories in the original predictive chart.
        for n in range(5):
            for w in product((0,1),repeat=n):
                x,y=chart.state((0,)+w),chart.state((1,)+w)
                dist=max(abs(a-b)/weight for a,b,weight in zip(x[1:],y[1:],D["weights"]))
                self.assertLessEqual(dist,D["diameter"]*D["eta"]**(n//2))

    def test_balanced_three_and_rare_four_dimensional(self):
        m=three_state_overlap()[2]
        D=discover(m,max_block=1,max_bits=2,modes=("weighted",))
        self.assertEqual(D["outcome"],"certified")
        self.assertEqual(D["cells"],3)
        self.assertEqual(D["contraction_length"],1)
        self.assertLess(D["eta"],F(3,4))
        self.assertEqual(D["nonnull"],F(7,16))
        r,M=replay_witness(m,D,use_local=False)
        self.assertEqual(r["eta"],D["eta"])
        # Finite comparisons are hostile regression, not the all-word proof.
        q=PredictiveQuotient(m)
        for n in range(4):
            for w in product((0,1),repeat=n):
                A=q.word_matrix(w);p=q.probability(w)
                self.assertLessEqual(max(abs(x) for row in A for x in row),M["J"]*p)
                for i,j in ((0,1),(0,2),(1,2)):
                    for k,l in ((0,1),(0,2),(1,2)):
                        self.assertLessEqual(abs(A[i][k]*A[j][l]-A[i][l]*A[j][k]),M["H"]*p*p*M["theta"]**n)
                for u in ((0,),(1,0)):
                    self.assertGreaterEqual(q.probability(u+w),M["b"]*q.probability(u)*p)
        m=finite_range_lift(iid_binary(F(1,256)),2,parity_kernel(2))[0]
        D=discover(m,max_block=1,max_bits=5,modes=("hidden",))
        self.assertEqual(D["outcome"],"certified")
        self.assertLess(D["eta"],F(64,100))
        self.assertEqual(D["primitive_words"],2)

    def test_adaptive_topology_slow_reset_without_long_word_products(self):
        m=slow_reset_model(8)
        D=discover_images(m,max_bits=10,max_cells=48,max_horizon=24,modes=("hidden",))
        self.assertEqual(D["outcome"],"certified")
        self.assertEqual((D["cells"],D["horizon"],D["primitive_words"]),(38,18,3))
        self.assertEqual(D["pair_edges"],4332)
        self.assertLess(D["eta"],F(77,100))
        self.assertGreater(D["one_step_eta"],1)
        r,_=replay_witness(m,D)
        self.assertLess(r["eta"],1)
        self.assertEqual(r["contraction_length"],1)

    def test_component_envelope_handles_nilpotent_switching(self):
        B=((((0,2),(0,0)),((0,3),(0,0))),)
        D=graph_horizon(B,((0,0),),2,weights=(F(1),F(1)))
        self.assertEqual((D["horizon"],D["eta"],D["method"]),(2,0,"component"))
        self.assertNotIn("potential",D)

    def test_fail_closed_singular_iid_and_budget(self):
        self.assertEqual(discover(singular_gap_counterexample(),max_block=1,max_bits=4)["outcome"],"undecided")
        self.assertEqual(discover_images(slow_reset_model(8),max_bits=4,max_cells=3,modes=("hidden",))["outcome"],"undecided")
        m=iid_binary(F(1,2))
        D=discover(m,max_block=1,max_bits=2)
        self.assertEqual(D["eta"],0)
        r,M=replay_witness(m,D)
        self.assertEqual((r["eta"],M["H"],M["b"]),(0,0,1))


if __name__=="__main__":unittest.main()
