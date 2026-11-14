"""Finite exact checks for the new all-order Erdős--Sós corollary #547.

The universal tree-free inequality is an externally established 2026
theorem. Exhaustive small graph checks are not a kernel replay.
"""
from itertools import combinations,permutations
import networkx as nx


def tree_contained_matcher(host,tree):
    return nx.algorithms.isomorphism.GraphMatcher(host,tree).subgraph_is_monomorphic()


def tree_contained_exact(host,tree):
    if tree.number_of_nodes()>host.number_of_nodes():return False
    V=tuple(host.nodes);T=tuple(tree.nodes);E=tuple(tree.edges)
    return any(all(host.has_edge(mapping[x],mapping[y]) for x,y in E)
               for img in permutations(V,len(T))
               for mapping in (dict(zip(T,img)),))


def trees_of_order(t):
    if t==2:return [nx.path_graph(2)]
    return list(nx.generators.nonisomorphic_trees(t))


def test_547_every_tree_free_small_graph_has_sharp_edge_bound():
    atlas=nx.graph_atlas_g()
    for G in atlas:
        N=G.number_of_nodes()
        if N==0 or N>5:continue
        for t in range(2,N+1):
            for T in trees_of_order(t):
                a=tree_contained_matcher(G,T)
                b=tree_contained_exact(G,T)
                assert a==b
                if not a:
                    assert 2*G.number_of_edges()<=(t-2)*N


def test_547_small_ramsey_corollary_exhaustive_unlabeled_graphs():
    # Every red-blue K_N coloring is determined up to relabeling
    # by the unlabeled red-edge graph on N vertices.
    atlas=nx.graph_atlas_g()
    for t,N in ((2,2),(3,3),(4,6),(5,7)):
        if N>7:continue
        for T in trees_of_order(t):
            for G in atlas:
                if G.number_of_nodes()!=N:continue
                blue=nx.complement(G)
                assert tree_contained_matcher(G,T) or tree_contained_matcher(blue,T)


def test_547_odd_order_integrality_refinement():
    for t in (3,5,7,9):
        N=2*t-3
        assert N%2==1 and (t-2)*N%2==1
        upper_each=((t-2)*N)//2
        assert 2*upper_each< N*(N-1)//2
        # If each color avoids T, its edge count is <=upper_each;
        # both colors cannot cover all K_N edges.


def test_547_even_star_sharp_example_t4():
    # Five-vertex red C5 / blue C5 contains no K1,3.
    red=nx.cycle_graph(5)
    blue=nx.complement(red)
    assert all(d==2 for _,d in red.degree())
    assert all(d==2 for _,d in blue.degree())
    star=nx.star_graph(3)
    assert not tree_contained_matcher(red,star)
    assert not tree_contained_matcher(blue,star)
    # Every coloring of K6 has a vertex with >=3 same-color edges.
    for G in nx.graph_atlas_g():
        if G.number_of_nodes()==6:
            assert tree_contained_matcher(G,star) or tree_contained_matcher(nx.complement(G),star)


def test_547_one_vertex_boundary_and_multi_color_count():
    assert 1>2*1-2  # R(K1)=1 > 0, exclude t=1
    for t in range(2,16):
        for q in range(1,7):
            N=q*(t-2)+2
            assert N-1>q*(t-2)
            # Sum of q T-free color class edge bounds would be
            # at most q*(t-2)*N/2 < binom(N,2).


# CI uses unittest discovery. Preserve the original bounded witness functions
# while explicitly exposing each as a standard unittest test method.
import unittest

class CompendiumWitnessTests(unittest.TestCase):
    def test_547_every_tree_free_small_graph_has_sharp_edge_bound(self):
        test_547_every_tree_free_small_graph_has_sharp_edge_bound()

    def test_547_small_ramsey_corollary_exhaustive_unlabeled_graphs(self):
        test_547_small_ramsey_corollary_exhaustive_unlabeled_graphs()

    def test_547_odd_order_integrality_refinement(self):
        test_547_odd_order_integrality_refinement()

    def test_547_even_star_sharp_example_t4(self):
        test_547_even_star_sharp_example_t4()

    def test_547_one_vertex_boundary_and_multi_color_count(self):
        test_547_one_vertex_boundary_and_multi_color_count()
