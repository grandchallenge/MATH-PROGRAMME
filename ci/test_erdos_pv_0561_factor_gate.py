#!/usr/bin/env python3
"""Two genuinely independent methods: cut obstruction versus direct edge 2-colouring.

This is a finite regression and role-scoped adversarial test, NOT formal
certification of a general graph-factor theorem or the full star-forest result.
"""
import itertools
import random
import unittest

from erdos_pv_0561_factor_gate import (
    Graph, all_graphs, cut_certificate, cut_condition, cuts,
    explicit_partition, weighted_cut_inequality,
)


def construct_reduced_example(a: int) -> tuple[Graph, tuple[tuple[int, int], ...]]:
    """a >= 3; n=(2a+1,a+1,1), alpha=a-1, beta=2a, rho=2, k=1.

    Construct an edge-disjoint decomposition into alpha matchings
    (one may be empty), three vertex-disjoint stars, and 1 residual edge.
    The unique vertex of degree D=3a-1 is a star center.
    """
    if a < 3:
        raise ValueError("a must be >=3")
    sizes = (2*a + 1, a + 1, 1)
    e = []
    centers = []
    leaves = []
    v = 0
    for n in sizes:
        c = v
        v += 1
        part = list(range(v, v+n))
        v += n
        centers.append(c)
        leaves.append(part)
        e.extend((c, leaf) for leaf in part)
    # alpha=a-1 matchings, with a-2 nonempty and one empty, all edge-disjoint.
    matchings = [((centers[0], leaves[1][i]),) for i in range(a-2)]
    matchings.append(())
    for M in matchings:
        e.extend(M)
    residual = ((leaves[0][1], leaves[2][0]),)
    e.extend(residual)
    g = Graph(v, tuple(sorted(e)))
    alpha, beta = a-1, sizes[0]-1
    assert max(g.degrees) == alpha+beta == 3*a-1
    assert all(u == centers[0] for u, d in enumerate(g.degrees) if d == alpha+beta)
    assert len(residual) == 1 <= beta-1
    # Direct constructive edge partition: assign alpha matchings plus one
    # first-star edge to J; K is all remaining edges, max degree beta.
    j = {edge for M in matchings for edge in M}
    j.add((centers[0], leaves[0][0]))
    degJ = [0]*g.n
    degK = [0]*g.n
    for edge in g.edges:
        ds = degJ if edge in j else degK
        ds[edge[0]] += 1
        ds[edge[1]] += 1
    assert max(degJ) <= alpha and max(degK) <= beta
    return g, tuple(sorted(j))


