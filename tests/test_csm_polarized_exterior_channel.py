"""Exact tests of channel-closed exterior-square inequalities and coupling."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"research"/"csm-001"))
from polarized_exterior_channel import (
    mixed_exterior,channel_closed_certificate,postprocess,strong_base,
    staggered_raw,coupled_model,coupled_channel,
)
from observable_exterior_square import exterior_square,anchored_certificate
from observable_memory_certificate import _rank
from marked_reset_spectral import multiply

L,R=(1,1,1,1),(1,5,5,25)


def microscopic(m,w):
    total=F(0)
    for states in product(range(m.dimension),repeat=len(w)+1):
        weight=m.pi[states[0]]
        for i,z in enumerate(w):
            weight*=m.matrices[z][states[i]][states[i+1]]
        total+=weight
    return total


class TestPolarizedExteriorChannel(unittest.TestCase):
    def test_polarization_exact_quadratic_expansion(self):
        raw=staggered_raw()
        for a,b in product(raw.matrices,repeat=2):
            self.assertEqual(mixed_exterior(a,b),mixed_exterior(b,a))
            self.assertEqual(mixed_exterior(a,a),exterior_square(a))
            s=tuple(tuple((2*x+3*y)/5 for x,y in zip(r,t)) for r,t in zip(a,b))
            A,B,C=exterior_square(a),mixed_exterior(a,b),exterior_square(b)
            expected=tuple(tuple((4*x+12*y+9*z)/25
                                 for x,y,z in zip(r,s,t)) for r,s,t in zip(A,B,C))
            self.assertEqual(exterior_square(s),expected)

    def test_all_channel_certificate(self):
        raw=staggered_raw()
        data=channel_closed_certificate(raw,0,L,R)
        self.assertEqual(data["eta"],F(1044484,16581375))
        self.assertLess(data["eta"],F(63,1000))
        self.assertEqual(data["quasi_bernoulli_lower"],F(261121,1052676))
        # Dense stochastic, deterministic coarse-graining, and single output.
        Hs=[
            tuple((F(i+1,12),F(10-i,12),F(1,12)) for i in range(9)),
            tuple(tuple(F(z==i%3) for z in range(3)) for i in range(9)),
            ((F(1),),)*9,
            coupled_channel(),
        ]
        for H in Hs:
            out=postprocess(raw,H)
            result=channel_closed_certificate(out,0,L,R)
            self.assertLessEqual(result["eta"],data["eta"])
            self.assertEqual(out.Q,raw.Q)
            self.assertEqual(out.pi,raw.pi)
            self.assertIsNone(out.full_support_obstruction())
            self.assertGreater(result["nonnull"],0)

    def test_channel_cascade(self):
        raw=staggered_raw()
        H=coupled_channel()
        G=tuple(tuple(F(z==i%3) for z in range(3)) for i in range(9))
        a=postprocess(postprocess(raw,H),G)
        b=postprocess(raw,multiply(H,G))
        self.assertEqual(a.matrices,b.matrices)

    def test_coupled_readout_is_not_independent_at_site(self):
        m=coupled_model()
        probs=[m.word_probability((i,)) for i in range(9)]
        ma=[sum(probs[3*i+j] for j in range(3)) for i in range(3)]
        mb=[sum(probs[3*i+j] for i in range(3)) for j in range(3)]
        self.assertNotEqual(probs[4],ma[1]*mb[1])
        self.assertNotEqual(probs[5],ma[1]*mb[2])
        self.assertEqual(m.minimal_linear_dimension,4)
        self.assertTrue(all(_rank(a)==4 for a in m.matrices))
        self.assertTrue(all(x>0 for row in m.Q for x in row))
        self.assertTrue(any(x==0 for row in m.matrices[0] for x in row))
        self.assertEqual(anchored_certificate(m,0,L,R)["eta"],
                         F(4467410150099971,70938546239953921))

    def test_independent_microscopic_coupled_cylinders(self):
        m=coupled_model();base=strong_base();H=coupled_channel()
        cache={}
        def bp(w):
            if w not in cache:cache[w]=microscopic(base,w)
            return cache[w]
        for n in range(4):
            for w in product(range(9),repeat=n):
                total=F(0)
                choices=[tuple(a for a in range(9) if H[a][z]>0) for z in w]
                for raw in product(*choices):
                    weight=F(1)
                    for a,z in zip(raw,w):weight*=H[a][z]
                    total+=weight*bp(tuple(x//3 for x in raw))*bp(tuple(x%3 for x in raw))
                self.assertEqual(m.word_probability(w),total)

    def test_reject_invalid_or_unused_channels(self):
        m=staggered_raw()
        for H in [((F(1),),)*8,((F(1),F(0)),)*9,((F(2),F(-1)),)*9]:
            with self.assertRaises(ValueError):postprocess(m,H)


if __name__=="__main__":unittest.main()
