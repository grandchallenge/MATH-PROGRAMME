"""Bounded source semantics for OPEN Erdős #544.

No finite list of R(3,k) settles either limit on successive gaps.
"""
from itertools import combinations
import networkx as nx


def triangle_free(G):
    return not any(G.has_edge(a,b) and G.has_edge(a,c) and G.has_edge(b,c)
                   for a,b,c in combinations(G.nodes,3))


def independence_bruteforce(G):
    vertices=tuple(G.nodes)
    return max(k for k in range(len(vertices)+1)
               if any(all(not G.has_edge(a,b) for a,b in combinations(S,2))
                      for S in combinations(vertices,k)))


def independence_via_clique(G):
    return max((len(x) for x in nx.find_cliques(nx.complement(G))),default=0)


def mobius_ladder_eight():
    G=nx.cycle_graph(8)
    G.add_edges_from((i,i+4) for i in range(4))
    return G


def test_544_independence_methods_graph_atlas():
    for G in nx.graph_atlas_g():
        if G.number_of_nodes()<=7:
            assert independence_bruteforce(G)==independence_via_clique(G)


def test_544_classical_r33_six_vertices_exact():
    C5=nx.cycle_graph(5)
    assert triangle_free(C5)
    assert independence_bruteforce(C5)==2
    for G in nx.graph_atlas_g():
        if G.number_of_nodes()==6:
            assert (not triangle_free(G)) or independence_bruteforce(G)>=3
    # Graph atlas contains all unlabeled graphs on six vertices:
    # hence this tests R(3,3)=6 exhaustively in that size.


def test_544_eight_vertex_lower_witness_r34():
    M=mobius_ladder_eight()
    assert M.number_of_nodes()==8 and M.number_of_edges()==12
    assert triangle_free(M)
    assert independence_bruteforce(M)==3
    assert independence_via_clique(M)==3
    # The known UPPER R(3,4)<=9 is external literature, not
    # established by only this eight-vertex witness.


def test_544_finite_documented_ramsey_differences():
    known={2:3,3:6,4:9,5:14,6:18,7:23,8:28,9:36}
    gaps=[known[k+1]-known[k] for k in range(2,9)]
    assert gaps==[3,3,5,4,5,5,8]
    assert all(1<=known[k+1]-known[k]<=k+1 for k in range(2,9))
    assert known[3]==6 and known[4]==9
    # R(3,k) values k>=4 are SOURCE-ATTRIBUTED numerical facts,
    # not all independently re-proved by this fixture.


# CI uses unittest discovery. Preserve the original bounded witness functions
# while explicitly exposing each as a standard unittest test method.
import unittest

class CompendiumWitnessTests(unittest.TestCase):
    def test_544_independence_methods_graph_atlas(self):
        test_544_independence_methods_graph_atlas()

    def test_544_classical_r33_six_vertices_exact(self):
        test_544_classical_r33_six_vertices_exact()

    def test_544_eight_vertex_lower_witness_r34(self):
        test_544_eight_vertex_lower_witness_r34()

    def test_544_finite_documented_ramsey_differences(self):
        test_544_finite_documented_ramsey_differences()
