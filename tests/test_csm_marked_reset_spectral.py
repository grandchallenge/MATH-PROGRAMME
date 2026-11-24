"""Exact replay of the WP06 spectral classification and cylinder odds."""
import sys
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from marked_reset_spectral import examples, identity, MarkedReset, power, positive
from observable_memory_certificate import ObservableFiniteMemory


def stationary_two(q):
    t=q[0][1]+q[1][0]
    return q[1][0]/t,q[0][1]/t


class TestMarkedResetSpectral(unittest.TestCase):
    def test_four_exact_spectral_certificates(self):
        expected={"diagonal":"gibbs_exponential","rank":"rank_continuity_obstruction",
                  "jordan":"polynomial_nonnull_obstruction",
                  "periodic":"periodic_continuity_obstruction"}
        for name,(m,lam,p,E) in examples().items():
            self.assertTrue(positive(m.q))
            self.assertEqual(m.classify(lam,p,E)["outcome"],expected[name])
            self.assertFalse(positive(power(m.a,20)))

    def test_independent_transfer_cylinder_odds(self):
        for m,_,_,_ in examples().values():
            model=ObservableFiniteMemory(stationary_two(m.q),m.transfers)
            self.assertIsNone(model.full_support_obstruction())
            for left,right in product(range(4),repeat=2):
                for i,j in product(range(m.markers),repeat=2):
                    words=[(i+1,)+(0,)*left+(a,)+(0,)*right+(j+1,)
                           for a in range(m.markers+1)]
                    mass=[model.word_probability(w) for w in words]
                    self.assertEqual(m.conditional(left,right,i,j),
                                     tuple(x/sum(mass) for x in mass))

    def test_positive_gap_limit_and_infinite_memory(self):
        m,lam,p,E=examples()["diagonal"]
        result=m.classify(lam,p,E)
        self.assertEqual(result["activities"],(F(1,2),F(1,12)))
        C=result["residues"][0]
        for n in range(10):
            gap=m.gap(n)
            for i,j in product(range(m.markers),repeat=2):
                # The remaining second diagonal contribution is exact.
                self.assertEqual(gap[i][j]/lam**n-C[i][j],
                                 m.v[i][1]*m.u[1][j]*F(1,2)**n)
        # For every k, conditioning on k zeros then a reset retains
        # dependence on the type of that reset. This follows from
        # unequal ratios of columns of the two rank-two U,V matrices.
        model=ObservableFiniteMemory(stationary_two(m.q),m.transfers)
        for k in range(8):
            self.assertEqual(model.check_reverse_order(k)["outcome"],"counterexample")

    def test_rank_obstruction_has_pure_exponential_gap_weights(self):
        m,lam,p,E=examples()["rank"]
        result=m.classify(lam,p,E)
        C=result["residues"][0]
        self.assertEqual(C,((F(7,32),F(5,32)),(F(5,32),F(7,32))))
        self.assertEqual(C[0][0]*C[1][1]-C[0][1]*C[1][0],F(3,128))
        for n in range(6):
            self.assertEqual(m.gap(n),tuple(tuple(x*lam**n for x in row) for row in C))
            self.assertEqual(m.odds(n,n,0,0,0),F(7,20))
            self.assertEqual(m.odds(n,n,1,1,0),F(5,28))
            self.assertNotEqual(m.conditional(n,n,0,0),m.conditional(n,n,1,1))

    def test_jordan_nonnull_failure(self):
        m,lam,p,E=examples()["jordan"]
        self.assertEqual(m.classify(lam,p,E)["degree"],1)
        for n in range(8):
            self.assertEqual(m.gap(n)[0][0],lam**n*(F(5,8)+F(3,8)*n))
        self.assertLess(m.conditional(100,100,0,0)[0],F(1,50))

    def test_periodic_discontinuity(self):
        m,lam,p,E=examples()["periodic"]
        C0,C1=m.classify(lam,p,E)["residues"]
        self.assertNotEqual(C0,C1)
        self.assertEqual(m.odds(20,20,0,0,0),m.odds(22,22,0,0,0))
        self.assertNotEqual(m.odds(20,20,0,0,0),m.odds(21,21,0,0,0))

    def test_reject_false_spectral_splittings(self):
        m,lam,p,E=examples()["diagonal"]
        with self.assertRaises(ValueError):
            m.classify(lam,p,identity(2))
        with self.assertRaises(ValueError):
            m.classify(F(1,4),p,((0,0),(0,1)))
        with self.assertRaises(ValueError):
            m.classify(lam,p,((1,1),(0,0)))
        with self.assertRaises(ValueError):
            examples()["periodic"][0].classify(F(3,8),1,identity(2))
        with self.assertRaises(ValueError):
            MarkedReset(((F(1,2),0),(0,F(1,4))),((0,),(F(3,4),)),((F(1,2),F(1,2)),))


if __name__ == "__main__":
    unittest.main()
