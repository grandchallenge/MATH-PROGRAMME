"""Exact rational tests of WP07 no-reset factorization."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from observable_exterior_square import (
    nonreset_model, persistent_nonreset_model, staggered_composition,
    word_matrix, exterior_square, exterior_norm, anchored_certificate,
    defect_bound, conditional_defect, normalized_basis_defect,
    product_defect_bound,
)
from observable_memory_certificate import _rank
from marked_reset_spectral import multiply


def microscopic(model, word):
    return sum((model.pi[s[0]] *
                prod(model.matrices[z][s[i]][s[i+1]]
                     for i,z in enumerate(word))
                for s in product(range(model.dimension),repeat=len(word)+1)),F(0))


def prod(values):
    r=F(1)
    for x in values:r*=x
    return r


class TestObservableExteriorSquare(unittest.TestCase):
    def test_exact_anchor_certificate(self):
        m=nonreset_model()
        d=anchored_certificate(m,0,(1,1),(1,10))
        self.assertEqual(d["eta"],F(2,3))
        self.assertEqual(d["quasi_bernoulli_lower"],F(11,40))
        self.assertEqual(d["constant"],176)
        self.assertGreater(d["nonnull"],0)
        self.assertEqual(m.minimal_linear_dimension,2)
        self.assertTrue(all(x>0 for row in m.Q for x in row))
        self.assertTrue(all(any(x==0 for row in a for x in row) for a in m.matrices))
        for a in m.matrices:self.assertEqual(_rank(a),2)
        self.assertEqual(exterior_norm(word_matrix(m,(0,)*12)),F(1,16)**12)

    def test_all_word_bounds_and_minor_identity(self):
        m=nonreset_model()
        data=anchored_certificate(m,0,(1,1),(1,10))
        b=data["quasi_bernoulli_lower"]
        for n in range(5):
            for w in product(range(3),repeat=n):
                a=word_matrix(m,w)
                self.assertLessEqual(exterior_norm(a)/a[0][0]**2,F(2,3)**n)
                for u,v in product(((),(0,),(1,),(2,),(1,2)),repeat=2):
                    self.assertGreaterEqual(m.word_probability(u+w),
                                            b*m.word_probability(u)*m.word_probability(w))
                    e=conditional_defect(m,u,w,v)
                    self.assertLessEqual(abs(e),defect_bound(data,n))
                    p=m.word_probability
                    # In dimension two the anchored minor factors into three determinants.
                    l=m.pi
                    for z in u:l=m._left_step(l,z)
                    r=m.message(v)
                    determinant=(l[0]*m.pi[1]-l[1]*m.pi[0])*exterior_square(a)[0][0]*(r[0]-r[1])
                    self.assertEqual(determinant,p(u+w+v)*p(w)-p(u+w)*p(w+v))
                self.assertLessEqual(normalized_basis_defect(m,w),defect_bound(data,n)/min(m.pi)**2)

    def test_block_certificate_and_fail_closed(self):
        m=nonreset_model()
        data=anchored_certificate(m,0,(1,1),(1,10),block=2)
        self.assertEqual(data["eta"],F(4,9))
        for n in range(6):
            for w in product(range(3),repeat=n):
                self.assertLessEqual(abs(conditional_defect(m,(1,),w,(2,))),
                                     defect_bound(data,n))
        for L,R in [((1,0),(1,10)),((1,1),(1,1)),((1,-1),(1,10))]:
            with self.assertRaises(ValueError):anchored_certificate(m,0,L,R)
        with self.assertRaises(ValueError):anchored_certificate(m,1,(1,1),(1,1))

    def test_exterior_square_multiplicative(self):
        m=staggered_composition(nonreset_model())
        for i,j in product(range(m.alphabet),repeat=2):
            a,b=m.matrices[i],m.matrices[j]
            self.assertEqual(exterior_square(multiply(a,b)),
                             multiply(exterior_square(a),exterior_square(b)))

    def test_staggered_overlapping_composition(self):
        base=nonreset_model()
        m=staggered_composition(base)
        self.assertEqual(m.minimal_linear_dimension,4)
        self.assertTrue(all(_rank(a)==4 for a in m.matrices))
        self.assertTrue(all(x>0 for row in m.Q for x in row))
        for n in range(4):
            for w in product(range(9),repeat=n):
                a=tuple(z//3 for z in w)
                b=tuple((z%3-z//3)%3 for z in w)
                self.assertEqual(m.word_probability(w),
                                 microscopic(base,a)*microscopic(base,b))
        data=anchored_certificate(base,0,(1,1),(1,10))
        for n in range(3):
            for w in product(range(9),repeat=n):
                for i,j in product(range(9),repeat=2):
                    self.assertLessEqual(abs(conditional_defect(m,(i,),w,(j,))),
                                         product_defect_bound(defect_bound(data,n)))

    def test_irreducible_no_reset_hostile_control(self):
        m=persistent_nonreset_model()
        self.assertEqual(m.minimal_linear_dimension,2)
        self.assertTrue(all(_rank(a)==2 for a in m.matrices))
        self.assertTrue(all(x>0 for row in m.Q for x in row))
        # The anchor certificate fails because A is a scalar identity.
        with self.assertRaisesRegex(ValueError,"block contraction"):
            anchored_certificate(m,0,(1,3),(1,3))
        for n in range(8):
            self.assertEqual(conditional_defect(m,(1,),(0,)*n,(1,)),F(1,18))
            # Direct two-sided conditional ratios on matching zero neighborhoods.
            qs=[]
            for marker in (1,2):
                masses=[m.word_probability((marker,)+(0,)*n+(a,)+(0,)*n+(marker,))
                        for a in range(3)]
                qs.append(tuple(x/sum(masses) for x in masses))
            self.assertNotEqual(qs[0],qs[1])

if __name__=="__main__":unittest.main()
