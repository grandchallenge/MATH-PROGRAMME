"""Finite exact regression for the CSM XOR support-only Gibbs no-go corollary.

Tests compute support invariance and conflicting finite boundary behavior;
the infinite-volume conclusion rests on the separately written proof.
"""
import sys
import unittest
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from xor_block_obstruction import cylinder_probability, exterior_conditional


def labelled_matrices(p):
    p = Q(p)
    if not 0 < p < 1:
        raise ValueError("p must be strictly between zero and one")
    return (((1-p, Q(0)), (Q(0), p)), ((Q(0), p), (1-p, Q(0))))


def transfer_cylinder(word, p):
    matrices = labelled_matrices(p)
    row = (1-Q(p), Q(p))
    for z in word:
        matrix = matrices[z]
        prior = row
        row = tuple(sum(prior[i]*matrix[i][j] for i in (0,1))
                    for j in (0,1))
    return sum(row)


class TestSupportOnlyGibbsNoGo(unittest.TestCase):
    def test_generators_have_identical_support_for_opposite_regimes(self):
        support = None
        for p in (Q(1,3), Q(1,2), Q(3,4), Q(9,10)):
            matrices = labelled_matrices(p)
            signs = tuple(tuple(tuple(int(x>0) for x in row) for row in m)
                          for m in matrices)
            if support is None:
                support = signs
            self.assertEqual(signs, support)
        self.assertEqual(support, (((1,0),(0,1)),((0,1),(1,0))))

    def test_supports_of_all_products_are_identical(self):
        for word_len in range(1,7):
            for word in product((0,1), repeat=word_len):
                supported = None
                for p in (Q(1,2), Q(3,4)):
                    matrices = labelled_matrices(p)
                    a = ((Q(1),Q(0)),(Q(0),Q(1)))
                    for z in word:
                        b=matrices[z]
                        a = tuple(tuple(sum(a[i][k]*b[k][j] for k in (0,1))
                                        for j in (0,1)) for i in (0,1))
                    pattern = tuple(tuple(int(a[i][j]>0) for j in (0,1))
                                    for i in (0,1))
                    if supported is None: supported=pattern
                    self.assertEqual(pattern,supported)

    def test_transfer_probabilities_equal_independent_xor_enumeration(self):
        for p in (Q(1,2),Q(3,4)):
            for n in range(0,7):
                for word in product((0,1),repeat=n):
                    self.assertEqual(transfer_cylinder(word,p),
                                     cylinder_probability(word,p))

    def test_identical_support_does_not_fix_boundary_conditionals(self):
        self.assertEqual(exterior_conditional(3,3,10,Q(1,2)),Q(1,2))
        self.assertEqual(exterior_conditional(3,4,10,Q(1,2)),Q(1,2))
        self.assertLess(exterior_conditional(3,3,10,Q(3,4)),Q(1,1000))
        self.assertGreater(exterior_conditional(3,4,10,Q(3,4)),Q(999,1000))


if __name__ == "__main__":
    unittest.main()
