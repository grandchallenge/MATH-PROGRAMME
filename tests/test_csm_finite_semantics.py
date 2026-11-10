"""Independent finite regression examples for CSM-001."""
import sys
import unittest
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from finite_semantics import (
    matrix, identity, compose, tensor, trace, power, ising_transfer,
    ising_partition_transfer, ising_partition_enumeration, pushforward,
)


class TestFiniteCategoricalSpecimen(unittest.TestCase):
    def test_identity_associativity(self):
        a = matrix([[1, 2], [3, 4]])
        b = matrix([[0, 1], [1, 0]])
        c = matrix([[1, 0], [2, 1]])
        self.assertEqual(compose(identity(2), a), a)
        self.assertEqual(compose(a, identity(2)), a)
        self.assertEqual(compose(c, compose(b, a)), compose(compose(c, b), a))

    def test_nonsquare_composition(self):
        a = matrix([[1, 2], [3, 4], [5, 6]])  # 2 -> 3
        b = matrix([[2, 0, 1]])  # 3 -> 1
        self.assertEqual(compose(b, a), matrix([[7, 10]]))

    def test_tensor(self):
        a = matrix([[1, 2], [3, 4]])
        b = matrix([[1, 0], [0, 2]])
        self.assertEqual(tensor(a, b), matrix([
            [1, 0, 2, 0],
            [0, 2, 0, 4],
            [3, 0, 4, 0],
            [0, 6, 0, 8],
        ]))

    def test_ising_against_independent_enumeration(self):
        for n in range(1, 9):
            with self.subTest(n=n):
                got = ising_partition_transfer(n)
                self.assertEqual(got, ising_partition_enumeration(n))
                self.assertEqual(got, 3 ** n + 1)

    def test_ising_general_rational_bonds(self):
        a, b = Fraction(3, 2), Fraction(1, 2)
        for n in range(1, 7):
            self.assertEqual(
                ising_partition_transfer(n, a, b),
                ising_partition_enumeration(n, a, b),
            )
            self.assertEqual(ising_partition_transfer(n, a, b), 2 ** n + 1)

    def test_total_weight_and_composable_coarse_graining(self):
        w = {"a": 2, "b": 3, "c": Fraction(1, 2), "d": 1}
        c = {"a": "left", "b": "left", "c": "right", "d": "right"}
        d = {"left": "all", "right": "all"}
        q = pushforward(w, c)
        self.assertEqual(q, {"left": 5, "right": Fraction(3, 2)})
        self.assertEqual(sum(q.values()), sum(w.values()))
        self.assertEqual(pushforward(q, d), pushforward(w, {x: "all" for x in w}))

    def test_validation(self):
        with self.assertRaises(ValueError):
            matrix([[1], [1, 2]])
        with self.assertRaises(ValueError):
            matrix([[1, -1]])
        with self.assertRaises(ValueError):
            compose(matrix([[1, 2]]), matrix([[1]]))
        with self.assertRaises(ValueError):
            pushforward({"a": 1}, {})
        with self.assertRaises(ValueError):
            ising_partition_transfer(0)


if __name__ == "__main__":
    unittest.main()
