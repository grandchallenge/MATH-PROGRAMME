"""WP10: exact quotient, finite contraction, and balanced overlapping controls."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from observable_polytope_certificate import (
    PredictiveQuotient, verify_polytope, balanced_source, balanced_overlap,
    balanced_vertices, coupled_kernel, row_mul, project, in_hull,
)
from finite_range_block_certificate import (
    finite_range_lift, universal_block_bounds, singular_gap_counterexample, iid_binary,
)
from observable_exterior_square import word_matrix
from observable_memory_certificate import ObservableFiniteMemory, _rank


class TestPredictivePolytope(unittest.TestCase):
    def test_balanced_overlap_exact_microscopic_probabilities(self):
        src=balanced_source()
        self.assertEqual(src.minimal_linear_dimension,2)
        self.assertEqual(src.word_probability((0,)),F(1,2))
        self.assertEqual(src.word_probability((1,)),F(1,2))
        self.assertEqual(min(src.word_probability(u) for u in product((0,1),repeat=2)),F(1,8))
        H=dict(zip(product((0,1),repeat=2),coupled_kernel()))
        out=balanced_overlap()
        self.assertEqual(out.dimension,4)
        self.assertEqual(out.minimal_linear_dimension,2)
        for n in range(6):
            for w in product((0,1),repeat=n):
                total=F(0)
                for a in product((0,1),repeat=n+1):
                    p=F(1,2)
                    for i,z in enumerate(w):
                        p*=F(3,4) if a[i]==a[i+1] else F(1,4)
                        p*=H[a[i:i+2]][z]
                    total+=p
                self.assertEqual(out.word_probability(w),total)
        self.assertNotEqual(out.word_probability((0,0)),out.word_probability((0,))**2)

    def test_exact_signed_minimal_quotient(self):
        out=balanced_overlap()
        q=PredictiveQuotient(out)
        self.assertEqual(q.probes,((),(0,)))
        self.assertEqual(q.initial,(F(1),F(3,8)))
        self.assertTrue(any(x<0 for A in q.matrices for r in A for x in r))
        for n in range(7):
            for w in product((0,1),repeat=n):
                self.assertEqual(q.probability(w),out.word_probability(w))
                self.assertEqual(q.state(w),tuple(out.word_probability(w+v)/out.word_probability(w) for v in q.probes))
                self.assertEqual(_rank(q.word_matrix(w)),2)

    def test_two_block_certificate_without_rare_anchor(self):
        out=balanced_overlap();q=PredictiveQuotient(out)
        data=verify_polytope(q,balanced_vertices(),2)
        self.assertEqual(data["eta"],F(225,289))
        self.assertEqual(data["nonnull"],F(3,10))
        self.assertEqual(data["diameter"],F(21,80))
        self.assertEqual(data["log_variation_constant"],F(7,8))
        with self.assertRaisesRegex(ValueError,"strict block contraction"):
            verify_polytope(q,balanced_vertices(),1)
        for h in range(4):
            for a in (0,1):
                for s in range(1,5):
                    with self.assertRaises(ValueError):
                        universal_block_bounds(balanced_source(),1,a,h,F(1,2),s)
        # Raw lifted matrix retains an invisible degeneracy.
        self.assertEqual(out.matrices[0][0][0],F(9,16))
        self.assertEqual(out.matrices[0][1][1],F(9,16))
        self.assertEqual(sum(x!=0 for x in out.matrices[0][0]),1)
        self.assertEqual(sum(x!=0 for x in out.matrices[0][1]),1)
        # No finite word is rank one in any equivalent presentation:
        # every minimal generator is invertible.
        self.assertTrue(all(_rank(A)==2 for A in q.matrices))

    def test_all_reachable_suffix_bounds(self):
        q=PredictiveQuotient(balanced_overlap())
        D=verify_polytope(q,balanced_vertices(),2)
        for n in range(5):
            for w in product((0,1),repeat=n):
                for u in ((),(0,),(1,),(0,1),(1,0)):
                    x,y=q.state(u+w),q.state(w)
                    self.assertTrue(in_hull(x,D["vertices"]))
                    self.assertLessEqual(abs(x[1]-y[1]),D["diameter"]*D["eta"]**(n//2))

    def test_singular_and_iid_controls(self):
        q=PredictiveQuotient(singular_gap_counterexample())
        self.assertEqual(q.dimension,2)
        # Any invariant certificate containing the stationary state must
        # contain states with a B likelihood approaching zero.
        with self.assertRaises(ValueError):
            verify_polytope(q,((1,F(1,4)),(1,F(1,2))),2)
        q=PredictiveQuotient(iid_binary(F(1,2)))
        self.assertEqual(verify_polytope(q,((1,),),1)["eta"],0)
        with self.assertRaises(ValueError):
            verify_polytope(q,((0,),),1)

    def test_affine_hull_membership(self):
        V=((F(1),F(0),F(0)),(F(1),F(1),F(0)),(F(1),F(0),F(1)))
        self.assertTrue(in_hull((1,F(1,3),F(1,3)),V))
        self.assertFalse(in_hull((1,F(3,4),F(3,4)),V))
        self.assertFalse(in_hull((1,-1,0),V))


if __name__=="__main__":unittest.main()
