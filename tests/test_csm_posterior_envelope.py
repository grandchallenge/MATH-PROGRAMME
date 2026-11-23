"""Independent rational posterior-envelope and structural-zero Gibbs replay."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from posterior_envelope import (
    PosteriorEnvelope, positive_current_emission_model,
    permute_hidden_states, disjoint_phase_union, observational_equivalence,
    positive_sector_rate, sector_posterior_tv_bound,
)
from observable_memory_certificate import (
    composed_xor_lift, phase_mixture, ObservableFiniteMemory,
)


def total_variation(a, b):
    return sum((abs(x-y) for x,y in zip(a,b)), F(0))/2


def perturb_without_changing_hidden_chain(model, amount):
    amount=F(amount)
    q=model.Q
    matrices=[]
    for z,A in enumerate(model.matrices):
        sign=1 if z==1 else -1
        matrices.append(tuple(tuple(A[i][j]+sign*amount*q[i][j]
                                    for j in range(model.dimension))
                              for i in range(model.dimension)))
    return ObservableFiniteMemory(model.pi, matrices)


def setup():
    a=positive_current_emission_model()
    b=permute_hidden_states(a,(1,0))
    union=disjoint_phase_union(a,b,F(3,7))
    return a,b,union


class TestPosteriorEnvelope(unittest.TestCase):
    def test_monotone_exact_posterior_diameters_for_all_prefixes(self):
        base,_,union=setup()
        cases=[
            base,union,composed_xor_lift(F(1,2)),
            composed_xor_lift(F(3,4)),
            phase_mixture(F(49,100),F(51,100)),
        ]
        for m in cases:
            env=PosteriorEnvelope(m)
            previous=None
            for k in range(6):
                uniform=env.uniform_diameter(k)["diameter"]
                if previous is not None:
                    self.assertLessEqual(uniform, previous)
                previous=uniform
                if k>=5: continue
                for u in product(range(m.alphabet),repeat=k):
                    diameter=env.diameter(u)["diameter"]
                    for z in range(m.alphabet):
                        self.assertLessEqual(env.diameter(u+(z,))["diameter"], diameter)

    def test_exact_column_barycentric_identity_for_all_future_tails(self):
        base,_,union=setup()
        for m in (base,union,composed_xor_lift(F(3,4))):
            env=PosteriorEnvelope(m)
            for k in range(4):
                for u in product(range(m.alphabet),repeat=k):
                    cols=env.columns(u)
                    for r in range(3):
                        for tail in product(range(m.alphabet),repeat=r):
                            b=m.message(tail)
                            # Compute future-message barycentric weights
                            after=m.pi
                            for z in u:
                                after=m._left_step(after,z)
                            mass=sum(after[j]*b[j] for j,_ in cols)
                            self.assertGreater(mass,0)
                            wts=tuple(after[j]*b[j]/mass for j,_ in cols)
                            self.assertEqual(sum(wts),1)
                            for a in range(m.alphabet):
                                bary=sum((wts[i]*col[a]
                                          for i,(_,col) in enumerate(cols)),F(0))
                                self.assertEqual(bary,env.conditional(a,u+tail))

    def test_reducible_zero_products_but_exact_infinite_memory_gibbs(self):
        base,permuted,union=setup()
        self.assertTrue(observational_equivalence(base,permuted)["equivalent"])
        self.assertEqual(base.minimal_linear_dimension,2)
        self.assertEqual(union.dimension,4)
        self.assertEqual(union.minimal_linear_dimension,2)
        self.assertEqual(union.find_finite_reverse_order()["outcome"],
                         "no_finite_order_under_external_theorem")
        self.assertEqual(base.find_finite_reverse_order()["outcome"],
                         "no_finite_order_under_external_theorem")
        for a in union.matrices:
            self.assertTrue(any(v==0 for row in a for v in row))
        for k in range(7):
            for word in product((0,1),repeat=k):
                self.assertEqual(base.word_probability(word),
                                 union.word_probability(word))

    def test_quantitative_rational_all_scale_bound_on_reducible_presentation(self):
        base,_,union=setup()
        data=positive_sector_rate(base)
        self.assertEqual(data["cross_ratio"],8)
        self.assertEqual(data["rational_contraction"],F(7,9))
        self.assertEqual(data["initial_ratio"],F(5,3))
        self.assertEqual(data["tv_prefactor"],F(2,3))
        self.assertEqual(data["uniform_nonnulllower"],F(7,20))
        left,right=PosteriorEnvelope(base),PosteriorEnvelope(union)
        for k in range(8):
            d1=left.uniform_diameter(k)["diameter"]
            d2=right.uniform_diameter(k)["diameter"]
            self.assertEqual(d1,d2)
            self.assertLessEqual(d2,sector_posterior_tv_bound(data,k))
        self.assertEqual(right.uniform_diameter(0)["diameter"],F(7,30))
        self.assertEqual(right.uniform_diameter(1)["diameter"],F(1,10))

    def test_persistent_bad_posterior_diameter_in_exact_counterexamples(self):
        fair=PosteriorEnvelope(composed_xor_lift(F(1,2)))
        biased=PosteriorEnvelope(composed_xor_lift(F(3,4)))
        mixed=PosteriorEnvelope(phase_mixture(F(49,100),F(51,100)))
        for k in range(7):
            self.assertEqual(fair.uniform_diameter(k)["diameter"],0)
            self.assertEqual(biased.uniform_diameter(k)["diameter"],F(1,2))
            self.assertEqual(mixed.uniform_diameter(k)["diameter"],F(1,50))
        self.assertEqual(fair.base_nonnulllower,F(1,2))
        self.assertEqual(biased.base_nonnulllower,F(1,4))
        self.assertEqual(mixed.base_nonnulllower,F(49,100))

    def test_exact_word_series_equivalence_rejects_small_weight_perturbation(self):
        base,permuted,_=setup()
        altered=perturb_without_changing_hidden_chain(permuted,F(1,1000))
        self.assertNotEqual(base.word_probability((1,)),
                            altered.word_probability((1,)))
        result=observational_equivalence(base,altered)
        self.assertFalse(result["equivalent"])
        word=result["witness_word"]
        self.assertLessEqual(len(word),base.dimension+altered.dimension-1)
        self.assertEqual(result["a_probability"],base.word_probability(word))
        self.assertEqual(result["b_probability"],altered.word_probability(word))
        self.assertNotEqual(result["a_probability"],result["b_probability"])

    def test_reject_nonpositive_sector_and_forbidden_output(self):
        _,_,union=setup()
        with self.assertRaises(ValueError):
            positive_sector_rate(union)
        with self.assertRaises(ValueError):
            positive_sector_rate(composed_xor_lift(F(3,4)))
        with self.assertRaises(ValueError):
            sector_posterior_tv_bound(positive_sector_rate(
                positive_current_emission_model()),-1)
        bad=ObservableFiniteMemory((1,),(((1,),),((0,),)))
        with self.assertRaises(ValueError):
            PosteriorEnvelope(bad)


if __name__ == "__main__":
    unittest.main()
