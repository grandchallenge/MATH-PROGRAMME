"""Independent exact finite checks for CSM-01-WP01 typed factor networks."""
import sys
import unittest
from fractions import Fraction
from itertools import product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "csm-001"))
from finite_semantics import compose, identity, matrix, tensor
from open_networks import (
    Factor, Network, copy_network, delete_network, glue,
    identity_network, star_network, swap_network, tensor_network,
)

B = (0, 1)


def wire(weights):
    return Network((("x", B), ("y", B)), ("x",), ("y",),
                   (Factor.make(("x", "y"), {
                       (i, j): weights[j][i] for i, j in product(B, repeat=2)
                   }),))


class TestOpenNetworks(unittest.TestCase):
    def test_matrix_composition_and_associativity(self):
        a = wire(((2, 1), (1, 2)))
        b = wire(((1, 3), (2, 4)))
        c = wire(((0, 1), (5, 2)))
        self.assertEqual(a.evaluate(), matrix([[2, 1], [1, 2]]))
        self.assertEqual(glue(a, b).evaluate(), compose(b.evaluate(), a.evaluate()))
        self.assertEqual(glue(glue(a, b), c).evaluate(),
                         glue(a, glue(b, c)).evaluate())
        self.assertEqual(glue(a, identity_network((B,))).evaluate(), a.evaluate())
        self.assertEqual(glue(identity_network((B,)), a).evaluate(), a.evaluate())

    def test_tensor_interchange_and_swap(self):
        a, b, c, d = [wire(w) for w in (
            ((1, 2), (3, 4)), ((2, 0), (1, 1)),
            ((0, 3), (2, 1)), ((4, 1), (0, 2)))]
        self.assertEqual(tensor_network(a, b).evaluate(), tensor(a.evaluate(), b.evaluate()))
        self.assertEqual(
            glue(tensor_network(a, b), tensor_network(c, d)).evaluate(),
            tensor(compose(c.evaluate(), a.evaluate()),
                   compose(d.evaluate(), b.evaluate())))
        self.assertEqual(swap_network(B, B).evaluate(), matrix([
            [1 if y == (x[1], x[0]) else 0
             for x in product(B, repeat=2)]
            for y in product(B, repeat=2)]))

    def test_copy_delete_counits(self):
        cp = copy_network(B)
        de = delete_network(B)
        self.assertEqual(cp.evaluate(), matrix([
            [int(y[0] == y[1] == x) for x in B]
            for y in product(B, repeat=2)]))
        self.assertEqual(glue(cp, tensor_network(de, identity_network((B,)))).evaluate(),
                         identity(2))
        self.assertEqual(glue(cp, tensor_network(identity_network((B,)), de)).evaluate(),
                         identity(2))
        self.assertEqual(
            glue(cp, tensor_network(cp, identity_network((B,)))).evaluate(),
            glue(cp, tensor_network(identity_network((B,)), cp)).evaluate())

    def test_star_exact_and_three_body_obstruction(self):
        result = star_network().evaluate()
        independent = []
        for abc in product(B, repeat=3):
            independent.append(sum(
                (2 if u else 1) *
                (2 if u == abc[0] else 1) *
                (2 if u == abc[1] else 1) *
                (2 if u == abc[2] else 1)
                for u in B))
        self.assertEqual([row[0] for row in result], independent)
        self.assertEqual(independent, [10, 8, 8, 10, 8, 10, 10, 17])
        even = odd = 1
        for abc, w in zip(product(B, repeat=3), independent):
            if sum(abc) % 2:
                odd *= w
            else:
                even *= w
        self.assertEqual((even, odd), (10000, 8704))
        self.assertNotEqual(even, odd)

    def test_closed_scalar_and_empty_boundary(self):
        net = Network((("x", B),), (), (),
                      (Factor.make(("x",), {(0,): Fraction(1, 2), (1,): 2}),))
        self.assertEqual(net.evaluate(), matrix([[Fraction(5, 2)]]))
        self.assertEqual(identity_network(()).evaluate(), matrix([[1]]))

    def test_reject_invalid_factors_and_boundary_types(self):
        with self.assertRaises(ValueError):
            glue(wire(((1, 0), (0, 1))), identity_network(((0, 1, 2),)))
        with self.assertRaises(ValueError):
            Network((("x", B),), ("x",), ("x",),
                    (Factor.make(("x",), {(0,): 1}),))
        with self.assertRaises(ValueError):
            Factor.make(("x",), {(0,): -1})
        with self.assertRaises(ValueError):
            Network((("x", B),), ("x", "x"), ())


if __name__ == "__main__":
    unittest.main()