class SourceFactorGateTests(unittest.TestCase):
    def test_lovasz_cut_criterion_vs_independent_edge_partition_all_graphs_0_to_4(self):
        count = 0
        for n in range(5):
            for g in all_graphs(n):
                for alpha, beta in itertools.product(range(1,4), repeat=2):
                    if max(g.degrees, default=0) > alpha+beta:
                        continue
                    cuts_pass, failing_cut = cut_condition(g, alpha, beta)
                    direct, coloring = explicit_partition(g, alpha, beta)
                    self.assertEqual(cuts_pass, direct,
                        (n, g.edges, alpha, beta, failing_cut))
                    self.assertTrue(weighted_cut_inequality(g, alpha, beta))
                    if direct:
                        self.assertIsNotNone(coloring)
                    else:
                        self.assertIsNotNone(failing_cut)
                        S, T, certificate = failing_cut
                        self.assertLess(certificate['A'], certificate['q_D'])
                    count += 1
        self.assertGreater(count, 600)

    def test_five_vertex_degree_two_scope_and_seeded_broader_graphs(self):
        count = 0
        for g in all_graphs(5):
            if max(g.degrees) <= 2:
                self.assertEqual(cut_condition(g, 1, 1)[0],
                                 explicit_partition(g, 1, 1)[0])
                count += 1
        self.assertGreater(count, 100)
        rng = random.Random(5612026)
        for _ in range(90):
            edges = tuple((u,v) for u in range(5) for v in range(u+1,5)
                          if rng.randrange(2))
            g = Graph(5, edges)
            alpha, beta = rng.choice(((1,3),(2,2),(2,3),(3,1),(3,2)))
            if max(g.degrees) <= alpha+beta:
                self.assertEqual(cut_condition(g, alpha, beta)[0],
                                 explicit_partition(g, alpha, beta)[0])

    def test_hostile_odd_regular_parity_and_boundary_term(self):
        for n, alpha, beta in ((3,1,1),(5,1,3)):
            g = Graph(n, tuple((u,v) for u in range(n) for v in range(u+1,n)))
            ok, cut = cut_condition(g, alpha, beta)
            self.assertFalse(ok)
            self.assertFalse(explicit_partition(g, alpha, beta)[0])
            self.assertEqual(cut[0:2], ((), ()))
            self.assertEqual(cut[2]['A'], 0)
            self.assertEqual(cut[2]['q_D'], 1)
        triangle = Graph(3, ((0,1),(0,2),(1,2)))
        c = cut_certificate(triangle,1,1,frozenset((2,)),frozenset((1,)))
        self.assertEqual(c['q_D'],0) # alpha|C| + e(C,T) is even
        self.assertEqual(c['A'],1)
        with self.assertRaises(ValueError):
            cut_certificate(triangle,0,2,frozenset(),frozenset())
        with self.assertRaises(ValueError):
            cut_certificate(triangle,1,1,frozenset((1,)),frozenset((1,)))

    def test_missing_star_center_hypothesis_is_not_safe_even_at_paper_budgets(self):
        # alpha=3 (a=4), beta=9 (>= 2a), D=12. K13 is 12-regular
        # on an odd number of vertices. A feasible partition would force
        # d_J(v)=3 at every vertex, impossible by the handshaking lemma.
        # Star-center localization excludes this counterexample:
        # 13 degree-D centers need >=26 distinct star vertices.
        g=Graph(13,tuple((u,v) for u in range(13) for v in range(u+1,13)))
        c=cut_certificate(g,3,9,frozenset(),frozenset())
        self.assertEqual(c['A'],0)
        self.assertEqual(c['q_D'],1)
        self.assertEqual(c['counted_components'],(tuple(range(13)),))
        self.assertEqual(g.degrees,(12,)*13)
        self.assertEqual(13*3%2,1)

    def test_integral_small_and_large_component_contradiction_all_budgets(self):
        # A proof-sanity regression over integer parameters, not a proof
        # that the prerequisite graph-theoretic reductions hold.
        checks = 0
        for alpha in range(2,13):
            for beta in range(2*(alpha+1), 35):
                D = alpha+beta
                self.assertGreater(alpha*beta, D) # D/alpha < beta
                self.assertGreaterEqual(beta, alpha)
                for r in range(1,60):
                    # All counted components small: each contributes >=D.
                    self.assertGreater(alpha*r*D, D*(r-1))
                    # At least one large component, e(R)<=beta-1.
                    self.assertGreater(beta*(D+r-2)+2, beta*(r-1))
                    self.assertGreater(alpha*(beta*(D+r-2)+2), D*(r-1))
                    checks += 1
        self.assertGreater(checks, 8000)

    def test_constructed_reduced_hypotheses_positive_and_wrong_center_control(self):
        rng = random.Random(20261117)
        for a in range(3,7):
            g, j = construct_reduced_example(a)
            alpha, beta = a-1, 2*a
            # All omitted high-degree center hypothesis tests are explicit in
            # constructor; 3^n cannot be exhaustively checked when n>15.
            for S,T in itertools.islice(cuts(g.n), 40):
                c=cut_certificate(g,alpha,beta,S,T)
                self.assertGreaterEqual(c['A'],c['q_D'])
            for _ in range(3000):
                labels=[rng.randrange(3) for _ in range(g.n)]
                S=frozenset(i for i,x in enumerate(labels) if x==1)
                T=frozenset(i for i,x in enumerate(labels) if x==2)
                c=cut_certificate(g,alpha,beta,S,T)
                self.assertGreaterEqual(c['A'],c['q_D'])
                self.assertGreaterEqual(c['q_gf'],0)
                self.assertEqual(c['q_D'],c['q_gf'])
                self.assertGreaterEqual((alpha+beta)*c['A'],c['weighted'])
            self.assertEqual(max(g.degrees),alpha+beta)
            self.assertEqual(len(j),a-1)


if __name__ == '__main__':
    unittest.main()
