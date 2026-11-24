"""Exact tests of automatic suffix-grid synthesis, resource bounds and controls."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from effective_polytope_synthesis import (
    synthesize,replay,normalized_products,quantitative_bounds,slow_reset_model,
    three_state_overlap,BudgetExceeded,
)
from observable_polytope_certificate import (
    PredictiveQuotient,verify_polytope,balanced_overlap,balanced_source,
    row_mul,secant_bound,
)
from finite_range_block_certificate import (
    singular_gap_counterexample,finite_range_lift,iid_binary,parity_kernel,
)
from observable_memory_certificate import ObservableFiniteMemory


class TestEffectivePolytopeSynthesis(unittest.TestCase):
    def test_automatic_balanced_certificate_and_replay(self):
        q=PredictiveQuotient(balanced_overlap())
        d=synthesize(q,8,8)
        self.assertEqual(d["outcome"],"certified")
        self.assertEqual((d["block"],d["grid_bits"],len(d["vertices"])),(3,4,2))
        self.assertEqual(d["eta"],F(243,256))
        self.assertGreater(d["slack"],0)
        r=replay(q,d["block"],d["grid_bits"])
        for k,v in r.items():self.assertEqual(d[k],v)
        self.assertEqual(verify_polytope(q,r["vertices"],r["block"])["eta"],r["eta"])

    def test_balanced_three_state_genuine_overlap(self):
        src,H,m=three_state_overlap()
        q=PredictiveQuotient(m)
        self.assertEqual(src.pi,(F(1,3),)*3)
        self.assertEqual(q.dimension,3)
        self.assertEqual(min(src.word_probability(w) for w in product(range(3),repeat=2)),F(1,12))
        self.assertNotEqual(H[0][0]*H[4][0],H[1][0]*H[3][0])
        self.assertNotEqual(m.word_probability((0,0)),m.word_probability((0,))**2)
        for n in range(4):
            for w in product((0,1),repeat=n):
                p=sum(src.word_probability(u)*prod(H[3*u[i]+u[i+1]][z]
                      for i,z in enumerate(w))
                      for u in product(range(3),repeat=n+1))
                self.assertEqual(p,q.probability(w))
        d=synthesize(q,6,8)
        self.assertEqual((d["outcome"],d["block"],d["grid_bits"]),("certified",4,7))
        self.assertEqual(len(d["vertices"]),20)
        self.assertEqual(d["eta"],F(11019472,11236473))
        self.assertEqual(verify_polytope(q,d["vertices"],4)["eta"],d["eta"])

    def test_four_dimensional_overlap_without_supplied_vertices(self):
        q=PredictiveQuotient(finite_range_lift(iid_binary(F(1,256)),2,parity_kernel(2))[0])
        d=synthesize(q,4,8)
        self.assertEqual(q.dimension,4)
        self.assertEqual((d["outcome"],d["block"],len(d["vertices"])),("certified",2,8))
        self.assertEqual(d["eta"],F(68300012320775,273825722925056))
        self.assertEqual(verify_polytope(q,d["vertices"],2)["eta"],d["eta"])

    def test_normalized_map_deduplication_is_exact(self):
        q=PredictiveQuotient(slow_reset_model(2))
        for n in range(1,6):
            brute=set()
            for w in product(range(3),repeat=n):
                A=q.word_matrix(w);p=q.probability(w)
                brute.add(tuple(tuple(x/p for x in r) for r in A))
            d=normalized_products(q,n,4096)
            self.assertEqual(set(d),brute)
            for A,w in d.items():self.assertEqual(row_mul(q.initial,A)[0],1)
        self.assertLess(len(d),3**5)

    def test_growing_block_lower_bound_and_synthesis(self):
        for N,expected in ((2,7),(4,11)):
            model=slow_reset_model(N)
            q=PredictiveQuotient(model)
            self.assertEqual(q.dimension,2)
            eps=F(1,1+2**N)
            x=q.state((1,))
            # Scalar projective derivative in any affine predictive coordinate.
            for s in range(1,2*N+1):
                A=q.word_matrix((0,)*s)
                det=A[0][0]*A[1][1]-A[1][0]*A[0][1]
                deriv=abs(det)/row_mul(x,A)[0]**2
                self.assertEqual(deriv,2**s/(1+(2**s-1)*eps)**2)
                self.assertGreaterEqual(deriv,1)
            self.assertEqual(synthesize(q,2*N,8)["outcome"],"undecided")
            d=synthesize(q,expected+1,12)
            self.assertEqual((d["outcome"],d["block"]),("certified",expected))
            self.assertEqual(len(d["vertices"]),2)
            self.assertLess(d["eta"],1)

    def test_conditional_resource_bound_and_dimension_one(self):
        q=PredictiveQuotient(balanced_source())
        B=quantitative_bounds(2,2,F(1,2),8,0,F(1,2))
        self.assertEqual((B["block"],B["grid_bits"]),(1,7))
        d=replay(q,B["block"],B["grid_bits"])
        self.assertLessEqual(len(d["vertices"]),B["vertex_bound"])
        self.assertEqual(d["eta"],0)
        q=PredictiveQuotient(iid_binary(F(1,2)))
        d=synthesize(q,1,2)
        self.assertEqual((d["outcome"],len(d["vertices"]),d["eta"]),("certified",1,0))
        B=quantitative_bounds(3,2,F(1,2),4,2,F(1,2))
        self.assertLess(B["D"]*F(1,2)**B["block"],B["radius"]/4)
        self.assertGreaterEqual(B["D"]*F(1,2)**(B["block"]-1),B["radius"]/4)

    def test_fail_closed_budget_and_forbidden_word(self):
        q=PredictiveQuotient(balanced_overlap())
        self.assertEqual(synthesize(q,8,8,max_products=1)["boundary"],"product_budget")
        self.assertEqual(synthesize(q,2,3,max_vertices=1)["outcome"],"undecided")
        with self.assertRaises(BudgetExceeded):replay(q,3,4,max_products=1)
        self.assertEqual(synthesize(PredictiveQuotient(singular_gap_counterexample()),6,6)["outcome"],"undecided")
        # Alternating deterministic process: both letters possible, 00 forbidden.
        m=ObservableFiniteMemory((F(1,2),F(1,2)),
             (((0,1),(0,0)),((0,0),(1,0))))
        d=synthesize(PredictiveQuotient(m),3,4)
        self.assertEqual(d["outcome"],"forbidden_word")
        self.assertEqual(m.word_probability(d["word"]),0)


def prod(xs):
    r=F(1)
    for x in xs:r*=x
    return r


if __name__=="__main__":unittest.main()
