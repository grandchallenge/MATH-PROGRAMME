"""Exact hostile and independent microscopic tests for WP09."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from finite_range_block_certificate import (
    singular_gap_counterexample, finite_range_lift, block_mixed_certificate,
    iid_binary, rare_history_bounds, parity_kernel, universal_block_bounds,
    rare_non_iid_source,
)
from observable_exterior_square import word_matrix, exterior_norm, conditional_defect
from polarized_exterior_channel import postprocess
from observable_memory_certificate import _rank


def direct_probability(source,r,H,w):
    """Sum source cylinders and conditional channel weights independently."""
    lut=dict(zip(product(range(source.alphabet),repeat=r+1),H))
    total=F(0)
    for u in product(range(source.alphabet),repeat=len(w)+r):
        mass=source.word_probability(u)
        for i,z in enumerate(w):mass*=lut[u[i:i+r+1]][z]
        total+=mass
    return total


class TestFiniteRangeBlockCertificate(unittest.TestCase):
    def test_singular_gap_full_support_minimal_primitive(self):
        m=singular_gap_counterexample()
        self.assertEqual(m.minimal_linear_dimension,2)
        self.assertIsNone(m.full_support_obstruction())
        self.assertTrue(all(x>0 for row in m.Q for x in row))
        for n in range(1,6):
            for w in product(range(3),repeat=n):
                A=word_matrix(m,w)
                self.assertEqual(_rank(A),1 if any(w) else 2)
                if not any(w):
                    self.assertEqual(A[1][1]/A[0][0],F(1,2)**n)
                else:self.assertEqual(exterior_norm(A),0)
        for n in range(12):
            p=m.word_probability
            self.assertEqual(p((1,)+(0,)*n)/p((0,)*n),F(1,4)/(2**n+1))
            self.assertEqual(p((1,)+(0,)*n)/(p((1,))*p((0,)*n)),F(2)/(2**n+1))
            # Exactly distinct finite-cylinder conditionals, and analytic limits.
            b=[p((1,)+(0,)*n+(a,)+(0,)*n+(1,)) for a in range(3)]
            c=[p((2,)+(0,)*n+(a,)+(0,)*n+(2,)) for a in range(3)]
            self.assertEqual(tuple(x/sum(b) for x in b),(F(1,3),)*3)
            t=F(1,2)**n
            expected=(F(1,2)+F(1,4)*t*t,F(1,4)*t*t,F(1,4)*(1+t)**2)
            self.assertEqual(tuple(x/sum(c) for x in c),tuple(x/sum(expected) for x in expected))

    def test_iid_radius_two_lift_and_two_block_certificate(self):
        src=iid_binary(F(1,256));r=2;H=parity_kernel(r)
        m,states=finite_range_lift(src,r,H)
        self.assertEqual(m.dimension,4)
        self.assertEqual(states,tuple((u,0) for u in product(range(2),repeat=r)))
        data=rare_history_bounds(F(1,256),r,F(1,2))
        d=block_mixed_certificate(m,0,data["L"],data["R"],r)
        self.assertLessEqual(d["eta"],data["eta_upper"])
        self.assertLess(d["eta"],1)
        with self.assertRaises(ValueError):
            block_mixed_certificate(m,0,data["L"],data["R"],1)
        for n in range(5):
            for w in product(range(2),repeat=n):
                self.assertEqual(m.word_probability(w),direct_probability(src,r,H,w))
                self.assertLessEqual(abs(conditional_defect(m,(1,),w,(1,))),
                    d["constant"]*d["eta"]**(n//r))

    def test_kernel_independent_certificate_on_non_iid_source(self):
        src=rare_non_iid_source()
        self.assertGreater(src.minimal_linear_dimension,1)
        r=2
        D=universal_block_bounds(src,r,0,0,F(1,2))
        self.assertLess(D["eta_upper"],1)
        # Different kernels, including deterministic values on all other inputs.
        kernels=[parity_kernel(r),
                 tuple((F(1,2),F(1,2)) if i==0 else (F(i%3==0),F(i%3!=0))
                       for i in range(8)),
                 ((F(1,2),F(1,2)),)*8]
        for H in kernels:
            m,states=finite_range_lift(src,r,H)
            self.assertEqual(states,D["states"])
            d=block_mixed_certificate(m,D["anchor"],D["L"],D["R"],r)
            self.assertLessEqual(d["eta"],D["eta_upper"])
            for n in range(4):
                for w in product(range(2),repeat=n):
                    self.assertEqual(m.word_probability(w),direct_probability(src,r,H,w))
        # Reference bound depends on source, not kernel.
        self.assertGreater(D["pivot_lower"],0)

    def test_stochastic_postprocessing_preserves_block_certificate(self):
        src=iid_binary(F(1,256));r=2
        m,_=finite_range_lift(src,r,parity_kernel(r))
        D=rare_history_bounds(F(1,256),r,F(1,2))
        d=block_mixed_certificate(m,0,D["L"],D["R"],r)
        for H in [((F(1,3),F(2,3)),(F(3,4),F(1,4))),
                  ((F(1),),(F(1),))]:
            out=postprocess(m,H)
            e=block_mixed_certificate(out,0,D["L"],D["R"],r)
            self.assertLessEqual(e["eta"],d["eta"])
            self.assertEqual(e["b"],d["b"])

    def test_deterministic_xor_is_not_unconditional_closure(self):
        src=iid_binary(F(3,4))
        m,_=finite_range_lift(src,1,((1,0),(0,1),(0,1),(1,0)))
        self.assertIsNone(m.full_support_obstruction())
        with self.assertRaises(ValueError):universal_block_bounds(src,1,0,0,F(1,2))
        with self.assertRaises(ValueError):block_mixed_certificate(m,0,(1,3),(1,3),2)

    def test_validation(self):
        src=iid_binary(F(1,256))
        with self.assertRaises(ValueError):finite_range_lift(src,2,((1,0),)*8)
        with self.assertRaises(ValueError):universal_block_bounds(src,2,0,0,0)
        with self.assertRaises(ValueError):rare_history_bounds(F(1,2),2,F(1,2))
        with self.assertRaises(ValueError):finite_range_lift(src,1,((2,-1),)*4)


if __name__=="__main__":unittest.main()
